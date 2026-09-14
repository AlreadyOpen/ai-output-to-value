# Engineering choices can be business decisions

> **Not every engineering detail is a management decision. But when an engineering choice changes cost, quality, latency, risk, or what can be offered to a customer, its consequences are part of the business decision.**

AI products make this boundary especially important because model selection, routing, evaluation, retries, tools, and escalation can directly change unit economics.

## Keep implementation detail and business consequence separate

Engineering should normally own implementation details such as prompts, schemas, routing, retries, SDK integration, caching, deployment topology, and observability.

Cross-functional decision-makers need the consequences when those choices change cost per acceptable outcome, quality, latency, failure behaviour, evaluation burden, support load, vendor dependency, risk, price, or margin.

> **Take implementation detail offline. Bring product-changing consequences back online.**

## Economics lives in the architecture

The price of one model does not determine the cost of an AI-enabled service.

**Relevant workflow cost = planning + generation/execution + tool use + retries + context + verification/evaluation + infrastructure + specialist or human intervention + failure handling + support**

Then measure:

> **Cost per acceptable outcome = total relevant cost of successful and unsuccessful attempts ÷ number of outcomes that meet the defined acceptance rule.**

The numerator and denominator must be stated. A cheap model can create an expensive workflow if it causes retries, corrections, escalation, downstream failures, or support work. A more expensive model can sometimes reduce total cost by reducing those terms.

The reverse can also be true: using the most capable model for simple, easily checked work may add cost without improving the customer outcome.

## Architecture options are hypotheses

A workflow might use one high-capability model for every request, route simpler work to cheaper models, cascade from inexpensive to stronger models, use a router, use a stronger model for planning while cheaper models or deterministic tools execute easier steps, constrain customer-facing agents with policy tools, or avoid LLMs for stages conventional software handles more reliably.

There is no universal winner. The target workload needs its own evaluation.

## Selective use of stronger models is an established design pattern

Research on LLM routing and cascading provides bounded evidence that selectively combining stronger and weaker models can improve cost-quality trade-offs in evaluated settings.

**RouteLLM** studies learned routing between stronger, more expensive models and weaker, cheaper models. **FrugalGPT** studies cascades and other budget-aware strategies.

Those studies support the narrow principle that a workflow does not necessarily need the most capable model for every step. They do **not** establish that a particular router, planner/executor split, model pair, benchmark saving, or quality level will transfer to a different production workload.

- RouteLLM: https://arxiv.org/abs/2406.18665
- FrugalGPT: https://arxiv.org/abs/2305.05176

## Define the denominator before comparing architectures

The table below is **fictional** and exists only to show how a comparison should be labelled.

Assume a batch of customer tasks with one shared acceptance rule:

- **First-pass acceptable** means the initial automated result meets the rule without escalation.
- **Escalated** means the task needs another model, deterministic validation, specialist review, repair, or another recovery step.
- **All-in variable cost per acceptable outcome** includes model/tool calls, unsuccessful attempts, retries, and expected variable escalation/evaluation cost. Fixed company overhead is excluded unless stated otherwise.
- **Median latency** is end-to-end workflow latency, not model inference time alone.

Because first-pass acceptable and escalated are mutually exclusive shares of the same task population in this illustration, each row sums to 100%.

| Architecture | First-pass acceptable | Escalated | Median end-to-end latency | All-in variable cost per acceptable outcome | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| A — strongest model everywhere | 97% | 3% | 24 s | $4.40 | Simple routing, expensive inference |
| B — route easier work to cheaper model | 95% | 5% | 17 s | $1.05 | Routing cost included |
| C — cheaper model only | 86% | 14% | 14 s | $0.95 | Cheap inference, much more repair/escalation |

The row with the cheapest model call is not necessarily the row with the cheapest acceptable outcome. Likewise, a 95% first-pass rate is not automatically acceptable. The customer promise, failure cost, and recovery process determine whether it is enough.

## Product discovery should be multidisciplinary

The UK Government AI Playbook recommends selecting AI use cases from business and user needs and using multidisciplinary teams. NIST's AI Risk Management Framework asks organisations to define context, business value, intended tasks, expected benefits, expected costs, and relevant actors.

These are governance sources rather than proofs of commercial success. They support a narrower organisational principle:

> **Business context, domain knowledge, technical design, risk, and economics need to meet before a customer commitment is made.**

## A practical division of decision rights

### Business / product / domain

Define the customer problem, desired outcome, acceptance rule, service level, risk tolerance, constraints, and commercial objective.

### Engineering

Design and test alternative model/tool combinations, routing, escalation, evaluation, reliability, and failure behaviour.

### Cross-functional decision

Compare options on quality, cost, latency, reliability, support burden, security/compliance, customer fit, price/margin, and strategic dependency.

> **Engineering owns the mechanism. The business must understand the consequences.**

## Architecture trade-off record

For each candidate architecture, record:

| Field | What to state |
| --- | --- |
| **Customer outcome** | What successful completion means to the user or buyer. |
| **Acceptance rule** | The explicit quality/fitness threshold used in the denominator. |
| **Attempt population** | What requests, documents, cases, or tasks are being measured. |
| **Architecture** | Models, tools, deterministic components, routing, and escalation path. |
| **First-pass performance** | Quality before repair or escalation. |
| **Escalation / retry rate** | Share of attempts needing additional work and what that work is. |
| **Cost boundary** | Which variable and fixed costs are included or excluded. |
| **Cost per acceptable outcome** | Total relevant cost divided by accepted outcomes. |
| **Latency / availability** | End-to-end service behaviour, not only model latency. |
| **Failure consequence** | What happens when the workflow remains unacceptable. |
| **Customer promise affected** | Which commitment changes if this architecture changes. |

This lets management compare commercial consequences without micromanaging implementation.

## Questions for a product meeting

1. **What customer outcome are we trying to produce?**
2. **What exactly counts as acceptable?**
3. **Which population are our rates and costs measured over?**
4. **Which steps need the strongest available capability, and which do not?**
5. **Which steps should use deterministic software rather than an LLM?**
6. **What architecture options have been compared?**
7. **What is the all-in relevant cost per acceptable outcome?**
8. **How much retry, evaluation, repair, and escalation does each option create?**
9. **What latency and availability can we realistically promise?**
10. **Which engineering choices materially change the customer proposition or unit economics?**

## The broader lesson

AI compresses the distance between architecture and business economics. Model calls may be variable cost; evaluation and escalation may be equally important variable costs; architecture may determine margin and service quality.

That does not make every architecture discussion an executive meeting. It means the organisation needs a reliable translation layer between engineering evidence and commercial decisions.

> **Economics lives in the architecture.**
