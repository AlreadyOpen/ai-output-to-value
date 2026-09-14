#!/usr/bin/env python3
"""Release-approval checks, deliberately separate from preview structure checks."""
from __future__ import annotations

import sys
from pathlib import Path

from publication_data import load_claim_records, load_yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []

    for _, claim in load_claim_records(ROOT):
        if not isinstance(claim, dict) or not claim.get("launch_critical"):
            continue
        if claim.get("independent_review_status") != "completed":
            errors.append(f"launch-critical claim has not completed independent review: {claim.get('id', '<missing id>')}")
        if not str(claim.get("reviewer", "")).strip() or not str(claim.get("reviewed", "")).strip():
            errors.append(f"launch-critical claim lacks an inspectable review record: {claim.get('id', '<missing id>')}")

    manifest = load_yaml(ROOT / "data" / "articles.yml")
    for article in manifest.get("articles", []):
        if article.get("section") == "core" and article.get("status") != "ready":
            errors.append(
                f"core article is not marked ready for publication: {article.get('id')} "
                f"(status={article.get('status')})"
            )

    if errors:
        for error in errors:
            print(f"RELEASE BLOCKER: {error}", file=sys.stderr)
        print(
            f"Release approval failed with {len(errors)} blocker(s). "
            "The preview build may still be structurally valid.",
            file=sys.stderr,
        )
        return 1

    print("Release approval checks passed. This records project approval criteria; it is not a guarantee of factual truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
