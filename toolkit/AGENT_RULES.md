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

**Workflow is not a seventh claim.** It is the end-to-end process boundary across which the requested claim must hold.

## Before declaring work complete

1. State the **decision being requested**.
2. State the **claim level being asserted**.
3. Separate **demonstrated facts** from **inference or assumptions**.
4. Name the **intended use** and important limits.
5. Map the **workflow boundary**: trigger/input, local task or product, downstream handoffs/verification, execution/delivery, unhappy path/recovery, and what counts as complete.
6. State where the **bottleneck may move** if this task becomes faster.
7. Provide evidence appropriate to the target claim.
8. Record the **assurance mechanism**. It may be human, AI, deterministic, specialist-tool, or hybrid.
9. State the **authority boundary** separately from evaluation quality.
10. State where **accountability / recourse** sits.
11. State the **next evidence** that would change the decision.
12. State a **stop or restrict rule**.

## Software-specific guidance

For exploration, a reproducible artefact plus explicit assumptions may be enough. Do not invent deployment, rollback, support, or ROI work if it would not change the exploration decision.

For a relied-upon Deliverable, include relevant acceptance criteria and evidence such as tests, contract checks, integration checks, error handling, known failure modes, intended-use boundaries, and the downstream workflow needed for the result to reach its intended user or system.

For operational Capability, add the controls that matter to the actual failure modes: ownership, monitoring, recovery/rollback where warranted, maintenance/debugging responsibility, support/escalation, and relevant operating cost.

When AI accelerates one software task, do not infer that the development workflow accelerated by the same amount. Check whether the constraint moved into review, integration testing, security review, deployment, support, or another downstream stage.

## Do not use producer identity as a shortcut

Do not say:

- "A human reviewed it, therefore it is safe."
- "AI generated it, therefore extra process is automatically required."
- "The agent completed the task, therefore the job is finished."
- "The code works locally, therefore the organisation can operate it."
- "More code was produced, therefore the end-to-end delivery workflow improved."

Instead ask:

> **What decision is being made, what claim is sufficient for that decision, what is the end-to-end workflow boundary, and what evidence establishes that claim across that boundary?**

## Machine-readable record

When a structured decision record is useful, produce a JSON file conforming to:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`

Use the deterministic gate rules at:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`
