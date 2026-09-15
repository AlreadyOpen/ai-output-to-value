# Representation is a channel, not the value

A company can be represented by a human. It can also increasingly be represented operationally by software and AI agents.

Those facts do not make the representative the source of the company’s value.

A director meeting a customer face-to-face may be useful. A sales lead joining a video call may be useful. An AI agent answering questions, analysing an offer, handling objections, or acting within delegated authority may also be useful. The business question is not simply **who appeared at the interface**. It is **what capability, authority, substance, evidence, and outcome sat behind that interaction**.

> **Representation is a channel. Value comes from what the company can actually understand, deliver, stand behind, and improve.**

## 1. A human can represent the company without being the only source of judgement

A director, founder, executive, employee, or authorised representative can speak and act for a company within the authority available to them.

Human representation can provide benefits such as:

- negotiation;
- trust-building;
- interpretation of ambiguity;
- empathy and relationship management;
- evaluation in novel situations;
- personal commitment;
- accountability for commitments;
- escalation when another process is insufficient.

But these are **possible sources of value**, not capabilities that should be assumed to belong uniquely to humans.

AI systems can also analyse evidence, compare options, generate persuasive arguments, adapt explanations, answer objections, and support or perform bounded decisions. Whether they do those things well enough for a particular business task is an empirical question.

A face-to-face meeting does not make a weak proposal strong. A polished pitch does not make an unsupported claim true. A senior executive sitting in the room does not turn an unverified capability into a verified one. Likewise, a fluent agent does not become a good salesperson or adviser merely because it sounds convincing.

The representation channel and the underlying business substance should be evaluated separately.

## 2. Face-to-face presence is not an intrinsic value multiplier

Physical meetings can be valuable when they improve an outcome that matters. For example, they may shorten negotiation, surface hidden concerns, strengthen a relationship, allow a physical demonstration, or help participants resolve ambiguity.

But the value is in those effects—not in physical presence itself.

Useful questions are:

- Did the interaction improve understanding?
- Did it reduce uncertainty?
- Did it speed a decision?
- Did it reveal requirements that were otherwise missed?
- Did it create trust that mattered to the transaction?
- Did it change the quality of the outcome?

If not, the fact that people travelled and met in person is activity rather than evidence of greater business value.

The same outcome test can be applied to a video call, an AI voice interaction, an agent-to-agent exchange, a kiosk, or an embodied robot.

## 3. The counterparty can also have agents

It is a mistake to imagine one side of a transaction using AI while the other side remains permanently human-only.

Customers can deploy agents to:

- search and compare suppliers;
- inspect offers;
- query product information;
- check availability and prices;
- analyse claims and documents;
- negotiate within defined parameters;
- make purchases;
- monitor service performance;
- prepare recommendations or questions;
- escalate unusual cases to other actors.

Cloudflare’s agentic-commerce material already describes AI agents searching, browsing, comparing, and buying on behalf of customers. Its announced identity and wallet model is designed around linking agent action to an authorising human or organisation and bounding transaction authority.

Investors and investment teams can likewise use AI systems for parts of research, screening, diligence, document review, monitoring, analysis, and decision preparation. The degree of autonomy and the authority to make or bind investment decisions depends on the organisation, mandate, jurisdiction, and controls in place.

The important point is structural:

> **The supplier should not assume that the person across the table is the only intelligence evaluating the offer.**

## 4. Human-to-human is only one possible interface

Traditional business often assumes this pattern:

**company → human representative → human customer/investor**

Agentic business allows more combinations:

- human representative ↔ human counterparty;
- human representative ↔ counterparty agent;
- company agent ↔ human counterparty;
- company agent ↔ counterparty agent;
- humans and agents share research, analysis, negotiation, approval, and follow-up;
- routine or well-bounded cases are automated while uncertain cases escalate to another model, specialist, manager, or authorised person.

None of these patterns is automatically higher or lower value.

The question is whether the chosen channel and actors improve the outcome while preserving appropriate authority, evidence, security, accountability, and recourse.

### WebMCP makes the channel distinction concrete

**Same standard does not mean the same interface.** A human may use visible controls, forms, menus, and direct manipulation. An AI agent may use a structured tool surface. A hybrid workflow may use both.

WebMCP is an emerging browser interface effort that allows a web page to expose structured tools through `document.modelContext`. Compatible agents can discover those tools, call them with structured arguments, and receive structured results while the page reuses its own application logic.

That matters to this project because an actor-neutral standard should not secretly mean **“the agent must imitate a human clicking the UI.”** The interaction channel can differ while the evidence standard remains the same:

- did the intended action actually happen?
- did it satisfy the same acceptance criteria?
- was the actor authorised to perform it?
- were consequential actions appropriately controlled?
- is there enough audit evidence to understand what occurred?
- can errors be detected, refused, recovered, or escalated?
- did the workflow improve the intended outcome at an acceptable cost and risk?

WebMCP therefore belongs at the **channel / interface** layer. It can improve agent access to a web application, but it does not by itself establish Deliverable, Capability, Outcome, or Value.

A public implementation example is [**Chisel — agentic browser CAD over WebMCP**](https://github.com/helenkwok/chisel-webmcp). It adds a WebMCP surface to an existing browser CAD application and exposes 17 CAD tools around the underlying solid-modelling workflow. Its public implementation routes consequential write operations through a shared confirmation gate and exposes visible activity/audit information.

That example is useful as an implementation pattern, not as independent proof that WebMCP or agent-operated CAD is generally safe or production-ready. The important architectural point is that the **human and agent can use different interfaces over the same underlying capability while consequential actions, evidence, and outcomes remain subject to explicit controls**.

WebMCP should also not be confused with backend MCP transport. It is an in-browser tool surface. The specification is still evolving, so current browser support, security guidance, and interface details should be checked before relying on it operationally.

## 5. Do not confuse personal effort with company value

A common management error is to equate visible personal effort with value:

- the boss personally attended the meeting;
- the founder personally wrote the proposal;
- the senior consultant personally made the slides;
- the developer personally typed the code;
- the executive personally presented to the investor.

These may matter in some contexts. They are not universal measures of value.

The company’s value may instead come from:

- accumulated domain knowledge;
- proprietary or well-governed data;
- reliable processes;
- software and agents;
- distribution;
- integration;
- brand and trust;
- contractual responsibility;
- support and recovery capability;
- intellectual property;
- governance;
- the ability to produce a useful outcome repeatedly.

If an agent can perform a task better, faster, or more consistently, using the agent does not make the company less substantive merely because a human did less visible work.

Likewise, inserting a human into a workflow does not automatically make the result more substantive or better judged.

## 6. A useful representation model

A better model is:

**Company legal entity**

→ **governance actors** — directors and authorised decision-makers

→ **operational actors** — employees, contractors, services, and AI agents

→ **representation channels** — face-to-face meetings, calls, email, web interfaces, APIs, WebMCP and other agent protocols, kiosks, and embodied systems

→ **instruments and infrastructure** — wallets, payment rails, identity systems, API keys, cloud platforms, databases

→ **actions and outcomes** — proposals, contracts, purchases, deliverables, service, investment decisions, support

The distinction matters because **channel, actor, instrument, authority, and outcome are not the same thing**.

A face-to-face meeting is a channel.

A director is a governance actor and may also be a representative.

An AI agent is an operational actor.

A wallet is an instrument.

The company is the legal and organisational entity tying these together.

## 7. Customer and investor agents change how companies should communicate

If counterparties use agents, companies may need to present information in forms that both humans and machines can evaluate.

That may include:

- structured product and pricing data;
- machine-readable terms;
- clear provenance for claims;
- API- or WebMCP-accessible service information and actions;
- evidence and audit records;
- stable identifiers;
- explicit permissions and transaction rules;
- concise human-readable summaries alongside structured detail.

This is not a prediction that every investor meeting disappears or that every client relationship becomes agent-to-agent.

It means the company should not treat human presence as the default proof of seriousness while treating machine-mediated interaction as inherently lesser.

## 8. When should human involvement be required or valuable?

There is no universal answer.

Human involvement may be valuable or required where:

- law or contract requires a named human decision-maker or sign-off;
- an individual’s personal commitment or relationship is part of the value proposition;
- the organisation wants an independent challenge from someone with relevant expertise;
- physical presence or embodiment produces a measurable benefit;
- authority has intentionally not been delegated to software;
- the organisation has evidence that a human or hybrid process performs better for that class of case;
- an exception exceeds the tested operating envelope of the automated system.

These are different from saying that **judgement, negotiation, strategy, or empathy are inherently human-only**.

Human decision-makers are fallible too. A human-in-the-loop control can catch errors, but it can also add delay, inconsistency, bias, or ineffective rubber-stamping. Automated controls can also fail. The assurance design should match the failure mode and consequence.

The project should therefore avoid both extremes:

> “Humans must always be in the loop because humans are the source of judgement.”

and

> “If an agent can technically execute the step, human involvement no longer matters.”

The useful question is:

> **Which actor or combination creates the best evidenced outcome for this decision, with the right authority and accountability?**

See [`ai-business-capability-and-judgement.md`](ai-business-capability-and-judgement.md) for the fuller distinction between analysis, judgement, authority, and accountability.

## 9. The e-commerce precedent

Retail provides a useful historical analogy for this change.

E-commerce did not have to eliminate physical stores in order to change the economics of retail. It shifted part of search, comparison, ordering, payment, and fulfilment into digital channels. Physical stores then had to justify the functions for which physical presence still added value: immediate pickup, product inspection, service, fitting, returns, experience, local fulfilment, or trust.

Official statistics show the shift without implying total replacement. The U.S. Census Bureau reported e-commerce at 17.1% of total U.S. retail sales in Q2 2026. In Australia, the ABS reports that online sales rose from 6.3% of retail turnover in 2019 to 11.4% in 2024. At the same time, OECD research documents hybrid and omnichannel retail rather than a simple disappearance of stores.

Research also shows real disruption. An NBER working paper studying the rollout of a major e-commerce firm's fulfilment centres found lower nearby brick-and-mortar sales and employment, more exits, and less entry. The point is not that physical retail became worthless. The point is that the digital channel changed what the physical channel had to be good for.

That is directly relevant to business representation:

> **E-commerce did not make the store meaningless. It made the store justify what the store was for. AI agents may do the same to human representation.**

See [`ecommerce-and-physical-retail.md`](ecommerce-and-physical-retail.md) for the full evidence and limitations.

## 10. The principle for decision-makers

A concise version for the website:

> **A boss can represent the company. An agent can represent the company operationally. Neither representation is the company’s value by itself.**

And for the other side of the transaction:

> **Your customer or investor can have agents too. Design for counterparties that may be human, agentic, or both.**

## Primary sources and current examples

- WebMCP specification/explainer source: https://github.com/webmachinelearning/webmcp
- OpenAI WebMCP Challenge resources: https://webmcp.devpost.com/resources
- Chisel — agentic browser CAD over WebMCP: https://github.com/helenkwok/chisel-webmcp
- Cloudflare, *Agentic Commerce*: https://www.cloudflare.com/solutions/agentic-commerce/
- Cloudflare, *Cloudflare Gives AI Agents an Identity and a Wallet*, 4 August 2026: https://www.cloudflare.com/press/press-releases/2026/cloudflare-gives-ai-agents-an-identity-and-a-wallet/
- Cloudflare Wallets documentation: https://developers.cloudflare.com/wallets/
- Cloudflare Agents, *Agentic Payments*: https://developers.cloudflare.com/agents/tools/payments/
- OpenAI, *GPT-Realtime*: https://developers.openai.com/api/docs/models/gpt-realtime
- Salvi, F. et al., *On the conversational persuasiveness of GPT-4*: https://www.nature.com/articles/s41562-025-02194-6
- U.S. Census Bureau, *Quarterly Retail E-Commerce Sales*: https://www.census.gov/retail/ecommerce.html
- Australian Bureau of Statistics, *Retail Trade — A journey through 75 years of retail statistics*: https://www.abs.gov.au/articles/retail-trade-journey-through-75-years-retail-statistics
- NBER, *Creative Destruction? Impact of E-Commerce on the Retail Sector*: https://www.nber.org/papers/w30077
- OECD, *Unpacking E-commerce*: https://www.oecd.org/en/publications/unpacking-e-commerce_23561431-en.html
- OECD, *SMEs in the era of hybrid retail*: https://www.oecd.org/en/publications/2023/05/smes-in-the-era-of-hybrid-retail_ea79f5fc.html

WebMCP's specification/explainer supports the claim that a web page can register structured tools for agent discovery and invocation through the browser. The Devpost resource page supports the description of WebMCP as an emerging open standard effort and provides current implementation/testing resources. Chisel is a public practitioner implementation maintained by this project's author; it demonstrates one human/agent/hybrid interface pattern but is not independent evidence of WebMCP safety or business effectiveness.

Cloudflare’s material supports the claim that agents can act on behalf of customers in browsing and commerce and that agent identity can link back to the human or organisation authorising it. OpenAI's documentation establishes realtime conversational interfaces, not sales effectiveness. The persuasion research establishes capability in controlled debate settings, not commercial sales performance. The retail sources support the channel-shift analogy, but retail goods and professional or investment relationships are not identical markets.
