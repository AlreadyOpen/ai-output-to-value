#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";

import { DEFAULT_PUBLICATION_URL, evaluateClaim, fetchJson, getStopRule } from "./core.mjs";

const publicationUrl = process.env.AIOV_PUBLICATION_URL || DEFAULT_PUBLICATION_URL;

function text(payload) {
  return {
    content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    structuredContent: payload
  };
}

function fail(message) {
  return { content: [{ type: "text", text: `ERROR: ${message}` }], isError: true };
}

function buildServer() {
  const server = new McpServer(
    { name: "ai-output-to-value", version: "0.1.0" },
    {
      instructions: "Use the target decision to select the minimum sufficient claim. Do not average claim levels and do not privilege human, AI, automated, or hybrid work by identity alone."
    }
  );

  server.registerTool(
    "get_stop_rule",
    {
      title: "Get decision stop rule",
      description: "Return the minimum sufficient claim and deterministic checks for a target decision.",
      inputSchema: z.object({
        decision_type: z.enum(["explore", "rely", "operate", "measure-outcome", "scale-renew-stop"])
      })
    },
    async ({ decision_type }) => {
      try {
        const gates = await fetchJson(publicationUrl, "api/v1/gates.json");
        return text(getStopRule(gates, decision_type));
      } catch (error) {
        return fail(error instanceof Error ? error.message : String(error));
      }
    }
  );

  server.registerTool(
    "evaluate_claim_record",
    {
      title: "Evaluate claim record",
      description: "Evaluate a structured claim record against the stop-rule gate selected by its targetDecision. This checks supplied evidence state; it does not independently verify the underlying facts.",
      inputSchema: z.object({ claim: z.record(z.string(), z.unknown()) })
    },
    async ({ claim }) => {
      try {
        const gates = await fetchJson(publicationUrl, "api/v1/gates.json");
        return text(evaluateClaim(claim, gates));
      } catch (error) {
        return fail(error instanceof Error ? error.message : String(error));
      }
    }
  );

  server.registerTool(
    "get_framework",
    {
      title: "Get AI Output to Value framework",
      description: "Return the current six-claim framework and actor-neutral rule from the published machine-readable surface.",
      inputSchema: z.object({})
    },
    async () => {
      try {
        return text(await fetchJson(publicationUrl, "api/v1/framework.json"));
      } catch (error) {
        return fail(error instanceof Error ? error.message : String(error));
      }
    }
  );

  server.registerTool(
    "list_articles",
    {
      title: "List publication articles",
      description: "List articles included in the currently published preview or release artifact.",
      inputSchema: z.object({
        section: z.string().max(80).optional()
      })
    },
    async ({ section }) => {
      try {
        const payload = await fetchJson(publicationUrl, "api/v1/articles.json");
        const wanted = (section || "").trim().toLowerCase();
        const articles = payload.articles.filter((item) => !wanted || `${item.section} ${item.releaseScope}`.toLowerCase().includes(wanted));
        return text({ publicationMode: payload.publicationMode, articles });
      } catch (error) {
        return fail(error instanceof Error ? error.message : String(error));
      }
    }
  );

  server.registerTool(
    "search_claims",
    {
      title: "Search evidence claims",
      description: "Search canonical claim records in the current publication artifact.",
      inputSchema: z.object({
        query: z.string().min(2).max(200),
        limit: z.number().int().min(1).max(20).default(8)
      })
    },
    async ({ query, limit }) => {
      try {
        const payload = await fetchJson(publicationUrl, "api/v1/claims.json");
        const needle = query.toLowerCase();
        const claims = payload.claims
          .filter((claim) => JSON.stringify(claim).toLowerCase().includes(needle))
          .slice(0, limit)
          .map((claim) => ({
            id: claim.id,
            claim_text: claim.claim_text,
            status: claim.status,
            independent_review_status: claim.independent_review_status,
            launch_critical: claim.launch_critical
          }));
        return text({ publicationMode: payload.publicationMode, query, claims });
      } catch (error) {
        return fail(error instanceof Error ? error.message : String(error));
      }
    }
  );

  return server;
}

await serveStdio(() => buildServer());
