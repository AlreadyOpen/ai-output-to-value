# Software and architecture worked cases — where Output becomes Deliverable and Operating capability

**Evidence character: fictional engineering cases.** The code and measurements below are constructed examples used to show claim boundaries. They are not reported incidents.

The point is not that every software change needs every control. The point is to show the **exact moment the justified claim changes**.

A useful shorthand is:

**Output** — the artefact/action exists.

**Deliverable** — evidence shows it is fit for the named intended use.

**Operating capability** — the organisation can repeatedly verify, operate, support, recover, maintain and improve the workflow.

The stable machine identifier for **Operating capability** remains `04-capability`.

The producer can be human, AI, automated or hybrid. The transition is created by evidence and operating capability, not by producer identity.

---

## Case A — generated database migration

### Situation

An agent is asked to add a `customer_tier` field to an existing PostgreSQL `customers` table and classify historical customers using an agreed business rule.

It produces:

```sql
ALTER TABLE customers
ADD COLUMN customer_tier text NOT NULL DEFAULT 'standard';

UPDATE customers
SET customer_tier = 'priority'
WHERE lifetime_value >= 10000;
```

The SQL parses and runs against an empty development database.

### At this point: Output

What has been demonstrated?

- a migration script exists;
- PostgreSQL accepts the syntax in the development environment;
- the intended transformation is visible in code.

What has **not** been established?

- whether the historical `lifetime_value` data is complete enough for this classification;
- whether the threshold matches the real business rule for all legacy cases;
- whether the migration completes within the acceptable deployment window on representative data;
- whether the application version running during rollout tolerates the new schema/state;
- whether the result preserves required invariants;
- how a partial or incorrect migration is recovered.

Calling this production-ready would be a claim jump from **Output** to **Deliverable**.

### Evidence that changes the claim to Deliverable

Assume the intended use is:

> **Apply this migration once to the production customer database during the planned maintenance window.**

The team now provides:

1. a restored production-like snapshot with representative historical cases;
2. a migration rehearsal against that snapshot;
3. before/after checks such as:

```sql
SELECT COUNT(*) FROM customers;
SELECT customer_tier, COUNT(*) FROM customers GROUP BY customer_tier;
SELECT COUNT(*)
FROM customers
WHERE customer_tier = 'priority'
  AND lifetime_value < 10000;
```

4. business-rule spot checks for known legacy customers;
5. an acceptance threshold for migration duration and lock impact;
6. a tested backup/restore or forward-fix plan appropriate to this migration;
7. an application compatibility check for the rollout sequence.

If those acceptance criteria pass, the evidence can justify:

> **Deliverable: this migration is fit for this named production migration event.**

That still does **not** prove the organisation has a mature migration capability.

### Evidence that changes the claim to Operating capability

The stronger claim is:

> **We can perform this class of production schema/data migration repeatedly and support it.**

Additional evidence now matters:

- migration changes are versioned and reviewed through a repeatable pipeline;
- representative rehearsal is a standard step rather than a one-off improvisation;
- backup/restore expectations and maintenance-window ownership are defined;
- deployment status and post-migration anomalies are observable;
- there is a named owner and escalation path;
- future migrations do not depend on one person's local script or memory;
- failed migrations have a rehearsed recovery path.

### Boundary

**SQL runs** → Output.

**This migration meets defined production acceptance criteria** → Deliverable.

**The organisation can repeatedly execute and recover this class of migration** → Operating capability.

---

## Case B — invoice API with retry behaviour

### Situation

A developer or coding agent adds an endpoint that creates an invoice in an external billing service.

```ts
export async function createInvoice(orderId: string) {
  const order = await db.orders.findUnique({ where: { id: orderId } });
  return billing.createInvoice({
    customerId: order.customerId,
    amount: order.total
  });
}
```

A test call succeeds and an invoice appears in the billing sandbox.

### At this point: Output

The implementation can create an invoice once.

But suppose the billing service creates the invoice and the network response is lost. The caller sees a timeout and retries. The second request may create a second invoice unless the operation has a safe retry/deduplication contract.

A successful happy-path demonstration therefore does not establish the intended use if retries are part of normal failure handling.

### Evidence that changes the claim to Deliverable

The implementation is changed so the operation has a stable request identity:

```ts
export async function createInvoice(orderId: string) {
  const order = await db.orders.findUnique({ where: { id: orderId } });

  return billing.createInvoice({
    idempotencyKey: `order:${order.id}:invoice:v1`,
    customerId: order.customerId,
    amount: order.total
  });
}
```

The acceptance evidence now includes:

- repeating the same request does not create an unintended second invoice;
- timeout-after-success is simulated;
- retry exhaustion has an explicit result;
- ambiguous completion can be reconciled against the billing provider;
- invalid/missing orders fail without creating side effects;
- the authority boundary for invoice creation is explicit.

If those criteria pass for the named workflow, **Deliverable** is justified.

### Evidence that changes the claim to Operating capability

Repeated operation needs more than the function:

- idempotency state/key behaviour is documented and maintained;
- duplicate/reconciliation anomalies are measurable;
- failed billing operations have an owner and alert/escalation path;
- the provider's rate limits and retry policy are known;
- the workflow has a support/recovery procedure;
- invoice creation can be traced back to the originating order and actor/action.

### Boundary

**One invoice was created** → Output.

**The invoice workflow is correct under the defined success/failure/retry conditions** → Deliverable.

**The organisation can repeatedly operate, observe, reconcile and recover the workflow** → Operating capability.

---

## Case C — authenticated export endpoint with missing authorization evidence

### Situation

An internal application adds an endpoint that lets signed-in users download a project report.

```ts
app.get('/projects/:projectId/export', requireLogin, async (req, res) => {
  const report = await buildProjectReport(req.params.projectId);
  res.json(report);
});
```

A logged-in project manager can call the endpoint successfully.

### At this point: Output

The endpoint works for an allowed user.

But the code only proves **authentication**. It does not establish that the user is authorised to export the requested project.

A user from Project A may be able to request the ID for Project B.

### Evidence that changes the claim to Deliverable

The resource boundary becomes explicit:

```ts
app.get('/projects/:projectId/export', requireLogin, async (req, res) => {
  const project = await db.projects.findUnique({
    where: { id: req.params.projectId }
  });

  if (!project || !canExportProject(req.user, project)) {
    return res.sendStatus(403);
  }

  res.json(await buildProjectReport(project.id));
});
```

The acceptance suite now checks:

- allowed role + allowed project → permitted;
- allowed role + different tenant/project → refused;
- insufficient role + same project → refused;
- deleted/unknown project → safe failure;
- the check is enforced server-side at the resource boundary;
- export contents themselves meet the intended data-access rules.

Now the claim can become:

> **Deliverable: the export endpoint is fit for the named internal access model.**

### Evidence that changes the claim to Operating capability

For repeated operational use, the organisation also establishes:

- a maintained authorization policy and ownership;
- audit evidence for high-consequence exports where appropriate;
- a process for role/permission changes;
- monitoring for abnormal or repeatedly denied export attempts where material;
- an escalation path for access-policy defects;
- regression tests that remain attached to the authorization contract.

### Boundary

**Authenticated user can export** → Output.

**Allowed users can export the right resources and disallowed users are refused under tested acceptance criteria** → Deliverable.

**Authorization policy, audit/review, maintenance and incident handling are repeatable** → Operating capability.

---

## Case D — coding agent opens a pull request

### Situation

A repository gives an AI coding agent an issue:

> Add CSV export to the orders screen.

The agent modifies the frontend, adds an API route, writes tests and opens a pull request. CI is green.

### At this point: Output

A plausible implementation and green test suite exist.

That is valuable. It is not automatically enough for the decision **merge this as relied-upon functionality**.

The relevant question is not whether the agent wrote the code. A human-authored PR with the same evidence would face the same gate.

### Why green CI may still be insufficient

Suppose the tests only prove:

```ts
expect(response.status).toBe(200);
expect(response.headers['content-type']).toContain('text/csv');
```

They may not establish:

- that the exported rows match the user's permitted order scope;
- that amounts/dates are formatted to the contractual/business rule;
- that large exports remain within response/runtime limits;
- that spreadsheet-formula injection or equivalent output hazards are handled if relevant;
- that the route works with the real authentication/authorization middleware;
- what happens when the query partially fails or times out.

### Evidence that changes the claim to Deliverable

For the decision **merge for the named internal use**, the PR adds or links evidence for:

- explicit export acceptance criteria;
- representative data cases;
- permission-boundary tests;
- empty/large/special-character cases;
- relevant integration tests with the actual route/middleware;
- known limitations and fallback behaviour;
- any material security/output-encoding checks for the export context.

The actor that produced the evidence can be human, AI, deterministic tooling or hybrid. What matters is whether the evidence directly tests the intended-use criteria.

### Evidence that changes the claim to Operating capability

If the claim becomes **we can repeatedly run coding agents against this repository and safely operate the resulting delivery workflow**, the unit of evaluation changes from one PR to the whole system.

Relevant evidence now includes:

- bounded repository/tool permissions;
- branch/release authority separated from code-generation capability where required;
- repeatable CI and acceptance checks;
- logs/audit evidence for agent actions and tool calls where consequential;
- ownership for failures and dependency/security updates;
- rollback/revert process;
- escalation when the agent cannot establish a required gate;
- cost, latency and review load for the complete workflow.

### Boundary

**Agent produced a PR and CI is green** → Output evidence for the change.

**The PR meets acceptance criteria for the intended use** → Deliverable.

**The organisation can repeatedly operate the agent-enabled delivery process with controls, recovery and ownership** → Operating capability.

---

## Case E — same code, different decision, different evidence threshold

A useful way to see the stop rule is to hold the implementation constant.

Suppose a script parses logs and suggests likely incident causes.

```python
def rank_causes(events):
    # implementation omitted
    return candidates
```

The exact same script can legitimately support different claims depending on the decision.

| Decision | Minimum useful claim | Example evidence |
| --- | --- | --- |
| **Use during a two-day internal investigation as a brainstorming aid** | **Output** | Script runs on supplied logs; assumptions visible; result is not treated as authoritative. |
| **Allow on-call engineers to rely on ranked causes during incident triage** | **Deliverable** | Evaluation on representative incidents, acceptance/error criteria, known limits, fallback to existing triage. |
| **Make it a standard supported incident-analysis service** | **Operating capability** | Operational owner, monitoring, data access controls, model/tool versioning, recovery, support and repeatable evaluation. |
| **Claim it reduced incident recovery time** | **Outcome** | Baseline and after measurement using the same recovery-time definition, with material confounds named. |
| **Expand it across the organisation** | **Value** | Outcome compared with total operating/evaluation/support cost, risk and alternatives. |

Nothing about the script itself forces the project to climb the ladder.

> **The decision determines the required claim. The claim determines the evidence.**

---

## A compact transition test for code reviews

When someone says **"done"**, ask which statement they mean:

### Output

> The code/artifact/action exists and can be reproduced.

### Deliverable

> For **this named intended use**, we have explicit acceptance criteria and evidence that the result meets them, including material failure modes and known limitations.

### Operating capability

> We can perform this repeatedly because ownership, assurance, operation, observability, recovery, maintenance and support are established at the level the consequence requires.

If the evidence only supports the first statement, call it Output. That is not an insult. It may be exactly enough for the next decision.

Use the [software failure-mode catalogue](software-failure-mode-catalogue.md) to choose tests that target the actual failure mode, and the [interactive claim gate](../tools/claim-gate.html) to record the decision.
