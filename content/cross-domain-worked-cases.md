# Cross-domain worked cases — common false claim promotions

These cases are **fictional illustrations**. Their numbers and organisations are invented. They are selected because each exposes a different claim-confusion failure mode, not because the framework needs a maturity model for each industry.

The same rule applies in every case:

> **Use the weakest claim sufficient for the next decision, and stop there.**

A gate status describes whether the evidence is sufficient for the selected decision. **PASS does not mean the initiative is good.** A PASS can establish that an Outcome became worse. BLOCKED means at least one required check explicitly failed. INSUFFICIENT EVIDENCE means no required check failed, but the evidence needed for the decision is incomplete.

| Case | False promotion | Target decision | Weakest sufficient claim | Gate result |
| --- | --- | --- | --- | --- |
| Customer-support agent | Containment/deflection → Outcome | Determine whether support actually improved | 05 Outcome | **INSUFFICIENT EVIDENCE** |
| Proposal/report factory | Polished Output → Deliverable | Permit reliance/submission | 03 Deliverable | **BLOCKED** |
| Agent with system-of-record write access | Successful writes → Operating capability | Operate repeatedly without per-write approval | 04 Operating capability | **BLOCKED** |
| Professional deliverable | “A human reviewed it” → Deliverable authority | Permit external reliance | 03 Deliverable | **INSUFFICIENT EVIDENCE** |
| Coding assistant | Local task speed → end-to-end Outcome | Measure software-delivery Outcome | 05 Outcome | **PASS — outcome worsened** |
| “Four hours saved” | Local Outcome → Value | Scale/renew/stop | 06 Value | **INSUFFICIENT EVIDENCE** |
| Killed pilot | “No launch” → no Outcome | Decide whether the experiment resolved the investment question | 05 Outcome | **PASS** |

---

## 1. Customer-support agent — containment is not resolution

### Situation

A support agent pilot raises automated containment from an illustrative 38% to 62%. Immediate human handoffs fall, so the dashboard looks better. The next management question, however, is not whether the bot can keep a conversation away from an agent. It is whether the support outcome improved.

**Target decision:** determine whether the pilot established a real support Outcome worth taking to a later scale decision.

**Weakest sufficient claim:** **05 Outcome**.

### Intended use and workflow boundary

The boundary starts when a customer asks for help and ends only after the issue is resolved or escalated and the agreed recurrence window has elapsed. Repeat contact, reopening, escalation and customer experience belong inside the workflow.

### Established evidence

- containment increased;
- immediate human handoffs decreased;
- the pilot categories and escalation policy are defined.

### Inferred or assumed

- that contained conversations were durably resolved;
- that repeat contacts did not rise;
- that CSAT/customer effort did not worsen;
- that work was not simply moved into later corrections or escalations.

### Gate result — INSUFFICIENT EVIDENCE

The Outcome measure and baseline can be defined, but the comparable post-pilot resolution, recurrence and customer-experience evidence is incomplete. Containment is evidence about one workflow point, not the end-to-end result.

**Authority/accountability/recourse:** the AI is authorised only for the pilot categories; human support retains escalation and exception authority; the support operations owner owns the outcome measures and the stop decision.

**Next evidence:** complete same-category no-repeat resolution, recurrence, escalation and CSAT measures using the pre-agreed definitions.

**Stop/restrict rule:** do not promote containment or deflection alone into an Outcome claim. Keep the pilot bounded until the end-to-end measures exist.

Machine-readable record: `toolkit/samples/customer-support-outcome-insufficient.claim.json`.

---

## 2. Proposal or report factory — finished-looking is not Deliverable

### Situation

An AI-assisted workflow produces a polished 30-page proposal with the requested sections, consistent formatting and a confident narrative. It looks finished enough to submit. A source spot check then finds an unsupported capability statement, and several quantitative claims have not completed traceability.

**Target decision:** permit the project team to rely on the proposal as submission-ready.

**Weakest sufficient claim:** **03 Deliverable**.

### Intended use and workflow boundary

The boundary includes source material, drafting, requirement coverage, factual and quantitative verification, commercial/contractual review and the authorised submission decision.

### Established evidence

- a reproducible, polished proposal exists;
- the structure and narrative cover the visible sections;
- the intended procurement use is defined.

### Inferred or assumed

- that visual completeness means factual completeness;
- that all requirements are actually covered;
- that every material number and capability claim is supported;
- that no important qualification or obligation was missed.

### Gate result — BLOCKED

The Deliverable acceptance criteria are explicit, and at least one has failed: a material claim is not supported by the approved evidence. That is a known failure, not merely missing paperwork.

**Authority/accountability/recourse:** the generator has no submission authority. The proposal owner is accountable for corrections and traceability; the authorised submitter controls the external commitment.

**Next evidence:** correct the unsupported statement, complete requirement/source traceability, run the named verification checks and record authorised acceptance.

**Stop/restrict rule:** keep the document labelled as draft Output. Do not submit or permit reliance until the Deliverable gate passes.

Machine-readable record: `toolkit/samples/report-factory-rely-blocked.claim.json`.

---

## 3. Agent with write access to a system of record — access is not authority or capability

### Situation

An agent can update approved customer-status fields in a system of record. In supervised tests it selects the intended record and writes the right values. The team proposes removing per-write human approval.

**Target decision:** operate the agent repeatedly with autonomous bounded writes.

**Weakest sufficient claim:** **04 Operating capability**.

### Intended use and workflow boundary

The workflow includes request interpretation, record selection, the write itself, verification, attribution, exception detection, reconciliation, rollback/recourse and support.

### Established evidence

- the bounded Deliverable criteria passed in supervised tests;
- writes are schema-valid and attributable;
- record-identity checks and an audit trail exist;
- an operational owner is named.

### Inferred or assumed

- that a technically valid service credential equals delegated business authority;
- that wrong-but-valid writes can be recovered safely;
- that the organisation has a workable recourse path at production volume;
- that support and operating cost are understood.

### Gate result — BLOCKED

The Deliverable evidence can be real while the Operating capability claim still fails. In this case fallback/recourse is not defined well enough and recovery/rollback has not been tested.

**Authority/accountability/recourse:** possession of a write credential is not treated as proof of autonomous authority. The operations owner can suspend the agent, but the recovery path for harmful writes is incomplete.

**Next evidence:** define and exercise rollback/reconciliation, complete the recourse and support path, and establish the relevant operating-cost boundary.

**Stop/restrict rule:** keep production use supervised or approval-required until recovery and recourse evidence supports the Operating capability claim.

Machine-readable record: `toolkit/samples/system-of-record-operate-blocked.claim.json`.

---

## 4. Regulated or professional deliverable — review quality and authority are separate

### Situation

An AI-assisted professional report has been reviewed by a knowledgeable subject-matter expert. The review note says no material technical error was found. The organisation's own submission policy, however, requires a separately authorised approver/signatory, and the record does not show that this authority has been satisfied for the version proposed for release.

**Target decision:** permit external reliance on the report as the organisation's approved professional deliverable.

**Weakest sufficient claim:** **03 Deliverable**.

### Intended use and workflow boundary

The boundary includes evidence gathering, drafting, technical review, approval/signatory authority, version control and controlled release.

### Established evidence

- technical review occurred;
- the report can be traced to an evidence index;
- failure modes around unsupported technical claims were considered.

### Inferred or assumed

- that “a human reviewed it” proves the person had approval authority;
- that a positive technical review proves the reviewed version is the released version;
- that review quality and organisational authority are the same control.

### Gate result — INSUFFICIENT EVIDENCE

The technical review may be good. The missing evidence is different: the Deliverable record does not yet establish the required approval authority and version binding. No technical failure needs to be invented to reach that conclusion.

**Authority/accountability/recourse:** the technical reviewer has review authority only. The deliverable owner must confirm the separate approval/signatory authority before release.

**Next evidence:** provide the approval/signatory record, bind it to the reviewed version and confirm all named Deliverable acceptance criteria.

**Stop/restrict rule:** keep the report in draft/review status. Do not treat human review as a substitute for required organisational authority.

Machine-readable record: `toolkit/samples/professional-deliverable-rely-insufficient.claim.json`.

---

## 5. Coding assistant productivity — a PASS can establish that the Outcome got worse

### Situation

A coding assistant cuts illustrative median code-production time from 120 minutes to 45 minutes. At the same time, median review wait rises from 3.5 hours to 7.8 hours, deployment rework rises from 6% to 12%, and median issue-to-successful-production lead time rises from 26 hours to 29 hours.

**Target decision:** determine what happened to the end-to-end software-delivery Outcome.

**Weakest sufficient claim:** **05 Outcome**.

### Intended use and workflow boundary

The boundary runs from work selection through code production, review, testing, deployment and any rework/recovery until the change reaches production or is abandoned under the same definition used for the baseline.

### Established evidence

- local code-production time improved substantially;
- review wait worsened;
- deployment rework worsened;
- the named end-to-end lead-time measure worsened under the same before/after definition;
- material confounds and the service boundary are recorded.

### Inferred or assumed

The rejected inference is that faster code production automatically means higher software-delivery productivity.

### Gate result — PASS

The gate passes because the Outcome question was actually measured against a comparable baseline with consistent definitions. The result is not favourable: the end-to-end workflow became slower on the named measure. PASS means the claim is evidenced, not that management should celebrate it.

**Authority/accountability/recourse:** coding assistance does not change review or deployment authority. The engineering lead owns the workflow measurement and can pause expansion.

**Next evidence:** redesign change size/review flow and repeat the same Outcome measurement before any separate scale or Value decision.

**Stop/restrict rule:** do not report local generation speed as end-to-end delivery productivity; pause expansion while lead time and rework remain worse than baseline.

Machine-readable record: `toolkit/samples/coding-assistant-outcome-pass.claim.json`.

---

## 6. “Four hours saved per person per week” — Outcome is not Value

### Situation

A bounded before/after study reports that employees spend an average of four fewer hours per week on selected tasks after adopting an AI tool. Someone multiplies four hours by salary and headcount and presents the number as annual Value.

**Target decision:** scale, renew or stop the tool at organisational level.

**Weakest sufficient claim:** **06 Value**.

### Intended use and workflow boundary

The decision boundary includes the observed time change, what the saved capacity became, transferred review/coordination work, output or quality effects, licensing/integration/support/assurance costs, risks and alternatives.

### Established evidence

- the selected task time changed under a defined before/after method;
- a bounded Outcome claim about local time use may therefore be legitimate.

### Inferred or assumed

- that every saved hour becomes additional useful output or reduced spend;
- that salary cost is automatically avoided cost;
- that review, integration, support and change-management work are zero;
- that the tool is better than reasonable alternatives.

### Gate result — INSUFFICIENT EVIDENCE

Outcome evidence is available, but the Value gate is not. Full cost, risk/trade-offs and alternatives are incomplete. The missing step is the mechanism from time saved to realised organisational benefit.

**Authority/accountability/recourse:** managers decide how capacity is redeployed; the scale decision owner must connect the Outcome evidence to realised benefit and the full decision boundary.

**Next evidence:** measure what the saved time became, complete the full relevant cost/risk boundary, compare alternatives and apply the pre-agreed scale rule.

**Stop/restrict rule:** do not convert saved hours directly into Value by multiplying them by salary and headcount unless the conversion mechanism is evidenced.

Machine-readable record: `toolkit/samples/time-saved-value-insufficient.claim.json`.

---

## 7. Killed pilot — stopping can still establish a legitimate Outcome

### Situation

A team uses a cheap prototype and structured conversations to test whether a proposed feature solves a sufficiently important problem for the target group. The prototype works technically, but the agreed demand threshold is not reached. The product is killed before full implementation.

**Target decision:** determine whether the experiment resolved enough uncertainty to make the product decision.

**Weakest sufficient claim:** **05 Outcome**.

### Intended use and workflow boundary

The boundary is the experiment itself: prototype, defined target group, pre-agreed response measure and the stop/continue decision.

### Established evidence

- the hypothesis and decision threshold were defined before the result;
- the relevant response evidence was collected;
- the product decision changed because the uncertainty was resolved;
- a larger build was avoided.

### Inferred or assumed

No inference to Operating capability or commercial Value is needed for the present decision. The prototype does not need to become a service for the experiment to have produced a useful result.

### Gate result — PASS

The Outcome is decision-changing learning. The initiative stops, but the evidence legitimately establishes that the experiment resolved the investment question. Information/option value is part of the result even though no production product follows.

**Authority/accountability/recourse:** the experiment informs but does not itself authorise production commitment; the product decision owner records the stop decision and evidence basis.

**Next evidence:** none for the current Outcome claim. If the idea is later revived for scale, collect the evidence required for the new decision rather than carrying this PASS upward.

**Stop/restrict rule:** stop productisation when the pre-agreed demand threshold is not reached. Do not continue merely because generation or implementation is cheap.

Machine-readable record: `toolkit/samples/killed-idea-outcome-pass.claim.json`.

---

## What this pack is designed to prevent

Across the seven cases, the recurring error is the same: evidence for one claim is promoted into a stronger claim because the artefact looks finished, a local metric moved, a credential exists, or a human was somewhere in the loop.

The framework does not require every initiative to reach Value. It requires the claim to match the decision:

- stop at Output when the decision is only to explore;
- require Deliverable evidence before someone may rely on the result;
- require Operating capability evidence before repeated operation is claimed;
- measure Outcome across the relevant workflow boundary;
- claim Value only when the evidenced Outcome is worth the full relevant cost, risk, alternatives and trade-offs.

That is why a lower claim can legitimately PASS and stop, while a stronger promotion remains BLOCKED or INSUFFICIENT EVIDENCE.
