#!/usr/bin/env python3
"""Release-approval checks, deliberately separate from preview structure checks."""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

from publication_data import load_claim_records, load_yaml

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get("PUBLICATION_ROOT", str(DEFAULT_ROOT))).resolve()
SITE = ROOT / "site"
RELEASE_SCOPES = {"guide", "policy"}
REVIEW_RECORD_REQUIRED = {"claim_revision", "source_versions_checked", "method", "finding", "disposition"}
ACCEPTING_REVIEW_DISPOSITIONS = {"accepted", "accepted_with_qualification", "revised_and_accepted"}


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


def valid_review_record(record) -> bool:
    if not isinstance(record, dict) or not REVIEW_RECORD_REQUIRED.issubset(record.keys()):
        return False
    for field in {"claim_revision", "method", "finding", "disposition"}:
        if not nonempty_string(record.get(field)):
            return False
    versions = record.get("source_versions_checked")
    return isinstance(versions, list) and bool(versions) and all(nonempty_string(value) for value in versions)


def canonical_repository_path(value) -> str | None:
    """Normalize a repository-relative path so aliases cannot change release scope."""
    if not nonempty_string(value):
        return None
    try:
        resolved = (ROOT / value).resolve()
        return resolved.relative_to(ROOT).as_posix()
    except (OSError, ValueError):
        return None


def published_files(claim: dict) -> set[str]:
    files: set[str] = set()
    publications = claim.get("published_in")
    if not isinstance(publications, list):
        return files
    for publication in publications:
        if not isinstance(publication, dict):
            continue
        normalized = canonical_repository_path(publication.get("file"))
        if normalized:
            files.add(normalized)
    return files


def main() -> int:
    errors: list[str] = []

    manifest = load_yaml(ROOT / "data" / "articles.yml")
    articles = manifest.get("articles", []) if isinstance(manifest, dict) else []
    expected_release_slugs: set[str] = set()
    working_slugs: set[str] = set()
    release_sources: set[str] = set()

    for article in articles:
        if not isinstance(article, dict):
            continue
        scope = article.get("release_scope")
        slug = article.get("slug")
        source = article.get("source")
        if scope in RELEASE_SCOPES and nonempty_string(source):
            normalized_source = canonical_repository_path(source)
            if normalized_source:
                release_sources.add(normalized_source)
            else:
                errors.append(f"release article source escapes publication root: {article.get('id')} ({source})")
        if scope in RELEASE_SCOPES and nonempty_string(slug):
            expected_release_slugs.add(slug)
            if scope == "guide" and article.get("status") != "ready":
                errors.append(f"guide article is not marked ready for publication: {article.get('id')} (status={article.get('status')})")
            if scope == "policy" and article.get("status") not in {"active_policy", "ready"}:
                errors.append(f"policy article is not release-ready: {article.get('id')} (status={article.get('status')})")
        elif scope == "working" and nonempty_string(slug):
            working_slugs.add(slug)
        elif scope not in {"guide", "policy", "working"}:
            errors.append(f"article has unknown release_scope: {article.get('id')} ({scope})")

    for _, claim in load_claim_records(ROOT):
        if not isinstance(claim, dict):
            continue
        critical = claim.get("launch_critical")
        if not isinstance(critical, bool):
            errors.append(f"claim lacks explicit Boolean launch_critical classification: {claim.get('id', '<missing id>')}")
            continue

        release_published = bool(published_files(claim) & release_sources)
        effective_critical = critical or release_published
        if not effective_critical:
            continue

        if release_published and critical is False:
            errors.append(
                f"release-published claim cannot opt out with launch_critical: false: {claim.get('id', '<missing id>')}"
            )

        if claim.get("independent_review_status") != "completed":
            errors.append(f"launch-critical claim has not completed independent review: {claim.get('id', '<missing id>')}")
        if not nonempty_string(claim.get("reviewer")) or not valid_date(claim.get("reviewed")):
            errors.append(f"launch-critical claim lacks an inspectable reviewer/process and valid review date: {claim.get('id', '<missing id>')}")

        record = claim.get("review_record")
        if not valid_review_record(record):
            errors.append(f"launch-critical claim lacks a complete independent review_record: {claim.get('id', '<missing id>')}")
        elif record.get("disposition") not in ACCEPTING_REVIEW_DISPOSITIONS:
            errors.append(
                f"launch-critical claim review disposition does not accept claim: "
                f"{claim.get('id', '<missing id>')} ({record.get('disposition')})"
            )

    article_dir = SITE / "articles"
    if article_dir.exists():
        for slug in expected_release_slugs:
            if not (article_dir / f"{slug}.html").exists():
                errors.append(f"release artifact is missing approved article: {slug}")
        for slug in working_slugs:
            if (article_dir / f"{slug}.html").exists():
                errors.append(f"release artifact incorrectly includes working article: {slug}")
    else:
        errors.append("release artifact has not been built: site/articles is missing")

    if errors:
        for error in errors:
            print(f"RELEASE BLOCKER: {error}", file=sys.stderr)
        print(f"Release approval failed with {len(errors)} blocker(s). The preview build may still be structurally valid.", file=sys.stderr)
        return 1

    print("Release approval checks passed for the declared release artifact and accepted review records. This is not a guarantee of factual truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
