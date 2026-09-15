# Claim card — decide what evidence is enough for the next decision

The six-claim model is a **claim filter**, not a maturity score and not a checklist that every project must complete.

Use this card before a review meeting, pilot decision, customer commitment, or scale decision.

## Start with the decision

Do not begin by asking, "How far along are we?"

Ask:

> **What decision are we trying to make, and what is the weakest claim that would be sufficient for that decision?**

| Decision sought | Minimum claim that normally matters | Typical evidence |
| --- | --- | --- |
| **Keep exploring?** | **Output** | Reproducible artefact/action, what was supplied, what was inferred, and what was learned. |
| **May someone rely on this for the named use?** | **Deliverable** | Intended use, acceptance criteria, evaluation against them, known limitations. |
| **May we sell, operate, support, or staff this repeatedly?** | **Capability** | Owners, runbook, tests/evaluation, fallback, operating cost, support and escalation. |
| **Did the initiative change the result we care about?** | **Outcome** | Baseline and after measurement using the same definition, with important confounds named. |
| **Should we scale, renew, expand, or stop?** | **Value** | Outcome compared with full relevant cost, risk, alternatives, and trade-offs. |

These are defaults, not laws. Consequence, regulation, contract, reversibility, and uncertainty can raise or lower the assurance needed.

## Do not average the six claims

A project with excellent **Access** and **Output** but no evidence of **Deliverable** is not "one-third complete".

The claims answer different questions. A zero at a decision-critical claim cannot be cancelled out by a two somewhere else.

## Evidence character

State what kind of evidence you are using before discussing conclusions.

- **Public measured evidence** — research, statistics, or measured case evidence whose method and scope can be inspected.
- **Public documented evidence** — official guidance, standards, product documentation, policies, or other inspectable records.
- **Internal evidence** — measurements or observations available inside an organisation but not suitable for public disclosure.
- **Illustrative** — a constructed example used to teach the reasoning. It is not evidence that the scenario occurred.
- **Editorial synthesis** — an interpretation or recommendation made by this project from the available evidence.

Confidentiality does not require pretending evidence does not exist. It requires keeping the public claim within what can safely be disclosed and keeping the private record inspectable by the people authorised to see it.

## Copyable claim card

### Decision

**Decision sought:** explore / rely / operate / sell / scale / renew / stop / other

**Intended use:**

**Decision date or review point:**

### Claim

**Current claim level:** Access / Output / Deliverable / Capability / Outcome / Value

**Evidence character:** public measured / public documented / internal / illustrative / editorial synthesis

**What has actually been demonstrated:**

**What was supplied to the AI or process:**

**What had to be inferred or assumed:**

**Known limitations / out of scope:**

### Actors, interface, and control

**Primary actor:** human / AI / automated system / hybrid

**Interaction channel:** human UI / WebMCP / API / other agent tool / hybrid

**Evaluation / assurance:**

**Authority holder:**

**Accountable owner / recourse:**

**Fallback / escalation:**

### Economics and measurement

**Outcome measure:**

**Baseline:**

**Full relevant cost boundary:**

**Option value / learning value:** What useful uncertainty was removed even if the work is not operationalised?

### Decision rule

**Decision now:** continue / restrict / rely / operate / scale / stop

**Next evidence that would change the decision:**

**Stop rule:** If this evidence is not reached by the agreed review point—or if a named risk/metric crosses the limit—what do we stop doing?

## Same standard does not mean the same interface

Actor-neutral evaluation does **not** require an AI agent to imitate a person clicking the same controls.

A human may use the visible interface. An agent may use a structured tool surface such as **WebMCP**. A hybrid workflow may use both, including explicit approval or escalation for consequential actions.

The interface can differ while the decision standard stays the same:

- did the intended action actually happen?
- did it meet the same acceptance criteria?
- was the actor authorised to perform it?
- are consequential actions appropriately controlled?
- can the result and failures be inspected?
- does the workflow improve the outcome at an acceptable cost and risk?

WebMCP is useful here because it allows a web page to expose structured application actions to compatible agents instead of requiring the agent to infer every action from the visual UI. That is an **interaction channel**, not proof of Deliverable, Capability, Outcome, or Value.

See [`representation-is-a-channel.md`](representation-is-a-channel.md) for the wider human/agent/hybrid channel model.

## Option value is a real outcome

A prototype can be valuable because it answers a question cheaply:

- a proposed feature is not wanted;
- a workflow is technically feasible but commercially weak;
- customers understand one interaction but reject another;
- an integration is easier or harder than expected;
- a team can stop a bad idea before a larger commitment.

That is not a failure to reach **Capability** or **Value**. It can be a legitimate **Outcome** if the learning changes a real decision.

Measure it explicitly: decision made, uncertainty removed, time to decision, cost of the test, or larger spend avoided.

## The practical rule

> **Use the lowest claim that is sufficient for the next decision, and stop adding process when more evidence would not change that decision.**
