import { readFile } from "node:fs/promises"
import { resolve } from "node:path"

const bundlePath = resolve(process.cwd(), "../site/ui/aiov-ui.js")
const source = await readFile(bundlePath, "utf8")

const forbidden = [
  "process.env.",
  "require(\"react\")",
  "require('react')",
]

const leaked = forbidden.filter((token) => source.includes(token))
if (leaked.length) {
  throw new Error(
    `Browser bundle contains Node-only/runtime-only tokens: ${leaked.join(", ")}. ` +
      "The static GitHub Pages bundle must execute without a Node process/require global.",
  )
}

for (const marker of ["claim-gate-root", "data-article-tools"]) {
  if (!source.includes(marker)) {
    throw new Error(`Browser bundle is missing expected mount marker: ${marker}`)
  }
}

console.log("Browser bundle smoke check passed: no Node globals leaked and mount points are present.")
