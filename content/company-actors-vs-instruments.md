# Company actors are not the same as company instruments

A company is a separate legal entity from the people who own and run it. But the company conducts its business through people, systems, policies, software, and delegated authority.

That makes an important distinction necessary:

> **An AI agent can be an operational actor. A credit card, wallet, membership card, or loyalty account is an instrument or credential.**

These are not the same kind of thing.

## The boss is inside the company operating system

A director is not legally identical to the company. However, a director is an internal governance actor who manages or directs the company and carries legal duties in doing so.

Employees and contractors can be human operational actors. Software and AI agents can also perform operational actions under delegated authority.

So a useful business model is:

**Company legal entity**

→ **governance actors** — directors and officeholders

→ **human operational actors** — employees and contractors

→ **software operational actors** — automations and AI agents

→ **instruments and infrastructure** — bank accounts, wallets, payment cards, API keys, databases and cloud services

The categories interact, but they should not be confused.

## Why an AI agent is not just another company card

A company credit card can enable payment. It does not decide which task to pursue.

A gym card proves access. It does not interpret a goal.

A frequent-flyer account records entitlements and activity. It does not plan or execute a workflow.

An AI agent may be able to:

- receive a goal;
- interpret context;
- choose among permitted actions;
- call APIs and tools;
- create or modify work products;
- communicate with other systems;
- initiate a transaction;
- evaluate intermediate results;
- continue a workflow without approval at every step.

That does not make the agent a director, employee, company, or legal person. It makes the agent a **delegated software actor**, rather than a passive credential.

## Cloudflare's architecture helps show the difference

Cloudflare Wallets separates the agent from the wallet it uses.

Cloudflare describes Account Wallets for human account owners and Virtual Wallets for agents. The account owner can delegate spending authority to a virtual wallet, while the agent operates using that wallet within its permissions.

The wallet is therefore an instrument used by the agent. It is not the agent itself.

Cloudflare also describes agent identity as linking the agent back to the human or organisation that authorised it. This gives a useful pattern:

**Legal entity → governance → delegated authority → actor → instrument → action → evidence**

The actor may be human or software.

## Why this matters for AI Output to Value

The project should not imply that human labour is what gives a service substance.

A company can legitimately automate most of a workflow. A very small company may use AI agents extensively and still provide real value.

The important questions are:

- Does the company understand the job it is selling?
- Is the agent acting within appropriate authority?
- Are the necessary requirements and assumptions actually represented?
- Can the result be verified and supported?
- Is there evidence of what happened?
- Can the company stand behind the result?

The boss is part of this chain too. Choosing the tool, defining what the company promises, setting authority, and approving delivery are management actions. Delegation does not move the agent outside the company simply because the agent is non-human.

## A concise principle

> **Non-human does not mean external. An agent can act inside a company's operating system; a card or credential cannot.**

## Sources

- ASIC, *Becoming a company director*: https://www.asic.gov.au/for-business-and-companies/small-business-director-essentials/becoming-a-company-director
- ASIC, *The replaceable rules for company governance*: https://www.asic.gov.au/for-business-and-companies/companies/register-a-company/the-replaceable-rules-for-company-governance
- Cloudflare, *Cloudflare Gives AI Agents an Identity and a Wallet*: https://www.cloudflare.com/press/press-releases/2026/cloudflare-gives-ai-agents-an-identity-and-a-wallet/
- Cloudflare Wallets: https://developers.cloudflare.com/wallets/
