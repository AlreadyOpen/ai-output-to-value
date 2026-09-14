# AI Output to Value

**An open, evidence-led guide to AI-assisted work, client readiness, accountability, and business value.**

> **Access is not capability. Output is not completion. Apparent completeness is not proof of substance. Activity is not business value.**

## Start here

If you are a business reader, do **not** read the repository front-to-back.

1. **[Start here — five-minute guide](START-HERE.md)**
2. **[A strong frame is not the same as a finished job](content/frame-vs-finished-work.md)**
3. **[Tool access vs client readiness](content/tool-access-vs-client-readiness.md)**
4. **[Executive guide](content/executive-guide.md)**
5. **[Worked decisions](content/worked-cases.md)**

For a meeting, use the **[one-page meeting brief](content/meeting-brief.md)**.

Deeper analyses cover product discovery, model capability versus strategy, architecture and unit economics, AI business-facing capability and judgement, open-source economics, organisational capability, agents, authority, representation, and changing interaction channels. See [`docs/reading-path.md`](docs/reading-path.md).

## The practical question

Generative AI can produce remarkably complete software, reports, research, designs, automations, proposals, presentations, analyses, customer interactions, and other work at very low marginal cost.

The project asks:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output or action to business value?**

This project uses a decision framework:

**Access → Output → Deliverable → Capability → Outcome → Value**

These are **six different claims**, not mandatory lifecycle stages. A disposable prototype can create a valuable learning outcome without becoming an operational service.

## Four distinctions that matter

### Tool capability ≠ job substance ≠ delivery capability

A capable agent may generate most of the visible artefact or perform much of a workflow. That does not automatically establish that the result reflects the actual job or that the supplier can repeatedly verify, operate, support, maintain, and stand behind it.

### Vibe coding, AI-assisted work, responsible practice, and slop are different dimensions

- **Vibe coding** describes a way of working.
- **AI-assisted work** means AI contributed to producing or performing the work.
- **Responsible AI-assisted practice** adds proportionate evaluation, ownership, and controls for the intended use.
- **AI slop / workslop** describes a quality problem.

They can overlap. Authorship or workflow does not determine fitness for purpose by itself.

### Judgement ≠ authority ≠ accountability

AI systems can analyse evidence, compare options, plan, recommend, communicate, persuade, and make bounded decisions. Those are capabilities to evaluate for the task; they are not inherently human-only.

A human decision-maker is not automatically correct because they are human or senior. An AI system is not automatically correct because it is fast or capable. **Human-in-the-loop is a control pattern, not a quality certificate.**

> **Apply the same standard to human, AI and hybrid work: assess the complete process and its results, not the identity of the producer.**

### Reduced labour ≠ reduced elapsed time ≠ realised financial value

AI may genuinely improve all three. The project keeps the units separate so a gain in one metric is not silently reported as a gain in another.

## Evidence model

This project is intended to be more than an “awesome links” list.

Canonical evidence lives under `data/`. Source and claim records may be split into topic-specific registries, but the builder and checker use the same shared loader in [`scripts/publication_data.py`](scripts/publication_data.py).

Important factual claims can therefore be traced as:

**Claim → source/version → exact locator → relevant finding → qualification → article location → reviewer → review status**

The generated evidence page gives each claim a stable anchor and links back to the articles using it. Generated article pages also show the claim records currently attached to that article.

See [`docs/evidence-policy.md`](docs/evidence-policy.md).

## Publication status is explicit

Generated article pages distinguish:

- **publication state** — Draft, Research draft, Editorial review in progress, Reviewed for publication, etc.;
- **Last updated** date;
- **evidence review state** for connected claims.

A date does not mean every factual statement has been independently approved.

The current launch-critical claims deliberately remain marked as pending editorial review. That is disclosure of the project’s current release process, not a claim that human review is intrinsically superior to other assurance methods.

## Publication layer

Markdown and YAML remain the maintained source. [`scripts/build_site.py`](scripts/build_site.py) generates static HTML into `site/`:

- styled article pages;
- article index and reading routes;
- bidirectional claim/evidence navigation;
- reader-facing review/status labels;
- mobile navigation;
- print-friendly layouts;
- links back to the source version used for the build.

No client-side application framework is required.

## Two different gates

A green build should not be mistaken for publication approval.

### Preview / structural gate

The normal [`publication-gate.yml`](.github/workflows/publication-gate.yml) runs:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python scripts/build_site.py
python scripts/check_publication.py
```

The regression tests and checker reject known structural defects including empty evidence values, invalid claim locations, completed review states without reviewer/date records, broken fragments, deployment-escaping links, and reserved article slugs.

A green preview gate means the draft **builds and is structurally consistent**. It does not establish factual truth or publication approval.

### Release approval gate

The manual [`release-gate.yml`](.github/workflows/release-gate.yml) additionally runs [`scripts/check_release.py`](scripts/check_release.py).

Under the current release policy it blocks release when:

- a launch-critical claim has not completed the declared editorial review;
- the review record is incomplete; or
- a core article has not been marked ready for publication.

This is a project publication control, not a guarantee of truth.

## Repository structure

```text
.
├── START-HERE.md
├── README.md
├── content/                         # Core guide + deeper analyses + practical material
├── data/
│   ├── articles.yml                 # Publication manifest
│   ├── sources*.yml                 # Canonical source registries
│   └── claims*.yml                  # Canonical claim registries
├── research/                        # Working notes / pointers, not a second registry
├── docs/
│   ├── evidence-policy.md
│   ├── positioning.md
│   └── reading-path.md
├── scripts/
│   ├── publication_data.py          # Shared evidence-loading contract
│   ├── build_site.py
│   ├── check_publication.py         # Preview / structural checks
│   └── check_release.py             # Release-policy checks
├── tests/
│   └── test_publication_checks.py   # Negative regression fixtures
└── .github/workflows/
    ├── publication-gate.yml
    └── release-gate.yml
```

`site/` is generated during the publication build.

## Corrections and editorial responsibility

The initial maintainer is **Helen Kwok**. Evidence-based corrections and counterexamples are welcome.

See [`content/corrections.md`](content/corrections.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Current status

**Pre-public-launch / pilot.** The reading route, evidence model, claim backlinks, static build, structural regression tests, and distinct preview/release gates are in place. Launch-critical factual claims still require the repository’s declared editorial approval; accessibility review, external-link/date review, licensing, hosting, and public-release decisions remain open.

## Licence

A final code/content licensing model has not yet been selected. Code and editorial/reference content may ultimately use different licences.
