from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseReadinessBoundaryTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def section(self, text: str, heading: str) -> str:
        match = re.search(
            rf"^### {re.escape(heading)}\n(?P<body>.*?)(?=^### |^## |\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing tooling surface section: {heading}")
        return match.group("body")

    def test_reviewed_release_explicitly_separates_tool_distribution(self):
        release = self.read("docs/first-reviewed-release.md")
        self.assertIn("Tooling publication is not a prerequisite", release)
        self.assertIn("tooling-distribution.md", release)
        self.assertIn("publishing or tagging a tool does **not** mean", release)

        # Distribution milestones may be discussed for clarity, but they must not
        # silently become acceptance checkboxes for the reviewed method release.
        distribution_checkbox = re.compile(
            r"^- \[[ xX]\].*(?:npm|native MCP|WebMCP|GitHub Action|agent[- ]skill|wrapper)",
            re.IGNORECASE | re.MULTILINE,
        )
        self.assertIsNone(
            distribution_checkbox.search(release),
            "tool distribution milestone leaked into the reviewed-method checklist",
        )

    def test_tooling_roadmap_records_boundary_for_every_surface(self):
        roadmap = self.read("docs/tooling-distribution.md")
        self.assertIn("Issue #1 remains the umbrella publication milestone", roadmap)
        self.assertIn("## Two independent readiness claims", roadmap)
        self.assertIn("## Tooling/distribution milestone checklist", roadmap)

        surfaces = (
            "Deterministic Claim Gate CLI and contract",
            "GitHub Action",
            "Native MCP / optional npm distribution",
            "Browser WebMCP",
            "Web UI and PDF build package",
            "Agent skill and wrappers",
        )
        for surface in surfaces:
            with self.subTest(surface=surface):
                body = self.section(roadmap, surface)
                self.assertIn("**Version identity:**", body)
                self.assertIn("**Intended use:**", body)
                self.assertIn("**Support / compatibility boundary:**", body)

    def test_public_status_cannot_equate_tool_release_with_method_review(self):
        readme = self.read("README.md")
        self.assertIn("## Two release tracks", readme)
        self.assertIn("**Reviewed method/publication**", readme)
        self.assertIn("**Tooling/distribution**", readme)
        self.assertIn("published or tagged tool does **not** mean the method", readme)
        self.assertIn(
            "method review does not establish support for every tool surface",
            readme,
        )

    def test_mcp_readme_matches_package_version_and_support_boundary(self):
        readme = self.read("packages/mcp/README.md")
        package = json.loads(self.read("packages/mcp/package.json"))
        self.assertIn(f"source package version `{package['version']}`", readme)
        self.assertIn("**Intended use:**", readme)
        self.assertIn("**Support / compatibility boundary:**", readme)
        self.assertIn("../../docs/tooling-distribution.md", readme)

    def test_web_readme_matches_package_version_and_support_boundary(self):
        readme = self.read("web/README.md")
        package = json.loads(self.read("web/package.json"))
        self.assertIn(f"version `{package['version']}`", readme)
        self.assertIn("**Intended use:**", readme)
        self.assertIn("**Support / compatibility boundary:**", readme)
        self.assertIn("../docs/tooling-distribution.md", readme)


if __name__ == "__main__":
    unittest.main()
