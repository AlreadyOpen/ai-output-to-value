from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_release.py"


class ReleaseCheckTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name)
        (self.root / "data").mkdir(parents=True)
        (self.root / "site" / "articles").mkdir(parents=True)
        self.write_valid_fixture()

    def tearDown(self):
        self._temp.cleanup()

    @staticmethod
    def write_yaml(path: Path, data) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def write_valid_fixture(self) -> None:
        self.write_yaml(self.root / "data" / "claims.yml", {"claims": [{
            "id": "critical-claim",
            "launch_critical": True,
            "published_in": [{"file": "content/guide.md", "locator": "Claim"}],
            "independent_review_status": "completed",
            "reviewer": "Independent review process",
            "reviewed": "2026-09-14",
            "review_record": {
                "claim_revision": "abc123",
                "source_versions_checked": ["source-v1"],
                "method": "Direct source inspection and qualification check.",
                "finding": "Claim follows within stated scope.",
                "disposition": "accepted_with_qualification",
            },
        }]})
        self.write_yaml(self.root / "data" / "articles.yml", {"articles": [
            {"id": "guide", "slug": "guide", "source": "content/guide.md", "release_scope": "guide", "status": "ready"},
            {"id": "policy", "slug": "policy", "source": "content/policy.md", "release_scope": "policy", "status": "active_policy"},
            {"id": "working", "slug": "working", "source": "content/working.md", "release_scope": "working", "status": "draft"},
        ]})
        (self.root / "site" / "articles" / "guide.html").write_text("guide", encoding="utf-8")
        (self.root / "site" / "articles" / "policy.html").write_text("policy", encoding="utf-8")

    def read_yaml(self, name: str):
        return yaml.safe_load((self.root / "data" / name).read_text(encoding="utf-8"))

    def run_checker(self):
        env = os.environ.copy()
        env["PUBLICATION_ROOT"] = str(self.root)
        return subprocess.run([sys.executable, str(CHECKER)], text=True, capture_output=True, env=env)

    def assert_fails_with(self, text: str):
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(text, result.stdout + result.stderr)

    def test_valid_release_fixture_passes(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepted_disposition_passes(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["review_record"]["disposition"] = "accepted"
        self.write_yaml(self.root / "data" / "claims.yml", data)
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejected_disposition_is_blocked(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["review_record"]["disposition"] = "rejected"
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("review disposition does not accept claim")

    def test_pending_critical_claim_is_blocked(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["independent_review_status"] = "pending"
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("has not completed independent review")

    def test_release_published_claim_cannot_opt_out_of_review(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["launch_critical"] = False
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("release-published claim cannot opt out")

    def test_working_only_noncritical_claim_can_remain_exempt(self):
        data = self.read_yaml("claims.yml")
        claim = data["claims"][0]
        claim["launch_critical"] = False
        claim["published_in"] = [{"file": "content/working.md", "locator": "Claim"}]
        claim["independent_review_status"] = "pending"
        claim["reviewer"] = ""
        claim.pop("review_record")
        self.write_yaml(self.root / "data" / "claims.yml", data)
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_criticality_is_blocked(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0].pop("launch_critical")
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("lacks explicit Boolean launch_critical classification")

    def test_empty_container_reviewer_is_blocked(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["reviewer"] = []
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("lacks an inspectable reviewer/process")

    def test_invalid_review_date_is_blocked(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0]["reviewed"] = "not-a-date"
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("lacks an inspectable reviewer/process")

    def test_missing_review_record_is_blocked(self):
        data = self.read_yaml("claims.yml")
        data["claims"][0].pop("review_record")
        self.write_yaml(self.root / "data" / "claims.yml", data)
        self.assert_fails_with("lacks a complete independent review_record")

    def test_guide_article_must_be_ready(self):
        data = self.read_yaml("articles.yml")
        data["articles"][0]["status"] = "draft"
        self.write_yaml(self.root / "data" / "articles.yml", data)
        self.assert_fails_with("guide article is not marked ready")

    def test_working_article_must_not_enter_release_artifact(self):
        (self.root / "site" / "articles" / "working.html").write_text("working", encoding="utf-8")
        self.assert_fails_with("incorrectly includes working article")

    def test_approved_article_must_exist_in_release_artifact(self):
        (self.root / "site" / "articles" / "guide.html").unlink()
        self.assert_fails_with("release artifact is missing approved article")


if __name__ == "__main__":
    unittest.main()
