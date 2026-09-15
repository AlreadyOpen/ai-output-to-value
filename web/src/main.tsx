import * as React from "react"
import { createRoot } from "react-dom/client"
import { ArticleTools } from "@/components/article-tools"
import { ClaimGateApp } from "@/components/claim-gate-app"
import "./styles.css"

function mountArticleTools() {
  document.querySelectorAll<HTMLElement>("[data-article-tools]").forEach((host) => {
    if (host.dataset.reactMounted === "true") return
    host.dataset.reactMounted = "true"
    createRoot(host).render(
      <ArticleTools
        mdPath={host.dataset.mdPath || ""}
        sourceUrl={host.dataset.sourceUrl || ""}
        title={host.dataset.title || document.title.replace(/\s+—\s+AI Output to Value$/, "")}
      />,
    )
  })
}

function mountClaimGate() {
  const host = document.getElementById("claim-gate-root")
  if (!host || host.dataset.reactMounted === "true") return
  host.dataset.reactMounted = "true"
  createRoot(host).render(<ClaimGateApp />)
}

mountArticleTools()
mountClaimGate()
