# How AI Output to Value relates to existing frameworks

AI Output to Value is **not** a replacement for a risk-management framework, management-system standard, law, or regulator guidance. It answers a narrower operational question:

> **What claim is sufficient for the next decision, and what evidence establishes that claim?**

That makes it a decision/evidence layer that can sit inside a larger governance system.

## NIST AI Risk Management Framework

NIST AI RMF 1.0 is a voluntary, use-case-agnostic risk-management framework organised around **GOVERN, MAP, MEASURE, and MANAGE**. NIST notes that AI RMF 1.0 is being revised in 2026.

AI Output to Value can complement it as follows:

| AI Output to Value concern | Closest NIST AI RMF use |
|---|---|
| authority, accountability, review responsibility | GOVERN |
| intended use, workflow boundary, actors, affected context | MAP |
| acceptance evidence, outcomes, baselines, uncertainty | MEASURE |
| controls, fallback, escalation, recovery, stop rules | MANAGE |

The six claims are **not** NIST maturity levels and should not be presented as a NIST crosswalk certification.

Official source: https://www.nist.gov/itl/ai-risk-management-framework

## ISO/IEC 42001:2023

ISO/IEC 42001 specifies requirements for establishing, implementing, maintaining, and continually improving an AI management system.

AI Output to Value is much smaller in scope. Its **Operating capability** claim can help an organisation ask whether ownership, assurance, fallback, maintenance, support, and improvement actually exist for a particular workflow. That can provide useful decision evidence inside an AI management system, but it does not establish conformity with ISO/IEC 42001 and is not a substitute for certification or a formal management-system audit.

Official source: https://www.iso.org/standard/42001

## UK Government AI Playbook

The UK Government AI Playbook calls for meaningful human control at appropriate stages, clear accountability, appropriate skills and expertise, testing, monitoring, and lifecycle management/support.

AI Output to Value can use those controls as evidence inputs where they are relevant, while keeping three questions separate: whether a review/control is effective, who has legal or organisational authority, and where accountability/recourse sits. Its statement that **human-in-the-loop is a control pattern, not a quality guarantee** should not be read as an argument against human control where law, policy, contract, consequence, or governance requires it.

Official source: https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html

## EU AI Act — Article 14 human oversight

Article 14 of Regulation (EU) 2024/1689 requires high-risk AI systems to be designed and developed so that they can be effectively overseen by natural persons during use, with oversight measures proportionate to the risks, autonomy, and context.

AI Output to Value's statement that **human-in-the-loop is a control pattern, not a quality guarantee** does not remove or weaken legal human-oversight requirements. Where law requires natural-person oversight, the authority and assurance design must satisfy that requirement. The framework's point is narrower: the existence of a human click or review step alone is not evidence that the control is effective.

Official source: https://eur-lex.europa.eu/eli/reg/2024/1689/oj

## Australia — Guidance for AI Adoption

Australia's National Artificial Intelligence Centre published **Guidance for AI Adoption** in October 2025. It sets out six essential practices for responsible AI governance and adoption and explicitly evolves/simplifies the earlier Voluntary AI Safety Standard.

For Australian organisations, this is a more current reference point than treating the 2024 Voluntary AI Safety Standard as the final form of national voluntary guidance.

AI Output to Value can complement that guidance by making each proposed business decision explicit and recording the claim, evidence, authority, accountability, workflow boundary, next evidence, and stop rule for that decision.

Official sources:

- https://www.industry.gov.au/sites/default/files/2025-10/guidance-for-ai-adoption-foundations.pdf
- https://www.industry.gov.au/sites/default/files/2025-10/guidance-for-ai-adoption-implementation-practices.pdf

## Closest relatives: logic models, benefits management and assurance cases

The frameworks above are governance and risk frameworks. The three below are the method's closest relatives by structure, and none of them was created for AI-assisted work. AI Output to Value does not claim to have invented the idea of following a result from what was produced to what changed, or of tying a claim to evidence. What it adds is narrower: the *decision* selects the one claim that is sufficient, and the gate records that single decision.

## Logic models and theory of change

The W.K. Kellogg Foundation's *Logic Model Development Guide* (updated January 2004) presents a basic logic model as five components read from left to right: resources (inputs), activities, outputs, outcomes and impact. It describes outputs as the direct products of program activities and outcomes as specific changes in participants, and notes that a logic model is often used interchangeably with program theory. The UK Treasury's *Magenta Book* describes a Theory of Change as documenting how an intervention is expected to work, and presents a linear version running from inputs through to the expected outputs and outcomes (section 2.2.1, Figure 2.2).

AI Output to Value shares the outputs-to-outcomes lineage. It differs in three ways:

- **A decision, not a chain.** A logic model or theory of change maps how a program is expected to produce change, and is read as a chain. The six claims are not a chain to walk. A named decision selects the one claim that is sufficient for it, and the ladder is never an aggregate score for the project.
- **Two claims between Output and Outcome.** A thing that was produced is not yet a thing someone may rely on, or one an organisation can repeatedly operate. **Deliverable** and **Operating capability** name those steps and the evidence each needs.
- **A separate question about worth.** The Kellogg guide defines impact as change. **Value** asks whether a measured Outcome was worth the full relevant cost, risk and alternatives, which is a different question.

This is the project's own reading, not an equivalence:

| Logic model component (Kellogg) | Closest AI Output to Value use |
|---|---|
| Resources / inputs | **01 Access**, for the tool; other resources are not modelled |
| Activities | Not a claim: recorded as the workflow boundary and actors in the decision record |
| Outputs | **02 Output**, and **03 Deliverable** when fitness for a named use is claimed |
| Outcomes | **05 Outcome** |
| Impact | **05 Outcome** for longer-term change, and **06 Value** when cost and alternatives are judged |

Official sources:

- https://wkkf.issuelab.org/resources/10124/10124.pdf
- https://www.gov.uk/government/publications/the-magenta-book/magenta-book-central-government-guidance-on-evaluation-html

## Benefits realisation management

The UK Government's *Teal Book* chapter on benefits management defines a benefit as measurable value or other positive impact from an outcome that stakeholders see as an advantage and that contributes to objectives (section 19.4). It expects the current performance level to be set as a baseline before work starts (19.6.3.5), gives each benefit a named owner (19.5), and says realisation usually needs continuing action once the solution is in operational use (19.6.3.8).

AI Output to Value asks for some of the same disciplines, but for one decision at a time. It does not replace a benefits register, benefit owners or a portfolio process. It can supply the evidence check inside them, and it asks for the earlier claims first, because a benefit cannot be realised from something that was never reliable or operable.

This is the project's own reading, not an equivalence:

| Benefits management activity (Teal Book) | Closest AI Output to Value use |
|---|---|
| Identify and categorise a benefit, and set its baseline (19.6.3.5) | **05 Outcome**: the outcome measure and baseline are defined |
| Value and appraise a benefit (19.6.3.6) | **06 Value**: full cost, risk trade-offs and alternatives, with an explicit value rule |
| Realise the benefit, including in operational use (19.6.3.8) | **04 Operating capability**: owner, assurance, fallback and support |
| Review and close the benefit (19.6.3.9 to 19.6.3.10) | The **scale, renew or stop** decision |

Official source: https://projectdelivery.gov.uk/teal-book/home/part-e-planning-and-control/chapter-19-benefits-management/

## Assurance cases

ISO/IEC/IEEE 15026-2:2022 specifies minimum requirements for the structure and meaning of assurance cases, and does not require a particular notation. The Goal Structuring Notation (GSN) Community Standard, version 3 (SCSC-141C), published by the Safety-Critical Systems Club, aims to give an authoritative definition of that notation and guidance on using it to develop and evaluate engineering arguments.

Assurance cases are the closest relative of the gate: both make a claim explicit and tie it to evidence. The difference is weight and scope. An assurance case sets out an argument for a claim. The gate keeps a small record of one decision: the claim it requires, whether each required check passed, failed or is unknown, who has authority, the next evidence and the stop rule. It does not test whether an argument is sound (**Gate ≠ truth**). A team that already maintains assurance cases should keep them, and can point a gate check's evidence at the relevant part of the case.

Official sources:

- https://standards.ieee.org/ieee/15026-2/10236/
- https://scsc.uk/gsn-standard

## What this framework is for

Use AI Output to Value when a meeting, project, procurement, experiment, delivery, or operating decision needs a disciplined answer to questions such as:

- Do we only have Access, or have we demonstrated useful Output?
- Is the result fit for the named use as a Deliverable?
- Can the organisation repeatedly operate and support it as an Operating capability?
- Did the intended Outcome actually change?
- Is that Outcome worth the full relevant cost, risk, alternatives, and trade-offs?

Then apply the relevant law, standard, regulatory guidance, contractual obligations, sector controls, and organisational policies around that decision.

## Maintenance note

External frameworks change. Before relying on this crosswalk for governed work, confirm the current official version and jurisdictional applicability. This page is orientation, not legal advice, certification guidance, or a compliance determination.
