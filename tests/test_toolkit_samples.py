from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from claim_gate import evaluate  # noqa: E402


class ToolkitSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gates = json.loads((REPO_ROOT / "schemas" / "v1" / "decision-gates.json").read_text(encoding="utf-8"))
        cls.samples = REPO_ROOT / "toolkit" / "samples"

    def evaluate_sample(self, name: str) -> dict:
        record = json.loads((self.samples / name).read_text(encoding="utf-8"))
        return evaluate(record, self.gates)

    def test_website_explore_passes(self):
        self.assertEqual(self.evaluate_sample("website-explore-pass.claim.json")["status"], "PASS")

    def test_same_website_operate_blocks(self):
        result = self.evaluate_sample("website-operate-blocked.claim.json")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any(item["id"] == "deliverable-gate-passed" for item in result["failedChecks"]))

    def test_internal_tool_rely_passes(self):
        self.assertEqual(self.evaluate_sample("internal-tool-rely-pass.claim.json")["status"], "PASS")

    def test_killed_idea_outcome_passes(self):
        self.assertEqual(self.evaluate_sample("killed-idea-outcome-pass.claim.json")["status"], "PASS")

    def test_cross_domain_false_promotion_pack_statuses(self):
        expected = {
            "customer-support-outcome-insufficient.claim.json": "INSUFFICIENT_EVIDENCE",
            "report-factory-rely-blocked.claim.json": "BLOCKED",
            "system-of-record-operate-blocked.claim.json": "BLOCKED",
            "professional-deliverable-rely-insufficient.claim.json": "INSUFFICIENT_EVIDENCE",
            "coding-assistant-outcome-pass.claim.json": "PASS",
            "time-saved-value-insufficient.claim.json": "INSUFFICIENT_EVIDENCE",
            "killed-idea-outcome-pass.claim.json": "PASS",
        }

        observed = {}
        for name, status in expected.items():
            with self.subTest(name=name):
                observed[name] = self.evaluate_sample(name)["status"]
                self.assertEqual(observed[name], status)

        self.assertEqual(set(observed.values()), {"PASS", "BLOCKED", "INSUFFICIENT_EVIDENCE"})

    def test_cross_domain_pack_preserves_key_claim_boundaries(self):
        report = json.loads((self.samples / "report-factory-rely-blocked.claim.json").read_text(encoding="utf-8"))
        self.assertEqual(report["assertedClaimLevel"], "02-output")
        self.assertEqual(report["requiredClaimLevel"], "03-deliverable")
        report_result = self.evaluate_sample("report-factory-rely-blocked.claim.json")
        self.assertTrue(any(item["id"] == "acceptance-criteria-met" for item in report_result["failedChecks"]))

        time_saved = json.loads((self.samples / "time-saved-value-insufficient.claim.json").read_text(encoding="utf-8"))
        self.assertEqual(time_saved["assertedClaimLevel"], "05-outcome")
        self.assertEqual(time_saved["requiredClaimLevel"], "06-value")

        professional = json.loads((self.samples / "professional-deliverable-rely-insufficient.claim.json").read_text(encoding="utf-8"))
        self.assertIn("does not establish", professional["authority"].lower())
        self.assertEqual(self.evaluate_sample("professional-deliverable-rely-insufficient.claim.json")["status"], "INSUFFICIENT_EVIDENCE")

        killed = json.loads((self.samples / "killed-idea-outcome-pass.claim.json").read_text(encoding="utf-8"))
        self.assertEqual(killed["requiredClaimLevel"], "05-outcome")
        self.assertEqual(self.evaluate_sample("killed-idea-outcome-pass.claim.json")["status"], "PASS")

    def test_software_outcome_pack_is_a_plan_not_a_pass_record(self):
        pack = json.loads((REPO_ROOT / "toolkit" / "templates" / "software-outcome-pack.json").read_text(encoding="utf-8"))
        self.assertEqual(pack["targetDecision"], "measure-outcome")
        self.assertIn("change lead time", pack["throughputMetrics"])
        self.assertIn("deployment rework rate", pack["instabilityMetrics"])
        self.assertNotIn("gateChecks", pack)

    def test_private_workbook_contains_core_files(self):
        workbook = REPO_ROOT / "toolkit" / "private-workbook"
        for relative in ("README.md", "decision.md", "claim.json", "evidence/README.md"):
            self.assertTrue((workbook / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
