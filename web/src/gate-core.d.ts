declare module "@gate-core" {
  export interface GateResult {
    status: "PASS" | "BLOCKED" | "INSUFFICIENT_EVIDENCE"
    targetDecision: string | null
    structuralErrors: string[]
    missingFields: string[]
    claimMismatch: boolean
    failedChecks: { id: string; label: string; state: string }[]
    unknownChecks: { id: string; label: string; state: string }[]
    passedChecks: { id: string; label: string; state: string }[]
    gateVersion: string | null
    principle: string | null
    [key: string]: unknown
  }
  export function evaluateClaim(record: unknown, gates: unknown, claimSchema: unknown): GateResult
  export function getStopRule(gates: unknown, decisionType: string): Record<string, unknown>
}
