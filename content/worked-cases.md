# Worked decisions

These cases are **fictional illustrations**, not reported client incidents. Their purpose is to show how the framework changes a decision rather than merely produce more questions.

## Case 1 — polished customer website, incomplete enquiry workflow

### Situation

An AI agent produces a convincing customer-facing website in one afternoon. The navigation, copy, services pages, contact form and responsive layout all work in the demonstration.

### Established

- the proposed positioning and visual direction have been approved;
- the site structure is coherent;
- the contact form UI can accept input;
- the intended customer journey can be demonstrated to stakeholders.

### Not yet established

- where the enquiry is actually delivered;
- who owns the mailbox or workflow;
- what happens when delivery fails;
- whether required privacy wording is correct;
- the launch acceptance criteria;
- who maintains content and handles incidents after launch.

### Decision

**Approve it as a stakeholder-ready prototype. Do not yet represent it as an operational customer-enquiry service.**

### Next evidence

1. Complete an end-to-end enquiry test in the intended environment.
2. Name the responsible recipient and backup owner.
3. Define failure handling and monitoring.
4. Confirm the relevant launch checks.

The problem is not that AI built the site. The problem would be making a stronger claim than the evidence supports.

---

## Case 2 — small internal tool where the AI-assisted result is already sufficient

### Situation

A team needs a disposable internal page that converts a known CSV export into a formatted summary used during a two-week planning exercise. No personal data is involved. The input format is stable and the output is checked against three known examples.

An agent builds the page in an hour.

### Established

- the task is narrow and temporary;
- the accepted input format is documented;
- three representative outputs match the existing manual calculation;
- the page runs only on the team's existing internal environment;
- the team agrees that an occasional failure can be handled by returning to the spreadsheet process;
- there is no requirement to maintain the tool after the planning exercise.

### Decision

**Use the AI-assisted tool. Do not add a database, production monitoring platform, elaborate test suite, or long-term support process.**

### Why this is responsible

The assurance burden is proportionate to the consequence of failure. Additional engineering would add cost without materially improving the intended outcome.

This case matters because the framework should not make every answer "more review".

---

## Case 3 — cheap production does not by itself prove a business

### Situation

A company can generate a client report for $8 of model and infrastructure cost. Previously the report took several hours of analyst time.

### Keep four variables separate

| Variable | Illustrative question |
| --- | --- |
| **Customer value** | Does the report improve a decision enough that the customer wants it? |
| **Delivery cost** | What do generation, verification, support, revisions and operations cost in total? |
| **Price / willingness to pay** | What will the customer pay given alternative tools and suppliers? |
| **Supplier margin** | Is the price greater than the full delivery cost at the required service level? |

Suppose production falls from $180 to $20, but customers will only pay $25 because comparable outputs are now abundant. The cheaper production is real, but it did not automatically create an attractive business.

Alternatively, suppose the company adds proprietary data, workflow integration, reliable verification and a decision process customers value at $400. The same cheap production can now support a strong margin.

### Decision principle

> **Cheap production creates an opportunity to test — not proof of a profitable business.**

---

## How to use the framework

For any AI-enabled proposal, write down:

1. **Situation** — what is being attempted?
2. **Established** — what has actually been demonstrated or verified?
3. **Not established** — which assumptions remain open?
4. **Decision** — approve, restrict, defer, stop, or scale?
5. **Next evidence** — what would justify changing that decision?

That structure turns the project's distinctions into an actual management decision.
