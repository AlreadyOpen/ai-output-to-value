#!/usr/bin/env python3
"""Small structural publication gate for AI Output to Value.

This script does not establish whether a claim is true. It checks that the
repository's evidence and publication structure is internally consistent:

- YAML parses;
- source IDs are unique;
- required source metadata is present;
- claim IDs are unique;
- claim evidence points to registered source IDs;
- claim publication targets exist;
- local Markdown/HTML links point to existing files or directories.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

SOURCE_REQUIRED = {
    "id",
    "title",
    "publisher",
    "url",
    "evidence_type",
    "supports",
    "scope",
    "limitations",
    "reviewed",
}

CLAIM_REQUIRED = {
    "id",
    "claim_text",
    "status",
    "evidence",
    "published_in",
    "reviewer",
    "reviewed",
    "human_review_status",
}

EVIDENCE_REQUIRED = {
    "source_id",
    "locator",
    "relevant_finding",
    "qualification",
}

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)

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


def load_yaml(path: Path, result: CheckResult):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # PyYAML provides useful parse details in str(exc)
        result.error(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return None


def check_sources(result: CheckResult) -> set[str]:
    source_ids: set[str] = set()

    for path in sorted(DATA_DIR.glob("*.yml")):
        data = load_yaml(path, result)
        if not isinstance(data, dict) or "sources" not in data:
            continue

        sources = data.get("sources")
        if not isinstance(sources, list):
            result.error(f"{path.relative_to(ROOT)}: 'sources' must be a list")
            continue

        for index, source in enumerate(sources, start=1):
            label = f"{path.relative_to(ROOT)}: source #{index}"
            if not isinstance(source, dict):
                result.error(f"{label} must be a mapping")
                continue

            missing = sorted(SOURCE_REQUIRED - source.keys())
            if missing:
                result.error(f"{label} missing fields: {', '.join(missing)}")

            source_id = source.get("id")
            if not isinstance(source_id, str) or not source_id.strip():
                result.error(f"{label} has an invalid id")
                continue

            if source_id in source_ids:
                result.error(f"duplicate source id: {source_id}")
            source_ids.add(source_id)

            supports = source.get("supports")
            if supports is not None and (
                not isinstance(supports, list)
                or not supports
                or not all(isinstance(item, str) and item.strip() for item in supports)
            ):
                result.error(f"{label} field 'supports' must be a non-empty list of strings")

    if not source_ids:
        result.error("no source records found in data/*.yml")

    return source_ids


def check_claims(source_ids: set[str], result: CheckResult) -> None:
    path = DATA_DIR / "claims.yml"
    if not path.exists():
        result.error("data/claims.yml is missing")
        return

    data = load_yaml(path, result)
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        result.error("data/claims.yml: top-level 'claims' must be a list")
        return

    claim_ids: set[str] = set()

    for index, claim in enumerate(data["claims"], start=1):
        label = f"data/claims.yml: claim #{index}"
        if not isinstance(claim, dict):
            result.error(f"{label} must be a mapping")
            continue

        missing = sorted(CLAIM_REQUIRED - claim.keys())
        if missing:
            result.error(f"{label} missing fields: {', '.join(missing)}")

        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            result.error(f"{label} has an invalid id")
            continue
        if claim_id in claim_ids:
            result.error(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)

        evidence = claim.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            result.error(f"{claim_id}: evidence must be a non-empty list")
        else:
            for evidence_index, item in enumerate(evidence, start=1):
                evidence_label = f"{claim_id}: evidence #{evidence_index}"
                if not isinstance(item, dict):
                    result.error(f"{evidence_label} must be a mapping")
                    continue
                missing_evidence = sorted(EVIDENCE_REQUIRED - item.keys())
                if missing_evidence:
                    result.error(
                        f"{evidence_label} missing fields: {', '.join(missing_evidence)}"
                    )
                source_id = item.get("source_id")
                if source_id not in source_ids:
                    result.error(
                        f"{evidence_label} references unknown source_id: {source_id}"
                    )

        published_in = claim.get("published_in")
        if not isinstance(published_in, list) or not published_in:
            result.error(f"{claim_id}: published_in must be a non-empty list")
        else:
            for pub_index, publication in enumerate(published_in, start=1):
                pub_label = f"{claim_id}: published_in #{pub_index}"
                if not isinstance(publication, dict):
                    result.error(f"{pub_label} must be a mapping")
                    continue
                target = publication.get("file")
                locator = publication.get("locator")
                if not isinstance(target, str) or not target.strip():
                    result.error(f"{pub_label} requires a file")
                    continue
                if not (ROOT / target).exists():
                    result.error(f"{pub_label} points to missing file: {target}")
                if not isinstance(locator, str) or not locator.strip():
                    result.error(f"{pub_label} requires a locator")

        if claim.get("human_review_status") != "completed":
            result.warn(
                f"{claim_id}: human review is {claim.get('human_review_status', 'unspecified')}"
            )


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".html"}:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def extract_links(path: Path, text: str) -> list[str]:
    if path.suffix.lower() == ".md":
        return MARKDOWN_LINK_RE.findall(text)
    return HTML_HREF_RE.findall(text)


def local_target(source_path: Path, raw_link: str) -> Path | None:
    raw_link = raw_link.strip()
    if not raw_link or raw_link.startswith("#"):
        return None

    parsed = urlsplit(raw_link)
    if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
        return None

    link_path = unquote(parsed.path)
    if not link_path:
        return None

    if link_path.startswith("/"):
        return ROOT / link_path.lstrip("/")
    return source_path.parent / link_path


def check_internal_links(result: CheckResult) -> None:
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            result.error(f"{path.relative_to(ROOT)}: not valid UTF-8")
            continue

        for raw_link in extract_links(path, text):
            target = local_target(path, raw_link)
            if target is None:
                continue
            resolved = target.resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                result.error(
                    f"{path.relative_to(ROOT)}: local link escapes repository: {raw_link}"
                )
                continue
            if not resolved.exists():
                result.error(
                    f"{path.relative_to(ROOT)}: broken internal link: {raw_link}"
                )


def main() -> int:
    result = CheckResult()
    source_ids = check_sources(result)
    check_claims(source_ids, result)
    check_internal_links(result)

    for warning in result.warnings:
        print(f"WARNING: {warning}")

    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"Publication checks failed: {len(result.errors)} error(s), "
            f"{len(result.warnings)} warning(s).",
            file=sys.stderr,
        )
        return 1

    print(
        f"Publication checks passed with {len(result.warnings)} warning(s). "
        "These checks establish structural consistency, not factual truth."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
