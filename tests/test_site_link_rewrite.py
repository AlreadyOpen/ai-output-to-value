from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_site  # noqa: E402


class SiteLinkRewriteTests(unittest.TestCase):
    source = REPO_ROOT / "content" / "claim-card.md"

    def rewrite(self, href: str) -> str:
        return build_site.rewrite_links(f'<a href="{href}">x</a>', {}, self.source)

    def test_links_to_published_files_stay_on_the_site(self):
        for href, expected in (
            ("../tools/claim-gate.html", "../tools/claim-gate.html"),
            ("../tools/claim-gate.html#samples", "../tools/claim-gate.html#samples"),
            ("../schemas/v1/claim.schema.json", "../schemas/v1/claim.schema.json"),
            ("../schemas/v1/decision-gates.json", "../schemas/v1/decision-gates.json"),
        ):
            with self.subTest(href=href):
                self.assertEqual(self.rewrite(href), f'<a href="{expected}">x</a>')

    def test_published_file_map_points_at_files_the_repo_has(self):
        for rel in build_site.PUBLISHED_FILES:
            with self.subTest(rel=rel):
                self.assertTrue((REPO_ROOT / rel).is_file())

    def test_unpublished_repository_files_still_link_to_source(self):
        result = self.rewrite("../toolkit/claim.example.json")
        self.assertIn("/blob/", result)
        self.assertIn("toolkit/claim.example.json", result)


if __name__ == "__main__":
    unittest.main()
