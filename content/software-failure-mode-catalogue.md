# Software and architecture failure-mode catalogue

**Evidence character: editorial operational synthesis with external reference anchors.**

This catalogue exists to answer a practical question:

> **What can make an implementation look complete at Output while still failing the evidence needed for Deliverable or Capability?**

It is not a maturity score, a vulnerability ranking, or a claim that every project needs every control. Use the failure modes that are material to the **decision and intended use**.

The canonical machine-readable catalogue is [`data/failure-modes.yml`](../data/failure-modes.yml). The public build also exposes it through the publication API.

## How to use the catalogue

1. Name the **target decision** first: explore, rely, operate, measure outcome, or scale/renew/stop.
2. Identify failure modes that could invalidate the claim required for that decision.
3. Choose evidence that directly tests those failure modes.
4. Do not add controls that would not change the decision.
5. If a required check fails, the gate is **BLOCKED**. If required evidence is missing, the gate is **INSUFFICIENT EVIDENCE**.

The identity of the producer does not change the failure mode. Human-written code can have an authorization gap. AI-generated code can be correct. A deterministic migration can lose data. A specialist tool can miss an integration assumption. Evaluate the complete process and result.

## Catalogue at a glance

| Failure mode | Why Output can still look good | Earliest claim at risk | Verification pattern |
| --- | --- | --- | --- |
| **Functional facade** | UI/API/demo exists but the promised downstream action is absent or unverified. | **Deliverable** | End-to-end test, contract test, failure injection |
| **Environment/configuration gap** | Local defaults, credentials or permissions differ from the target environment. | **Deliverable** | Representative-environment test, configuration review |
| **Acceptance-oracle gap** | Tests validate the implementation rather than the real acceptance criteria. | **Deliverable** | Acceptance test, invariant check, negative/boundary tests |
| **Exceptional-condition failure** | Happy path works; timeout, malformed data or partial failure does not. | **Deliverable** | Fault injection, timeout/degraded-mode tests |
| **Retry duplicate side effect** | One successful call works; ambiguous retry creates a second effect. | **Deliverable** | Idempotency, retry and reconciliation tests |
| **Authorization boundary gap** | Allowed user works; forbidden user/tenant/object was never tested. | **Deliverable** | Negative authorization/object-level access tests |
| **Migration semantic loss** | SQL executes, but real historical data or invariants are damaged. | **Deliverable** | Representative-data rehearsal, invariants, rollback/forward-fix test |
| **Concurrency/state race** | Sequential tests pass; concurrent calls create impossible or stale state. | **Deliverable** | Concurrency/property tests and invariant checks |
| **Supply-chain integrity gap** | Dependency resolves, but provenance/integrity/update path is unverified. | **Deliverable** | Locked/reproducible build, provenance/dependency review |
| **Observability blindness** | Service runs while directly watched, but failure is invisible in normal operation. | **Capability** | Monitoring/alert test, synthetic check |
| **Rollback/recovery gap** | Forward deployment works; bad change or partial failure cannot be recovered. | **Capability** | Rollback, restore or failover rehearsal |
| **Hidden manual/expert step** | Original builder silently compensates from memory or local state. | **Capability** | Runbook rehearsal, handover test, dependency map |
| **Scale/cost/latency cliff** | Demo volume hides queueing, context growth, retries, rate limits or cost. | **Capability** | Load/capacity/rate-limit test, cost per acceptable outcome |

## The important boundary: Deliverable vs Capability

A **Deliverable** claim is about a defined result being fit for a defined use. It does not require building a permanent operations organisation around every one-off output.

A **Capability** claim is stronger. It says the organisation can repeatedly verify, operate, support, maintain, recover and improve the workflow.

That distinction changes what evidence matters.

For example, a one-off migration can become a Deliverable after a representative rehearsal, invariant checks, and an acceptable recovery plan for that migration event. Claiming an ongoing migration capability requires more: repeatable tooling, ownership, runbooks, monitoring, backup/restore expectations, and a process that does not depend on one person's memory.

## Failure mode 1 — functional facade

A form, endpoint or workflow may look complete while its promised side effect is missing.

**Output evidence:** the interface renders and accepts data.

**Deliverable evidence:** a test proves that an enquiry reaches the intended destination, failures are surfaced, and the intended-use acceptance criteria are met.

**Capability evidence:** the handoff is monitored, an owner is named, and failed submissions can be diagnosed or replayed.

The transition is not caused by adding more code. It is caused by establishing the claim that matters.

## Failure mode 2 — acceptance-oracle gap

Passing tests do not automatically establish Deliverable if the tests merely reproduce implementation assumptions.

A useful chain is:

**business acceptance criterion** → **observable test/evaluation** → **evidence result**

rather than:

**generated function** → **generated test that agrees with the function** → **"done"**

Independent review can be human, AI, deterministic, specialist-tool, or hybrid. The relevant property is whether the evaluation meaningfully checks the acceptance criterion rather than merely restating the originating implementation.

## Failure mode 3 — retry duplicate side effect

Distributed calls can fail ambiguously: the caller may time out after the server has already completed the action. A blind retry can then repeat the side effect.

For retryable consequential operations, evidence may need to show an idempotency/deduplication contract, repeated-request behaviour, and reconciliation for ambiguous completion.

This is a good example of why **"the API call worked once"** is Output evidence, not automatically Deliverable evidence.

## Failure mode 4 — authorization boundary gap

Positive-path evidence answers:

> Can this actor perform the allowed action?

Authorization evidence also needs to answer:

> Are actors outside the intended authority boundary refused?

For a customer-facing or multi-tenant system, testing only the allowed path can leave a serious substance gap even when the feature is otherwise polished.

## Failure mode 5 — migration semantic loss

A generated schema migration can be syntactically valid and run cleanly against a toy database while still damaging real data.

A stronger Deliverable case may require:

- representative historical data;
- before/after row counts and domain invariants;
- compatibility with the application versions used during rollout;
- a tested rollback or forward-fix path appropriate to the migration;
- explicit handling of long-running or partial migration failure where material.

An ongoing migration **Capability** adds repeatability: a maintained procedure, ownership, backup/restore expectations, monitoring and a process for future migrations.

## Failure mode 6 — observability blindness

A service can be fit for a one-off use without a full observability platform. But a claim that the organisation can operate it repeatedly becomes weak if important failures are invisible until a customer reports them.

The control should match the failure mode. Relevant evidence may be a simple synthetic check and actionable alert; it does not automatically require a large monitoring stack.

## Failure mode 7 — scale/cost/latency cliff

A five-request demo does not establish an operating capability at 50,000 requests per day.

At intended volume, the system may encounter:

- queueing and concurrency effects;
- API or model rate limits;
- larger context or payload costs;
- retries and fallback calls;
- evaluator/review load;
- database contention;
- external-service quotas;
- latency that breaks the user workflow.

The relevant economic unit is the **complete workflow**, not the cheapest successful call.

## Reference anchors and limits

The catalogue uses several external sources as **reference anchors**, not as proof that this project's categories form a universal taxonomy:

- **OWASP Top 10:2025** includes categories for Security Misconfiguration, Insecure Design, Software or Data Integrity Failures, Security Logging and Alerting Failures, and Mishandling of Exceptional Conditions: https://top10.owasp.org/2025/
- **NIST SP 800-218 (SSDF 1.1)** describes a core set of secure software-development practices intended to be integrated into software-development lifecycles: https://csrc.nist.gov/pubs/sp/800/218/final
- **AWS Builders' Library — Making retries safe with idempotent APIs** describes idempotency as a way to make retried distributed operations avoid unintended additional side effects: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/

Those sources support specific engineering concerns. They do **not** establish the six-claim framework, rank these failure modes by prevalence, or prove that a particular control is proportionate for a particular project.

## Practical rule

> **Do not ask whether the code looks finished. Ask which failure could invalidate the claim required for the next decision, and what evidence would expose that failure.**

Then stop when additional evidence would no longer change the decision.
