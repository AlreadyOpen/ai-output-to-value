#!/usr/bin/env python3
"""Build the static publication site from maintained Markdown/YAML sources.

The repository keeps editorial content in Markdown and evidence in YAML.
This script renders normal HTML pages into site/ without client-side JavaScript.
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REPO_URL = "https://github.com/helenkwok/ai-output-to-value"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def page_shell(title: str, body: str, *, source: str | None = None, meta: str = "") -> str:
    source_link = (
        f'<a href="{REPO_URL}/blob/main/{html.escape(source)}">View source</a>' if source else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="AI Output to Value — evidence-led guidance for business decisions about AI-assisted work.">
  <title>{html.escape(title)} — AI Output to Value</title>
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="../publication.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="shell header-inner">
      <a class="brand" href="../index.html"><span class="brand-mark" aria-hidden="true">O→V</span><span>AI Output to Value</span></a>
      <nav class="nav" aria-label="Primary navigation">
        <a href="index.html">Articles</a>
        <a href="../evidence/index.html">Evidence</a>
        <a href="{REPO_URL}">GitHub</a>
      </nav>
    </div>
  </header>
  <details class="mobile-nav">
    <summary>Menu</summary>
    <nav aria-label="Mobile navigation">
      <a href="../index.html">Home</a>
      <a href="index.html">Articles</a>
      <a href="../evidence/index.html">Evidence</a>
      <a href="{REPO_URL}">GitHub</a>
    </nav>
  </details>
  <main id="main" class="article-shell">
    <article class="article-body">
      <div class="article-meta">{meta}</div>
      {body}
    </article>
    <aside class="article-aside" aria-label="Article links">
      <strong>AI Output to Value</strong>
      <a href="../index.html">Home</a>
      <a href="index.html">All articles</a>
      <a href="../evidence/index.html">Evidence</a>
      {source_link}
      <a href="corrections.html">Report a correction</a>
    </aside>
  </main>
</body>
</html>
"""


def rewrite_internal_links(rendered: str, source_to_url: dict[str, str], source_path: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        path_part, sep, fragment = href.partition("#")
        if not path_part:
            return match.group(0)
        resolved = (source_path.parent / path_part).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        mapped = source_to_url.get(rel)
        if mapped:
            suffix = f"#{fragment}" if sep else ""
            return f'href="{mapped}{suffix}"'
        if rel.startswith("data/"):
            return f'href="{REPO_URL}/blob/main/{rel}"'
        return match.group(0)

    return re.sub(r'href="([^"]+)"', replace, rendered)


def render_articles() -> list[dict]:
    manifest = load_yaml(ROOT / "data" / "articles.yml")
    articles = sorted(manifest["articles"], key=lambda x: x.get("order", 9999))
    source_to_url = {item["source"]: f'{item["slug"]}.html' for item in articles}

    out = SITE / "articles"
    out.mkdir(parents=True, exist_ok=True)

    for item in articles:
        source_path = ROOT / item["source"]
        md = source_path.read_text(encoding="utf-8")
        body = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
        body = rewrite_internal_links(body, source_to_url, source_path)
        meta = (
            f'<span class="status-label">{html.escape(item.get("status", "draft"))}</span> '
            f'&nbsp; Maintained by {html.escape(item.get("maintainer", ""))} · '
            f'Reviewed {html.escape(str(item.get("reviewed", "")))}'
        )
        page = page_shell(item["title"], body, source=item["source"], meta=meta)
        (out / f'{item["slug"]}.html').write_text(page, encoding="utf-8")

    sections = [
        ("core", "Core reading"),
        ("deeper", "Deeper analysis"),
        ("advanced", "Advanced / agentic organisations"),
        ("policy", "Publication policy"),
    ]
    blocks = ["<h1>Articles</h1><p>Start with the core route. The deeper and advanced material supports the argument but is not required for the five-minute introduction.</p>"]
    for key, label in sections:
        selected = [a for a in articles if a.get("section") == key]
        if not selected:
            continue
        blocks.append(f"<h2>{html.escape(label)}</h2><div class=\"evidence-grid\">")
        for item in selected:
            blocks.append(
                f'<a class="source-card" href="{html.escape(item["slug"])}.html">'
                f'<span>{html.escape(item.get("status", "draft"))}</span>'
                f'<strong>{html.escape(item["title"])}</strong>'
                f'<p>{html.escape(item.get("summary", ""))}</p></a>'
            )
        blocks.append("</div>")
    (out / "index.html").write_text(page_shell("Articles", "".join(blocks)), encoding="utf-8")
    return articles


def render_evidence() -> None:
    sources_data = load_yaml(ROOT / "data" / "sources.yml")
    claims_data = load_yaml(ROOT / "data" / "claims.yml")
    sources = {s["id"]: s for s in sources_data["sources"]}

    blocks = [
        "<h1>Evidence and claims</h1>",
        "<p>This page connects published claims to exact source records, locators, qualifications and review status. Automated checks confirm structural consistency; they do not establish factual truth.</p>",
    ]
    for claim in claims_data["claims"]:
        status = html.escape(str(claim.get("status", "")))
        review = html.escape(str(claim.get("human_review_status", "")))
        blocks.append('<section class="evidence-record">')
        blocks.append(f'<p><span class="status-label">{status}</span> <span class="status-label">human review: {review}</span></p>')
        blocks.append(f'<h2>{html.escape(claim["claim_text"])}</h2>')
        for ev in claim.get("evidence", []):
            src = sources.get(ev.get("source_id"), {})
            url = html.escape(src.get("url", "#"))
            title = html.escape(src.get("title", ev.get("source_id", "Unknown source")))
            blocks.append(f'<h3><a href="{url}">{title}</a></h3>')
            blocks.append(f'<p><strong>Locator:</strong> {html.escape(str(ev.get("locator", "")))}</p>')
            blocks.append(f'<p><strong>Finding:</strong> {html.escape(str(ev.get("relevant_finding", "")))}</p>')
            blocks.append(f'<p><strong>Qualification:</strong> {html.escape(str(ev.get("qualification", "")))}</p>')
        blocks.append('</section>')

    out = SITE / "evidence"
    out.mkdir(parents=True, exist_ok=True)
    page = page_shell("Evidence", "".join(blocks), source="data/claims.yml", meta="Claim-level traceability")
    (out / "index.html").write_text(page, encoding="utf-8")


def build() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    shutil.copy2(ROOT / "index.html", SITE / "index.html")
    shutil.copy2(ROOT / "styles.css", SITE / "styles.css")
    shutil.copy2(ROOT / "publication.css", SITE / "publication.css")

    render_articles()
    render_evidence()
    print(f"Built static site at {SITE}")


if __name__ == "__main__":
    build()
