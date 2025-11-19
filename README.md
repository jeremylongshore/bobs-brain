# 🤖 Bob's Brain - Hard Mode

<div align="center">

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![ADK](https://img.shields.io/badge/Google-ADK-4285F4.svg)](https://cloud.google.com/vertex-ai/docs/agent-development-kit)
[![Agent Engine](https://img.shields.io/badge/Vertex%20AI-Agent%20Engine-4285F4.svg)](https://cloud.google.com/vertex-ai/docs/agent-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Production Slack AI assistant powered by Google ADK and Vertex AI Agent Engine**

**Hard Mode:** ADK-only, CI-enforced, drift-protected architecture

[Quick Start](#-quick-start) • [Architecture](#-architecture) • [Hard Rules](#-hard-rules) • [Documentation](000-docs/)

</div>

---

## 🎯 What is Bob's Brain?

Bob's Brain is a **production Slack AI assistant** built with Google's Agent Development Kit (ADK) and deployed on Vertex AI Agent Engine. It enforces strict architectural rules ("Hard Mode") to ensure maintainability, scalability, and compliance.

### Hard Mode Principles

✅ **ADK-Only** - No alternative frameworks (LangChain, CrewAI, etc.)
✅ **Agent Engine Runtime** - Managed runtime, not self-hosted
✅ **CI-Only Deployments** - All deploys via GitHub Actions with WIF
✅ **Dual Memory** - Session + Memory Bank for conversation continuity
✅ **Drift Detection** - Automated CI scans block architectural violations
✅ **SPIFFE Identity** - Immutable agent identity propagated everywhere
✅ **Gateway Separation** - Cloud Run proxies only (no embedded runners)
✅ **Single Docs Folder** - All documentation in `000-docs/`

### Built from Template

Bob's Brain is built from the **Intent Agent Model (IAM1)** template:

**Template Repository:** [iam1-intent-agent-model-vertex-ai](https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai)

The template provides:
- Hard Mode architecture (R1-R8 rules)
- ADK + Agent Engine foundation
- Terraform infrastructure boilerplate
- CI/CD workflows with drift detection
- Complete documentation structure

Bob's Brain is a **specific implementation** of this template for Slack integration.

---

## 🏗️ Architecture

### Canonical Directory Structure

```
bobs-brain/
├── .github/           # CI/CD workflows (drift check, tests, deploy)
├── 000-docs/          # All documentation (AARs, architecture, runbooks)
├── my_agent/          # Agent implementation (ADK LlmAgent + tools)
│   ├── agent.py       # Core agent with dual memory
│   ├── a2a_card.py    # A2A protocol AgentCard
│   └── tools/         # Custom tool implementations
├── service/           # Protocol gateways (proxy to Agent Engine)
│   ├── a2a_gateway/   # A2A protocol HTTP endpoint
│   └── slack_webhook/ # Slack event handler
├── infra/             # Terraform IaC (Agent Engine, Cloud Run, IAM)
├── scripts/           # CI scripts (drift detection, deployment)
├── tests/             # Unit and integration tests
├── .env.example       # Configuration template
├── requirements.txt   # Python dependencies (google-adk, a2a-sdk)
├── Dockerfile         # Agent container for Agent Engine
└── VERSION            # Semantic version (MAJOR.MINOR.PATCH)
```

### Data Flow

```
Slack → service/slack_webhook/ (Cloud Run)
          ↓ (REST API)
       Vertex AI Agent Engine ← my_agent/ (ADK LlmAgent)
          ↓
       Dual Memory (Session + Memory Bank)
```

---

## ⚡ Hard Rules (R1-R8)

These rules are **enforced in CI**. Violations will fail the build.

### R1: Agent Implementation
- ✅ **Required:** `google-adk` LlmAgent
- ❌ **Prohibited:** LangChain, CrewAI, AutoGen, custom frameworks

### R2: Deployed Runtime
- ✅ **Required:** Vertex AI Agent Engine
- ❌ **Prohibited:** Self-hosted runners, Cloud Run with embedded Runner

### R3: Cloud Run Gateway Rules
- ✅ **Allowed:** HTTP gateways that proxy to Agent Engine via REST
- ❌ **Prohibited:** Importing `Runner`, direct LLM calls, agent logic in gateways

### R4: CI-Only Deployments
- ✅ **Required:** GitHub Actions with Workload Identity Federation (WIF)
- ❌ **Prohibited:** Manual `gcloud` commands, service account keys

### R5: Dual Memory Wiring
- ✅ **Required:** VertexAiSessionService + VertexAiMemoryBankService
- ✅ **Required:** `after_agent_callback` to persist sessions

### R6: Single Docs Folder
- ✅ **Required:** All docs in `000-docs/` with NNN-CC-ABCD naming
- ❌ **Prohibited:** Multiple doc folders, scattered documentation

### R7: SPIFFE ID
- ✅ **Required:** `spiffe://intent.solutions/agent/bobs-brain/<env>/<region>/<version>`
- ✅ **Required:** Propagated in AgentCard, logs, HTTP headers

### R8: Drift Detection
- ✅ **Required:** CI scans for forbidden imports/patterns
- ❌ **Blocks:** Alternative frameworks, Runner in gateways, local credentials

**Enforcement:** `scripts/ci/check_nodrift.sh` runs first in CI pipeline.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Google Cloud account with Vertex AI enabled
- Slack workspace with admin access
- GitHub account (for CI/CD)

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values:
#   - PROJECT_ID (GCP project)
#   - LOCATION (e.g., us-central1)
#   - AGENT_ENGINE_ID (created by Terraform)
#   - AGENT_SPIFFE_ID (immutable identity)
```

### 2. Verify Imports

```bash
# Test that all ADK imports work
python3 -c "
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from a2a.types import AgentCard
print('✅ All imports successful')
"
```

### 3. Run Drift Detection

```bash
# Verify no hard rule violations
bash scripts/ci/check_nodrift.sh
```

### 4. Deploy (CI Only)

```bash
# Push to main branch (triggers CI/CD)
git add .
git commit -m "feat: your feature description"
git push origin main

# GitHub Actions will:
# 1. Run drift detection
# 2. Run tests
# 3. Build Docker container
# 4. Deploy to Vertex AI Agent Engine
# 5. Deploy Cloud Run gateways
```

---

## 🚀 Deployment to Vertex AI Agent Engine

Bob's Brain deploys to **Vertex AI Agent Engine** using ADK CLI with full CI/CD automation.

### Deployment Architecture

```
GitHub Actions (WIF)
    ↓
ADK CLI (adk deploy agent_engine)
    ↓
Vertex AI Agent Engine (Managed Runtime)
    ↑
Cloud Run Gateways (A2A + Slack) - REST API Proxy
```

### Prerequisites

Before deploying, ensure:

- ✅ **GCP Project** - With Vertex AI and Cloud Run APIs enabled
- ✅ **GitHub Secrets** - WIF provider, service account, project ID, region, staging bucket
- ✅ **Terraform State** - Infrastructure applied (`infra/terraform/`)
- ✅ **Staging Bucket** - Created by Terraform (`gs://<project-id>-adk-staging`)

### Deployment Workflow

**Automatic (Recommended):**
```bash
# Push to main branch
git push origin main

# GitHub Actions automatically:
# 1. Runs drift detection (blocks if violations found)
# 2. Runs tests
# 3. Authenticates via Workload Identity Federation (no keys!)
# 4. Deploys agent to Agent Engine with --trace_to_cloud
# 5. Deploys Cloud Run gateways
```

**Manual Trigger:**
1. Go to: https://github.com/jeremylongshore/bobs-brain/actions/workflows/deploy-agent-engine.yml
2. Click "Run workflow"
3. Select environment: `dev`, `staging`, or `prod`
4. Click "Run workflow"

### ADK CLI Deployment Command

The workflow executes:

```bash
adk deploy agent_engine my_agent \
  --project "bobs-brain-dev" \
  --region "us-central1" \
  --staging_bucket "gs://bobs-brain-dev-adk-staging" \
  --display_name "bobs-brain-dev" \
  --description "Bob's Brain AI Assistant - Deployed from GitHub Actions" \
  --trace_to_cloud \
  --env_file .env.example
```

**What this does:**
1. Packages agent code from `my_agent/`
2. Uses `my_agent/agent_engine_app.py` as entrypoint (exports `app` variable)
3. Builds Docker container
4. Uploads to staging bucket
5. Deploys to Agent Engine
6. **Enables Cloud Trace automatically** (`--trace_to_cloud` flag)

### Required GitHub Secrets

Configure in repository settings (Settings → Secrets → Actions):

| Secret | Description | Example |
|--------|-------------|---------|
| `WIF_PROVIDER` | Workload Identity Federation provider | `projects/123.../providers/github-oidc` |
| `WIF_SERVICE_ACCOUNT` | Service account email for deployments | `github-actions@bobs-brain-dev.iam.gserviceaccount.com` |
| `PROJECT_ID` | GCP project ID | `bobs-brain-dev` |
| `REGION` | Deployment region | `us-central1` |
| `STAGING_BUCKET` | GCS staging bucket URL | `gs://bobs-brain-dev-adk-staging` |

**Setup Guide:** See [000-docs/068-OD-CONF-github-secrets-configuration.md](000-docs/068-OD-CONF-github-secrets-configuration.md)

### Deployment Verification

After deployment completes:

**1. Check Agent Engine:**
```bash
gcloud ai reasoning-engines list \
  --project=bobs-brain-dev \
  --region=us-central1 \
  --filter="displayName:bobs-brain"
```

**2. Check Cloud Trace (automatic telemetry):**
```
https://console.cloud.google.com/traces/list?project=bobs-brain-dev
```

**3. Check Cloud Logging:**
```
https://console.cloud.google.com/logs/query?project=bobs-brain-dev&query=resource.type="aiplatform.googleapis.com/AgentEngine"
```

**4. Test A2A Gateway:**
```bash
curl https://bobs-brain-a2a-gateway-HASH.run.app/card | jq
```

**5. Test Agent Invocation:**
```bash
curl -X POST https://bobs-brain-a2a-gateway-HASH.run.app/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ADK?", "session_id": "test"}'
```

### Observability (Automatic with --trace_to_cloud)

**Cloud Trace** - Distributed tracing of every agent invocation:
- Agent execution timing
- Memory operations (Session + Memory Bank)
- Model inference latency
- Tool execution spans

**Cloud Logging** - Structured logs with SPIFFE ID:
- Agent invocations
- Memory auto-save operations
- Error stack traces

**Cloud Monitoring** - Performance metrics:
- Request count
- Response time (P50, P95, P99)
- Error rate
- Token usage

**Error Reporting** - Exception tracking and grouping

**See:** [000-docs/069-OD-TELE-observability-telemetry-guide.md](000-docs/069-OD-TELE-observability-telemetry-guide.md)

### Deployment Runbook

For complete step-by-step deployment instructions:

**📖 [000-docs/070-OD-RBOK-deployment-runbook.md](000-docs/070-OD-RBOK-deployment-runbook.md)**

Includes:
- Prerequisites checklist
- 7-phase deployment process (~2 hours)
- Verification steps
- Rollback procedures
- Troubleshooting guide

### Key Features

✅ **Automatic Telemetry** - Cloud Trace enabled with single flag
✅ **Dual Memory Persistence** - Session Service + Memory Bank auto-save
✅ **SPIFFE ID Propagation** - Immutable identity in all logs/traces
✅ **WIF Authentication** - No service account keys (R4 compliance)
✅ **Drift Protection** - CI blocks architectural violations
✅ **Gateway Separation** - Cloud Run as thin proxy (R3 compliance)

---

## 📚 Documentation

### Key Documents

**Architecture & Rules:**
- **[CLAUDE.md](CLAUDE.md)** - Hard Mode rules and enforcement (800+ lines)
- **[000-docs/053-AA-REPT-hardmode-baseline.md](000-docs/053-AA-REPT-hardmode-baseline.md)** - Phase 1-2 implementation AAR
- **[000-docs/054-AT-ALIG-notebook-alignment-checklist.md](000-docs/054-AT-ALIG-notebook-alignment-checklist.md)** - Alignment with Google Cloud patterns
- **[000-docs/055-AA-CRIT-import-path-corrections.md](000-docs/055-AA-CRIT-import-path-corrections.md)** - Import path verification
- **[000-docs/056-AA-CONF-usermanual-import-verification.md](000-docs/056-AA-CONF-usermanual-import-verification.md)** - User manual compliance

**Deployment & Operations:**
- **[000-docs/067-PM-PLAN-vertex-ai-deployment-plan.md](000-docs/067-PM-PLAN-vertex-ai-deployment-plan.md)** - Complete deployment plan with research
- **[000-docs/068-OD-CONF-github-secrets-configuration.md](000-docs/068-OD-CONF-github-secrets-configuration.md)** - GitHub secrets setup guide (WIF)
- **[000-docs/069-OD-TELE-observability-telemetry-guide.md](000-docs/069-OD-TELE-observability-telemetry-guide.md)** - Cloud Trace, Logging, Monitoring
- **[000-docs/070-OD-RBOK-deployment-runbook.md](000-docs/070-OD-RBOK-deployment-runbook.md)** - Step-by-step deployment runbook

**Configuration:**
- **[.env.example](.env.example)** - Configuration template with all required variables

### User Manual (Google Cloud Notebooks)

- **[000-docs/001-usermanual/](000-docs/001-usermanual/)** - Official ADK reference notebooks
  - Multi-agent systems with Claude (102KB)
  - Memory for ADK in Cloud Run (30KB)

### Document Filing System

All docs follow `NNN-CC-ABCD-description.md` format:
- **NNN**: Sequential number (001-999)
- **CC**: Category (PP, AT, TQ, OD, LS, RA, MC, PM, DR, UC, BL, RL, AA, WA, DD, MS)
- **ABCD**: Document type (ARCH, REPT, ALIG, CRIT, CONF, etc.)
- **description**: 1-4 words in kebab-case

---

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests
pytest

# Check coverage
pytest --cov=my_agent --cov-report=html
```

---

## 🛠️ Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature
```

### 2. Implement Changes

- Edit code in `my_agent/` (agent logic)
- Edit code in `service/` (gateways only - no Runner imports)
- Add tests in `tests/`
- Update docs in `000-docs/`

### 3. Run Local Checks

```bash
# Drift detection
bash scripts/ci/check_nodrift.sh

# Tests
pytest

# Linting
flake8 my_agent/ service/
black --check my_agent/ service/
mypy my_agent/ service/
```

### 4. Commit & Push

```bash
git add .
git commit -m "feat(scope): description

Details about the change

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"
git push origin feature/your-feature
```

### 5. Create Pull Request

- CI will run drift detection, tests, and validation
- Merge only if all checks pass

---

## 🔧 Configuration

### Required Environment Variables

```bash
# Google Cloud
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
AGENT_ENGINE_ID=your-agent-engine-id

# Agent Identity (R7)
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0

# Application
APP_NAME=bobs-brain
APP_VERSION=0.6.0

# Slack (optional)
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret

# Gateway URLs (R3)
PUBLIC_URL=https://your-a2a-gateway.run.app
```

See [.env.example](.env.example) for complete configuration template.

---

## 🚨 Troubleshooting

### ImportError: cannot import Runner

**Cause:** Violates R3 (Cloud Run as proxy only)

**Fix:** Remove `Runner` imports from `service/`. Use REST API calls to Agent Engine.

### CI failed: Drift violations detected

**Cause:** Forbidden imports found (LangChain, Runner in gateway, etc.)

**Fix:** Check `scripts/ci/check_nodrift.sh` output and remove violations.

### Deploy failed: Agent Engine not found

**Cause:** Agent Engine hasn't been bootstrapped

**Fix:**
1. Set `TF_VAR_allow_agent_engine_bootstrap=true` in Terraform (ONCE, CI only)
2. Verify Agent Engine exists in Vertex AI console

---

## 📊 Project Status

### Completed (Phase 1-4)

**Phase 1-2: Hard Mode Baseline**
- ✅ Flattened repository structure (canonical 8-directory tree)
- ✅ Hard Mode rules documented (R1-R8) in CLAUDE.md
- ✅ ADK LlmAgent implementation with dual memory
- ✅ A2A protocol AgentCard
- ✅ Drift detection script (`check_nodrift.sh`)
- ✅ CI/CD workflows with drift-first pipeline
- ✅ Import path verification (aligned with Google Cloud notebooks)
- ✅ Configuration template (.env.example)
- ✅ User manual reference notebooks

**Phase 3-4: Agent Engine Deployment**
- ✅ Agent Engine entrypoint (`my_agent/agent_engine_app.py`)
- ✅ Terraform infrastructure (Agent Engine, Cloud Run, IAM, staging bucket)
- ✅ GitHub Actions deployment workflow with WIF authentication
- ✅ GitHub secrets configuration guide (WIF setup)
- ✅ Cloud Trace automatic telemetry (`--trace_to_cloud` flag)
- ✅ Observability documentation (Trace, Logging, Monitoring, Error Reporting)
- ✅ Complete deployment runbook (7-phase, ~2 hours)
- ✅ README updated with deployment instructions

### In Progress (Phase 5)

- 🟡 Initial deployment to dev environment
- 🟡 Telemetry verification (Cloud Trace, logs, metrics)
- 🟡 Smoke testing (end-to-end agent invocations)

### Planned (Phase 6)

- ⏳ Production deployment validation
- ⏳ Slack integration testing
- ⏳ Performance baseline establishment
- ⏳ Custom monitoring dashboards

---

## 🤝 Contributing

This repository follows strict architectural rules (Hard Mode). Before contributing:

1. Read [CLAUDE.md](CLAUDE.md) completely
2. Understand all 8 hard rules (R1-R8)
3. Run `bash scripts/ci/check_nodrift.sh` locally
4. Ensure all tests pass
5. Update documentation in `000-docs/`

**All pull requests must pass drift detection and CI checks.**

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🔗 Resources

- **Google ADK Docs:** https://cloud.google.com/vertex-ai/docs/agent-development-kit
- **Vertex AI Agent Engine:** https://cloud.google.com/vertex-ai/docs/agent-engine
- **A2A Protocol:** https://github.com/google/adk-python/blob/main/docs/a2a.md
- **SPIFFE Spec:** https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE.md

---

**Last Updated:** 2025-11-19
**Version:** 0.6.0
**Status:** Phase 4 Complete (Agent Engine Deployment Ready)

**Next Milestone:** Initial deployment to dev environment with telemetry verification
