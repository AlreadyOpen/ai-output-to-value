#!/usr/bin/env python3
"""Refine agent-access presentation after the static homepage has been built."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
MCP_URL = "https://github.com/AlreadyOpen/ai-output-to-value/tree/main/packages/mcp"


def main() -> None:
    homepage = SITE / "index.html"
    if not homepage.exists():
        return

    text = homepage.read_text(encoding="utf-8")

    # WebMCP is useful progressive enhancement, but browser support is not yet a
    # headline publication status like Working preview.
    text = text.replace(
        '<a class="status-label" href="#interfaces" title="This site exposes read-only WebMCP tools for compatible AI agents">WebMCP enabled</a>',
        "",
    )

    # The streamlined executive landing page no longer carries a long
    # #interfaces section. If the older builder injected that anchor, point it
    # at the practical native-MCP setup rather than leaving a dead fragment.
    text = text.replace(
        '<a href="#interfaces">AI access</a>',
        f'<a href="{MCP_URL}">AI access</a>',
    )

    text = text.replace(
        '<h3>WebMCP structured tools</h3>\n            <p>WebMCP lets a page expose structured application actions through <code>document.modelContext</code> so compatible agents can discover and invoke them instead of guessing every action from the visual UI.</p>',
        '<h3>Native MCP for IDE and terminal agents</h3>\n            <p>The local <code>@alreadyopen/mcp-output-to-value</code> server exposes the same gate, evidence search, failure-mode search, and software Outcome template over stdio for MCP-capable IDE and terminal workflows.</p>',
    )

    text = text.replace(
        '<strong>WebMCP changes the channel, not the claim.</strong>\n          <p>Structured agent access is useful Access/Output capability. It does not by itself establish Deliverable, organisational Capability, Outcome or Value.</p>\n          <p><a href="https://webmcp.devpost.com/resources">WebMCP resources</a> · <a href="articles/claim-card.html#same-standard-does-not-mean-the-same-interface">Apply the same-standard test in the claim card</a></p>',
        '<strong>Structured agent access changes the channel, not the claim.</strong>\n          <p><strong>Native MCP</strong> is the practical IDE/terminal path. <strong>WebMCP</strong> remains progressive enhancement when a browser exposes <code>document.modelContext</code>. Neither channel by itself establishes Deliverable, Operating capability, Outcome or Value.</p>\n          <p><a href="https://github.com/AlreadyOpen/ai-output-to-value/tree/main/packages/mcp">Native MCP setup</a> · <a href="https://webmcp.devpost.com/resources">WebMCP resources</a> · <a href="articles/claim-card.html#same-standard-does-not-mean-the-same-interface">Apply the same-standard test</a></p>',
    )

    text = text.replace(
        '<p><strong>This site is WebMCP-enabled.</strong> Compatible agents can use six read-only tools to read the framework, list and read articles, search evidence, inspect claims, and retrieve the meeting guide. Browser/runtime support is reported below.</p>',
        '<p><strong>Agent access is available through native MCP.</strong> Browser WebMCP is also exposed as progressive enhancement when the current browser provides <code>document.modelContext</code>; runtime support is reported below.</p>',
    )
    text = text.replace(
        '<p><strong>This site is WebMCP-enabled.</strong> Compatible agents can use seven read-only tools to read the framework, list and read articles, search evidence, inspect claims, search the software failure-mode catalogue, and retrieve the meeting guide. Browser/runtime support is reported below.</p>',
        '<p><strong>Agent access is available through native MCP.</strong> Browser WebMCP is also exposed as progressive enhancement when the current browser provides <code>document.modelContext</code>; runtime support is reported below.</p>',
    )

    homepage.write_text(text, encoding="utf-8")
    print("Refined homepage agent access: native MCP primary, WebMCP progressive enhancement")


if __name__ == "__main__":
    main()
