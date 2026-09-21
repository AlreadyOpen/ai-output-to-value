// Exhaustively check the page's verdict rule against the shared gate's status, so the page
// cannot show PASS unless the gate would, or BLOCKED without a failed check or a gate BLOCK.
import { formVerdict, type FormStatus } from "../src/lib/verdict"

const gateStatuses: (FormStatus | null)[] = [null, "PASS", "BLOCKED", "INSUFFICIENT_EVIDENCE"]
const problems: string[] = []
let checked = 0

for (const failedCount of [0, 1])
  for (const unknownCount of [0, 1])
    for (const gapCount of [0, 1])
      for (const claimMismatch of [false, true])
        for (const hasRule of [false, true])
          for (const gateStatus of gateStatuses) {
            const input = { failedCount, unknownCount, gapCount, claimMismatch, hasRule, gateStatus }
            const status = formVerdict(input)
            checked += 1
            const label = JSON.stringify(input)
            if (status === "PASS" && (gateStatus !== "PASS" || failedCount || unknownCount || gapCount || claimMismatch || !hasRule)) {
              problems.push(`PASS shown without a gate PASS and a complete form: ${label}`)
            }
            if (status === "BLOCKED" && !failedCount && gateStatus !== "BLOCKED") {
              problems.push(`BLOCKED shown without a failed check or a gate BLOCK: ${label}`)
            }
            if (failedCount && status !== "BLOCKED") problems.push(`failed check not BLOCKED: ${label}`)
          }

if (problems.length) throw new Error(`UI verdict rule is unsound:\n- ${problems.join("\n- ")}`)
console.log(`UI verdict rule holds for all ${checked} input combinations.`)
