# Claim card — decide what evidence is enough for the next decision

The six-claim model is a **claim filter**, not a maturity score and not a checklist that every project must complete.

Use this card before a review meeting, pilot decision, customer commitment, merge/release decision, or scale decision.

> **What decision are we trying to make, and what is the weakest claim that would be sufficient for that decision?**

For a live version, use the [interactive claim gate](../tools/claim-gate.html). It produces a deterministic **PASS / BLOCKED / INSUFFICIENT EVIDENCE** result and can export Markdown or `claim.json`.

## Start with the decision

| Decision sought | Minimum claim that normally matters | Gate logic |
| --- | --- | --- |
| **Keep exploring?** | **02 Output** | Reproducible/inspectable output plus important assumptions and inferences made visible. |
| **May someone rely on this for the named use?** | **03 Deliverable** | Intended use, acceptance criteria, evidence they were met, relevant failure/fallback checks, and stated limitations. |
| **May we sell, operate, support, or staff this repeatedly?** | **04 Capability** | Deliverable gate plus ownership, assurance, fallback/recovery, support/maintenance, and relevant operating-cost boundary. |
| **Did the initiative change the result we care about?** | **05 Outcome** | Defined outcome measure, comparable baseline, after measurement, consistent definitions, and material confounds named. |
| **Should we scale, renew, expand, or stop?** | **06 Value** | Outcome evidence plus full relevant cost, risk/trade-offs, alternatives, and an explicit value decision rule. |

These are defaults, not laws. Consequence, regulation, contract, reversibility, and uncertainty can raise or lower the assurance needed.

## Gate status is not a score

The decision gate has three states:

- **PASS** — every check required for this target decision is evidenced as passed.
- **BLOCKED** — at least one decision-critical check explicitly failed.
- **INSUFFICIENT EVIDENCE** — no required check is recorded as failed, but one or more required checks or decision-record fields are missing or unknown.

A project with excellent **Access** and **Output** but no evidence of **Deliverable** is not "one-third complete". A failed or unknown decision-critical claim cannot be cancelled out by strength somewhere else.

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

**Decision sought:** explore / rely / operate / measure outcome / scale-renew-stop

**Required claim:** 02 Output / 03 Deliverable / 04 Capability / 05 Outcome / 06 Value

**Claim being asserted:**

**Intended use:**

**Decision date or review point:**

### Claim

**Evidence character:** public measured / public documented / internal / illustrative / editorial synthesis

**What has actually been demonstrated:**

**What was supplied to the AI or process:**

**What had to be inferred or assumed:**

**Known limitations / out of scope:**

### Actors, interface, and control

**Primary actor:** human / AI agent / deterministic system / specialist tool / hybrid

**Interaction channel:** human UI / WebMCP / MCP / API / CLI / IDE agent / other agent tool / hybrid

**Evaluation / assurance:**

**Authority holder / boundary:**

**Accountable owner / recourse:**

**Fallback / escalation:**

### Economics and measurement

**Outcome measure:**

**Baseline:**

**Full relevant cost boundary:**

**Option value / learning value:** What useful uncertainty was removed even if the work is not operationalised?

### Decision rule

**Decision now:** continue / restrict / rely / operate / scale / renew / stop

**Next evidence that would change the decision:**

**Stop rule:** If this evidence is not reached by the agreed review point—or if a named risk/metric crosses the limit—what do we stop or restrict?

## Machine-readable claim record

The same decision record can be expressed as JSON using the versioned schema:

- [`claim.schema.json`](../schemas/v1/claim.schema.json)
- [`decision-gates.json`](../schemas/v1/decision-gates.json)
- [example claim record](https://github.com/AlreadyOpen/ai-output-to-value/blob/main/toolkit/claim.example.json)

The schema deliberately separates **actor**, **assurance**, **authority**, and **accountability**. The deterministic gate is selected by `targetDecision`, not by whether the producer was human or AI.

A repository or CI process can evaluate a record with:

```bash
python scripts/claim_gate.py path/to/claim.json --json
```

## Same standard does not mean the same interface

Actor-neutral evaluation does **not** require an AI agent to imitate a person clicking the same controls.

A human may use the visible interface. An agent may use a structured tool surface such as **WebMCP**, a native **MCP** server, an API, CLI, or IDE agent. A hybrid workflow may use several channels.

The interface can differ while the decision standard stays the same:

- did the intended action actually happen?
- did it meet the same acceptance criteria?
- was the actor authorised to perform it?
- are consequential actions appropriately controlled?
- can the result and failures be inspected?
- does the workflow improve the outcome at an acceptable cost and risk?

WebMCP is an **interaction channel**, not proof of Deliverable, Capability, Outcome, or Value.

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
