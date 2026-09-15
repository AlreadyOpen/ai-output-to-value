(() => {
  "use strict";

  const toolbar = document.querySelector("[data-article-tools]");
  if (!toolbar) return;

  const mdUrl = new URL(toolbar.dataset.mdPath || "", window.location.href).toString();
  const sourceUrl = toolbar.dataset.sourceUrl || "";
  const pageUrl = window.location.href.split("#")[0];
  const title = toolbar.dataset.title || document.title.replace(/\s+—\s+AI Output to Value$/, "");
  const repo = toolbar.dataset.repo || "AlreadyOpen/ai-output-to-value";

  const prompt = [
    `Read and discuss the AI Output to Value page \"${title}\".`,
    "Use the published Markdown as the primary source, preserve its evidence qualifications and publication status, and distinguish source claims from your own inference.",
    `Markdown: ${mdUrl}`,
    `Page: ${pageUrl}`,
  ].join("\n");

  function providerUrl(provider) {
    const encodedPrompt = encodeURIComponent(prompt);
    if (provider === "chatgpt") {
      const params = new URLSearchParams({ hints: "search", prompt });
      return `https://chatgpt.com/?${params.toString()}`;
    }
    if (provider === "claude") {
      return `https://claude.ai/new?${new URLSearchParams({ q: prompt }).toString()}`;
    }
    if (provider === "t3") {
      return `https://t3.chat/new?${new URLSearchParams({ q: prompt }).toString()}`;
    }
    if (provider === "cursor") {
      return `https://cursor.com/link/prompt?${new URLSearchParams({ text: prompt }).toString()}`;
    }
    if (provider === "copilot") {
      const appLink = `ghapp://session/new?${new URLSearchParams({ repo, mode: "interactive", prompt }).toString()}`;
      return `https://github.com/copilot/app/launch?${new URLSearchParams({ open: appLink }).toString()}`;
    }
    return "#";
  }

  async function copyText(text) {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
  }

  function flash(button, successText) {
    const original = button.dataset.originalLabel || button.textContent;
    button.dataset.originalLabel = original;
    button.textContent = successText;
    window.setTimeout(() => {
      button.textContent = original;
    }, 1600);
  }

  const copyMd = toolbar.querySelector("[data-copy-md]");
  if (copyMd) {
    copyMd.addEventListener("click", async () => {
      try {
        const response = await fetch(mdUrl, { cache: "no-store" });
        if (!response.ok) throw new Error(`Markdown request failed: ${response.status}`);
        await copyText(await response.text());
        flash(copyMd, "Copied MD");
      } catch (error) {
        console.error(error);
        flash(copyMd, "Copy failed");
      }
    });
  }

  const copyMdLink = toolbar.querySelector("[data-copy-md-link]");
  if (copyMdLink) {
    copyMdLink.addEventListener("click", async () => {
      try {
        await copyText(mdUrl);
        flash(copyMdLink, "Copied MD link");
        copyMdLink.closest("details")?.removeAttribute("open");
      } catch (error) {
        console.error(error);
        flash(copyMdLink, "Copy failed");
      }
    });
  }

  toolbar.querySelectorAll("[data-open-provider]").forEach((link) => {
    link.href = providerUrl(link.dataset.openProvider);
  });

  const github = toolbar.querySelector("[data-open-github]");
  if (github && sourceUrl) github.href = sourceUrl;

  const openMarkdown = toolbar.querySelector("[data-open-markdown]");
  if (openMarkdown) openMarkdown.href = mdUrl;

  document.addEventListener("click", (event) => {
    const details = toolbar.querySelector("details[open]");
    if (details && !details.contains(event.target)) details.removeAttribute("open");
  });
})();
