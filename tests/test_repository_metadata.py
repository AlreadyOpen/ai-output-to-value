from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class SecurityPolicyTests(unittest.TestCase):
    def test_security_policy_links_to_existing_correction_template(self):
        text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        match = re.search(r"issues/new\?template=([\w.-]+)", text)
        self.assertIsNotNone(match, "SECURITY.md should send factual corrections to the issue template")
        self.assertTrue((ROOT / ".github" / "ISSUE_TEMPLATE" / match.group(1)).is_file())

    def test_security_policy_reports_privately(self):
        text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("security/advisories/new", text)
        self.assertIn("privately", text)


if __name__ == "__main__":
    unittest.main()
