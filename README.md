# AI Output to Value

**An open, evidence-led guide to AI-assisted work, client readiness, accountability, and business value.**

> **Access is not capability. Output is not completion. Apparent completeness is not proof of substance. Activity is not business value.**

## Start here

If you are a business reader, do **not** read the repository front-to-back.

1. **[Start here — five-minute guide](START-HERE.md)**
2. **[Tool access vs client readiness](content/tool-access-vs-client-readiness.md)**
3. **[Executive guide](content/executive-guide.md)**

That is the primary reading path.

The repository also contains deeper analyses on open source, technical capability, company actors and AI agents, representation channels, retail transformation, and organisational value. They support the broader framework but are **not prerequisites** for understanding the main argument. See [`docs/reading-path.md`](docs/reading-path.md).

## The practical question

Generative AI can produce remarkably complete software, reports, research, designs, automations, and other work at very low marginal cost.

The project asks a narrower management question:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output to business value?**

A useful progression is:

**Access → Output → Deliverable → Capability → Outcome → Value**

| Stage | Question |
| --- | --- |
| **Access** | Do we have the model, agent, API, subscription, or tool? |
| **Output** | Did it generate something useful-looking or functional? |
| **Deliverable** | Is it fit for the intended purpose and acceptance criteria? |
| **Capability** | Can the organisation repeatedly verify, operate, support, maintain, and improve it? |
| **Outcome** | What actually changed? |
| **Value** | Was that outcome worth the full cost, risk, and trade-offs? |

The model is not a maturity score. A prototype may intentionally stop early. Assurance should match the consequence of being wrong.

## Three distinctions that matter

### Tool capability ≠ job substance ≠ delivery capability

A capable agent may generate most of the visible artefact. That does not automatically establish that the result reflects the actual client's requirements or that the supplier can verify, operate, support, maintain, and stand behind it.

### Vibe coding ≠ AI-assisted work ≠ AI slop

- **Vibe coding** describes a way of working.
- **AI-assisted work** describes AI involvement in the workflow.
- **AI slop / workslop** describes a quality problem.

They are not three levels of the same thing.

### Faster generation ≠ faster workflow ≠ realised financial value

AI may genuinely reduce all three. The project simply keeps them separate so that a gain in one stage is not automatically reported as a gain in another.

## Evidence model

This project is intended to be more than an “awesome links” list.

Source registers record:

**Source → evidence type → supported topics → scope → limitations → review date**

For important published factual claims, [`data/claims.yml`](data/claims.yml) adds:

**Claim → exact source locator → relevant finding → qualification → publication location → reviewer → review status**

See [`docs/evidence-policy.md`](docs/evidence-policy.md).

The current claim register intentionally marks its first external-source checks as **AI-assisted initial checks with human review pending**. The repository should not imply independent human verification that has not occurred.

## Publication gate

A small GitHub Actions publication gate runs:

```bash
python scripts/check_publication.py
```

It checks:

- YAML validity;
- unique source and claim IDs;
- required source metadata;
- claim references to registered sources;
- publication-target existence;
- broken local Markdown/HTML links.

These checks prevent structural publishing mistakes. **They do not establish truth or source quality.**

## Deeper reading

The broader material is organised by question in [`docs/reading-path.md`](docs/reading-path.md), including:

- strong frames versus finished work;
- AI and technical capability;
- source code and open-source economics;
- humans, agents, authority, and instruments inside a company;
- dynamic valuation of organisational capabilities;
- representation channels and the e-commerce / brick-and-mortar analogy.

These pages should remain supporting analysis unless they are necessary to answer the primary business question.

## Repository structure

```text
.
├── START-HERE.md
├── README.md
├── CONTRIBUTING.md
├── index.html
├── styles.css
├── content/                 # Core guide + deeper analyses
├── data/
│   ├── claims.yml           # Claim-level traceability
│   ├── sources.yml          # Core source register
│   └── *-sources.yml        # Topic-specific source registers
├── docs/
│   ├── evidence-policy.md
│   ├── positioning.md
│   └── reading-path.md
├── scripts/
│   └── check_publication.py
└── .github/workflows/
    └── publication-gate.yml
```

## Contributing

Contributions are welcome, especially strong sources, corrections, counterexamples, clearer executive explanations, case studies, and examples of both successful and unsuccessful AI-assisted workflows.

Before submitting, see [`CONTRIBUTING.md`](CONTRIBUTING.md) and run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/check_publication.py
```

## Current status

**Pre-public-launch foundation.** The core message and reading path are in place. Evidence is being migrated from topic-level source registration toward claim-level traceability, and launch-critical claims still require independent human review.

## Licence

A final code/content licensing model has not yet been selected. Code and editorial/reference content may ultimately use different licences.
