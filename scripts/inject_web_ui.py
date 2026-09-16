#!/usr/bin/env python3
"""Attach the React/Tailwind/shadcn enhancement bundle to generated HTML."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def relative_prefix(path: Path) -> str:
    rel = path.relative_to(SITE)
    depth = len(rel.parts) - 1
    return "../" * depth


def inject(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    prefix = relative_prefix(path)
    css = f'{prefix}ui/aiov-ui.css'
    js = f'{prefix}ui/aiov-ui.js'

    if css not in text:
        text = text.replace("</head>", f'<link rel="stylesheet" href="{css}">\n</head>', 1)

    # The React/Base UI toolbar replaces the old progressively-enhanced toolbar.
    # Remove the obsolete script reference rather than loading two competing UI
    # implementations for the same visible controls.
    text = text.replace('<script src="../article-tools.js" defer></script>\n', "")
    text = text.replace('<script src="article-tools.js" defer></script>\n', "")

    if js not in text:
        text = text.replace("</body>", f'<script type="module" src="{js}"></script>\n</body>', 1)

    if path.name == "meeting-brief.html" and "ai-output-to-value-meeting-brief.pdf" not in text:
        marker = '<aside class="article-aside" aria-label="Article links">'
        text = text.replace(
            marker,
            marker + '<a href="../downloads/ai-output-to-value-meeting-brief.pdf"><strong>Download meeting brief PDF</strong></a>',
            1,
        )

    path.write_text(text, encoding="utf-8")


def remove_obsolete_assets() -> None:
    # build_site/augment_site still copy these compatibility files before the
    # React build runs. They are not part of the final publication contract and
    # must not be shipped as apparently supported alternative implementations.
    for path in (SITE / "article-tools.js", SITE / "tools" / "claim-gate.js"):
        if path.exists():
            path.unlink()


def main() -> None:
    if not SITE.exists():
        raise SystemExit("site/ does not exist; build the publication first")
    count = 0
    for path in SITE.rglob("*.html"):
        inject(path)
        count += 1
    remove_obsolete_assets()
    print(f"Injected React/Tailwind/shadcn UI bundle into {count} HTML files and removed obsolete UI assets")


if __name__ == "__main__":
    main()
