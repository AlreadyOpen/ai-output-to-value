#!/usr/bin/env python3
"""Replace article-toolbar JS placeholders with real static provider links.

The generated HTML must remain meaningful to crawlers and no-JS readers. The
React toolbar enhances this markup, but it must not be responsible for turning
`href="#"` placeholders into functioning links.
"""
from __future__ import annotations

import html
import os
import re
from pathlib import Path
from urllib.parse import urlencode, urljoin

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SITE_URL = os.environ.get(
    "PUBLICATION_SITE_URL",
    "https://alreadyopen.github.io/ai-output-to-value/",
).rstrip("/") + "/"

PROVIDER_RE = re.compile(
    r'<a href="[^"]*" data-open-provider="(?P<provider>chatgpt|claude|t3|copilot|cursor)"'
)
OPEN_MARKDOWN_RE = re.compile(
    r'\n?<a href="[^"]*" data-open-markdown role="menuitem" target="_blank" rel="noopener">.*?</a>',
    re.DOTALL,
)
MD_PATH_RE = re.compile(r'data-md-path="\.\./md/(?P<slug>[a-z0-9-]+)\.md"')


def provider_url(provider: str, md_url: str) -> str:
    prompt = f"Read {md_url}, I want to ask questions about it."
    if provider == "chatgpt":
        return "https://chatgpt.com/?" + urlencode({"hints": "search", "q": prompt})
    if provider == "claude":
        return "https://claude.ai/new?" + urlencode({"q": prompt})
    if provider == "t3":
        return "https://t3.chat/new?" + urlencode({"q": prompt})
    if provider == "copilot":
        return "https://copilot.microsoft.com/?" + urlencode({"q": prompt})
    if provider == "cursor":
        return "https://cursor.com/link/prompt?" + urlencode({"text": prompt})
    raise ValueError(f"Unknown provider: {provider}")


def fix_article(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = MD_PATH_RE.search(text)
    if not match:
        return

    md_url = urljoin(SITE_URL, f"md/{match.group('slug')}.md")

    def replace_provider(match: re.Match[str]) -> str:
        url = html.escape(provider_url(match.group("provider"), md_url), quote=True)
        return f'<a href="{url}" data-open-provider="{match.group("provider")}"'

    text = PROVIDER_RE.sub(replace_provider, text)
    text = OPEN_MARKDOWN_RE.sub("", text)
    text = text.replace("<span>GitHub Copilot</span>", "<span>Copilot</span>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    article_dir = SITE / "articles"
    if not article_dir.exists():
        raise SystemExit("site/articles does not exist; build the publication first")

    count = 0
    for path in article_dir.glob("*.html"):
        before = path.read_text(encoding="utf-8")
        fix_article(path)
        after = path.read_text(encoding="utf-8")
        if before != after:
            count += 1

    print(f"Emitted static open-in provider links for {count} article page(s)")


if __name__ == "__main__":
    main()
