# First reviewed release — public acceptance bar

The public site remains a **working preview** until this checklist is satisfied. Passing CI or rendering a green Claim Gate result is not the same as approving the publication.

## Scope boundary — reviewed method ≠ tool distribution

This checklist approves the **reviewed method/publication artefact**. **Tooling publication is not a prerequisite** unless a specific checked requirement below genuinely depends on a tool surface that is part of the reviewed artefact.

In particular, npm publication, native MCP packaging, broad WebMCP/browser-agent compatibility, GitHub Action tagging/marketplace distribution, and installable agent-skill/wrapper distribution are tracked separately in [`tooling-distribution.md`](tooling-distribution.md).

The Claim Gate, schema, example records, and rendered browser/PDF artefacts may still be required here because they are part of the reviewed publication. That requirement does **not** mean every wrapper, package, transport, host, or distribution channel is operationally supported.

The reverse boundary matters too: publishing or tagging a tool does **not** mean the cited empirical claims, terminology, examples, or reviewed publication artefact have completed independent review.

## Required core instrument

- [ ] The six-claim stop-rule framework is stable enough for the release.
- [ ] The deterministic Claim Gate, schema, and example records included in the reviewed artefact are internally consistent; no separate package/registry publication is implied.
- [ ] The Claim Gate clearly states that `PASS` evaluates the supplied record and is **not an audit of the underlying system or evidence**.
- [ ] The one-page meeting brief renders and prints correctly.
- [ ] The private workbook is available for confidential organisational use.

## Required teaching material

- [ ] Five worked decisions are included and clearly labelled illustrative where invented.
- [ ] The website prototype demonstrates a weaker decision passing and a stronger decision blocking without changing the artefact.
- [ ] The option-value case shows that learning can be an Outcome without forcing productisation.
- [ ] The software measurement case uses an explicit baseline, after-period, metric definitions, cost boundary, and confound/attribution qualification.

## Required evidence review

The release gate derives review scope from the publication manifest. **Every claim published in a `guide` or `policy` source is review-critical by construction**, even if its record says `launch_critical: false`. Working-only claims enter the review scope when explicitly marked `launch_critical: true`.

Every review-critical claim must have a completed independent review record and an accepting disposition (`accepted`, `accepted_with_qualification`, or `revised_and_accepted`). This includes the prominent evidence used in the first-time reading route, including:

- [ ] METR's early-2025 experienced open-source developer study;
- [ ] the Microsoft/GitHub Copilot controlled HTTP-server experiment;
- [ ] Noy and Zhang's professional-writing experiment;
- [ ] Dell'Acqua et al.'s consulting experiment;
- [ ] DORA software-delivery evidence;
- [ ] the Harvard Business Review workflow source;
- [ ] the Harvard Business Review teamwork source where used in core guidance;
- [ ] Brynjolfsson, Li and Raymond where the customer-support study is used;
- [ ] any other claim published in a `guide` or `policy` source, or explicitly marked `launch_critical: true`.

Every evidence entry must also identify the inspected `source_version` so the reviewed source state can be reconstructed.

A source logo or citation is not itself independent review.

## Publication quality

- [ ] Core-route pages receive rendered desktop/mobile accessibility and usability checks.
- [ ] The generated PDF meeting brief receives a real print/render check.
- [ ] External links and source dates are reviewed.
- [ ] The dedicated social-preview image is present.
- [ ] At least one non-technical sponsor completes the [human-kit reader test](human-kit-reader-test.md) using only Start Here, the eight questions, Claim Card / meeting brief, and evidence; the test does not require Claim Gate, the schema, MCP tooling, or JSON.
  - Give the reader this deliberately misleading summary: **“Output: strong; Deliverable: almost; Operating capability: not yet; Outcome / Value: unknown.”** Ask: **“What is wrong with this assessment, and how would you rewrite it?”**
  - A passing response must reject one project-wide ladder and restate separate **decision + intended use + subject/scope + required claim/evidence** records. It should recognise that the same project can legitimately reach different conclusions for different decisions. The probe and pass criteria are in the [human-kit reader test](human-kit-reader-test.md#misleading-summary-probe).
- [ ] Working/research essays remain visibly separated from the release guide and do not leak into the reviewed artifact.

## Governance and reuse

- [x] Code licence is selected and published (Apache-2.0, `LICENSE`).
- [x] Editorial/reference-content licence is selected and published; it may differ from the code licence (CC BY 4.0, `LICENSE-CONTENT`).
- [ ] Provenance, corrections, confidentiality, and evidence policy are included.
- [ ] The release commit/tag is explicit and reproducible.
- [ ] The manual release approval gate passes before deployment.

Tooling/distribution milestones remain in [`tooling-distribution.md`](tooling-distribution.md) and do not become publication blockers merely because a surface exists in the repository.

## Release statement

Only after the checklist is satisfied should the header move beyond **Working preview**. Even then, the project is an open decision method, not an industry standard, certification, audit opinion, or guarantee that any particular project is fit for use.
