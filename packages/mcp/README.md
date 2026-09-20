# @alreadyopen/mcp-output-to-value

Native Model Context Protocol access to the **AI Output to Value** decision framework.

This package is the practical agent interface for IDE, desktop and terminal workflows. It uses the same published `/api/v1` framework, gate, article, claim, template, and working failure-mode data as the browser implementation. WebMCP remains a progressive browser enhancement; native MCP does not depend on `document.modelContext`.

## Status

Early package source inside the main repository. It is **not yet published to npm**. No public package licence has been selected yet; `package.json` is therefore marked `UNLICENSED` until the project makes an explicit release/licensing decision.

- **Version identity:** source package version `0.1.0`, plus the repository tag/commit containing this package and the method/contract revision it consumes.
- **Intended use:** local stdio MCP access for IDE, desktop, and terminal agents that need to query the framework or evaluate a supplied claim record.
- **Support / compatibility boundary:** Node.js 20+ and stdio are the current source boundary. Host-specific MCP behaviour, future Streamable HTTP deployment, npm/package-manager distribution, and broader compatibility claims require their own tooling release evidence. For governed use, pin a reviewed tag or commit rather than `main`.

Publishing this package later would be a **tooling/distribution release**, not proof that the method or its cited evidence completed independent review. Conversely, a reviewed method release would not make every MCP host or transport supported. See [`../../docs/tooling-distribution.md`](../../docs/tooling-distribution.md).

## Transport

The first supported transport is **stdio**, suitable for local MCP hosts such as IDEs and terminal agents. A remote Streamable HTTP deployment can use the same server factory later.

## Run from this repository

```bash
cd packages/mcp
npm install
npm start
```

By default it reads the public publication API from:

`https://alreadyopen.github.io/ai-output-to-value/`

Override that for another preview/release host:

```bash
AIOV_PUBLICATION_URL=https://example.test/ npm start
```

## Tools

- `get_stop_rule(decision_type)` — minimum sufficient claim and required checks.
- `evaluate_claim_record(claim)` — deterministic evaluation of a structured claim record. It checks the supplied evidence state; it does not independently verify the underlying facts.
- `get_framework()` — current six-claim framework and actor-neutral rule.
- `get_software_outcome_template()` — DORA-based software-delivery Outcome measurement pack plus optional AI-specific leading indicators; it marks no check PASS automatically.
- `list_articles(section?)` — articles included in the currently published artifact.
- `search_claims(query, limit?)` — canonical claim records from the current publication artifact.
- `search_failure_modes(query, limit?)` — working software/architecture failure-mode catalogue.

> **Gate ≠ truth.** A green result means the supplied record satisfies the deterministic gate for the selected decision. It is not an audit of the underlying system or evidence.

## Claude Code

For a local checkout, add the stdio server to the project:

```bash
claude mcp add --scope project ai-output-to-value -- \
  node /absolute/path/to/ai-output-to-value/packages/mcp/src/index.mjs

claude mcp list
```

Claude Code's current CLI uses `--` to separate Claude's MCP options from the stdio command and arguments.

## Cursor

Create `.cursor/mcp.json` in the project (or `~/.cursor/mcp.json` for a personal global configuration):

```json
{
  "mcpServers": {
    "ai-output-to-value": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/absolute/path/to/ai-output-to-value/packages/mcp/src/index.mjs"
      ]
    }
  }
}
```

The same configuration is also available to Cursor CLI.

## VS Code / GitHub Copilot

For a repository-scoped MCP server in VS Code, create `.vscode/mcp.json`:

```json
{
  "servers": {
    "ai-output-to-value": {
      "command": "node",
      "args": [
        "/absolute/path/to/ai-output-to-value/packages/mcp/src/index.mjs"
      ]
    }
  }
}
```

Start the server from the MCP configuration UI, then use its tools from Copilot Chat in Agent mode.

## Design rule

> **The target decision determines the required gate. Producer identity does not.**

The MCP server therefore does not impose a special penalty merely because work was AI-generated and does not treat human approval as automatic proof of quality.

For governed workflows, pin the repository to a reviewed release/tag or commit rather than assuming `main` is a reviewed instrument.

Current host references:

- Claude Code MCP: https://docs.anthropic.com/en/docs/claude-code/mcp
- Cursor MCP: https://cursor.com/docs/mcp
- GitHub Copilot / VS Code MCP: https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/extend-copilot-chat-with-mcp
