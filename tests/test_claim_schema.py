from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


class ClaimSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "schemas" / "v1" / "claim.schema.json").read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def assert_valid_claim(self, path: Path):
        record = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(self.validator.iter_errors(record), key=lambda error: list(error.path))
        self.assertFalse(
            errors,
            f"{path.relative_to(ROOT)} failed claim.schema.json:\n"
            + "\n".join(f"- {'/'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors),
        )

    def test_example_claim_is_schema_valid(self):
        self.assert_valid_claim(ROOT / "toolkit" / "claim.example.json")

    def test_private_workbook_claim_is_schema_valid(self):
        self.assert_valid_claim(ROOT / "toolkit" / "private-workbook" / "claim.json")

    def test_all_teaching_samples_are_schema_valid(self):
        samples = sorted((ROOT / "toolkit" / "samples").glob("*.claim.json"))
        self.assertGreaterEqual(len(samples), 4)
        for path in samples:
            with self.subTest(path=path.name):
                self.assert_valid_claim(path)


if __name__ == "__main__":
    unittest.main()
