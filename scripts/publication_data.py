#!/usr/bin/env python3
"""Shared data-loading helpers for the publication builder and validators.

Canonical publication evidence lives under data/. Source records may be split
across multiple YAML files, as may claim records. Both the builder and checks
must use this module so that they agree on what counts as a published source or
claim.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _registry_records(data_dir: Path, key: str) -> list[tuple[Path, dict]]:
    records: list[tuple[Path, dict]] = []
    for path in sorted(data_dir.glob("*.yml")):
        data = load_yaml(path)
        if not isinstance(data, dict) or key not in data:
            continue
        values = data.get(key)
        if not isinstance(values, list):
            raise ValueError(f"{path}: top-level '{key}' must be a list")
        for record in values:
            records.append((path, record))
    return records


def load_source_records(root: Path) -> list[tuple[Path, dict]]:
    return _registry_records(root / "data", "sources")


def load_claim_records(root: Path) -> list[tuple[Path, dict]]:
    return _registry_records(root / "data", "claims")


def source_map(root: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for path, source in load_source_records(root):
        source_id = source.get("id") if isinstance(source, dict) else None
        if not isinstance(source_id, str) or not source_id.strip():
            continue
        if source_id in result:
            raise ValueError(f"duplicate source id across canonical registries: {source_id} ({path})")
        result[source_id] = source
    return result


def claims(root: Path) -> list[dict]:
    return [record for _, record in load_claim_records(root) if isinstance(record, dict)]
