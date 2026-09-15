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

    def test_claim_gate_accepts_agent_and_file_handoffs(self):
        source = (ROOT / "web" / "src" / "components" / "claim-gate-app.tsx").read_text(encoding="utf-8")
        self.assertIn('window.addEventListener("aiov:load-claim-record"', source)
        self.assertIn("Import claim.json", source)
        self.assertIn("Copy claim.json", source)
        self.assertIn("aiov_evaluate_claim_record", source)
        self.assertIn("aiov_load_claim_gate_record", source)

    def test_claim_gate_handoff_does_not_claim_server_mutation(self):
        source = (ROOT / "webmcp.js").read_text(encoding="utf-8")
        self.assertIn("does not write to a server, publication, review record, or GitHub", source)


if __name__ == "__main__":
    unittest.main()
