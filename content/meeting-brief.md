# One-page meeting brief

Use this when reviewing an AI-enabled proposal, prototype, deliverable, service, or decision process.

## Start with the decision, not the taxonomy

Which decision are we trying to make?

| Decision sought | Claim that normally matters |
| --- | --- |
| **Keep exploring?** | **Output** — enough to learn from a reproducible artefact or action. |
| **May someone rely on it for the named use?** | **Deliverable** — fit against explicit acceptance criteria. |
| **May we sell, operate or support it repeatedly?** | **Capability** — owners, controls, fallback and operating process exist. |
| **Did it change the result we care about?** | **Outcome** — the named measure moved versus a baseline. |
| **Should we scale, renew or stop?** | **Value** — the outcome is worth full relevant cost, risk and alternatives. |

The six claims are not a maturity score. Strong **Access** and **Output** do not average into partial **Deliverable**.

## Eight questions

1. **What exactly have we demonstrated?**
2. **What did the AI know, and what did it infer?**
3. **What remains before the intended use?**
4. **Which work disappeared, which work moved elsewhere, and where will the workflow bottleneck move?**
5. **Which actor or combination performs this task or decision best: human, AI, automated system, or hybrid?**
6. **Where do authority, accountability, verification, approval, operation and support sit?**
7. **Which business outcome are we trying to change—including learning or uncertainty removed?**
8. **What evidence would justify the next decision?**

## Workflow test

A September 2026 *Harvard Business Review* process-management article recommends treating the **workflow rather than the isolated task** as the object of AI redesign. Use that as a practical meeting test:

- **Outcome:** what customer, user, operational, learning, or business result is the workflow supposed to produce?
- **Boundary:** where does the workflow start, and what counts as complete?
- **Constraint:** if AI accelerates one task, where does the bottleneck move next?
- **Unhappy path:** what happens when information is missing, confidence is low, a dependency fails, or the action must be stopped or reversed?
- **Metric:** are we measuring the outcome, or only activity such as code generated, reports drafted, tickets closed, or handoffs avoided?

**Workflow is not a seventh claim.** It is the end-to-end process boundary across which Output must become Deliverable, Capability, Outcome, and Value.

## Three capabilities

| Capability | Question |
| --- | --- |
| **Tool capability** | Can the AI produce the artefact or perform the task? |
| **Job substance** | Does it contain what this actual job requires? |
| **Delivery capability** | Can the organisation stand behind it? |

A useful substance-gap example:

> **A contact form can look complete while enquiries never reach the business. The interface exists; the promised workflow does not.**

## Same standard, different interfaces

Actor-neutral evaluation does not require identical interaction channels.

A human may use the visible UI. An agent may use a structured tool surface such as **WebMCP**. A hybrid workflow may use both.

Judge each path against the same intended-use standard:

- did the action actually happen?
- did it meet the acceptance criteria?
- was the actor authorised?
- were consequential actions appropriately controlled?
- can success, refusal, and failure be inspected?

**WebMCP changes the interface available to an agent; it does not by itself prove Deliverable, Capability, Outcome, or Value.**

## Do not bundle judgement with authority

| Question | Meaning |
| --- | --- |
| **Judgement / evaluation** | Which option appears better under the evidence, goals and trade-offs? |
| **Authority** | Who or what is permitted to act or bind the organisation? |
| **Accountability / recourse** | Who must answer for the outcome and correct failures? |

A human decision is not automatically good because a human made it. An AI decision is not automatically good because it is fast or scalable. **Human-in-the-loop is a control pattern, not a quality guarantee.**

## Count the whole job

Track the unit you actually mean: labour hours, elapsed time, external spend, review/rework, incidents, throughput, customer outcome, learning, revenue or margin.

Do not turn a reduction in one metric into a claim about another without evidence.

## Decision record

**Evidence character:** public measured / public documented / internal / illustrative / editorial synthesis

**Established:** What is already known or verified?

**Not established:** What remains an assumption?

**Workflow boundary:** Where does the end-to-end process start, where is it complete, and where can the bottleneck or unhappy path move?

**Actor / interface / authority:** Who or what performs the task, through which channel (human UI / WebMCP / API / other / hybrid), who may approve or commit, and where does recourse sit?

**Decision:** Continue, restrict, rely, operate, scale, or stop?

**Next evidence:** What would change the decision?

**Stop rule:** What result, date, cost, or risk threshold would make us stop rather than generate more output?

For a fuller reusable template, use the [Claim card](claim-card.md). For the longer explanation, see [Workflow is the unit](workflow-not-task.md).

---

**AI Output to Value** — Use AI ambitiously. Keep the claims clear.
