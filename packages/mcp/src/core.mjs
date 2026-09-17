import { readFileSync } from "node:fs";

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

export const DEFAULT_PUBLICATION_URL = "https://alreadyopen.github.io/ai-output-to-value/";

const claimSchema = JSON.parse(
  readFileSync(new URL("../../../schemas/v1/claim.schema.json", import.meta.url), "utf8")
);
const bundledGates = JSON.parse(
  readFileSync(new URL("../../../schemas/v1/decision-gates.json", import.meta.url), "utf8")
);
const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);
const validateClaim = ajv.compile(claimSchema);

export async function fetchJson(baseUrl, path) {
  const url = new URL(path, baseUrl).href;
  const response = await fetch(url, { headers: { accept: "application/json" } });
  if (!response.ok) throw new Error(`${url} returned HTTP ${response.status}`);
  return response.json();
}

export function loadBundledGates() {
  return bundledGates;
}

const REQUIRED_TEXT_FIELDS = ["project", "intendedUse", "authority", "accountability", "nextEvidence", "stopRule"];

function schemaErrors(record) {
  validateClaim(record);
  return (validateClaim.errors ?? []).map((error) => {
    const location = error.instancePath ? error.instancePath.replace(/^\//, "") : "<root>";
    return `claim.schema.json ${location}: ${error.message}`;
  });
}

function resultMetadata(gates) {
  const principle = gates?.principle ?? null;
  return {
    gateVersion: gates?.version ?? null,
    principle,
    rule: principle
  };
}

export function evaluateClaim(record, gates) {
  const decisionId = record?.targetDecision;
  const rule = typeof decisionId === "string" ? gates?.decisions?.[decisionId] : undefined;
  const structuralErrors = schemaErrors(record);
  const missingFields = [];

  if (!rule) {
    structuralErrors.push(`unknown targetDecision: ${JSON.stringify(decisionId)}`);
    return {
      status: "BLOCKED",
      targetDecision: decisionId ?? null,
      errors: structuralErrors,
      structuralErrors,
      missingFields,
      claimMismatch: false,
      failedChecks: [],
      unknownChecks: [],
      passedChecks: [],
      ...resultMetadata(gates)
    };
  }

  if (record?.requiredClaimLevel !== rule.requiredClaimLevel) {
    const message = `requiredClaimLevel must be ${rule.requiredClaimLevel} for ${decisionId}`;
    if (!structuralErrors.includes(message)) structuralErrors.push(message);
  }

  for (const field of REQUIRED_TEXT_FIELDS) {
    if (typeof record?.[field] === "string" && !record[field].trim()) missingFields.push(field);
  }
  if (Array.isArray(record?.actors) && record.actors.length === 0) missingFields.push("actors");

  const claimMismatch = record?.assertedClaimLevel !== rule.requiredClaimLevel;
  const checks = record?.gateChecks && typeof record.gateChecks === "object" && !Array.isArray(record.gateChecks)
    ? record.gateChecks
    : {};
  const failedChecks = [];
  const unknownChecks = [];
  const passedChecks = [];

  for (const check of rule.requiredChecks ?? []) {
    const state = checks[check.id] ?? "unknown";
    const result = { id: check.id, label: check.label, state };
    if (state === "fail") failedChecks.push(result);
    else if (state === "pass") passedChecks.push(result);
    else unknownChecks.push(result);
  }

  let status = "PASS";
  if (structuralErrors.length || failedChecks.length) status = "BLOCKED";
  else if (unknownChecks.length || missingFields.length || claimMismatch) status = "INSUFFICIENT_EVIDENCE";

  return {
    status,
    targetDecision: decisionId,
    decisionLabel: rule.label,
    requiredClaimLevel: rule.requiredClaimLevel,
    assertedClaimLevel: record?.assertedClaimLevel ?? null,
    errors: structuralErrors,
    structuralErrors,
    missingFields,
    claimMismatch,
    failedChecks,
    unknownChecks,
    passedChecks,
    ...resultMetadata(gates)
  };
}

export function getStopRule(gates, decisionType) {
  const rule = gates?.decisions?.[decisionType];
  if (!rule) throw new Error(`Unknown decision type: ${decisionType}`);
  return {
    decisionType,
    ...rule,
    gateVersion: gates?.version ?? null,
    principle: gates.principle
  };
}
