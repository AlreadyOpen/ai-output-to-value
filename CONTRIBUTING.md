# Contributing to AI Output to Value

Thank you for helping improve the project.

This repository is intended to become a business-friendly, evidence-led guide rather than a catalogue of opinions about AI. Contributions are welcome from technical and nontechnical perspectives.

## Good contributions

Examples include stronger primary sources, corrections, useful counterexamples, well-described case studies, clearer explanations, practical decision tools, examples of genuine AI value, examples where work moved rather than disappeared, and accessibility/usability improvements.

## Before adding a source

Check:

1. Does the source exist and remain accessible?
2. What type of source is it?
3. What claim does it actually support?
4. Where exactly does it support that claim?
5. What is its scope?
6. What are the important limitations?
7. Is there newer work that qualifies or supersedes it?

Do not add a source merely because its publisher is prestigious or its headline agrees with the project.

## Source records

Canonical source records live under `data/`:

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

## Claim-level traceability

Important factual claims should also be registered under `data/claims*.yml`:

```yaml
- id: stable-claim-id
  claim_text: The wording the project intends to publish.
  status: supported
  launch_critical: true
  evidence:
    - source_id: registered-source-id
      source_version: source version/date used
      locator: Exact section, page, table, figure, or named subsection.
      relevant_finding: What this location establishes.
      qualification: What must remain visible to avoid overclaiming.
  published_in:
    - file: content/example.md
      locator: "## Exact heading"
  reviewer: reviewer or review process
  reviewed: 2026-09-14
  independent_review_status: pending
```

`launch_critical` must be an explicit Boolean. Omission is not a way to bypass review.

## Independent review

Independent review is actor-neutral. It may be performed by a human, AI system, automated method, specialist toolchain, or hybrid process.

The review should be sufficiently separate from the originating authoring step, inspect the relevant evidence directly, apply the same stated criteria, preserve qualifications, and leave an auditable record.

When `independent_review_status: completed`, add:

```yaml
review_record:
  claim_revision: commit, tag, content hash, or other stable revision
  source_versions_checked:
    - source/version actually inspected
  method: What the review process checked.
  finding: What it concluded about support, scope, and qualifications.
  disposition: accepted_with_qualification
```

Allowed dispositions are `accepted`, `accepted_with_qualification`, `revised_and_accepted`, and `rejected`.

A completed review record should expose what was checked without exposing private chain-of-thought.

## Practitioner stories and community discussions

Real-world stories can reveal mechanisms before formal research measures them well, but they must remain labelled as accounts, reports, discussions, or allegations where appropriate.

Do not convert votes, comments, repetition, or generated summaries into prevalence evidence. Keep fictional teaching cases distinct from reported accounts.

## AI-assisted contributions are welcome

AI may be used to research, draft, reorganise, translate, test, or review a contribution. The acceptance standard is the same regardless of actor:

- links must work;
- claims must match their sources;
- qualifications must remain visible;
- constructed examples must be labelled;
- fabricated citations/details must be removed;
- responsibility and recourse for the submitted change must remain clear.

## Editorial style

Write for an intelligent reader who may not work in software or AI. Prefer concrete distinctions, plain language, neutral business framing, visible evidence, and questions that improve real decisions.

Avoid insulting managers, developers, consultants, nontechnical builders, or AI users; treating AI-generated as synonymous with bad; treating human-written as synonymous with good; universal productivity claims from one study; or marketing language without evidence.

## Reading and release scope

The first-time business route is intentionally narrow. New material should not automatically enter the reviewed release.

Article `release_scope` values are:

- `guide` — boss-facing reviewed release pages;
- `policy` — evidence/correction policy shipped with the guide;
- `working` — deeper or advanced working material excluded from the reviewed release artifact.

Broader analyses remain available in the working preview.

## Website changes

For publication UI changes, preserve keyboard accessibility, readable contrast, reduced-motion preferences, narrow/wide layout quality, and usable print output.

Do not validate only an intermediate HTML generator. The supported publication artifact includes the Python publication layer **plus** the React/shadcn/Base UI/Tailwind enhancement, generated machine surfaces, WebMCP scope refinement, and pdfcn/Takumi PDF output.

## Publication checks

Before submitting, run the same finished-artifact path used by CI and Pages:

```bash
python -m pip install -r requirements-dev.txt

cd web
npm install --no-audit --no-fund
npm run pdfcn:sync
npm run typecheck
cd ..

python -m unittest discover -s tests -p 'test_*.py'
python scripts/claim_gate.py toolkit/claim.example.json --json

cd packages/mcp
npm install --no-audit --no-fund
npm test
cd ../..

python scripts/build_with_ui.py
python scripts/check_publication.py
python scripts/check_site_links.py

PUBLICATION_MODE=release python scripts/build_with_ui.py
python scripts/check_site_links.py
```

`scripts/build_site.py` is an internal/intermediate publication generator used by the finished build pipeline. Do **not** treat its direct output as the deployable website or reviewed release candidate.

The preview checks structure, traceability, local links, and interaction-integrity rules. They do not approve a release.

The manual release workflow uses the same `build_with_ui.py` deployable pipeline in `PUBLICATION_MODE=release` and then applies `scripts/check_release.py` to the declared review and artifact-scope rules.

## Corrections

A good correction explains what is wrong or misleading, what the source actually supports, the proposed replacement wording, and whether related pages, claims, or source records should change.

If evidence is genuinely contested, prefer showing the disagreement over forcing false consensus.

## Licence

The repository has not yet selected its final code/content licensing model. Avoid contributing material that cannot legally be redistributed under an eventual open licence.
