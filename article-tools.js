(() => {
  "use strict";

  const toolbar = document.querySelector("[data-article-tools]");
  if (!toolbar) return;

  const mdUrl = new URL(toolbar.dataset.mdPath || "", window.location.href).toString();
  const sourceUrl = toolbar.dataset.sourceUrl || "";
  const prompt = `Read ${mdUrl}, I want to ask questions about it.`;

  function providerUrl(provider) {
    if (provider === "chatgpt") {
      return `https://chatgpt.com/?${new URLSearchParams({ hints: "search", q: prompt }).toString()}`;
    }
    if (provider === "claude") {
      return `https://claude.ai/new?${new URLSearchParams({ q: prompt }).toString()}`;
    }
    if (provider === "t3") {
      return `https://t3.chat/new?${new URLSearchParams({ q: prompt }).toString()}`;
    }
    if (provider === "copilot") {
      return `https://copilot.microsoft.com/?${new URLSearchParams({ q: prompt }).toString()}`;
    }
    if (provider === "cursor") {
      return `https://cursor.com/link/prompt?${new URLSearchParams({ text: prompt }).toString()}`;
    }
    throw new Error(`Unknown open-in provider: ${provider}`);
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

  document.addEventListener("click", (event) => {
    const details = toolbar.querySelector("details[open]");
    if (details && !details.contains(event.target)) details.removeAttribute("open");
  });
})();
