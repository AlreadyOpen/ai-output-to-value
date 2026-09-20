# Value cost ledger

Use this when the decision is **scale, renew, expand, or stop** and the required claim is **06 Value**.

This is a fillable decision workbook for a bounded decision, not a universal ROI calculator. Complete it with the units that matter to the decision. Do not convert unlike units into one total unless the conversion is explicit and defensible.

A completed ledger can supply evidence to a Claim Gate record, but it does **not** mark any gate check PASS automatically.

> **Value = evidenced Outcome considered against the full relevant cost, labour movement, elapsed-time effect, risk, alternatives, trade-offs, and option value for the defined decision.**

## 1. Decision boundary

| Required field | Entry |
| --- | --- |
| Initiative / intervention |  |
| Decision sought — scale / renew / expand / stop / other |  |
| Workflow / population in scope |  |
| Observation period |  |
| Baseline or reasonable alternative |  |
| Outcome evidence being valued |  |
| Attribution qualification |  |
| Decision owner |  |

## 2. Work and time boundary

Record **elapsed time** and **labour hours** separately. Record labour that disappears separately from labour that moves into review, rework, support, or incident handling.

| Required field | Baseline / alternative | AI-assisted / proposed | Difference | Evidence / source | Notes / uncertainty |
| --- | ---: | ---: | ---: | --- | --- |
| Elapsed time for the defined workflow |  |  |  |  |  |
| Total labour hours for the defined workflow |  |  |  |  |  |
| Labour displaced / removed from the prior task |  |  |  |  |  |
| Labour moved into review / checking |  |  |  |  |  |
| Labour moved into rework / correction |  |  |  |  |  |
| Labour moved into support / maintenance |  |  |  |  |  |
| Labour moved into incident handling / recovery |  |  |  |  |  |
| Other material labour movement |  |  |  |  |  |

Do not count “minutes saved” as labour removed when the work simply reappears elsewhere in the workflow.

## 3. Cash and operating cost boundary

Use money, labour/time, or another suitable unit. Preserve the original unit when a conversion would create false precision.

| Cost / trade-off | Baseline / alternative | AI-assisted / proposed | Difference | Evidence / source | Notes / uncertainty |
| --- | ---: | ---: | ---: | --- | --- |
| Model / API / tool / vendor cost |  |  |  |  |  |
| Infrastructure — compute / storage / network |  |  |  |  |  |
| Integration / data preparation |  |  |  |  |  |
| Testing / evaluation / assurance / security |  |  |  |  |  |
| Deployment / migration / change management |  |  |  |  |  |
| Monitoring / observability |  |  |  |  |  |
| Support / maintenance / debugging |  |  |  |  |  |
| Rework / rollback / recovery |  |  |  |  |  |
| Incident / error / risk cost material to this decision |  |  |  |  |  |
| Procurement / contract / governance overhead |  |  |  |  |  |
| Opportunity cost / alternative not taken |  |  |  |  |  |
| Other decision-relevant cost or trade-off |  |  |  |  |  |

## 4. Outcome, alternatives, and option value

| Required field | Entry |
| --- | --- |
| Outcome change being valued |  |
| Measurement definition stayed consistent? — yes / no / qualified |  |
| Material confounds or attribution limits |  |
| Adverse effects / quality regressions |  |
| Reasonable alternatives considered |  |
| What happens if we do nothing? |  |
| Opportunity cost / alternative not taken |  |
| **Option value of information**, including a justified stop |  |
| Evidence that supports the option-value claim |  |

A justified stop can be a positive result. Information that prevents a larger commitment can have decision value even when no production system is launched. Do not turn the avoided future spend into automatic realised profit; state the counterfactual and uncertainty.

## 5. Pre-agreed value rule

Write the rule before reading the final result where practical.

Examples:

- renew only if the measured Outcome exceeds the agreed threshold without a material increase in instability or support burden;
- scale only if the additional Outcome remains worthwhile after review, integration, operating, and support cost;
- stop if the next evidence is unlikely to change the decision enough to justify further spend.

**Our scale / renew / expand / stop rule:**

**Result that would reverse or materially weaken the conclusion:**

## 6. Decision record

**Decision:** scale / renew / expand / stop / continue measuring

**Why:**

**Attribution qualification:**

**Evidence still missing:**

**Next review point:**

**What would change this decision:**

---

## Worked example — positive option value from stopping a bad idea

**Proposal:** build an AI-assisted self-service workflow for a specialist internal request type.

**Pre-agreed rule:** continue to a production build only if at least 15 of 50 representative users complete the prototype task successfully and say they would use it for the defined request.

**Pilot result:** 50 users tested the prototype; 6 completed the task successfully and 4 said they would use it. The threshold was not met.

**Pilot cost:** AUD 8,000 in prototype, participant, and analysis effort.

**Planned next commitment if the pilot passed:** approximately AUD 80,000 for integration, assurance, rollout, and first-year support.

**Decision:** stop.

**Why this is still a positive information result:** the pilot resolved a decision-critical uncertainty before the larger commitment. It provided option value by supporting a justified stop and preserving the ability to spend that budget on another alternative.

**What is *not* claimed:** this ledger does not book AUD 72,000 as realised profit or claim universal ROI. The AUD 80,000 build was a planned counterfactual, not cash already earned. The defensible claim is that the bounded experiment supplied useful information that changed the decision and avoided making the larger commitment under the stated assumptions.

**Attribution qualification:** strong for the stop decision because the threshold and population were set in advance; weak for any claim about wider market demand beyond this internal population.

---

This ledger supports a Value decision record. It does not independently verify the underlying Outcome measurement, price risk, labour estimates, counterfactual, or evidence sources.
