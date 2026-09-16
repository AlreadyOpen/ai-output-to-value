# AI Output to Value — drop-in agent rules

Use these rules in coding agents, IDE agents, terminal agents, or repository guidance when the team wants the AI Output to Value decision discipline without forcing every task through production-grade process.

## Core rule

**The target decision determines the required claim and evidence. The identity of the producer does not.**

Do not assume work must progress through every claim level.

- **02 Output** can be enough for exploration or learning.
- **03 Deliverable** is required before someone may rely on the result for a named use.
- **04 Operating capability** is required before the organisation claims it can operate, support, sell, or staff the workflow repeatedly. The stable machine identifier remains `04-capability`.
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

## Do not accept management vocabulary as evidence

If a request uses terms such as **workflow**, **teamwork**, **KPI**, **productivity**, **leadership**, or **alignment**, do not treat the term itself as an acceptance criterion or explanation.

Operationalise it first:

- **workflow** — trigger, completion boundary, handoffs, unhappy path, outcome;
- **teamwork** — participants, roles, before/during/after activity, decision rights, follow-up;
- **KPI** — exact metric definition, unit, data source, baseline, cadence, guardrails;
- **productivity** — accepted output/outcome per relevant input, including quality and downstream rework boundary;
- **leadership** — observable decisions, coordination, authority, escalation, accountability, capability built, outcomes;
- **alignment** — aligned on which decision, constraint, priority, or measure, and how drift or disagreement becomes visible.

A title, slogan, meeting, dashboard, or meme can frame a question. It does not prove performance.

Apply this rule to executive, management, technical, operational, human, AI, and hybrid claims symmetrically.

## Software-specific guidance

For exploration, a reproducible artefact plus explicit assumptions may be enough. Do not invent deployment, rollback, support, or ROI work if it would not change the exploration decision.

For a relied-upon Deliverable, include relevant acceptance criteria and evidence such as tests, contract checks, integration checks, error handling, known failure modes, intended-use boundaries, and the downstream workflow needed for the result to reach its intended user or system.

For Operating capability, add the controls that matter to the actual failure modes: ownership, monitoring, recovery/rollback where warranted, maintenance/debugging responsibility, support/escalation, and relevant operating cost.

When AI accelerates one software task, do not infer that the development workflow accelerated by the same amount. Check whether the constraint moved into review, integration testing, security review, deployment, support, or another downstream stage.

## Do not use producer identity as a shortcut

Do not say:

- "A human reviewed it, therefore it is safe."
- "AI generated it, therefore extra process is automatically required."
- "The agent completed the task, therefore the job is finished."
- "The code works locally, therefore the organisation can operate it."
- "More code was produced, therefore the end-to-end delivery workflow improved."
- "Management called it a KPI/productivity/teamwork problem, therefore the term is already well defined."

Instead ask:

> **What decision is being made, what claim is sufficient for that decision, what is the end-to-end workflow boundary, what do the management terms mean operationally, and what evidence establishes the claim across that boundary?**

## Machine-readable record

When a structured decision record is useful, produce a JSON file conforming to:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`

Use the deterministic gate rules at:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`
