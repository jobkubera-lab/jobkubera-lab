const agents = [
  { id: "agent-02", harness: "Review Agent", task: "Review an evidence-backed Civic Evidence change", state: "waiting_approval", approval: true, updated: "needs Nikola" },
  { id: "agent-03", harness: "Verifier", task: "Investigate a failing parity check before any merge", state: "failed", approval: false, updated: "blocked" },
  { id: "agent-01", harness: "Builder", task: "Run reference tests and prepare a local draft", state: "running", approval: false, updated: "working" }
];

const setup = [
  { kind: "guide", name: "Repository Agent Guide", path: "AGENTS.md", note: "Commands, repository map, hard invariants and completion checks." },
  { kind: "operator", name: "KUBERA Operator", path: "kubera-lab/innovation-stack/KUBERA_OPERATOR.md", note: "WorkContract, gates, idempotency, improvement loop and approval boundary." },
  { kind: "skill", name: "Verify before claim", path: "kubera-lab/operator-workspace-kit/skills/verify-before-claim.md", note: "Do not turn an assumption into a factual statement." },
  { kind: "skill", name: "Recheck before write", path: "kubera-lab/operator-workspace-kit/skills/recheck-before-write.md", note: "Re-read the current file/state immediately before a write." },
  { kind: "gate", name: "Profile README Lock", path: ".github/workflows/profile-readme-lock.yml", note: "Deterministic protection is stronger than repeating a prose instruction." }
];

const proposals = [
  {
    id: "p-readme",
    kind: "gate",
    title: "Keep protected profile files out of normal agent edits",
    evidence: "4 compact correction signals · 3 conversations · pain 6",
    signal: "Repeated correction: do not change the root profile README during unrelated work.",
    target: "AGENTS.md",
    diff: "--- a/AGENTS.md\n+++ b/AGENTS.md\n@@\n+Do not modify root README.md unless Nikola explicitly commands a profile-page change.\n"
  },
  {
    id: "p-verify",
    kind: "skill",
    title: "Promote verification-before-handoff into a reusable skill",
    evidence: "3 compact correction signals · 3 conversations · pain 4",
    signal: "Repeated correction: verify tests/current state before saying work is ready.",
    target: "skills/verify-before-handoff.md",
    diff: "--- /dev/null\n+++ b/skills/verify-before-handoff.md\n@@\n+1. Re-read changed files.\n+2. Run relevant tests.\n+3. Confirm protected files are unchanged.\n+4. Report only verified status.\n"
  }
];

function esc(value) {
  return value.replace(/[&<>\"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
}

function renderAgents() {
  document.querySelector("#agent-grid").innerHTML = agents.map(agent => `
    <article class="card">
      <div class="card-head">
        <strong>${esc(agent.harness)}</strong>
        <span class="status ${agent.state}">${agent.state.replace("_", " ")}</span>
      </div>
      <p class="task">${esc(agent.task)}</p>
      <div class="meta"><span>${esc(agent.id)}</span><span>${esc(agent.updated)}</span></div>
    </article>
  `).join("");
}

function renderSetup() {
  document.querySelector("#setup-list").innerHTML = setup.map(item => `
    <article class="row">
      <div class="row-head">
        <div><span class="kind">${esc(item.kind)}</span> <strong>${esc(item.name)}</strong></div>
      </div>
      <p class="path">${esc(item.path)}</p>
      <p class="muted">${esc(item.note)}</p>
    </article>
  `).join("");
}

function renderProposals() {
  document.querySelector("#proposal-list").innerHTML = proposals.map(proposal => `
    <article class="row" data-proposal="${proposal.id}">
      <div class="row-head">
        <div><span class="kind">${proposal.kind}</span> <strong>${esc(proposal.title)}</strong></div>
        <span class="muted">${esc(proposal.evidence)}</span>
      </div>
      <p class="signal">${esc(proposal.signal)}</p>
      <p class="path">Target: ${esc(proposal.target)}</p>
      <div class="actions">
        <button data-action="dismiss">Dismiss</button>
        <button data-action="preview">Preview diff</button>
        <button class="approve" data-action="approve">Approve proposal</button>
      </div>
    </article>
  `).join("");
}

function switchView(view) {
  document.querySelectorAll(".tab").forEach(tab => tab.classList.toggle("active", tab.dataset.view === view));
  document.querySelectorAll(".view").forEach(panel => panel.classList.toggle("active", panel.id === view));
}

document.querySelectorAll(".tab").forEach(tab => tab.addEventListener("click", () => switchView(tab.dataset.view)));

const dialog = document.querySelector("#diff-dialog");
const diffContent = document.querySelector("#diff-content");
const diffTitle = document.querySelector("#diff-title");
document.querySelector("#close-dialog").addEventListener("click", () => dialog.close());

function markDecision(card, decision) {
  card.querySelectorAll("button").forEach(button => button.disabled = true);
  const actions = card.querySelector(".actions");
  const result = document.createElement("strong");
  result.textContent = decision === "approved"
    ? "Approved for the normal PR/CI workflow — not auto-applied"
    : "Dismissed in demo";
  actions.appendChild(result);
}

document.querySelector("#proposal-list").addEventListener("click", event => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const card = button.closest("[data-proposal]");
  const proposal = proposals.find(item => item.id === card.dataset.proposal);
  if (button.dataset.action === "preview") {
    diffTitle.textContent = proposal.title;
    diffContent.textContent = proposal.diff;
    dialog.showModal();
    return;
  }
  if (button.dataset.action === "approve") markDecision(card, "approved");
  if (button.dataset.action === "dismiss") markDecision(card, "dismissed");
});

renderAgents();
renderSetup();
renderProposals();
