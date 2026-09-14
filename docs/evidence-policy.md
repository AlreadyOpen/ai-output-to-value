# Evidence policy

AI Output to Value is intended to be useful in management conversations, procurement discussions, delivery reviews, and professional practice. That requires a higher standard than collecting persuasive links.

The project therefore separates **evidence**, **interpretation**, **recommendation**, and **anecdote**.

## 1. Evidence classes

The policy uses a small set of broad evidence classes. The structured source register may use a more specific `evidence_type` label where that improves precision; those labels must still roll up to one of these policy classes.

### Research study

Empirical or experimental work with a described method, sample, measures, and limitations. This includes peer-reviewed papers and clearly identified working papers.

**Use for:** claims about measured effects in a defined context.

**Do not use for:** universal productivity multipliers or claims outside the study population without additional evidence.

### Official guidance / standard / statistics

Material issued by governments, regulators, standards bodies, official statistical agencies, or other institutions with a defined public assurance or measurement role.

**Use for:** official statistics, governance expectations, lifecycle considerations, assurance practices, procurement questions, and terminology where applicable.

**Do not use for:** proving a financial return that the source does not measure.

### Industry research

Research, surveys, or measurement programmes produced by companies, industry organisations, foundations, or research groups.

**Use for:** observed patterns, operational metrics, practitioner data, and emerging evidence.

**Requirement:** disclose who produced the work and retain important methodology and limitations.

### Vendor guidance / product documentation / announcement

Material published by a company that sells the relevant product or service.

**Use for:** product behaviour, availability, vendor framing, implementation guidance, or clearly described internal evidence.

**Do not use for:** treating commercial positioning as independent proof of quality, ROI, or general effectiveness.

For product capability, record availability explicitly when relevant: for example **announced**, **preview**, **available**, or a more precise status such as **handle reservation available / full capability forthcoming**.

### Case study

A described implementation or outcome in a specific organisation.

**Use for:** showing that an approach can work in a particular setting and identifying practical mechanisms.

**Do not use for:** estimating prevalence or assuming generalisation.

### Practitioner analysis

Reasoned professional commentary by an identifiable practitioner or team.

**Use for:** terminology, workflow patterns, practical distinctions, and hypotheses worth testing.

**Do not use for:** quantitative prevalence claims without independent data.

### Practitioner account / community discussion

First-person accounts, forum posts, Reddit discussions, issue threads, or similar material.

**Use for:** discovering failure modes, incentives, questions, and realistic examples.

**Do not use for:** establishing that an event occurred exactly as described, identifying culpable organisations, measuring prevalence, or proving causation.

### Editorial recommendation / inference

A recommendation or interpretation made by this project after considering evidence and practical consequences.

**Use for:** decision frameworks, analogies, and conclusions that combine several sources.

**Requirement:** label it as editorial rather than presenting it as a direct research finding.

### Registry labels

Specific machine labels can be more detailed than the policy classes. Examples:

| Registry `evidence_type` example | Policy class |
| --- | --- |
| `research_study`, `research_working_paper`, `research_summary` | Research study |
| `official_statistics`, `official_guidance`, `intergovernmental_standard_guidance` | Official guidance / standard / statistics |
| `industry_research`, `industry_research_summary`, `foundation_report_summary` | Industry research |
| `vendor_product_documentation`, `vendor_announcement`, `vendor_guidance` | Vendor guidance / product documentation / announcement |
| `practitioner_analysis` | Practitioner analysis |
| `community_discussion` | Practitioner account / community discussion |

The label should describe the source, not inflate its authority. Claim status and qualification still determine what can responsibly be published.

## 2. Claim statuses

Important claims should use one of these statuses in working notes or structured content:

- **supported** — directly supported by the cited evidence within its stated scope;
- **qualified** — supported only with material limitations or contextual conditions;
- **contested** — credible sources or interpretations disagree;
- **illustrative** — an example constructed to explain a concept, not an observed measurement;
- **anecdotal** — based on a practitioner account or community discussion;
- **editorial** — a recommendation or interpretation made by this project.

A source's prestige does not change the status of the claim it can support.

## 3. The traceability rule

For each important factual claim, the project should be able to reconstruct:

> **Claim → source → exact locator → relevant finding → qualification → publication location → reviewer → review date**

The source register in [`data/sources.yml`](../data/sources.yml) identifies publications. The claim register in [`data/claims.yml`](../data/claims.yml) records the narrower relationship between a published sentence and the evidence that supports it.

For launch-critical factual claims, record at minimum:

```yaml
- id: stable-claim-id
  claim_text: The wording the project intends to publish.
  status: supported
  launch_critical: true
  evidence:
    - source_id: registered-source-id
      locator: Exact section, page, table, figure, paragraph, or named subsection.
      relevant_finding: What that location actually establishes.
      qualification: What must remain visible to avoid overclaiming.
  published_in:
    - file: index.html
      locator: "#evidence"
  reviewer: Name or transparent review role
  reviewed: 2026-09-14
  human_review_status: pending
```

A broad `supports:` tag in a source record is useful for discovery, but it is **not** a substitute for claim-level traceability when a factual statement is published prominently.

The `reviewer` field must not imply independent human verification when none occurred. AI-assisted source checks should be labelled as such and may retain `human_review_status: pending` until a person independently checks the source.

## 4. Preserve scope

When summarising research, retain enough context to prevent a true result from becoming a misleading generalisation.

At minimum, record when available:

- population or sample;
- task or domain;
- intervention or tool;
- comparison or baseline;
- measured outcome;
- study period;
- major limitations;
- whether the source is peer-reviewed, a working paper, survey, case study, or vendor analysis.

For example, a measured productivity improvement in customer support should not become “AI improves worker productivity by X%” without the customer-support context.

## 5. Separate speed from value

The project should not treat any of the following as interchangeable:

- reduced labour hours;
- reduced elapsed delivery time;
- faster generation;
- faster completion;
- reduced cost;
- increased capacity;
- increased revenue;
- increased profit;
- reduced risk;
- improved user or customer outcomes.

A source or calculation that measures one does not automatically support claims about the others.

When using percentages, name the quantity. “Uses 75% fewer labour hours” is different from “75% faster.”

## 6. Count displaced work

When discussing productivity or savings, look for work that moved rather than disappeared:

- prompt and specification preparation;
- review and fact-checking;
- correction and rework;
- testing and validation;
- integration;
- security and compliance work;
- maintenance;
- support;
- incident response;
- downstream interpretation by colleagues or customers.

This is an accounting principle for the guide, not an assumption that AI necessarily increases total work.

## 7. Treat anecdotes carefully

Anecdotes can be useful when they reveal a mechanism that formal research has not yet measured well.

For community accounts:

- describe them as accounts, reports, or discussions;
- avoid naming uninvolved companies based on speculation in comments;
- do not infer prevalence from votes or comment volume;
- preserve meaningful counterarguments when they change the interpretation;
- extract the durable management question rather than endorsing interpersonal behaviour in the story.

## 8. Source updates and reversals matter

AI research and product availability move quickly. Later work or documentation may qualify earlier results.

The source register includes a `reviewed` date and may include publication dates, versions, availability status, or relationships such as `supersedes` and `qualified_by`. When a later source materially changes an earlier interpretation, the website should update the explanation rather than preserve the more convenient headline.

## 9. AI-assisted contributions

AI tools may be used to draft, organise, translate, search, or analyse contributions to this repository.

That does not change the acceptance standard:

- linked sources must exist;
- cited sources must support the associated claims;
- summaries must preserve material qualifications;
- generated examples must be labelled when readers could mistake them for observed cases;
- the contributor submitting a change is responsible for what the project publishes.

AI use is neither a reason to reject a contribution nor a substitute for verification.

## 10. Publication checks

The repository includes [`scripts/build_site.py`](../scripts/build_site.py), [`scripts/check_publication.py`](../scripts/check_publication.py), and a GitHub Actions workflow.

The structural publication gate checks:

- whether YAML files parse;
- whether source, claim, and article IDs are unique;
- whether required metadata is present;
- whether claim evidence references registered source IDs;
- whether claim publication targets exist;
- whether article source files exist;
- whether the static publication builds;
- whether relative Markdown and HTML links resolve to repository or generated-site targets.

These checks **cannot establish truth, source quality, or whether a source really supports a sentence**. They prevent avoidable structural publishing errors. Evidence review remains an editorial responsibility.

## 11. Corrections

Corrections are part of the evidence system, not an embarrassment to hide.

A correction should explain:

1. what was wrong or misleading;
2. what changed;
3. which source or reasoning supports the correction;
4. whether other pages or claims are affected.

Where a disputed interpretation cannot be resolved cleanly, present the disagreement rather than forcing certainty.
