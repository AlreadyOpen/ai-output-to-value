# AI Output to Value — adopter toolkit

This directory packages the decision framework into lightweight operational artefacts. The target decision determines the gate; the identity of the producer does not.

## 1. Start with a machine-readable claim

Copy [`claim.example.json`](claim.example.json) and validate it against:

- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/claim.schema.json`
- `https://alreadyopen.github.io/ai-output-to-value/schemas/v1/decision-gates.json`

Local deterministic evaluation:

```bash
python scripts/claim_gate.py path/to/claim.json --json
```

Possible gate states are `PASS`, `BLOCKED`, and `INSUFFICIENT_EVIDENCE`. There is deliberately no percentage-complete score.

> **Gate ≠ truth.** `PASS` means the supplied record satisfies the deterministic gate for the selected decision. It is not an audit of the underlying system, measurement, people, or evidence references.

## 2. Learn from filled samples before starting blank

The [`samples/`](samples/) folder contains three fictional teaching cases represented by four records:

- website prototype — **Explore → PASS**;
- the same website — **Operate → BLOCKED**;
- internal incident-summary tool — **Rely → PASS**;
- killed idea — **Outcome → PASS** on decision-changing learning.

The website pair deliberately keeps the artefact conceptually the same while changing the requested decision. This demonstrates why the decision selects the gate.

The live Claim Gate can load these samples directly.

## 3. Use the interactive gate

Open:

`https://alreadyopen.github.io/ai-output-to-value/tools/claim-gate.html`

Human, AI and hybrid workflows operate on the same `claim.json` contract:

- **human** — complete/edit the visible form;
- **AI** — evaluate the record through WebMCP or native MCP;
- **hybrid** — import/export `claim.json`, or let a compatible browser agent populate the local form for inspection/editing.

The tool can copy Markdown/JSON, download JSON, and print a compact decision record. Its HTML also contains a readable static fallback, schema links, decision thresholds and teaching records for no-JavaScript clients and crawlers.

## 4. Use the software Outcome pack when the decision is 05 Outcome

[`templates/software-outcome-pack.json`](templates/software-outcome-pack.json) supplies a measurement plan for software-delivery initiatives using DORA's five current metric names:

- change lead time;
- deployment frequency;
- failed deployment recovery time;
- change fail rate;
- deployment rework rate.

For AI-assisted delivery, the template also suggests leading indicators such as AI-touched share, review wait on AI-touched changes, and revert/rollback rate on those changes.

The template marks **no gate check PASS automatically**. It helps define what to measure; it does not prove the outcome or causal attribution.

## 5. Count full relevant cost for 06 Value

Use [`value-cost-ledger.md`](value-cost-ledger.md) when the decision is scale, renew, expand, or stop.

The ledger keeps local task savings separate from total value by making the decision-relevant boundary explicit: model/API cost, licences, compute, review/correction, integration, testing/assurance, deployment, monitoring, support, rework/recovery, training/change management, procurement overhead, opportunity cost, and other material trade-offs.

Do not force unlike quantities into one total unless the conversion is explicit and defensible.

## 6. Keep real evidence private with the workbook

Use [`private-workbook/`](private-workbook/) inside the adopting organisation. It contains:

```text
private-workbook/
├── README.md
├── decision.md
├── claim.json
└── evidence/
    └── README.md
```

The built site also publishes a downloadable ZIP at:

`/downloads/ai-output-to-value-private-workbook.zip`

The public project does not need access to the organisation's confidential evidence. Keep client names, contracts, production metrics, personal data, proprietary workflows, credentials and other restricted material inside the appropriate controlled systems.

## 7. Add the GitHub Action

After checking out the caller repository:

```yaml
- name: AI Output to Value decision gate
  uses: AlreadyOpen/ai-output-to-value@main
  with:
    claim: governance/claim.json
```

For governed use, replace `@main` with a reviewed release/tag or commit SHA.

The Action evaluates the supplied `claim.json`. It does **not** add extra requirements merely because code was AI-generated.

By default the step fails when the gate does not return `PASS`. Set `fail-on-block: 'false'` to read the result and let the calling workflow decide — **only the exact value `false` disables failure**, so a typo such as `yes` or an empty value keeps the protective behaviour. A missing or malformed claim record always fails the step, because there is no result to report.

The Action exposes the gate result as step outputs, so a caller can branch on the verdict instead of parsing stdout:

```yaml
- name: AI Output to Value decision gate
  id: gate
  uses: AlreadyOpen/ai-output-to-value@main
  with:
    claim: governance/claim.json
    fail-on-block: 'false'

- name: Require Operating capability before release
  if: steps.gate.outputs.status != 'PASS'
  run: |
    echo "Gate returned ${{ steps.gate.outputs.status }} for ${{ steps.gate.outputs.decision-label }}"
    echo "Required claim: ${{ steps.gate.outputs.required-claim-level }}"
    echo "${{ steps.gate.outputs.failed-check-count }} failed, ${{ steps.gate.outputs.unknown-check-count }} unknown"
    exit 1
```

| Output | Meaning |
| --- | --- |
| `status` | `PASS`, `BLOCKED` or `INSUFFICIENT_EVIDENCE` |
| `target-decision` | Identifier of the decision evaluated |
| `decision-label` | Human-facing label for that decision |
| `required-claim-level` | Weakest claim level sufficient for the decision |
| `asserted-claim-level` | Claim level asserted by the record |
| `claim-mismatch` | `true` when the asserted level does not match the required one |
| `failed-check-count` / `unknown-check-count` / `passed-check-count` | Check tallies |
| `result-json` | The complete result as compact JSON |

The step also writes a short verdict to the job summary.

**Gate ≠ truth.** A `PASS` output reports that the *supplied record* satisfies the deterministic checks for the selected decision. It is not an audit of the underlying system, measurement, people, or evidence references.

## 8. Add the pull-request questions

This repository's [pull request template](../.github/pull_request_template.md) is intentionally actor-neutral. Adapt the same sections in adopter repositories:

- decision sought;
- demonstrated vs inferred;
- intended use and limits;
- workflow boundary and moved bottleneck;
- actors / assurance / authority / accountability;
- evidence and measurement;
- next evidence and stop rule.

## 9. Give agents the same rules

Copy [`AGENT_RULES.md`](AGENT_RULES.md) into the repository guidance used by coding or terminal agents. The rules explicitly allow exploration to stop at Output while preventing an agent from declaring a higher claim without the evidence required for that decision.

For native MCP setup, see [`../packages/mcp/README.md`](../packages/mcp/README.md).

## 10. Use instruments to inspect claims, not to mint Value

[`operating-kit.md`](operating-kit.md) lists vendor-neutral instrument classes for evaluation/trace, contract/e2e testing, operational evidence, software-delivery telemetry, and cost/value evidence.

MCP servers and skills are context pipes. They can materially improve Access, Output and evidence retrieval; they do not create Value merely by being connected.

## 11. Place the method inside the relevant governance system

See [`../docs/framework-crosswalk.md`](../docs/framework-crosswalk.md) for a short orientation to NIST AI RMF, ISO/IEC 42001, EU AI Act Article 14, and Australia's current Guidance for AI Adoption.

AI Output to Value is a decision/evidence method, not a substitute for law, certification, regulator guidance, contract obligations, or sector controls.

## 12. Machine-readable publication data

The public site generates:

- `/api/v1/framework.json`
- `/api/v1/gates.json`
- `/api/v1/articles.json`
- `/api/v1/claims.json`
- `/api/v1/sources.json`
- `/api/v1/failure-modes.json` in the working preview;
- `/templates/software-outcome-pack.json`;
- `/samples/*.claim.json`.

WebMCP, native MCP and the interactive UI should consume the same published contract rather than re-encoding the framework independently.
