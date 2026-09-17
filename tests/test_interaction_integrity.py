from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

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
        workflow = (ROOT / ".github" / "workflows" / "publication-gate.yml").read_text(encoding="utf-8")
        self.assertIn('python-version: "3.12"', source)
        self.assertIn("Validate reusable claim gate Action end to end", workflow)
        self.assertIn("uses: ./", workflow)

    def test_third_party_actions_are_pinned_to_commit_shas(self):
        """A version tag can be repointed at new code; a commit SHA cannot.

        This matters most for `action.yml`, which downstream repositories execute,
        but the same standard applies to this repository's own publication and
        release workflows. Local `./` references are the action under test.
        """
        sources = [ROOT / "action.yml", *sorted((ROOT / ".github" / "workflows").glob("*.yml"))]
        checked = 0
        for source in sources:
            for reference in re.findall(r"uses:\s*(\S+)", source.read_text(encoding="utf-8")):
                if reference.startswith((".", "/")):
                    continue
                checked += 1
                with self.subTest(source=source.name, reference=reference):
                    self.assertRegex(
                        reference,
                        r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$",
                        f"{source.name}: {reference} is not pinned to a commit SHA",
                    )
        self.assertGreater(checked, 0, "no third-party action references found")

    def test_reusable_action_exposes_gate_result_as_outputs(self):
        action = yaml.safe_load((ROOT / "action.yml").read_text(encoding="utf-8"))
        outputs = action.get("outputs") or {}
        for name in (
            "status",
            "target-decision",
            "decision-label",
            "required-claim-level",
            "asserted-claim-level",
            "claim-mismatch",
            "failed-check-count",
            "unknown-check-count",
            "passed-check-count",
            "result-json",
        ):
            with self.subTest(output=name):
                self.assertIn(name, outputs)
                self.assertIn("description", outputs[name])
                self.assertIn("steps.gate.outputs.", outputs[name]["value"])

        # A caller must be able to read a BLOCKED verdict, so the gate step has to
        # publish its outputs before the action decides whether to fail.
        self.assertIn("fail-on-block", action.get("inputs") or {})
        self.assertEqual(action["inputs"]["fail-on-block"]["default"], "true")

    def test_action_output_writer_resists_claim_record_injection(self):
        """A claim record is attacker-controlled in an adopter's pull request.

        GITHUB_OUTPUT is last-write-wins, so a record that can close the heredoc
        and append `status=PASS` turns a BLOCKED verdict green for any consumer
        branching on the output.
        """
        source = (ROOT / "action.yml").read_text(encoding="utf-8")
        self.assertIn("secrets.token_hex", source)
        self.assertNotIn('delim = "ghadelim_claim_gate"', source)
        self.assertIn("if delimiter in value:", source)
        # Single-line outputs are flattened, so a newline cannot start a new pair.
        self.assertIn("def scalar(value):", source)
        for output in ("status", "target-decision", "asserted-claim-level"):
            with self.subTest(output=output):
                self.assertIn(f'"{output}": scalar(', source)

    def test_action_sanitises_claim_controlled_label(self):
        """`targetDecision` is echoed verbatim when it matches no known decision.

        A newline in it would forge a `::error::` annotation or a Markdown heading
        in the job summary, because both are parsed only at the start of a line.
        """
        source = (ROOT / "action.yml").read_text(encoding="utf-8")
        self.assertIn(
            'label = scalar(result.get("decisionLabel") or result.get("targetDecision")',
            source,
        )
        self.assertIn('label.replace("`", "\'")', source)
        self.assertIn("- Decision: `{label}`", source)

    def test_action_fail_on_block_fails_closed(self):
        """Only an explicit 'false' may disable failure; a typo must not."""
        source = (ROOT / "action.yml").read_text(encoding="utf-8")
        self.assertIn('!= "false"', source)
        self.assertNotIn('== "true"', source)

    def test_workflows_do_not_interpolate_outputs_into_shell(self):
        """Step outputs carry claim-record text; pass them through env instead."""
        import yaml as _yaml

        for path in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
            document = _yaml.safe_load(path.read_text(encoding="utf-8"))
            for job in (document.get("jobs") or {}).values():
                for step in job.get("steps") or []:
                    script = step.get("run")
                    if not script:
                        continue
                    with self.subTest(workflow=path.name, step=step.get("name")):
                        self.assertNotIn(
                            "${{",
                            script,
                            f"{path.name}: '{step.get('name')}' interpolates an expression into the shell",
                        )

    def test_mcp_package_does_not_claim_unselected_public_licence(self):
        source = (ROOT / "packages" / "mcp" / "package.json").read_text(encoding="utf-8")
        self.assertIn('"private": true', source)
        self.assertIn('"license": "UNLICENSED"', source)

    def test_machine_framework_publishes_operating_capability_label(self):
        source = (ROOT / "scripts" / "augment_site.py").read_text(encoding="utf-8")
        self.assertIn('{"level": "04-capability", "name": "Operating capability"', source)

    def test_failure_mode_machine_links_follow_publication_scope(self):
        publisher = (ROOT / "scripts" / "publish_failure_modes.py").read_text(encoding="utf-8")
        refiner = (ROOT / "scripts" / "refine_webmcp_scope.py").read_text(encoding="utf-8")
        build = (ROOT / "scripts" / "build_publication.py").read_text(encoding="utf-8")
        mcp = (ROOT / "packages" / "mcp" / "src" / "index.mjs").read_text(encoding="utf-8")
        self.assertIn('"catalogueIncluded": included', publisher)
        self.assertIn('"catalogueUrl": "articles/software-failure-mode-catalogue.html" if included else None', publisher)
        self.assertIn("catalogue: payload.catalogueUrl ? siteUrl(payload.catalogueUrl) : null", refiner)
        self.assertIn("refine_webmcp_scope()", build)
        self.assertIn("catalogueUrl: payload.catalogueUrl ? new URL(payload.catalogueUrl, publicationUrl).href : null", mcp)


if __name__ == "__main__":
    unittest.main()
