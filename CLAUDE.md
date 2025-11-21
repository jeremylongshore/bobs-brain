# CLAUDE.md – How to Work With Claude in bobs-brain

## 1. Purpose of This File

This is the **live** guide for Claude Code when working in the `bobs-brain` repository. It provides essential context, patterns, and house rules to help AI assistants work effectively with this ADK-based agent department.

**For deeper context:** See `000-docs/claude-working-notes-archive.md` for historical notes and detailed background.

---

## 2. Repo Context (Short)

**Bob's Brain** is a production-grade **ADK agent department** built on Google's Agent Development Kit (ADK) and Vertex AI Agent Engine. It serves as:

- The canonical reference implementation for multi-agent SWE (Software Engineering) departments
- A Slack AI assistant powered by ADK agents
- A reusable template for other product repositories

**Key Components:**
- `bob` - Global orchestrator agent
- `iam-senior-adk-devops-lead` - Departmental foreman
- `iam-*` specialists - ADK design, issues, fixes, QA, docs, cleanup, indexing

**Architecture Pattern:** Agent Factory with strict "Hard Mode" rules (R1-R8) enforced via CI/CD.

---

## 3. How to Talk to Claude About This Repo

### Example Prompts

**For agents/department work:**
- "Design the iam-adk specialist agent following Bob's patterns"
- "Audit agent.py files for ADK compliance against Hard Mode rules"
- "Propose A2A wiring between iam-foreman and iam-issue"

**For infrastructure:**
- "Update Terraform to add Agent Engine configuration for iam-adk"
- "Design CI workflow for multi-agent ARV (Agent Readiness Verification)"

**For CI/CD:**
- "Add drift detection checks for new iam-* agents"
- "Implement ARV gates in GitHub Actions"

### Key Expectations

When working in this repo, Claude should:

1. **Respect repo layout** - Don't invent new folders without permission
2. **Consult `000-docs/`** - Check existing standards before creating new patterns
3. **Use plugins/tools first** - Search ADK docs and repo patterns before guessing
4. **Propose small changes** - Break work into reviewable commits
5. **Follow phases** - Structure work into phases with PLAN and AAR docs
6. **Think in agents** - Consider which department agent (bob, foreman, specialist) owns the work

---

## 4. Expectations & House Rules

### Architecture Standards

**Hard Mode Rules (R1-R8)** - CI-enforced, cannot be violated:
- R1: ADK-Only (no LangChain, CrewAI, custom frameworks)
- R2: Vertex AI Agent Engine runtime (no self-hosted runners)
- R3: Gateway separation (Cloud Run proxies only, no Runner in service/)
- R4: CI-only deployments (GitHub Actions with WIF, no manual gcloud)
- R5: Dual memory wiring (VertexAiSessionService + VertexAiMemoryBankService)
- R6: Single doc folder (all docs in `000-docs/` with NNN-CC-ABCD naming)
- R7: SPIFFE ID propagation (in AgentCard, logs, headers)
- R8: Drift detection (runs first in CI, blocks violations)

**See:** `000-docs/6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md` for complete spec.

### Coding Style

**Python (agents/):**
- Follow lazy-loading App pattern (see 6774 standard)
- Use `google-adk` imports exclusively
- Implement `after_agent_callback` for R5 compliance
- Module-level `app`, not `agent`

**Terraform (infra/):**
- Use modules over copy-pasted resources
- Keep env configs in `envs/dev`, `envs/prod`
- Name resources consistently with existing patterns

**CI Workflows:**
- Reuse job patterns from existing `.github/workflows/`
- Group checks logically (lint, test, build, deploy, ARV)
- Keep workflows focused (avoid mega-workflows)

### Documentation Standards

**Document Filing System v2.0:**
- Format: `NNN-CC-ABCD-description.md`
- Categories: PP (Planning), AT (Architecture), AA (After-Action Reports), DR (Documentation/Reference)
- All docs in `000-docs/` - NO scattered documentation

**Key Doc Types:**
- **PLAN** (`NNN-AA-PLAN-*.md`) - Phase planning before work starts
- **REPT** (`NNN-AA-REPT-*.md`) - After-Action Report after phase completes
- **STND** (`NNN-DR-STND-*.md`) - Standards and specifications
- **ARCH** (`NNN-AT-ARCH-*.md`) - Architecture designs

### Phases & AARs

**All significant work** must be structured into phases:

1. **Phase Planning**
   - Create `NNN-AA-PLAN-phase-name.md` in `000-docs/`
   - Define scope, steps, decisions, expected artifacts

2. **Implementation**
   - Work in small, reviewable commits
   - Reference phase name in commit messages

3. **AAR (After-Action Report)**
   - Create `NNN-AA-REPT-phase-name.md` when complete
   - Document what was built, decisions made, lessons learned

**Example Phase Flow:**
```
Phase 1: Design iam-adk specialist
├── 001-AA-PLAN-iam-adk-design.md (planning)
├── [implementation commits]
└── 002-AA-REPT-iam-adk-implementation.md (AAR)
```

### Commit Messages

Use conventional commits format:
```
<type>(<scope>): <subject>

<optional body>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`

**Examples:**
- `feat(agents): scaffold iam-adk specialist agent`
- `docs(000-docs): add plan for iam-adk design phase`
- `ci(workflows): add ARV checks for agent readiness`

---

## 5. Where to Find the Deep Details

**All detailed documentation lives in `000-docs/`** - DON'T overcrowd this file.

### Key SOP Documents (6767-series)

All **6767-prefixed docs act as Standard Operating Procedures (SOPs)** - these are canonical standards:

- **6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md** - Hard Mode rules (R1-R8)
- **6774-DR-STND-adk-lazy-loading-app-pattern.md** - Lazy-loading App pattern
- **6775-DR-STND-inline-source-deployment-for-vertex-agent-engine.md** - Inline source deployment
- **6767-115-DR-STND-prompt-design-and-a2a-contracts-for-department-adk-iam.md** - Prompt design contracts

### Other Key References

- **127-DR-STND-agent-engine-entrypoints.md** - Canonical entrypoints for inline deployment
- **126-AA-AUDT-appaudit-devops-playbook.md** - Complete DevOps onboarding (15k words)
- **claude-working-notes-archive.md** - Historical verbose content

### How to Find What You Need

```bash
# List all SOPs (6767-series)
ls 000-docs/6767*.md

# List all standards
ls 000-docs/*-DR-STND-*.md

# Search for keyword
grep -r "inline source" 000-docs/

# Find doc by number
ls 000-docs/127-*
```

**Rule**: When you need detailed info, **search `000-docs/` first** - don't bloat CLAUDE.md.

---

## 6. Changelog / Maintenance

**Last Update:** 2025-11-21

**Recent Changes:**
- Added 127-DR-STND-agent-engine-entrypoints.md (canonical entrypoints reference)
- Updated Section 5 to emphasize 6767-series as SOPs
- Added clear search commands for finding docs in 000-docs/

**Maintenance Policy:**
- **DON'T overcrowd CLAUDE.md** - it's a pointer doc, not a knowledge base
- All detailed docs go in `000-docs/` following NNN-CC-ABCD naming
- 6767-series docs = SOPs (Standard Operating Procedures)
- CLAUDE.md should remain < 8k chars for performance
- When adding new standards, update Section 5 with pointer, not full content

---

## Quick Reference Commands

```bash
# Navigate to repo
cd /home/jeremy/000-projects/iams/bobs-brain/

# Run tests
pytest
pytest tests/unit/test_a2a_card.py -v

# Check compliance
bash scripts/ci/check_nodrift.sh
make check-arv-minimum

# Local development
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# View documentation
ls 000-docs/
cat 000-docs/6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md
```

---

**For complete historical context, patterns, and examples:** See `000-docs/claude-working-notes-archive.md`
