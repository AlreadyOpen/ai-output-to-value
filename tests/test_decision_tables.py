from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = json.loads((ROOT / "schemas" / "v1" / "decision-gates.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "schemas" / "v1" / "claim.schema.json").read_text(encoding="utf-8"))

# One phrase per decision that every human-readable decision table must carry.
TABLE_PHRASES = {
    "access": "access to try it",
    "explore": "keep exploring",
}
DECISION_TABLES = (
    "README.md",
    "content/claim-card.md",
    "content/meeting-brief.md",
    "index.html",
    "tools/claim-gate.html",
    "toolkit/skills/applying-ai-output-to-value/SKILL.md",
    ".github/pull_request_template.md",
)
SENTENCE = "An Access decision only justifies trying the tool."


class DecisionTableTests(unittest.TestCase):
    def test_schema_enums_match_the_gate_rules(self):
        decisions = list(GATES["decisions"])
        self.assertEqual(SCHEMA["properties"]["targetDecision"]["enum"], decisions)
        levels = [rule["requiredClaimLevel"] for rule in GATES["decisions"].values()]
        self.assertEqual(SCHEMA["properties"]["requiredClaimLevel"]["enum"], levels)

    def test_the_two_schema_copies_are_identical(self):
        for name in ("claim.schema.json", "decision-gates.json"):
            with self.subTest(name=name):
                self.assertEqual(
                    (ROOT / "schemas" / "v1" / name).read_bytes(),
                    (ROOT / "packages" / "mcp" / "schemas" / "v1" / name).read_bytes(),
                )

    def test_every_decision_table_lists_access_and_exploring(self):
        for path in DECISION_TABLES:
            text = (ROOT / path).read_text(encoding="utf-8").lower()
            for decision, phrase in TABLE_PHRASES.items():
                with self.subTest(table=path, decision=decision):
                    self.assertTrue(phrase in text, f"{path} has no decision-table entry containing {phrase!r}")

    def test_the_access_boundary_sentence_sits_under_the_decision_tables(self):
        for path in ("content/claim-card.md", "content/meeting-brief.md", "index.html", "tools/claim-gate.html"):
            with self.subTest(table=path):
                self.assertTrue(SENTENCE in (ROOT / path).read_text(encoding="utf-8"), f"{path} lacks the Access boundary sentence")

    def test_access_requires_the_access_claim_and_no_more(self):
        rule = GATES["decisions"]["access"]
        self.assertEqual(rule["requiredClaimLevel"], "01-access")
        self.assertEqual([check["id"] for check in rule["requiredChecks"]], ["tool-identified", "available-to-users", "trial-use-permitted"])


if __name__ == "__main__":
    unittest.main()
