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

    def test_software_outcome_pack_is_a_plan_not_a_pass_record(self):
        pack = json.loads((REPO_ROOT / "toolkit" / "templates" / "software-outcome-pack.json").read_text(encoding="utf-8"))
        self.assertEqual(pack["targetDecision"], "measure-outcome")
        self.assertIn("change lead time", pack["throughputMetrics"])
        self.assertIn("deployment rework rate", pack["instabilityMetrics"])
        self.assertNotIn("gateChecks", pack)

    def test_outcome_and_value_instruments_cover_decision_boundaries(self):
        outcome = (REPO_ROOT / "toolkit" / "templates" / "outcome-worksheet.md").read_text(encoding="utf-8")
        value = (REPO_ROOT / "toolkit" / "value-cost-ledger.md").read_text(encoding="utf-8")

        for phrase in (
            "Decision / intervention being assessed",
            "Baseline and comparison",
            "Elapsed time",
            "Labour hours",
            "Material confounders",
            "Adverse effects / quality regressions",
            "Attribution strength / qualification",
            "Result that would reverse",
            "Outcome without Value",
        ):
            with self.subTest(instrument="outcome", phrase=phrase):
                self.assertIn(phrase, outcome)

        for phrase in (
            "Labour displaced / removed",
            "Labour moved into review / checking",
            "Model / API / tool / vendor cost",
            "Infrastructure",
            "Testing / evaluation / assurance / security",
            "Incident / error / risk cost",
            "Opportunity cost / alternative not taken",
            "Option value of information",
            "positive option value from stopping a bad idea",
            "Attribution qualification",
        ):
            with self.subTest(instrument="value", phrase=phrase):
                self.assertIn(phrase, value)

    def test_private_workbook_contains_core_files(self):
        workbook = REPO_ROOT / "toolkit" / "private-workbook"
        for relative in ("README.md", "decision.md", "claim.json", "evidence/README.md"):
            self.assertTrue((workbook / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
