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

REQUIRED_TEXT_FIELDS = (
    "project",
    "intendedUse",
    "authority",
    "accountability",
    "nextEvidence",
    "stopRule",
)


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def evaluate(record: dict, gates: dict) -> dict:
    decision_id = record.get("targetDecision")
    decisions = gates.get("decisions", {})
    rule = decisions.get(decision_id)

    structural_errors: list[str] = []
    missing_fields: list[str] = []

    if record.get("schemaVersion") != "1.0":
        structural_errors.append("schemaVersion must be '1.0'")

    if not isinstance(rule, dict):
        structural_errors.append(f"unknown targetDecision: {decision_id!r}")
        return {
            "status": "BLOCKED",
            "targetDecision": decision_id,
            "errors": structural_errors,
            "structuralErrors": structural_errors,
            "missingFields": missing_fields,
            "claimMismatch": False,
            "failedChecks": [],
            "unknownChecks": [],
            "passedChecks": [],
        }

    expected_claim = rule.get("requiredClaimLevel")
    if record.get("requiredClaimLevel") != expected_claim:
        structural_errors.append(
            f"requiredClaimLevel must be {expected_claim!r} for targetDecision {decision_id!r}"
        )

    for field in REQUIRED_TEXT_FIELDS:
        if not str(record.get(field, "")).strip():
            missing_fields.append(field)

    actors = record.get("actors")
    if not isinstance(actors, list) or not actors:
        missing_fields.append("actors")

    claim_mismatch = record.get("assertedClaimLevel") != expected_claim

    checks = record.get("gateChecks")
    if not isinstance(checks, dict):
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
            # "unknown" and "not-applicable" both mean the evidence needed
            # for this required gate check has not been established.
            unknown.append(item)

    if structural_errors or failed:
        status = "BLOCKED"
    elif unknown or missing_fields or claim_mismatch:
        status = "INSUFFICIENT_EVIDENCE"
    else:
        status = "PASS"

    return {
        "status": status,
        "targetDecision": decision_id,
        "decisionLabel": rule.get("label"),
        "requiredClaimLevel": expected_claim,
        "assertedClaimLevel": record.get("assertedClaimLevel"),
        "errors": structural_errors,
        "structuralErrors": structural_errors,
        "missingFields": missing_fields,
        "claimMismatch": claim_mismatch,
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
        for error in result.get("structuralErrors", []):
            print(f"ERROR: {error}")
        for field in result.get("missingFields", []):
            print(f"MISSING: {field}")
        if result.get("claimMismatch"):
            print("MISMATCH: assertedClaimLevel does not match the claim required by targetDecision")
        for check in result.get("failedChecks", []):
            print(f"FAIL: {check['label']}")
        for check in result.get("unknownChecks", []):
            print(f"UNKNOWN: {check['label']}")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
