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
4. **What is the scope?** Population, task, organisation, domain, or conditions?
5. **What are the important limitations?**
6. **Is there newer work that qualifies or supersedes it?**

Do not add a source simply because its publisher is prestigious or because its headline supports the project's current position.

## Source register format

Sources live in [`data/sources.yml`](data/sources.yml).

A typical entry looks like:

```yaml
- id: short-stable-id
  title: Source title
  publisher: Publisher or author
  url: https://example.com/source
  evidence_type: research_study
  supports:
    - concise_claim_identifier
  scope: What the evidence actually covers.
  limitations: What readers must know before generalising it.
  reviewed: 2026-09-14
```

See [`docs/evidence-policy.md`](docs/evidence-policy.md) for the evidence classes and editorial rules.

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

The contributor is responsible for the submitted change.

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

## Website changes

For changes to `index.html` or `styles.css`:

- keep the site usable without JavaScript unless a feature genuinely needs it;
- preserve keyboard accessibility;
- preserve readable contrast;
- respect `prefers-reduced-motion`;
- test narrow and wide layouts;
- avoid decorative complexity that makes the guide harder to read.

## Corrections

Corrections are encouraged.

A good correction explains:

- what is wrong or misleading;
- what the source actually supports;
- the proposed replacement wording;
- whether related pages or source records should also change.

If the evidence is genuinely contested, prefer showing the disagreement over forcing a false consensus.

## Licence

The repository has not yet selected its final code/content licensing model. Please avoid contributing material that cannot legally be redistributed under an open licence once that decision is made.
