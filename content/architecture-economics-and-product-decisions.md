# Engineering choices can be business decisions

> **Not every engineering detail is a management decision. But when an engineering choice changes cost, quality, latency, risk, or what can be offered to a customer, its consequences are part of the business decision.**

AI products make this boundary especially important.

A discussion can begin with what sounds like a technical question:

- Which model should handle this step?
- Should every request use the most capable model?
- Can a cheaper model perform routine work?
- Should difficult cases be escalated?
- Should one model plan while other components execute?

Those questions have technical implementations. But their answers can determine whether a customer workflow is affordable, reliable, fast enough, supportable, and commercially viable.

That means the correct organisational response is not to make every executive debate model-routing code. It is to separate **implementation detail** from **business consequence**.

## The boundary to preserve

### Engineering should own implementation detail

Examples include:

- router implementation;
- prompts and tool schemas;
- caching and batching;
- SDK and provider integration;
- retry and timeout logic;
- queueing and orchestration;
- deployment topology;
- observability implementation;
- internal evaluation harnesses.

These are normally engineering design decisions within agreed constraints.

### Cross-functional decision-makers need the consequences

Examples include:

- expected cost per completed customer outcome;
- quality or acceptance rate;
- latency and throughput;
- failure and escalation behaviour;
- human-review requirements;
- support burden;
- vendor dependency and portability;
- privacy, security, or regulatory constraints;
- expected gross margin or cost saving;
- whether the resulting service level is good enough for the customer proposition.

These are not merely coding details. They can change the product and its economics.

## Economics lives in the architecture

The price of one model does not determine the cost of an AI-enabled service.

A useful approximation is:

**Cost per customer outcome = planning + generation/execution + tool use + retries + context + verification + infrastructure + human intervention + failure handling + support**

Different architectures can change every term.

For example, a workflow might use:

1. one high-capability model for every request;
2. a lower-cost model for most requests and a stronger model only when needed;
3. a cascade in which an inexpensive model attempts the task first and difficult cases escalate;
4. a router that predicts which model should handle each request;
5. a strong model for planning or difficult judgement while lower-cost models, deterministic software, or tools execute routine steps;
6. no large language model at all for stages that can be handled more reliably by conventional software.

There is no universal winner. The point is that **architecture determines how much expensive capability is actually consumed and what additional verification or recovery work is created**.

So these two statements can both be misleading:

> **“The model is cheap, so the service will be cheap.”**

> **“The model is expensive, so the service cannot be viable.”**

The relevant unit is usually the **completed, acceptable customer outcome**, not the headline token price.

## Selective use of stronger models is an established design pattern

Research on LLM routing and cascading provides evidence that stronger and weaker models can sometimes be combined to improve the cost-quality trade-off.

**RouteLLM** studies learned routing between stronger, more expensive models and weaker, cheaper models. Its experiments show that routing can reduce cost while preserving benchmark performance in the evaluated settings.

**FrugalGPT** studies prompt adaptation, model approximation, and LLM cascades. Its experiments show that selectively combining models can, in some evaluated settings, match or improve the performance of a more expensive model at lower cost.

These results support a general principle:

> **A workflow does not necessarily need to use the most capable model for every step.**

They do **not** prove that any particular planner/executor architecture, router, model pair, benchmark result, or cost saving will transfer to a different customer workflow.

The target workload still needs its own evaluation.

Sources:

- RouteLLM paper: https://arxiv.org/abs/2406.18665
- RouteLLM repository: https://github.com/lm-sys/RouteLLM
- FrugalGPT paper: https://arxiv.org/abs/2305.05176
- FrugalGPT repository: https://github.com/stanford-futuredata/FrugalGPT

## A strong planner plus cheaper executors is a hypothesis, not a law

One plausible architecture is:

**higher-capability model → planning / decomposition / difficult judgement**

followed by:

**lower-cost models or deterministic tools → routine execution**

This can be attractive when the expensive reasoning step is infrequent and the execution steps are easier to verify.

But it should not be treated as an automatic best practice.

Questions include:

- Does the planner actually improve downstream success?
- Can the cheaper executor follow the plan reliably?
- Does decomposition create more calls than a single-model approach?
- How much latency does orchestration add?
- What happens when the plan is wrong?
- Can deterministic software replace some model calls entirely?
- Is verification cheap enough to preserve the expected saving?
- Does the workload contain enough repeated structure for routing or cascading to help?

A multi-model architecture can reduce cost. It can also add complexity, latency, retries, and new failure modes.

That is why the business decision should be based on measured **end-to-end outcomes**, not architectural fashion.

## Technical feasibility and commercial feasibility are coupled

Consider a hypothetical AI-enabled service.

Engineering discovers three possible architectures:

| Architecture | Accepted task rate | Median latency | Estimated cost per completed task | Human review | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| A — strongest model everywhere | 97% | 24 s | $4.20 | 3% | Simple architecture, high model cost |
| B — route routine work to cheaper model | 95% | 15 s | $0.85 | 5% | Lower cost, routing needed |
| C — cheaper model only | 86% | 8 s | $0.18 | 18% | Cheap inference, high downstream burden |

These numbers are illustrative, not benchmark claims.

Engineering can determine how each option works. But choosing among them may depend on questions outside engineering:

- Is 95% acceptable for the customer promise?
- Is a 5% review rate operationally sustainable?
- Does lower latency matter enough to affect adoption?
- What price will the customer pay?
- What support commitment is included?
- How costly is a failed task?
- Does the organisation prefer higher margin or higher assurance?

Once those questions appear, the decision is cross-functional.

## Do not send economically material consequences out of the room

It can be completely reasonable to take implementation discussion offline.

A management meeting does not need to decide:

- how a routing score is calculated;
- which SDK method is called;
- how retries are coded;
- where a cache lives.

But if the engineering discussion changes any of the following, the consequences need to come back into the product/business decision:

- whether the proposed customer workflow is technically possible;
- what quality level is realistically achievable;
- what the workflow costs to deliver;
- how long it takes;
- how much human review is required;
- which risks remain;
- what customer promise can responsibly be made.

A useful rule is:

> **Take implementation detail offline. Bring product-changing consequences back online.**

## Product discovery should be multidisciplinary

The UK Government AI Playbook says AI use cases should be led by business and user needs rather than by what the technology can do, and it calls for multidisciplinary teams that can identify user needs, build and test products, measure service performance, and support live operation.

NIST's AI Risk Management Framework similarly asks organisations to establish deployment context, define business value, document intended tasks, prioritise interdisciplinary participation, and examine expected benefits and costs.

These are governance sources rather than proofs of commercial success. They support the narrower organisational principle that **business context, domain expertise, technical design, risk, and economics should meet during AI product discovery**.

Sources:

- UK Government AI Playbook: https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html
- NIST AI RMF Core: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST AI RMF Playbook — MAP: https://airc.nist.gov/airmf-resources/playbook/map/

## A better division of decision rights

A practical operating model is:

### Business / product / domain

Define:

- the customer problem;
- the desired outcome;
- the acceptable service level;
- critical constraints;
- risk tolerance;
- commercial goals;
- what would count as a useful solution.

### Engineering

Design and test:

- alternative architectures;
- model/tool combinations;
- routing or escalation logic;
- reliability mechanisms;
- evaluation methods;
- operating and failure behaviour.

### Cross-functional decision

Compare options on:

- quality;
- cost;
- latency;
- reliability;
- support burden;
- security and compliance;
- customer fit;
- price and margin;
- strategic dependency.

The objective is not to let business micromanage engineering or to let engineering define the product alone.

The objective is to make **trade-offs visible before commitments are made**.

## Use cost per acceptable outcome, not cost per call

A cheap model can create an expensive workflow if it causes:

- more retries;
- more human review;
- more corrections;
- more failed downstream actions;
- more support incidents;
- more customer rework.

A more expensive model can sometimes reduce total cost if it reduces those downstream terms.

The opposite can also be true: using a frontier model for simple, easily verified work can waste money without improving the outcome.

So the measurement unit should be close to what the customer or business actually values:

- cost per accepted document;
- cost per resolved case;
- cost per successful design iteration;
- cost per completed workflow;
- cost per validated analysis;
- cost per correctly executed transaction;
- cost per customer outcome.

This keeps optimisation connected to value rather than model prestige.

## Questions for a product meeting

1. **What customer outcome are we trying to produce?**
2. **What quality threshold is actually required?**
3. **Which steps need the strongest available reasoning, and which do not?**
4. **Which steps should use deterministic software rather than an LLM?**
5. **What architecture options have been compared?**
6. **What is the end-to-end cost per acceptable outcome?**
7. **How much review, retry, and failure-handling work does each option create?**
8. **What latency and availability can we realistically promise?**
9. **Which technical choices materially change the customer proposition or unit economics?**
10. **Which implementation details can engineering decide independently once those constraints are agreed?**

## The broader lesson

AI compresses the distance between technical architecture and business economics.

When model calls are a material variable cost, routing, cascading, tool use, verification, and human escalation can directly determine margin and service quality.

That does not make every architecture review an executive meeting.

It means the organisation needs a reliable translation layer between engineering evidence and commercial decisions.

> **Engineering owns the mechanism. The business must understand the consequences.**

And the most compact version is:

> **Economics lives in the architecture.**
