from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InteractionIntegrityTests(unittest.TestCase):
    def test_legacy_ui_sources_are_explicit_placeholders_only(self):
        article_legacy = (ROOT / "article-tools.js").read_text(encoding="utf-8")
        gate_legacy = (ROOT / "tools" / "claim-gate.js").read_text(encoding="utf-8")
        self.assertIn("Do not add interaction logic here", article_legacy)
        self.assertIn("Do not add decision-gate logic here", gate_legacy)
        self.assertNotIn("addEventListener", article_legacy)
        self.assertNotIn("addEventListener", gate_legacy)

    def test_final_build_removes_legacy_ui_assets(self):
        source = (ROOT / "scripts" / "inject_web_ui.py").read_text(encoding="utf-8")
        self.assertIn('SITE / "article-tools.js"', source)
        self.assertIn('SITE / "tools" / "claim-gate.js"', source)
        self.assertIn("path.unlink()", source)

    def test_webmcp_claim_gate_handoff_is_acknowledged_not_assumed(self):
        source = (ROOT / "webmcp.js").read_text(encoding="utf-8")
        self.assertNotIn("loaded: true", source)
        self.assertIn("requestClaimGateHandoff", source)
        self.assertIn('window.addEventListener("aiov:claim-record-loaded"', source)
        self.assertIn("handoffRequested: true", source)
        self.assertIn("applicationConfirmed: false", source)
        self.assertIn("applicationConfirmed: true", source)
        self.assertIn("did not acknowledge the handoff before the timeout", source)

    def test_claim_gate_preserves_schema_evidence_state(self):
        source = (ROOT / "web" / "src" / "components" / "claim-gate-app.tsx").read_text(encoding="utf-8")
        self.assertIn('type CheckState = "unknown" | "pass" | "fail" | "not-applicable"', source)
        self.assertIn('value: "not-applicable"', source)
        self.assertIn('actor: "unselected"', source)
        self.assertIn('actors = state.actor === "unselected"', source)

    def test_software_outcome_pack_is_loaded_from_canonical_asset(self):
        source = (ROOT / "web" / "src" / "components" / "claim-gate-app.tsx").read_text(encoding="utf-8")
        self.assertIn('fetch("../templates/software-outcome-pack.json"', source)
        self.assertNotIn("DORA throughput: change lead time", source)

    def test_reusable_action_owns_its_python_dependency(self):
        source = (ROOT / "action.yml").read_text(encoding="utf-8")
        self.assertIn("uses: actions/setup-python@v5", source)
        self.assertIn('python-version: "3.12"', source)

    def test_mcp_package_does_not_claim_unselected_public_licence(self):
        source = (ROOT / "packages" / "mcp" / "package.json").read_text(encoding="utf-8")
        self.assertIn('"private": true', source)
        self.assertIn('"license": "UNLICENSED"', source)

    def test_machine_framework_publishes_operating_capability_label(self):
        source = (ROOT / "scripts" / "refine_agent_access.py").read_text(encoding="utf-8")
        self.assertIn('claim.get("level") == "04-capability"', source)
        self.assertIn('claim["name"] = "Operating capability"', source)


if __name__ == "__main__":
    unittest.main()
