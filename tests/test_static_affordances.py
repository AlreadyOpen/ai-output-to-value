from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StaticAffordanceTests(unittest.TestCase):
    def test_article_provider_sources_do_not_use_dead_hash_fallbacks(self):
        react = (ROOT / "web" / "src" / "components" / "article-tools.tsx").read_text(encoding="utf-8")
        legacy = (ROOT / "article-tools.js").read_text(encoding="utf-8")
        self.assertNotIn('return "#"', react)
        self.assertNotIn('return "#"', legacy)
        self.assertIn('hints: "search", q: prompt', react)
        self.assertIn('https://copilot.microsoft.com/', react)
        self.assertIn('https://cursor.com/link/prompt', react)

    def test_publication_postprocessor_emits_static_provider_urls(self):
        source = (ROOT / "scripts" / "fix_article_open_links.py").read_text(encoding="utf-8")
        self.assertIn('https://chatgpt.com/?', source)
        self.assertIn('https://claude.ai/new?', source)
        self.assertIn('https://t3.chat/new?', source)
        self.assertIn('https://copilot.microsoft.com/?', source)
        self.assertIn('https://cursor.com/link/prompt?', source)
        self.assertIn('Read {md_url}, I want to ask questions about it.', source)

    def test_claim_gate_has_static_readable_fallback(self):
        source = (ROOT / "tools" / "claim-gate.html").read_text(encoding="utf-8")
        self.assertIn("Use the ladder as a stop rule, not a score.", source)
        self.assertIn("claim.schema.json", source)
        self.assertIn("decision-gates.json", source)
        self.assertIn("website-explore-pass.claim.json", source)
        self.assertIn("Gate ≠ truth.", source)


if __name__ == "__main__":
    unittest.main()
