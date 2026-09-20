from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import claim_gate  # noqa: E402
from claim_gate import evaluate  # noqa: E402


class ClaimGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gates = json.loads((REPO_ROOT / "schemas" / "v1" / "decision-gates.json").read_text(encoding="utf-8"))
        cls.conformance = json.loads(
            (REPO_ROOT / "tests" / "fixtures" / "claim-gate-conformance.json").read_text(encoding="utf-8")
        )

    def base_record(self):
        return copy.deepcopy(self.conformance["baseRecord"])

    def patched_record(self, patch, remove=()):
        record = self.base_record()
        for key, replacement in (patch or {}).items():
            if key == "gateChecks" and isinstance(replacement, dict):
                record["gateChecks"].update(replacement)
            else:
                record[key] = copy.deepcopy(replacement)
        for key in remove:
            record.pop(key, None)
        return record

    def test_shared_conformance_fixture(self):
        for item in self.conformance["cases"]:
            with self.subTest(item=item["name"]):
                if "record" in item:
                    record = copy.deepcopy(item["record"])
                else:
                    record = self.patched_record(item.get("patch", {}), item.get("remove", ()))
                result = evaluate(record, self.gates)
                self.assertEqual(result["status"], item["expectedStatus"])
                self.assertEqual(result["gateVersion"], self.gates["version"])
                self.assertEqual(result["principle"], self.gates["principle"])
                self.assertEqual(result["rule"], self.gates["principle"])
                if "expectedClaimMismatch" in item:
                    self.assertEqual(result["claimMismatch"], item["expectedClaimMismatch"])
                if "expectedMissingFields" in item:
                    self.assertEqual(result["missingFields"], item["expectedMissingFields"])
                errors = " ".join(result["structuralErrors"]).lower()
                for needle in item.get("errorContains", []):
                    self.assertIn(str(needle).lower(), errors)

    def test_every_schema_format_is_enforced_by_the_python_gate(self):
        schema = json.loads((REPO_ROOT / "schemas" / "v1" / "claim.schema.json").read_text(encoding="utf-8"))
        formats: set[str] = set()

        def walk(node):
            if isinstance(node, dict):
                if isinstance(node.get("format"), str):
                    formats.add(node["format"])
                for child in node.values():
                    walk(child)
            elif isinstance(node, list):
                for child in node:
                    walk(child)

        walk(schema)
        checker = claim_gate.claim_validator().format_checker
        self.assertTrue(formats)
        for name in sorted(formats):
            with self.subTest(format=name):
                self.assertIn(name, checker.checkers)

    def test_gate_files_carry_an_spdx_licence_header(self):
        for relative in ("scripts/claim_gate.py", "packages/mcp/src/core.mjs"):
            with self.subTest(file=relative):
                head = (REPO_ROOT / relative).read_text(encoding="utf-8").splitlines()[:3]
                self.assertIn("SPDX-License-Identifier: Apache-2.0", "\n".join(head))

    def test_complete_required_gate_passes(self):
        result = evaluate(self.base_record(), self.gates)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["gateVersion"], "1.1")
        self.assertEqual(result["principle"], self.gates["principle"])
        self.assertEqual(result["rule"], result["principle"])

    def test_failed_required_check_blocks(self):
        record = self.base_record()
        record["gateChecks"]["failure-modes-tested"] = "fail"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["failedChecks"])

    def test_unknown_required_check_is_insufficient(self):
        record = self.base_record()
        record["gateChecks"]["acceptance-criteria-met"] = "unknown"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "INSUFFICIENT_EVIDENCE")

    def test_not_applicable_required_check_is_insufficient_and_preserved(self):
        record = self.base_record()
        record["gateChecks"]["acceptance-criteria-met"] = "not-applicable"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(result["unknownChecks"][0]["state"], "not-applicable")

    def test_empty_required_text_is_schema_blocked(self):
        record = self.base_record()
        record["authority"] = ""
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("authority", " ".join(result["structuralErrors"]))

    def test_empty_actor_list_is_schema_blocked(self):
        record = self.base_record()
        record["actors"] = []
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("actors", " ".join(result["structuralErrors"]))

    def test_non_string_required_fields_are_schema_blocked(self):
        record = self.base_record()
        record.update({
            "authority": [],
            "accountability": False,
            "stopRule": 0,
            "intendedUse": {},
        })
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        errors = " ".join(result["structuralErrors"])
        for field in ("authority", "accountability", "stopRule", "intendedUse"):
            self.assertIn(field, errors)

    def test_invalid_gate_check_state_is_schema_blocked(self):
        record = self.base_record()
        record["gateChecks"]["acceptance-criteria-met"] = "maybe"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("gateChecks", " ".join(result["structuralErrors"]))

    def test_schema_rejects_undeclared_top_level_properties(self):
        record = self.base_record()
        record["unexpectedField"] = "not in claim.schema.json"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("Additional properties", " ".join(result["structuralErrors"]))

    def test_schema_enforces_field_length_constraints(self):
        record = self.base_record()
        record["authority"] = "x" * 1001
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("authority", " ".join(result["structuralErrors"]))

    def test_asserted_claim_mismatch_is_insufficient(self):
        record = self.base_record()
        record["assertedClaimLevel"] = "02-output"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "INSUFFICIENT_EVIDENCE")
        self.assertTrue(result["claimMismatch"])

    def test_decision_controls_required_claim(self):
        record = self.base_record()
        record["requiredClaimLevel"] = "02-output"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("requiredClaimLevel", " ".join(result["structuralErrors"]))

    def test_unsupported_schema_version_blocks(self):
        record = self.base_record()
        record["schemaVersion"] = "2.0"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("schemaVersion" in error for error in result["structuralErrors"]))

    def test_non_string_target_decision_returns_structured_block(self):
        record = self.base_record()
        record["targetDecision"] = []
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["targetDecision"], [])
        self.assertTrue(result["structuralErrors"])

    def test_cli_non_string_target_decision_returns_json_without_traceback(self):
        for decision_id in ([], {}, False, 0, None):
            with self.subTest(targetDecision=decision_id), tempfile.TemporaryDirectory() as temp_dir:
                record = self.base_record()
                record["targetDecision"] = decision_id
                claim_path = Path(temp_dir) / "claim.json"
                claim_path.write_text(json.dumps(record), encoding="utf-8")

                result = subprocess.run(
                    [sys.executable, str(REPO_ROOT / "scripts" / "claim_gate.py"), str(claim_path), "--json"],
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "BLOCKED")
                self.assertEqual(payload["targetDecision"], decision_id)
                self.assertTrue(
                    any("targetDecision" in error for error in payload["structuralErrors"]),
                    payload,
                )

    def test_producer_identity_does_not_change_gate(self):
        ai_record = self.base_record()
        human_record = self.base_record()
        human_record["actors"] = [{"type": "human", "role": "Author"}]
        self.assertEqual(evaluate(ai_record, self.gates)["status"], evaluate(human_record, self.gates)["status"])


if __name__ == "__main__":
    unittest.main()
