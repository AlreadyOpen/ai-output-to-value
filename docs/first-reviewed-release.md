# First reviewed release — public acceptance bar

The public site remains a **working preview** until this checklist is satisfied. Passing CI or rendering a green Claim Gate result is not the same as approving the publication.

## Required core instrument

- [ ] The six-claim stop-rule framework is stable enough for the release.
- [ ] The deterministic Claim Gate, schema, and example records are internally consistent.
- [ ] The Claim Gate clearly states that `PASS` evaluates the supplied record and is **not an audit of the underlying system or evidence**.
- [ ] The one-page meeting brief renders and prints correctly.
- [ ] The private workbook is available for confidential organisational use.

## Required teaching material

- [ ] Five worked decisions are included and clearly labelled illustrative where invented.
- [ ] The website prototype demonstrates a weaker decision passing and a stronger decision blocking without changing the artefact.
- [ ] The option-value case shows that learning can be an Outcome without forcing productisation.
- [ ] The software measurement case uses an explicit baseline, after-period, metric definitions, cost boundary, and confound/attribution qualification.

## Required evidence review

Launch-critical claims must have completed independent review records and an accepting disposition (`accepted`, `accepted_with_qualification`, or `revised_and_accepted`). At minimum, the first reviewed release should include accepted review records for the flagship claims relying on:

- [ ] DORA software-delivery evidence;
- [ ] the Harvard Business Review workflow source;
- [ ] the Harvard Business Review teamwork source where used in core guidance;
- [ ] Brynjolfsson, Li and Raymond where the customer-support study is used;
- [ ] any other claim marked `launch_critical: true` by the release gate.

A source logo or citation is not itself independent review.

## Publication quality

- [ ] Core-route pages receive rendered desktop/mobile accessibility and usability checks.
- [ ] The generated PDF meeting brief receives a real print/render check.
- [ ] External links and source dates are reviewed.
- [ ] The dedicated social-preview image is present.
- [ ] A small reader test covers Start Here, Claim Gate, Claim Card, worked decisions, and the meeting brief.
  - Give the reader this deliberately misleading summary: **“Output: strong; Deliverable: almost; Operating capability: not yet; Outcome / Value: unknown.”** Ask: **“What is wrong with this assessment, and how would you rewrite it?”**
  - A passing response must reject one project-wide ladder and restate separate **decision + intended use + subject/scope + required claim/evidence** records. It should recognise that the same project can legitimately receive different gate results for different decisions.
- [ ] Working/research essays remain visibly separated from the release guide and do not leak into the reviewed artifact.

## Governance and reuse

- [x] Code licence is selected and published (Apache-2.0, `LICENSE`).
- [x] Editorial/reference-content licence is selected and published; it may differ from the code licence (CC BY 4.0, `LICENSE-CONTENT`).
- [ ] Provenance, corrections, confidentiality, and evidence policy are included.
- [ ] The release commit/tag is explicit and reproducible.
- [ ] The manual release approval gate passes before deployment.

## Release statement

Only after the checklist is satisfied should the header move beyond **Working preview**. Even then, the project is an open decision method, not an industry standard, certification, audit opinion, or guarantee that any particular project is fit for use.
