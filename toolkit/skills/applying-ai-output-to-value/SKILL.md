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

**Never assign one claim-level status to an entire project.** A summary such as **“Output: strong; Deliverable: almost; Operating capability: not yet; Outcome / Value: unknown”** is a maturity-ladder misuse even without a numeric score.

## Select the decision first

Use the lowest claim sufficient for the next decision:

- keep exploring → `02-output`
- permit reliance for a named use → `03-deliverable`
- sell, operate, support, or staff the named use within the stated scope repeatedly → `04-capability`
- determine whether the initiative changed the result → `05-outcome`
- scale, renew, expand, or stop → `06-value`

Do not let strong Access or Output compensate for a missing decision-critical Deliverable, Operating capability, Outcome, or Value claim.

If the user explicitly asks for a descriptive inventory across several claim levels, do not turn it into a project verdict. Represent each entry as a separate **decision + intended use + subject/scope + required claim + evidence**. The same project may legitimately PASS an exploration decision, have INSUFFICIENT EVIDENCE for a reliance decision, and be BLOCKED for a repeated-operation decision.

Treat repository stars, forks, downloads, mentions, or user counts as **adoption/reach signals**, not readiness evidence, unless the target decision itself is explicitly about adoption or reach.

## Work from the machine contract

Prefer the published contract rather than re-encoding the framework from memory:

- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`
- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`

If the native MCP server is available, use `get_stop_rule` and `evaluate_claim_record`.

## Build or inspect the decision record

For the selected decision:

1. State the project / initiative.
2. State the intended use.
3. State the **subject / scope**: artefact or system version, users, environment, workflow boundary, time period, and relevant exclusions.
4. Identify the required claim from the target decision.
5. Describe the end-to-end workflow boundary when local task completion is not the same as delivery.
6. Record actors and interaction channels separately from authority and accountability. Do not silently infer an actor when none is supplied.
7. Evaluate each required gate check from supplied evidence as `pass`, `fail`, `unknown`, or `not-applicable` where the schema allows it.
8. Treat `unknown` and `not-applicable` on a **required** check as insufficient evidence; do not infer PASS from confidence, plausibility, or convenience.
9. Name evidence references, next evidence that would change the decision, and the stop rule.
10. For Outcome, define the measure, baseline/comparison, and material confounds.
11. For Value, include the full relevant cost/risk/alternative boundary rather than local task cost alone.

## Gate ≠ truth

A deterministic gate result evaluates the supplied record.

- `PASS` means the record is structurally coherent, required decision-record information is present, the asserted claim matches the selected decision, and all required checks are `pass`.
- `BLOCKED` means a required check explicitly failed **or** the record is structurally incompatible with the gate contract, for example an unsupported schema version, unknown target decision, or wrong required-claim mapping.
- `INSUFFICIENT_EVIDENCE` means no required check failed and the record is structurally usable, but required information/evidence is missing or unknown/not-applicable, or the asserted claim does not match the decision.

A PASS is **not** an independent audit of the underlying system, measurement, source, test, or person.

## When working with software

Before claiming Deliverable or Operating capability, consider relevant failure modes such as environment/configuration gaps, authorization boundaries, retry duplicate side effects, schema migration loss, concurrency races, observability gaps, rollback/recovery gaps, hidden manual steps, and scale/cost/latency cliffs.

For Operating capability, explicitly ask **“Operating capability for what repeated use, under which scope and boundary?”** Select controls from the material failure modes for that use; do not treat any universal checklist as sufficient independently of context.

If the native MCP server is available, use `search_failure_modes`.

For a software Outcome measurement plan, use `get_software_outcome_template` when available. The template proposes measurements; it does not mark evidence PASS automatically and does not choose an actor for the record.

## Human / AI / hybrid handoff

Use the same `claim.json` across channels. An agent may prepare or evaluate the record; a person may inspect or edit it; CI may apply the deterministic gate. Changing the interface does not change the standard.

Do not claim a local/UI handoff completed merely because an event or request was sent. Require acknowledgement from the receiving surface or describe the handoff as unconfirmed.

Do not claim that a human approval click proves quality. Do not claim that an AI evaluation proves quality. State the actual assurance process and evidence.

## Output

When asked to apply the method, return:

- target decision;
- intended use and subject/scope;
- required claim;
- gate status;
- decision-critical PASS / FAIL / UNKNOWN / NOT-APPLICABLE checks;
- demonstrated vs inferred/assumed points;
- workflow boundary if relevant;
- authority and accountability boundary;
- next evidence that would change the decision;
- stop rule;
- a `claim.json` record when structured output is useful.

Keep the conclusion bounded to the supplied evidence, intended use, subject/scope, and target decision. Do not emit one six-level status ladder for the project.
