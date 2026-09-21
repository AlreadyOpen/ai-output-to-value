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


class CitationFileTests(unittest.TestCase):
    def setUp(self):
        self.citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))

    def test_citation_has_the_required_fields(self):
        for key in ("cff-version", "message", "title", "authors"):
            with self.subTest(key=key):
                self.assertIn(key, self.citation)

    def test_citation_licences_match_the_two_licence_files(self):
        self.assertEqual(set(self.citation["license"]), {"Apache-2.0", "CC-BY-4.0"})
        self.assertIn("Apache License", (ROOT / "LICENSE").read_text(encoding="utf-8"))
        self.assertIn("Attribution 4.0", (ROOT / "LICENSE-CONTENT").read_text(encoding="utf-8"))

    def test_citation_repository_matches_the_readme(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(self.citation["repository-code"].rstrip("/"), readme)


if __name__ == "__main__":
    unittest.main()
