from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_site_links.py"


class SiteLinkCheckTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name)
        (self.root / "site" / "articles").mkdir(parents=True)
        (self.root / "site" / "index.html").write_text(
            '<main id="main"><a href="articles/guide.html#section">Guide</a></main>',
            encoding="utf-8",
        )
        (self.root / "site" / "articles" / "guide.html").write_text(
            '<main id="main"><h2 id="section">Section</h2><a href="/index.html">Home</a></main>',
            encoding="utf-8",
        )

    def tearDown(self):
        self._temp.cleanup()

    def run_checker(self):
        env = os.environ.copy()
        env["PUBLICATION_ROOT"] = str(self.root)
        return subprocess.run([sys.executable, str(CHECKER)], text=True, capture_output=True, env=env)

    def test_valid_generated_site_passes(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_broken_generated_site_link_fails(self):
        (self.root / "site" / "index.html").write_text(
            '<a href="articles/missing.html">Missing</a>', encoding="utf-8"
        )
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("broken generated-site href", result.stdout + result.stderr)

    def test_missing_fragment_fails(self):
        (self.root / "site" / "index.html").write_text(
            '<a href="articles/guide.html#missing">Missing fragment</a>', encoding="utf-8"
        )
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing fragment target", result.stdout + result.stderr)

    def test_dead_hash_link_fails(self):
        (self.root / "site" / "index.html").write_text('<a href="#">Looks active</a>', encoding="utf-8")
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dead placeholder link", result.stdout + result.stderr)

    def test_missing_local_script_fails(self):
        (self.root / "site" / "index.html").write_text('<script src="missing.js"></script>', encoding="utf-8")
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("broken generated-site src", result.stdout + result.stderr)

    def test_static_article_copy_control_fails(self):
        (self.root / "site" / "articles" / "guide.html").write_text(
            '<div data-article-tools><button data-copy-md>Copy MD</button></div>', encoding="utf-8"
        )
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("JS-only Copy MD control", result.stdout + result.stderr)

    def test_obsolete_ui_asset_fails(self):
        (self.root / "site" / "article-tools.js").write_text("legacy", encoding="utf-8")
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("obsolete UI implementation", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
