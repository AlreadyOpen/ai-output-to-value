#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Give every built page the one site navigation defined in site_nav.py."""
from __future__ import annotations

from pathlib import Path

import site_nav

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def main() -> None:
    if not SITE.exists():
        raise SystemExit("site/ does not exist; build the publication first")
    changed = 0
    pages = [path for path in sorted(SITE.rglob("*.html")) if "md" not in path.relative_to(SITE).parts]
    for path in pages:
        depth = len(path.relative_to(SITE).parts) - 1
        text = path.read_text(encoding="utf-8")
        try:
            updated = site_nav.apply_navigation(text, site_nav.prefix_for(depth))
        except ValueError as error:
            raise SystemExit(f"{path.relative_to(ROOT)}: {error}") from error
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Applied the site navigation to {len(pages)} page(s) ({changed} changed)")


if __name__ == "__main__":
    main()
