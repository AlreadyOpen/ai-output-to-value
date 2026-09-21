# Human-kit reader test

This is the reader-test protocol for the default entry path introduced by issue #13.

## Purpose

Check whether a non-technical sponsor can make a bounded AI-related decision in **15–20 minutes** without first learning the schema, Claim Gate internals, MCP/WebMCP, CLI/CI integration, or `claim.json`.

The test is about the human decision method, not whether the participant understands the repository.

## Participant

Use at least one sponsor, manager, client representative, or budget / operational decision-maker who is comfortable discussing a business proposal but is **not participating as a software/tooling specialist** for this test.

Do not coach the participant on the six claims before the session beyond what the public human kit itself says.

## Materials allowed

Give the participant only:

1. `START-HERE.md` (or the rendered Start Here page);
2. the eight questions;
3. the Claim Card **or** printable meeting brief;
4. the evidence relevant to the chosen decision.

Do not require the participant to open the Claim Gate, schema files, MCP package, WebMCP documentation, CLI, CI, or a JSON record.

## Task

Use a real or safely fictional proposal and ask the participant to:

1. state the next decision in one sentence;
2. work through the eight questions;
3. record what is established and not established;
4. identify the evidence that matters for the decision;
5. choose the next action or stop rule.

Stop after 20 minutes even if the record is incomplete. The point is to expose friction rather than coach around it.

### Watch Questions 4 and 6

Two of the eight questions pack several ideas into one sentence, and an outside review predicted they would stall a 15-minute meeting. Treat that as a hypothesis to test, not a fact. For **Question 4** (what work disappeared or moved, and where the bottleneck goes next) and **Question 6** (who decides, who is accountable, and who verifies, runs and supports it), note without coaching:

- how long the participant takes to give a first answer;
- whether they answer every part, only one part, or skip it;
- whether the facilitator prompt beside the question changed what they said.

### Misleading-summary probe

After the main task, and outside the 20 minutes, give the participant this deliberately misleading summary, with no explanation:

> **“Output: strong; Deliverable: almost; Operating capability: not yet; Outcome / Value: unknown.”**

Ask: **“What is wrong with this assessment, and how would you rewrite it?”**

Use the same materials as above. Do not point the participant to the Claim Gate or hint at the answer.

## Pass conditions

Record whether the participant could, without tooling help:

- identify the decision being made;
- distinguish demonstrated facts from assumptions;
- identify at least one important missing item or limitation;
- name the business outcome or learning objective;
- state what evidence would change the decision;
- leave with a clear continue / restrict / rely / operate / scale / renew / stop action or an explicit statement that evidence is insufficient.

For the probe, the participant must:

- reject the idea that one project can be given one overall rating across the claims;
- rewrite it as separate decisions, each with what the result is for, which version or scope it covers, and the evidence it needs;
- recognise that the same project can be fine for one decision (for example, keep exploring) and not for another (for example, run it repeatedly for customers).

A reader test is not passed merely because the participant can repeat the six claim names.

## Observation record

Complete this section after an actual session.

- **Date:**
- **Participant role (no personal name required):**
- **Scenario / decision:**
- **Materials used:**
- **Elapsed time:**
- **Could run without tooling documentation?** yes / no
- **Could state the decision?** yes / no
- **Could separate established vs assumed?** yes / no
- **Could identify next evidence / stop rule?** yes / no
- **Question 4:** answered fully / one part only / stalled / skipped; seconds to first answer: ___; what they asked or misread:
- **Question 6:** answered fully / one part only / stalled / skipped; seconds to first answer: ___; what they asked or misread:
- **Did the facilitator prompt help on Question 4 or 6?** yes / no
- **Rejected the one-rating summary and rewrote it as separate decisions?** yes / no
- **Where did the participant hesitate or misread the method?**
- **What did the participant say about the misleading summary?**
- **What should change in Start Here / Claim Card / meeting brief?**
- **Result:** pass / revise and retest

## What would change the wording of Questions 4 and 6

Do not reword either question from a single session. If **two or more** participants stall on, or answer only part of, the same question, revise it: split it, or move more of it into the prompt, and retest. If participants answer both fully, keep them as written and record that.

## Evidence rule

Do not pre-fill or invent a successful participant result. The first reviewed release criterion is complete only after an actual non-technical sponsor session has been recorded here or in a linked review record.
