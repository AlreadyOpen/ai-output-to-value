export const DEFAULT_PUBLICATION_URL = "https://alreadyopen.github.io/ai-output-to-value/";

export async function fetchJson(baseUrl, path) {
  const url = new URL(path, baseUrl).href;
  const response = await fetch(url, { headers: { accept: "application/json" } });
  if (!response.ok) throw new Error(`${url} returned HTTP ${response.status}`);
  return response.json();
}

export function evaluateClaim(record, gates) {
  const decisionId = record?.targetDecision;
  const rule = gates?.decisions?.[decisionId];
  if (!rule) {
    return {
      status: "BLOCKED",
      targetDecision: decisionId ?? null,
      errors: [`Unknown targetDecision: ${String(decisionId)}`],
      failedChecks: [],
      unknownChecks: []
    };
  }

  const errors = [];
  if (record?.requiredClaimLevel !== rule.requiredClaimLevel) {
    errors.push(`requiredClaimLevel must be ${rule.requiredClaimLevel} for ${decisionId}`);
  }

  const checks = record?.gateChecks && typeof record.gateChecks === "object" ? record.gateChecks : {};
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

  const requiredTextFields = ["project", "intendedUse", "authority", "accountability", "nextEvidence", "stopRule"];
  for (const field of requiredTextFields) {
    if (!String(record?.[field] ?? "").trim()) errors.push(`Missing required decision-record field: ${field}`);
  }
  if (!Array.isArray(record?.actors) || record.actors.length === 0) errors.push("actors must contain at least one actor record");

  let status = "PASS";
  if (failedChecks.length || errors.length) status = "BLOCKED";
  else if (unknownChecks.length) status = "INSUFFICIENT_EVIDENCE";

  return {
    status,
    targetDecision: decisionId,
    decisionLabel: rule.label,
    requiredClaimLevel: rule.requiredClaimLevel,
    assertedClaimLevel: record?.assertedClaimLevel ?? null,
    errors,
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
