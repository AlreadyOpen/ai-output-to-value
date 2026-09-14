# Non-human does not mean non-accountable

A company is not a human being. An AI agent is not a human being either.

That similarity is useful, but it should not be pushed too far.

A company can be a **separate legal entity**. An AI agent, today, is generally a **software actor operating under authority delegated by a person or organisation**. Technical identity or the ability to use tools does not by itself make an agent a legal person.

The important business question is therefore not whether a human personally performed the work. It is:

> **Where do legal standing, authority, capability, evidence, accountability, and recourse sit?**

## Companies already act through representatives and systems

Companies routinely enter contracts, own assets, incur debts, employ people, sell services, and can sue or be sued even though the company itself is not a natural person.

In Australia, ASIC describes a company as having a legal existence separate from its owners. Directors and other officeholders manage the company and carry legal responsibilities for how it operates.

Companies therefore already act through people, processes, software, contractors, credentials, and delegated authority. AI agents can become another part of that operating system.

## Agent identity is not legal identity

Cloudflare's August 2026 Wallets and cloudflare.pay announcement is a useful example, but its **availability status matters**.

Cloudflare announced a design in which agent identity can be linked back to the human or organisation that authorised the agent. It also announced an Account Wallet / Virtual Wallet model intended to support bounded delegated spending by agents.

At the documentation review date, **only wallet-handle reservation is available**. Cloudflare's Wallets documentation says a reserved handle does not yet allow sending, receiving, or holding funds. Full wallet access and Virtual Wallet issuance remain forthcoming.

Cloudflare separately documents **Agentic Payments** protocols for agents. Those current payment-flow documents should not be used as evidence that the separate Cloudflare Wallets product is already fully available.

The broader distinction still holds:

**Legal entity → authority → actor → instrument → action → evidence → accountability**

An actor may be human or software. A wallet, API key, card, or other credential is an instrument used by an actor.

## Human labour is not the measure of substance

An AI-native company does not become insubstantial merely because agents perform much of its operational work.

A small company could legitimately use agents for substantial parts of software development, research, analysis, sales preparation, customer support, monitoring, scheduling, document preparation, or routine operational work.

The company may still provide real value through domain knowledge, data, product design, integration, contractual commitments, distribution, reputation, governance, support, risk-bearing, and ongoing operation.

> **Human labour is not the measure of substance.**

The project should not imply that a service is legitimate only when humans manually perform a large amount of work.

## Judgement and accountability are different questions

An AI system can analyse evidence, compare alternatives, recommend an action, persuade a customer, or make a bounded operational decision without becoming the legal entity responsible for the result.

Likewise, a human director or manager can hold legal or organisational authority without that fact proving the quality of the judgement exercised.

Keep the questions separate:

- **Judgement / evaluation** — which option appears better under the available evidence and goals?
- **Authority** — who or what is permitted to act?
- **Accountability** — who must answer for the result?
- **Recourse** — where can a customer, counterparty, employee, regulator, or other affected party seek correction or remedy?

This distinction matters because **human-in-the-loop is not itself an accountability model**. A human can click “approve” without meaningful review. Conversely, an automated system can be extensively tested, logged, bounded, and monitored while responsibility remains with the organisation deploying it.

See [`ai-business-capability-and-judgement.md`](ai-business-capability-and-judgement.md).

## But legal form does not create job substance either

The opposite mistake is equally important.

Registering a company does not prove that the company has the expertise or operational capability needed for a client job. Announcing or adopting agent infrastructure does not prove that either.

Neither fact alone demonstrates that:

- the client's requirements were understood;
- important assumptions were identified;
- the output was verified;
- the system can be supported;
- the organisation can recover from failure;
- the promised result can be delivered repeatedly.

This connects directly to the project's existing model:

**Tool capability** asks whether the agent can do something.

**Job substance** asks whether the result solves the real job.

**Delivery capability** asks whether the supplier can reliably stand behind it.

A legal company and an autonomous agent can both be parts of delivery capability. Neither substitutes for job substance.

## Accountability may become more important, not less

As agents gain more ability to act without a human approving every individual step, businesses need clearer answers to questions such as:

- Which legal entity authorised this agent?
- What is the agent allowed to do?
- What records show what happened?
- Who can revoke its authority?
- Which actions require higher-level approval?
- Where does contractual or legal recourse sit?

The purpose is not to force a human into every loop. It is to make delegated authority inspectable.

## What the Cloudflare examples do and do not show

The Cloudflare material is evidence that infrastructure is being developed for agent identity, bounded authority, machine-readable payments, and transaction evidence.

It does **not** establish that:

- the announced Wallets functionality is fully available today;
- an AI agent is a legal person;
- an AI agent can replace a company director under current company law;
- the organisation that authorised an agent is automatically insulated from responsibility for its conduct.

Those are separate technical, contractual, and legal questions.

## The business principle

> **Non-human does not mean non-business. Non-human does not mean non-accountable.**

A company can be non-human and economically substantive. An AI agent can be non-human and operationally capable. What matters is how authority, evidence, capability, responsibility, and value connect.

The useful question for an AI-enabled supplier is:

> **Who or what did the work, under whose authority, with what evidence, and who can stand behind the result?**

## Primary sources

- ASIC, *Starting a small business company*: https://asic.gov.au/for-business/small-business/starting-a-small-business-company/
- Cloudflare, *Cloudflare Gives AI Agents an Identity and a Wallet*, 4 August 2026: https://www.cloudflare.com/press/press-releases/2026/cloudflare-gives-ai-agents-an-identity-and-a-wallet/
- Cloudflare Wallets documentation, reviewed 14 September 2026: https://developers.cloudflare.com/wallets/
- Cloudflare Agents, *Agentic Payments*: https://developers.cloudflare.com/agents/tools/payments/
