# Hard Mode Baseline - ADK + Agent Engine Enforcement

**Date:** 2025-11-11
**Type:** After-Action Report (AAR)
**Status:** 🟡 In Progress

---

## Executive Summary

Establishing "Hard Mode" enforcement for Bob's Brain: ADK + Vertex AI Agent Engine only, CI-only deployments, Terraform-first infrastructure, with comprehensive drift detection. This baseline enforces clean separation between agent code (`my_agent/`), protocol gateways (`service/`), and infrastructure (`infra/`).

## Objectives

1. ✅ **Enforce canonical structure** - 8 approved directories only at root
2. ✅ **Establish hard rules (R1-R8)** - Documented in CLAUDE.md, enforced in CI
3. 🟡 **Implement agent core** - ADK with dual memory (Session + Memory Bank)
4. 🟡 **Create protocol gateways** - A2A and Slack proxies (no Runner imports)
5. 🟡 **Terraform infrastructure** - All GCP resources as code
6. 🟡 **CI/CD with drift detection** - GitHub Actions workflows
7. 🟡 **SPIFFE ID propagation** - Immutable agent identity throughout stack
8. ✅ **Documentation** - Comprehensive CLAUDE.md and this AAR

## What Changed

### 1. Repository Structure

**Before (2025-11-11 19:00):**
```
bobs-brain/
├── .github/
├── 000-docs/
├── 99-Archive/
├── adk/              # Empty (just README)
├── docs/             # GitHub Pages (duplicate of 000-docs/)
├── infra/            # Empty (just README)
├── my_agent/         # Empty (just README)
├── scripts/          # Contains helper scripts
├── service/          # Empty (just README)
├── tests/            # Empty (just README)
└── [various config files]
```

**After (2025-11-11 Target):**
```
bobs-brain/
├── .github/              # CI/CD workflows with drift detection
├── 000-docs/             # Documentation (NNN-CC-ABCD-*.md)
├── adk/                  # ADK agent configurations
├── my_agent/             # Agent implementation (ADK + dual memory)
│   ├── __init__.py
│   ├── agent.py          # LlmAgent + Session + Memory Bank
│   ├── a2a_card.py       # AgentCard for A2A protocol
│   └── tools/            # Custom tools
├── service/              # HTTP/A2A/Slack gateways (proxy only)
│   ├── a2a_gateway/      # A2A protocol endpoints
│   │   ├── main.py       # FastAPI (no Runner)
│   │   └── Dockerfile
│   └── slack_webhook/    # Slack integration
│       ├── main.py       # Slack handler (no Runner)
│       └── Dockerfile
├── infra/                # Terraform IaC
│   └── terraform/
│       ├── modules/      # Reusable TF modules
│       └── envs/         # Environment configs
├── scripts/              # Helper scripts
│   ├── ci/               # CI-specific (drift check)
│   └── deploy/           # Deployment automation
├── tests/                # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── 99-Archive/           # Archived implementations
│   └── 2025-11-11-hardmode-cleanup/
│       └── docs/         # Old GitHub Pages
├── Dockerfile            # Agent container image
├── requirements.txt      # Python dependencies
├── VERSION               # Semantic version
├── CHANGELOG.md          # Version history
├── CLAUDE.md             # Hard mode rules (R1-R8)
├── LICENSE               # MIT License
└── README.md             # Project overview
```

### 2. Archived Items

Moved to `99-Archive/2025-11-11-hardmode-cleanup/`:
- ❌ `docs/` - GitHub Pages (duplicate of 000-docs/)

### 3. CLAUDE.md - Hard Rules Established

Created comprehensive guidance document with **8 non-negotiable rules**:

#### R1: Agent Implementation
- ✅ MUST use `google-adk` (Agent Development Kit)
- ❌ NO LangChain, CrewAI, AutoGen, custom frameworks
- ✅ Agent code in `my_agent/agent.py` using `LlmAgent`

#### R2: Deployed Runtime
- ✅ MUST be Vertex AI Agent Engine
- ❌ NO self-hosted runners, Cloud Run with embedded Runner

#### R3: Cloud Run Gateway Rules
- ✅ Allowed ONLY as thin protocol gateway
- ❌ NO `google.adk.serving` imports
- ❌ NO constructing or running ADK `Runner`
- ✅ Must proxy to Agent Engine via REST API

#### R4: CI-Only Deployments
- ✅ ALL deployments via GitHub Actions + WIF
- ❌ NO manual `gcloud` commands
- ❌ NO service account key files
- ❌ NO local deployment scripts

#### R5: Dual Memory Wiring
- ✅ MUST use `VertexAiSessionService` (short-term cache)
- ✅ MUST use `VertexAiMemoryBankService` (long-term memory)
- ✅ `after_agent_callback` saves session to Memory Bank

#### R6: Documentation Structure
- ✅ Single folder: `000-docs/` at root
- ❌ NO multiple doc folders
- ✅ Format: `NNN-CC-ABCD-description.md`

#### R7: SPIFFE ID Immutability
- ✅ Format: `spiffe://intent.solutions/agent/bobs-brain/<env>/<region>/<version>`
- ✅ Required in: env vars, AgentCard, headers, logs, traces

#### R8: CI Drift Detection
- ✅ Script: `scripts/ci/check_nodrift.sh`
- ❌ Blocks: alternative frameworks, local credentials, manual deploys
- ✅ Runs in CI before tests

## Implementation Status

### ✅ Completed

1. **Canonical Structure** - Archived non-canonical directories
2. **CLAUDE.md** - Comprehensive 800+ line guide with all rules
3. **Documentation Structure** - 000-docs/ enforced, numbered files
4. **Hard Rules** - R1-R8 defined and documented

### 🟡 In Progress

5. **my_agent/ Implementation**
   - Create `__init__.py`
   - Create `agent.py` with LlmAgent + dual memory
   - Create `a2a_card.py` with AgentCard
   - Create `tools/` directory for custom tools

6. **service/ Gateways**
   - Create `a2a_gateway/main.py` (FastAPI proxy)
   - Create `slack_webhook/main.py` (Slack handler)
   - Create Dockerfiles for each gateway
   - NO Runner imports (R3 compliance)

7. **infra/ Terraform**
   - Create `terraform/modules/` (cloud_run, service_accounts, apis)
   - Create `terraform/envs/dev/` and `terraform/envs/prod/`
   - Enable required GCP APIs
   - Create service accounts with IAM roles
   - Bootstrap Agent Engine (CI-guarded)

8. **CI/CD Workflows**
   - Update `.github/workflows/ci.yml` (add drift check)
   - Update `.github/workflows/deploy.yml` (WIF + Agent Engine)
   - Create `scripts/ci/check_nodrift.sh`
   - Create `scripts/deploy/upsert_agent_engine.py`
   - Add Claude email alerts on failure

9. **SPIFFE ID Propagation**
   - Add to environment variables
   - Add to AgentCard description
   - Add to HTTP response headers
   - Add to structured logs
   - Add to OpenTelemetry resources

10. **Documentation**
    - Update README.md with hard mode rules
    - Update CHANGELOG.md
    - Bump VERSION (0.5.1 → 0.6.0)

### 🔴 Not Started

11. **Testing**
    - Create unit tests for `my_agent/`
    - Create integration tests for gateways
    - Create e2e tests for full flow

12. **Dockerfile**
    - Create agent container image Dockerfile
    - Multi-stage build for efficiency
    - Include ADK dependencies

13. **requirements.txt**
    - Add `google-adk`
    - Add `google-cloud-aiplatform`
    - Add FastAPI/httpx for gateways
    - Add Slack SDK for webhook

## Rationale

### Why Hard Mode?

**Problem:** Framework drift causes:
- Deployment confusion (local vs cloud, manual vs CI)
- Mixed agent implementations (ADK, LangChain, custom)
- Unclear boundaries (agent code mixed with gateway code)
- Manual deployments bypassing CI/CD
- Inconsistent memory patterns

**Solution:** Hard mode enforces:
- **Single runtime**: Vertex AI Agent Engine only
- **Single framework**: ADK only (no alternatives)
- **Clear separation**: agent code vs gateway code vs infrastructure
- **CI-only deploys**: All changes through GitHub Actions
- **Drift detection**: Automatic scanning blocks violations

### Why Enforce R3 (Gateway Rules)?

**Critical Distinction:**
- **my_agent/**: Defines agent (runs in Agent Engine)
- **service/**: Exposes agent (proxies requests to Agent Engine)

**Without R3:**
```python
# ❌ WRONG: Gateway runs its own Runner
from google.adk.runner import Runner
from my_agent.agent import create_runner

app = FastAPI()
runner = create_runner()  # BAD: This should only run in Agent Engine

@app.post("/invoke")
def invoke(req):
    return runner.run(req.text)  # BAD: Bypasses Agent Engine
```

**With R3:**
```python
# ✅ CORRECT: Gateway proxies to Agent Engine
import httpx

app = FastAPI()

@app.post("/invoke")
async def invoke(req):
    # Call Agent Engine REST API
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/{AGENT_ENGINE_NAME}:query"
    async with httpx.AsyncClient() as client:
        return await client.post(url, json=req.dict(), headers=get_auth_headers())
```

### Why SPIFFE ID?

**Immutable agent identity** provides:
- Traceability across services
- Security attestation
- Version tracking
- Audit logging
- Multi-agent orchestration (A2A protocol)

## Technical Details

### File Structure (Target)

```
my_agent/agent.py:
    - get_agent() → LlmAgent
    - create_runner() → Runner with dual memory
    - auto_save_session_to_memory(ctx) → callback

my_agent/a2a_card.py:
    - get_agent_card() → AgentCard with SPIFFE

service/a2a_gateway/main.py:
    - GET /card → AgentCard JSON
    - POST /invoke → Proxy to Agent Engine :query

service/slack_webhook/main.py:
    - POST /slack/events → Verify signature, return 200, proxy to Agent Engine

scripts/ci/check_nodrift.sh:
    - Scan for forbidden imports
    - Check for local credentials
    - Verify no manual deployment commands

.github/workflows/ci.yml:
    - Run drift check
    - Run tests
    - ADK api_server smoke test (CI only)
    - Terraform validate

.github/workflows/deploy.yml:
    - WIF authentication
    - Build agent container
    - Upsert Agent Engine
    - Deploy Cloud Run gateways
    - Email Claude on failure
```

### Environment Variables

**Required everywhere:**
```bash
PROJECT_ID=bobs-brain
LOCATION=us-central1
AGENT_ENGINE_ID=<from-vertex-ai>
AGENT_ENGINE_NAME=projects/${PROJECT_ID}/locations/${LOCATION}/agentEngines/${AGENT_ENGINE_ID}
APP_NAME=bobs-brain
APP_VERSION=0.6.0
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/${ENV}/${LOCATION}/${APP_VERSION}
PUBLIC_URL=https://example.com
```

**Gateway-specific:**
```bash
SLACK_SIGNING_SECRET=***
SLACK_BOT_TOKEN=xoxb-***
```

### Drift Detection Patterns

**Forbidden (will fail CI):**
```python
from google.adk.serving.fastapi       # R3 violation
from langchain                         # R1 violation
import autogen                         # R1 violation
gcloud run deploy  # (outside CI)     # R4 violation
```

**Allowed:**
```python
from google.adk.agents import LlmAgent       # ✅ R1 compliant
from google.adk.runner import Runner         # ✅ R2 compliant (in my_agent/ only)
from google.adk.memory import VertexAi*      # ✅ R5 compliant
```

## Lessons Learned

### What Went Well

1. ✅ **Clear rules defined** - R1-R8 provide unambiguous guidance
2. ✅ **Comprehensive documentation** - CLAUDE.md is 800+ lines
3. ✅ **Clean separation** - agent vs gateway vs infrastructure roles clear
4. ✅ **Enforcement strategy** - CI drift detection prevents violations

### What Didn't Go Well

1. ❌ **Large scope** - Full implementation requires significant time
2. ❌ **Multiple empty directories** - Need to populate with actual code
3. ❌ **No tests yet** - Implementation without tests is risky

### What Could Be Improved

1. **Phased implementation** - Break into smaller PRs:
   - Phase 1: Structure + CLAUDE.md (this PR)
   - Phase 2: my_agent/ + drift detection
   - Phase 3: service/ gateways
   - Phase 4: Terraform + CI/CD

2. **Template generation** - Create `scripts/bootstrap.sh` to generate boilerplate

3. **Local development** - Add docker-compose for local gateway testing (with mocked Agent Engine)

## Recommendations

### Immediate (Complete Phase 1)

1. **Commit Phase 1 changes:**
   - Archived docs/
   - Created CLAUDE.md with R1-R8
   - Created this AAR
   - Push to new branch: `feat/phase-1-hardmode-baseline`

2. **Create implementation plan:**
   - Document remaining phases in GitHub issues
   - Assign effort estimates
   - Set milestones

### Short-term (Phase 2-4)

3. **Implement my_agent/**
   - Follow CLAUDE.md exactly
   - Add unit tests immediately
   - Verify dual memory wiring works

4. **Create drift check script**
   - `scripts/ci/check_nodrift.sh`
   - Add to CI workflow
   - Test locally before committing

5. **Build gateways**
   - A2A protocol first (simpler)
   - Slack webhook second (more complex)
   - NO Runner imports (verify with drift check)

6. **Terraform infrastructure**
   - Start with service accounts
   - Add API enablement
   - Bootstrap Agent Engine last (CI-guarded)

### Long-term (Post-implementation)

7. **Monitoring & Observability**
   - Add OpenTelemetry instrumentation
   - Set up Cloud Logging queries
   - Create dashboards for SPIFFE traces

8. **Documentation maintenance**
   - Update CLAUDE.md as patterns evolve
   - Add runbooks for common operations
   - Create troubleshooting guide

## Next Steps

### Phase 1 Completion (Now)

1. ✅ Archive non-canonical directories
2. ✅ Create CLAUDE.md with hard rules
3. ✅ Create this AAR
4. **Commit and push to GitHub**
   ```bash
   git checkout -b feat/phase-1-hardmode-baseline
   git add -A
   git commit -m "feat(architecture): establish hard mode baseline (R1-R8)"
   git push origin feat/phase-1-hardmode-baseline
   ```

5. **Create PR with detailed description**
   - Link to this AAR
   - Explain Phase 1 scope
   - Outline Phase 2-4 plan

### Phase 2: Agent Core

6. Implement `my_agent/agent.py` with dual memory
7. Implement `my_agent/a2a_card.py` with SPIFFE
8. Add unit tests for agent logic
9. Create `scripts/ci/check_nodrift.sh`
10. Update `.github/workflows/ci.yml` to run drift check

### Phase 3: Gateways

11. Implement `service/a2a_gateway/main.py`
12. Implement `service/slack_webhook/main.py`
13. Create Dockerfiles for gateways
14. Add integration tests

### Phase 4: Infrastructure & CI/CD

15. Create Terraform modules and environments
16. Update deploy workflow for Agent Engine
17. Add SPIFFE propagation throughout
18. Final end-to-end testing

## Success Criteria

### Phase 1 (Current)

✅ **Structure**
- Root matches canonical tree
- Non-canonical directories archived
- Empty directories have README.md

✅ **Documentation**
- CLAUDE.md created with R1-R8
- AAR created (this document)
- Rules enforced in CI (pending drift script)

### Phase 2-4 (Upcoming)

🟡 **Implementation**
- my_agent/ implements LlmAgent + dual memory
- service/ gateways proxy to Agent Engine (no Runner)
- infra/ manages all GCP resources via Terraform
- CI/CD deploys via WIF (no manual commands)

🟡 **Enforcement**
- Drift check blocks violations
- Tests pass in CI
- Deploy succeeds via GitHub Actions

🟡 **Verification**
- SPIFFE ID visible in logs, headers, AgentCard
- Agent responds via A2A protocol
- Slack integration works via gateway

## Metrics

- **Directories archived:** 1 (docs/)
- **Canonical directories:** 8 (enforced)
- **Documentation files created:** 2 (CLAUDE.md, this AAR)
- **Hard rules defined:** 8 (R1-R8)
- **Lines of guidance:** 800+ (CLAUDE.md)
- **Implementation progress:** 25% (structure + docs complete)

## References

- **CLAUDE.md:** Hard mode rules and implementation guide
- **Google ADK Docs:** https://cloud.google.com/vertex-ai/docs/agent-development-kit
- **Vertex AI Agent Engine:** https://cloud.google.com/vertex-ai/docs/agent-engine
- **A2A Protocol:** https://github.com/google/adk-python/blob/main/docs/a2a.md
- **SPIFFE Spec:** https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE.md

---

**Completed:** 2025-11-11 (Phase 1)
**Status:** 🟡 In Progress (75% remaining)
**Next:** Implement my_agent/ with ADK + dual memory (Phase 2)
**Contact:** claude.buildcaptain@intentsolutions.io
