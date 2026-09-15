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
  "Which work disappeared, and which work moved elsewhere?",
  "Which actor or combination performs this task or decision best?",
  "Where do authority, accountability, verification, operation and support sit?",
  "Which business outcome are we trying to change—including learning or uncertainty removed?",
  "What evidence would justify the next decision, and when should we stop?",
]

const thresholds = [
  ["Explore", "Output", "Enough to reproduce the artefact/action and learn from it."],
  ["Rely", "Deliverable", "Fit for the named use against explicit acceptance criteria."],
  ["Operate / sell repeatedly", "Capability", "Owners, controls, fallback and operating process exist."],
  ["Measure change", "Outcome", "The named measure moved versus a baseline."],
  ["Scale / renew / stop", "Value", "The outcome is worth full relevant cost, risk and alternatives."],
]

function MeetingBrief() {
  return (
    <PdfcnThemeProvider>
      <Stack gap="sm">
        <div tw="flex items-center justify-between">
          <div>
            <Text>AI Output to Value</Text>
            <Text>One-page meeting brief</Text>
          </div>
          <Badge>Decision tool</Badge>
        </div>
        <Divider />

        <Section spacing="sm">
          <Text>Start with the decision, not the taxonomy</Text>
          <div tw="mt-2 flex flex-col gap-1">
            {thresholds.map(([decision, claim, evidence]) => (
              <div key={decision} tw="flex gap-2 rounded border border-gray-200 px-2 py-1">
                <Text>{decision}</Text>
                <Text>{claim}</Text>
                <Text>{evidence}</Text>
              </div>
            ))}
          </div>
          <Text>Do not average the six claims. A missing decision-critical claim cannot be offset by strength somewhere else.</Text>
        </Section>

        <Section spacing="sm">
          <Text>Eight questions</Text>
          <div tw="mt-1 grid grid-cols-2 gap-x-4 gap-y-1">
            {questions.map((question, index) => (
              <Text key={question}>{index + 1}. {question}</Text>
            ))}
          </div>
        </Section>

        <Section spacing="sm">
          <Text>Decision record</Text>
          <div tw="mt-1 grid grid-cols-2 gap-x-4 gap-y-1">
            <Text>Established: ______________________________</Text>
            <Text>Not established: __________________________</Text>
            <Text>Actor / interface / authority: _____________</Text>
            <Text>Accountability / recourse: _________________</Text>
            <Text>Next evidence: _____________________________</Text>
            <Text>Stop rule: _________________________________</Text>
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
  margin: { top: 30, right: 32, bottom: 30, left: 32 },
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
