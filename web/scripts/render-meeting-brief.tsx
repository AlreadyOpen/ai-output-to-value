import { mkdir, writeFile } from "node:fs/promises"
import { resolve } from "node:path"
import { render } from "takumi-pdf"
import { PdfcnThemeProvider } from "../src/components/pdf/theme-provider"
import { Text } from "../src/components/pdf/text/text"
import { Section } from "../src/components/pdf/section/section"
import { Stack } from "../src/components/pdf/stack/stack"
import { Badge } from "../src/components/pdf/badge/badge"
import { Divider } from "../src/components/pdf/divider/divider"

const questions = [
  "What exactly have we demonstrated?",
  "What did the AI know, and what did it infer?",
  "What remains before the intended use?",
  "Which work disappeared, moved elsewhere, or became the next workflow bottleneck?",
  "Which actor or combination performs this task or decision best?",
  "Where do authority, accountability, verification, operation and support sit?",
  "Which business outcome are we trying to change—including learning or uncertainty removed?",
  "What evidence would justify the next decision, and when should we stop?",
]

const thresholds = [
  ["Explore", "Output", "Reproduce the artefact/action and learn."],
  ["Rely", "Deliverable", "Fit for the named use and acceptance criteria."],
  ["Operate / sell", "Capability", "Owners, controls, fallback and operating process."],
  ["Measure change", "Outcome", "Named measure moved versus a baseline."],
  ["Scale / renew / stop", "Value", "Outcome is worth relevant cost, risk and alternatives."],
]

function MeetingBrief() {
  return (
    <PdfcnThemeProvider>
      <Stack gap="xs">
        <div tw="flex items-center justify-between">
          <div tw="flex flex-col">
            <Text>AI Output to Value</Text>
            <Text>One-page meeting brief</Text>
          </div>
          <Badge>Decision tool</Badge>
        </div>
        <Divider />

        <Section spacing="xs">
          <Text>Start with the decision, not the taxonomy</Text>
          <div tw="mt-1 flex flex-col gap-1">
            {thresholds.map(([decision, claim, evidence]) => (
              <div key={decision} tw="flex gap-2 rounded border border-gray-200 px-2 py-0.5">
                <Text>{decision}</Text>
                <Text>{claim}</Text>
                <Text>{evidence}</Text>
              </div>
            ))}
          </div>
          <Text>Do not average claims. A missing decision-critical claim is not offset by strength elsewhere.</Text>
          <Text>Workflow test: outcome, end-to-end boundary, next bottleneck, unhappy path, outcome metric. Workflow is the process boundary—not a seventh claim.</Text>
          <Text>Management-word test: workflow, teamwork, KPI, productivity, leadership and alignment need an explicit process, role, metric, quality boundary or claimed outcome.</Text>
        </Section>

        <Section spacing="xs">
          <Text>Eight questions</Text>
          <div tw="mt-1 grid grid-cols-2 gap-x-4 gap-y-0.5">
            {questions.map((question, index) => (
              <Text key={question}>{index + 1}. {question}</Text>
            ))}
          </div>
        </Section>

        <Section spacing="xs">
          <Text>Decision record</Text>
          <div tw="mt-1 grid grid-cols-2 gap-x-4 gap-y-0.5">
            <Text>Established: __________________________</Text>
            <Text>Not established: ______________________</Text>
            <Text>Workflow / unhappy path: ______________</Text>
            <Text>Teamwork / KPI / productivity: _________</Text>
            <Text>Actor / interface / authority: __________</Text>
            <Text>Accountability / recourse: _____________</Text>
            <Text>Next evidence / stop rule: _____________</Text>
          </div>
        </Section>

        <Divider />
        <Text>Use AI ambitiously. Keep the claims clear. Human, AI, automated and hybrid work use the same intended-use and evidence standard.</Text>
      </Stack>
    </PdfcnThemeProvider>
  )
}

const pdf = await render(<MeetingBrief />, {
  size: "a4",
  margin: { top: 22, right: 28, bottom: 22, left: 28 },
  tagged: true,
  lang: "en",
  metadata: {
    title: "AI Output to Value — One-page meeting brief",
    authors: ["AlreadyOpen"],
  },
})

const outputDir = resolve(process.cwd(), "../site/downloads")
await mkdir(outputDir, { recursive: true })
await writeFile(resolve(outputDir, "ai-output-to-value-meeting-brief.pdf"), pdf)
console.log("Generated site/downloads/ai-output-to-value-meeting-brief.pdf using pdfcn + Takumi")
