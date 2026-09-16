/* AI Output to Value — WebMCP surface.
 * Most tools are read/evaluate-only and use generated /api/v1 publication data.
 * aiov_load_claim_gate_record may request a local Claim Gate form handoff only;
 * it does not mutate the publication, GitHub, review state, or any server record.
 */
(() => {
  "use strict";
  if (window.__aiovWebMCPRegistered) return;
  window.__aiovWebMCPRegistered = true;

  const script = document.currentScript || [...document.scripts].find((node) => /\/webmcp\.js(?:\?|$)/.test(node.src));
  const rootUrl = new URL("./", script?.src || document.baseURI);
  const siteUrl = (path) => new URL(path, rootUrl).href;
  const modelContext = document.modelContext;

  const MEETING_QUESTIONS = [
    "What exactly have we demonstrated?",
    "What did the AI know, and what did it infer?",
    "What remains before the intended use?",
    "Which work disappeared, which work moved elsewhere, and where will the workflow bottleneck move?",
    "Which actor or combination performs this task or decision best: human, AI, automated system, or hybrid?",
    "Where do authority, accountability, verification, approval, operation, and support sit?",
    "Which business outcome are we trying to change, including learning or uncertainty removed?",
    "What evidence would justify the next decision, and when should we stop?"
  ];

  function result(payload) {
    const json = JSON.stringify(payload, null, 2);
    const max = 14000;
    const text = json.length <= max ? json : `${json.slice(0, max)}\n\n[TRUNCATED: narrow the query or page the article.]`;
    return { content: [{ type: "text", text }] };
  }

  function error(message) {
    return { content: [{ type: "text", text: `ERROR: ${message}` }], isError: true };
  }

  async function fetchJson(path) {
    const response = await fetch(siteUrl(path), { credentials: "same-origin" });
    if (!response.ok) throw new Error(`${path} returned HTTP ${response.status}`);
    return response.json();
  }

  async function fetchText(path) {
    const response = await fetch(siteUrl(path), { credentials: "same-origin" });
    if (!response.ok) throw new Error(`${path} returned HTTP ${response.status}`);
    return response.text();
  }

  function runtimeStatus(message) {
    const host = document.querySelector("[data-webmcp-status-host], #interfaces .reading-route");
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

  function evaluateClaimRecord(record, gates) {
    const decisionId = record?.targetDecision;
    const rule = gates?.decisions?.[decisionId];
    const structuralErrors = [];
    const missingFields = [];

    if (record?.schemaVersion !== "1.0") {
      structuralErrors.push("schemaVersion must be '1.0'");
    }

    if (!rule) {
      structuralErrors.push(`Unknown targetDecision: ${String(decisionId)}`);
      return {
        status: "BLOCKED",
        targetDecision: decisionId ?? null,
        errors: structuralErrors,
        structuralErrors,
        missingFields,
        claimMismatch: false,
        failedChecks: [],
        unknownChecks: [],
        passedChecks: [],
        interactiveClaimGate: siteUrl("tools/claim-gate.html")
      };
    }

    if (record?.requiredClaimLevel !== rule.requiredClaimLevel) {
      structuralErrors.push(`requiredClaimLevel must be ${rule.requiredClaimLevel} for ${decisionId}`);
    }

    const checks = record?.gateChecks && typeof record.gateChecks === "object" && !Array.isArray(record.gateChecks)
      ? record.gateChecks
      : {};
    const failedChecks = [];
    const unknownChecks = [];
    const passedChecks = [];

    for (const check of rule.requiredChecks ?? []) {
      const state = checks[check.id] ?? "unknown";
      const item = { id: check.id, label: check.label, state };
      if (state === "fail") failedChecks.push(item);
      else if (state === "pass") passedChecks.push(item);
      else unknownChecks.push(item);
    }

    const requiredTextFields = ["project", "intendedUse", "authority", "accountability", "nextEvidence", "stopRule"];
    for (const field of requiredTextFields) {
      if (!String(record?.[field] ?? "").trim()) missingFields.push(field);
    }
    if (!Array.isArray(record?.actors) || record.actors.length === 0) missingFields.push("actors");

    const claimMismatch = record?.assertedClaimLevel !== rule.requiredClaimLevel;
    let status = "PASS";
    if (structuralErrors.length || failedChecks.length) status = "BLOCKED";
    else if (unknownChecks.length || missingFields.length || claimMismatch) status = "INSUFFICIENT_EVIDENCE";

    return {
      status,
      targetDecision: decisionId,
      decisionLabel: rule.label,
      requiredClaimLevel: rule.requiredClaimLevel,
      assertedClaimLevel: record?.assertedClaimLevel ?? null,
      errors: structuralErrors,
      structuralErrors,
      missingFields,
      claimMismatch,
      failedChecks,
      unknownChecks,
      passedChecks,
      principle: gates?.principle ?? null,
      interactiveClaimGate: siteUrl("tools/claim-gate.html")
    };
  }

  if (!modelContext?.registerTool) {
    runtimeStatus("WebMCP runtime: this browser does not currently expose document.modelContext. The site still publishes the same machine-readable API and normal human interface.");
    return;
  }

  const emptySchema = { type: "object", properties: {}, additionalProperties: false };
  const claimObjectSchema = { type: "object", additionalProperties: true };

  const tools = [
    {
      name: "aiov_get_framework",
      description: "Read-only. Returns the six-claim framework, actor-neutral rule, and deterministic decision gates from the current publication build.",
      inputSchema: emptySchema,
      async execute() {
        try {
          const [framework, gates] = await Promise.all([fetchJson("api/v1/framework.json"), fetchJson("api/v1/gates.json")]);
          return result({ framework, gates, claim_gate: siteUrl("tools/claim-gate.html") });
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    },
    {
      name: "aiov_list_articles",
      description: "Read-only. Lists articles included in the current publication build.",
      inputSchema: {
        type: "object",
        properties: { section: { type: "string", maxLength: 80 } },
        additionalProperties: false
      },
      async execute({ section } = {}) {
        try {
          const payload = await fetchJson("api/v1/articles.json");
          const wanted = String(section || "").trim().toLowerCase();
          const articles = payload.articles.filter((item) => !wanted || `${item.section} ${item.releaseScope}`.toLowerCase().includes(wanted));
          return result({ publicationMode: payload.publicationMode, count: articles.length, articles: articles.map((item) => ({ ...item, url: siteUrl(item.url), markdownUrl: siteUrl(item.markdownUrl) })) });
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    },
    {
      name: "aiov_get_article",
      description: "Read-only. Reads the published Markdown of one article by slug. Use offset and max_chars for long articles.",
      inputSchema: {
        type: "object",
        properties: {
          slug: { type: "string", pattern: "^[a-z0-9-]+$", maxLength: 100 },
          offset: { type: "integer", minimum: 0, default: 0 },
          max_chars: { type: "integer", minimum: 500, maximum: 12000, default: 7000 }
        },
        required: ["slug"],
        additionalProperties: false
      },
      async execute({ slug, offset = 0, max_chars = 7000 }) {
        if (!/^[a-z0-9-]+$/.test(slug || "")) return error("Invalid article slug.");
        try {
          const index = await fetchJson("api/v1/articles.json");
          const article = index.articles.find((item) => item.slug === slug);
          if (!article) return error(`Article is not included in this publication build: ${slug}`);
          const text = await fetchText(article.markdownUrl);
          const start = Math.min(Number(offset) || 0, text.length);
          const size = Math.min(Math.max(Number(max_chars) || 7000, 500), 12000);
          return result({
            title: article.title,
            slug,
            url: siteUrl(article.url),
            markdownUrl: siteUrl(article.markdownUrl),
            offset: start,
            returned_chars: Math.min(size, Math.max(0, text.length - start)),
            total_chars: text.length,
            has_more: start + size < text.length,
            text: text.slice(start, start + size)
          });
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    },
    {
      name: "aiov_search_evidence",
      description: "Read-only. Searches claim-level evidence records in the current publication build.",
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
        const needle = String(query || "").trim().toLowerCase();
        if (needle.length < 2) return error("query must contain at least 2 characters.");
        try {
          const payload = await fetchJson("api/v1/claims.json");
          const matches = payload.claims
            .filter((claim) => JSON.stringify(claim).toLowerCase().includes(needle))
            .slice(0, Math.min(Math.max(Number(limit) || 6, 1), 12))
            .map((claim) => ({
              claim_id: claim.id,
              claim: claim.claim_text,
              status: claim.status,
              independent_review: claim.independent_review_status,
              launch_critical: claim.launch_critical,
              url: `${siteUrl("evidence/index.html")}#${encodeURIComponent(claim.id)}`
            }));
          return result({ query, publicationMode: payload.publicationMode, count: matches.length, matches });
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    },
    {
      name: "aiov_get_claim",
      description: "Read-only. Returns one canonical claim record from the current publication build.",
      inputSchema: {
        type: "object",
        properties: { claim_id: { type: "string", pattern: "^[a-z0-9-]+$", maxLength: 160 } },
        required: ["claim_id"],
        additionalProperties: false
      },
      async execute({ claim_id }) {
        if (!/^[a-z0-9-]+$/.test(claim_id || "")) return error("Invalid claim_id.");
        try {
          const payload = await fetchJson("api/v1/claims.json");
          const claim = payload.claims.find((item) => item.id === claim_id);
          if (!claim) return error(`Claim is not included in this publication build: ${claim_id}`);
          return result({ publicationMode: payload.publicationMode, claim, url: `${siteUrl("evidence/index.html")}#${encodeURIComponent(claim_id)}` });
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    },
    {
      name: "aiov_search_failure_modes",
      description: "Read-only. Searches the working software/architecture failure-mode catalogue for patterns that can invalidate Deliverable or Operating capability claims.",
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
        const needle = String(query || "").trim().toLowerCase();
        if (needle.length < 2) return error("query must contain at least 2 characters.");
        try {
          const payload = await fetchJson("api/v1/failure-modes.json");
          const matches = (payload.failureModes || [])
            .filter((mode) => JSON.stringify(mode).toLowerCase().includes(needle))
            .slice(0, Math.min(Math.max(Number(limit) || 6, 1), 12));
          return result({
            query,
            publicationMode: payload.publicationMode,
            reviewState: payload.reviewState,
            character: payload.character,
            count: matches.length,
            matches,
            catalogue: siteUrl("articles/software-failure-mode-catalogue.html")
          });
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    },
    {
      name: "aiov_evaluate_claim_record",
      description: "Read-only/evaluation. Evaluate a claim.json record against the same published decision-gate rules used by the interactive Claim Gate. This checks the supplied record; it does not independently verify the underlying facts.",
      inputSchema: {
        type: "object",
        properties: { claim: claimObjectSchema },
        required: ["claim"],
        additionalProperties: false
      },
      async execute({ claim }) {
        try {
          const gates = await fetchJson("api/v1/gates.json");
          return result(evaluateClaimRecord(claim, gates));
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    },
    {
      name: "aiov_load_claim_gate_record",
      description: "Hybrid/local UI bridge. Request that an agent-prepared claim.json record be loaded into the currently open interactive Claim Gate form so a person can inspect or edit it. This changes local browser form state only and does not write to a server, publication, review record, or GitHub.",
      inputSchema: {
        type: "object",
        properties: { claim: claimObjectSchema },
        required: ["claim"],
        additionalProperties: false
      },
      async execute({ claim }) {
        const host = document.getElementById("claim-gate-root");
        if (!host || host.dataset.reactMounted !== "true") {
          return error(`Open the interactive Claim Gate and wait for it to load first: ${siteUrl("tools/claim-gate.html")}`);
        }
        window.dispatchEvent(new CustomEvent("aiov:load-claim-record", { detail: { claim } }));
        return result({
          handoffRequested: true,
          applicationConfirmed: false,
          scope: "local-browser-form-only",
          claim_gate: window.location.href,
          message: "The record handoff event was dispatched to the mounted Claim Gate. This tool cannot yet independently confirm that the form accepted it; inspect the visible form before relying on the handoff."
        });
      }
    },
    {
      name: "aiov_get_meeting_guide",
      description: "Read-only. Returns the eight meeting questions, workflow-boundary test, deterministic decision gates, and links to the printable brief and interactive claim gate.",
      inputSchema: emptySchema,
      async execute() {
        try {
          const gates = await fetchJson("api/v1/gates.json");
          return result({
            questions: MEETING_QUESTIONS,
            workflowTest: {
              rule: "Workflow is the end-to-end process boundary across which the target claim must hold; it is not a seventh claim.",
              questions: [
                "What outcome should this workflow produce?",
                "Where does the workflow start, and what counts as complete?",
                "If AI accelerates one task, where can the bottleneck move next?",
                "What is the unhappy path, including escalation, stop, reversal, or recovery?",
                "Are we measuring the outcome or only local activity?"
              ]
            },
            decisionGates: gates.decisions,
            printable_brief: siteUrl("downloads/ai-output-to-value-meeting-brief.pdf"),
            meeting_brief_article: siteUrl("articles/meeting-brief.html"),
            claim_card: siteUrl("articles/claim-card.html"),
            workflow_guide: siteUrl("articles/workflow-not-task.html"),
            interactive_claim_gate: siteUrl("tools/claim-gate.html"),
            ai_claim_gate_tool: "aiov_evaluate_claim_record",
            hybrid_claim_gate_tool: "aiov_load_claim_gate_record",
            software_failure_catalogue: siteUrl("articles/software-failure-mode-catalogue.html"),
            software_worked_cases: siteUrl("articles/software-architecture-worked-cases.html")
          });
        } catch (err) { return error(err instanceof Error ? err.message : String(err)); }
      }
    }
  ];

  Promise.all(tools.map((tool) => modelContext.registerTool(tool)))
    .then(() => runtimeStatus(`WebMCP runtime: ${tools.length} tools registered. Eight are read/evaluate-only; aiov_load_claim_gate_record can request a local Claim Gate handoff without server-side writes.`))
    .catch((err) => runtimeStatus(`WebMCP runtime: tool registration failed (${err instanceof Error ? err.message : String(err)}).`));
})();
