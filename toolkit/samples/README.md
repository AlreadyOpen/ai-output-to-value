# Claim Gate teaching samples

These records are **illustrative teaching cases**, not reports of client work. They are designed to show that the same artefact can support different decisions depending on the claim being asked of it.

## Case 1 — website prototype

- [`website-explore-pass.claim.json`](website-explore-pass.claim.json) — **Explore → PASS**. A reproducible prototype plus explicit assumptions is enough for the exploration decision.
- [`website-operate-blocked.claim.json`](website-operate-blocked.claim.json) — **Operate → BLOCKED**. The visible website is not evidence that the end-to-end enquiry workflow, ownership, monitoring, recovery, support, or cost boundary is established.

This pair is the shortest demonstration of the stop-rule principle: **the code/artefact did not change; the decision did.**

## Case 2 — internal incident-summary tool

- [`internal-tool-rely-pass.claim.json`](internal-tool-rely-pass.claim.json) — **Rely → PASS** for one bounded internal drafting use after the acceptance criteria and relevant failure modes are evidenced.

It does not claim autonomous incident resolution or repeatable organisational Capability.

## Case 3 — killed idea / option value

- [`killed-idea-outcome-pass.claim.json`](killed-idea-outcome-pass.claim.json) — **Outcome → PASS** because a bounded experiment removed decision-relevant uncertainty and triggered the pre-agreed stop rule.

No scale decision is sought. A useful learning Outcome does not need to become an operational Capability or a commercial Value claim.

## Case 4 — cross-domain false claim promotions

The cross-domain pack exercises different claim-confusion failures rather than adding sector-specific maturity models:

- [`customer-support-outcome-insufficient.claim.json`](customer-support-outcome-insufficient.claim.json) — **Outcome → INSUFFICIENT EVIDENCE**. Containment/deflection improved, but durable resolution, recurrence, and customer experience have not yet been measured comparably.
- [`report-factory-rely-blocked.claim.json`](report-factory-rely-blocked.claim.json) — **Rely → BLOCKED**. A polished, apparently complete proposal remains Output after a material source-traceability acceptance check fails.
- [`system-of-record-operate-blocked.claim.json`](system-of-record-operate-blocked.claim.json) — **Operate → BLOCKED**. Supervised writes can satisfy a bounded Deliverable claim while rollback, recourse, support, and delegated operating authority remain incomplete.
- [`professional-deliverable-rely-insufficient.claim.json`](professional-deliverable-rely-insufficient.claim.json) — **Rely → INSUFFICIENT EVIDENCE**. Technical human review is separate from the approval/signatory authority required for the named use.
- [`coding-assistant-outcome-pass.claim.json`](coding-assistant-outcome-pass.claim.json) — **Outcome → PASS**. The end-to-end measure is evidenced even though local coding speed improved while review wait, rework, and issue-to-production lead time worsened.
- [`time-saved-value-insufficient.claim.json`](time-saved-value-insufficient.claim.json) — **Value → INSUFFICIENT EVIDENCE**. A bounded time-saving Outcome does not establish realised Value without the conversion mechanism, full cost, risks, and alternatives.
- [`killed-idea-outcome-pass.claim.json`](killed-idea-outcome-pass.claim.json) — **Outcome → PASS**. The existing option-value sample is the seventh case: stopping productisation can still be a legitimate decision-changing Outcome.

The readable companion is `content/cross-domain-worked-cases.md`.

## Important interpretation

A green gate means the **supplied decision record satisfies the deterministic gate for the selected decision**. It is not an audit of the underlying system, measurements, people, or evidence references.
