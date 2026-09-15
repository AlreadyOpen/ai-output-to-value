#!/usr/bin/env python3
"""Validate local links inside the generated site artifact only.

This check is intentionally independent of editorial release approval. It can be
run against both preview and release-mode builds to answer one question:
Does the generated artifact contain broken local links or fragment targets?
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get("PUBLICATION_ROOT", str(DEFAULT_ROOT))).resolve()
SITE = ROOT / "site"
HTML_HREF_RE = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)
HTML_ID_RE = re.compile(r"\bid=[\"']([^\"']+)[\"']", re.IGNORECASE)
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}


def html_ids(path: Path) -> set[str]:
    try:
        return set(HTML_ID_RE.findall(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeDecodeError):
        return set()


def main() -> int:
    errors: list[str] = []
    if not SITE.exists():
        print("ERROR: generated site directory is missing", file=sys.stderr)
        return 1

    pages = sorted(SITE.rglob("*.html"))
    if not pages:
        print("ERROR: generated site contains no HTML pages", file=sys.stderr)
        return 1

    site_root = SITE.resolve()
    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{page.relative_to(ROOT)}: not valid UTF-8")
            continue

        for raw in HTML_HREF_RE.findall(text):
            parsed = urlsplit(raw.strip())
            if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
                continue

            if not parsed.path:
                if parsed.fragment and parsed.fragment not in html_ids(page):
                    errors.append(f"{page.relative_to(ROOT)}: missing fragment target: {raw}")
                continue

            if parsed.path.startswith("/"):
                target = (SITE / unquote(parsed.path).lstrip("/")).resolve()
            else:
                target = (page.parent / unquote(parsed.path)).resolve()

            try:
                target.relative_to(site_root)
            except ValueError:
                errors.append(f"{page.relative_to(ROOT)}: link escapes generated site: {raw}")
                continue

            if not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: broken generated-site link: {raw}")
                continue

            if parsed.fragment and target.suffix.lower() == ".html" and parsed.fragment not in html_ids(target):
                errors.append(f"{page.relative_to(ROOT)}: missing fragment target: {raw}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Generated-site link check failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Generated-site link check passed for {len(pages)} HTML page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
