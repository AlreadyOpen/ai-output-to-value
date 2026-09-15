# AI Output to Value — drop-in agent rules

Use these rules in coding agents, IDE agents, terminal agents, or repository guidance when the team wants the AI Output to Value decision discipline without forcing every task through production-grade process.

## Core rule

**The target decision determines the required claim and evidence. The identity of the producer does not.**

Do not assume work must progress through every claim level.

- **02 Output** can be enough for exploration or learning.
- **03 Deliverable** is required before someone may rely on the result for a named use.
- **04 Capability** is required before the organisation claims it can operate, support, sell, or staff the workflow repeatedly.
- **05 Outcome** is required before claiming the initiative changed a measured result.
- **06 Value** is required before claiming the evidenced outcome justified the full relevant cost, risk, alternatives, and trade-offs.

## Before declaring work complete

1. State the **decision being requested**.
2. State the **claim level being asserted**.
3. Separate **demonstrated facts** from **inference or assumptions**.
4. Name the **intended use** and important limits.
5. Provide evidence appropriate to the target claim.
6. Record the **assurance mechanism**. It may be human, AI, deterministic, specialist-tool, or hybrid.
7. State the **authority boundary** separately from evaluation quality.
8. State where **accountability / recourse** sits.
9. State the **next evidence** that would change the decision.
10. State a **stop or restrict rule**.

## Software-specific guidance

For exploration, a reproducible artefact plus explicit assumptions may be enough. Do not invent deployment, rollback, support, or ROI work if it would not change the exploration decision.

For a relied-upon Deliverable, include relevant acceptance criteria and evidence such as tests, contract checks, integration checks, error handling, known failure modes, and intended-use boundaries.

For operational Capability, add the controls that matter to the actual failure modes: ownership, monitoring, recovery/rollback where warranted, maintenance/debugging responsibility, support/escalation, and relevant operating cost.

## Do not use producer identity as a shortcut

Do not say:

- "A human reviewed it, therefore it is safe."
- "AI generated it, therefore extra process is automatically required."
- "The agent completed the task, therefore the job is finished."
- "The code works locally, therefore the organisation can operate it."

Instead ask:

> **What decision is being made, what claim is sufficient for that decision, and what evidence establishes that claim?**

## Machine-readable record

When a structured decision record is useful, produce a JSON file conforming to:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`

Use the deterministic gate rules at:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`
