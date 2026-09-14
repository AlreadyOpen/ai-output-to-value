#!/usr/bin/env python3
"""Structural preview-publication gate.

This validates structure, traceability and deployment-local links. It does not
establish factual truth and is deliberately separate from release approval.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from publication_data import load_claim_records, load_source_records, load_yaml

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get("PUBLICATION_ROOT", str(DEFAULT_ROOT))).resolve()
DATA_DIR, SITE_DIR = ROOT / "data", ROOT / "site"
SOURCE_REQUIRED = {"id", "title", "publisher", "url", "evidence_type", "supports", "scope", "limitations", "reviewed"}
CLAIM_REQUIRED = {"id", "claim_text", "status", "evidence", "published_in", "reviewer", "reviewed", "human_review_status"}
EVIDENCE_REQUIRED = {"source_id", "locator", "relevant_finding", "qualification"}
ARTICLE_REQUIRED = {"id", "title", "source", "slug", "section", "order", "summary", "maintainer", "reviewed", "status"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)
HTML_ID_RE = re.compile(r"\bid=[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
RESERVED_ARTICLE_SLUGS = {"index"}


class CheckResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
    def error(self, message: str) -> None: self.errors.append(message)
    def warn(self, message: str) -> None: self.warnings.append(message)


def text_ok(value) -> bool:
    return value is not None and bool(str(value).strip())


def slugify_heading(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def check_sources(result: CheckResult) -> set[str]:
    ids: set[str] = set()
    try:
        records = load_source_records(ROOT)
    except Exception as exc:
        result.error(f"canonical source registry could not be loaded: {exc}")
        return ids
    for path, source in records:
        label = f"{path.relative_to(ROOT)}: source"
        if not isinstance(source, dict):
            result.error(f"{label} must be a mapping"); continue
        missing = sorted(SOURCE_REQUIRED - source.keys())
        if missing: result.error(f"{label} missing fields: {', '.join(missing)}")
        for field in SOURCE_REQUIRED - {"supports"}:
            if field in source and not text_ok(source.get(field)):
                result.error(f"{label} field '{field}' must be non-empty")
        sid = source.get("id")
        if not text_ok(sid): continue
        sid = str(sid)
        if sid in ids: result.error(f"duplicate source id: {sid}")
        ids.add(sid)
        supports = source.get("supports")
        if not isinstance(supports, list) or not supports or not all(text_ok(x) for x in supports):
            result.error(f"{label} field 'supports' must be a non-empty list of non-empty strings")
    if not ids: result.error("no source records found in canonical data/*.yml registries")
    return ids


def locator_exists(target: Path, locator: str) -> bool:
    try: text = target.read_text(encoding="utf-8")
    except Exception: return False
    return locator.strip() in text


def check_claims(source_ids: set[str], result: CheckResult) -> None:
    try:
        records = load_claim_records(ROOT)
    except Exception as exc:
        result.error(f"canonical claim registry could not be loaded: {exc}"); return
    if not records: result.error("no claim records found in data/*.yml")
    ids: set[str] = set()
    for path, claim in records:
        label = f"{path.relative_to(ROOT)}: claim"
        if not isinstance(claim, dict): result.error(f"{label} must be a mapping"); continue
        missing = sorted(CLAIM_REQUIRED - claim.keys())
        if missing: result.error(f"{label} missing fields: {', '.join(missing)}")
        for field in CLAIM_REQUIRED - {"evidence", "published_in"}:
            if field in claim and not text_ok(claim.get(field)):
                result.error(f"{label} field '{field}' must be non-empty")
        cid = str(claim.get("id", "")).strip()
        if not cid: continue
        if cid in ids: result.error(f"duplicate claim id: {cid}")
        ids.add(cid)
        evidence = claim.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            result.error(f"{cid}: evidence must be a non-empty list")
        else:
            for i, item in enumerate(evidence, 1):
                elabel = f"{cid}: evidence #{i}"
                if not isinstance(item, dict): result.error(f"{elabel} must be a mapping"); continue
                missing_e = sorted(EVIDENCE_REQUIRED - item.keys())
                if missing_e: result.error(f"{elabel} missing fields: {', '.join(missing_e)}")
                for field in EVIDENCE_REQUIRED:
                    if field in item and not text_ok(item.get(field)):
                        result.error(f"{elabel} field '{field}' must be non-empty")
                if item.get("source_id") not in source_ids:
                    result.error(f"{elabel} references unknown source_id: {item.get('source_id')}")
        pubs = claim.get("published_in")
        if not isinstance(pubs, list) or not pubs:
            result.error(f"{cid}: published_in must be a non-empty list")
        else:
            for i, pub in enumerate(pubs, 1):
                plabel = f"{cid}: published_in #{i}"
                if not isinstance(pub, dict): result.error(f"{plabel} must be a mapping"); continue
                target, locator = pub.get("file"), pub.get("locator")
                if not text_ok(target): result.error(f"{plabel} requires a file"); continue
                if not text_ok(locator): result.error(f"{plabel} requires a locator"); continue
                target_path = ROOT / str(target)
                if not target_path.exists(): result.error(f"{plabel} points to missing file: {target}")
                elif not locator_exists(target_path, str(locator)):
                    result.error(f"{plabel} locator was not found in {target}: {locator}")
        review = claim.get("human_review_status")
        if review == "completed":
            if not text_ok(claim.get("reviewer")) or not text_ok(claim.get("reviewed")):
                result.error(f"{cid}: completed human review requires reviewer and reviewed date")
        else:
            result.warn(f"{cid}: human review is {review or 'unspecified'}")


def check_articles(result: CheckResult) -> None:
    path = DATA_DIR / "articles.yml"
    try: data = load_yaml(path)
    except Exception as exc: result.error(f"data/articles.yml invalid: {exc}"); return
    articles = data.get("articles") if isinstance(data, dict) else None
    if not isinstance(articles, list): result.error("data/articles.yml: top-level 'articles' must be a list"); return
    ids, slugs = set(), set()
    for i, article in enumerate(articles, 1):
        label = f"data/articles.yml: article #{i}"
        if not isinstance(article, dict): result.error(f"{label} must be a mapping"); continue
        missing = sorted(ARTICLE_REQUIRED - article.keys())
        if missing: result.error(f"{label} missing fields: {', '.join(missing)}")
        for field in ARTICLE_REQUIRED - {"order"}:
            if field in article and not text_ok(article.get(field)):
                result.error(f"{label} field '{field}' must be non-empty")
        aid, slug, source = str(article.get("id", "")).strip(), str(article.get("slug", "")).strip(), str(article.get("source", "")).strip()
        if aid in ids: result.error(f"duplicate article id: {aid}")
        elif aid: ids.add(aid)
        if slug in slugs: result.error(f"duplicate article slug: {slug}")
        elif slug: slugs.add(slug)
        if slug in RESERVED_ARTICLE_SLUGS: result.error(f"reserved article slug: {slug}")
        if slug and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug): result.error(f"invalid article slug: {slug}")
        if source and not (ROOT / source).exists(): result.error(f"{label} source does not exist: {source}")


def iter_text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html"} and not any(p in SKIP_DIRS for p in path.parts):
            yield path


def extract_links(path: Path, text: str) -> list[str]:
    return MARKDOWN_LINK_RE.findall(text) if path.suffix.lower() == ".md" else HTML_HREF_RE.findall(text)


def fragment_exists(target: Path, fragment: str) -> bool:
    fragment = unquote(fragment)
    try: text = target.read_text(encoding="utf-8")
    except Exception: return False
    if target.suffix.lower() == ".html": return fragment in set(HTML_ID_RE.findall(text))
    if target.suffix.lower() == ".md": return fragment in {slugify_heading(h) for h in HEADING_RE.findall(text)}
    return True


def built_candidate(source_path: Path, raw_link: str) -> Path | None:
    try: rel = source_path.resolve().relative_to(ROOT)
    except ValueError: return None
    if rel.parts and rel.parts[0] == "site": return None
    parsed = urlsplit(raw_link)
    if parsed.scheme or parsed.netloc or not parsed.path: return None
    candidate = (SITE_DIR / rel).parent / unquote(parsed.path)
    try: candidate.resolve().relative_to(SITE_DIR.resolve())
    except ValueError: return None
    return candidate.resolve() if candidate.exists() else None


def check_internal_links(result: CheckResult) -> None:
    for path in iter_text_files():
        try: text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError: result.error(f"{path.relative_to(ROOT)}: not valid UTF-8"); continue
        in_site = False
        try: path.resolve().relative_to(SITE_DIR.resolve()); in_site = True
        except ValueError: pass
        for raw in extract_links(path, text):
            parsed = urlsplit(raw.strip())
            if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc: continue
            if not parsed.path:
                if parsed.fragment and path.suffix.lower() == ".html" and not fragment_exists(path, parsed.fragment):
                    result.error(f"{path.relative_to(ROOT)}: missing fragment target: {raw}")
                continue
            target = ((ROOT / unquote(parsed.path).lstrip("/")) if parsed.path.startswith("/") else (path.parent / unquote(parsed.path))).resolve()
            if in_site:
                try: target.relative_to(SITE_DIR.resolve())
                except ValueError:
                    result.error(f"{path.relative_to(ROOT)}: built link escapes deployment root: {raw}"); continue
            else:
                try: target.relative_to(ROOT)
                except ValueError:
                    result.error(f"{path.relative_to(ROOT)}: local link escapes repository: {raw}"); continue
            actual = target if target.exists() else built_candidate(path, raw)
            if actual is None:
                result.error(f"{path.relative_to(ROOT)}: broken internal link: {raw}"); continue
            if parsed.fragment and not fragment_exists(actual, parsed.fragment):
                result.error(f"{path.relative_to(ROOT)}: missing fragment target: {raw}")


def check_built_site(result: CheckResult) -> None:
    for path in [SITE_DIR / "index.html", SITE_DIR / "articles" / "index.html", SITE_DIR / "evidence" / "index.html"]:
        if not path.exists(): result.error(f"built publication file is missing: {path.relative_to(ROOT)}")


def main() -> int:
    result = CheckResult()
    source_ids = check_sources(result)
    check_claims(source_ids, result); check_articles(result); check_built_site(result); check_internal_links(result)
    for warning in result.warnings: print(f"WARNING: {warning}")
    if result.errors:
        for error in result.errors: print(f"ERROR: {error}", file=sys.stderr)
        print(f"Publication checks failed: {len(result.errors)} error(s), {len(result.warnings)} warning(s).", file=sys.stderr)
        return 1
    print(f"Publication checks passed with {len(result.warnings)} warning(s). These checks establish structural consistency, not factual truth or release approval.")
    return 0


if __name__ == "__main__": raise SystemExit(main())
