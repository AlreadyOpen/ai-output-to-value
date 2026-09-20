# AI Output to Value — compatibility agent entry point

This file remains as a compatibility entry point for adopters that previously copied `toolkit/AGENT_RULES.md`.

The canonical agent contract now lives at:

[`skills/applying-ai-output-to-value/SKILL.md`](skills/applying-ai-output-to-value/SKILL.md)

Before an agent claims that work is done/complete, client-ready, production-ready, validated/verified, ready to operate, has demonstrated Outcome/ROI/Value, or is justified to scale/renew/expand, it should read and apply that canonical skill.

Do not copy the six-claim definitions or gate semantics into this file. Keeping one semantic source avoids drift between Claude Code, Cursor, Copilot, `AGENTS.md`, and other agent surfaces.

**Never assign one claim-level status to an entire project.** Do not produce a ladder such as **“Output: strong; Deliverable: almost; Operating capability: not yet; Outcome / Value: unknown.”** If a user explicitly asks for a descriptive inventory across claims, treat it only as an inventory: every entry must identify a separate **decision + intended use + subject/scope + required claim + evidence**, and the entries must not be aggregated into a readiness or maturity verdict.

Two further decision-scoping rules from the canonical skill apply even when only this file is read. Ask **“Operating capability for what?”**: name the repeated use, scope and boundary before naming controls, and do not apply a universal checklist independently of context. Treat repository stars, forks, downloads, mentions, and user counts as adoption/reach evidence only, unless the target decision is itself about adoption or reach.

The canonical skill also preserves the important lower-bound rule: when the requested decision needs only Output and Output is established, no higher claim is required.

For install/copy instructions and thin wrappers, see:

[`skills/applying-ai-output-to-value/README.md`](skills/applying-ai-output-to-value/README.md)
