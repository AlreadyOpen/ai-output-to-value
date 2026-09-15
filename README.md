# AI Output to Value

**An open, evidence-led guide to AI-assisted work, client readiness, accountability, and business value.**

> **Access is not capability. Output is not completion. Apparent completeness is not proof of substance. Activity is not business value.**

**Live working preview:** https://alreadyopen.github.io/ai-output-to-value/

**Organisation:** [AlreadyOpen](https://github.com/AlreadyOpen) · **Repository:** [AlreadyOpen/ai-output-to-value](https://github.com/AlreadyOpen/ai-output-to-value)

## Start here

For a first-time business reader:

1. **[Start here — five-minute guide](START-HERE.md)**
2. **[A strong frame is not the same as a finished job](content/frame-vs-finished-work.md)**
3. **[Tool access vs client readiness](content/tool-access-vs-client-readiness.md)**
4. **[Worked decisions](content/worked-cases.md)**
5. **[Claim card — decide what evidence is enough](content/claim-card.md)**

For a meeting, use the **[one-page meeting brief](content/meeting-brief.md)**.

For provenance, confidentiality and review responsibility, see **[Who stands behind this guide?](content/provenance.md)**.

Deeper analyses cover product discovery, model strategy, architecture and unit economics, AI business-facing capability and judgement, open-source economics, organisational capability, agents, authority, representation, and changing interaction channels. They are deliberately separated as working/research material rather than being treated as part of the reviewed core guide. See [`docs/reading-path.md`](docs/reading-path.md).

## The practical question

Generative AI can produce remarkably complete software, reports, research, designs, automations, proposals, presentations, analyses, customer interactions, and other work at very low marginal cost.

The project asks:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output or action to business value?**

This project uses a decision framework:

**Access → Output → Deliverable → Capability → Outcome → Value**

These are six different claims, not mandatory lifecycle stages and not a maturity score.

## Decision first

The ladder is a **claim filter**. Start with the decision and require the weakest claim that is sufficient for that decision:

- **keep exploring?** → Output may be enough;
- **may someone rely on it?** → Deliverable;
- **may we sell, operate or support it repeatedly?** → Capability;
- **did it change the result?** → Outcome;
- **should we scale, renew or stop?** → Value.

A strong Access/Output score does not average into partial Deliverable. The [claim card](content/claim-card.md) adds evidence character, actor/authority, measurement, option value and a stop rule.

## Four distinctions that matter

### Tool capability ≠ job substance ≠ delivery capability
A capable agent may generate most of the visible artefact or perform much of a workflow. That does not automatically establish that the result reflects the actual job or that the supplier can repeatedly evaluate, operate, support, maintain, and stand behind it.

### Vibe coding, AI-assisted work, responsible practice, and slop are different dimensions
AI involvement describes how work was produced. Fitness for purpose is a separate assessment.

### Judgement ≠ authority ≠ accountability
AI systems can analyse evidence, compare options, plan, recommend, communicate, persuade, and make bounded decisions. A human decision-maker is not automatically correct because they are human or senior. An AI system is not automatically correct because it is fast or capable.

> **Apply the same standard to human, AI and hybrid work: assess the complete process and its results, not the identity of the producer.**

### Reduced labour ≠ reduced elapsed time ≠ realised financial value
AI may genuinely improve all three, but a gain in one metric should not silently become a claim about another.

## Option value counts

A prototype can create a legitimate **Outcome** by removing uncertainty even when it never becomes an operational service. "We now know not to build this" can be valuable if the experiment changed a real decision cheaply enough.

The worked cases now include both a synthetic 90-day software measurement example and an option-value case where stopping productisation is the correct decision.

## Evidence model

Canonical evidence lives under `data/`. Source and claim records may be split into topic-specific registries, but the builder and checker use the same loader in [`scripts/publication_data.py`](scripts/publication_data.py).

Important factual claims can be traced as:

**Claim → source/version → exact locator → relevant finding → qualification → article location → reviewer/process → independent review status → review record → disposition**

Independent review is actor-neutral. A completed review may be performed by a human, AI system, automated method, specialist toolchain, or hybrid process if it is sufficiently separate from the originating authoring step, directly checks the evidence, applies the stated criteria, and leaves an auditable record.

> **Review completed is not the same as claim accepted.**

`rejected` is a valid review disposition for the evidence history. A launch-critical claim can pass release approval only with an accepting disposition: `accepted`, `accepted_with_qualification`, or `revised_and_accepted`.

Evidence character is also made explicit where useful: public measured evidence, public documented evidence, internal evidence, illustrative material, or editorial synthesis.

See [`docs/evidence-policy.md`](docs/evidence-policy.md).

## Confidentiality

Rigour does not require publishing client names, contracts, production metrics, personal data or proprietary workflows. Internal evidence can remain private while the authorised decision record stays inspectable inside the organisation.

Public teaching cases in this repository are labelled **illustrative**; they are not presented as disguised client incidents. See [`content/provenance.md`](content/provenance.md).

## Working preview versus reviewed release

The public GitHub Pages site currently deploys the **working preview** from `main`. It includes the core guide plus deeper and advanced working material, with publication and evidence-review states kept visible.

Normal CI also builds a proposed release artifact with `PUBLICATION_MODE=release` and checks its local links independently of editorial approval. This separates two questions:

> **Does the proposed release build work?**
>
> **Has that release been approved?**

Each article declares a `release_scope`:

- `guide` — boss-facing release pages;
- `policy` — evidence/provenance/correction policy included with the guide;
- `working` — deeper or advanced research excluded from the reviewed release artifact.

The manual release gate additionally checks that launch-critical claims have completed independent review with inspectable records and an accepting disposition, guide pages are marked ready, policy pages are release-ready, expected release pages exist, and working pages did not enter the artifact.

## Publication controls

Normal CI runs regression tests, builds and checks the working preview, then independently builds and link-checks the proposed release artifact. The artifact-only link checker is itself covered by regression tests.

GitHub Pages is deployed through [`.github/workflows/pages.yml`](.github/workflows/pages.yml). Pushes to `main` automatically publish the working preview; a manual workflow run can select `release`, in which case the release-approval checks run before deployment.

## Repository structure

```text
.
├── START-HERE.md
├── README.md
├── content/                         # Core guide + decision tools + deeper analyses
├── data/
│   ├── articles.yml                 # Publication manifest and release scope
│   ├── sources*.yml                 # Canonical source registries
│   └── claims*.yml                  # Canonical claim registries
├── research/                        # Working notes / pointers, not a second registry
├── docs/
│   ├── evidence-policy.md
│   ├── positioning.md
│   └── reading-path.md
├── scripts/
│   ├── publication_data.py
│   ├── build_site.py
│   ├── check_publication.py
│   ├── check_site_links.py
│   └── check_release.py
├── tests/
│   ├── test_publication_checks.py
│   ├── test_site_links.py
│   └── test_release_checks.py
└── .github/workflows/
    ├── publication-gate.yml
    ├── release-gate.yml
    └── pages.yml
```

## Corrections and responsibility

The initial maintainer is **Helen Kwok**. Evidence-based corrections and counterexamples are welcome. See [`content/provenance.md`](content/provenance.md), [`content/corrections.md`](content/corrections.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Current status

**Public working preview / labelled pilot.** The repository is under AlreadyOpen and the GitHub Pages preview is live.

Still open before the first reviewed release:

- complete independent review records with accepting dispositions for launch-critical claims;
- rendered accessibility/usability and print testing of the actual release pages;
- review all external links and source dates;
- create a dedicated social-preview image asset;
- decide the final code/content licensing model;
- run a small reader test of the core route, claim card and meeting brief;
- explicitly approve and deploy the reviewed release artifact.

A further positive real-world case can improve the guide, but confidential commercial work is not a prerequisite for a rigorous public method.

## Licence

A final code/content licensing model has not yet been selected. Code and editorial/reference content may ultimately use different licences.
