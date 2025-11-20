# 🤖 Bob's Brain

<div align="center">

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4.svg)](https://cloud.google.com/vertex-ai/docs/agent-development-kit)
[![Agent Engine](https://img.shields.io/badge/Vertex%20AI-Agent%20Engine-4285F4.svg)](https://cloud.google.com/vertex-ai/docs/agent-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Your AI teammate that keeps codebases clean, documented, and ready for production.**

Production Slack assistant built with Google ADK, Vertex AI Agent Engine, A2A protocol, Session Cache + Memory Bank. Hard Mode architecture enforces drift-free development. Open source for everyone.

[Quick Start](#-quick-start) • [What It Does](#-what-bob-does) • [Hard Mode Rules](#%EF%B8%8F-hard-mode-explained) • [Use as Template](#-use-as-template)

</div>

---

## 👋 What is Bob's Brain?

Bob's Brain is a **Slack AI assistant that actually helps your team ship better code.** Think of it as that senior engineer who remembers to update docs, catches architectural drift, and makes sure your CI doesn't break at 2am.

We built Bob using Google's Agent Development Kit (ADK) and Vertex AI Agent Engine, following what we call **"Hard Mode"** – a set of strict architectural rules that make agents maintainable, scalable, and actually production-ready.

### Why Bob Exists

Most AI coding assistants are demos. They work great in tutorials, fall apart in production. Bob's different:

- **Actually deployed** - Running in production Slack workspaces, not just localhost
- **Multi-repo aware** - Audits your entire portfolio, not just one project
- **Self-documenting** - Generates AARs, architecture docs, and runbooks as it works
- **Template-ready** - Copy this entire setup to your product in days, not months

### What Makes It "Hard Mode"

We enforce 8 architectural rules (R1-R8) that prevent the usual agent chaos:

- ✅ **ADK-only** - No mixing LangChain, CrewAI, or other frameworks
- ✅ **Managed runtime** - Vertex AI Agent Engine, not self-hosted containers
- ✅ **CI-enforced** - Automated checks block bad patterns before they merge
- ✅ **Memory that works** - Dual Session + Memory Bank for real continuity
- ✅ **Clean separation** - Cloud Run proxies, not franken-servers with embedded agents
- ✅ **One docs folder** - All docs in `000-docs/`, no scattered README files
- ✅ **Immutable identity** - SPIFFE IDs everywhere for clean tracing
- ✅ **Drift detection** - CI fails if you try to sneak in forbidden imports

**Tl;dr:** Bob's Brain is the agent system your CTO would approve, not yell about.

---

## 🎯 What Bob Does

Bob orchestrates an entire **software engineering department** of specialist agents:

### Core Capabilities

**🔍 Code Audits**
- Scans repos for ADK/Vertex compliance
- Detects architectural drift and anti-patterns
- Checks documentation quality and completeness

**🛠️ Automated Fixes**
- Creates fix plans for detected issues
- Generates pull requests with proper context
- Runs QA checks before suggesting merges

**📋 Portfolio Management**
- Audits multiple repos simultaneously
- Aggregates metrics across your entire org
- Stores results in centralized GCS buckets

**📝 Documentation**
- Writes AARs (After-Action Reports) for all major work
- Generates architecture diagrams and runbooks
- Maintains a searchable knowledge hub

**💬 Slack Integration**
- Responds to questions about your codebase
- Sends alerts for failed CI/CD runs
- Creates GitHub issues from Slack threads (coming soon)

### The Multi-Agent Team

Bob coordinates specialist agents for different tasks:

```
┌─────────────┐
│     Bob     │  ← Global orchestrator (your Slack interface)
└──────┬──────┘
       │
┌──────▼──────────────────────────┐
│ iam-senior-adk-devops-lead      │  ← Department foreman
└──────┬──────────────────────────┘
       │
       ├─→ iam-adk         (ADK/Vertex pattern expert)
       ├─→ iam-issue       (Issue detector & spec writer)
       ├─→ iam-fix-plan    (Fix strategy planner)
       ├─→ iam-fix-impl    (Fix implementer)
       ├─→ iam-qa          (Quality assurance)
       ├─→ iam-docs        (Documentation specialist)
       ├─→ iam-cleanup     (Code cleanup & refactoring)
       └─→ iam-index       (Knowledge hub curator)
```

Each agent has a specific job. No agent tries to do everything. Clean delegation, clear responsibilities.

---

## 🏗️ Architecture

### How It Works

**For end users (Slack):**
```
You in Slack
   ↓
Slack webhook (Cloud Run)
   ↓
Vertex AI Agent Engine ← Bob's Brain (ADK agent)
   ↓
Dual Memory (Session + Memory Bank)
```

**For portfolio audits (CLI):**
```
python3 scripts/run_portfolio_swe.py
   ↓
Portfolio Orchestrator
   ↓
iam-senior-adk-devops-lead (foreman)
   ↓
iam-* specialist agents
   ↓
GCS Knowledge Hub (results storage)
```

### Directory Structure

```
bobs-brain/
├── agents/
│   └── bob/              # Main agent (LlmAgent + tools)
│       ├── agent.py      # Core agent logic
│       ├── a2a_card.py   # Agent-to-Agent protocol
│       └── tools/        # Custom tools
│
├── service/              # HTTP gateways (proxies only!)
│   ├── a2a_gateway/      # A2A protocol endpoint
│   └── slack_webhook/    # Slack event handler
│
├── infra/terraform/      # All infrastructure as code
├── .github/workflows/    # CI/CD (drift check first!)
├── 000-docs/             # All documentation (AARs, guides)
├── tests/                # Unit & integration tests
└── scripts/              # Deployment & maintenance tools
```

**Key principle:** Cloud Run services are **proxies only**. They forward requests to Agent Engine via REST. No `Runner` imports allowed in gateways.

---

## ⚡️ Hard Mode Explained

"Hard Mode" means we enforce strict rules that keep this agent system maintainable as it scales. Here's what that looks like:

### The 8 Rules (R1-R8)

Every rule is **enforced in CI**. Violations fail the build automatically.

#### R1: Agent Implementation
- ✅ Use `google-adk` LlmAgent
- ❌ No LangChain, CrewAI, AutoGen, or custom frameworks

**Why:** Mixing frameworks creates integration nightmares. Pick one, stick with it.

#### R2: Deployed Runtime
- ✅ Deploy to Vertex AI Agent Engine
- ❌ No self-hosted runners or Cloud Run with embedded Runner

**Why:** Let Google manage the runtime. Focus on agent logic, not infrastructure.

#### R3: Gateway Separation
- ✅ Cloud Run as HTTP proxy to Agent Engine
- ❌ No `Runner` imports in gateway code

**Why:** Clean separation means gateways can restart without touching agents.

#### R4: CI-Only Deployments
- ✅ All deploys via GitHub Actions + Workload Identity Federation
- ❌ No manual `gcloud deploy` or service account keys

**Why:** Reproducible deployments. No "works on my machine" excuses.

#### R5: Dual Memory Wiring
- ✅ VertexAiSessionService + VertexAiMemoryBankService
- ✅ `after_agent_callback` to persist sessions

**Why:** Actual conversation continuity, not just storing embeddings.

#### R6: Single Docs Folder
- ✅ All docs in `000-docs/` with `NNN-CC-ABCD-name.md` format
- ❌ No scattered docs, multiple doc folders, or random READMEs

**Why:** Predictable structure. Easy to find things. Easy to copy to new repos.

#### R7: SPIFFE Identity
- ✅ `spiffe://intent.solutions/agent/bobs-brain/<env>/<region>/<version>`
- ✅ Propagated in AgentCard, logs, HTTP headers

**Why:** Immutable identity makes tracing and security audits straightforward.

#### R8: Drift Detection
- ✅ `scripts/ci/check_nodrift.sh` runs first in CI
- ❌ Blocks alternative frameworks, Runner in gateways, local creds

**Why:** Prevent architectural decay before it gets committed.

### Enforcement

The drift check script (`scripts/ci/check_nodrift.sh`) runs **before** anything else in CI:

```yaml
# .github/workflows/ci.yml
jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check for drift violations
        run: bash scripts/ci/check_nodrift.sh
        # Fails build if violations found
```

If drift check fails, the entire pipeline stops. No tests run. No deployment happens. Fix the violations first.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Google Cloud account with Vertex AI enabled
- (Optional) Slack workspace for integration
- (Optional) GitHub account for CI/CD

### 1. Clone & Setup

```bash
# Get the code
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure your environment
cp .env.example .env
# Edit .env with your GCP project details
```

### 2. Verify Everything Works

```bash
# Check all imports are valid
python3 -c "
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from a2a.types import AgentCard
print('✅ All ADK imports working')
"

# Run drift detection locally
bash scripts/ci/check_nodrift.sh
```

### 3. Deploy (CI Recommended)

**Option A: Via GitHub Actions (Recommended)**
```bash
# Push to main triggers automatic deployment
git add .
git commit -m "feat: your feature description"
git push origin main

# GitHub Actions handles:
# 1. Drift detection
# 2. Tests
# 3. Docker build
# 4. Deploy to Agent Engine
# 5. Deploy gateways
```

**Option B: Manual (Local Testing Only)**
```bash
# This is for local development only
# Production deployments MUST go through CI
cd agents/bob
python3 -c "from agent import get_agent; a = get_agent(); print('✅ Agent created')"
```

### 4. Run Portfolio Audits

```bash
# Audit all local repos
python3 scripts/run_portfolio_swe.py

# Audit specific repos
python3 scripts/run_portfolio_swe.py --repos bobs-brain,diagnosticpro

# Export results
python3 scripts/run_portfolio_swe.py --output audit.json --markdown report.md
```

**That's it.** You've got a working AI agent that can audit code, fix issues, and generate docs.

---

## 📦 Portfolio Multi-Repo Audits

One of Bob's superpowers: **auditing multiple repos at once** and giving you org-wide metrics.

### How It Works

1. Define your repos in `config/repos.yaml`:

```yaml
repos:
  - id: bobs-brain
    display_name: "Bob's Brain"
    local_path: "."
    tags: ["adk", "agents", "production"]
    slack_channel: "#bobs-brain-alerts"

  - id: diagnosticpro
    display_name: "DiagnosticPro"
    local_path: "external"  # Not checked out locally (skipped gracefully)
    tags: ["production", "firebase"]
```

2. Run the portfolio orchestrator:

```bash
python3 scripts/run_portfolio_swe.py
```

3. Get aggregated results:

```json
{
  "portfolio_run_id": "c98cc8f2-...",
  "timestamp": "2025-11-20T03:52:34Z",
  "summary": {
    "total_repos_analyzed": 5,
    "total_issues_found": 42,
    "total_issues_fixed": 30,
    "fix_rate": 71.4
  },
  "issues_by_severity": {
    "high": 5,
    "medium": 20,
    "low": 17
  },
  "repos": [...]
}
```

### CLI Options

```bash
# Basic usage
python3 scripts/run_portfolio_swe.py

# Specific repos only
python3 scripts/run_portfolio_swe.py --repos bobs-brain,diagnosticpro

# Filter by tags
python3 scripts/run_portfolio_swe.py --tag production

# Different modes
python3 scripts/run_portfolio_swe.py --mode preview   # Read-only analysis
python3 scripts/run_portfolio_swe.py --mode dry-run   # Show what would change
python3 scripts/run_portfolio_swe.py --mode create    # Actually fix issues

# Export results
python3 scripts/run_portfolio_swe.py --output results.json --markdown report.md
```

### Automated CI/CD Integration

The portfolio audit runs nightly via GitHub Actions:

```bash
# Manual trigger
gh workflow run portfolio-swe.yml \
  --ref main \
  --field repos=all \
  --field mode=preview
```

**Features:**
- ✅ Multi-repo ARV checks
- ✅ Automated audits (nightly at 2 AM UTC)
- ✅ JSON/Markdown export
- ✅ GCS storage for historical results (v0.9.0+)
- 📐 Slack notifications (coming soon)
- 📐 GitHub issue creation (coming soon)

**Roadmap:**
- **LIVE1-GCS (v0.9.0):** ✅ Complete - GCS org-wide storage
- **LIVE-BQ (Future):** BigQuery analytics integration
- **LIVE2 (Planned):** Vertex AI Search RAG + Agent Engine calls (dev-only)
- **LIVE3 (Planned):** Slack notifications + GitHub issue creation

---

## 🗄️ Org-Wide Storage

**New in v0.9.0** - All your portfolio audit results stored in one place for easy querying and analytics.

### What It Does

- **Centralized GCS bucket** for all audit results
- **Lifecycle management** (90-day retention for per-repo details)
- **Graceful fallback** (writes never crash your pipeline)
- **Environment-aware** (separate buckets for dev/staging/prod)

### GCS Bucket Structure

```
gs://intent-org-knowledge-hub-{env}/
├── portfolio/runs/{run_id}/summary.json        # Portfolio-level summary
├── portfolio/runs/{run_id}/per-repo/*.json     # Per-repo details
├── swe/agents/{agent}/runs/{run_id}.json       # Single-repo runs (future)
├── docs/                                        # Org docs (future)
└── vertex-search/                               # RAG snapshots (LIVE2+)
```

### Setup

**1. Enable in Terraform:**
```hcl
# infra/terraform/envs/dev.tfvars
org_storage_enabled     = true
org_storage_bucket_name = "intent-org-knowledge-hub-dev"
```

**2. Check readiness:**
```bash
python3 scripts/check_org_storage_readiness.py
python3 scripts/check_org_storage_readiness.py --write-test
```

**3. Enable writes:**
```bash
export ORG_STORAGE_WRITE_ENABLED=true
export ORG_STORAGE_BUCKET=intent-org-knowledge-hub-dev
```

**4. Run audit:**
```bash
python3 scripts/run_portfolio_swe.py
# Results automatically written to GCS
```

### Key Features

- ✅ **Opt-in by default** - Nothing writes unless you explicitly enable it
- ✅ **Graceful errors** - If GCS fails, pipeline continues (just logs error)
- ✅ **Fully tested** - 36 tests with 100% pass rate
- ✅ **IAM-secured** - Service account-based access control

**Documentation:**
- [Org Storage Architecture](000-docs/6767-112-AT-ARCH-org-storage-architecture.md)
- [LIVE1-GCS Implementation AAR](000-docs/6767-113-AA-REPT-live1-gcs-implementation.md)

---

## 🎨 Use as Template

Bob's Brain isn't just a product – it's a **complete multi-agent template** you can copy to your own repos.

### What You Get

When you port Bob's Brain to your product (DiagnosticPro, PipelinePilot, etc.):

- ✅ **Multi-agent architecture** - bob → foreman → iam-* specialists
- ✅ **SWE pipeline** - audit → issues → fixes → QA → docs
- ✅ **Shared contracts** - JSON schemas for all agent interactions
- ✅ **A2A communication** - Agent-to-Agent protocol wiring
- ✅ **ARV checks** - Agent Readiness Verification for CI
- ✅ **Gateway services** - A2A and Slack endpoints
- ✅ **Terraform infrastructure** - Agent Engine, Cloud Run, IAM
- ✅ **CI/CD workflows** - Drift check, tests, deploy
- ✅ **Documentation system** - 000-docs/ with filing standards

### Time to Port

- **Basic setup:** 1-2 days
- **Full integration:** 1 week
- **Production-ready:** 2 weeks (with proper testing)

### Porting Guides

Start here:
1. [Porting Guide](000-docs/6767-105-DR-GUIDE-porting-iam-department-to-new-repo.md) - Step-by-step instructions
2. [Integration Checklist](000-docs/6767-106-DR-STND-iam-department-integration-checklist.md) - Don't miss anything
3. [Template Scope](000-docs/6767-104-DR-STND-iam-department-template-scope-and-rules.md) - What to customize
4. [Template Files](templates/iam-department/README.md) - Reusable components

### Original Template

Bob's Brain is built on top of:
- [iam1-intent-agent-model-vertex-ai](https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai)

That's the foundational Hard Mode architecture. Bob extends it into a full multi-agent department.

---

## 🚀 Deployment to Vertex AI Agent Engine

Bob deploys to **Vertex AI Agent Engine** using ADK CLI with full CI/CD automation.

### Deployment Architecture

```
GitHub Actions (WIF)
    ↓
ADK CLI (adk deploy agent_engine)
    ↓
Vertex AI Agent Engine ← Managed runtime
    ↑
Cloud Run Gateways (A2A + Slack) ← HTTP proxies only
```

### Prerequisites

Before deploying:
- ✅ GCP project with Vertex AI enabled
- ✅ GitHub secrets configured (WIF provider, service account)
- ✅ Terraform infrastructure applied (`infra/terraform/`)
- ✅ Staging bucket created (`gs://<project-id>-adk-staging`)

### CI/CD Deployment (Recommended)

```bash
# Push to main triggers automatic deployment
git push origin main

# GitHub Actions automatically:
# 1. Runs drift detection (blocks if violations)
# 2. Runs tests
# 3. Authenticates via WIF (no keys!)
# 4. Builds Docker container
# 5. Deploys to Agent Engine
# 6. Deploys Cloud Run gateways
```

### Manual Deployment (Local Testing)

```bash
# For local development only
# Production MUST use CI

cd agents/bob
adk deploy agent_engine \
  --project-id=$PROJECT_ID \
  --region=$LOCATION \
  --staging-bucket=gs://$PROJECT_ID-adk-staging

# Deploy gateways
cd service/a2a_gateway
gcloud run deploy a2a-gateway --source .

cd ../slack_webhook
gcloud run deploy slack-webhook --source .
```

**Important:** Manual deployments skip drift checks and don't generate proper audit trails. Use CI for production.

---

## 📚 Documentation

All docs live in `000-docs/` following the `NNN-CC-ABCD-name.md` format.

### Key Documents

**Architecture & Hard Mode:**
- [CLAUDE.md](CLAUDE.md) - Hard Mode rules and enforcement (800+ lines)
- [Hardmode Baseline AAR](000-docs/6767-053-AA-REPT-hardmode-baseline.md) - Phase 1-2 implementation
- [Notebook Alignment](000-docs/6767-054-AT-ALIG-notebook-alignment-checklist.md) - Google Cloud patterns
- [Import Path Corrections](000-docs/6767-055-AA-CRIT-import-path-corrections.md) - ADK import verification

**Deployment & Operations:**
- [Deployment Plan](000-docs/6767-067-PM-PLAN-vertex-ai-deployment-plan.md) - Complete setup guide
- [GitHub Secrets](000-docs/6767-068-OD-CONF-github-secrets-configuration.md) - WIF configuration
- [Observability](000-docs/6767-069-OD-TELE-observability-telemetry-guide.md) - Cloud Trace, Logging
- [Deployment Runbook](000-docs/6767-070-OD-RBOK-deployment-runbook.md) - Step-by-step procedures

**Portfolio & Org Storage (v0.9.0):**
- [Portfolio Scope](000-docs/6767-109-PP-PLAN-multi-repo-swe-portfolio-scope.md) - PORT1/PORT2/PORT3 plan
- [Portfolio Orchestrator AAR](000-docs/6767-110-AA-REPT-portfolio-orchestrator-implementation.md) - Implementation
- [CI/Slack Integration](000-docs/6767-111-AT-ARCH-portfolio-ci-slack-integration-design.md) - Future design
- [Org Storage Architecture](000-docs/6767-112-AT-ARCH-org-storage-architecture.md) - GCS hub design
- [LIVE1-GCS AAR](000-docs/6767-113-AA-REPT-live1-gcs-implementation.md) - v0.9.0 implementation

**IAM Department Templates (v0.9.0):**
- [Template Standards](000-docs/6767-104-DR-STND-iam-department-template-scope-and-rules.md)
- [Porting Guide](000-docs/6767-105-DR-GUIDE-porting-iam-department-to-new-repo.md)
- [Integration Checklist](000-docs/6767-106-DR-STND-iam-department-integration-checklist.md)
- [Operations Runbook](000-docs/6767-107-RB-OPS-adk-department-operations-runbook.md)
- [User Guide](000-docs/6767-108-DR-GUIDE-how-to-use-bob-and-iam-department-for-swe.md)

### Document Filing System

Format: `NNN-CC-ABCD-description.md`

- **NNN:** Sequential number (001-999)
- **CC:** Category (PP, AT, TQ, OD, LS, RA, MC, PM, DR, UC, BL, RL, AA, WA, DD, MS)
- **ABCD:** Document type (ARCH, REPT, ALIG, CRIT, CONF, etc.)
- **description:** 1-4 words in kebab-case

**Example:** `6767-112-AT-ARCH-org-storage-architecture.md`

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest --cov=agents.bob --cov-report=html

# Verbose output
pytest -v
```

### Test Coverage

- ✅ Agent initialization and tool registration
- ✅ A2A protocol and AgentCard generation
- ✅ Portfolio orchestrator (36 tests for org storage)
- ✅ Storage config and GCS writer
- ✅ Memory wiring (Session + Memory Bank)

---

## 🛠️ Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature
```

### 2. Make Changes

- Edit agent logic in `agents/bob/`
- Edit gateway code in `service/` (proxies only, no Runner!)
- Add tests in `tests/`
- Update docs in `000-docs/`

### 3. Run Local Checks

```bash
# Drift detection
bash scripts/ci/check_nodrift.sh

# Tests
pytest

# Linting
flake8 agents/bob/ service/
black --check agents/bob/ service/
mypy agents/bob/ service/
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

CI will automatically:
- Run drift detection
- Run tests
- Deploy to staging (if PR is to main)

---

## 🔧 Configuration

### Environment Variables

Required in `.env`:

```bash
# GCP Core
PROJECT_ID=your-gcp-project
LOCATION=us-central1
AGENT_ENGINE_ID=your-engine-id
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.9.0

# Application
APP_NAME=bobs-brain
APP_VERSION=0.9.0

# Org Storage (v0.9.0+)
ORG_STORAGE_WRITE_ENABLED=true
ORG_STORAGE_BUCKET=intent-org-knowledge-hub-dev

# Vertex AI Search
VERTEX_SEARCH_DATASTORE_ID=adk-documentation

# Gateway URLs
PUBLIC_URL=https://your-a2a-gateway.run.app
```

See [.env.example](.env.example) for full template.

### Terraform Variables

In `infra/terraform/envs/{env}.tfvars`:

```hcl
project_id = "your-gcp-project"
location   = "us-central1"

# Org Storage
org_storage_enabled     = true
org_storage_bucket_name = "intent-org-knowledge-hub-dev"

# Agent Engine
agent_engine_id   = "bobs-brain-dev"
agent_runtime_sa  = "bob-agent-dev@your-project.iam.gserviceaccount.com"
```

---

## 🚨 Troubleshooting

### Drift Detection Failed

**Symptom:** CI fails with "Drift violations detected"

**Fix:**
```bash
# Run locally to see violations
bash scripts/ci/check_nodrift.sh

# Common issues:
# 1. Imported Runner in service/ → Remove it, use REST API
# 2. Found LangChain/CrewAI → Remove alternative frameworks
# 3. Service account keys in repo → Remove, use WIF
```

### Agent Can't Find ADK Docs

**Symptom:** Agent says "I don't have information about that ADK pattern"

**Fix:**
```bash
# Set up Vertex AI Search
bash scripts/deployment/setup_vertex_search.sh

# Check datastore exists
export VERTEX_SEARCH_DATASTORE_ID=adk-documentation
```

### Org Storage Not Writing

**Symptom:** Portfolio audit runs but no GCS files appear

**Fix:**
```bash
# Check readiness
python3 scripts/check_org_storage_readiness.py --write-test

# Common issues:
# 1. ORG_STORAGE_WRITE_ENABLED not set → export ORG_STORAGE_WRITE_ENABLED=true
# 2. Bucket doesn't exist → Apply Terraform with org_storage_enabled=true
# 3. No IAM permissions → Add service account to org_storage_writer_service_accounts
```

### Deploy Failed: Agent Engine Not Found

**Symptom:** `adk deploy` fails with "Agent Engine not found"

**Fix:**
```bash
# Create infrastructure first
cd infra/terraform
terraform init
terraform plan -var-file=envs/dev.tfvars
terraform apply -var-file=envs/dev.tfvars

# Verify engine exists
gcloud ai agent-engines list --region=us-central1
```

---

## 📊 Project Status

**Current Version:** v0.9.0

**Status:** ✅ Production-ready

**Recent Updates:**
- ✅ LIVE1-GCS: Org-wide storage with GCS (v0.9.0)
- ✅ PORT1-3: Multi-repo portfolio orchestration (v0.9.0)
- ✅ IAM Templates: Reusable multi-agent framework (v0.9.0)

**Roadmap:**
- 🔄 LIVE-BQ: BigQuery analytics integration
- 📐 LIVE2: Vertex AI Search RAG + Agent Engine calls (dev-only)
- 📐 LIVE3: Slack notifications + GitHub issue creation

**Metrics:**
- 226 files
- 36 tests (100% pass)
- 20+ comprehensive docs
- 8 enforced Hard Mode rules
- 3 deployment environments (dev/staging/prod)

---

## 🔧 What Was Wrong and What We Fixed (v0.7.0)

Before Hard Mode, Bob's Brain had typical agent repo problems:

**Problems:**
- ❌ Mixed frameworks (ADK + LangChain + custom code)
- ❌ Self-hosted runners (containers that sometimes crashed)
- ❌ Manual deployments (inconsistent environments)
- ❌ Scattered docs (README, wiki, notion, random .md files)
- ❌ No drift detection (architectural decay over time)

**Solutions (Hard Mode):**
- ✅ R1-R8 rules enforced in CI
- ✅ Vertex AI Agent Engine (let Google manage runtime)
- ✅ GitHub Actions with WIF (reproducible deploys)
- ✅ Single `000-docs/` folder with filing system
- ✅ Automated drift checks block violations

**Result:** Agent system that's maintainable, scalable, and actually works in production.

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Reporting Issues

- Use GitHub Issues
- Include drift check output if relevant
- Provide minimal reproduction steps

### Pull Requests

1. Fork the repository
2. Create feature branch (`feature/your-feature`)
3. Follow Hard Mode rules (R1-R8)
4. Add tests for new functionality
5. Update docs in `000-docs/`
6. Ensure drift check passes
7. Submit PR with clear description

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/bobs-brain.git
cd bobs-brain

# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run checks
bash scripts/ci/check_nodrift.sh
pytest
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

You're free to:
- Use this in commercial products
- Modify and distribute
- Use as a template for your own agents

Just keep the license notice and don't blame us if things break. 😊

---

## 🔗 Resources

**This Project:**
- [GitHub Repository](https://github.com/jeremylongshore/bobs-brain)
- [Release Notes](https://github.com/jeremylongshore/bobs-brain/releases)
- [Documentation](000-docs/)

**Foundation Template:**
- [iam1-intent-agent-model-vertex-ai](https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai)

**Google ADK & Vertex:**
- [ADK Documentation](https://cloud.google.com/vertex-ai/docs/agent-development-kit)
- [Agent Engine Docs](https://cloud.google.com/vertex-ai/docs/agent-engine)
- [Vertex AI Platform](https://cloud.google.com/vertex-ai)

**Related Technologies:**
- [A2A Protocol](https://github.com/google/adk-python) - Agent-to-Agent communication
- [SPIFFE](https://spiffe.io/) - Immutable identity framework
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) - Keyless auth

---

<div align="center">

**Built with ❤️ using Google ADK**

[⭐ Star us on GitHub](https://github.com/jeremylongshore/bobs-brain) • [📖 Read the docs](000-docs/) • [💬 Join the discussion](https://github.com/jeremylongshore/bobs-brain/discussions)

</div>
