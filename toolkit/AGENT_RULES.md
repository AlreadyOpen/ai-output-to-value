# AI Output to Value — drop-in agent rules

Use these rules in coding agents, IDE agents, terminal agents, or repository guidance when the team wants the AI Output to Value decision discipline without forcing every task through production-grade process.

## Core rule

**The target decision determines the required claim and evidence. The identity of the producer does not.**

Do not assume work must progress through every claim level.

**Never assign one claim-level status to an entire project.** Do not produce a ladder such as **“Output: strong; Deliverable: almost; Operating capability: not yet; Outcome / Value: unknown.”** If a user explicitly asks for a descriptive inventory across claims, treat it only as an inventory: every entry must identify a separate **decision + intended use + subject/scope + required claim + evidence**, and the entries must not be aggregated into a readiness or maturity verdict.

- **02 Output** can be enough for exploration or learning.
- **03 Deliverable** is required before someone may rely on the result for a named use.
- **04 Operating capability** is required before the organisation claims it can operate, support, sell, or staff the **named use within the stated scope** repeatedly. Ask **“Operating capability for what?”** The stable machine identifier remains `04-capability`.
- **05 Outcome** is required before claiming the initiative changed a measured result.
- **06 Value** is required before claiming the evidenced outcome justified the full relevant cost, risk, alternatives, and trade-offs.

**Workflow is not a seventh claim.** It is the end-to-end process boundary across which the requested claim must hold.

## Before declaring work complete

1. State the **decision being requested**.
2. Name the **intended use**.
3. State the **subject / scope**: artefact or system version, users, environment, workflow boundary, time period, and important exclusions as relevant.
4. State the **claim level being asserted**.
5. Separate **demonstrated facts** from **inference or assumptions**.
6. Map the **workflow boundary**: trigger/input, local task or product, downstream handoffs/verification, execution/delivery, unhappy path/recovery, and what counts as complete.
7. State where the **bottleneck may move** if this task becomes faster.
8. Provide evidence appropriate to the target claim.
9. Record the **assurance mechanism**. It may be human, AI, deterministic, specialist-tool, or hybrid.
10. State the **authority boundary** separately from evaluation quality.
11. State where **accountability / recourse** sits.
12. State the **next evidence** that would change the decision.
13. State a **stop or restrict rule**.

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

For Operating capability, first ask **Operating capability for what repeated use, under which scope and boundary?** Then add only the controls that matter to the actual failure modes: ownership, monitoring, recovery/rollback where warranted, maintenance/debugging responsibility, support/escalation, and relevant operating cost. Do not apply a universal checklist independently of context.

When AI accelerates one software task, do not infer that the development workflow accelerated by the same amount. Check whether the constraint moved into review, integration testing, security review, deployment, support, or another downstream stage.

## Do not use producer identity as a shortcut

Do not say:

- "A human reviewed it, therefore it is safe."
- "AI generated it, therefore extra process is automatically required."
- "The agent completed the task, therefore the job is finished."
- "The code works locally, therefore the organisation can operate it."
- "More code was produced, therefore the end-to-end delivery workflow improved."
- "Management called it a KPI/productivity/teamwork problem, therefore the term is already well defined."
- "The repository has many stars, forks, downloads, or users, therefore it is ready to rely on or operate."

Instead ask:

> **What decision is being made, for what intended use and subject/scope, what claim is sufficient for that decision, what is the end-to-end workflow boundary, what do the management terms mean operationally, and what evidence establishes the claim across that boundary?**

Treat stars, forks, downloads, mentions, and user counts as **adoption/reach evidence only**. They are readiness evidence only when the target decision itself is explicitly about adoption or reach.

## Machine-readable record

When a structured decision record is useful, produce a JSON file conforming to:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`

Use the deterministic gate rules at:

`https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`
