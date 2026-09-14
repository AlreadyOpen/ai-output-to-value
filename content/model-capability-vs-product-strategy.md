# A model capability is not a product strategy

A new AI model can unlock genuinely useful capabilities. Exploring those capabilities is legitimate R&D.

The management mistake is treating this as automatic:

> **The model can do something impressive, therefore we should create a customer product around it.**

A model capability can start product discovery. It is not, by itself, evidence of a customer problem, a usable workflow, a client-ready service, or a viable business.

## Two different starting points

Capability-first exploration may look like:

**new capability → possible application → experiment**

That is useful technology scouting.

A product commitment needs additional evidence:

**customer problem → current workflow → desired outcome → constraints / acceptance rule → technology choice → solution architecture → delivery model → economics**

The paths can meet. A new capability may reveal an opportunity customers did not know was possible. The capability still has to connect to a real use context and a defensible value proposition before productisation.

## Keep six questions separate

1. **Capability discovery** — What can the technology do?
2. **Use-case discovery** — Whose problem might that capability solve, and how is the problem handled today?
3. **Product design** — What complete workflow would turn the capability into something useful?
4. **Solution architecture** — Which combination of models, deterministic tools, data, evaluation, escalation, and operational components meets the required outcome?
5. **Delivery feasibility** — Can the organisation operate, support, maintain, recover, and stand behind the solution?
6. **Business viability** — Is the result worth paying for after counting the whole system?

## “Can the model make X?” is only one question

A model generating a domain-specific file, design, analysis, or other artefact can be technically significant.

It does not yet establish:

- that the output meets the relevant domain requirements;
- that it interoperates with the customer's actual systems;
- that important semantics survive the workflow;
- that output quality is repeatable enough for the intended use;
- that evaluation is efficient enough;
- that the customer needs the capability often enough to justify a product;
- that the customer would pay this supplier rather than use the underlying tool directly.

A demonstration can provide **capability evidence**. A product also needs **workflow evidence** and **value evidence**.

## The product is the system around the model

The model may be an important component rather than the whole product. Customer value can come from problem definition, domain knowledge, data and system integration, workflow design, evaluation, governance, interface design, reliable operations, accountability, support, maintenance, convenience, and risk reduction.

Two organisations using the same underlying model can therefore create very different amounts of value.

Access to a frontier model does not automatically establish a differentiated offering.

## Architecture can change the business case

The economics of an AI product are properties of the whole solution architecture, not just the price of the most capable model in it.

A service may use one model for every request, route easier work to cheaper models, escalate uncertain cases, use a stronger model for planning or difficult evaluation, combine models with deterministic tools, or avoid model calls for steps conventional software can handle more reliably.

These choices can change:

- cost per acceptable customer outcome;
- quality and acceptance rate;
- latency and throughput;
- evaluation / escalation burden;
- failure and support behaviour;
- vendor dependency;
- pricing and margin.

See [`architecture-economics-and-product-decisions.md`](architecture-economics-and-product-decisions.md).

## Do not let the model choose the problem

A useful test is:

> **If this particular model were unavailable, would the customer problem still be important?**

If yes, the team probably has a problem worth solving and can compare technologies against it.

If no, the idea may still be worthwhile as an experiment, but it is more accurately described as **capability exploration** than a validated customer product.

A second test is:

> **What evidence says the customer needs this workflow, rather than evidence that the model can perform the task?**

Those are different evidence sets.

## Technology-choice comparison

Do not finish the discussion at “the model can do it.” Write down why this technology belongs in the product.

| Field | Question |
| --- | --- |
| **Customer problem** | What important problem exists independently of this model? |
| **Desired outcome** | What should improve, and how will we know? |
| **Required capability** | Which part of the workflow actually needs AI or this model's distinctive capability? |
| **Task evidence** | What evidence shows the model performs the exact task at the required quality? |
| **Alternatives** | What cheaper model, conventional software, existing product, manual process, or hybrid approach could achieve the outcome? |
| **Constraints** | What latency, privacy, security, integration, availability, regulatory, or deployment constraints matter? |
| **Evaluation / recovery** | How are unacceptable outputs detected, corrected, or escalated? |
| **Switchability** | What happens if model quality, price, terms, or availability changes? |
| **Full delivery cost** | What is the cost per acceptable outcome after tools, retries, evaluation, infrastructure, support, and failures? |
| **Supplier value** | Why should a customer buy the complete service rather than use the underlying model or tool directly? |

A useful decision statement is:

> **We prefer [technology / architecture] for [workflow] because it meets [acceptance rule] at [measured cost / latency / risk], and it performs better for this use than [alternatives]. The main remaining uncertainty is [unknown], which we will test with [next experiment].**

This gives the article a concrete output: **a technology-choice comparison**, not merely a warning against technology-push thinking.

## Cost is not the first business case

Model price matters only relative to the use case and expected outcome.

A cheap workflow can be wasteful if nobody needs it. A costly workflow can be attractive if it reliably creates much more value than it costs.

The useful questions are:

> **Is there a sufficiently valuable workflow here?**

and then:

> **What is the least costly architecture that meets the required quality, latency, reliability, and risk constraints?**

The answer may involve a frontier model, cheaper models, routing, deterministic software, automated evaluation, specialist intervention, human approval where required, or a combination.

## Questions for a meeting

1. **What customer problem are we solving?**
2. **How is it solved today?**
3. **What measurable outcome should improve?**
4. **Which part genuinely needs this AI capability?**
5. **What evidence shows it works on the exact task?**
6. **What simpler or cheaper alternatives have we compared?**
7. **What architecture options have been compared end-to-end?**
8. **What is the full delivery cost per acceptable outcome?**
9. **What happens when the model is unavailable or produces an unacceptable result?**
10. **Which technical choices materially change the customer promise or unit economics?**
11. **Why would a customer pay us rather than use the underlying model or tool directly?**

## Technology-push innovation is still legitimate

Some important products start with a newly available capability rather than an explicit customer request. Customers cannot always ask for something they do not know is possible.

The distinction is between **discovery** and **evidence**.

Technology can inspire the hypothesis. Product and business evidence still determine whether the hypothesis deserves investment.

> **Capability can start the conversation. Customer value has to finish it.**

## Public guidance supporting the distinction

The **UK Government AI Playbook** says AI use cases should be led by business and user needs, pain points, and inefficiencies rather than by what the technology can do. It also recommends choosing the right tool for the job and considering non-AI alternatives:

https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html

The **NIST AI Risk Management Framework** asks organisations to establish context, define business value or business use, specify intended tasks and application scope, prioritise interdisciplinary participation, and consider expected benefits and costs before deployment decisions:

https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Research on LLM routing and cascades provides examples of how model selection can change cost-quality trade-offs without implying that one architecture is universally best:

- RouteLLM: https://arxiv.org/abs/2406.18665
- FrugalGPT: https://arxiv.org/abs/2305.05176

These sources do not show that every successful product must begin with explicit customer demand, or that multi-model routing is always correct. They support the narrower principles that AI capability should be evaluated in a defined context of use and that technical design can materially change the economics of delivering it.
