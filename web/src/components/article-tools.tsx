import * as React from "react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLink,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

type Props = {
  mdPath: string
  sourceUrl: string
  title: string
  repo: string
}

function providerUrl(provider: string, prompt: string, repo: string) {
  if (provider === "chatgpt") {
    return `https://chatgpt.com/?${new URLSearchParams({ hints: "search", prompt }).toString()}`
  }
  if (provider === "claude") {
    return `https://claude.ai/new?${new URLSearchParams({ q: prompt }).toString()}`
  }
  if (provider === "t3") {
    return `https://t3.chat/new?${new URLSearchParams({ q: prompt }).toString()}`
  }
  if (provider === "cursor") {
    return `https://cursor.com/link/prompt?${new URLSearchParams({ text: prompt }).toString()}`
  }
  if (provider === "copilot") {
    const open = `ghapp://session/new?${new URLSearchParams({ repo, mode: "interactive", prompt }).toString()}`
    return `https://github.com/copilot/app/launch?${new URLSearchParams({ open }).toString()}`
  }
  return "#"
}

async function copyText(text: string) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text)
    return
  }
  const textarea = document.createElement("textarea")
  textarea.value = text
  textarea.setAttribute("readonly", "")
  textarea.style.position = "fixed"
  textarea.style.opacity = "0"
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand("copy")
  textarea.remove()
}

export function ArticleTools({ mdPath, sourceUrl, title, repo }: Props) {
  const [copyLabel, setCopyLabel] = React.useState("Copy MD")
  const mdUrl = new URL(mdPath, window.location.href).toString()
  const pageUrl = window.location.href.split("#")[0]
  const prompt = [
    `Read and discuss the AI Output to Value page \"${title}\".`,
    "Use the published Markdown as the primary source, preserve its evidence qualifications and publication status, and distinguish source claims from your own inference.",
    `Markdown: ${mdUrl}`,
    `Page: ${pageUrl}`,
  ].join("\n")

  async function copyMarkdown() {
    try {
      const response = await fetch(mdUrl, { cache: "no-store" })
      if (!response.ok) throw new Error(`Markdown request failed: ${response.status}`)
      await copyText(await response.text())
      setCopyLabel("Copied MD")
    } catch (error) {
      console.error(error)
      setCopyLabel("Copy failed")
    } finally {
      window.setTimeout(() => setCopyLabel("Copy MD"), 1600)
    }
  }

  return (
    <div className="aiov-react-toolbar" data-aiov-interactive-only>
      <Button variant="outline" size="sm" onClick={copyMarkdown}>
        {copyLabel}
      </Button>
      <DropdownMenu>
        <DropdownMenuTrigger render={<Button variant="outline" size="sm" />}>
          Open in <span aria-hidden="true">⌄</span>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onClick={() => void copyText(mdUrl)}>Copy MD link</DropdownMenuItem>
          <DropdownMenuLink render={<a href={mdUrl} target="_blank" rel="noreferrer" />}>
            Open Markdown
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={sourceUrl} target="_blank" rel="noreferrer" />}>
            GitHub
          </DropdownMenuLink>
          <DropdownMenuSeparator />
          <DropdownMenuLink render={<a href={providerUrl("chatgpt", prompt, repo)} target="_blank" rel="noreferrer" />}>
            ChatGPT
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("claude", prompt, repo)} target="_blank" rel="noreferrer" />}>
            Claude
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("t3", prompt, repo)} target="_blank" rel="noreferrer" />}>
            T3 Chat
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("copilot", prompt, repo)} target="_blank" rel="noreferrer" />}>
            GitHub Copilot
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("cursor", prompt, repo)} target="_blank" rel="noreferrer" />}>
            Cursor
          </DropdownMenuLink>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
