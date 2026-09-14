# Non-human does not mean non-accountable

A company is not a human being. An AI agent is not a human being either.

That similarity is useful, but it should not be pushed too far.

A company can be a **separate legal entity**. An AI agent, today, is generally a **software actor operating under authority delegated by a person or organisation**. Giving an agent an identity, wallet, API key, or ability to transact does not by itself make the agent a legal person.

The important business question is therefore not:

> Was a human personally doing the work?

It is:

> **Where do legal standing, authority, capability, evidence, accountability, and recourse sit?**

## 1. Companies already separate the actor from the human

Companies routinely enter contracts, own assets, incur debts, employ people, sell services, and can sue or be sued even though the company itself is not a natural person.

In Australia, ASIC describes a company as an entity with a legal existence separate from its owners and notes that its legal status allows it to incur debt, sue and be sued. Directors and other officeholders then manage the company and carry legal responsibilities for how it operates.

This means business has never required every commercially relevant action to be performed directly by the legal entity as a human-like actor. Companies act through people, processes, software, contractors, banking systems, delegated authorities, and other mechanisms.

An AI agent can become another mechanism in that chain.

## 2. Agent identity is not the same thing as legal identity

Cloudflare's 2026 Wallets and cloudflare.pay announcement is a useful example of the distinction.

Cloudflare describes giving AI agents a stable identity and the ability to make purchases within limits established by their owners. Its stated goal is to let a receiving business determine who authorised the agent. Cloudflare describes that identity as a link back to the **human or organisation that owns the agent**.

The Wallets documentation makes the delegation model even clearer:

- **Account Wallets** are designed for human owners and users of Cloudflare accounts.
- **Virtual Wallets** are designed for agents.
- owners can delegate spending authority to agent wallets;
- the agent operates within defined permissions.

This is a technical and commercial identity system. It does not, by itself, confer legal personhood on the agent.

## 3. The emerging chain is more useful than a human-versus-AI distinction

A useful model is:

**Legal entity → authority → agent → action / payment → receipt / audit → accountability**

For example:

1. A company has the legal relationship with a client or supplier.
2. The company authorises an AI agent to perform a defined class of actions.
3. The agent receives technical credentials and scoped authority.
4. The agent buys an API result, calls a paid MCP tool, places an order, or performs another permitted action.
5. The transaction produces credentials, receipts, logs, and other evidence.
6. The company remains the place where contractual responsibility and recourse normally sit unless the law or contract provides otherwise.

Cloudflare's Agentic Payments documentation already supports much of the operational middle of this chain. Its HTTP 402 payment flow lets agents request a resource, receive a payment challenge, fulfil the payment, retry with a payment credential, and receive the resource together with a receipt. Production guidance also recommends scoped access keys, spending limits, and recipient restrictions.

## 4. This changes the question for AI-native businesses

An AI-native company does not become insubstantial merely because agents perform much of its operational work.

A one-person or small company could legitimately use agents to perform substantial parts of:

- software development;
- research;
- customer support;
- procurement;
- scheduling;
- document preparation;
- monitoring;
- billing and payments;
- routine operational decisions.

The company may still provide real value through its domain knowledge, data, product design, integration, contractual commitments, distribution, reputation, governance, support, risk-bearing, and ongoing operation.

The important point for **AI Output to Value** is therefore:

> **Human labour is not the measure of substance.**

The project should not imply that a service is legitimate only when humans manually perform a large amount of work.

## 5. But legal form does not create job substance either

The opposite mistake is equally important.

Registering a company does not prove that the company has the expertise or operational capability needed for a client job. Giving an AI agent an identity and wallet does not prove that either.

A limited-liability entity can exist around a very thin operation. An AI agent can perform many actions autonomously. Neither fact alone demonstrates that:

- the client's requirements were understood;
- important assumptions were identified;
- the output was verified;
- the system can be supported;
- the organisation can recover from failure;
- the promised result can be delivered repeatedly;
- the customer has meaningful recourse for the particular risk involved.

This connects directly to the project's existing substance-gap model:

**Tool capability** asks whether the agent can do something.

**Job substance** asks whether the result solves the real job.

**Delivery capability** asks whether the supplier can reliably stand behind it.

A legal company and an autonomous agent can both be parts of delivery capability. Neither substitutes for job substance.

## 6. Accountability may become more important, not less

As agents gain the ability to act and pay without a human approving every individual step, businesses need clearer answers to questions that were previously implicit:

- Which legal entity authorised this agent?
- What is the agent allowed to do?
- What spending or transaction limits apply?
- Which counterparties may it transact with?
- What records prove what happened?
- Who can revoke the authority?
- Who bears the loss if the agent acts incorrectly?
- Which actions require human or higher-level approval?
- What contractual or legal recourse does the counterparty have?

The purpose is not to force a human into every loop. It is to make delegated authority inspectable.

## 7. What Cloudflare's example does and does not show

Cloudflare's 2026 infrastructure is strong evidence that agentic commerce is moving toward stable identity, delegated authority, programmable spending, machine-to-machine payments, and transaction evidence.

It does **not** establish that:

- an AI agent is a legal person;
- an AI agent can currently replace a company director under a particular jurisdiction's company law;
- an agent independently owns the money in a legal sense merely because it controls a virtual wallet;
- the owner is automatically insulated from liability for the agent's conduct.

Those are separate legal questions and must be handled jurisdiction by jurisdiction.

## 8. The distinction the project should preserve

The useful comparison is:

| Company | AI agent |
| --- | --- |
| Non-human legal entity | Non-human software actor |
| Can have separate legal rights and obligations | Can have technical identity and delegated permissions |
| Acts through directors, employees, contractors, systems and agents | Acts through models, tools, credentials and policies |
| Can be a contracting party and locus of legal recourse | Typically acts on behalf of a human or organisation |
| Governance defines who may exercise authority | Policies, credentials and limits define what the agent may do |

The future may change some of these legal boundaries. The current project should not assume that change in advance.

## 9. The business principle

A useful line for decision-makers is:

> **Non-human does not mean non-business. Non-human does not mean non-accountable.**

A company can be non-human and economically substantive. An AI agent can be non-human and operationally capable. What matters is how authority, evidence, capability, responsibility, and value connect.

That also changes the question we ask of an AI-enabled supplier.

Not:

> How many humans worked on this?

But:

> **Who or what did the work, under whose authority, with what evidence, and who can stand behind the result?**

## Primary sources

- ASIC, *Starting a small business company*: https://asic.gov.au/for-business/small-business/starting-a-small-business-company/
- Cloudflare, *Cloudflare Gives AI Agents an Identity and a Wallet*, 4 August 2026: https://www.cloudflare.com/press/press-releases/2026/cloudflare-gives-ai-agents-an-identity-and-a-wallet/
- Cloudflare Wallets documentation: https://developers.cloudflare.com/wallets/
- Cloudflare Agents, *Agentic Payments*: https://developers.cloudflare.com/agents/tools/payments/
- Cloudflare Agents, *Pay from the Agents SDK*: https://developers.cloudflare.com/agents/tools/payments/mpp/pay-from-agents-sdk/
