# Mild operating kit — instruments that can inspect a claim

This is intentionally **not** a preferred-vendor stack. Tools, MCP servers, agents, dashboards, and repositories can increase Access and Output. They do not automatically establish Deliverable, Capability, Outcome, or Value.

Choose instruments according to the failure mode and the decision being made.

| Claim boundary | Evidence job | Typical instrument class | Examples |
| --- | --- | --- | --- |
| **Access → Output** | Confirm the tool can actually produce or perform the bounded task | usage inventory, reproducible fixture, tool/API log | organisation usage inventory; API/tool logs; a saved reproducible prompt/fixture |
| **Output → Deliverable** | Test the named acceptance criteria and important failure modes | eval/trace system, deterministic fixture, contract test, end-to-end test | Promptfoo, Langfuse, Braintrust, or in-house fixtures; API contract tests; browser/e2e tests; the enquiry actually arriving at the intended business process |
| **Deliverable → Capability** | Show the organisation can repeatedly operate, detect, recover, support, and change the workflow | CI/CD controls, observability, runbooks, rollback/recovery tests, ownership records | existing CI/CD platform; service telemetry; incident/runbook system; recovery rehearsal |
| **Capability → Outcome** | Measure whether the end-to-end result changed against a baseline | product/operations measurement, DORA-capable delivery telemetry, experimental or quasi-experimental comparison | application/service delivery telemetry; baseline/after measurement; DORA software-delivery metrics for software work |
| **Outcome → Value** | Account for relevant cost, risk, alternatives and trade-offs | finance/cost records, incident cost, support effort, customer/business measure, decision log | internal cost data; cloud/model/tool spend; support and rework effort; business outcome and decision records |

## MCP and agent skills are context pipes

Repository, documentation, ticket, log, browser and data MCP/skill integrations can give an agent better context and make the workflow more inspectable. That can materially improve **Access**, **Output**, and the evidence-gathering process.

They do not mint Value simply because the agent can reach more systems.

Ask instead:

- Which claim does this integration help inspect?
- Which evidence becomes easier to retrieve or reproduce?
- Which permissions or authority does it expose?
- Which new failure mode does the integration introduce?
- What remains outside the tool's view?

## Software Outcome default

For a software-delivery initiative, the project provides a [software Outcome pack](templates/software-outcome-pack.json) based on DORA's five current delivery metrics:

- change lead time;
- deployment frequency;
- failed deployment recovery time;
- change fail rate;
- deployment rework rate.

When AI-assisted delivery is the intervention, also consider leading indicators such as the share of AI-touched changes, review wait time for those changes, and revert/rollback rate for those changes.

These are measurement suggestions, not automatic evidence that AI caused the result or that the result created business Value.

## Keep the operating kit proportionate

An exploration does not need production observability merely because production observability is useful elsewhere. Use the **lowest claim sufficient for the next decision**, and add an instrument only when the evidence it provides can change that decision.
