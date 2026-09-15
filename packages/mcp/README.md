# @alreadyopen/mcp-output-to-value

Native Model Context Protocol access to the **AI Output to Value** decision framework.

This package complements the website's WebMCP surface for IDE, desktop and terminal-agent workflows. It uses the same published `/api/v1` framework, gate, article and claim data as the browser implementation.

## Status

Early package source inside the main repository. It is **not yet published to npm**.

## Transport

The first supported transport is **stdio**, suitable for local MCP hosts such as IDEs and terminal agents. A remote Streamable HTTP deployment can use the same server factory later.

The implementation targets the stable v2 MCP TypeScript server package.

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
- `list_articles(section?)` — articles included in the currently published artifact.
- `search_claims(query, limit?)` — canonical claim records from the current publication artifact.

## Design rule

> **The target decision determines the required gate. Producer identity does not.**

The MCP server therefore does not impose a special penalty merely because work was AI-generated and does not treat human approval as automatic proof of quality.

## Example host configuration

After the package is published or installed locally, configure a stdio MCP host to launch:

```text
node /absolute/path/to/ai-output-to-value/packages/mcp/src/index.mjs
```

Exact configuration syntax varies by host. Pin a reviewed release or commit when using the server in governed workflows.
