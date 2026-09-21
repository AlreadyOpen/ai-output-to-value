// The Claim Gate page's verdict for the form being edited.
//
// While a form is incomplete the page says INSUFFICIENT_EVIDENCE and lists what is missing,
// because an unfilled field is not a malformed record. Once the form is complete the verdict
// is the shared gate's verdict for the record the form exports, so the page can never show a
// PASS that the CLI, the MCP server, WebMCP or the Action would not also return.

export type FormStatus = "PASS" | "BLOCKED" | "INSUFFICIENT_EVIDENCE"

export type VerdictInput = {
  failedCount: number
  unknownCount: number
  gapCount: number
  claimMismatch: boolean
  hasRule: boolean
  /** Status the shared gate returns for the exported record, or null if it could not run. */
  gateStatus: FormStatus | null
}

export function formVerdict(input: VerdictInput): FormStatus {
  if (input.failedCount) return "BLOCKED"
  if (input.unknownCount || input.gapCount || input.claimMismatch || !input.hasRule) return "INSUFFICIENT_EVIDENCE"
  return input.gateStatus ?? "INSUFFICIENT_EVIDENCE"
}
