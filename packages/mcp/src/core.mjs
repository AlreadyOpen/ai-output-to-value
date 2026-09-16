export const DEFAULT_PUBLICATION_URL = "https://alreadyopen.github.io/ai-output-to-value/";

export async function fetchJson(baseUrl, path) {
  const url = new URL(path, baseUrl).href;
  const response = await fetch(url, { headers: { accept: "application/json" } });
  if (!response.ok) throw new Error(`${url} returned HTTP ${response.status}`);
  return response.json();
}

const REQUIRED_TEXT_FIELDS = ["project", "intendedUse", "authority", "accountability", "nextEvidence", "stopRule"];

export function evaluateClaim(record, gates) {
  const decisionId = record?.targetDecision;
  const rule = gates?.decisions?.[decisionId];
  const structuralErrors = [];
  const missingFields = [];

  if (record?.schemaVersion !== "1.0") {
    structuralErrors.push("schemaVersion must be '1.0'");
  }

  if (!rule) {
    structuralErrors.push(`Unknown targetDecision: ${String(decisionId)}`);
    return {
      status: "BLOCKED",
      targetDecision: decisionId ?? null,
      errors: structuralErrors,
      structuralErrors,
      missingFields,
      claimMismatch: false,
      failedChecks: [],
      unknownChecks: [],
      passedChecks: []
    };
  }

  if (record?.requiredClaimLevel !== rule.requiredClaimLevel) {
    structuralErrors.push(`requiredClaimLevel must be ${rule.requiredClaimLevel} for ${decisionId}`);
  }

  for (const field of REQUIRED_TEXT_FIELDS) {
    if (!String(record?.[field] ?? "").trim()) missingFields.push(field);
  }
  if (!Array.isArray(record?.actors) || record.actors.length === 0) missingFields.push("actors");

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
    principle: gates?.principle ?? null
  };
}

export function getStopRule(gates, decisionType) {
  const rule = gates?.decisions?.[decisionType];
  if (!rule) throw new Error(`Unknown decision type: ${decisionType}`);
  return { decisionType, ...rule, principle: gates.principle };
}
