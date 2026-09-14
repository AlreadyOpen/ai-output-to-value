#!/usr/bin/env python3
"""Build the static publication from Markdown and canonical YAML evidence."""
from __future__ import annotations

import html
import os
import re
import shutil
from pathlib import Path

import markdown
from publication_data import claims as load_claims
from publication_data import load_yaml, source_map

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REPO_URL = "https://github.com/helenkwok/ai-output-to-value"
SOURCE_REF = os.environ.get("PUBLICATION_SOURCE_REF") or os.environ.get("GITHUB_SHA") or "main"
STATUS = {
    "draft": "Draft",
    "research_draft": "Research draft",
    "editorial_review": "Editorial review in progress",
    "active_policy": "Active publication policy",
    "ready": "Reviewed for publication",
}


def status_label(value: str) -> str:
    return STATUS.get(value, value.replace("_", " ").title())


def heading_anchor(locator: str) -> str | None:
    m = re.match(r"^#{1,6}\s+(.+?)\s*$", locator.strip())
    if not m:
        return None
    text = re.sub(r"[`*_~]", "", m.group(1)).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", text).strip("-") or None


def page_shell(title: str, body: str, source: str | None = None, meta: str = "") -> str:
    source_link = ""
    if source:
        source_link = f'<a href="{REPO_URL}/blob/{SOURCE_REF}/{html.escape(source)}">View source version</a>'
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="AI Output to Value — evidence-led guidance for business decisions about AI-assisted work.">
<title>{html.escape(title)} — AI Output to Value</title>
<link rel="stylesheet" href="../styles.css"><link rel="stylesheet" href="../publication.css"></head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="../index.html"><span class="brand-mark" aria-hidden="true">O→V</span><span>AI Output to Value</span></a><nav class="nav" aria-label="Primary navigation"><a href="../articles/index.html">Articles</a><a href="../evidence/index.html">Evidence</a><a href="{REPO_URL}">GitHub</a></nav></div></header>
<details class="mobile-nav"><summary>Menu</summary><nav aria-label="Mobile navigation"><a href="../index.html">Home</a><a href="../articles/index.html">Articles</a><a href="../evidence/index.html">Evidence</a><a href="{REPO_URL}">GitHub</a></nav></details>
<main id="main" class="article-shell"><article class="article-body"><div class="article-meta">{meta}</div>{body}</article><aside class="article-aside" aria-label="Article links"><strong>AI Output to Value</strong><a href="../index.html">Home</a><a href="../articles/index.html">All articles</a><a href="../evidence/index.html">Evidence</a>{source_link}<a href="../articles/corrections.html">Report a correction</a></aside></main></body></html>"""


def rewrite_links(rendered: str, mapping: dict[str, str], source_path: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            return match.group(0)
        path_part, sep, fragment = href.partition("#")
        resolved = (source_path.parent / path_part).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        if rel in mapping:
            return f'href="{mapping[rel]}{("#" + fragment) if sep else ""}"'
        if resolved.exists():
            return f'href="{REPO_URL}/blob/{SOURCE_REF}/{rel}{("#" + fragment) if sep else ""}"'
        return match.group(0)
    return re.sub(r'href="([^"]+)"', repl, rendered)


def claims_for(source: str, records: list[dict]) -> list[dict]:
    return [c for c in records if any(p.get("file") == source for p in c.get("published_in", []))]


def evidence_block(records: list[dict]) -> str:
    if not records:
        return '<section class="article-evidence-links"><h2>Evidence connection</h2><p>No claim-level evidence records are attached to this page yet. Treat factual statements according to the visible publication status.</p></section>'
    items = []
    for c in records:
        cid = html.escape(str(c.get("id", "")))
        text = html.escape(str(c.get("claim_text", "")))
        review = html.escape(str(c.get("human_review_status", "unspecified")))
        items.append(f'<li><a href="../evidence/index.html#{cid}">{text}</a> <span class="evidence-review-note">(human review: {review})</span></li>')
    return '<section class="article-evidence-links"><h2>Evidence used on this page</h2><p>Factual claims currently connected to the publication evidence register:</p><ul>' + ''.join(items) + '</ul></section>'


def meta_for(item: dict, records: list[dict]) -> str:
    if records:
        pending = sum(c.get("human_review_status") != "completed" for c in records)
        evidence_state = f"Evidence review: {pending} connected claim(s) await human approval" if pending else "Evidence review: connected claims marked complete"
    else:
        evidence_state = "Evidence review: no claim-level records attached yet"
    return (f'<span class="status-label">{html.escape(status_label(str(item.get("status", "draft"))))}</span> '
            f'&nbsp; Maintained by {html.escape(str(item.get("maintainer", "")))} · Last updated {html.escape(str(item.get("reviewed", "")))}<br>'
            f'<span class="review-scope">{html.escape(evidence_state)}</span>')


def render_articles() -> list[dict]:
    manifest = load_yaml(ROOT / "data" / "articles.yml")
    articles = sorted(manifest["articles"], key=lambda x: x.get("order", 9999))
    mapping = {a["source"]: f'{a["slug"]}.html' for a in articles}
    records = load_claims(ROOT)
    out = SITE / "articles"; out.mkdir(parents=True, exist_ok=True)
    for item in articles:
        source_path = ROOT / item["source"]
        body = markdown.markdown(source_path.read_text(encoding="utf-8"), extensions=["tables", "fenced_code", "sane_lists", "toc"])
        body = rewrite_links(body, mapping, source_path)
        related = claims_for(item["source"], records)
        body += evidence_block(related)
        (out / f'{item["slug"]}.html').write_text(page_shell(item["title"], body, item["source"], meta_for(item, related)), encoding="utf-8")
    blocks = ["<h1>Articles</h1>", "<p>Status labels describe publication state. Dates mean last updated, not that every factual claim has completed evidence review.</p>"]
    for key, label in [("core", "Core reading"), ("deeper", "Deeper analysis"), ("advanced", "Advanced / agentic organisations"), ("policy", "Publication policy")]:
        selected = [a for a in articles if a.get("section") == key]
        if not selected: continue
        blocks.append(f'<h2>{label}</h2><div class="evidence-grid">')
        for a in selected:
            blocks.append(f'<a class="source-card" href="{html.escape(a["slug"])}.html"><span>{html.escape(status_label(str(a.get("status", "draft"))))}</span><strong>{html.escape(a["title"])}</strong><p>{html.escape(a.get("summary", ""))}</p></a>')
        blocks.append("</div>")
    (out / "index.html").write_text(page_shell("Articles", "".join(blocks)), encoding="utf-8")
    return articles


def backlink(pub: dict, article_by_source: dict[str, dict]) -> str:
    target, locator = str(pub.get("file", "")), str(pub.get("locator", ""))
    article = article_by_source.get(target)
    if article:
        anchor = heading_anchor(locator)
        href = f'../articles/{article["slug"]}.html' + (f'#{anchor}' if anchor else '')
        return f'<a href="{href}">{html.escape(article["title"])}</a> — {html.escape(locator)}'
    if target == "index.html":
        return f'<a href="../index.html">Homepage</a> — {html.escape(locator)}'
    return f'<a href="{REPO_URL}/blob/{SOURCE_REF}/{html.escape(target)}">{html.escape(target)}</a> — {html.escape(locator)}'


def render_evidence() -> None:
    sources, records = source_map(ROOT), load_claims(ROOT)
    articles = load_yaml(ROOT / "data" / "articles.yml")["articles"]
    by_source = {a["source"]: a for a in articles}
    blocks = ["<h1>Evidence and claims</h1>", "<p>Claim records show source, locator, qualification, review state, and where each claim appears. Structural checks do not establish factual truth.</p>"]
    for c in records:
        cid = html.escape(str(c.get("id", "")))
        blocks.append(f'<section class="evidence-record" id="{cid}"><p><span class="status-label">{html.escape(str(c.get("status", "")))}</span> <span class="status-label">human review: {html.escape(str(c.get("human_review_status", "")))}</span></p><h2>{html.escape(str(c.get("claim_text", "")))}</h2>')
        blocks.append(f'<p><strong>Review record:</strong> {html.escape(str(c.get("reviewer", "")))} · {html.escape(str(c.get("reviewed", "")))}</p>')
        if c.get("launch_critical") is not None:
            blocks.append(f'<p><strong>Launch-critical:</strong> {"yes" if c.get("launch_critical") else "no"}</p>')
        for ev in c.get("evidence", []):
            src = sources.get(ev.get("source_id"), {})
            blocks.append(f'<h3><a href="{html.escape(str(src.get("url", "#")))}">{html.escape(str(src.get("title", ev.get("source_id", "Unknown source"))))}</a></h3>')
            blocks.append(f'<p><strong>Source:</strong> {html.escape(str(src.get("publisher", "")))} · {html.escape(str(src.get("evidence_type", "")))}</p>')
            if ev.get("source_version"): blocks.append(f'<p><strong>Version/date used:</strong> {html.escape(str(ev.get("source_version")))}</p>')
            blocks.append(f'<p><strong>Locator:</strong> {html.escape(str(ev.get("locator", "")))}</p><p><strong>Finding:</strong> {html.escape(str(ev.get("relevant_finding", "")))}</p><p><strong>Qualification:</strong> {html.escape(str(ev.get("qualification", "")))}</p>')
            if src.get("scope"): blocks.append(f'<p><strong>Source scope:</strong> {html.escape(str(src.get("scope")))}</p>')
            if src.get("limitations"): blocks.append(f'<p><strong>Source limitations:</strong> {html.escape(str(src.get("limitations")))}</p>')
        if c.get("published_in"):
            blocks.append('<h3>Used in</h3><ul>' + ''.join(f'<li>{backlink(p, by_source)}</li>' for p in c["published_in"]) + '</ul>')
        blocks.append('</section>')
    out = SITE / "evidence"; out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page_shell("Evidence", "".join(blocks), "data/claims.yml", "Claim-level traceability · preview build · structural checks are not factual approval"), encoding="utf-8")


def build() -> None:
    if SITE.exists(): shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    for name in ("index.html", "styles.css", "publication.css"): shutil.copy2(ROOT / name, SITE / name)
    render_articles(); render_evidence()
    print(f"Built static site at {SITE} using source ref {SOURCE_REF}")


if __name__ == "__main__": build()
