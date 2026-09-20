import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// scripts/claim_gate.py ports the `uri` grammar that ajv-formats applies in "full"
// mode. The conformance fixture only proves agreement on the inputs it lists, so this
// test pins the grammar itself: it fails when the installed ajv-formats changes.

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const pythonGate = await readFile(resolve(here, "../../../scripts/claim_gate.py"), "utf8");
const ajvFormatsDir = dirname(require.resolve("ajv-formats"));
const ajvFormats = await readFile(resolve(ajvFormatsDir, "formats.js"), "utf8");
const ajvFormatsVersion = JSON.parse(await readFile(resolve(ajvFormatsDir, "../package.json"), "utf8")).version;

function ajvUri() {
  const grammar = ajvFormats.match(/^const URI = \/(.*)\/(\w*);$/m);
  const precondition = ajvFormats.match(/^const NOT_URI_FRAGMENT = \/(.*)\/(\w*);$/m);
  const wrapper = ajvFormats.match(/^function uri\(str\) \{[\s\S]*?\n\}/m);
  assert.ok(grammar && precondition && wrapper, "ajv-formats no longer defines URI, NOT_URI_FRAGMENT and uri() this way");
  return { grammar, precondition, wrapper: wrapper[0] };
}

function pythonUri() {
  const grammar = pythonGate.match(/_URI_RFC3986 = re\.compile\(\s*r"""\\A([\s\S]*?)\\Z""",\s*re\.IGNORECASE \| re\.ASCII,?\s*\)/);
  assert.ok(grammar, "claim_gate.py no longer defines _URI_RFC3986 in the expected shape");
  return grammar[1];
}

test("claim_gate.py URI grammar is the installed ajv-formats URI grammar", () => {
  const ajv = ajvUri();
  assert.equal(ajv.grammar[2], "i", "ajv-formats URI flags changed; update _URI_RFC3986 flags");
  assert.ok(ajv.grammar[1].startsWith("^") && ajv.grammar[1].endsWith("$"), "ajv-formats URI is no longer anchored with ^ and $");
  const ajvBody = ajv.grammar[1].slice(1, -1);
  assert.equal(
    pythonUri(),
    ajvBody,
    `claim_gate.py _URI_RFC3986 differs from ajv-formats ${ajvFormatsVersion}; re-port it and extend the conformance fixture`
  );
});

test("claim_gate.py keeps the ajv-formats uri() precondition", () => {
  const ajv = ajvUri();
  assert.equal(ajv.precondition[1], "\\/|:", "ajv-formats NOT_URI_FRAGMENT changed");
  assert.match(ajv.wrapper, /NOT_URI_FRAGMENT\.test\(str\) && URI\.test\(str\)/, "ajv-formats uri() no longer ANDs the precondition with the grammar");
  assert.match(pythonGate, /\("\/" in value or ":" in value\) and _URI_RFC3986\.match\(value\) is not None/);
});

test("claim_gate.py records the ajv-formats version it was ported from", () => {
  const recorded = pythonGate.match(/ajv-formats (\d+\.\d+\.\d+)/);
  assert.ok(recorded, "claim_gate.py should name the ajv-formats version");
  assert.equal(recorded[1], ajvFormatsVersion, "ajv-formats was updated: re-check the port and update the version note");
});
