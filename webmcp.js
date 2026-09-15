/* AI Output to Value — read-only WebMCP surface.
 *
 * This file intentionally exposes publication-reading tools only. It does not
 * mutate the site, GitHub, review records, or release state. WebMCP changes the
 * interaction channel; the publication's evidence and authority rules remain
 * unchanged.
 */
(() => {
  "use strict";

  if (window.__aiovWebMCPRegistered) return;
  window.__aiovWebMCPRegistered = true;

  const script = document.currentScript || [...document.scripts].find((node) => /\/webmcp\.js(?:\?|$)/.test(node.src));
  const rootUrl = new URL("./", script?.src || document.baseURI);
  const siteUrl = (path) => new URL(path, rootUrl).href;
  const modelContext = document.modelContext;

  const FRAMEWORK = {
    principle: "Use AI ambitiously. Keep the claims clear.",
    actor_neutral_rule: "Assess human, AI, automated, and hybrid work by the complete process and its results, not the identity of the producer.",
    claims: [
      { level: 1, name: "Access", meaning: "We have a model, API, subscription, agent, or tool.", does_not_prove: "effective use" },
      { level: 2, name: "Output", meaning: "The system produced an artefact or performed an action.", does_not_prove: "correctness or client fit" },
      { level: 3, name: "Deliverable", meaning: "The result is fit for a defined intended use.", does_not_prove: "repeatability" },
      { level: 4, name: "Capability", meaning: "The organisation can verify, operate, support, maintain, and improve it.", does_not_prove: "a valuable outcome" },
      { level: 5, name: "Outcome", meaning: "Something meaningful changed, including learning or uncertainty removed where that is the purpose.", does_not_prove: "that the gain exceeds full cost" },
      { level: 6, name: "Value", meaning: "The outcome is worth the full cost, risk, alternatives, and trade-offs.", does_not_prove: "that every task needs this claim" }
    ],
    distinctions: [
      "Access is not capability.",
      "Output is not completion.",
      "Judgement is not authority.",
      "Activity is not value."
    ]
  };

  const DECISION_THRESHOLDS = [
    { decision: "Keep exploring?", claim: "Output", evidence: "Enough to reproduce the artefact/action and learn from it." },
    { decision: "May someone rely on it for the named use?", claim: "Deliverable", evidence: "Intended use, acceptance criteria, evaluation against them, and known limits." },
    { decision: "May we sell, operate, support, or staff it repeatedly?", claim: "Capability", evidence: "Owners, controls, fallback, operating process, and operating cost." },
    { decision: "Did it change the result we care about?", claim: "Outcome", evidence: "Baseline and after measurement using the same definition, with material confounds named." },
    { decision: "Should we scale, renew, expand, or stop?", claim: "Value", evidence: "Outcome compared with full relevant cost, risk, alternatives, and trade-offs." }
  ];

  const MEETING_QUESTIONS = [
    "What exactly have we demonstrated?",
    "What did the AI know, and what did it infer?",
    "What remains before the intended use?",
    "Which work disappeared, and which work moved elsewhere?",
    "Which actor or combination performs this task or decision best: human, AI, automated system, or hybrid?",
    "Where do authority, accountability, verification, approval, operation, and support sit?",
    "Which business outcome are we trying to change, including learning or uncertainty removed?",
    "What evidence would justify the next decision, and when should we stop?"
  ];

  const normalize = (value) => String(value ?? "").replace(/\s+/g, " ").trim();

  function result(payload) {
    const json = JSON.stringify(payload, null, 2);
    const max = 14000;
    const text = json.length <= max
      ? json
      : `${json.slice(0, max)}\n\n[TRUNCATED by AI Output to Value: ${json.length - max} characters omitted. Narrow the query or use article offset/max_chars.]`;
    return { content: [{ type: "text", text }] };
  }

  function error(message) {
    return { content: [{ type: "text", text: `ERROR: ${message}` }], isError: true };
  }

  async function fetchDocument(path) {
    const response = await fetch(siteUrl(path), { credentials: "same-origin" });
    if (!response.ok) throw new Error(`${path} returned HTTP ${response.status}`);
    return new DOMParser().parseFromString(await response.text(), "text/html");
  }

  function runtimeStatus(message) {
    const host = document.querySelector("#interfaces .reading-route");
    if (!host) return;
    let node = document.getElementById("webmcp-runtime-status");
    if (!node) {
      node = document.createElement("p");
      node.id = "webmcp-runtime-status";
      node.className = "measure-note";
      host.appendChild(node);
    }
    node.textContent = message;
  }

  if (!modelContext?.registerTool) {
    runtimeStatus("WebMCP runtime: this browser does not currently expose document.modelContext. The normal human-readable site remains fully available.");
    return;
  }

  const emptySchema = { type: "object", properties: {}, additionalProperties: false };

  const tools = [
    {
      name: "aiov_get_framework",
      description: "Read-only. Returns the AI Output to Value six-claim framework, actor-neutral rule, core distinctions, and decision thresholds.",
      inputSchema: emptySchema,
      execute() {
        return result({
          framework: FRAMEWORK,
          decision_thresholds: DECISION_THRESHOLDS,
          claim_card: siteUrl("articles/claim-card.html"),
          evidence: siteUrl("evidence/index.html")
        });
      }
    },
    {
      name: "aiov_list_articles",
      description: "Read-only. Lists published article cards from the current AI Output to Value build, preserving visible status and section labels.",
      inputSchema: {
        type: "object",
        properties: {
          section: { type: "string", description: "Optional case-insensitive text filter for section headings such as core, working, research, or policy.", maxLength: 80 }
        },
        additionalProperties: false
      },
      async execute({ section } = {}) {
        try {
          const doc = await fetchDocument("articles/index.html");
          const wanted = normalize(section).toLowerCase();
          const articles = [];
          for (const heading of doc.querySelectorAll(".article-body h2")) {
            const sectionName = normalize(heading.textContent);
            if (wanted && !sectionName.toLowerCase().includes(wanted)) continue;
            let grid = heading.nextElementSibling;
            while (grid && !grid.classList?.contains("evidence-grid") && grid.tagName !== "H2") grid = grid.nextElementSibling;
            if (!grid || !grid.classList?.contains("evidence-grid")) continue;
            for (const card of grid.querySelectorAll("a.source-card")) {
              articles.push({
                section: sectionName,
                status: normalize(card.querySelector("span")?.textContent),
                title: normalize(card.querySelector("strong")?.textContent),
                summary: normalize(card.querySelector("p")?.textContent),
                url: new URL(card.getAttribute("href"), siteUrl("articles/index.html")).href
              });
            }
          }
          return result({ count: articles.length, articles });
        } catch (err) {
          return error(err instanceof Error ? err.message : String(err));
        }
      }
    },
    {
      name: "aiov_get_article",
      description: "Read-only. Reads the rendered text of one AI Output to Value article by slug. Use offset and max_chars to page through long articles.",
      inputSchema: {
        type: "object",
        properties: {
          slug: { type: "string", description: "Article slug, for example claim-card or executive-guide.", pattern: "^[a-z0-9-]+$", maxLength: 100 },
          offset: { type: "integer", minimum: 0, default: 0 },
          max_chars: { type: "integer", minimum: 500, maximum: 12000, default: 7000 }
        },
        required: ["slug"],
        additionalProperties: false
      },
      async execute({ slug, offset = 0, max_chars = 7000 }) {
        if (!/^[a-z0-9-]+$/.test(slug || "")) return error("Invalid article slug.");
        try {
          const path = `articles/${slug}.html`;
          const doc = await fetchDocument(path);
          const body = doc.querySelector(".article-body");
          if (!body) return error(`Article not found: ${slug}`);
          const clone = body.cloneNode(true);
          clone.querySelector(".article-meta")?.remove();
          const text = normalize(clone.textContent);
          const start = Math.min(Number(offset) || 0, text.length);
          const size = Math.min(Math.max(Number(max_chars) || 7000, 500), 12000);
          return result({
            title: normalize(doc.querySelector("h1")?.textContent || doc.title),
            slug,
            url: siteUrl(path),
            offset: start,
            returned_chars: Math.min(size, Math.max(0, text.length - start)),
            total_chars: text.length,
            has_more: start + size < text.length,
            text: text.slice(start, start + size)
          });
        } catch (err) {
          return error(err instanceof Error ? err.message : String(err));
        }
      }
    },
    {
      name: "aiov_search_evidence",
      description: "Read-only. Searches claim-level evidence records in the current publication build and returns matching claims with review state.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", minLength: 2, maxLength: 200 },
          limit: { type: "integer", minimum: 1, maximum: 12, default: 6 }
        },
        required: ["query"],
        additionalProperties: false
      },
      async execute({ query, limit = 6 }) {
        const needle = normalize(query).toLowerCase();
        if (needle.length < 2) return error("query must contain at least 2 characters.");
        try {
          const doc = await fetchDocument("evidence/index.html");
          const matches = [];
          for (const record of doc.querySelectorAll(".evidence-record")) {
            const haystack = normalize(record.textContent).toLowerCase();
            if (!haystack.includes(needle)) continue;
            const labels = [...record.querySelectorAll(".status-label")].map((node) => normalize(node.textContent));
            matches.push({
              claim_id: record.id,
              claim: normalize(record.querySelector("h2")?.textContent),
              status: labels[0] || "",
              independent_review: labels[1] || "",
              url: `${siteUrl("evidence/index.html")}#${encodeURIComponent(record.id)}`
            });
            if (matches.length >= Math.min(Math.max(Number(limit) || 6, 1), 12)) break;
          }
          return result({ query, count: matches.length, matches });
        } catch (err) {
          return error(err instanceof Error ? err.message : String(err));
        }
      }
    },
    {
      name: "aiov_get_claim",
      description: "Read-only. Returns one claim-level evidence record, including visible source findings, qualifications, limitations, and independent-review state.",
      inputSchema: {
        type: "object",
        properties: {
          claim_id: { type: "string", pattern: "^[a-z0-9-]+$", maxLength: 160 }
        },
        required: ["claim_id"],
        additionalProperties: false
      },
      async execute({ claim_id }) {
        if (!/^[a-z0-9-]+$/.test(claim_id || "")) return error("Invalid claim_id.");
        try {
          const doc = await fetchDocument("evidence/index.html");
          const record = doc.getElementById(claim_id);
          if (!record) return error(`Claim not found: ${claim_id}`);
          const labels = [...record.querySelectorAll(".status-label")].map((node) => normalize(node.textContent));
          const sources = [...record.querySelectorAll("h3 a")].map((link) => ({
            title: normalize(link.textContent),
            url: link.href
          }));
          return result({
            claim_id,
            claim: normalize(record.querySelector("h2")?.textContent),
            status: labels[0] || "",
            independent_review: labels[1] || "",
            sources,
            record_text: normalize(record.textContent),
            url: `${siteUrl("evidence/index.html")}#${encodeURIComponent(claim_id)}`
          });
        } catch (err) {
          return error(err instanceof Error ? err.message : String(err));
        }
      }
    },
    {
      name: "aiov_get_meeting_guide",
      description: "Read-only. Returns the eight meeting questions, typical claim thresholds, and links to the printable brief and claim card.",
      inputSchema: emptySchema,
      execute() {
        return result({
          questions: MEETING_QUESTIONS,
          decision_thresholds: DECISION_THRESHOLDS,
          printable_brief: siteUrl("articles/meeting-brief.html"),
          claim_card: siteUrl("articles/claim-card.html")
        });
      }
    }
  ];

  Promise.all(tools.map((tool) => modelContext.registerTool(tool)))
    .then(() => runtimeStatus(`WebMCP runtime: ${tools.length} read-only AI Output to Value tools registered in this browser.`))
    .catch((err) => runtimeStatus(`WebMCP runtime: tool registration was not available (${err instanceof Error ? err.message : String(err)}).`));
})();
