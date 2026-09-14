# Evidence policy

AI Output to Value is intended for management conversations, procurement discussions, delivery reviews, and professional practice. That requires more than collecting persuasive links.

The project separates **evidence**, **interpretation**, **recommendation**, and **anecdote**. It also separates **a structurally valid preview** from **an approved release**.

## 1. Evidence classes

The structured registries may use specific `evidence_type` labels, but they should remain recognisable as one of these broad classes.

### Research study

Empirical or experimental work with a described method, sample, measures, and limitations.

**Use for:** measured effects in a defined context.

**Do not use for:** universal multipliers or conclusions outside the studied task without additional evidence.

### Official guidance / standard / statistics

Material issued by governments, regulators, standards bodies, or official statistical agencies.

**Use for:** official statistics, governance expectations, lifecycle considerations, assurance practices, procurement questions, and terminology where applicable.

**Do not use for:** financial return or technical effectiveness the source does not measure.

### Industry research

Research, surveys, or measurement programmes produced by companies, foundations, or industry research groups.

**Requirement:** disclose who produced it and retain material methodology and limitations.

### Vendor guidance / product documentation / announcement

Material published by the supplier of the relevant product or service.

**Use for:** product behaviour, interfaces, availability, vendor positioning, and implementation guidance.

**Do not use for:** treating commercial positioning as independent proof of quality, ROI, or general effectiveness.

When availability matters, record it explicitly: for example **announced**, **preview**, **available**, or a more precise status.

### Case study

A described implementation or outcome in a specific organisation.

**Use for:** showing that an approach can work in that setting and identifying mechanisms.

**Do not use for:** prevalence or automatic generalisation.

### Practitioner analysis

Reasoned professional commentary by an identifiable practitioner or team.

**Use for:** terminology, workflow patterns, and hypotheses worth testing.

### Practitioner account / community discussion

First-person accounts, forum posts, issue threads, or community discussions.

**Use for:** discovering failure modes, incentives, questions, and realistic scenarios.

**Do not use for:** proving that an event occurred exactly as described, measuring prevalence, or proving causation.

### Editorial recommendation / inference

A recommendation or synthesis made by this project.

**Requirement:** label it as editorial rather than presenting it as a direct research finding.

## 2. Claim statuses

Important factual claims may use:

- **supported** — directly supported by the cited evidence within its stated scope;
- **qualified** — supported only with material limitations or contextual conditions;
- **contested** — credible evidence or interpretations disagree;
- **illustrative** — a constructed example rather than an observed measurement;
- **anecdotal** — based on a practitioner account or community discussion;
- **editorial** — a recommendation or synthesis made by this project.

A prestigious source cannot support a claim outside what it actually says.

## 3. Canonical publication registries

Canonical publication evidence lives under `data/`.

Source records may be split across files such as:

```text
data/sources.yml
data/sources-product-discovery.yml
data/sources-architecture-economics.yml
data/ai-business-capability-sources.yml
```

Claim records may likewise be split across:

```text
data/claims.yml
data/claims-product-discovery.yml
data/claims-architecture-economics.yml
data/claims-ai-business-capability.yml
```

The exact filenames are less important than the contract: a canonical file under `data/` contains a top-level `sources:` or `claims:` list and is loaded through the shared publication-data loader.

Both the builder and validator use [`scripts/publication_data.py`](../scripts/publication_data.py). This prevents one component from accepting evidence that another component cannot render.

Files under `research/` are working notes or pointers. They are not a second publication registry.

## 4. The traceability rule

For each important factual claim, the project should be able to reconstruct:

> **Claim → source → source version/date → exact locator → relevant finding → qualification → publication location → reviewer/process → review date/status**

A broad `supports:` tag in a source record helps discovery. It is not a substitute for claim-level traceability.

A claim record should resemble:

```yaml
- id: stable-claim-id
  claim_text: The wording the project intends to publish.
  status: supported
  launch_critical: true
  evidence:
    - source_id: registered-source-id
      source_version: version or review date used
      locator: exact section, page, table, figure or named subsection
      relevant_finding: what the source actually establishes
      qualification: what must remain visible to avoid overclaiming
  published_in:
    - file: content/example.md
      locator: "## Exact heading in the article"
  reviewer: transparent reviewer or review process
  reviewed: 2026-09-14
  independent_review_status: pending
```

The structural checker verifies that publication locators exist. The built evidence page gives each claim a stable HTML anchor and links back to the pages using it.

## 5. Independent review must be actor-neutral

A date on an article means **Last updated**, not “all factual claims approved”.

Reader-facing article metadata should distinguish:

- publication status, such as **Draft**, **Research draft**, **Editorial review in progress**, or **Reviewed for publication**;
- last-updated date;
- independent-review state for connected claims.

Machine values such as `research_draft` may remain in YAML but should be translated into normal reader-facing wording.

A claim marked `independent_review_status: completed` must have an inspectable reviewer/process and review date.

> **Independent review is a property of the process, not the identity of the reviewer.**

The reviewer may be a human, AI system, automated method, specialist toolchain, or hybrid process. The same standard applies: the review should be sufficiently separate from the originating authoring step, inspect the relevant source or evidence directly, test whether the claim follows within scope, preserve material qualifications, and record enough information to audit what happened.

A second pass by the same authoring process should not be labelled independent merely because it produced a different answer. Likewise, a human author reading their own draft again is not automatically independent review. Independence is about separation, method, and evidence.

Different contexts may still require a particular type of approval. For example, a law, contract, board rule, safety procedure, or professional standard may require a named human sign-off. That is an **authority or governance requirement**, not evidence that human review is intrinsically a better truth-finding mechanism.

## 6. Preserve scope

When summarising research, retain enough context to prevent a true result from becoming a misleading generalisation.

Record when available:

- population or sample;
- task or domain;
- intervention or tool;
- comparison or baseline;
- measured outcome;
- study period;
- major limitations;
- peer-review / working-paper / survey / vendor status.

A measured productivity effect in customer support, for example, should remain a customer-support finding unless additional evidence supports broader use.

## 7. Separate speed, cost, and value

Do not treat these as interchangeable:

- reduced labour hours;
- reduced elapsed time;
- faster generation;
- reduced cost;
- increased capacity;
- increased revenue;
- increased profit;
- reduced risk;
- improved customer outcome.

When using percentages, name the quantity. “Uses 75% fewer labour hours” is not the same statement as “75% faster.”

For commercial examples, keep **customer value**, **selling price**, **relevant delivery cost**, **contribution before fixed costs**, and **total business profit** separate.

For AI-service architecture comparisons, define both the numerator and denominator of **cost per acceptable outcome**.

## 8. Count displaced work

When discussing productivity or savings, look for work that moved rather than disappeared:

- specification and context preparation;
- evaluation and fact-checking;
- correction and rework;
- testing and validation;
- integration;
- security and compliance;
- maintenance and support;
- incident response;
- downstream interpretation.

This is an accounting discipline, not an assumption that AI necessarily increases total work.

## 9. Treat anecdotes carefully

Community accounts can reveal mechanisms that formal studies have not yet measured well.

For practitioner accounts:

- describe them as accounts or discussions;
- do not infer prevalence from votes or comment volume;
- avoid identifying uninvolved organisations from speculation;
- preserve counterarguments when they materially change interpretation;
- extract the durable management question rather than endorsing interpersonal behaviour.

Fictional teaching cases must remain visibly separate from practitioner accounts and independently observed outcomes.

## 10. AI-assisted contributions

AI may be used to draft, organise, translate, search, analyse, test, or review contributions.

That does not change the acceptance standard:

- linked sources must exist;
- sources must support the associated claim;
- material qualifications must remain visible;
- fictional/generated examples must be labelled when readers could mistake them for observed evidence;
- publication responsibility remains explicit.

AI use is neither a reason to reject work nor a substitute for evidence.

## 11. Preview gate versus release gate

These are deliberately different.

### Preview / structural gate

[`scripts/check_publication.py`](../scripts/check_publication.py), run by [`publication-gate.yml`](../.github/workflows/publication-gate.yml), checks that the draft publication is internally consistent.

It rejects, among other things:

- invalid YAML or duplicate IDs;
- empty required source/claim/evidence values;
- unknown source references;
- claim publication locators that do not exist;
- completed independent-review states without reviewer/date records;
- duplicate, invalid, or reserved article slugs;
- broken local links;
- missing HTML fragments;
- generated-site links that escape the deployed `site/` root;
- missing required built pages.

Regression tests in [`tests/test_publication_checks.py`](../tests/test_publication_checks.py) deliberately construct these failures and require the checker to reject them for the intended reason.

A green preview gate means **the draft builds and passes structural controls**. It does not mean the publication has been factually approved.

### Release approval gate

[`scripts/check_release.py`](../scripts/check_release.py) and the manual [`release-gate.yml`](../.github/workflows/release-gate.yml) apply the project’s current release policy.

At minimum:

- launch-critical claims must have completed independent review;
- the review record must be inspectable;
- core articles must be marked ready for publication.

The independent reviewer/process may be human, AI, automated, or hybrid, provided it meets the same evidence and separation criteria. A release gate is still not a guarantee of truth. It records that the project’s chosen publication controls have been completed.

## 12. Versioned publication links

The builder uses the build’s source reference when linking back to GitHub. In CI this can resolve to the commit being built rather than always pointing to moving `main`.

A released guide should therefore remain auditable after later edits.

## 13. Corrections

Corrections are part of the evidence system.

A correction should explain:

1. what was wrong or misleading;
2. what changed;
3. which source or reasoning supports the change;
4. whether other pages or claims are affected.

Where a disputed interpretation cannot be resolved cleanly, present the disagreement rather than forcing certainty.
