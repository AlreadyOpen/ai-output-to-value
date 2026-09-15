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

Possible gate states are:

- `PASS`
- `BLOCKED`
- `INSUFFICIENT_EVIDENCE`

There is deliberately no percentage-complete score.

## 2. Use the interactive gate

Open:

`https://alreadyopen.github.io/ai-output-to-value/tools/claim-gate.html`

Choose the target decision, record the gate checks and decision context, then export Markdown, JSON, or a printable record.

## 3. Add the GitHub Action

After checking out the caller repository:

```yaml
- name: AI Output to Value decision gate
  uses: AlreadyOpen/ai-output-to-value@main
  with:
    claim: governance/claim.json
```

For pinned production use, replace `@main` with a reviewed release/tag or commit SHA.

The Action evaluates the supplied `claim.json`. It does **not** add extra requirements merely because code was AI-generated.

## 4. Add the pull-request questions

This repository's [pull request template](../.github/pull_request_template.md) is intentionally actor-neutral. Adapt the same sections in adopter repositories:

- decision sought;
- demonstrated vs inferred;
- intended use and limits;
- actors / assurance / authority / accountability;
- evidence;
- whole-job impact;
- next evidence and stop rule.

## 5. Give agents the same rules

Copy [`AGENT_RULES.md`](AGENT_RULES.md) into the repository guidance used by your coding or terminal agents. The rules explicitly allow exploration to stop at Output while preventing an agent from declaring a higher claim without the evidence required for that decision.

## 6. Machine-readable publication data

The public site generates:

- `/api/v1/framework.json`
- `/api/v1/gates.json`
- `/api/v1/articles.json`
- `/api/v1/claims.json`
- `/api/v1/sources.json`

WebMCP reads those same generated records. Native MCP and other integrations should consume the same contract rather than re-encoding the framework independently.
