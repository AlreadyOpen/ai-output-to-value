#!/usr/bin/env python3
"""Add machine-readable and interactive surfaces to an already-built site/."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from publication_data import load_claim_records, load_source_records, load_yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PUBLICATION_MODE = os.environ.get("PUBLICATION_MODE", "preview").strip().lower()
RELEASE_SCOPES = {"guide", "policy"}

FRAMEWORK = {
    "version": "1.0",
    "principle": "Use AI ambitiously. Keep the claims clear.",
    "actorNeutralRule": "Assess human, AI, automated, and hybrid work by the complete process and its results, not the identity of the producer.",
    "workflowRule": {
        "statement": "Workflow is the end-to-end process boundary across which the target claim must hold; it is not a seventh claim.",
        "questions": [
            "What outcome should this workflow produce?",
            "Where does the workflow start, and what counts as complete?",
            "Which handoffs, verification, integration, operation, or support steps sit downstream of the local task or product?",
            "If AI accelerates one task, where can the bottleneck move next?",
            "What is the unhappy path, including escalation, stop, reversal, or recovery?",
            "Are we measuring the end-to-end outcome or only local activity?"
        ]
    },
    "managementLanguageRule": {
        "statement": "Management vocabulary is not evidence by itself. Terms such as workflow, teamwork, KPI, productivity, leadership, and alignment must be operationalised before they justify a decision.",
        "questions": [
            "If teamwork is claimed, who participates, what happens before/during/after, how are decisions made, and what follow-up turns discussion into action?",
            "If a KPI is claimed, what is the exact metric, unit, source, baseline, cadence, and guardrail?",
            "If productivity is claimed, what accepted output or outcome is divided by which relevant input, and are quality and downstream rework included?",
            "If leadership or alignment is claimed, which observable decisions, coordination, authority, capability, or outcome improved?"
        ]
    },
    "claims": [
        {"level": "01-access", "name": "Access", "meaning": "We have a model, API, subscription, agent, or tool.", "doesNotProve": "effective use"},
        {"level": "02-output", "name": "Output", "meaning": "The system produced an artefact or performed an action.", "doesNotProve": "correctness or client fit"},
        {"level": "03-deliverable", "name": "Deliverable", "meaning": "The result is fit for a defined intended use.", "doesNotProve": "repeatability"},
        {"level": "04-capability", "name": "Capability", "meaning": "The organisation can verify, operate, support, maintain, and improve it.", "doesNotProve": "a valuable outcome"},
        {"level": "05-outcome", "name": "Outcome", "meaning": "Something meaningful changed, including learning or uncertainty removed where that is the purpose.", "doesNotProve": "that the gain exceeds full cost"},
        {"level": "06-value", "name": "Value", "meaning": "The outcome is worth the full cost, risk, alternatives, and trade-offs.", "doesNotProve": "that every task needs this claim"}
    ],
    "distinctions": [
        "Access is not capability.",
        "Output is not completion.",
        "Judgement is not authority.",
        "Activity is not value."
    ]
}


def selected_articles() -> list[dict]:
    manifest = load_yaml(ROOT / "data" / "articles.yml")
    articles = sorted(manifest["articles"], key=lambda item: item.get("order", 9999))
    if PUBLICATION_MODE == "release":
        return [item for item in articles if item.get("release_scope") in RELEASE_SCOPES]
    return articles


def json_default(value):
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        return isoformat()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=json_default) + "\n",
        encoding="utf-8",
    )


def publish_api(articles: list[dict]) -> None:
    api = SITE / "api" / "v1"
    gates = json.loads((ROOT / "schemas" / "v1" / "decision-gates.json").read_text(encoding="utf-8"))
    included_sources = {item["source"] for item in articles}

    article_records = []
    for item in articles:
        article_records.append({
            "id": item["id"],
            "title": item["title"],
            "slug": item["slug"],
            "section": item["section"],
            "releaseScope": item["release_scope"],
            "status": item["status"],
            "summary": item.get("summary", ""),
            "url": f"articles/{item['slug']}.html",
            "markdownUrl": f"md/{item['slug']}.md"
        })

    claims = [record for _, record in load_claim_records(ROOT) if isinstance(record, dict)]
    if PUBLICATION_MODE == "release":
        claims = [
            claim for claim in claims
            if any(
                pub.get("file") == "index.html" or pub.get("file") in included_sources
                for pub in claim.get("published_in", [])
            )
        ]

    source_ids = {
        evidence.get("source_id")
        for claim in claims
        for evidence in claim.get("evidence", [])
        if isinstance(evidence, dict) and evidence.get("source_id")
    }
    sources = [
        record for _, record in load_source_records(ROOT)
        if isinstance(record, dict) and record.get("id") in source_ids
    ]

    write_json(api / "framework.json", {**FRAMEWORK, "decisionGates": "gates.json"})
    write_json(api / "gates.json", gates)
    write_json(api / "articles.json", {"publicationMode": PUBLICATION_MODE, "articles": article_records})
    write_json(api / "claims.json", {"publicationMode": PUBLICATION_MODE, "claims": claims})
    write_json(api / "sources.json", {"publicationMode": PUBLICATION_MODE, "sources": sources})


def publish_toolkit() -> None:
    schemas_out = SITE / "schemas" / "v1"
    schemas_out.mkdir(parents=True, exist_ok=True)
    for name in ("claim.schema.json", "decision-gates.json"):
        shutil.copy2(ROOT / "schemas" / "v1" / name, schemas_out / name)

    tools_out = SITE / "tools"
    tools_out.mkdir(parents=True, exist_ok=True)
    for name in ("claim-gate.html", "claim-gate.js"):
        shutil.copy2(ROOT / "tools" / name, tools_out / name)


def inject_workflow_homepage(text: str) -> str:
    """Surface workflow and operational management language on the landing page."""
    text = text.replace(
        '<a href="#whole-job">The whole job</a>',
        '<a href="#whole-job">Workflow / whole job</a>',
    )

    old_intro = '''          <p class="eyebrow">Count the whole job</p>
          <h2>Use the metric you actually mean.</h2>
          <p>The example below uses <strong>summed labour hours</strong>. It does not claim the same percentage change in elapsed delivery time.</p>
          <p>Waiting, handoffs, and parallel work can change calendar duration without changing total labour hours.</p>'''
    new_intro = '''          <p class="eyebrow">Workflow, not isolated task</p>
          <h2>Improve the end-to-end result, not only local production.</h2>
          <p>A September 2026 <em>Harvard Business Review</em> process-management article recommends treating the <strong>workflow rather than the individual task</strong> as the object of AI redesign. Its coding-agent example is especially relevant: more code can be produced while the constraint moves into review, integration testing, security review, or deployment.</p>
          <p><strong>Workflow is not a seventh claim.</strong> It is the end-to-end process boundary across which Output must become Deliverable, repeatable Capability, Outcome, and Value.</p>
          <p>The same discipline applies to familiar management language. <strong>Teamwork, KPI, productivity, leadership, and alignment are not evidence by themselves.</strong> Define the participants/process, metric, denominator and quality boundary, authority, or claimed outcome before using the term to justify a decision.</p>
          <p>The labour-hour example alongside this section therefore measures the complete illustrated workflow, not just drafting. Waiting, handoffs, and parallel work can still change calendar duration without changing summed labour hours.</p>
          <p><a href="articles/workflow-not-task.html">Read: Workflow is the unit — where AI output becomes business delivery →</a></p>'''
    if old_intro in text:
        text = text.replace(old_intro, new_intro, 1)

    text = text.replace(
        '<li><span>4</span><p><strong>Which work disappeared, and which work moved elsewhere?</strong><br>Look beyond generation time.</p></li>',
        '<li><span>4</span><p><strong>Which work disappeared, which work moved elsewhere, and where will the workflow bottleneck move?</strong><br>Look beyond local generation speed to the end-to-end flow.</p></li>',
        1,
    )

    hbr_workflow_card = '''          <a class="source-card" href="https://hbr.org/2026/09/stop-automating-old-processes-design-new-ones-instead">
            <span>Management / process source · registered claims pending independent review</span>
            <strong>Harvard Business Review — redesign the workflow, not only the task</strong>
            <p>Shunko and Netessine argue that local AI acceleration can miss value, ignore the unhappy path, move bottlenecks downstream, or optimize the wrong metric when the end-to-end workflow is not redesigned.</p>
          </a>
'''
    hbr_teamwork_card = '''          <a class="source-card" href="https://hbr.org/2026/09/ai-can-enhance-every-stage-of-teamwork-under-two-conditions">
            <span>Management / teamwork source · registered claims pending independent review</span>
            <strong>Harvard Business Review — teamwork has a before, during, and after</strong>
            <p>Rosani and Farri operationalise teamwork across preparation, the live collaborative session, and follow-up, and propose intentionality and craft as conditions for useful team-AI collaboration.</p>
          </a>
'''
    dora_marker = '''          <a class="source-card" href="https://dora.dev/research/2025/dora-report/">'''
    if "Harvard Business Review — redesign the workflow" not in text and dora_marker in text:
        text = text.replace(dora_marker, hbr_workflow_card + hbr_teamwork_card + dora_marker, 1)
    elif "Harvard Business Review — teamwork has a before" not in text and dora_marker in text:
        text = text.replace(dora_marker, hbr_teamwork_card + dora_marker, 1)

    return text


def inject_discovery_links() -> None:
    homepage = SITE / "index.html"
    text = homepage.read_text(encoding="utf-8")
    if 'tools/claim-gate.html' not in text:
        text = text.replace(
            '<a href="articles/index.html">Articles</a>',
            '<a href="tools/claim-gate.html">Claim gate</a>\n        <a href="articles/index.html">Articles</a>',
            1,
        )
        text = text.replace(
            '<p><a href="articles/claim-card.html">Open the copyable claim card →</a></p>',
            '<p><a href="tools/claim-gate.html"><strong>Run the interactive claim gate →</strong></a> · <a href="articles/claim-card.html">Open the copyable claim card</a></p>',
            1,
        )
    text = inject_workflow_homepage(text)
    text = text.replace(
        '<p><a class="button primary" href="articles/meeting-brief.html">Print the meeting brief</a></p>',
        '<p><a class="button primary" href="downloads/ai-output-to-value-meeting-brief.pdf" target="_blank" rel="noopener">Open printable meeting brief PDF</a></p>',
        1,
    )
    homepage.write_text(text, encoding="utf-8")

    for path in (SITE / "articles").glob("*.html"):
        article = path.read_text(encoding="utf-8")
        if '../tools/claim-gate.html' in article:
            continue
        article = article.replace(
            '<a href="../index.html#interfaces">AI access</a><a href="../articles/index.html">Articles</a>',
            '<a href="../index.html#interfaces">AI access</a><a href="../tools/claim-gate.html">Claim gate</a><a href="../articles/index.html">Articles</a>',
        )
        article = article.replace(
            '<a href="../index.html#interfaces">AI access / WebMCP</a><a href="../articles/index.html">All articles</a>',
            '<a href="../index.html#interfaces">AI access / WebMCP</a><a href="../tools/claim-gate.html">Interactive claim gate</a><a href="../articles/index.html">All articles</a>',
        )
        path.write_text(article, encoding="utf-8")


def augment() -> None:
    if not SITE.exists():
        raise SystemExit("site/ does not exist; run scripts/build_site.py first")
    articles = selected_articles()
    publish_api(articles)
    publish_toolkit()
    inject_discovery_links()
    print(f"Augmented {PUBLICATION_MODE} site with API, schema, claim gate, workflow, and management-language framing")


if __name__ == "__main__":
    augment()
