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

Broader analyses cover product ideation versus discovery, model capability versus product strategy, architecture and unit economics, AI business-facing capability and judgement, open source, technical capability, company actors and AI agents, representation channels, retail transformation, and organisational capability. See [`docs/reading-path.md`](docs/reading-path.md).

## The practical question

Generative AI can produce remarkably complete software, reports, research, designs, automations, proposals, presentations, analyses, customer interactions, and other work at very low marginal cost.

The project asks:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output or action to business value?**

This project uses a decision framework:

**Access → Output → Deliverable → Capability → Outcome → Value**

These are **six different claims**, not six mandatory steps. A disposable prototype can create a valuable learning outcome without becoming an operational service.

A useful reverse-planning question is:

> **What outcome do we need, and what evidence, capability, and work would make that outcome plausible?**

## Four distinctions that matter

### Tool capability ≠ job substance ≠ delivery capability

A capable agent may generate most of the visible artefact or perform much of the workflow. That does not automatically establish that the result reflects the actual client's requirements or that the supplier can verify, operate, support, maintain, and stand behind it.

### Vibe coding, AI-assisted work, responsible practice, and slop are different dimensions

- **Vibe coding** describes a way of working.
- **AI-assisted work** means AI contributed to producing or performing the work.
- **Responsible AI-assisted practice** adds proportionate evaluation, ownership, and controls for the intended use.
- **AI slop / workslop** describes a quality problem.

They can overlap. A vibe-coded artefact is AI-assisted; whether it is fit for purpose is a separate assessment.

### Judgement ≠ authority ≠ accountability

AI systems can analyse evidence, compare options, plan, recommend, communicate, persuade, and make bounded decisions. Those are capabilities to evaluate for the task; they are not inherently human-only.

- **Judgement / evaluation** asks which option appears better under the available evidence and goals.
- **Authority** asks who or what is permitted to act or bind the organisation.
- **Accountability / recourse** asks where responsibility for the outcome sits and who must correct failures.

A human decision-maker is not automatically correct because they are human or senior. An AI system is not automatically correct because it is fast or capable. **Human-in-the-loop is a control pattern, not a quality certificate.** See [`content/ai-business-capability-and-judgement.md`](content/ai-business-capability-and-judgement.md).

### Reduced labour ≠ reduced elapsed time ≠ realised financial value

AI may genuinely improve all three. The project keeps the units separate so that a gain in one metric is not automatically reported as a gain in another.

## Evidence model

This project is intended to be more than an “awesome links” list.

The canonical [`data/sources.yml`](data/sources.yml) identifies publications and records source type, supported topics, scope, limitations, review date, and availability status where relevant.

For important published factual claims, [`data/claims.yml`](data/claims.yml) records:

**Claim → exact source locator → relevant finding → qualification → publication location → reviewer → review status**

See [`docs/evidence-policy.md`](docs/evidence-policy.md).

The current claim register intentionally marks its initial external-source checks as **AI-assisted checks with human editorial review pending**. This is a disclosure of the repository's present review process, not a claim that human review is inherently superior to automated or model-based assurance.

## Publication layer

Markdown and YAML remain the maintained source. [`scripts/build_site.py`](scripts/build_site.py) generates normal static HTML pages into `site/`:

- styled article pages;
- article index and reading routes;
- claim-level evidence page;
- mobile navigation;
- print-friendly layouts;
- links back to the raw source for inspection.

This keeps the publication lightweight: no client-side application framework is required.

## Publication gate

GitHub Actions runs:

```bash
python scripts/build_site.py
python scripts/check_publication.py
```

The gate checks:

- YAML validity;
- unique source, claim, article IDs and article slugs;
- required evidence metadata;
- claim references to registered sources;
- article source existence;
- publication-target existence;
- built-site presence;
- broken local Markdown/HTML links.

These checks prevent structural publishing mistakes. **They do not establish factual truth or source quality.**

## Repository structure

```text
.
├── START-HERE.md
├── README.md
├── CONTRIBUTING.md
├── index.html
├── styles.css
├── publication.css
├── content/                 # Core guide + deeper analyses + meeting/corrections material
├── data/
│   ├── articles.yml         # Publication manifest
│   ├── claims.yml           # Claim-level traceability
│   ├── sources.yml          # Canonical source register
│   └── *-sources.yml        # Topic-specific research registers
├── docs/
│   ├── evidence-policy.md
│   ├── positioning.md
│   └── reading-path.md
├── scripts/
│   ├── build_site.py
│   └── check_publication.py
└── .github/workflows/
    └── publication-gate.yml
```

`site/` is generated during the publication build.

## Corrections and editorial responsibility

The initial maintainer is **Helen Kwok**. Evidence-based corrections and counterexamples are explicitly welcome.

See [`content/corrections.md`](content/corrections.md) for the correction route and [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidance.

## Current status

**Pre-public-launch.** The core reading route, evidence model, static publication build, and structural checks are in place. Launch-critical external claims still require the repository's independent editorial review, and licensing/hosting remain open decisions.

## Licence

A final code/content licensing model has not yet been selected. Code and editorial/reference content may ultimately use different licences.
