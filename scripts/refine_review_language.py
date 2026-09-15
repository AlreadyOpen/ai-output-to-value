#!/usr/bin/env python3
"""Clarify visible review wording without changing canonical review state."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def refine(text: str) -> str:
    text = re.sub(
        r"Evidence review: (\d+) connected claim\(s\) await independent review",
        r"Evidence state: initial source checks recorded; independent review not yet completed for \1 connected claim(s)",
        text,
    )
    text = text.replace(
        "registered claim pending independent review",
        "registered claim · initial source check recorded · independent review not yet completed",
    )
    text = text.replace(
        "registered claims pending independent review",
        "registered claims · initial source checks recorded · independent review not yet completed",
    )
    # The canonical data still uses independent_review_status: pending. The
    # rendered evidence register separates that from the already-recorded
    # initial source check so readers do not interpret `pending` as `unchecked`.
    text = text.replace(
        '<span class="status-label">independent review: pending</span>',
        '<span class="status-label">initial source check: recorded</span> <span class="status-label">independent review: not completed</span>',
    )
    return text


def main() -> None:
    count = 0
    for path in SITE.rglob("*.html"):
        before = path.read_text(encoding="utf-8")
        after = refine(before)
        if after != before:
            path.write_text(after, encoding="utf-8")
            count += 1
    print(f"Clarified independent-review wording on {count} generated HTML page(s)")


if __name__ == "__main__":
    main()
