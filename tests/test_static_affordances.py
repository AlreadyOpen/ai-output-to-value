from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fix_article_open_links import fix_article  # noqa: E402


class StaticAffordanceTests(unittest.TestCase):
    def test_article_provider_sources_do_not_use_dead_hash_fallbacks(self):
        react = (ROOT / "web" / "src" / "components" / "article-tools.tsx").read_text(encoding="utf-8")
        legacy = (ROOT / "article-tools.js").read_text(encoding="utf-8")
        self.assertNotIn('return "#"', react)
        self.assertNotIn('return "#"', legacy)
        self.assertIn('hints: "search", q: prompt', react)
        self.assertIn('https://copilot.microsoft.com/', react)
        self.assertIn('https://cursor.com/link/prompt', react)

    def test_generated_article_markup_contains_real_provider_urls(self):
        source = '''<div data-article-tools data-md-path="../md/start-here.md">
<a href="#" data-open-provider="chatgpt">ChatGPT</a>
<a href="#" data-open-provider="claude">Claude</a>
<a href="#" data-open-provider="t3">T3 Chat</a>
<a href="#" data-open-provider="copilot"><span>GitHub Copilot</span></a>
<a href="#" data-open-provider="cursor">Cursor</a>
<a href="../md/start-here.md" data-open-markdown role="menuitem" target="_blank" rel="noopener">Open Markdown</a>
</div>'''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "article.html"
            path.write_text(source, encoding="utf-8")
            fix_article(path)
            rendered = path.read_text(encoding="utf-8")

        self.assertNotIn('href="#" data-open-provider', rendered)
        self.assertIn('https://chatgpt.com/?', rendered)
        self.assertIn('hints=search&amp;q=Read+', rendered)
        self.assertIn('https://claude.ai/new?', rendered)
        self.assertIn('https://t3.chat/new?', rendered)
        self.assertIn('https://copilot.microsoft.com/?', rendered)
        self.assertIn('https://cursor.com/link/prompt?', rendered)
        self.assertIn('<span>Copilot</span>', rendered)
        self.assertNotIn('data-open-markdown', rendered)

    def test_publication_postprocessor_uses_better_auth_prompt_contract(self):
        source = (ROOT / "scripts" / "fix_article_open_links.py").read_text(encoding="utf-8")
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
