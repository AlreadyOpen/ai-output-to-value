from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from publish_failure_modes import order_modes  # noqa: E402


class FailureModeCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = yaml.safe_load((REPO_ROOT / "data" / "failure-modes.yml").read_text(encoding="utf-8"))
        cls.sources = yaml.safe_load((REPO_ROOT / "data" / "sources-software-failure-modes.yml").read_text(encoding="utf-8"))

    def test_catalogue_has_unique_ids_and_required_fields(self):
        required = {
            "id",
            "title",
            "category",
            "substance_layer",
            "earliest_claim_at_risk",
            "signal",
            "why_output_can_pass",
            "deliverable_evidence",
            "capability_evidence",
            "verification_patterns",
            "references",
        }
        modes = self.catalogue.get("failure_modes", [])
        self.assertGreaterEqual(len(modes), 10)
        ids = []
        for mode in modes:
            self.assertTrue(required.issubset(mode.keys()), mode.get("id"))
            self.assertIn(mode["earliest_claim_at_risk"], {"03-deliverable", "04-capability"})
            self.assertIn(mode["substance_layer"], {"tool-capability", "job-substance", "delivery-capability"})
            self.assertIsInstance(mode["deliverable_evidence"], list)
            self.assertIsInstance(mode["capability_evidence"], list)
            self.assertIsInstance(mode["verification_patterns"], list)
            ids.append(mode["id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_reference_ids_resolve(self):
        source_ids = {item["id"] for item in self.sources.get("sources", [])}
        for mode in self.catalogue.get("failure_modes", []):
            for reference in mode.get("references", []):
                self.assertIn(reference, source_ids, f"{mode['id']} references unknown source {reference}")

    def test_catalogue_is_explicitly_not_a_prevalence_ranking(self):
        scope = str(self.catalogue.get("scope", "")).lower()
        self.assertIn("not a prevalence ranking", scope)

    def test_public_order_is_alphanumeric_by_title(self):
        modes = self.catalogue.get("failure_modes", [])
        ordered = order_modes(modes)
        titles = [str(mode["title"]) for mode in ordered]
        self.assertEqual(titles, sorted(titles, key=str.casefold))


if __name__ == "__main__":
    unittest.main()
