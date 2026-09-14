#!/usr/bin/env python3
"""Structural preview-publication gate.

Validates structure, traceability, metadata types and deployment-local links.
It does not establish factual truth and is separate from release approval.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

from publication_data import load_claim_records, load_source_records, load_yaml

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get("PUBLICATION_ROOT", str(DEFAULT_ROOT))).resolve()
DATA_DIR, SITE_DIR = ROOT / "data", ROOT / "site"

SOURCE_REQUIRED = {"id", "title", "publisher", "url", "evidence_type", "supports", "scope", "limitations", "reviewed"}
CLAIM_REQUIRED = {"id", "claim_text", "status", "launch_critical", "evidence", "published_in", "reviewer", "reviewed", "independent_review_status"}
EVIDENCE_REQUIRED = {"source_id", "locator", "relevant_finding", "qualification"}
ARTICLE_REQUIRED = {"id", "title", "source", "slug", "section", "order", "summary", "maintainer", "reviewed", "status", "release_scope"}
REVIEW_RECORD_REQUIRED = {"claim_revision", "source_versions_checked", "method", "finding", "disposition"}

CLAIM_STATUSES = {"supported", "qualified", "contested", "illustrative", "anecdotal", "editorial"}
REVIEW_STATUSES = {"pending", "completed", "not_required"}
REVIEW_DISPOSITIONS = {"accepted", "accepted_with_qualification", "revised_and_accepted", "rejected"}
ARTICLE_SECTIONS = {"core", "deeper", "advanced", "policy"}
ARTICLE_STATUSES = {"draft", "research_draft", "editorial_review", "active_policy", "ready"}
RELEASE_SCOPES = {"guide", "policy", "working"}
RESERVED_ARTICLE_SLUGS = {"index"}

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)
HTML_ID_RE = re.compile(r"\bid=[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


class CheckResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_date(value) -> bool:
    if isinstance(value, date):
        return True
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        date.fromisoformat(value.strip())
        return True
    except ValueError:
        return False


def slugify_heading(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def require_string(mapping: dict, field: str, label: str, result: CheckResult) -> None:
    if field in mapping and not nonempty_string(mapping.get(field)):
        result.error(f"{label} field '{field}' must be a non-empty string")


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
            result.error(f"{label} must be a mapping")
            continue
        missing = sorted(SOURCE_REQUIRED - source.keys())
        if missing:
            result.error(f"{label} missing fields: {', '.join(missing)}")
        for field in SOURCE_REQUIRED - {"supports", "reviewed"}:
            require_string(source, field, label, result)
        if "reviewed" in source and not valid_date(source.get("reviewed")):
            result.error(f"{label} field 'reviewed' must be an ISO date")

        sid = source.get("id")
        if not nonempty_string(sid):
            continue
        if sid in ids:
            result.error(f"duplicate source id: {sid}")
        ids.add(sid)

        supports = source.get("supports")
        if not isinstance(supports, list) or not supports or not all(nonempty_string(x) for x in supports):
            result.error(f"{label} field 'supports' must be a non-empty list of non-empty strings")

    if not ids:
        result.error("no source records found in canonical data/*.yml registries")
    return ids


def locator_exists(target: Path, locator: str) -> bool:
    try:
        text = target.read_text(encoding="utf-8")
    except Exception:
        return False
    return locator.strip() in text


def check_review_record(claim: dict, cid: str, result: CheckResult) -> None:
    record = claim.get("review_record")
    if not isinstance(record, dict):
        result.error(f"{cid}: completed independent review requires a structured review_record")
        return
    missing = sorted(REVIEW_RECORD_REQUIRED - record.keys())
    if missing:
        result.error(f"{cid}: review_record missing fields: {', '.join(missing)}")
    for field in REVIEW_RECORD_REQUIRED - {"source_versions_checked"}:
        require_string(record, field, f"{cid}: review_record", result)
    versions = record.get("source_versions_checked")
    if not isinstance(versions, list) or not versions or not all(nonempty_string(v) for v in versions):
        result.error(f"{cid}: review_record source_versions_checked must be a non-empty list of strings")
    disposition = record.get("disposition")
    if nonempty_string(disposition) and disposition not in REVIEW_DISPOSITIONS:
        result.error(f"{cid}: unknown review disposition: {disposition}")


def check_claims(source_ids: set[str], result: CheckResult) -> None:
    try:
        records = load_claim_records(ROOT)
    except Exception as exc:
        result.error(f"canonical claim registry could not be loaded: {exc}")
        return
    if not records:
        result.error("no claim records found in data/*.yml")

    ids: set[str] = set()
    for path, claim in records:
        label = f"{path.relative_to(ROOT)}: claim"
        if not isinstance(claim, dict):
            result.error(f"{label} must be a mapping")
            continue
        missing = sorted(CLAIM_REQUIRED - claim.keys())
        if missing:
            result.error(f"{label} missing fields: {', '.join(missing)}")

        for field in {"id", "claim_text", "status", "reviewer", "independent_review_status"}:
            require_string(claim, field, label, result)
        if "reviewed" in claim and not valid_date(claim.get("reviewed")):
            result.error(f"{label} field 'reviewed' must be an ISO date")
        if "launch_critical" in claim and not isinstance(claim.get("launch_critical"), bool):
            result.error(f"{label} field 'launch_critical' must be a Boolean")

        cid = claim.get("id") if nonempty_string(claim.get("id")) else "<missing id>"
        if cid != "<missing id>":
            if cid in ids:
                result.error(f"duplicate claim id: {cid}")
            ids.add(cid)

        status = claim.get("status")
        if nonempty_string(status) and status not in CLAIM_STATUSES:
            result.error(f"{cid}: unknown claim status: {status}")
        review_status = claim.get("independent_review_status")
        if nonempty_string(review_status) and review_status not in REVIEW_STATUSES:
            result.error(f"{cid}: unknown independent_review_status: {review_status}")

        evidence = claim.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            result.error(f"{cid}: evidence must be a non-empty list")
        else:
            for i, item in enumerate(evidence, 1):
                elabel = f"{cid}: evidence #{i}"
                if not isinstance(item, dict):
                    result.error(f"{elabel} must be a mapping")
                    continue
                missing_e = sorted(EVIDENCE_REQUIRED - item.keys())
                if missing_e:
                    result.error(f"{elabel} missing fields: {', '.join(missing_e)}")
                for field in EVIDENCE_REQUIRED:
                    require_string(item, field, elabel, result)
                if item.get("source_id") not in source_ids:
                    result.error(f"{elabel} references unknown source_id: {item.get('source_id')}")

        pubs = claim.get("published_in")
        if not isinstance(pubs, list) or not pubs:
            result.error(f"{cid}: published_in must be a non-empty list")
        else:
            for i, pub in enumerate(pubs, 1):
                plabel = f"{cid}: published_in #{i}"
                if not isinstance(pub, dict):
                    result.error(f"{plabel} must be a mapping")
                    continue
                target, locator = pub.get("file"), pub.get("locator")
                if not nonempty_string(target):
                    result.error(f"{plabel} requires a non-empty string file")
                    continue
                if not nonempty_string(locator):
                    result.error(f"{plabel} requires a non-empty string locator")
                    continue
                target_path = ROOT / target
                if not target_path.exists():
                    result.error(f"{plabel} points to missing file: {target}")
                elif not locator_exists(target_path, locator):
                    result.error(f"{plabel} locator was not found in {target}: {locator}")

        if review_status == "completed":
            if not nonempty_string(claim.get("reviewer")) or not valid_date(claim.get("reviewed")):
                result.error(f"{cid}: completed independent review requires reviewer/process and a valid reviewed date")
            check_review_record(claim, cid, result)
        elif review_status == "not_required" and claim.get("launch_critical") is True:
            result.error(f"{cid}: launch-critical claim cannot set independent review to not_required")
        else:
            result.warn(f"{cid}: independent review is {review_status or 'unspecified'}")


def check_articles(result: CheckResult) -> None:
    path = DATA_DIR / "articles.yml"
    try:
        data = load_yaml(path)
    except Exception as exc:
        result.error(f"data/articles.yml invalid: {exc}")
        return
    articles = data.get("articles") if isinstance(data, dict) else None
    if not isinstance(articles, list):
        result.error("data/articles.yml: top-level 'articles' must be a list")
        return

    ids, slugs = set(), set()
    for i, article in enumerate(articles, 1):
        label = f"data/articles.yml: article #{i}"
        if not isinstance(article, dict):
            result.error(f"{label} must be a mapping")
            continue
        missing = sorted(ARTICLE_REQUIRED - article.keys())
        if missing:
            result.error(f"{label} missing fields: {', '.join(missing)}")

        for field in {"id", "title", "source", "slug", "section", "summary", "maintainer", "status", "release_scope"}:
            require_string(article, field, label, result)
        if "reviewed" in article and not valid_date(article.get("reviewed")):
            result.error(f"{label} field 'reviewed' must be an ISO date")
        if "order" in article and (not isinstance(article.get("order"), int) or isinstance(article.get("order"), bool)):
            result.error(f"{label} field 'order' must be an integer")

        aid = article.get("id") if nonempty_string(article.get("id")) else ""
        slug = article.get("slug") if nonempty_string(article.get("slug")) else ""
        source = article.get("source") if nonempty_string(article.get("source")) else ""
        if aid in ids:
            result.error(f"duplicate article id: {aid}")
        elif aid:
            ids.add(aid)
        if slug in slugs:
            result.error(f"duplicate article slug: {slug}")
        elif slug:
            slugs.add(slug)
        if slug in RESERVED_ARTICLE_SLUGS:
            result.error(f"reserved article slug: {slug}")
        if slug and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
            result.error(f"invalid article slug: {slug}")
        if source and not (ROOT / source).exists():
            result.error(f"{label} source does not exist: {source}")

        section = article.get("section")
        status = article.get("status")
        release_scope = article.get("release_scope")
        if nonempty_string(section) and section not in ARTICLE_SECTIONS:
            result.error(f"{label} unknown section: {section}")
        if nonempty_string(status) and status not in ARTICLE_STATUSES:
            result.error(f"{label} unknown status: {status}")
        if nonempty_string(release_scope) and release_scope not in RELEASE_SCOPES:
            result.error(f"{label} unknown release_scope: {release_scope}")


def iter_text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html"} and not any(p in SKIP_DIRS for p in path.parts):
            yield path


def extract_links(path: Path, text: str) -> list[str]:
    return MARKDOWN_LINK_RE.findall(text) if path.suffix.lower() == ".md" else HTML_HREF_RE.findall(text)


def fragment_exists(target: Path, fragment: str) -> bool:
    fragment = unquote(fragment)
    try:
        text = target.read_text(encoding="utf-8")
    except Exception:
        return False
    if target.suffix.lower() == ".html":
        return fragment in set(HTML_ID_RE.findall(text))
    if target.suffix.lower() == ".md":
        return fragment in {slugify_heading(h) for h in HEADING_RE.findall(text)}
    return True


def built_candidate(source_path: Path, raw_link: str) -> Path | None:
    try:
        rel = source_path.resolve().relative_to(ROOT)
    except ValueError:
        return None
    if rel.parts and rel.parts[0] == "site":
        return None
    parsed = urlsplit(raw_link)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    base = SITE_DIR if parsed.path.startswith("/") else (SITE_DIR / rel).parent
    candidate = base / unquote(parsed.path).lstrip("/") if parsed.path.startswith("/") else base / unquote(parsed.path)
    try:
        candidate.resolve().relative_to(SITE_DIR.resolve())
    except ValueError:
        return None
    return candidate.resolve() if candidate.exists() else None


def check_internal_links(result: CheckResult) -> None:
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            result.error(f"{path.relative_to(ROOT)}: not valid UTF-8")
            continue

        try:
            path.resolve().relative_to(SITE_DIR.resolve())
            in_site = True
        except ValueError:
            in_site = False

        for raw in extract_links(path, text):
            parsed = urlsplit(raw.strip())
            if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
                continue
            if not parsed.path:
                if parsed.fragment and path.suffix.lower() == ".html" and not fragment_exists(path, parsed.fragment):
                    result.error(f"{path.relative_to(ROOT)}: missing fragment target: {raw}")
                continue

            if parsed.path.startswith("/"):
                root = SITE_DIR if in_site else ROOT
                target = (root / unquote(parsed.path).lstrip("/")).resolve()
            else:
                target = (path.parent / unquote(parsed.path)).resolve()

            allowed_root = SITE_DIR.resolve() if in_site else ROOT.resolve()
            try:
                target.relative_to(allowed_root)
            except ValueError:
                kind = "built link escapes deployment root" if in_site else "local link escapes repository"
                result.error(f"{path.relative_to(ROOT)}: {kind}: {raw}")
                continue

            actual = target if target.exists() else built_candidate(path, raw)
            if actual is None:
                result.error(f"{path.relative_to(ROOT)}: broken internal link: {raw}")
                continue
            if parsed.fragment and not fragment_exists(actual, parsed.fragment):
                result.error(f"{path.relative_to(ROOT)}: missing fragment target: {raw}")


def check_built_site(result: CheckResult) -> None:
    for path in [SITE_DIR / "index.html", SITE_DIR / "articles" / "index.html", SITE_DIR / "evidence" / "index.html"]:
        if not path.exists():
            result.error(f"built publication file is missing: {path.relative_to(ROOT)}")


def main() -> int:
    result = CheckResult()
    source_ids = check_sources(result)
    check_claims(source_ids, result)
    check_articles(result)
    check_built_site(result)
    check_internal_links(result)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Publication checks failed: {len(result.errors)} error(s), {len(result.warnings)} warning(s).", file=sys.stderr)
        return 1

    print(f"Publication checks passed with {len(result.warnings)} warning(s). These checks establish structural consistency, not factual truth or release approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
