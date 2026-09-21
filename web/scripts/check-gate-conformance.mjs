// Run the shared claim-gate conformance cases against the built browser bundle, so the
// code that ships to the browser is the code the fixture proves.
import { readFile } from "node:fs/promises"
import { resolve } from "node:path"
import { pathToFileURL } from "node:url"

import { runConformance } from "../../tests/conformance-harness.mjs"

const repo = resolve(process.cwd(), "..")
const readJson = async (path) => JSON.parse(await readFile(resolve(repo, path), "utf8"))

const core = await import(pathToFileURL(resolve(repo, "site/ui/gate-core.js")).href)
const [fixture, gates, claimSchema] = await Promise.all([
  readJson("tests/fixtures/claim-gate-conformance.json"),
  readJson("schemas/v1/decision-gates.json"),
  readJson("schemas/v1/claim.schema.json"),
])

const failures = await runConformance({
  fixture,
  gates,
  evaluate: (record) => core.evaluateClaim(record, gates, claimSchema),
})

if (failures.length) {
  throw new Error(`Browser gate bundle disagrees with the conformance fixture:\n- ${failures.join("\n- ")}`)
}
console.log(`Browser gate bundle passes all ${fixture.cases.length} shared conformance cases.`)
