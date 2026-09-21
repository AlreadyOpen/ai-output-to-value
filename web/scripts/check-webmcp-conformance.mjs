// Run the shared claim-gate conformance cases through the real webmcp.js.
//
// webmcp.js is executed under Node with a stub `document`, its base URL pointed at the built
// site/ directory (file: URLs), and the aiov_evaluate_claim_record tool is called for every
// case. That proves the WebMCP surface returns the fixture's verdicts using the built gate.
import { readFile } from "node:fs/promises"
import { resolve } from "node:path"
import { pathToFileURL } from "node:url"
import vm from "node:vm"

import { runConformance } from "../../tests/conformance-harness.mjs"

const repo = resolve(process.cwd(), "..")
const site = pathToFileURL(resolve(repo, "site") + "/").href
const readJson = async (path) => JSON.parse(await readFile(resolve(repo, path), "utf8"))

const tools = []
const document = {
  currentScript: { src: `${site}webmcp.js` },
  scripts: [],
  baseURI: `${site}index.html`,
  modelContext: { registerTool: async (tool) => { tools.push(tool) } },
  querySelector: () => null,
  getElementById: () => null,
}
const window = {
  location: { href: `${site}index.html` },
  addEventListener() {},
  removeEventListener() {},
  dispatchEvent() {},
  setTimeout,
  clearTimeout,
}
async function fileFetch(url) {
  const target = new URL(url)
  if (target.protocol !== "file:") throw new Error(`unexpected non-file fetch: ${url}`)
  // The publication step copies schemas/v1/ into site/schemas/v1/. Read the canonical files
  // when that step has not run, so this check needs only the UI build.
  const canonical = target.pathname.includes("/site/schemas/v1/")
    ? resolve(repo, "schemas/v1", target.pathname.split("/").pop())
    : null
  const text = await readFile(target, "utf8").catch((err) => {
    if (canonical && err.code === "ENOENT") return readFile(canonical, "utf8")
    throw err
  })
  return { ok: true, status: 200, json: async () => JSON.parse(text), text: async () => text }
}

const context = vm.createContext({ window, document, fetch: fileFetch, URL, console, setTimeout, clearTimeout, Date, Math, JSON, Promise })
new vm.Script(await readFile(resolve(repo, "webmcp.js"), "utf8"), {
  filename: resolve(repo, "webmcp.js"),
  importModuleDynamically: vm.constants.USE_MAIN_CONTEXT_DEFAULT_LOADER,
}).runInContext(context)
await new Promise((done) => setTimeout(done, 0))

const tool = tools.find((item) => item.name === "aiov_evaluate_claim_record")
if (!tool) throw new Error("webmcp.js did not register aiov_evaluate_claim_record")

const [fixture, gates] = await Promise.all([
  readJson("tests/fixtures/claim-gate-conformance.json"),
  readJson("schemas/v1/decision-gates.json"),
])

const failures = await runConformance({
  fixture,
  gates,
  evaluate: async (record) => {
    const response = await tool.execute({ claim: record })
    const text = response.content[0].text
    if (response.isError) throw new Error(text)
    return JSON.parse(text)
  },
})

if (failures.length) {
  throw new Error(`webmcp.js disagrees with the conformance fixture:\n- ${failures.join("\n- ")}`)
}
console.log(`webmcp.js passes all ${fixture.cases.length} shared conformance cases through aiov_evaluate_claim_record.`)
