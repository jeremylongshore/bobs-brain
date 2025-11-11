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

## 📚 Documentation

### Key Documents

- **[CLAUDE.md](CLAUDE.md)** - Hard Mode rules and enforcement (800+ lines)
- **[000-docs/053-AA-REPT-hardmode-baseline.md](000-docs/053-AA-REPT-hardmode-baseline.md)** - Phase 1-2 implementation AAR
- **[000-docs/054-AT-ALIG-notebook-alignment-checklist.md](000-docs/054-AT-ALIG-notebook-alignment-checklist.md)** - Alignment with Google Cloud patterns
- **[000-docs/055-AA-CRIT-import-path-corrections.md](000-docs/055-AA-CRIT-import-path-corrections.md)** - Import path verification
- **[000-docs/056-AA-CONF-usermanual-import-verification.md](000-docs/056-AA-CONF-usermanual-import-verification.md)** - User manual compliance
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

### Completed (Phase 1-2)

- ✅ Flattened repository structure (canonical 8-directory tree)
- ✅ Hard Mode rules documented (R1-R8) in CLAUDE.md
- ✅ ADK LlmAgent implementation with dual memory
- ✅ A2A protocol AgentCard
- ✅ Drift detection script (`check_nodrift.sh`)
- ✅ CI/CD workflows with drift-first pipeline
- ✅ Import path verification (aligned with Google Cloud notebooks)
- ✅ Configuration template (.env.example)
- ✅ User manual reference notebooks

### In Progress (Phase 3)

- 🟡 Service gateways (A2A + Slack) - proxy only
- 🟡 Dockerfile for Agent Engine container
- 🟡 Unit tests for my_agent/

### Planned (Phase 4)

- ⏳ Terraform infrastructure (Agent Engine, Cloud Run, IAM)
- ⏳ GitHub Actions deployment workflows
- ⏳ Production deployment validation

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

**Last Updated:** 2025-11-11
**Version:** 0.6.0
**Status:** Phase 2 Complete (Agent Core + Drift Detection)
