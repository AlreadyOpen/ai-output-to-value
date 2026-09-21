#!/usr/bin/env python3
"""Validate links and visible interaction integrity in the generated site artifact.

This check is intentionally independent of editorial release approval. It can be
run against both preview and release-mode builds to answer two questions:
1. Does the generated artifact contain broken local links or fragment targets?
2. Does it expose an affordance that looks usable but still depends on a missing
   placeholder/legacy interaction?
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import site_nav

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get("PUBLICATION_ROOT", str(DEFAULT_ROOT))).resolve()
SITE = ROOT / "site"
HTML_HREF_RE = re.compile(r"\bhref=[\"']([^\"']*)[\"']", re.IGNORECASE)
HTML_SRC_RE = re.compile(r"\bsrc=[\"']([^\"']*)[\"']", re.IGNORECASE)
HTML_ID_RE = re.compile(r"\bid=[\"']([^\"']+)[\"']", re.IGNORECASE)
PROVIDER_PLACEHOLDER_RE = re.compile(
    r'<a\b[^>]*href=["\']#["\'][^>]*data-open-provider=', re.IGNORECASE
)
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}
FORBIDDEN_FINAL_ASSETS = (
    Path("article-tools.js"),
    Path("tools/claim-gate.js"),
)


def html_ids(path: Path) -> set[str]:
    try:
        return set(HTML_ID_RE.findall(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeDecodeError):
        return set()


def check_local_target(page: Path, raw: str, *, kind: str, site_root: Path, errors: list[str]) -> None:
    value = raw.strip()
    if not value:
        errors.append(f"{page.relative_to(ROOT)}: empty {kind} target")
        return
    if kind == "href" and value == "#":
        errors.append(f"{page.relative_to(ROOT)}: dead placeholder link: href=\"#\"")
        return

    parsed = urlsplit(value)
    if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
        return

    if not parsed.path:
        if kind == "href" and parsed.fragment and parsed.fragment not in html_ids(page):
            errors.append(f"{page.relative_to(ROOT)}: missing fragment target: {raw}")
        return

    if parsed.path.startswith("/"):
        target = (SITE / unquote(parsed.path).lstrip("/")).resolve()
    else:
        target = (page.parent / unquote(parsed.path)).resolve()

    try:
        target.relative_to(site_root)
    except ValueError:
        errors.append(f"{page.relative_to(ROOT)}: {kind} escapes generated site: {raw}")
        return

    if not target.exists():
        errors.append(f"{page.relative_to(ROOT)}: broken generated-site {kind}: {raw}")
        return

    if kind == "href" and parsed.fragment and target.suffix.lower() == ".html" and parsed.fragment not in html_ids(target):
        errors.append(f"{page.relative_to(ROOT)}: missing fragment target: {raw}")


def check_navigation(page: Path, text: str, *, site_root: Path, errors: list[str]) -> None:
    """Every page carries the one site navigation (site_nav.py), so the navs cannot drift."""
    prefix = site_nav.prefix_for(len(page.relative_to(site_root).parts) - 1)
    for name, expected in (("primary", site_nav.primary(prefix)), ("mobile", site_nav.mobile(prefix))):
        if expected not in text:
            errors.append(f"{page.relative_to(ROOT)}: {name} navigation differs from the site navigation")


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

        check_navigation(page, text, site_root=site_root, errors=errors)

        if PROVIDER_PLACEHOLDER_RE.search(text):
            errors.append(f"{page.relative_to(ROOT)}: open-in provider still uses href=\"#\"")

        # The static article toolbar is the no-JS contract. Clipboard buttons are
        # added only by React; if these attrs survive in final HTML they look
        # functional but do nothing when JavaScript is unavailable.
        if "data-article-tools" in text:
            if "data-copy-md " in text or "data-copy-md>" in text:
                errors.append(f"{page.relative_to(ROOT)}: static article toolbar still exposes JS-only Copy MD control")
            if "data-copy-md-link" in text:
                errors.append(f"{page.relative_to(ROOT)}: static article toolbar still exposes JS-only Copy MD link control")

        for raw in HTML_HREF_RE.findall(text):
            check_local_target(page, raw, kind="href", site_root=site_root, errors=errors)
        for raw in HTML_SRC_RE.findall(text):
            check_local_target(page, raw, kind="src", site_root=site_root, errors=errors)

    for relative in FORBIDDEN_FINAL_ASSETS:
        path = SITE / relative
        if path.exists():
            errors.append(f"{path.relative_to(ROOT)}: obsolete UI implementation shipped in final artifact")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Generated-site interaction/link check failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Generated-site interaction/link check passed for {len(pages)} HTML page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
