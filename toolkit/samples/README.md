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

## Important interpretation

A green gate means the **supplied decision record satisfies the deterministic gate for the selected decision**. It is not an audit of the underlying system, measurements, people, or evidence references.
