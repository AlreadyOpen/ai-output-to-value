# Contributing to AI Output to Value

Thank you for helping improve the project.

This repository is intended to become a business-friendly, evidence-led guide rather than a catalogue of opinions about AI. Contributions are welcome from technical and nontechnical perspectives.

## Good contributions

Examples include:

- a strong primary or official source;
- a correction to a claim that overstates the evidence;
- a useful counterexample;
- a case study with enough context to understand what actually changed;
- a clearer explanation for a nontechnical decision-maker;
- a practical framework or meeting question;
- an example of AI creating genuine value;
- an example where apparent productivity moved work elsewhere;
- accessibility, usability, or visual improvements to the website.

## Before adding a source

Please check:

1. **Does the source exist and remain accessible?**
2. **What type of source is it?** Research, official guidance, industry research, vendor guidance, case study, practitioner analysis, or community account?
3. **What claim does it actually support?**
4. **Where exactly does it support that claim?** Record a page, section, table, figure, paragraph, or other stable locator when possible.
5. **What is the scope?** Population, task, organisation, domain, or conditions?
6. **What are the important limitations?**
7. **Is there newer work that qualifies or supersedes it?**

Do not add a source simply because its publisher is prestigious or because its headline supports the project's current position.

## Source register format

Source records live in `data/*.yml` files.

A typical entry looks like:

```yaml
- id: short-stable-id
  title: Source title
  publisher: Publisher or author
  url: https://example.com/source
  evidence_type: research_study
  supports:
    - concise_topic_identifier
  scope: What the evidence actually covers.
  limitations: What readers must know before generalising it.
  reviewed: 2026-09-14
```

The `supports` list is a discovery aid. It does not by itself prove that a particular published sentence is supported.

## Claim-level traceability

Important factual claims—especially quantitative claims, legal or governance claims, current vendor/product claims, and claims used on the home page—should also be registered in the canonical `data/claims*.yml` files.

A typical claim record looks like:

```yaml
- id: stable-claim-id
  claim_text: The wording the project intends to publish.
  status: supported
  launch_critical: true
  evidence:
    - source_id: registered-source-id
      locator: Exact section, page, table, figure, or named subsection.
      relevant_finding: What this location establishes.
      qualification: What must remain visible to avoid overclaiming.
  published_in:
    - file: index.html
      locator: "#evidence"
  reviewer: Transparent reviewer or review process
  reviewed: 2026-09-14
  independent_review_status: pending
```

Do not mark independent review as completed merely because the same authoring process checked its own work. **Independence is a property of the review process, not the identity of the reviewer.** An independent review may be performed by a human, AI system, automated method, or hybrid process if it is sufficiently separate from the originating work and applies the stated evidence criteria. Record the reviewer/process transparently.

See [`docs/evidence-policy.md`](docs/evidence-policy.md) for evidence classes, claim statuses, and editorial rules.

## Practitioner stories and community discussions

Real-world stories can reveal important organisational mechanisms long before formal research catches up. They are welcome, but must remain clearly labelled.

When adding an anecdotal source:

- describe it as an account, report, discussion, or allegation where appropriate;
- do not convert votes, comments, or repetition into prevalence evidence;
- do not identify companies based on speculation in comments;
- include meaningful counterarguments when they materially change the lesson;
- extract the decision or governance question rather than endorsing personal conflict.

## AI-assisted contributions are welcome

You may use AI tools to research, draft, reorganise, translate, or improve a contribution.

The acceptance standard is the same regardless of the tool used:

- verify the links;
- verify the claims against the linked sources;
- preserve material qualifications;
- label constructed examples when they could be mistaken for observed cases;
- remove fabricated citations, details, or statistics;
- be prepared to explain and revise what you submit.

The submitting actor or maintainer remains responsible for the change under the repository's governance process.

## Editorial style

Write for an intelligent reader who may not work in software or AI.

Prefer:

- concrete distinctions;
- short explanations before specialist detail;
- neutral business language;
- questions readers can use in real decisions;
- acknowledgement of benefits as well as risks;
- precise claims with visible evidence.

Avoid:

- insulting managers, developers, consultants, nontechnical builders, or AI users;
- treating “AI-generated” as a synonym for “bad”;
- treating “human-written” as a synonym for “good”;
- assuming every prototype needs production-level assurance;
- presenting an illustrative number as measured evidence;
- universal productivity claims based on one study or case;
- marketing language without evidence.

## Reading-path discipline

The first-time business reading path is intentionally narrow. New material should not automatically be added to the home page or README.

Before promoting a topic into the primary path, ask whether it is necessary to answer:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output to business value?**

Broader analyses can remain valuable as deeper reading. See [`docs/reading-path.md`](docs/reading-path.md).

## Website changes

For changes to `index.html` or `styles.css`:

- keep the site usable without JavaScript unless a feature genuinely needs it;
- preserve keyboard accessibility;
- preserve readable contrast;
- respect `prefers-reduced-motion`;
- test narrow and wide layouts;
- avoid decorative complexity that makes the guide harder to read.

## Publication checks

Before submitting, run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/check_publication.py
```

The check validates source/claim structure and local links. It does **not** determine whether a factual claim is true or whether a source is persuasive enough.

## Corrections

Corrections are encouraged.

A good correction explains:

- what is wrong or misleading;
- what the source actually supports;
- the proposed replacement wording;
- whether related pages, claim records, or source records should also change.

If the evidence is genuinely contested, prefer showing the disagreement over forcing a false consensus.

## Licence

The repository has not yet selected its final code/content licensing model. Please avoid contributing material that cannot legally be redistributed under an open licence once that decision is made.
