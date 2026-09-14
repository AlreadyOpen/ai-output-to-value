# AI can do business work too: judgement, authority, and accountability are different

AI capability is not confined to coding, drafting, or back-office automation.

Modern AI systems can already participate in many activities that organisations traditionally describe as **business work**:

- analysing reports, files, tables, and other business information;
- preparing proposals, pitches, presentations, scripts, briefs, and customer communications;
- answering enquiries and explaining products;
- researching alternatives and comparing options;
- preparing recommendations and decision material;
- conducting live voice interactions;
- adapting a message to a customer's questions or concerns;
- using tools and APIs to continue a workflow;
- producing or coordinating multimodal content;
- monitoring a situation and escalating or acting within delegated limits.

The project should therefore avoid a misleading division in which AI is treated as capable of implementation while **judgement, persuasion, analysis, strategy, or customer interaction are assumed to belong uniquely to humans**.

> **Judgement is a capability to evaluate. Authority is permission to act. Accountability is where responsibility and recourse sit. They are related, but they are not the same thing.**

## 1. Business work is not defined by being human

A proposal does not become strategically insightful because a human wrote it.

A presentation does not become persuasive because a senior executive delivered it.

A customer reply does not become helpful because a salesperson typed it manually.

Likewise, an AI-generated proposal, analysis, presentation, or customer interaction is not automatically good because the model is advanced.

The relevant questions are the same ones used elsewhere in this project:

- Is the content accurate enough for the intended use?
- Does it address the customer's real problem?
- Does the interaction improve the desired outcome?
- Are important assumptions visible?
- Is the system operating within the right authority?
- Can failures be detected and recovered from?
- Is the result worth the total cost and risk?

This is a more useful standard than asking whether the work was performed by a person or a model.

## 2. AI can participate in persuasion and customer interaction

Persuasion is not a uniquely human capability.

Controlled research has found that large language models can produce persuasive messages and can perform at human-comparable or, in some experimental conditions, stronger levels in structured conversational persuasion tasks. A 2025 *Nature Human Behaviour* study comparing GPT-4 and humans in short debates found no significant difference between non-personalised AI and the human baseline, while personalised GPT-4 was more persuasive than the human baseline in that experiment. A 2025 meta-analysis later found **no significant overall difference** between LLMs and humans across the small set of eligible persuasion studies, with substantial variation by context.

That evidence does **not** prove that an AI system is automatically a good salesperson, negotiator, consultant, public speaker, or account manager. Sales and professional communication involve product knowledge, customer context, timing, trust, compliance, pricing authority, follow-up, and the ability to deal with failure or unusual situations.

It does establish the narrower point:

> **The ability to persuade, explain, handle objections, or adapt arguments should not be treated as a permanent human monopoly.**

The same discipline applies to customer support. Research on a generative-AI conversational assistant used by 5,179 customer-support agents found a 14% average increase in issues resolved per hour in that specific setting, with larger gains among novice and lower-skilled workers, alongside improved customer sentiment. That was an **AI-assisted human workflow**, not evidence that autonomous AI support will always outperform people.

## 3. Realtime AI changes the interface, not the standard of proof

Current realtime AI APIs can process and produce live audio and text, maintain a conversational session, and call or delegate to tools. This makes live AI interaction technically practical across channels such as web applications, voice systems, telephony, kiosks, and other interfaces.

Combined with an appropriate embodied system, the same conversational layer could be connected to a robot or other physical interface.

But this distinction matters:

**Realtime speech capability** is not the same claim as **effective selling, presenting, advising, or customer service**.

A customer-facing AI or embodied agent should be evaluated on outcomes such as:

- factual accuracy;
- successful resolution;
- customer satisfaction;
- conversion or progression through a legitimate sales process;
- ability to answer objections correctly;
- latency and conversational quality;
- accessibility and language coverage;
- safe tool use;
- disclosure and consent where required;
- escalation and recovery;
- compliance with company policy and applicable law;
- total operating cost.

A convincing voice or physical presence is a channel. It is not proof of business effectiveness.

## 4. AI can analyse company information rapidly, but analysis still needs an evaluation target

Modern model APIs can accept files and images and can use tools such as file search, web search, code execution, and custom functions.

That enables workflows such as:

- comparing company reports;
- extracting and reconciling facts across documents;
- calculating metrics from supplied data;
- generating charts and summaries;
- identifying anomalies or missing information;
- preparing questions for management;
- comparing scenarios;
- drafting recommendations;
- connecting an analysis to other company systems through tools.

The mistake would be to turn either direction into a universal rule:

> **“AI analysed it, therefore it must be correct.”**

or

> **“Only a human analyst can exercise judgement.”**

Both are unsupported shortcuts.

The useful standard is task-specific performance: what evidence shows that the analysis is accurate, complete enough, calibrated, useful, and robust to the failure modes that matter?

## 5. Human judgement is not a correctness certificate

Human decision-makers can make excellent decisions. They can also make poor ones.

Formal seniority, confidence, experience, or legal authority does not guarantee that a decision is well calibrated or that a strategy will succeed. Businesses can fail because of market changes, execution problems, financing, competition, bad assumptions, governance failures, technical failures, or poor decisions by people with substantial authority.

The purpose of saying this is not to claim that AI judgement is superior in general.

It is to remove a false baseline:

> **The comparison should not be “fallible AI versus infallible human judgement.” The real comparison is between alternative decision processes, each with different strengths, weaknesses, costs, information, incentives, and failure modes.**

For a defined task, an AI system may be better, worse, or complementary to a human decision-maker. That is an empirical question.

## 6. Separate four things that are often bundled together

| Concept | Question | Can AI participate? |
| --- | --- | --- |
| **Analysis** | What does the evidence indicate? | Yes. Models can retrieve, calculate, compare, summarise, and reason over supplied information. |
| **Judgement / evaluation** | Which option appears better under the stated goals, evidence, and trade-offs? | Yes, subject to task-specific reliability and limits. |
| **Authority** | Who or what is permitted to commit money, make an offer, change a system, or bind the organisation? | Sometimes delegable to software within defined bounds; legal and organisational rules determine the limit. |
| **Accountability / recourse** | Who or what must answer for the outcome, correct failures, and provide legal or contractual recourse? | This is an organisational and legal design question; software capability alone does not answer it. |

This is why **“a human made the decision”** and **“a human is legally accountable for the decision”** are different statements.

It is also why an AI system can perform substantial evaluative work without becoming a legal person or company officer.

## 7. Human-in-the-loop is a control pattern, not a quality guarantee

Human review can be valuable. It can add:

- independent challenge;
- domain context;
- authority that cannot be delegated;
- relationship or trust value;
- handling of exceptions;
- an additional failure detector;
- a legally required approval.

But adding a person to a workflow does not automatically make the workflow correct.

The reviewer may be rushed, under-qualified, overconfident, biased, inattentive, or unable to inspect a large volume of machine-generated material effectively. Conversely, automated checks can sometimes be more consistent than manual review for well-defined conditions.

So assurance should be designed around the failure mode:

- automated tests for deterministic rules;
- cross-model or multi-method checks where useful;
- retrieval and source verification;
- statistical monitoring;
- specialist review for domain-specific risk;
- human approval where authority, law, contract, or relationship requires it;
- hybrid escalation where routine cases are automated and uncertain cases are routed elsewhere.

> **Human-in-the-loop is an architecture choice. It is not a synonym for quality.**

## 8. Evaluate humans, agents, and hybrid systems by the same outcome where possible

For tasks that can be compared meaningfully, useful dimensions include:

- correctness or acceptance rate;
- calibration and uncertainty handling;
- consistency;
- speed and availability;
- cost per acceptable outcome;
- customer satisfaction;
- conversion or resolution rate where appropriate;
- ability to use evidence;
- adaptability to new context;
- compliance and safety;
- recovery from mistakes;
- escalation behaviour;
- auditability;
- resilience when tools, models, or people are unavailable.

Some dimensions cannot be reduced to one score. Legal authority, fiduciary duty, employment responsibility, and personal relationships are not simply benchmark metrics.

The point is symmetry: **do not assume the human wins before measuring the task, and do not assume the AI wins because it is newer or faster.**

## 9. A robot can change presence without changing the underlying questions

An embodied AI system can combine:

**sensors + perception + realtime conversation + planning + tools + physical actuation + safety controls + identity and permissions**

Such a system could potentially perform customer-facing or presentation functions that once required a physically present person.

Whether it is a *good* salesperson, host, guide, presenter, service representative, or public speaker still depends on evidence.

A robot may add value through:

- physical presence;
- mobility;
- gestures or demonstrations;
- access to on-site sensors and equipment;
- continuous availability;
- consistent delivery;
- multilingual interaction;
- integration with digital systems.

It may also introduce new costs and risks:

- hardware reliability;
- physical safety;
- maintenance;
- network dependency;
- privacy;
- social acceptance;
- accessibility;
- security of delegated actions;
- recovery when the embodied system fails.

The right comparison is therefore not **robot versus human in the abstract**. It is **which complete system produces the better outcome for this particular interaction and risk level**.

## 10. The project should not protect management from the same capability test applied to everyone else

AI changes more than implementation work.

It can assist or automate parts of:

- research;
- analysis;
- forecasting;
- reporting;
- presentation;
- customer communication;
- proposal development;
- planning;
- option comparison;
- monitoring;
- negotiation support;
- decision preparation;
- operational coordination.

Therefore, the project should not imply that technical staff must prove their continuing value while management judgement is treated as inherently non-automatable.

The same capability review should apply across the organisation:

> **What outcome does this function improve? Which parts can now be performed by agents? Which authority or accountability cannot simply be inferred from model capability? What evidence shows the resulting human, AI, or hybrid system is better?**

## 11. The principle for decision-makers

The compact version is:

> **Do not confuse human involvement with judgement, or judgement with authority, or authority with accountability.**

And the positive version is:

> **Use the actor—human, AI, automated system, or hybrid—that produces the best evidenced outcome within the required authority, accountability, safety, and economic constraints.**

That principle is deliberately symmetrical.

It does not assume people are obsolete.

It does not assume AI is a junior assistant forever.

It asks what the system can actually do and what the organisation can responsibly stand behind.

## Sources and evidence boundaries

- OpenAI, *GPT-Realtime*: https://developers.openai.com/api/docs/models/gpt-realtime
- OpenAI, *Live API reference*: https://developers.openai.com/api/reference/typescript/resources/live
- OpenAI, *Responses API reference*: https://developers.openai.com/api/reference/cli/resources/responses/methods/create
- Brynjolfsson, E., Li, D. and Raymond, L.R., *Generative AI at Work*, NBER Working Paper 31161: https://www.nber.org/papers/w31161
- Salvi, F. et al. (2025), *On the conversational persuasiveness of GPT-4*, Nature Human Behaviour: https://www.nature.com/articles/s41562-025-02194-6
- Hölbling, L., Maier, S. and Feuerriegel, S. (2025), *A meta-analysis of the persuasive power of large language models*, Scientific Reports: https://www.nature.com/articles/s41598-025-30783-y

The OpenAI documentation establishes technical interfaces and supported modalities/tools; it does not establish sales, presentation, or robot performance. The NBER study establishes results for a particular AI-assisted customer-support setting, not autonomous customer service generally. The persuasion studies concern controlled persuasion tasks, not commercial sales effectiveness. Claims about embodied customer-facing systems in this article are therefore **capability implications and product hypotheses**, not evidence that a particular robot or agent will outperform a human professional.