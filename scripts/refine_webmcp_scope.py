#!/usr/bin/env python3
"""Keep generated WebMCP links inside the current publication artifact.

The source WebMCP implementation is shared by preview and release builds. The
failure-mode catalogue is working material, so release builds intentionally omit
its article. Refine the generated asset after failure-modes.json is published so
machine clients never receive a URL to a page excluded from that artifact.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

OLD = '''            count: matches.length,
            matches,
            catalogue: siteUrl("articles/software-failure-mode-catalogue.html")
'''
NEW = '''            count: matches.length,
            matches,
            catalogueIncluded: payload.catalogueIncluded === true,
            catalogue: payload.catalogueUrl ? siteUrl(payload.catalogueUrl) : null
'''


def main() -> None:
    path = SITE / "webmcp.js"
    if not path.exists():
        raise SystemExit("site/webmcp.js is missing; build the publication first")
    text = path.read_text(encoding="utf-8")
    if OLD not in text:
        raise SystemExit("WebMCP failure-mode response shape changed; update refine_webmcp_scope.py instead of silently skipping scope refinement")
    path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("Refined generated WebMCP failure-mode links for publication scope")


if __name__ == "__main__":
    main()
