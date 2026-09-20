# AI Output to Value

**An open, evidence-led guide and decision method for AI-assisted work, client readiness, accountability, and business value.**

> **Access is not capability. Output is not completion. Apparent completeness is not proof of substance. Activity is not business value.**

**Live working preview:** https://alreadyopen.github.io/ai-output-to-value/

**Organisation:** [AlreadyOpen](https://github.com/AlreadyOpen) · **Repository:** [AlreadyOpen/ai-output-to-value](https://github.com/AlreadyOpen/ai-output-to-value)

## Start here

For a first-time business reader or review meeting:

1. **[Start here — five-minute guide](START-HERE.md)**
2. **[Interactive Claim Gate](https://alreadyopen.github.io/ai-output-to-value/tools/claim-gate.html)** — decision → required claim → `PASS` / `BLOCKED` / `INSUFFICIENT EVIDENCE`.
3. **[Filled sample claim records](toolkit/samples/README.md)** — see the same website pass Explore and block Operate.
4. **[Worked decisions](content/worked-cases.md)** — including software measurement and option value.
5. **[One-page meeting brief](content/meeting-brief.md)**.

For confidential organisational use, copy the **[private workbook](toolkit/private-workbook/README.md)** instead of publishing a client case. The built site also provides `downloads/ai-output-to-value-private-workbook.zip`.

For provenance, confidentiality and review responsibility, see **[Who stands behind this guide?](content/provenance.md)**.

Deeper analyses cover product discovery, model strategy, architecture and unit economics, AI business-facing capability and judgement, open-source economics, organisational capability, agents, authority, representation, and changing interaction channels. They are deliberately separated as working/research material rather than competing with the core method. See [`docs/reading-path.md`](docs/reading-path.md).

## The practical question

Generative AI can produce remarkably complete software, reports, research, designs, automations, proposals, presentations, analyses, customer interactions, and other work at very low marginal cost.

The project asks:

> **We bought or gained access to AI. What have we actually achieved, what remains, and what evidence connects the output or action to business value?**

This project uses a decision framework:

**Access → Output → Deliverable → Operating capability → Outcome → Value**

The stable machine identifier for **Operating capability** is `04-capability`.

These are six different claims, not mandatory lifecycle stages and not a maturity score.

## Decision first

The ladder is a **claim filter**. Start with the decision and require the weakest claim sufficient for that decision:

- **keep exploring?** → Output may be enough;
- **may someone rely on it?** → Deliverable;
- **may we sell, operate or support it repeatedly?** → Operating capability;
- **did it change the result?** → Outcome;
- **should we scale, renew or stop?** → Value.

A strong Access/Output result does not average into partial Deliverable.

> **Gate ≠ truth.** A Claim Gate `PASS` means the **supplied record** satisfies the deterministic checks for the selected decision. It is not an audit of the underlying system, measurement, people, or evidence references.

## Four distinctions that matter

### Tool capability ≠ job substance ≠ delivery capability
A capable agent may generate most of the visible artefact or perform much of a workflow. That does not automatically establish that the result reflects the actual job or that the supplier can repeatedly evaluate, operate, support, maintain, and stand behind it.

### Workflow is a boundary, not a seventh claim
Local task or product acceleration can move the bottleneck into review, integration, deployment, support, or another downstream step. Define where the workflow starts, what counts as complete, what happens on the unhappy path, and which end-to-end outcome should change.

### Judgement ≠ authority ≠ accountability
AI systems can analyse evidence, compare options, plan, recommend, communicate, persuade, and make bounded decisions. A human decision-maker is not automatically correct because they are human or senior. An AI system is not automatically correct because it is fast or capable.

> **Apply the same standard to human, AI and hybrid work: assess the complete process and its results, not the identity of the producer.**

### Reduced labour ≠ reduced elapsed time ≠ realised financial value
AI may genuinely improve all three, but a gain in one metric should not silently become a claim about another.

## Learn from samples before starting blank

The Claim Gate ships with three fictional teaching cases represented by four `claim.json` records:

- website prototype — **Explore → PASS**;
- the same website — **Operate → BLOCKED**;
- internal tool — **Rely → PASS**;
- killed idea — **Outcome → PASS** on learning/option value.

The samples are under [`toolkit/samples/`](toolkit/samples/). They are teaching records, not disguised client incidents.

## Software Outcome pack

For software-delivery initiatives, [`toolkit/templates/software-outcome-pack.json`](toolkit/templates/software-outcome-pack.json) suggests a 05 Outcome measurement plan using DORA's five current software-delivery metrics:

- change lead time;
- deployment frequency;
- failed deployment recovery time;
- change fail rate;
- deployment rework rate.

When AI-assisted delivery is the intervention, the template also suggests leading indicators such as AI-touched share, review wait on AI-touched changes, and revert/rollback rate on those changes.

The template marks **no gate check PASS automatically**. It defines what to measure; it does not establish causal attribution, customer value, AI ROI, or business profitability.

## Human, AI and hybrid interfaces

Same standard does not require the same interface.

- **Human:** visible Claim Gate form.
- **AI:** native MCP `evaluate_claim_record` or compatible browser WebMCP.
- **Hybrid:** exchange the same `claim.json`; a compatible browser agent may request a local form handoff, which the mounted Claim Gate must acknowledge before WebMCP reports it as applied.

The practical IDE/terminal integration is the local MCP package under [`packages/mcp/`](packages/mcp/). Its README includes current Claude Code, Cursor and VS Code/GitHub Copilot examples. WebMCP remains progressive enhancement when the browser exposes `document.modelContext`.

## Private evidence can stay private

Rigour does not require publishing client names, contracts, production metrics, personal data or proprietary workflows. Internal evidence can remain private while the authorised decision record stays inspectable inside the organisation.

Use [`toolkit/private-workbook/`](toolkit/private-workbook/) for real work. The public project does not need access to the organisation's evidence folder.

## Mild operating kit

[`toolkit/operating-kit.md`](toolkit/operating-kit.md) points to classes of instrument that can inspect a claim: evaluation/trace, contract/e2e testing, operational evidence, DORA-capable delivery telemetry, usage inventories, and cost/value records.

For the two upper decision claims, use the fillable [Outcome worksheet](toolkit/templates/outcome-worksheet.md) and [Value cost ledger](toolkit/value-cost-ledger.md). They keep baseline/after evidence, elapsed time, labour movement, confounds, adverse effects, attribution, full cost boundaries, and option value explicit without auto-populating Claim Gate PASS states.

MCP servers, skills, repository tools, documentation connectors and log access are **context pipes**. They can improve Access, Output and evidence retrieval; they do not mint Value merely because they are connected.

## Evidence model

Canonical evidence lives under `data/`. Important factual claims can be traced as:

**Claim → source/version → exact locator → relevant finding → qualification → article location → reviewer/process → independent review status → review record → disposition**

Independent review is actor-neutral. A completed review may be performed by a human, AI system, automated method, specialist toolchain, or hybrid process if it is sufficiently separate from the originating authoring step, directly checks the evidence, applies the stated criteria, and leaves an auditable record.

> **Review completed is not the same as claim accepted.**

`rejected` is a valid review disposition. A launch-critical claim can pass release approval only with an accepting disposition: `accepted`, `accepted_with_qualification`, or `revised_and_accepted`.

Evidence character is explicit where useful: public measured evidence, public documented evidence, internal evidence, illustrative material, or editorial synthesis. See [`docs/evidence-policy.md`](docs/evidence-policy.md).

## Working preview versus reviewed release

The public GitHub Pages site currently deploys the **working preview** from `main`. It includes the core guide plus deeper and advanced working material, with publication and evidence-review states kept visible.

Normal CI separately builds and interaction/link-checks a proposed release artifact. This keeps two questions distinct:

> **Does the proposed release artifact structurally and operationally work?**
>
> **Has that artifact actually been reviewed and approved?**

Each article declares a `release_scope` of `guide`, `policy`, or `working`. Working research is physically excluded from release mode.

The public acceptance bar for the first reviewed release is now explicit in **[`docs/first-reviewed-release.md`](docs/first-reviewed-release.md)**. It covers the core instrument, worked decisions, independent evidence review, rendered usability/print checks, licences, provenance/corrections, reader testing, and explicit release approval.

Until that checklist is satisfied, **Working preview stays in the header**.

## Publication controls

Normal CI runs regression tests; exercises the reusable Claim Gate Action; tests the native MCP package; type-checks the React/Base UI layer; builds the finished preview including Tailwind, WebMCP machine surfaces and pdfcn output; validates evidence/traceability; checks interaction/link integrity; and then independently builds and checks the proposed release artifact.

GitHub Pages runs the same relevant evidence, interaction, Action, MCP, UI and artifact checks before it uploads a deployment. A release-mode deployment additionally runs the release-approval checks.

## Repository structure

```text
.
├── START-HERE.md
├── README.md
├── content/                         # Core guide + decision tools + deeper analyses
├── data/                            # Canonical source / claim / article records
├── docs/                            # Evidence, reading, release and positioning policy
├── schemas/v1/                     # claim.json and decision-gate contracts
├── toolkit/
│   ├── samples/                    # Filled teaching claim records
│   ├── templates/                  # General + software Outcome instruments
│   ├── private-workbook/           # Confidential-use folder template
│   ├── AGENT_RULES.md
│   ├── operating-kit.md
│   └── value-cost-ledger.md        # Fillable Value decision workbook
├── packages/mcp/                   # Native stdio MCP server
├── web/                            # shadcn/Base UI + Tailwind + pdfcn
├── scripts/                        # Build / validation / publication tooling
├── tests/
└── .github/workflows/
```

## Corrections and responsibility

The initial maintainer is **Helen Kwok**. Evidence-based corrections and counterexamples are welcome. See [`content/provenance.md`](content/provenance.md), [`content/corrections.md`](content/corrections.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Current status

**Public working preview / labelled pilot.** The repository is under AlreadyOpen and the GitHub Pages preview is live.

The remaining bar is maintained in [`docs/first-reviewed-release.md`](docs/first-reviewed-release.md), rather than being implied by a green CI build.

## Licence

A final code/content licensing model has not yet been selected. Code and editorial/reference content may ultimately use different licences. Selecting and publishing those licences is a required item before the first reviewed release.
