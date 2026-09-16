import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

import { evaluateClaim, getStopRule } from "../src/core.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const gates = JSON.parse(await readFile(resolve(here, "../../../schemas/v1/decision-gates.json"), "utf8"));

function record() {
  return {
    schemaVersion: "1.0",
    project: "example",
    targetDecision: "rely",
    requiredClaimLevel: "03-deliverable",
    assertedClaimLevel: "03-deliverable",
    intendedUse: "Named use",
    actors: [{ type: "ai-agent", role: "Draft" }],
    authority: "Bounded",
    accountability: "Organisation",
    gateChecks: {
      "intended-use-defined": "pass",
      "acceptance-criteria-defined": "pass",
      "acceptance-criteria-met": "pass",
      "failure-modes-tested": "pass",
      "limitations-stated": "pass"
    },
    nextEvidence: "Fresh evaluation",
    stopRule: "Stop if threshold fails"
  };
}

test("complete gate passes", () => {
  assert.equal(evaluateClaim(record(), gates).status, "PASS");
});

test("failed check blocks", () => {
  const value = record();
  value.gateChecks["acceptance-criteria-met"] = "fail";
  assert.equal(evaluateClaim(value, gates).status, "BLOCKED");
});

test("unknown evidence remains insufficient", () => {
  const value = record();
  value.gateChecks["acceptance-criteria-met"] = "unknown";
  assert.equal(evaluateClaim(value, gates).status, "INSUFFICIENT_EVIDENCE");
});

test("not-applicable required evidence remains insufficient and is preserved", () => {
  const value = record();
  value.gateChecks["acceptance-criteria-met"] = "not-applicable";
  const result = evaluateClaim(value, gates);
  assert.equal(result.status, "INSUFFICIENT_EVIDENCE");
  assert.equal(result.unknownChecks[0].state, "not-applicable");
});

test("missing decision-record text is insufficient rather than blocked", () => {
  const value = record();
  value.authority = "";
  const result = evaluateClaim(value, gates);
  assert.equal(result.status, "INSUFFICIENT_EVIDENCE");
  assert.deepEqual(result.missingFields, ["authority"]);
});

test("missing actors is insufficient rather than silently inferred", () => {
  const value = record();
  value.actors = [];
  const result = evaluateClaim(value, gates);
  assert.equal(result.status, "INSUFFICIENT_EVIDENCE");
  assert.ok(result.missingFields.includes("actors"));
});

test("asserted claim mismatch is insufficient", () => {
  const value = record();
  value.assertedClaimLevel = "02-output";
  const result = evaluateClaim(value, gates);
  assert.equal(result.status, "INSUFFICIENT_EVIDENCE");
  assert.equal(result.claimMismatch, true);
});

test("required claim mapping mismatch is structurally blocked", () => {
  const value = record();
  value.requiredClaimLevel = "02-output";
  const result = evaluateClaim(value, gates);
  assert.equal(result.status, "BLOCKED");
  assert.ok(result.structuralErrors.length > 0);
});

test("unsupported schema version is structurally blocked", () => {
  const value = record();
  value.schemaVersion = "2.0";
  const result = evaluateClaim(value, gates);
  assert.equal(result.status, "BLOCKED");
  assert.ok(result.structuralErrors.some((message) => message.includes("schemaVersion")));
});

test("actor identity does not change the gate", () => {
  const ai = record();
  const human = record();
  human.actors = [{ type: "human", role: "Author" }];
  assert.equal(evaluateClaim(ai, gates).status, evaluateClaim(human, gates).status);
});

test("stop rule comes from target decision", () => {
  assert.equal(getStopRule(gates, "operate").requiredClaimLevel, "04-capability");
});
