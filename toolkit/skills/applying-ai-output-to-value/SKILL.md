---
name: applying-ai-output-to-value
description: Apply the AI Output to Value stop-rule framework to a proposal, code change, workflow, experiment, or operating decision. Use when deciding what has actually been demonstrated, which claim is sufficient for the next decision, what evidence is missing, or whether a human/AI/hybrid result is ready to rely on, operate, measure, scale, renew, or stop.
---

# Applying AI Output to Value

Use the target decision to choose the gate. Do not average claim levels and do not privilege or penalise work because it was produced by a human, AI system, automation, or hybrid process.

## Core rule

The framework uses six claims:

**01 Access → 02 Output → 03 Deliverable → 04 Operating capability → 05 Outcome → 06 Value**

The stable machine identifier for Operating capability is `04-capability`.

These are different claims, not a maturity score and not six mandatory lifecycle stages.

## Select the decision first

Use the lowest claim sufficient for the next decision:

- keep exploring → `02-output`
- permit reliance for a named use → `03-deliverable`
- sell, operate, support, or staff repeatedly → `04-capability`
- determine whether the initiative changed the result → `05-outcome`
- scale, renew, expand, or stop → `06-value`

Do not let strong Access or Output compensate for a missing decision-critical Deliverable, Operating capability, Outcome, or Value claim.

## Work from the machine contract

Prefer the published contract rather than re-encoding the framework from memory:

- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`
- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`

If the native MCP server is available, use `get_stop_rule` and `evaluate_claim_record`.

## Build or inspect the decision record

For the selected decision:

1. State the project / initiative and intended use.
2. Identify the required claim from the target decision.
3. Describe the end-to-end workflow boundary when local task completion is not the same as delivery.
4. Record actors and interaction channels separately from authority and accountability.
5. Evaluate each required gate check as `pass`, `fail`, or `unknown` from supplied evidence.
6. Keep missing or unverified evidence as `unknown`; do not infer PASS from confidence or plausibility.
7. Name evidence references, next evidence that would change the decision, and the stop rule.
8. For Outcome, define the measure, baseline/comparison, and material confounds.
9. For Value, include the full relevant cost/risk/alternative boundary rather than local task cost alone.

## Gate ≠ truth

A deterministic gate result evaluates the supplied record.

- `PASS` means the record satisfies the checks for the selected decision.
- `BLOCKED` means at least one decision-critical check explicitly failed.
- `INSUFFICIENT_EVIDENCE` means the decision is not yet justified by the supplied record.

A PASS is **not** an independent audit of the underlying system, measurement, source, test, or person.

## When working with software

Before claiming Deliverable or Operating capability, consider relevant failure modes such as environment/configuration gaps, authorization boundaries, retry duplicate side effects, schema migration loss, concurrency races, observability gaps, rollback/recovery gaps, hidden manual steps, and scale/cost/latency cliffs.

If the native MCP server is available, use `search_failure_modes`.

For a software Outcome measurement plan, use `get_software_outcome_template` when available. The template proposes measurements; it does not mark evidence PASS automatically.

## Human / AI / hybrid handoff

Use the same `claim.json` across channels. An agent may prepare or evaluate the record; a person may inspect or edit it; CI may apply the deterministic gate. Changing the interface does not change the standard.

Do not claim that a human approval click proves quality. Do not claim that an AI evaluation proves quality. State the actual assurance process and evidence.

## Output

When asked to apply the method, return:

- target decision;
- required claim;
- gate status;
- decision-critical PASS / FAIL / UNKNOWN checks;
- demonstrated vs inferred/assumed points;
- workflow boundary if relevant;
- authority and accountability boundary;
- next evidence that would change the decision;
- stop rule;
- a `claim.json` record when structured output is useful.

Keep the conclusion bounded to the supplied evidence and intended decision.
