# Workflow is the unit: where AI output becomes business delivery

**Evidence character: editorial synthesis with Harvard Business Review management sources.**

A team can build a strong product, feature, model integration, report, or automation and still leave the surrounding business workflow incomplete.

That is not a criticism of engineering. It is a boundary problem.

> **The product or task is often one component. The workflow is the end-to-end path from trigger and inputs through work, verification, handoffs, exceptions, authority, delivery, support, and the outcome someone actually values.**

Workflow is therefore **not a seventh claim** in this project. It is the process boundary across which the six claims have to be tested.

## Why workflow belongs in the core model

A September 2026 *Harvard Business Review* article by Masha Shunko and Serguei Netessine recommends treating the **workflow rather than the individual task** as the object of AI redesign. The authors describe four ways task-level automation can fail: activity gets faster without creating value, the unhappy path is ignored, the end-to-end flow is ignored, or the wrong metric is optimized.

That management framing fits the distinction this project is already making:

| Claim | Workflow question |
| --- | --- |
| **Output** | Did one task, component, artefact, or action get produced? |
| **Deliverable** | Does the end-to-end result meet the acceptance criteria for the named use? |
| **Capability** | Can the organisation run, verify, support, recover, and improve the workflow repeatedly? |
| **Outcome** | Did the workflow change the customer, operational, learning, risk, or business result that matters? |
| **Value** | Was that outcome worth the complete workflow cost, risk, and alternatives? |

This makes workflow the bridge between **local production** and **business delivery**.

A product can be an important part of that bridge. So can software engineering, domain work, operations, assurance, customer handling, support, or a human/AI handoff. None of those components should be dismissed merely because it is not the whole workflow.

## Product, task, workflow, and deliverable are different claims

The words are often mixed together in management discussions.

**Task** — a bounded activity: draft a report, write a function, classify a ticket, generate a design, approve an invoice.

**Product / system** — a maintained artefact or service that exposes capability to a user or another system.

**Workflow** — the connected sequence that turns a trigger or need into an accepted result, including handoffs, checks, exception handling, authority, and feedback.

**Deliverable** — the result that someone is permitted to rely on for the named use because its acceptance criteria have been established.

A technically strong product can therefore exist inside a weak workflow. Conversely, a simple tool can support an excellent workflow if the surrounding process makes the result reliable and useful.

> **“We built the product” and “the workflow is ready” are not contradictory statements. They are different claims.**

## The coding-agent example is unusually useful

The HBR article uses coding agents to make the point concrete. An agent can increase the volume of code produced while the constraint moves downstream into code review, integration testing, security review, or deployment.

The local productivity improvement can be real.

But if the surrounding delivery system cannot absorb, verify, integrate, and safely release the additional output, the end-to-end development cycle may improve little—or may become worse.

That maps directly to this project's software worked case:

**Agent writes code + tests pass** → useful **Output** evidence.

**The change meets the actual intended-use acceptance criteria** → evidence for **Deliverable**.

**The organisation can repeatedly run the agent-enabled delivery process with bounded permissions, verification, release controls, recovery, ownership, and support** → evidence for **Capability**.

See [Software and architecture worked cases](software-architecture-worked-cases.md).

## A workflow includes the unhappy path

A workflow is not complete merely because the standard path works.

Before a relied-upon or operational claim is made, ask what happens when:

- information is missing or contradictory;
- a model or person is uncertain;
- a downstream system rejects the action;
- credentials or permissions do not match;
- a timeout makes completion ambiguous;
- the result fails an acceptance check;
- the action needs to be stopped, reversed, or corrected;
- repeated exceptions reveal a design problem.

The HBR article makes this an explicit part of workflow design: recognise uncertainty, define escalation, place authority, provide a stop/reversal path, and learn from corrections.

This does not imply that every workflow needs a large governance layer. The control should remain proportionate to the consequence and reversibility of the failure.

The [software failure-mode catalogue](software-failure-mode-catalogue.md) provides concrete examples of which failure modes may justify which tests.

## Where this project differs from HBR's 4A framing

The HBR article proposes **Assist, Approve, Audit, and Automate** as four modes for deciding where human authority remains. It recommends more human control where stakes are high or actions are difficult to reverse.

That is a useful management model, but this project keeps a slightly different distinction.

**Human presence is not itself the assurance claim.**

We separate:

- **judgement / evaluation** — which option appears better under the evidence;
- **authority** — who or what is permitted to act or bind the organisation;
- **assurance** — what independent or deterministic checks make the process sufficiently reliable;
- **accountability / recourse** — where responsibility and remedy sit.

A workflow may legitimately use a human approver because law, contract, policy, or risk allocation requires it. Another workflow may use deterministic controls, a second model, specialist review, post-action audit, bounded automation, or a combination.

The question is not simply **“is a human in the loop?”** It is **“is the authority-and-assurance design appropriate for this failure mode and consequence?”**

## Management words are not evidence

Terms such as **workflow**, **teamwork**, **KPI**, **productivity**, **leadership**, and **alignment** are useful shorthand. They are not self-proving explanations of why a proposal is good or why another team has failed.

Before using one of these words to justify approval, rejection, investment, reorganisation, praise, or criticism, turn it into something inspectable:

| Management term | Operationalise it | Evidence to look for |
| --- | --- | --- |
| **Workflow** | Trigger, boundary, completion condition, handoffs, unhappy path, authority, outcome | End-to-end test, process trace, runbook/recovery evidence, outcome measure |
| **Teamwork** | Who works together, what happens before/during/after, roles, shared information, decision rights, follow-up | Collaboration artefacts, decisions, handoffs, follow-through, outcome evidence |
| **KPI** | Exact metric definition, unit, numerator/denominator, data source, cadence, baseline, guardrails | Reproducible calculation plus evidence that the KPI is connected to the desired outcome |
| **Productivity** | Accepted output or outcome per relevant input, with quality held explicit and downstream rework counted | Comparable whole-workflow measurement rather than local activity volume alone |
| **Leadership** | Decisions, coordination, authority, escalation, resource allocation, accountability, learning | Inspectable decisions, operating changes, capability built, risks handled, outcomes |

A separate September 2026 *Harvard Business Review* article by Gabriele Rosani and Elisa Farri is useful precisely because it makes **teamwork** more operational. Based on hands-on workshops involving more than 300 managers across 35 organisations, the authors describe a full arc of teamwork: preparation **before** a meeting or workshop, collaborative work **during** it, and reflection/follow-up **after** it. They propose **intentionality** and **craft** as conditions for useful team-AI collaboration, where the work is deliberately redesigned and the AI interaction is given enough context, roles, steps, prompts, and pauses.

The narrower lesson for this project is important:

> **Saying “we need teamwork” is no more complete than saying “we need AI.” Define the collaborative process, what each participant contributes, how decisions move, what happens afterward, and which result should improve.**

The HBR authors frame intentionality strongly around the team leader. AI Output to Value does not generalise that into a rule that hierarchy itself proves agency, judgement, or quality. The evidence standard remains symmetric across executives, managers, specialists, technical staff, AI systems, and hybrid processes.

The familiar **boss-versus-leader cart meme** is a good example of rhetoric rather than operating evidence. It is memorable because it compresses leadership into one visible contrast: riding versus pulling. But the picture cannot tell us whether work is allocated according to expertise, whether the leader's highest-value contribution is direction or manual effort, whether risk and authority are placed correctly, whether the team can handle exceptions, or whether the result is actually better.

Use a meme or slogan to start a question, not to close one.

> **Management vocabulary should meet the same standard as technical vocabulary: define the claim, define the process or metric, and show the evidence.**

## What a manager can ask instead of “where is the workflow?”

Turn the criticism into an inspectable set of questions:

1. **What outcome is this workflow supposed to produce?**
2. **Where does it start and where is it actually complete?**
3. **Which parts are product/engineering output, and which parts are handoff, verification, operation, or support?**
4. **Where will the bottleneck move if AI accelerates one task?**
5. **What is the unhappy path?**
6. **Which acceptance criteria turn the output into a Deliverable?**
7. **Who or what has authority at consequential steps?**
8. **How will failure be detected, stopped, reversed, or escalated?**
9. **Which metric represents the outcome rather than merely the amount of activity?**
10. **What evidence would justify operating or scaling the workflow?**

This is more useful than treating “workflow” as a vague demand for more meetings or more process.

## A compact workflow boundary

For many AI-enabled projects, a useful first sketch is:

**trigger / need → inputs → AI or human work → verification → decision / authority → handoff / execution → exception / recovery → accepted deliverable → outcome → feedback**

Not every workflow contains every step, and several may be automated or collapsed together.

The point is to make the process boundary visible enough to test the claim.

> **Do not ask only whether the product works. Ask whether the complete workflow produces a result someone can rely on—and whether the organisation can stand behind it at the level being claimed.**

## Sources and qualification

Primary management sources:

- Masha Shunko and Serguei Netessine, *Stop Automating Old Processes. Design New Ones Instead.*, *Harvard Business Review*, 14 September 2026: https://hbr.org/2026/09/stop-automating-old-processes-design-new-ones-instead
- Gabriele Rosani and Elisa Farri, *AI Can Enhance Every Stage of Teamwork—Under Two Conditions*, *Harvard Business Review*, 7 September 2026: https://hbr.org/2026/09/ai-can-enhance-every-stage-of-teamwork-under-two-conditions

These are strong executive/practitioner sources. The workflow article reports that its authors refined their framework with companies and executive-education participants. The teamwork article reports hands-on workshops involving more than 300 managers across 35 organisations. Neither source is a universal controlled comparative benchmark, and this project does not treat either source's management framework as a universal standard.

Use the [Claim card](claim-card.md) to turn the workflow boundary into a decision record, and the [One-page meeting brief](meeting-brief.md) for a shorter discussion format.
