# Evidence policy

AI Output to Value is intended for management conversations, procurement discussions, delivery reviews, and professional practice. That requires more than collecting persuasive links.

The project separates **evidence**, **interpretation**, **recommendation**, and **anecdote**. It also separates a **working preview** from a **reviewed release artifact**.

## 1. Evidence classes

### Research study
Empirical or experimental work with a described method, sample, measures, and limitations. Use it for measured effects within the studied context, not universal multipliers.

### Official guidance / standard / statistics
Material issued by governments, regulators, standards bodies, or official statistical agencies. Use it for official statistics, governance expectations, lifecycle considerations, and assurance practices—not financial or technical effects it does not measure.

### Industry research
Research, surveys, or measurement programmes produced by companies, foundations, or industry groups. Disclose the producer and retain important methodological limits.

### Vendor guidance / product documentation / announcement
Use for product behaviour, interfaces, availability, vendor positioning, and implementation guidance. Do not treat vendor positioning as independent proof of quality, ROI, or general effectiveness.

### Case study
Use to show what happened in a specific implementation. Do not infer prevalence automatically.

### Practitioner analysis
Reasoned professional commentary useful for terminology, workflow patterns, and hypotheses.

### Practitioner account / community discussion
Useful for discovering failure modes and questions. Do not use it to prove prevalence, causation, or that every reported event occurred exactly as described.

### Editorial recommendation / inference
A synthesis made by this project. Label it as editorial rather than as a research result.

## 2. Claim statuses

Important claims use one of:

- **supported** — directly supported within the source's stated scope;
- **qualified** — supported only with material limitations or conditions;
- **contested** — credible evidence or interpretations disagree;
- **illustrative** — a constructed example rather than an observed measurement;
- **anecdotal** — based on a practitioner account or discussion;
- **editorial** — a recommendation or synthesis made by this project.

Source prestige cannot expand what a source actually establishes.

## 3. Canonical publication registries

Canonical source and claim records live under `data/` and may be split across topic-specific files. Both the builder and validator load them through [`scripts/publication_data.py`](../scripts/publication_data.py).

Files under `research/` are working notes or pointers, not a second publication registry.

## 4. Claim traceability

For each important factual claim, the project should be able to reconstruct:

> **Claim → source/version → exact locator → relevant finding → qualification → publication location → reviewer/process → independent-review state → review record**

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

`launch_critical` must be an explicit Boolean. Omission must not silently exempt a claim from release review.

## 5. Independent review is actor-neutral

> **Independent review is a property of the process, not the identity of the reviewer.**

The reviewer may be a human, AI system, automated method, specialist toolchain, or hybrid process. The review should be sufficiently separate from the originating authoring step, inspect the relevant evidence directly, test whether the claim follows within scope, preserve material qualifications, and leave an auditable record.

A second pass by the same authoring process is not automatically independent. A human author rereading their own draft is not automatically independent either.

A law, contract, board rule, safety procedure, or professional standard may still require a named human sign-off. That is an **authority/governance requirement**, not evidence that human review is inherently a better truth-finding mechanism.

### Completed-review record

A claim marked `independent_review_status: completed` must include an inspectable `review_record`:

```yaml
review_record:
  claim_revision: commit, tag, content hash, or other stable claim revision
  source_versions_checked:
    - source/version identifier actually inspected
  method: what the independent process checked
  finding: what the review concluded about support, scope, and qualifications
  disposition: accepted
```

Allowed dispositions are:

- `accepted`;
- `accepted_with_qualification`;
- `revised_and_accepted`;
- `rejected`.

This record need not expose private chain-of-thought. It should expose enough process evidence to show what was checked and why the disposition is inspectable.

## 6. Preserve scope

When summarising evidence, retain enough context to prevent a true result becoming a misleading generalisation. Record population/task, intervention, comparison, measured outcome, study period, source type, and important limitations where available.

A measured productivity effect in customer support should remain a customer-support finding unless additional evidence supports broader use.

## 7. Separate speed, cost, and value

Do not silently treat these as interchangeable:

- reduced labour hours;
- reduced elapsed time;
- faster generation;
- reduced cost;
- increased capacity;
- increased revenue;
- increased profit;
- reduced risk;
- improved customer outcome.

For commercial examples, keep **customer value**, **selling price**, **relevant delivery cost**, **contribution before fixed costs**, and **total business profit** separate.

For AI-service architecture comparisons:

> **Cost per acceptable outcome = total relevant workflow cost ÷ number of outcomes meeting the defined acceptance rule.**

State the numerator, denominator, task population, and acceptance rule.

## 8. Count displaced work

When discussing productivity or savings, look for work that moved rather than disappeared: specification, evaluation, correction, testing, integration, security/compliance, maintenance, support, incident response, and downstream interpretation.

This is an accounting discipline, not an assumption that AI increases total work.

## 9. Treat anecdotes and illustrations separately

Practitioner stories can reveal mechanisms, but must remain labelled as accounts or discussions. Do not infer prevalence from votes or repetition.

Fictional teaching cases must remain visibly separate from practitioner accounts and independently observed outcomes.

## 10. AI-assisted contributions

AI may be used to draft, organise, translate, search, analyse, test, or review contributions. The acceptance standard is the same regardless of actor:

- linked sources must exist;
- sources must support the associated claim;
- material qualifications must remain visible;
- constructed examples must be labelled;
- publication responsibility and recourse must remain explicit.

## 11. Preview gate versus release gate

### Working preview

The normal publication gate builds the full working publication, including core, deeper, advanced, and policy material. It checks structural integrity but does not approve factual claims for release.

The validator rejects, among other things:

- invalid or mistyped metadata;
- missing explicit `launch_critical` classification;
- invalid claim/article/review statuses;
- invalid dates;
- empty evidence values;
- unknown source references;
- missing claim publication locators;
- incomplete completed-review records;
- invalid article slugs or sections;
- broken links/fragments;
- built links that escape the deployment root.

Regression tests cover these failures directly.

### Reviewed release artifact

Each article declares a `release_scope`:

- `guide` — boss-facing pages intended for the reviewed release;
- `policy` — evidence/correction policy needed with that guide;
- `working` — deeper or advanced material that remains available in preview/source form but is excluded from the reviewed release artifact.

The release workflow builds with `PUBLICATION_MODE=release`, physically excluding `working` articles from the release artifact.

The release gate then checks that:

- every launch-critical claim completed independent review with an inspectable record;
- every `guide` article is marked `ready`;
- every included `policy` article is release-ready;
- expected release pages exist; and
- working pages did not enter the release artifact.

A passed release gate records completion of the project's declared controls for that revision. It is not a guarantee of truth.

## 12. Versioned publication links

The builder uses the build's source revision for links back to GitHub when available. This makes a released guide auditable after later edits.

The source repository URL and AlreadyOpen umbrella URL are configuration values so an eventual repository transfer does not require rewriting publication logic.

## 13. Corrections

Corrections are part of the evidence system. A correction should state:

1. what was wrong or misleading;
2. what changed;
3. which source or reasoning supports the change;
4. whether other pages or claims are affected.

Where a disputed interpretation cannot be resolved cleanly, present the disagreement rather than forcing certainty.
