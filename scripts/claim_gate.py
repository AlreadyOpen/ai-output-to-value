#!/usr/bin/env python3
"""Evaluate one claim record against the AI Output to Value decision gate.

This checker is intentionally actor-neutral. The target decision selects the
required claim and checks; the producer identity does not.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES_PATH = ROOT / "schemas" / "v1" / "decision-gates.json"

REQUIRED_FIELDS = {
    "schemaVersion",
    "project",
    "targetDecision",
    "requiredClaimLevel",
    "assertedClaimLevel",
    "intendedUse",
    "actors",
    "authority",
    "accountability",
    "gateChecks",
    "nextEvidence",
    "stopRule",
}


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def evaluate(record: dict, gates: dict) -> dict:
    errors: list[str] = []
    missing = sorted(field for field in REQUIRED_FIELDS if field not in record)
    if missing:
        errors.append("missing required field(s): " + ", ".join(missing))

    if record.get("schemaVersion") != "1.0":
        errors.append("schemaVersion must be '1.0'")

    decisions = gates.get("decisions", {})
    decision_id = record.get("targetDecision")
    rule = decisions.get(decision_id)
    if not isinstance(rule, dict):
        errors.append(f"unknown targetDecision: {decision_id!r}")
        return {
            "status": "BLOCKED",
            "targetDecision": decision_id,
            "errors": errors,
            "failedChecks": [],
            "unknownChecks": [],
        }

    expected_claim = rule.get("requiredClaimLevel")
    if record.get("requiredClaimLevel") != expected_claim:
        errors.append(
            f"requiredClaimLevel must be {expected_claim!r} for targetDecision {decision_id!r}"
        )

    actors = record.get("actors")
    if not isinstance(actors, list) or not actors:
        errors.append("actors must contain at least one actor record")

    checks = record.get("gateChecks")
    if not isinstance(checks, dict):
        errors.append("gateChecks must be an object")
        checks = {}

    failed: list[dict] = []
    unknown: list[dict] = []
    passed: list[dict] = []
    for check in rule.get("requiredChecks", []):
        check_id = check.get("id")
        value = checks.get(check_id, "unknown")
        item = {"id": check_id, "label": check.get("label", ""), "state": value}
        if value == "fail":
            failed.append(item)
        elif value == "pass":
            passed.append(item)
        else:
            unknown.append(item)

    if errors or failed:
        status = "BLOCKED"
    elif unknown:
        status = "INSUFFICIENT_EVIDENCE"
    else:
        status = "PASS"

    return {
        "status": status,
        "targetDecision": decision_id,
        "decisionLabel": rule.get("label"),
        "requiredClaimLevel": expected_claim,
        "assertedClaimLevel": record.get("assertedClaimLevel"),
        "errors": errors,
        "failedChecks": failed,
        "unknownChecks": unknown,
        "passedChecks": passed,
        "rule": gates.get("principle"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claim", type=Path, help="Path to a claim JSON record")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    try:
        record = load_json(args.claim)
        gates = load_json(GATES_PATH)
        result = evaluate(record, gates)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['status']}: {result.get('decisionLabel') or result.get('targetDecision')}")
        print(f"Required claim: {result.get('requiredClaimLevel')}")
        for error in result.get("errors", []):
            print(f"ERROR: {error}")
        for check in result.get("failedChecks", []):
            print(f"FAIL: {check['label']}")
        for check in result.get("unknownChecks", []):
            print(f"UNKNOWN: {check['label']}")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
