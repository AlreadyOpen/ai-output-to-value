#!/usr/bin/env python3
"""Publish the working software failure-mode catalogue into site/api/v1."""
from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PUBLICATION_MODE = os.environ.get("PUBLICATION_MODE", "preview").strip().lower()


def main() -> None:
    source = yaml.safe_load((ROOT / "data" / "failure-modes.yml").read_text(encoding="utf-8"))
    modes = source.get("failure_modes", []) if isinstance(source, dict) else []

    payload = {
        "publicationMode": PUBLICATION_MODE,
        "character": source.get("character", "editorial_operational_catalogue") if isinstance(source, dict) else "editorial_operational_catalogue",
        "scope": source.get("scope", "") if isinstance(source, dict) else "",
        "reviewState": "working material; excluded from reviewed release" if PUBLICATION_MODE == "release" else "working preview",
        "failureModes": [] if PUBLICATION_MODE == "release" else modes,
    }

    target = SITE / "api" / "v1" / "failure-modes.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Published {len(payload['failureModes'])} failure modes for {PUBLICATION_MODE} mode")


if __name__ == "__main__":
    main()
