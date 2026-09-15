import * as React from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"

type CheckState = "unknown" | "pass" | "fail"
type GateCheck = { id: string; label: string }
type GateRule = {
  label: string
  description: string
  requiredClaimLevel: ClaimLevel
  requiredChecks: GateCheck[]
}
type GateRules = { decisions: Record<string, GateRule> }
type ClaimLevel = "01-access" | "02-output" | "03-deliverable" | "04-capability" | "05-outcome" | "06-value"

type FormState = {
  project: string
  decision: string
  assertedClaim: ClaimLevel
  intendedUse: string
  workflowBoundary: string
  workflowCompletion: string
  downstreamHandoffs: string
  movedBottleneck: string
  unhappyPath: string
  actor: string
  channel: string
  authority: string
  accountability: string
  evidence: string
  nextEvidence: string
  stopRule: string
  checks: Record<string, CheckState>
}

const claimLabels: Record<ClaimLevel, string> = {
  "01-access": "01 Access",
  "02-output": "02 Output",
  "03-deliverable": "03 Deliverable",
  "04-capability": "04 Capability",
  "05-outcome": "05 Outcome",
  "06-value": "06 Value",
}

const claimOptions = Object.entries(claimLabels).map(([value, label]) => ({ value: value as ClaimLevel, label }))
const actorOptions = [
  { value: "human", label: "Human" },
  { value: "ai-agent", label: "AI agent" },
  { value: "deterministic-system", label: "Deterministic system" },
  { value: "specialist-tool", label: "Specialist tool" },
  { value: "hybrid", label: "Hybrid" },
]
const channelOptions = [
  { value: "human-ui", label: "Human UI" },
  { value: "webmcp", label: "WebMCP" },
  { value: "mcp", label: "MCP" },
  { value: "api", label: "API" },
  { value: "cli", label: "CLI" },
  { value: "ide-agent", label: "IDE agent" },
  { value: "other-agent-tool", label: "Other agent tool" },
  { value: "hybrid", label: "Hybrid" },
  { value: "other", label: "Other" },
]
const checkOptions = [
  { value: "unknown", label: "Unknown / not evidenced" },
  { value: "pass", label: "Pass" },
  { value: "fail", label: "Fail" },
]

function lines(value: string) {
  return value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean)
}

function NativeFieldSelect({
  value,
  options,
  onChange,
  ariaLabel,
}: {
  value: string
  options: { value: string; label: string }[]
  onChange: (value: string) => void
  ariaLabel: string
}) {
  return (
    <Select value={value} onValueChange={(next) => onChange(String(next))} items={options}>
      <SelectTrigger aria-label={ariaLabel}>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {options.map((item) => (
          <SelectItem key={item.value} value={item.value}>
            {item.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}

function Field({ label, children, full = false }: { label: string; children: React.ReactNode; full?: boolean }) {
  return (
    <div className={cn("grid gap-2", full && "md:col-span-2")}>
      <Label>{label}</Label>
      {children}
    </div>
  )
}

export function ClaimGateApp() {
  const [gates, setGates] = React.useState<GateRules | null>(null)
  const [loadError, setLoadError] = React.useState<string | null>(null)
  const [state, setState] = React.useState<FormState>({
    project: "",
    decision: "",
    assertedClaim: "02-output",
    intendedUse: "",
    workflowBoundary: "",
    workflowCompletion: "",
    downstreamHandoffs: "",
    movedBottleneck: "",
    unhappyPath: "",
    actor: "ai-agent",
    channel: "human-ui",
    authority: "",
    accountability: "",
    evidence: "",
    nextEvidence: "",
    stopRule: "",
    checks: {},
  })

  React.useEffect(() => {
    fetch("../schemas/v1/decision-gates.json")
      .then(async (response) => {
        if (!response.ok) throw new Error(`Gate rules returned HTTP ${response.status}`)
        return (await response.json()) as GateRules
      })
      .then((payload) => {
        const firstDecision = Object.keys(payload.decisions)[0]
        const firstRule = payload.decisions[firstDecision]
        const checks = Object.fromEntries(firstRule.requiredChecks.map((check) => [check.id, "unknown"])) as Record<string, CheckState>
        setGates(payload)
        setState((previous) => ({
          ...previous,
          decision: firstDecision,
          assertedClaim: firstRule.requiredClaimLevel,
          checks,
        }))
      })
      .catch((error) => setLoadError(error instanceof Error ? error.message : String(error)))
  }, [])

  const rule = gates && state.decision ? gates.decisions[state.decision] : null

  function updateDecision(decision: string) {
    if (!gates) return
    const next = gates.decisions[decision]
    setState((previous) => ({
      ...previous,
      decision,
      assertedClaim: next.requiredClaimLevel,
      checks: Object.fromEntries(next.requiredChecks.map((check) => [check.id, "unknown"])) as Record<string, CheckState>,
    }))
  }

  function metadataGaps() {
    const gaps: string[] = []
    if (!state.project.trim()) gaps.push("Project / initiative is not named.")
    if (!state.intendedUse.trim()) gaps.push("Intended use is not defined.")
    if (!state.authority.trim()) gaps.push("Authority boundary is not recorded.")
    if (!state.accountability.trim()) gaps.push("Accountability / recourse is not recorded.")
    if (!state.nextEvidence.trim()) gaps.push("Next evidence is not recorded.")
    if (!state.stopRule.trim()) gaps.push("Stop rule is not recorded.")
    return gaps
  }

  const failed = rule?.requiredChecks.filter((check) => state.checks[check.id] === "fail") ?? []
  const unknown = rule?.requiredChecks.filter((check) => (state.checks[check.id] ?? "unknown") === "unknown") ?? []
  const gaps = metadataGaps()
  const claimMismatch = Boolean(rule && state.assertedClaim !== rule.requiredClaimLevel)
  const status = loadError
    ? "TOOL_ERROR"
    : failed.length
      ? "BLOCKED"
      : unknown.length || gaps.length || claimMismatch || !rule
        ? "INSUFFICIENT_EVIDENCE"
        : "PASS"

  const reasons = [
    ...failed.map((check) => `Failed: ${check.label}`),
    ...unknown.map((check) => `Missing/unknown evidence: ${check.label}`),
    ...gaps,
    ...(claimMismatch && rule
      ? [`The asserted claim (${claimLabels[state.assertedClaim]}) does not match the claim required by this target decision (${claimLabels[rule.requiredClaimLevel]}).`]
      : []),
  ]
  if (!reasons.length && status === "PASS") reasons.push("All required checks and decision-record fields are present.")

  function record() {
    if (!rule) return null
    return {
      $schema: new URL("../schemas/v1/claim.schema.json", window.location.href).href,
      schemaVersion: "1.0",
      project: state.project.trim(),
      targetDecision: state.decision,
      requiredClaimLevel: rule.requiredClaimLevel,
      assertedClaimLevel: state.assertedClaim,
      intendedUse: state.intendedUse.trim(),
      workflowBoundary: state.workflowBoundary.trim(),
      workflowCompletion: state.workflowCompletion.trim(),
      downstreamHandoffs: lines(state.downstreamHandoffs),
      movedBottleneck: state.movedBottleneck.trim(),
      unhappyPath: state.unhappyPath.trim(),
      actors: [{ type: state.actor, role: "Primary actor for the assessed workflow", interactionChannel: state.channel }],
      authority: state.authority.trim(),
      accountability: state.accountability.trim(),
      evidenceRefs: lines(state.evidence),
      gateChecks: state.checks,
      nextEvidence: state.nextEvidence.trim(),
      stopRule: state.stopRule.trim(),
    }
  }

  function markdownSummary() {
    const item = record()
    if (!item || !rule) return ""
    const rows = rule.requiredChecks.map((check) => `- **${(item.gateChecks[check.id] || "unknown").toUpperCase()}** — ${check.label}`).join("\n")
    return `# AI Output to Value — decision gate\n\n**Project:** ${item.project || "(not supplied)"}\n\n**Target decision:** ${rule.label}\n\n**Required claim:** ${claimLabels[item.requiredClaimLevel]}\n\n**Asserted claim:** ${claimLabels[item.assertedClaimLevel]}\n\n**Gate status:** ${status.replaceAll("_", " ")}\n\n## Intended use\n\n${item.intendedUse || "(not supplied)"}\n\n## Workflow boundary\n\n**Start / boundary:** ${item.workflowBoundary || "(not supplied)"}\n\n**What counts as complete:** ${item.workflowCompletion || "(not supplied)"}\n\n**Downstream handoffs:**\n${item.downstreamHandoffs.length ? item.downstreamHandoffs.map((x) => `- ${x}`).join("\n") : "(none supplied)"}\n\n**Where could the bottleneck move?** ${item.movedBottleneck || "(not supplied)"}\n\n**Unhappy path:** ${item.unhappyPath || "(not supplied)"}\n\n## Required checks\n\n${rows}\n\n## Authority\n\n${item.authority || "(not supplied)"}\n\n## Accountability / recourse\n\n${item.accountability || "(not supplied)"}\n\n## Evidence references\n\n${item.evidenceRefs.length ? item.evidenceRefs.map((x) => `- ${x}`).join("\n") : "(none supplied)"}\n\n## Next evidence\n\n${item.nextEvidence || "(not supplied)"}\n\n## Stop rule\n\n${item.stopRule || "(not supplied)"}\n`
  }

  async function copyMarkdown() {
    await navigator.clipboard.writeText(markdownSummary())
  }

  function downloadJson() {
    const item = record()
    if (!item) return
    const blob = new Blob([JSON.stringify(item, null, 2)], { type: "application/json" })
    const href = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = href
    link.download = `${item.project || "claim"}.claim.json`
    link.click()
    window.setTimeout(() => URL.revokeObjectURL(href), 1000)
  }

  const decisionOptions = gates
    ? Object.entries(gates.decisions).map(([value, item]) => ({ value, label: `${item.label} — ${claimLabels[item.requiredClaimLevel]}` }))
    : []

  return (
    <main className="aiov-gate-root">
      <div className="mb-8 max-w-3xl">
        <Badge className="mb-3">Interactive decision tool</Badge>
        <h1 className="font-serif text-4xl font-semibold tracking-tight md:text-5xl">Claim gate</h1>
        <p className="mt-4 text-lg text-muted-foreground">
          Choose the decision you are trying to make. The target decision selects the minimum claim and required checks. <strong className="text-foreground">This is a stop rule, not a maturity score.</strong>
        </p>
        <p className="mt-2 text-sm text-muted-foreground">The evaluator is actor-neutral: human, AI, automated and hybrid work use the same gate for the same intended decision.</p>
        <p className="mt-2 text-sm text-muted-foreground"><strong className="text-foreground">Workflow is not a seventh claim.</strong> The optional workflow fields make the end-to-end process boundary visible without changing the deterministic gate score.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <Card>
          <CardHeader>
            <CardTitle>Decision record</CardTitle>
            <CardDescription>Record only the evidence needed for the decision you are actually making.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-5 md:grid-cols-2">
            <Field label="Project / initiative">
              <Input value={state.project} onChange={(event) => setState({ ...state, project: event.target.value })} placeholder="e.g. auto-triage-bot" />
            </Field>
            <Field label="Decision sought">
              <NativeFieldSelect value={state.decision} options={decisionOptions} onChange={updateDecision} ariaLabel="Decision sought" />
            </Field>
            <Field label="Claim being asserted">
              <NativeFieldSelect
                value={state.assertedClaim}
                options={claimOptions}
                onChange={(value) => setState({ ...state, assertedClaim: value as ClaimLevel })}
                ariaLabel="Claim being asserted"
              />
            </Field>
            <Field label="Primary actor">
              <NativeFieldSelect value={state.actor} options={actorOptions} onChange={(value) => setState({ ...state, actor: value })} ariaLabel="Primary actor" />
            </Field>
            <Field label="Interaction channel">
              <NativeFieldSelect value={state.channel} options={channelOptions} onChange={(value) => setState({ ...state, channel: value })} ariaLabel="Interaction channel" />
            </Field>
            <Field label="Intended use" full>
              <Textarea value={state.intendedUse} onChange={(event) => setState({ ...state, intendedUse: event.target.value })} placeholder="What will someone rely on this for?" />
            </Field>

            <div className="md:col-span-2 mt-2 rounded-lg border border-border bg-muted/30 p-4">
              <h2 className="text-lg font-semibold">Workflow boundary <span className="text-sm font-normal text-muted-foreground">(optional; not another gate score)</span></h2>
              <p className="mt-1 text-sm text-muted-foreground">Describe the end-to-end process when local task or product completion is not the same as business delivery.</p>
            </div>
            <Field label="Where does the workflow start?" full>
              <Textarea value={state.workflowBoundary} onChange={(event) => setState({ ...state, workflowBoundary: event.target.value })} placeholder="Trigger, request, input, customer need, incident, order…" />
            </Field>
            <Field label="What counts as actually complete?" full>
              <Textarea value={state.workflowCompletion} onChange={(event) => setState({ ...state, workflowCompletion: event.target.value })} placeholder="Describe the accepted end state, not only the local artefact or task." />
            </Field>
            <Field label="Downstream handoffs / verification / integration / operation / support" full>
              <Textarea value={state.downstreamHandoffs} onChange={(event) => setState({ ...state, downstreamHandoffs: event.target.value })} placeholder="One downstream step per line." />
            </Field>
            <Field label="Where could the bottleneck move?" full>
              <Textarea value={state.movedBottleneck} onChange={(event) => setState({ ...state, movedBottleneck: event.target.value })} placeholder="If this task becomes much faster, which downstream constraint may become dominant?" />
            </Field>
            <Field label="Unhappy path / escalation / stop / reversal / recovery" full>
              <Textarea value={state.unhappyPath} onChange={(event) => setState({ ...state, unhappyPath: event.target.value })} placeholder="What happens with missing information, ambiguity, dependency failure, refusal, timeout, or an action that must be reversed?" />
            </Field>

            <Field label="Authority boundary" full>
              <Textarea value={state.authority} onChange={(event) => setState({ ...state, authority: event.target.value })} placeholder="What may this actor recommend, change, send, spend, approve or commit?" />
            </Field>
            <Field label="Accountability / recourse" full>
              <Textarea value={state.accountability} onChange={(event) => setState({ ...state, accountability: event.target.value })} placeholder="Which organisational or legal party must answer for failures and provide correction?" />
            </Field>
            <Field label="Evidence references" full>
              <Textarea value={state.evidence} onChange={(event) => setState({ ...state, evidence: event.target.value })} placeholder="One reference per line: eval result, test run, incident record, source, measurement…" />
            </Field>
            <Field label="Next evidence that would change the decision" full>
              <Textarea value={state.nextEvidence} onChange={(event) => setState({ ...state, nextEvidence: event.target.value })} />
            </Field>
            <Field label="Stop rule" full>
              <Textarea value={state.stopRule} onChange={(event) => setState({ ...state, stopRule: event.target.value })} placeholder="What result, date, cost or risk threshold makes you stop or restrict the work?" />
            </Field>

            <div className="md:col-span-2 mt-2">
              <h2 className="text-xl font-semibold">Required checks</h2>
              <p className="mt-1 text-sm text-muted-foreground">{rule?.description ?? "Loading gate rules…"}</p>
              <div className="mt-4 divide-y divide-border rounded-lg border border-border">
                {rule?.requiredChecks.map((check) => (
                  <div key={check.id} className="grid gap-3 p-4 md:grid-cols-[minmax(0,1fr)_13rem] md:items-center">
                    <Label>{check.label}</Label>
                    <NativeFieldSelect
                      value={state.checks[check.id] ?? "unknown"}
                      options={checkOptions}
                      onChange={(value) => setState({ ...state, checks: { ...state.checks, [check.id]: value as CheckState } })}
                      ariaLabel={check.label}
                    />
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="h-fit lg:sticky lg:top-24" aria-live="polite">
          <CardHeader>
            <Badge>Decision gate</Badge>
            <CardTitle>{rule ? `Required claim: ${claimLabels[rule.requiredClaimLevel]}` : "Required claim"}</CardTitle>
          </CardHeader>
          <CardContent>
            <div
              className={cn(
                "rounded-lg px-4 py-3 text-sm font-bold",
                status === "PASS" && "bg-emerald-50 text-emerald-800",
                status === "BLOCKED" && "bg-red-50 text-red-800",
                status === "INSUFFICIENT_EVIDENCE" && "bg-amber-50 text-amber-800",
                status === "TOOL_ERROR" && "bg-red-50 text-red-800",
              )}
            >
              {status.replaceAll("_", " ")}
            </div>
            <p className="mt-4 text-sm text-muted-foreground">
              {loadError
                ? loadError
                : status === "PASS"
                  ? `The supplied record satisfies every check required for ${rule?.label}. This does not prove facts beyond the supplied evidence.`
                  : status === "BLOCKED"
                    ? "At least one decision-critical check explicitly failed. Strength at other claim levels does not offset it."
                    : "No decision-critical check is recorded as failed, but the record is not sufficient to justify this decision."}
            </p>
            <ul className="mt-4 list-disc space-y-2 pl-5 text-sm">
              {reasons.map((reason) => <li key={reason}>{reason}</li>)}
            </ul>
            <p className="mt-4 text-sm text-muted-foreground">Strong Access or Output cannot compensate for a failed decision-critical check.</p>
            <div className="mt-5 flex flex-wrap gap-2" data-aiov-interactive-only>
              <Button size="sm" onClick={() => void copyMarkdown()}>Copy Markdown</Button>
              <Button size="sm" variant="outline" onClick={downloadJson}>Download JSON</Button>
              <Button size="sm" variant="outline" onClick={() => window.print()}>Print</Button>
            </div>
            <p className="mt-5 text-xs text-muted-foreground">
              <a className="underline" href="../schemas/v1/claim.schema.json">claim.schema.json</a> · {" "}
              <a className="underline" href="../schemas/v1/decision-gates.json">gate rules</a> · {" "}
              <a className="underline" href="../articles/claim-card.html">claim-card guidance</a>
            </p>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
