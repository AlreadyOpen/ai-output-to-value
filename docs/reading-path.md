# Reading path

The repository contains a focused business guide plus broader analysis. A first-time reader should not have to read everything in order.

## Path 1 — first-time business reader

Read these in order:

1. [`START-HERE.md`](../START-HERE.md) — the core argument in about five minutes.
2. [`content/frame-vs-finished-work.md`](../content/frame-vs-finished-work.md) — why a strong concept, scaffold, or prototype can be valuable without proving the whole job is finished.
3. [`content/tool-access-vs-client-readiness.md`](../content/tool-access-vs-client-readiness.md) — tool capability, job substance, delivery capability, and the substance gap.
4. [`content/executive-guide.md`](../content/executive-guide.md) — workflow accounting, ownership, quality, and business value.
5. [`content/worked-cases.md`](../content/worked-cases.md) — fictional examples showing how the framework changes an actual decision.

If those pages answer the reader's question, they can stop there.

For a meeting, use the printable [`content/meeting-brief.md`](../content/meeting-brief.md).

## Path 2 — deeper analysis by decision

The deeper pages should each help produce a different decision artefact rather than repeat the same warning.

| Decision | Read | Practical output |
| --- | --- | --- |
| **Is this idea worth investigating?** | [`product-ideas-vs-product-discovery.md`](../content/product-ideas-vs-product-discovery.md) | **Opportunity hypothesis** — user, problem, evidence, current workaround, desired outcome, unknowns, cheapest next test. |
| **Why should this AI capability be part of the product?** | [`model-capability-vs-product-strategy.md`](../content/model-capability-vs-product-strategy.md) | **Technology-choice comparison** — customer problem, required capability, evidence, alternatives, constraints, delivery model and economics. |
| **Which technical design makes the service viable?** | [`architecture-economics-and-product-decisions.md`](../content/architecture-economics-and-product-decisions.md) | **Architecture trade-off record** — acceptance rule, attempts, routing/escalation, all-in cost per acceptable outcome, latency and failure consequence. |
| **Who or what should analyse, decide, communicate or act?** | [`ai-business-capability-and-judgement.md`](../content/ai-business-capability-and-judgement.md) | **Authority-and-assurance map** — actor, evaluative role, authority boundary, assurance mechanism, escalation and recourse. |

These four decisions are related, but they are not interchangeable:

**opportunity evidence → technology fit → delivery architecture → actor/authority/assurance design**

A team may revisit them iteratively rather than follow them as a waterfall.

### What happens to technical capability when AI gets much better?

- [`content/ai-does-not-eliminate-technical-capability.md`](../content/ai-does-not-eliminate-technical-capability.md)
- [`content/source-code-open-source-and-ai.md`](../content/source-code-open-source-and-ai.md)
- [`content/assess-every-layer-of-the-company.md`](../content/assess-every-layer-of-the-company.md)

### How should a company think about humans, agents, authority, and instruments?

- [`content/company-actors-vs-instruments.md`](../content/company-actors-vs-instruments.md)
- [`content/non-human-actors-and-accountability.md`](../content/non-human-actors-and-accountability.md)

### Does physical or human presence automatically create more value?

- [`content/representation-is-a-channel.md`](../content/representation-is-a-channel.md)
- [`content/ecommerce-and-physical-retail.md`](../content/ecommerce-and-physical-retail.md)

These supporting analyses and analogies should not dominate the public landing experience.

## Path 3 — evidence and editorial review

For contributors, reviewers, researchers, and readers who want to inspect the evidence system:

1. [`docs/evidence-policy.md`](evidence-policy.md) — evidence classes, canonical registry rules, review status, preview/release gates, and corrections.
2. [`data/claims.yml`](../data/claims.yml) — the base claim registry; additional canonical topic-specific claim registries live beside it under `data/claims*.yml`.
3. [`data/sources.yml`](../data/sources.yml) — the base source registry; additional canonical topic-specific source registries live beside it under `data/sources*.yml` and other `data/*.yml` files containing a top-level `sources:` list.
4. [`content/corrections.md`](../content/corrections.md) — correction and editorial-review route.

The publication build combines those canonical registries into one reader-facing evidence page with stable claim links and article backlinks.

## Editorial rule

The home page and `START-HERE.md` should remain narrow:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output to business value?**

Broader material belongs in deeper reading unless it is necessary to answer that question directly.
