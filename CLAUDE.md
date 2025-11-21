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

**All detailed documentation lives in `000-docs/`**

Key things to know:
- **6767-prefixed docs** = SOP (Standard Operating Procedures) - canonical standards
- **Archive**: `claude-working-notes-archive.md` - Historical verbose content
- **Search first**: Use `ls 000-docs/` or `grep` to find what you need

When you need deep details on architecture, patterns, or standards - look in `000-docs/` first.

---

## 6. Changelog / Maintenance

**Last Substantial Refresh:** 2025-11-21

**Change:** Slimmed CLAUDE.md from 42,237 chars to < 8,000 chars by:
- Moving verbose content to `000-docs/claude-working-notes-archive.md`
- Keeping focused "how to work with Claude" guidance
- Adding clear pointers to key `000-docs/` standards

**Maintenance Policy:**
- If CLAUDE.md gets bloated again, move excess content to:
  - `000-docs/claude-working-notes-archive.md` (scratchpad, historical)
  - Specific `000-docs/` files (if content belongs in a standard/guide)
- CLAUDE.md should remain a **quick start + pointer doc**, not an everything-doc

**Future Updates:**
- Add links as new canonical docs (6767-series) are created
- Update architecture section when major versions change
- Keep this under ~8k characters for performance

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
