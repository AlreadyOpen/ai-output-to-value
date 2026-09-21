from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AiHybridClaimGateTests(unittest.TestCase):
    def test_webmcp_exposes_claim_gate_evaluation_and_handoff(self):
        source = (ROOT / "webmcp.js").read_text(encoding="utf-8")
        self.assertIn('name: "aiov_evaluate_claim_record"', source)
        self.assertIn('name: "aiov_load_claim_gate_record"', source)
        self.assertIn('scope: "local-browser-form-only"', source)
        self.assertIn('new CustomEvent("aiov:load-claim-record"', source)

    def test_webmcp_delegates_evaluation_to_the_shared_gate(self):
        """The evaluator must not be copied back into webmcp.js (issue #8)."""
        source = (ROOT / "webmcp.js").read_text(encoding="utf-8")
        self.assertIn('import(siteUrl("ui/gate-core.js"))', source)
        self.assertIn("core.evaluateClaim(record, gates, claimSchema)", source)
        for copied in ("requiredTextFields", "REQUIRED_TEXT_FIELDS", "requiredClaimLevel must be", ".trim()) missingFields"):
            with self.subTest(copied=copied):
                self.assertNotIn(copied, source)

    def test_web_build_checks_the_gate_bundle_and_webmcp_against_the_fixture(self):
        import json

        scripts = json.loads((ROOT / "web" / "package.json").read_text(encoding="utf-8"))["scripts"]
        self.assertIn("check-gate-conformance.mjs", scripts["build"])
        self.assertIn("check-webmcp-conformance.mjs", scripts["build"])

    def test_claim_gate_accepts_agent_and_file_handoffs(self):
        source = (ROOT / "web" / "src" / "components" / "claim-gate-app.tsx").read_text(encoding="utf-8")
        self.assertIn('window.addEventListener("aiov:load-claim-record"', source)
        self.assertIn('new CustomEvent("aiov:claim-record-loaded"', source)
        self.assertIn('host.dataset.claimGateReady = "true"', source)
        self.assertIn("Import claim.json", source)
        self.assertIn("Copy claim.json", source)
        self.assertIn("Agent-prepared claim record", source)
        self.assertIn("Load software Outcome pack", source)
        self.assertIn("website-explore-pass.claim.json", source)
        self.assertIn("website-operate-blocked.claim.json", source)

    def test_claim_gate_does_not_hide_actor_or_evidence_defaults(self):
        source = (ROOT / "web" / "src" / "components" / "claim-gate-app.tsx").read_text(encoding="utf-8")
        self.assertIn('actor: "unselected"', source)
        self.assertIn('channel: "unselected"', source)
        self.assertIn('value: "not-applicable"', source)
        self.assertIn('value !== "pass" && value !== "fail"', source)
        self.assertNotIn('actor: "hybrid",\n      outcomeMeasure:', source)
        self.assertIn('fetch("../templates/software-outcome-pack.json"', source)
        self.assertIn("No actor was inferred", source)

    def test_webmcp_handoff_requires_mounted_ready_form_and_acknowledgement(self):
        source = (ROOT / "webmcp.js").read_text(encoding="utf-8")
        self.assertIn("does not write to a server, publication, review record, or GitHub", source)
        self.assertIn('host.dataset.claimGateReady !== "true"', source)
        self.assertIn('window.addEventListener("aiov:claim-record-loaded"', source)
        self.assertIn("requestId", source)
        self.assertIn("handoffRequested: true", source)
        self.assertIn("applicationConfirmed: false", source)
        self.assertIn("applicationConfirmed: true", source)
        self.assertNotIn("loaded: true", source)

    def test_meeting_guide_printable_link_targets_pdf(self):
        source = (ROOT / "webmcp.js").read_text(encoding="utf-8")
        self.assertIn('printable_brief: siteUrl("downloads/ai-output-to-value-meeting-brief.pdf")', source)
        self.assertIn('meeting_brief_article: siteUrl("articles/meeting-brief.html")', source)


if __name__ == "__main__":
    unittest.main()
