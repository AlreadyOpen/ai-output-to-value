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
}

type Provider = "chatgpt" | "claude" | "t3" | "copilot" | "cursor"

function providerUrl(provider: Provider, mdUrl: string) {
  // Match the Better Auth docs interaction pattern: pass the stable published
  // Markdown URL and a short instruction, rather than embedding article text
  // or inventing provider-specific repo/session state.
  const prompt = `Read ${mdUrl}, I want to ask questions about it.`
  if (provider === "chatgpt") {
    return `https://chatgpt.com/?${new URLSearchParams({ hints: "search", q: prompt }).toString()}`
  }
  if (provider === "claude") {
    return `https://claude.ai/new?${new URLSearchParams({ q: prompt }).toString()}`
  }
  if (provider === "t3") {
    return `https://t3.chat/new?${new URLSearchParams({ q: prompt }).toString()}`
  }
  if (provider === "copilot") {
    return `https://copilot.microsoft.com/?${new URLSearchParams({ q: prompt }).toString()}`
  }
  return `https://cursor.com/link/prompt?${new URLSearchParams({ text: prompt }).toString()}`
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

export function ArticleTools({ mdPath, sourceUrl }: Props) {
  const [copyLabel, setCopyLabel] = React.useState("Copy MD")
  const mdUrl = new URL(mdPath, window.location.href).toString()

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
          <DropdownMenuLink render={<a href={sourceUrl} target="_blank" rel="noreferrer noopener" />}>
            GitHub
          </DropdownMenuLink>
          <DropdownMenuSeparator />
          <DropdownMenuLink render={<a href={providerUrl("chatgpt", mdUrl)} target="_blank" rel="noreferrer noopener" />}>
            ChatGPT
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("claude", mdUrl)} target="_blank" rel="noreferrer noopener" />}>
            Claude
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("t3", mdUrl)} target="_blank" rel="noreferrer noopener" />}>
            T3 Chat
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("copilot", mdUrl)} target="_blank" rel="noreferrer noopener" />}>
            Copilot
          </DropdownMenuLink>
          <DropdownMenuLink render={<a href={providerUrl("cursor", mdUrl)} target="_blank" rel="noreferrer noopener" />}>
            Cursor
          </DropdownMenuLink>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
