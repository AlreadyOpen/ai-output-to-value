# AI Output to Value

**An open, evidence-led guide to AI-assisted work, client readiness, accountability, and business value.**

> **Access is not capability. Output is not completion. Apparent completeness is not proof of substance. Activity is not business value.**

## Umbrella initiative

This project is part of **AlreadyOpen**: https://github.com/AlreadyOpen

The repository currently remains at `helenkwok/ai-output-to-value`. A future transfer to `AlreadyOpen/ai-output-to-value` is an organisational/release decision; repository and umbrella URLs are configuration values in the publication builder.

## Start here

For a first-time business reader:

1. **[Start here — five-minute guide](START-HERE.md)**
2. **[A strong frame is not the same as a finished job](content/frame-vs-finished-work.md)**
3. **[Tool access vs client readiness](content/tool-access-vs-client-readiness.md)**
4. **[Executive guide](content/executive-guide.md)**
5. **[Worked decisions](content/worked-cases.md)**

For a meeting, use the **[one-page meeting brief](content/meeting-brief.md)**.

Deeper analyses cover product discovery, model strategy, architecture and unit economics, AI business-facing capability and judgement, open-source economics, organisational capability, agents, authority, representation, and changing interaction channels. See [`docs/reading-path.md`](docs/reading-path.md).

## The practical question

Generative AI can produce remarkably complete software, reports, research, designs, automations, proposals, presentations, analyses, customer interactions, and other work at very low marginal cost.

The project asks:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output or action to business value?**

This project uses a decision framework:

**Access → Output → Deliverable → Capability → Outcome → Value**

These are six different claims, not mandatory lifecycle stages.

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

## Evidence model

Canonical evidence lives under `data/`. Source and claim records may be split into topic-specific registries, but the builder and checker use the same loader in [`scripts/publication_data.py`](scripts/publication_data.py).

Important factual claims can be traced as:

**Claim → source/version → exact locator → relevant finding → qualification → article location → reviewer/process → independent review status → review record → disposition**

Independent review is actor-neutral. A completed review may be performed by a human, AI system, automated method, specialist toolchain, or hybrid process if it is sufficiently separate from the originating authoring step, directly checks the evidence, applies the stated criteria, and leaves an auditable record.

A completed claim review must record the claim revision, source versions checked, review method, finding, and disposition. This does not require exposing private reasoning.

> **Review completed is not the same as claim accepted.**

`rejected` is a valid review disposition for the evidence history. A launch-critical claim can pass release approval only with an accepting disposition: `accepted`, `accepted_with_qualification`, or `revised_and_accepted`.

See [`docs/evidence-policy.md`](docs/evidence-policy.md).

## Working preview versus reviewed release

The repository has two publication modes.

### Working preview and proposed-release integrity

The normal publication gate builds the full guide plus deeper and advanced working material. It validates structure, types, dates, classifications, evidence links, locators, fragments, and deployment-local links.

The same normal CI run then builds again with `PUBLICATION_MODE=release` and runs [`scripts/check_site_links.py`](scripts/check_site_links.py) against the proposed release artifact.

This intentionally separates two questions:

> **Does the proposed release build work?**
>
> **Has that release been approved?**

The first can pass while independent review and release approval remain pending.

### Reviewed release artifact

Each article declares a `release_scope`:

- `guide` — boss-facing release pages;
- `policy` — evidence/correction policy included with the guide;
- `working` — deeper or advanced research excluded from the reviewed release artifact.

The builder uses the same selected-article manifest for the homepage. In release mode, a homepage reference to a `working` article is rendered as clearly labelled working material rather than a link to a page that the release excludes.

The manual release gate additionally checks that launch-critical claims have completed independent review with inspectable records and an accepting disposition, guide pages are marked ready, policy pages are release-ready, expected release pages exist, and working pages did not enter the artifact.

This records the project's declared controls for a specific revision; it is not a guarantee of truth.

## Publication controls

Normal CI runs regression tests, builds and checks the working preview, then independently builds and link-checks the proposed release artifact. The artifact-only link checker is itself covered by regression tests.

The manual release gate runs the same structural preparation and then executes [`scripts/check_release.py`](scripts/check_release.py). Its tests include the distinction between an accepted review and a completed-but-rejected review.

The architecture example uses consistent denominators and plain-text formula rendering; the executive guide has also been cleaned of authoring instructions and repetitive producer-identity caveats.

## Repository structure

```text
.
├── START-HERE.md
├── README.md
├── content/                         # Core guide + deeper analyses + practical material
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
    └── release-gate.yml
```

## Corrections and responsibility

The initial maintainer is **Helen Kwok**. Evidence-based corrections and counterexamples are welcome. See [`content/corrections.md`](content/corrections.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Current status

**Pre-public-launch / labelled pilot.** The core reading route, actor-neutral evidence model, preview/release split, stricter validators, release-scope artifact, structured independent-review record, release-artifact link checking, and regression tests are in place.

Still open before the first reviewed public release:

- complete independent review records with accepting dispositions for launch-critical claims;
- rendered accessibility/usability and print testing of the actual release pages;
- external-link/source-date review;
- metadata/social-preview assets;
- code/content licensing;
- hosting/deployment choice;
- timing of transfer to `AlreadyOpen/ai-output-to-value`;
- the explicit decision to make the repository/publication public.

A further positive real-world case can improve the guide, but it is not a substitute for finishing the release controls above.

## Licence

A final code/content licensing model has not yet been selected. Code and editorial/reference content may ultimately use different licences.
