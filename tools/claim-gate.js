(() => {
  "use strict";

  const form = document.getElementById("gate-form");
  const decision = document.getElementById("decision");
  const checksHost = document.getElementById("gate-checks");
  const requiredClaim = document.getElementById("required-claim");
  const gateDescription = document.getElementById("gate-description");
  const statusBox = document.getElementById("status-box");
  const statusSummary = document.getElementById("status-summary");
  const statusReasons = document.getElementById("status-reasons");

  let gates;
  let assertedClaim;

  const claimLabels = {
    "01-access": "01 Access",
    "02-output": "02 Output",
    "03-deliverable": "03 Deliverable",
    "04-capability": "04 Capability",
    "05-outcome": "05 Outcome",
    "06-value": "06 Value"
  };

  function lines(value) {
    return String(value || "").split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
  }

  function makeAssertedClaimField() {
    const wrap = document.createElement("div");
    wrap.className = "gate-field";
    const label = document.createElement("label");
    label.htmlFor = "asserted-claim";
    label.textContent = "Claim being asserted";
    assertedClaim = document.createElement("select");
    assertedClaim.id = "asserted-claim";
    for (const [value, text] of Object.entries(claimLabels)) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = text;
      assertedClaim.append(option);
    }
    wrap.append(label, assertedClaim);
    decision.closest(".gate-field").after(wrap);
    assertedClaim.addEventListener("change", evaluate);
  }

  function currentRule() {
    return gates.decisions[decision.value];
  }

  function renderDecisionOptions() {
    decision.replaceChildren();
    for (const [id, rule] of Object.entries(gates.decisions)) {
      const option = document.createElement("option");
      option.value = id;
      option.textContent = `${rule.label} — ${claimLabels[rule.requiredClaimLevel]}`;
      decision.append(option);
    }
  }

  function renderChecks() {
    const rule = currentRule();
    requiredClaim.textContent = `Required claim: ${claimLabels[rule.requiredClaimLevel]}`;
    gateDescription.textContent = rule.description;
    if (!assertedClaim.dataset.touched) assertedClaim.value = rule.requiredClaimLevel;
    checksHost.replaceChildren();

    for (const check of rule.requiredChecks) {
      const row = document.createElement("div");
      row.className = "gate-check";
      const label = document.createElement("label");
      label.htmlFor = `check-${check.id}`;
      label.textContent = check.label;
      const select = document.createElement("select");
      select.id = `check-${check.id}`;
      select.dataset.checkId = check.id;
      for (const [value, text] of [
        ["unknown", "Unknown / not evidenced"],
        ["pass", "Pass"],
        ["fail", "Fail"]
      ]) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = text;
        select.append(option);
      }
      select.addEventListener("change", evaluate);
      row.append(label, select);
      checksHost.append(row);
    }
    evaluate();
  }

  function metadataGaps() {
    const gaps = [];
    const requiredText = [
      ["project", "Project / initiative is not named."],
      ["intended-use", "Intended use is not defined."],
      ["authority", "Authority boundary is not recorded."],
      ["accountability", "Accountability / recourse is not recorded."],
      ["next-evidence", "Next evidence is not recorded."],
      ["stop-rule", "Stop rule is not recorded."]
    ];
    for (const [id, message] of requiredText) {
      if (!document.getElementById(id).value.trim()) gaps.push(message);
    }
    return gaps;
  }

  function evaluate() {
    if (!gates || !assertedClaim) return;
    const rule = currentRule();
    const failed = [];
    const unknown = [];
    for (const select of checksHost.querySelectorAll("select[data-check-id]")) {
      const check = rule.requiredChecks.find((item) => item.id === select.dataset.checkId);
      if (select.value === "fail") failed.push(check.label);
      if (select.value === "unknown") unknown.push(check.label);
    }

    const gaps = metadataGaps();
    const claimMismatch = assertedClaim.value !== rule.requiredClaimLevel;
    let status;
    if (failed.length) status = "BLOCKED";
    else if (unknown.length || gaps.length || claimMismatch) status = "INSUFFICIENT_EVIDENCE";
    else status = "PASS";

    statusBox.dataset.status = status;
    statusBox.textContent = status.replaceAll("_", " ");
    statusSummary.textContent = status === "PASS"
      ? `The supplied record satisfies every check required for ${rule.label}. This does not prove facts beyond the supplied evidence.`
      : status === "BLOCKED"
        ? `At least one decision-critical check explicitly failed. Strength at other claim levels does not offset it.`
        : `No decision-critical check is recorded as failed, but the record is not sufficient to justify this decision.`;

    statusReasons.replaceChildren();
    const reasons = [
      ...failed.map((text) => `Failed: ${text}`),
      ...unknown.map((text) => `Missing/unknown evidence: ${text}`),
      ...gaps,
      ...(claimMismatch ? [`The asserted claim (${claimLabels[assertedClaim.value]}) does not match the claim required by this target decision (${claimLabels[rule.requiredClaimLevel]}).`] : [])
    ];
    if (!reasons.length) reasons.push("All required checks and decision-record fields are present.");
    for (const reason of reasons) {
      const li = document.createElement("li");
      li.textContent = reason;
      statusReasons.append(li);
    }
  }

  function record() {
    const rule = currentRule();
    const gateChecks = {};
    for (const select of checksHost.querySelectorAll("select[data-check-id]")) {
      gateChecks[select.dataset.checkId] = select.value;
    }
    return {
      $schema: new URL("../schemas/v1/claim.schema.json", location.href).href,
      schemaVersion: "1.0",
      project: document.getElementById("project").value.trim(),
      targetDecision: decision.value,
      requiredClaimLevel: rule.requiredClaimLevel,
      assertedClaimLevel: assertedClaim.value,
      intendedUse: document.getElementById("intended-use").value.trim(),
      actors: [{
        type: document.getElementById("actor").value,
        role: "Primary actor for the assessed workflow",
        interactionChannel: document.getElementById("channel").value
      }],
      authority: document.getElementById("authority").value.trim(),
      accountability: document.getElementById("accountability").value.trim(),
      evidenceRefs: lines(document.getElementById("evidence").value),
      gateChecks,
      nextEvidence: document.getElementById("next-evidence").value.trim(),
      stopRule: document.getElementById("stop-rule").value.trim()
    };
  }

  function markdownSummary() {
    const r = record();
    const rule = currentRule();
    const rows = rule.requiredChecks.map((check) => {
      const state = r.gateChecks[check.id] || "unknown";
      return `- **${state.toUpperCase()}** — ${check.label}`;
    }).join("\n");
    return `# AI Output to Value — decision gate\n\n` +
      `**Project:** ${r.project || "(not supplied)"}\n\n` +
      `**Target decision:** ${rule.label}\n\n` +
      `**Required claim:** ${claimLabels[r.requiredClaimLevel]}\n\n` +
      `**Asserted claim:** ${claimLabels[r.assertedClaimLevel]}\n\n` +
      `**Gate status:** ${statusBox.textContent}\n\n` +
      `## Intended use\n\n${r.intendedUse || "(not supplied)"}\n\n` +
      `## Required checks\n\n${rows}\n\n` +
      `## Authority\n\n${r.authority || "(not supplied)"}\n\n` +
      `## Accountability / recourse\n\n${r.accountability || "(not supplied)"}\n\n` +
      `## Evidence references\n\n${r.evidenceRefs.length ? r.evidenceRefs.map((x) => `- ${x}`).join("\n") : "(none supplied)"}\n\n` +
      `## Next evidence\n\n${r.nextEvidence || "(not supplied)"}\n\n` +
      `## Stop rule\n\n${r.stopRule || "(not supplied)"}\n`;
  }

  async function copy(text, button) {
    await navigator.clipboard.writeText(text);
    const before = button.textContent;
    button.textContent = "Copied";
    setTimeout(() => { button.textContent = before; }, 1200);
  }

  async function init() {
    const response = await fetch("../schemas/v1/decision-gates.json");
    if (!response.ok) throw new Error(`Gate rules returned HTTP ${response.status}`);
    gates = await response.json();
    makeAssertedClaimField();
    renderDecisionOptions();
    decision.addEventListener("change", () => {
      assertedClaim.dataset.touched = "";
      renderChecks();
    });
    assertedClaim.addEventListener("change", () => {
      assertedClaim.dataset.touched = "true";
      evaluate();
    });
    for (const input of form.querySelectorAll("input, textarea, select")) input.addEventListener("input", evaluate);
    renderChecks();

    document.getElementById("copy-md").addEventListener("click", (event) => copy(markdownSummary(), event.currentTarget));
    document.getElementById("download-json").addEventListener("click", () => {
      const blob = new Blob([JSON.stringify(record(), null, 2)], { type: "application/json" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `${record().project || "claim"}.claim.json`;
      link.click();
      setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    });
    document.getElementById("print").addEventListener("click", () => window.print());
  }

  init().catch((error) => {
    statusBox.dataset.status = "BLOCKED";
    statusBox.textContent = "TOOL ERROR";
    statusSummary.textContent = error instanceof Error ? error.message : String(error);
  });
})();
