from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_publication.py"


class PublicationCheckTests(unittest.TestCase):
    def make_fixture(self) -> Path:
        root = Path(self._temp.name)
        for path in [root / "data", root / "content", root / "site" / "articles", root / "site" / "evidence"]:
            path.mkdir(parents=True, exist_ok=True)
        (root / "README.md").write_text("# Repository only\n", encoding="utf-8")
        (root / "content" / "article.md").write_text("# Article\n\n## Section\n\nEvidence statement.\n", encoding="utf-8")
        source = {"sources": [{
            "id": "source-1", "title": "Source", "publisher": "Publisher",
            "url": "https://example.com/source", "evidence_type": "test",
            "supports": ["claim"], "scope": "Fixture scope",
            "limitations": "Fixture limitations", "reviewed": "2026-09-14",
        }]}
        claim = {"claims": [{
            "id": "claim-1", "claim_text": "Evidence statement.", "status": "supported",
            "evidence": [{"source_id": "source-1", "locator": "Section 1",
                          "relevant_finding": "Finding", "qualification": "Qualification"}],
            "published_in": [{"file": "content/article.md", "locator": "## Section"}],
            "reviewer": "Independent review process", "reviewed": "2026-09-14", "independent_review_status": "completed",
        }]}
        articles = {"articles": [{
            "id": "article", "title": "Article", "source": "content/article.md",
            "slug": "article", "section": "core", "order": 1, "summary": "Summary",
            "maintainer": "Maintainer", "reviewed": "2026-09-14", "status": "ready",
        }]}
        self.write_yaml(root / "data" / "sources.yml", source)
        self.write_yaml(root / "data" / "claims.yml", claim)
        self.write_yaml(root / "data" / "articles.yml", articles)
        (root / "site" / "index.html").write_text("<main id='main'>Home</main>", encoding="utf-8")
        (root / "site" / "articles" / "index.html").write_text("<main id='main'>Index</main>", encoding="utf-8")
        (root / "site" / "articles" / "article.html").write_text("<main id='main'><h2 id='section'>Section</h2></main>", encoding="utf-8")
        (root / "site" / "evidence" / "index.html").write_text("<main id='main'>Evidence</main>", encoding="utf-8")
        return root

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.root = self.make_fixture()

    def tearDown(self):
        self._temp.cleanup()

    @staticmethod
    def write_yaml(path: Path, data) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def read_yaml(self, name: str):
        return yaml.safe_load((self.root / "data" / name).read_text(encoding="utf-8"))

    def run_checker(self):
        env = os.environ.copy(); env["PUBLICATION_ROOT"] = str(self.root)
        return subprocess.run([sys.executable, str(CHECKER)], text=True, capture_output=True, env=env)

    def assert_fails_with(self, text: str):
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(text, result.stderr + result.stdout)

    def test_valid_fixture_passes(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_empty_evidence_fields_fail(self):
        data = self.read_yaml("claims.yml")
        ev = data["claims"][0]["evidence"][0]
        ev["locator"] = ev["relevant_finding"] = ev["qualification"] = ""
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("field 'locator' must be non-empty")

    def test_completed_review_requires_reviewer_and_date(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["reviewer"] = ""
        data["claims"][0]["reviewed"] = ""
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("completed independent review requires reviewer and reviewed date")

    def test_missing_publication_locator_fails(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["published_in"][0]["locator"] = "## Does not exist"
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("locator was not found")

    def test_missing_html_fragment_fails(self):
        (self.root / "site" / "articles" / "index.html").write_text('<a href="article.html#missing">Broken</a>', encoding="utf-8")
        self.assert_fails_with("missing fragment target")

    def test_built_link_cannot_escape_deployment_root(self):
        (self.root / "site" / "articles" / "article.html").write_text('<a href="../../README.md">Repository file</a>', encoding="utf-8")
        self.assert_fails_with("built link escapes deployment root")

    def test_reserved_index_slug_fails(self):
        data = self.read_yaml("articles.yml")
        data["articles"][0]["slug"] = "index"
        self.write_yaml(self.root / "data" / "articles.yml", data)
        self.assert_fails_with("reserved article slug: index")

    def test_additional_canonical_source_registry_is_valid(self):
        data = self.read_yaml("sources.yml")
        extra = data["sources"].pop()
        self.write_yaml(self.root / "data" / "sources.yml", data)
        self.write_yaml(self.root / "data" / "sources-extra.yml", {"sources": [extra]})
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
