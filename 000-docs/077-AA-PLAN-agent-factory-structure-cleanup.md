# Agent Factory Structure Cleanup Plan

**Document Type:** After Action / Planning
**Created:** 2025-11-19
**Status:** Awaiting Approval for Execution
**Purpose:** Transform bobs-brain into canonical home for Bob + iam-* agent team

---

## Executive Summary

This AAR documents the discovery phase for restructuring bobs-brain from a single-agent repository into a production-grade agent factory that will house:
- **Bob** - Orchestrator agent (user-facing, Slack)
- **iam-* specialists** - Backend worker agents (iam-adk, iam-issue, iam-fix-plan, etc.)

**Current State:** Working single-agent repo with some organizational debt
**Target State:** CTO-ready agent factory with zero mess and clear structure
**Risk Level:** Low-Medium (moves only, no deletions without archiving)
**Approval Status:** ⏳ Awaiting explicit approval to execute

---

## Phase 0: Discovery & Current State

### Repository Identity

**What This Repo Is:**
- Bob's Brain - Production Slack AI assistant
- Deployed to Vertex AI Agent Engine
- Built with Hard Mode architecture (ADK-only, R1-R8 compliant)
- Version: 0.7.0
- Status: Operational and deployed

**Evolution Path:**
- **Current:** Single orchestrator agent (Bob)
- **Target:** Canonical home for Bob + iam-* specialist team
- **Goal:** Production-grade agent factory

### Current Directory Structure

```
bobs-brain/
├── .github/                        # ✅ CI/CD workflows
├── 000-docs/                       # ✅ 34 documents (well-organized)
├── 99-Archive/                     # ⚠️ Should be lowercase 'archive'
├── adk/                            # ❌ Near-empty placeholder
├── adk-a2a/                        # ❌ Completely empty
├── infra/terraform/                # ✅ Infrastructure (clean)
├── my_agent/                       # ⚠️ Bob's agent (generic name, wrong location)
├── scripts/                        # ⚠️ Mixed content, needs organization
├── service/                        # ✅ Gateways (clean)
├── tests/                          # ✅ Test suite (clean)
├── tmp/                            # ❌ Empty, shouldn't be tracked
├── tools/                          # ⚠️ ADK crawler (confusing name)
├── .env                            # ✅ Gitignored, active config
├── .env.example                    # ✅ Template
├── .env.sample                     # ❌ Redundant
├── .env.crawler.example            # ⚠️ Belongs with crawler
├── CHANGELOG.md                    # ✅ Version history
├── CLAUDE.md                       # ✅ Developer guide
├── CRAWLER_SUMMARY.md              # ⚠️ Top-level doc about utility
├── Dockerfile                      # ✅ Agent container
├── LICENSE                         # ✅ MIT license
├── Makefile                        # ✅ Dev commands
├── README.md                       # ✅ Project overview
├── VERSION                         # ✅ 0.7.0
└── requirements.txt                # ✅ Dependencies
```

### What Looks Clean ✅

**Well-Structured Areas:**
- `000-docs/` - 34 properly numbered documents (NNN-CC-ABCD convention)
- `my_agent/` - Clean ADK agent implementation (just wrong location)
- `service/` - Gateway services properly separated (a2a_gateway, slack_webhook)
- `infra/terraform/` - Infrastructure as Code properly isolated
- `tests/` - Test suite with clear structure
- `.github/workflows/` - CI/CD workflows present
- Standard files - CLAUDE.md, README.md, CHANGELOG.md, VERSION all maintained
- `99-Archive/` - Archive directory exists and being used

**Good Patterns Already in Place:**
- Hard Mode R1-R8 compliance architecture
- Document Filing System v2.0 (NNN-CC-ABCD naming)
- Clear separation of concerns (agent vs service vs infra)
- Proper .gitignore (correctly ignores .env)

### What Looks Messy 🔴

#### 1. Top-Level File Clutter

**Multiple .env Variants (CRITICAL):**
```
.env                    - 50 lines  (active config, gitignored) ✅
.env.example            - 106 lines (primary template) ✅
.env.sample             - 5 lines   (redundant!) ❌
.env.crawler.example    - 30 lines  (belongs with crawler) ⚠️
```

**Problem:** 4 .env files at top level, 2 are redundant/misplaced

**Loose Documentation:**
- `CRAWLER_SUMMARY.md` - Top-level doc about crawler utility
  - **Should be:** In 000-docs/ OR with crawler code

#### 2. Empty/Placeholder Directories

**Completely Empty:**
```
adk-a2a/    - 0 files (only . and ..)
tmp/        - 0 files (only . and ..)
```

**Near-Empty:**
```
adk/        - Only README.md (appears to be placeholder)
```

**Problem:** Empty directories suggest incomplete features or abandoned experiments

#### 3. Confusing Directory Names/Purposes

**`tools/` Directory Confusion:**
- **Contains:** ADK docs crawler scripts (adk_docs_crawler.py, adk_docs_uploader.py, etc.)
- **Looks Like:** Agent tools (but those are in my_agent/tools/)
- **Actually Is:** Utility scripts for crawling/indexing ADK documentation
- **Should Be:** `scripts/adk-docs-crawler/` or similar

**`my_agent/` Generic Name:**
- **Current:** `my_agent/` (generic, unclear which agent)
- **Problem:** When we add iam-adk, iam-issue, etc., this is confusing
- **Should Be:** `agents/bob/` (clear identity)

**`99-Archive/` Naming:**
- **Current:** Numbered prefix (99-Archive)
- **Better:** `archive/` (lowercase, consistent with other dirs)

#### 4. Scripts Directory Disorganization

**Current scripts/ Contents:**
```
scripts/
├── ci/                         ✅ Clear purpose
├── setup_vertex_search.sh      ⚠️ Deployment helper (no category)
├── start_unified_bob_v2.sh     ❌ Legacy? (v2 suggests superseded)
├── test_adk_knowledge.py       ⚠️ Crawler-related (wrong location)
├── version-selector.py         ⚠️ Unclear purpose
└── README.md                   ✅ Documentation exists
```

**Problem:** Mixed content without clear categorization

#### 5. Missing Agent Factory Structure

**Critical Gap:** No structure for multiple agents
- No `agents/` directory
- No `templates/` for reusable scaffolds
- No clear convention for where iam-adk, iam-issue, etc. will live

**Current assumption:** This repo only has Bob
**Reality:** Needs to support Bob + 8+ iam-* specialists

---

## Phase 1: Cleanup & Structure Plan

### Target Top-Level Structure

```
bobs-brain/                         # Canonical home for Bob + iam-* team
├── .github/                        # CI/CD workflows ✅
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
│
├── 000-docs/                       # All documentation (R6) ✅
│   ├── [001-076 existing docs]
│   └── 077-AA-PLAN-agent-factory-structure-cleanup.md (this doc)
│
├── agents/                         # 🆕 ALL AGENTS LIVE HERE
│   ├── bob/                        # Bob orchestrator (moved from my_agent/)
│   │   ├── agent.py
│   │   ├── tools/
│   │   ├── system-prompt.md
│   │   ├── agent_engine_app.py
│   │   └── README.md
│   │
│   ├── iam-adk/                    # ADK specialist (exists in ../iam-adk/)
│   │   └── (symlink or reference to ../iam-adk/)
│   │
│   ├── iam-issue/                  # GitHub issue specialist (future)
│   ├── iam-fix-plan/               # Fix planning specialist (future)
│   ├── iam-fix-impl/               # Fix implementation specialist (future)
│   ├── iam-qa/                     # QA specialist (future)
│   ├── iam-doc/                    # Documentation specialist (future)
│   ├── iam-cleanup/                # Cleanup specialist (future)
│   ├── iam-index/                  # Indexing specialist (future)
│   └── README.md                   # 🆕 Agent registry/index
│
├── templates/                      # 🆕 Reusable agent scaffolds
│   ├── specialist-agent-adk/      # Template for iam-* agents
│   │   ├── agent.py.template
│   │   ├── system-prompt.md.template
│   │   ├── README.md.template
│   │   └── a2a/
│   ├── orchestrator-agent/        # Template for Bob-like agents
│   └── README.md                  # Template usage guide
│
├── service/                        # Gateway services (Cloud Run) ✅
│   ├── a2a_gateway/
│   ├── slack_webhook/
│   └── README.md
│
├── infra/                          # Infrastructure as Code ✅
│   ├── terraform/
│   └── README.md
│
├── scripts/                        # Operational & utility scripts
│   ├── ci/                         # CI-specific scripts ✅
│   │   └── check_nodrift.sh
│   │
│   ├── adk-docs-crawler/           # 🆕 ADK crawler (moved from tools/)
│   │   ├── .env.example            # Moved from top-level
│   │   ├── adk_docs_crawler.py
│   │   ├── adk_docs_chunker.py
│   │   ├── adk_docs_extract.py
│   │   ├── adk_docs_uploader.py
│   │   ├── config.py
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── README.md               # Incorporates CRAWLER_SUMMARY.md
│   │
│   ├── deployment/                 # 🆕 Deployment helpers
│   │   ├── setup_vertex_search.sh
│   │   └── version-selector.py
│   │
│   └── README.md                   # Updated organization
│
├── tests/                          # Test suite ✅
│   ├── unit/
│   ├── test_bob.py
│   └── README.md
│
├── archive/                        # 🔄 Renamed from 99-Archive
│   ├── 2025-11-11-final-cleanup/
│   ├── 2025-11-11-hardmode-cleanup/
│   └── legacy-scripts/             # 🆕 For archived scripts
│       └── start_unified_bob_v2.sh
│
├── .env.example                    # Config template ✅
├── .gitignore                      # Updated with tmp/, *.tmp, etc.
├── CHANGELOG.md                    # Version history ✅
├── CLAUDE.md                       # Developer guide (updated paths)
├── Dockerfile                      # Agent container ✅
├── LICENSE                         # MIT ✅
├── Makefile                        # Dev commands ✅
├── README.md                       # Project overview (updated)
├── VERSION                         # 0.7.0 ✅
└── requirements.txt                # Dependencies ✅
```

**Key Principles:**
1. **`agents/`** = Home for ALL agents (Bob + iam-* team)
2. **`templates/`** = Reusable scaffolds for stamping out new agents
3. **`scripts/`** = Organized by purpose (ci/, deployment/, adk-docs-crawler/)
4. **Zero empty directories** = Everything has a purpose
5. **Clear naming** = No generic "my_agent", use actual agent names

---

## Detailed Cleanup Actions

### A. Top-Level File Cleanup

#### DELETE (Safe - Redundant)
```
.env.sample                 - 5 lines, redundant with .env.example
```
**Reason:** Minimal content, .env.example is comprehensive template

#### MOVE
```
.env.crawler.example        → scripts/adk-docs-crawler/.env.example
CRAWLER_SUMMARY.md          → scripts/adk-docs-crawler/README.md (incorporate content)
```
**Reason:** Crawler-specific files belong with crawler code

#### KEEP (No Changes)
```
.env.example                - Primary config template
.env                        - Active config (gitignored, not tracked)
README.md                   - Project overview
CLAUDE.md                   - Developer guide
CHANGELOG.md                - Version history
VERSION                     - Semantic version
Dockerfile                  - Agent container
LICENSE                     - MIT license
Makefile                    - Dev commands
requirements.txt            - Dependencies
.gitignore                  - Ignore patterns
.pre-commit-config.yaml     - Git hooks
```

### B. Directory Reorganization

#### CREATE New Directories
```bash
agents/                     # Home for all agents
agents/bob/                 # Bob orchestrator
agents/README.md            # Agent registry

templates/                  # Reusable scaffolds
templates/specialist-agent-adk/
templates/orchestrator-agent/
templates/README.md

scripts/adk-docs-crawler/   # Crawler utility
scripts/deployment/         # Deployment helpers
```

#### MOVE Operations
```bash
# Move Bob to agents/
my_agent/                   → agents/bob/
  ├── agent.py              → agents/bob/agent.py
  ├── tools/                → agents/bob/tools/
  ├── agent_engine_app.py   → agents/bob/agent_engine_app.py
  ├── __init__.py           → agents/bob/__init__.py
  └── README.md             → agents/bob/README.md

# Move crawler to scripts/
tools/                      → scripts/adk-docs-crawler/
  ├── adk_docs_crawler.py   → scripts/adk-docs-crawler/adk_docs_crawler.py
  ├── adk_docs_chunker.py   → scripts/adk-docs-crawler/adk_docs_chunker.py
  ├── adk_docs_extract.py   → scripts/adk-docs-crawler/adk_docs_extract.py
  ├── adk_docs_uploader.py  → scripts/adk-docs-crawler/adk_docs_uploader.py
  ├── config.py             → scripts/adk-docs-crawler/config.py
  ├── __init__.py           → scripts/adk-docs-crawler/__init__.py
  ├── __main__.py           → scripts/adk-docs-crawler/__main__.py
  └── README.md             → scripts/adk-docs-crawler/README.md

# Move .env variants
.env.crawler.example        → scripts/adk-docs-crawler/.env.example

# Organize scripts/
setup_vertex_search.sh      → scripts/deployment/setup_vertex_search.sh
version-selector.py         → scripts/deployment/version-selector.py
test_adk_knowledge.py       → scripts/adk-docs-crawler/test_adk_knowledge.py
```

#### RENAME
```bash
99-Archive/                 → archive/
```
**Reason:** Lowercase consistent with other directory names

#### DELETE Empty Directories
```bash
adk-a2a/                    - Completely empty (0 files)
tmp/                        - Completely empty (0 files)
adk/                        - Only README.md, no real content
```
**Reason:** No content, unclear purpose, clutter

#### ARCHIVE (Before Potential Deletion)
```bash
scripts/start_unified_bob_v2.sh → archive/legacy-scripts/start_unified_bob_v2.sh
```
**Reason:** Version number "v2" suggests this may be legacy, preserve for safety

### C. Documentation Updates

#### CREATE New Documents
```bash
000-docs/077-AA-PLAN-agent-factory-structure-cleanup.md (this document)
  - Discovery phase findings
  - Cleanup plan
  - Before/after structure

agents/README.md
  - Agent registry and index
  - How to add new agents
  - Naming conventions
  - Agent status table

templates/README.md
  - How to use templates
  - Template customization guide
  - Creating new agent types
```

#### UPDATE Existing Documents
```bash
CLAUDE.md
  - Update paths: my_agent/ → agents/bob/
  - Add agents/ directory section
  - Add templates/ directory section
  - Update import examples

README.md
  - Update directory structure references
  - Add agent team architecture diagram
  - Update quick start paths

scripts/README.md
  - Document new organization (ci/, deployment/, adk-docs-crawler/)
  - Purpose of each subdirectory
```

#### CONSOLIDATE
```bash
CRAWLER_SUMMARY.md → scripts/adk-docs-crawler/README.md
  - Move content into crawler's README
  - Remove top-level file
```

### D. .gitignore Updates

#### ADD Patterns
```gitignore
# Temporary directories (should never be tracked)
tmp/
*.tmp
.cache/

# Local environment variations
.env.local
.env.*.local
```

### E. Import Path Updates

After moving `my_agent/` → `agents/bob/`, update imports:

**Files to Update:**
```
service/a2a_gateway/main.py
service/slack_webhook/main.py
tests/test_bob.py
tests/unit/*
infra/terraform/* (if any Python references)
```

**Pattern:**
```python
# OLD
from my_agent.agent import get_agent

# NEW
from agents.bob.agent import get_agent
```

**Verification:**
```bash
# After moving, grep for old imports
grep -r "from my_agent" .
grep -r "import my_agent" .
```

---

## Execution Strategy

### Phase 2A: Preparation (Safety First)

**Step 1: Create Cleanup Branch**
```bash
git checkout -b chore/agent-factory-structure-cleanup
```

**Step 2: Verify Clean Working Tree**
```bash
git status  # Ensure no uncommitted changes
```

### Phase 2B: Execution (Small Commits)

#### Commit 1: Create New Directory Structure
```bash
# Create new directories
mkdir -p agents/bob
mkdir -p templates/specialist-agent-adk
mkdir -p templates/orchestrator-agent
mkdir -p scripts/adk-docs-crawler
mkdir -p scripts/deployment
mkdir -p archive/legacy-scripts

git add agents/ templates/ scripts/deployment/
git commit -m "chore: create agent factory directory structure

- agents/ - home for all agents (Bob + iam-* team)
- templates/ - reusable agent scaffolds
- scripts/deployment/ - deployment helpers

Prepares repo for multi-agent architecture."
```

#### Commit 2: Move Bob Agent
```bash
# Move my_agent → agents/bob
git mv my_agent agents/bob

git commit -m "refactor: move Bob agent to agents/bob/

- my_agent/ → agents/bob/ (clear agent identity)
- Prepares for multi-agent structure
- Import paths will be updated in next commit"
```

#### Commit 3: Update Import Paths
```bash
# Update all imports from my_agent → agents.bob
# (Manual edits to service/, tests/, etc.)

git add service/ tests/
git commit -m "refactor: update import paths for agents/bob/

- service/a2a_gateway/main.py
- service/slack_webhook/main.py
- tests/test_bob.py
- tests/unit/*

All imports updated: my_agent → agents.bob"
```

#### Commit 4: Move Crawler to Scripts
```bash
# Move tools/ → scripts/adk-docs-crawler/
git mv tools scripts/adk-docs-crawler

# Move related files
git mv .env.crawler.example scripts/adk-docs-crawler/.env.example
git mv test_adk_knowledge.py scripts/adk-docs-crawler/

git commit -m "refactor: move ADK crawler to scripts/adk-docs-crawler/

- tools/ → scripts/adk-docs-crawler/ (clarify purpose)
- .env.crawler.example → scripts/adk-docs-crawler/.env.example
- test_adk_knowledge.py → scripts/adk-docs-crawler/

Separates utility scripts from agent tools."
```

#### Commit 5: Organize Scripts
```bash
# Move deployment scripts
git mv setup_vertex_search.sh scripts/deployment/
git mv version-selector.py scripts/deployment/

git commit -m "chore: organize deployment scripts

- setup_vertex_search.sh → scripts/deployment/
- version-selector.py → scripts/deployment/

Categorizes scripts by purpose."
```

#### Commit 6: Rename Archive
```bash
git mv 99-Archive archive

git commit -m "chore: rename 99-Archive to archive

Normalizes directory naming (lowercase, no prefix)."
```

#### Commit 7: Archive Legacy Scripts
```bash
git mv scripts/start_unified_bob_v2.sh archive/legacy-scripts/

git commit -m "chore: archive legacy start script

- start_unified_bob_v2.sh → archive/legacy-scripts/

Version number suggests this is superseded. Preserved for reference."
```

#### Commit 8: Remove Empty Directories
```bash
git rm -r adk-a2a
git rm -r tmp
git rm -r adk

git commit -m "chore: remove empty placeholder directories

Deleted:
- adk-a2a/ (empty, no clear purpose)
- tmp/ (empty, should not be tracked)
- adk/ (only README.md, no content)

Cleaned up repository clutter."
```

#### Commit 9: Remove Redundant Files
```bash
git rm .env.sample

git commit -m "chore: remove redundant .env.sample

.env.example is the comprehensive template. No need for duplicate."
```

#### Commit 10: Update Documentation
```bash
# Create new docs
# - agents/README.md
# - templates/README.md
# - 000-docs/077-AA-PLAN-agent-factory-structure-cleanup.md

# Update existing docs
# - CLAUDE.md (paths)
# - README.md (structure)
# - scripts/README.md

git add agents/README.md templates/README.md
git add 000-docs/077-AA-PLAN-agent-factory-structure-cleanup.md
git add CLAUDE.md README.md scripts/README.md

git commit -m "docs: update documentation for agent factory structure

Created:
- agents/README.md (agent registry)
- templates/README.md (template guide)
- 000-docs/077-AA-PLAN-agent-factory-structure-cleanup.md (this AAR)

Updated:
- CLAUDE.md (paths: my_agent → agents/bob)
- README.md (structure references)
- scripts/README.md (new organization)

All documentation reflects new agent factory structure."
```

#### Commit 11: Update .gitignore
```bash
# Add tmp/, *.tmp, .env.local patterns

git add .gitignore
git commit -m "chore: update .gitignore for temporary files

Added:
- tmp/ (temporary directory)
- *.tmp (temp files)
- .env.local (local env variants)
- .cache/ (cache directory)"
```

#### Commit 12: Move Crawler Summary
```bash
# Incorporate CRAWLER_SUMMARY.md into scripts/adk-docs-crawler/README.md
git rm CRAWLER_SUMMARY.md

git commit -m "docs: consolidate CRAWLER_SUMMARY.md into crawler README

Content moved to scripts/adk-docs-crawler/README.md.
Removes top-level documentation clutter."
```

### Phase 2C: Verification

**Step 1: Test Imports**
```bash
# Verify no broken imports
grep -r "from my_agent" .
grep -r "import my_agent" .
# Should return nothing

# Verify new imports work
python -c "from agents.bob.agent import get_agent; print('✅ Import works')"
```

**Step 2: Run Tests**
```bash
make test
# OR
pytest tests/
```

**Step 3: Verify Structure**
```bash
tree -L 2 -I '.venv|__pycache__|*.pyc|.git'
# Should match target structure
```

**Step 4: Check Git Status**
```bash
git status
# Should show clean working tree
```

### Phase 2D: Review & Merge

**Step 1: Create PR**
```bash
git push origin chore/agent-factory-structure-cleanup
gh pr create --title "Agent Factory Structure Cleanup" \
  --body "See 000-docs/077-AA-PLAN-agent-factory-structure-cleanup.md for full plan"
```

**Step 2: Review Commits**
- Each commit should be focused and reviewable
- All moves preserve git history
- No data loss

**Step 3: Merge**
```bash
# After approval
git checkout main
git merge chore/agent-factory-structure-cleanup
git push origin main
```

---

## Before vs After Comparison

### Before (Current State)

**Top-Level:**
```
.env, .env.example, .env.sample, .env.crawler.example    ❌ 4 env files
CRAWLER_SUMMARY.md                                        ❌ Loose doc
my_agent/                                                 ⚠️ Generic name
tools/                                                    ⚠️ Confusing name
adk-a2a/, tmp/, adk/                                     ❌ Empty dirs
99-Archive/                                              ⚠️ Numbered name
scripts/                                                  ⚠️ Disorganized
```

**Issues:**
- No clear home for iam-* agents
- Utility scripts look like agent tools
- Empty directories suggest incomplete work
- Top-level clutter

### After (Clean State)

**Top-Level:**
```
.env.example                                             ✅ Single template
agents/                                                   ✅ All agents here
  ├── bob/                                               ✅ Clear identity
  ├── iam-adk/ (future)
  └── iam-*/  (future)
templates/                                                ✅ Reusable scaffolds
scripts/                                                  ✅ Organized
  ├── ci/
  ├── adk-docs-crawler/
  └── deployment/
archive/                                                  ✅ Consistent naming
```

**Benefits:**
- Clear home for all agents
- Organized scripts by purpose
- Zero empty directories
- Zero top-level clutter
- Production-grade structure

---

## Risk Assessment & Mitigations

### Low Risk (Safe Operations)

**Operations:**
- Creating new directories
- Moving files/directories (git mv preserves history)
- Renaming directories (99-Archive → archive)
- Deleting empty directories

**Why Low Risk:**
- No code changes
- Full git history preserved
- Can revert easily

### Medium Risk (Needs Verification)

**Operations:**
- Moving my_agent/ → agents/bob/ (import path changes)
- Moving tools/ → scripts/adk-docs-crawler/ (verify no external references)
- Archiving start_unified_bob_v2.sh (confirm not actively used)

**Mitigations:**
- Test all imports after moving
- Run full test suite
- Grep for old import paths
- Archive before deleting anything

### Verification Checklist

After execution, verify:
- [ ] All imports work (no "ModuleNotFoundError")
- [ ] Tests pass (make test OR pytest)
- [ ] Agent can be imported: `from agents.bob.agent import get_agent`
- [ ] No references to old paths in service/, tests/
- [ ] Directory structure matches target
- [ ] No empty directories remain
- [ ] Documentation updated with correct paths

---

## Rollback Plan

If issues discovered after merge:

**Option 1: Revert Entire Cleanup**
```bash
git revert <merge-commit-sha>
git push origin main
```

**Option 2: Fix Forward**
```bash
# Fix specific import issues
# Create hotfix branch
# Patch and merge
```

**Option 3: Cherry-Pick Good Commits**
```bash
git checkout -b hotfix/partial-cleanup
git cherry-pick <good-commit-1>
git cherry-pick <good-commit-2>
# Skip problematic commits
```

**Safety:** All changes are in git history, can restore any state

---

## Success Criteria

This cleanup is successful when:

✅ **Zero top-level clutter**
- Only standard files (README, CLAUDE, .env.example, etc.)
- No random scripts or docs

✅ **Clear agent organization**
- Bob lives in agents/bob/
- Ready to add iam-* specialists
- Agent registry exists

✅ **Organized scripts**
- Categorized by purpose (ci/, deployment/, adk-docs-crawler/)
- No confusion about what goes where

✅ **No empty directories**
- Every directory has clear purpose and content

✅ **All imports work**
- No broken references
- Tests pass
- Agent can be deployed

✅ **Documentation updated**
- CLAUDE.md reflects new structure
- README.md shows correct paths
- Agent registry documents all agents

✅ **CTO-ready**
- A hard-ass CTO can open the repo and see zero mess
- Clear, consistent hierarchy
- Production-grade organization

---

## Timeline Estimate

**Phase 2 Execution:** 2-3 hours
- 30 min: Branch creation and directory setup
- 60 min: Moving files and updating imports
- 30 min: Documentation updates
- 30 min: Testing and verification

**Review & Merge:** 30 min
- PR creation
- Final review
- Merge to main

**Total:** 2.5-3.5 hours

---

## Approval Required

**State:** ⏳ **AWAITING APPROVAL**

**To Proceed:** Respond with:
```
APPROVE_CLEANUP_PLAN – EXECUTE PHASE 2
```

**To Modify:** Respond with changes/concerns, will update plan

**To Reject:** Respond with reasons, will propose alternative

---

## Appendix A: Agent Registry Template

**File:** `agents/README.md` (to be created)

```markdown
# Agent Registry

This directory contains all agents in the Bob's Brain agent team.

## Active Agents

| Agent | Type | Status | Version | Location |
|-------|------|--------|---------|----------|
| Bob | Orchestrator | ✅ Deployed | 0.7.0 | agents/bob/ |
| iam-adk | Specialist | 🔄 In Development | 0.1.0 | ../iam-adk/ (external) |

## Planned Agents

| Agent | Type | Purpose | Priority |
|-------|------|---------|----------|
| iam-issue | Specialist | GitHub issue management | High |
| iam-fix-plan | Specialist | Fix planning | High |
| iam-fix-impl | Specialist | Fix implementation | High |
| iam-qa | Specialist | Quality assurance | Medium |
| iam-doc | Specialist | Documentation | Medium |
| iam-cleanup | Specialist | Code cleanup | Low |
| iam-index | Specialist | Knowledge indexing | Low |

## Agent Naming Convention

- **Orchestrators:** `<name>` (e.g., `bob`)
- **Specialists:** `iam-<specialty>` (e.g., `iam-adk`)

## Adding New Agents

1. Use template from `templates/specialist-agent-adk/` or `templates/orchestrator-agent/`
2. Create directory under `agents/<agent-name>/`
3. Implement agent.py, tools/, system-prompt.md
4. Add entry to this registry
5. Update 000-docs/ with agent documentation
```

---

## Appendix B: Commit Message Convention

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactor (no functional change)
- `chore` - Maintenance (no code change to src)
- `docs` - Documentation only
- `test` - Test only
- `ci` - CI/CD changes

**Example:**
```
refactor(agents): move Bob to agents/bob/

- my_agent/ → agents/bob/
- Prepares for multi-agent structure
- Import paths will be updated in next commit

Part of agent factory structure cleanup.
```

---

**Document Status:** Ready for approval
**Next Action:** Awaiting user response to proceed with Phase 2 execution
**Created:** 2025-11-19
**Last Updated:** 2025-11-19
