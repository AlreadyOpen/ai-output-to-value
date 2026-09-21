from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import site_nav  # noqa: E402

PAGE = (
    '<header class="site-header"><nav class="nav" aria-label="Primary navigation"><a href="x.html">X</a></nav></header>'
    "<main>body</main>"
)


class SiteNavTests(unittest.TestCase):
    def test_every_local_nav_target_exists_in_the_repository_sources(self):
        sources = {
            "index.html": REPO_ROOT / "index.html",
            "tools/claim-gate.html": REPO_ROOT / "tools" / "claim-gate.html",
            "articles/claim-card.html": REPO_ROOT / "content" / "claim-card.md",
        }
        for label, path in site_nav.ITEMS:
            if path.startswith("http"):
                continue
            with self.subTest(label=label):
                self.assertIn(path.split("#")[0], {"index.html", "tools/claim-gate.html", "articles/claim-card.html", "articles/index.html", "evidence/index.html"})
        for name, source in sources.items():
            with self.subTest(source=name):
                self.assertTrue(source.is_file())

    def test_prefix_follows_page_depth(self):
        self.assertEqual(site_nav.prefix_for(0), "")
        self.assertEqual(site_nav.prefix_for(1), "../")

    def test_apply_replaces_the_primary_nav_and_adds_the_mobile_nav(self):
        result = site_nav.apply_navigation(PAGE, "../")
        self.assertIn(site_nav.primary("../"), result)
        self.assertIn(site_nav.mobile("../"), result)
        self.assertNotIn('href="x.html"', result)
        self.assertLess(result.index("</header>"), result.index('class="mobile-nav"'))

    def test_apply_is_idempotent_and_replaces_an_existing_mobile_nav(self):
        once = site_nav.apply_navigation(PAGE, "")
        self.assertEqual(site_nav.apply_navigation(once, ""), once)
        self.assertEqual(once.count('class="mobile-nav"'), 1)

    def test_apply_fails_loudly_instead_of_skipping_a_page(self):
        with self.assertRaises(ValueError):
            site_nav.apply_navigation("<header></header><main></main>", "")
        with self.assertRaises(ValueError):
            site_nav.apply_navigation(PAGE.replace("</header>", ""), "")

    def test_machine_access_points_at_the_mcp_package_not_a_missing_anchor(self):
        self.assertIn(f'<a href="{site_nav.MCP_URL}">AI access</a>', site_nav.primary(""))
        self.assertNotIn("#interfaces", site_nav.primary("") + site_nav.mobile(""))
        self.assertNotIn("#interfaces", (REPO_ROOT / "scripts" / "build_site.py").read_text(encoding="utf-8"))

    def test_mobile_nav_is_the_primary_nav_plus_home(self):
        self.assertEqual(site_nav.HOME, ("Home", "index.html"))
        primary_labels = [label for label, _ in site_nav.ITEMS]
        mobile_html = site_nav.mobile("")
        for label in primary_labels:
            with self.subTest(label=label):
                self.assertIn(f">{label}</a>", mobile_html)


if __name__ == "__main__":
    unittest.main()
