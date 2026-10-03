# GitHub Profile Cleanup Final Checklist

## ✅ Completed

- [x] Portfolio Evidence Audit passing (PR #61)
- [x] EXTENDED_README.md created (PR #63)
- [x] PR #59, #62 closed as superseded
- [x] NikolaKubera README cleaned (Japanese Doll Collection preserved)
- [x] Reference disclaimer PRs created for govuk-infrastructure (#1) and llm-eval-monitor-framework (#1)

## 🔴 Requires Manual GitHub UI Action

### 1. Update Repository About

**Repo:** `jobkubera-lab/jobkubera-lab`

**Current description:**
```
Profile repository for Nikola Kubera: AI-powered migration consultant with expertise in visas, job placement, and HR automation projects.
```

**New description:**
```
AI systems engineering portfolio focused on bounded agents, AI assurance, evidence-driven automation and human-controlled execution.
```

**How to:**
1. Go to https://github.com/jobkubera-lab/jobkubera-lab
2. Click **Settings** → **About**
3. Replace description
4. Save

### 2. Add Topics

**Repo:** `jobkubera-lab/jobkubera-lab`

**Add topics:**
- `ai-agents`
- `ai-assurance`
- `agent-orchestration`
- `human-in-the-loop`
- `mcp`
- `ai-governance`
- `evidence`
- `python`
- `llm-evaluation`

**How to:**
1. Go to https://github.com/jobkubera-lab/jobkubera-lab
2. Click **Settings** → **Repository details** → **Topics**
3. Add above topics
4. Save

### 3. Rename Repository

**Current name:** `kubera-learning.`

**New name:** `kubera-learning`

**How to:**
1. Go to https://github.com/jobkubera-lab/kubera-learning.
2. Click **Settings** → **Danger zone** → **Rename**
3. Change from `kubera-learning.` to `kubera-learning`
4. Click **Rename**
5. GitHub will automatically redirect old links

**After rename:**
- GitHub automatically handles old URL redirects
- Check if any public repos have hardcoded links to old name
- If yes, update them in separate PRs

### 4. Update Description for Renamed Repo

**Repo:** `kubera-learning` (after rename)

**Current description:**
```
Learning repository of Nikolay (Kubera) for studying Python, GitHub, and building AI projects.
```

**New description:**
```
Learning and experimentation repository for Python, GitHub workflows and applied AI engineering.
```

**How to:**
1. Go to https://github.com/jobkubera-lab/kubera-learning
2. Click **Settings** → **About**
3. Replace description
4. Save

## 🟡 Requires PR Review + Merge

### Reference Disclaimer PRs

Two PRs are ready and waiting for merge:

1. **govuk-infrastructure PR #1**
   - Adds upstream reference disclaimer banner
   - Ready to merge when reviewed
   - https://github.com/jobkubera-lab/govuk-infrastructure/pull/1

2. **llm-eval-monitor-framework PR #1**
   - Adds upstream reference disclaimer banner
   - Ready to merge when reviewed
   - https://github.com/jobkubera-lab/llm-eval-monitor-framework/pull/1

**Action:** Review PRs and merge if CI passes.

## 📋 Verification Steps

After all actions complete:

1. ✅ Check `jobkubera-lab/jobkubera-lab` About is updated
2. ✅ Check Topics are added to main repo
3. ✅ Verify `kubera-learning` (without dot) now shows on profile
4. ✅ Check that old `kubera-learning.` URL redirects to new name
5. ✅ Review govuk-infrastructure and llm-eval-monitor-framework reference banners are visible
6. ✅ Run Profile Evidence Audit — should pass green

---

**Profile cleanup status: Final polish — just GitHub UI settings remaining.**
