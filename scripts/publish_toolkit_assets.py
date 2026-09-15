#!/usr/bin/env python3
"""Publish reusable Claim Gate samples, templates, and the private workbook."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def copy_tree(source: Path, target: Path) -> None:
    if not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=True)


def main() -> None:
    copy_tree(ROOT / "toolkit" / "samples", SITE / "samples")
    copy_tree(ROOT / "toolkit" / "templates", SITE / "templates")

    private_source = ROOT / "toolkit" / "private-workbook"
    downloads = SITE / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    copy_tree(private_source, downloads / "private-workbook")

    archive_base = downloads / "ai-output-to-value-private-workbook"
    archive_path = archive_base.with_suffix(".zip")
    if archive_path.exists():
        archive_path.unlink()
    if private_source.exists():
        shutil.make_archive(str(archive_base), "zip", root_dir=private_source)

    print("Published Claim Gate samples, software Outcome template, and private workbook")


if __name__ == "__main__":
    main()
