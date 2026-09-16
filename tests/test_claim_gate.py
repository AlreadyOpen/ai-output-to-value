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

    def test_missing_required_text_is_insufficient_not_blocked(self):
        record = self.base_record()
        record["authority"] = ""
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(result["missingFields"], ["authority"])

    def test_missing_actor_is_insufficient_not_silently_inferred(self):
        record = self.base_record()
        record["actors"] = []
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "INSUFFICIENT_EVIDENCE")
        self.assertIn("actors", result["missingFields"])

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
        self.assertIn("requiredClaimLevel must be", " ".join(result["structuralErrors"]))

    def test_unsupported_schema_version_blocks(self):
        record = self.base_record()
        record["schemaVersion"] = "2.0"
        result = evaluate(record, self.gates)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("schemaVersion" in error for error in result["structuralErrors"]))

    def test_producer_identity_does_not_change_gate(self):
        ai_record = self.base_record()
        human_record = self.base_record()
        human_record["actors"] = [{"type": "human", "role": "Author"}]
        self.assertEqual(evaluate(ai_record, self.gates)["status"], evaluate(human_record, self.gates)["status"])


if __name__ == "__main__":
    unittest.main()
