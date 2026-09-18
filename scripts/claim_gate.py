#!/usr/bin/env python3
"""Evaluate one claim record against the AI Output to Value decision gate.

This checker is intentionally actor-neutral. The target decision selects the
required claim and checks; the producer identity does not.
"""
from __future__ import annotations

import argparse
import json
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
GATES_PATH = ROOT / "schemas" / "v1" / "decision-gates.json"
CLAIM_SCHEMA_PATH = ROOT / "schemas" / "v1" / "claim.schema.json"

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


@lru_cache(maxsize=1)
def claim_validator() -> Draft202012Validator:
    schema = load_json(CLAIM_SCHEMA_PATH)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_errors(record: dict) -> list[str]:
    errors = sorted(
        claim_validator().iter_errors(record),
        key=lambda error: (list(error.path), error.message),
    )
    rendered: list[str] = []
    for error in errors:
        location = "/".join(map(str, error.path)) or "<root>"
        rendered.append(f"claim.schema.json {location}: {error.message}")
    return rendered


def result_metadata(gates: dict) -> dict:
    principle = gates.get("principle")
    return {
        "gateVersion": gates.get("version"),
        "principle": principle,
        # Backward-compatible alias while all consumers migrate to `principle`.
        "rule": principle,
    }


def evaluate(record: dict, gates: dict) -> dict:
    structural_errors: list[str] = schema_errors(record)
    missing_fields: list[str] = []

    decision_id = record.get("targetDecision")
    decisions = gates.get("decisions")
    # Do not use untrusted claim data as a mapping key until its type is known.
    # This guard is independent of schema validation so malformed input still
    # produces a structured BLOCKED result rather than an exception.
    rule = (
        decisions.get(decision_id)
        if isinstance(decisions, dict) and isinstance(decision_id, str)
        else None
    )

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
            **result_metadata(gates),
        }

    expected_claim = rule.get("requiredClaimLevel")
    if record.get("requiredClaimLevel") != expected_claim:
        message = f"requiredClaimLevel must be {expected_claim!r} for targetDecision {decision_id!r}"
        if message not in structural_errors:
            structural_errors.append(message)

    for field in REQUIRED_TEXT_FIELDS:
        value = record.get(field)
        if isinstance(value, str) and not value.strip():
            missing_fields.append(field)

    actors = record.get("actors")
    if isinstance(actors, list) and not actors:
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
        **result_metadata(gates),
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
