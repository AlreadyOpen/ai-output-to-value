// SPDX-License-Identifier: Apache-2.0
// The shared claim-gate conformance cases (tests/fixtures/claim-gate-conformance.json), as
// one harness. Every JavaScript surface that evaluates claims runs its cases through this
// file: the native MCP server, the browser bundle and WebMCP.

/** Build the record a case evaluates: a whole-record override, or the base record patched. */
export function caseInput(fixture, item) {
  if ("record" in item) return structuredClone(item.record);
  const value = structuredClone(fixture.baseRecord);
  for (const [key, replacement] of Object.entries(item.patch ?? {})) {
    if (key === "gateChecks" && replacement && typeof replacement === "object" && !Array.isArray(replacement)) {
      value.gateChecks = { ...value.gateChecks, ...replacement };
    } else {
      value[key] = replacement;
    }
  }
  for (const key of item.remove ?? []) delete value[key];
  return value;
}

/** Return why `result` does not satisfy the case, or null when it does. */
export function checkCase(item, result, gates) {
  const problems = [];
  if (result?.status !== item.expectedStatus) problems.push(`status ${result?.status} != ${item.expectedStatus}`);
  if (result?.gateVersion !== gates.version) problems.push(`gateVersion ${result?.gateVersion} != ${gates.version}`);
  if (result?.principle !== gates.principle) problems.push("principle differs from the rules");
  if (result?.rule !== gates.principle) problems.push("rule alias differs from the rules");
  if (Object.hasOwn(item, "expectedClaimMismatch") && result?.claimMismatch !== item.expectedClaimMismatch) {
    problems.push(`claimMismatch ${result?.claimMismatch} != ${item.expectedClaimMismatch}`);
  }
  if (item.expectedMissingFields && JSON.stringify(result?.missingFields) !== JSON.stringify(item.expectedMissingFields)) {
    problems.push(`missingFields ${JSON.stringify(result?.missingFields)} != ${JSON.stringify(item.expectedMissingFields)}`);
  }
  const errors = (result?.structuralErrors ?? []).join(" ").toLowerCase();
  for (const needle of item.errorContains ?? []) {
    if (!errors.includes(String(needle).toLowerCase())) problems.push(`structural errors lack "${needle}"`);
  }
  return problems.length ? problems.join("; ") : null;
}

/** Run every case through `evaluate(record)` (sync or async); return the failures. */
export async function runConformance({ fixture, gates, evaluate }) {
  const failures = [];
  for (const item of fixture.cases) {
    let problem;
    try {
      problem = checkCase(item, await evaluate(caseInput(fixture, item)), gates);
    } catch (error) {
      problem = `threw ${error instanceof Error ? error.message : String(error)}`;
    }
    if (problem) failures.push(`${item.name}: ${problem}`);
  }
  return failures;
}
