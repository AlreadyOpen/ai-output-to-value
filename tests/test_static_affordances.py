from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fix_article_open_links import fix_article  # noqa: E402


class StaticAffordanceTests(unittest.TestCase):
    def test_react_article_provider_urls_match_real_provider_contracts(self):
        react = (ROOT / "web" / "src" / "components" / "article-tools.tsx").read_text(encoding="utf-8")
        self.assertNotIn('return "#"', react)
        self.assertIn('hints: "search", q: prompt', react)
        self.assertIn('https://copilot.microsoft.com/', react)
        self.assertIn('https://cursor.com/link/prompt', react)

    def test_generated_article_markup_contains_only_working_static_affordances(self):
        source = '''<div data-article-tools data-md-path="../md/start-here.md">
<button class="article-tool-button" type="button" data-copy-md aria-label="Copy this article as Markdown">Copy MD</button>
<details><summary>Open in</summary><div>
<button type="button" data-copy-md-link role="menuitem">Copy MD link</button>
<a href="#" data-open-provider="chatgpt">ChatGPT</a>
<a href="#" data-open-provider="claude">Claude</a>
<a href="#" data-open-provider="t3">T3 Chat</a>
<a href="#" data-open-provider="copilot"><span>GitHub Copilot</span></a>
<a href="#" data-open-provider="cursor">Cursor</a>
<a href="../md/start-here.md" data-open-markdown role="menuitem" target="_blank" rel="noopener">Open Markdown</a>
</div></details></div>'''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "article.html"
            path.write_text(source, encoding="utf-8")
            fix_article(path)
            rendered = path.read_text(encoding="utf-8")

        self.assertNotIn('href="#" data-open-provider', rendered)
        self.assertNotIn("<button", rendered)
        self.assertNotIn("data-copy-md", rendered)
        self.assertNotIn("data-copy-md-link", rendered)
        self.assertNotIn("data-open-markdown", rendered)
        self.assertIn('> View Markdown</a>', rendered)
        self.assertIn('https://chatgpt.com/?', rendered)
        self.assertIn('hints=search&amp;q=Read+', rendered)
        self.assertIn('https://claude.ai/new?', rendered)
        self.assertIn('https://t3.chat/new?', rendered)
        self.assertIn('https://copilot.microsoft.com/?', rendered)
        self.assertIn('https://cursor.com/link/prompt?', rendered)
        self.assertIn('<span>Copilot</span>', rendered)

    def test_publication_postprocessor_uses_better_auth_prompt_contract(self):
        source = (ROOT / "scripts" / "fix_article_open_links.py").read_text(encoding="utf-8")
        self.assertIn('Read {md_url}, I want to ask questions about it.', source)
        self.assertIn("static HTML must", source)
        self.assertIn("not expose controls whose interaction only exists after JavaScript executes", source)

    def test_claim_gate_has_static_readable_fallback(self):
        source = (ROOT / "tools" / "claim-gate.html").read_text(encoding="utf-8")
        self.assertIn("Use the ladder as a stop rule, not a score.", source)
        self.assertIn("claim.schema.json", source)
        self.assertIn("decision-gates.json", source)
        self.assertIn("website-explore-pass.claim.json", source)
        self.assertIn("Gate ≠ truth.", source)

    def test_homepage_prioritizes_the_human_decision_kit(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        hero = source.split('<section class="hero"', 1)[1].split("</section>", 1)[0]
        self.assertIn("Run the eight questions", hero)
        self.assertIn("Open / print the Claim Card", hero)
        self.assertIn("printable meeting brief", hero)
        self.assertIn("optional structured record", hero)
        self.assertLess(hero.index("Run the eight questions"), hero.index("interactive Claim Gate"))

    def test_start_here_runs_the_human_kit_before_the_taxonomy(self):
        source = (ROOT / "START-HERE.md").read_text(encoding="utf-8")
        self.assertIn("## Run the 15-minute decision discussion", source)
        self.assertIn("Decision → eight questions → Claim Card / printable brief → evidence → optional structured record", source)
        self.assertLess(
            source.index("## Run the 15-minute decision discussion"),
            source.index("## Six different claims, not six mandatory steps"),
        )
        self.assertIn("not the conceptual front door", source)

    def test_claim_gate_static_fallback_sends_first_meetings_to_the_human_kit(self):
        source = (ROOT / "tools" / "claim-gate.html").read_text(encoding="utf-8")
        first_meeting = source.index("Starting a first meeting?")
        machine_contract = source.index("Optional machine-readable contract")
        self.assertLess(first_meeting, machine_contract)
        self.assertIn("../index.html#questions", source)
        self.assertIn("../articles/claim-card.html", source)
        self.assertIn("../downloads/ai-output-to-value-meeting-brief.pdf", source)

    def test_homepage_builder_does_not_promote_webmcp_into_primary_navigation(self):
        source = (ROOT / "scripts" / "build_site.py").read_text(encoding="utf-8")
        self.assertIn("progressive enhancement", source)
        self.assertNotIn('<a href="#interfaces">AI access</a>', source)


if __name__ == "__main__":
    unittest.main()
