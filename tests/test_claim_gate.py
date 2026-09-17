from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from claim_gate import evaluate  # noqa: E402


class ClaimGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gates = json.loads((REPO_ROOT / "schemas" / "v1" / "decision-gates.json").read_text(encoding="utf-8"))

    def base_record(self):
        return {
            "schemaVersion": "1.0",
            "project": "example",
            "targetDecision": "rely",
            "requiredClaimLevel": "03-deliverable",
            "assertedClaimLevel": "03-deliverable",
            "intendedUse": "Named use",
            "actors": [{"type": "ai-agent", "role": "Draft"}],
            "authority": "Bounded",
            "accountability": "Organisation",
            "gateChecks": {
                "intended-use-defined": "pass",
                "acceptance-criteria-defined": "pass",
                "acceptance-criteria-met": "pass",
                "failure-modes-tested": "pass",
                "limitations-stated": "pass",
            },
            "nextEvidence": "Fresh evaluation",
            "stopRule": "Stop if threshold fails",
        }

    def test_complete_required_gate_passes(self):
        result = evaluate(self.base_record(), self.gates)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["gateVersion"], "1.0")
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

    def test_producer_identity_does_not_change_gate(self):
        ai_record = self.base_record()
        human_record = self.base_record()
        human_record["actors"] = [{"type": "human", "role": "Author"}]
        self.assertEqual(evaluate(ai_record, self.gates)["status"], evaluate(human_record, self.gates)["status"])


if __name__ == "__main__":
    unittest.main()
