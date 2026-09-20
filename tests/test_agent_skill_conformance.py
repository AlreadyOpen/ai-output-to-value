from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from claim_gate import evaluate  # noqa: E402


class AgentSkillConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_dir = REPO_ROOT / "toolkit" / "skills" / "applying-ai-output-to-value"
        cls.fixtures = json.loads((cls.skill_dir / "conformance" / "fixtures.json").read_text(encoding="utf-8"))
        cls.gates = json.loads((REPO_ROOT / "schemas" / "v1" / "decision-gates.json").read_text(encoding="utf-8"))
        cls.claim_schema = json.loads((REPO_ROOT / "schemas" / "v1" / "claim.schema.json").read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.claim_schema)

    def test_fixture_records_follow_canonical_gate_contract(self):
        ids: set[str] = set()
        for fixture in self.fixtures["fixtures"]:
            with self.subTest(fixture=fixture["id"]):
                self.assertNotIn(fixture["id"], ids)
                ids.add(fixture["id"])

                record = fixture["record"]
                self.validator.validate(record)

                expected = fixture["expected"]
                rule = self.gates["decisions"][record["targetDecision"]]
                self.assertEqual(record["requiredClaimLevel"], rule["requiredClaimLevel"])
                self.assertEqual(expected["requiredClaimLevel"], rule["requiredClaimLevel"])
                self.assertEqual(evaluate(record, self.gates)["status"], expected["gateStatus"])

                self.assertNotIn("overallRating", fixture)
                self.assertNotIn("overallRating", expected)
                self.assertNotIn("score", expected)

    def test_fixture_set_covers_required_interventions(self):
        tags = {tag for fixture in self.fixtures["fixtures"] for tag in fixture["tags"]}
        self.assertTrue({
            "adversarial-done",
            "adversarial-production-ready",
            "adversarial-roi",
            "output-sufficient",
            "review-vs-authority",
        }.issubset(tags))

    def test_output_only_fixture_stops_at_output(self):
        fixture = next(
            item for item in self.fixtures["fixtures"]
            if "output-sufficient" in item["tags"]
        )
        self.assertEqual(fixture["record"]["targetDecision"], "explore")
        self.assertEqual(fixture["expected"]["requiredClaimLevel"], "02-output")
        self.assertEqual(
            fixture["expected"]["supportedClaim"],
            "Output established; no higher claim is needed for this decision.",
        )

    def test_skill_contains_intervention_and_non_goals(self):
        skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "done / complete",
            "production ready",
            "ROI demonstrated",
            "What decision is actually being made?",
            "Weakest sufficient claim",
            "Never emit a project-wide ladder rating",
            "Review / assurance ≠ authority / sign-off",
            "Do not invent a human approval step",
            "Output established; no higher claim is needed for this decision.",
        ):
            self.assertIn(phrase, skill)

    def test_wrappers_defer_to_one_canonical_skill(self):
        wrapper_paths = (
            self.skill_dir / "wrappers" / "cursor.mdc",
            self.skill_dir / "wrappers" / "copilot-instructions.md",
            self.skill_dir / "wrappers" / "AGENTS.fragment.md",
        )
        for path in wrapper_paths:
            with self.subTest(wrapper=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn(".ai-output-to-value/SKILL.md", text)
                self.assertNotIn("01 Access", text)
                self.assertNotIn("02 Output", text)
                self.assertNotIn("03 Deliverable", text)
                self.assertNotIn("04 Operating capability", text)
                self.assertNotIn("05 Outcome", text)
                self.assertNotIn("06 Value", text)

    def test_legacy_agent_rules_is_only_a_compatibility_pointer(self):
        text = (REPO_ROOT / "toolkit" / "AGENT_RULES.md").read_text(encoding="utf-8")
        self.assertIn("canonical agent contract", text)
        self.assertIn("skills/applying-ai-output-to-value/SKILL.md", text)
        self.assertNotIn("01 Access", text)
        self.assertNotIn("02 Output", text)


if __name__ == "__main__":
    unittest.main()
