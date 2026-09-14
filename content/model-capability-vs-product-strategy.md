# A model capability is not a product strategy

A new AI model can unlock genuinely useful capabilities. Exploring those capabilities is legitimate R&D.

The management mistake is treating this as automatic:

> **The model can do something impressive, therefore we should create a customer product around it.**

A model capability can start product discovery. It is not, by itself, evidence of a customer problem, a usable workflow, a client-ready service, or a viable business.

## Two different starting points

A capability-first exploration may look like:

**New model → impressive capability → possible application → experiment**

That is useful technology scouting.

A product commitment needs additional steps:

**Customer problem → current workflow → desired outcome → constraints and acceptance criteria → suitable technology → validated solution → delivery model → economics**

The paths can meet. A new capability may reveal an opportunity customers did not know was possible. But before productisation, the capability still has to connect to a real use context and a defensible value proposition.

## Keep five questions separate

1. **Capability discovery** — What can the technology do?
2. **Use-case discovery** — Whose problem does that capability solve, and how is the problem handled today?
3. **Product design** — What complete workflow turns the capability into something useful?
4. **Delivery feasibility** — Can the organisation operate, support, maintain, and stand behind the solution?
5. **Business viability** — Is the result worth paying for after counting the whole system?

## “Can the model make X?” is only one question

A model generating a domain-specific file, design, analysis, or other artefact can be technically significant.

It does not yet establish:

- that the output meets the relevant domain requirements;
- that it interoperates with the customer's actual systems;
- that important semantics survive the workflow;
- that output quality is repeatable enough for the intended use;
- that validation is efficient enough;
- that the customer needs the capability often enough to justify a product;
- that the customer would pay this supplier rather than use the underlying tool directly.

A demonstration can provide **capability evidence**. A product also needs **workflow evidence** and **value evidence**.

## The product is the system around the model

The model may be an important component rather than the whole product. Customer value can come from problem definition, domain knowledge, data and system integration, workflow design, evaluation, governance, a usable interface, reliable operations, accountability, support, maintenance, convenience, and risk reduction.

This is why two organisations using the same underlying model can create very different amounts of value.

It is also why access to a frontier model does not automatically establish a differentiated offering.

## Architecture can change the business case

Even after a useful capability and customer problem have been identified, one more distinction matters:

> **The economics of an AI product are properties of the whole solution architecture, not just the price of the most capable model in it.**

A service may use one model for every request, route simpler work to cheaper models, escalate difficult cases, use a stronger model only for planning or difficult judgement, combine models with deterministic tools, or avoid model calls entirely for steps that conventional software can handle more reliably.

These are engineering choices, but their consequences can change:

- cost per completed customer outcome;
- quality and acceptance rate;
- latency and throughput;
- human-review burden;
- failure and support behaviour;
- vendor dependency;
- customer pricing and margin.

So implementation detail can remain inside engineering while economically material consequences must return to the product and business decision.

See [`architecture-economics-and-product-decisions.md`](architecture-economics-and-product-decisions.md).

## Do not let the model choose the problem

A useful test is:

> **If this particular model were unavailable, would the customer problem still be important?**

If yes, the team probably has a problem worth solving and can compare technologies against it.

If no, the idea may still be worthwhile as an experiment, but it should be described as **capability exploration**, not yet as a validated customer product.

A second test is:

> **What evidence says the customer needs this workflow, rather than evidence that the model can perform the task?**

Those are different evidence sets.

## Cost is not the first business case

Model price matters, but only relative to a use case and an expected outcome.

A cheap workflow can still be wasteful if nobody needs it. A costly workflow can be attractive if it reliably creates much more value than it costs.

The useful question is not only:

> **Can we afford the model?**

It is:

> **Is there a sufficiently valuable workflow here, and is this model the right component of a reliable and economical way to deliver it?**

And once the workflow is identified, ask a second question:

> **What is the cheapest architecture that meets the required quality, latency, reliability, and risk constraints?**

The answer may involve the most capable model, cheaper models, routing, deterministic software, human review, or a combination.

## Eleven questions for a meeting

1. **What customer problem are we solving?**
2. **How is that problem solved today?**
3. **What measurable outcome should improve?**
4. **Which part of the workflow actually requires the most capable model or a distinctive AI capability?**
5. **What evidence shows it works on the exact task we care about?**
6. **What cheaper or simpler alternatives have we compared?**
7. **What architecture options have been compared end-to-end?**
8. **What is the full delivery and operating cost per acceptable outcome, not just the model price?**
9. **What happens when a model is unavailable, too slow, or produces an unacceptable result?**
10. **Which engineering choices materially change the customer promise or unit economics?**
11. **Why would a customer pay us rather than use the underlying model or tool directly?**

## Technology-push innovation is still legitimate

Some important products start with a newly available capability rather than a customer request. Customers cannot always ask for something they do not know is possible.

The distinction is between **discovery** and **evidence**.

Technology can inspire the hypothesis. Product and business evidence still determine whether the hypothesis deserves investment.

> **Capability can start the conversation. Customer value has to finish it.**

## Public guidance supporting the distinction

The **UK Government AI Playbook** says AI use cases should be led by business and user needs, pain points, and inefficiencies rather than by what the technology can do. It also recommends choosing the right tool for the job and considering non-AI alternatives:

https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html

The **NIST AI Risk Management Framework** asks organisations to establish context, clearly define business value or business use, specify intended tasks and application scope, prioritise interdisciplinary participation, and consider expected benefits and costs before deployment decisions:

https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Research on LLM routing and cascades provides concrete examples of how model selection can change the cost-quality frontier without implying that any one architecture is universally best:

- RouteLLM: https://arxiv.org/abs/2406.18665
- FrugalGPT: https://arxiv.org/abs/2305.05176

These sources do not show that every successful product must begin with explicit customer demand, or that multi-model routing is always the correct architecture. They support the narrower principles that AI capability should be evaluated in a defined context of use and that technical design can materially change the economics of delivering that capability.
