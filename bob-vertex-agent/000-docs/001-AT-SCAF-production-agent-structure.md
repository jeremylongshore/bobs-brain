# Production Agent Structure Scaffold

**Last Updated:** 2025-11-10
**Category:** Architecture & Technical
**Type:** Scaffold
**Status:** Reference Implementation

---

## Overview

This document defines the production-ready directory structure for Google ADK + Vertex AI Agent Engine + A2A Protocol agents. It provides a clean, maintainable layout optimized for:

- **FastAPI server** with ADK + A2A endpoints
- **Agent Engine deployment** to Vertex AI
- **Cloud Run frontends** (optional)
- **CI/CD pipelines** with GitHub Actions
- **Developer experience** with clear separation of concerns

---

## 📁 Recommended Production Structure

```
bob-vertex-agent/
├─ main.py                     # FastAPI server (ADK + A2A endpoints, health check)
├─ requirements.txt            # google-adk, a2a-python, fastapi, uvicorn, aiplatform[adk,agent_engines]
├─ README.md                   # How to run local, deploy, env vars
├─ Makefile                    # make dev / test / deploy-agent / deploy-run
├─ .env.sample                 # PROJECT_ID, LOCATION, AGENT_ENGINE_ID, PUBLIC_URL, PORT
├─ .gitignore
├─ .dockerignore
├─ Dockerfile
├─ pyproject.toml              # uv dependencies (alternative to requirements.txt)
├─ uv.lock                     # Dependency lock file (if using uv)
│
├─ 000-docs/                   # Project documentation (Document Filing System v2.0)
│  ├─ 001-AT-SCAF-production-agent-structure.md  # This file
│  ├─ 002-DR-QREF-api-reference.md               # API endpoint reference
│  ├─ 003-PP-PLAN-deployment-strategy.md         # Deployment planning
│  └─ ...
│
├─ bob_agent/                  # Main agent module (or my_agent/)
│  ├─ __init__.py
│  ├─ agent.py                 # LlmAgent + Runner wiring to VertexAiSessionService + VertexAiMemoryBankService
│  ├─ a2a_manager.py           # AgentCard + skills for A2A discovery
│  ├─ tools.py                 # Custom tool funcs (e.g., get_current_time_tool)
│  ├─ retrievers.py            # RAG pipeline (Vertex AI Search + Rank)
│  ├─ prompts/
│  │  ├─ system.md             # Long-form instruction text (keeps code lean)
│  │  ├─ iam1_config.md        # IAM1 configuration and business rules
│  │  └─ sub_agent_prompts.md  # Sub-agent (IAM2) system prompts
│  └─ resources/
│     ├─ examples/
│     │  └─ a2a_examples.json  # Sample payloads for skills (optional)
│     └─ schemas/
│        └─ agent_card.json    # A2A AgentCard schema
│
├─ slack_webhook/              # Slack integration (Cloud Functions Gen2)
│  ├─ main.py                  # Webhook handler
│  ├─ requirements.txt         # Slack SDK dependencies
│  ├─ README.md                # Setup and configuration guide
│  └─ DEPLOYMENT.md            # Deployment instructions
│
├─ scripts/
│  ├─ run_local.sh             # uvicorn main:app --reload
│  ├─ smoke_test.sh            # curl /_health && curl /
│  ├─ deploy_agent_engine.sh   # gcloud builds + Agent Engine deploy
│  ├─ deploy_cloud_run.sh      # gcloud run deploy (if you front it with Cloud Run)
│  └─ setup_secrets.sh         # Setup Google Secret Manager secrets
│
├─ tests/
│  ├─ __init__.py
│  ├─ unit/
│  │  ├─ test_agent.py         # Asserts model, tools, callbacks wired
│  │  ├─ test_tools.py         # Pure unit tests for tool funcs
│  │  └─ test_retrievers.py    # RAG pipeline tests
│  ├─ integration/
│  │  ├─ test_a2a_protocol.py  # A2A discovery and coordination tests
│  │  ├─ test_agent_engine.py  # Agent Engine REST API tests
│  │  └─ test_slack_webhook.py # Slack integration tests
│  └─ load_test/
│     └─ load_test.py          # Locust load testing
│
├─ deployment/
│  ├─ terraform/               # Infrastructure as Code
│  │  ├─ dev/                  # Dev environment
│  │  ├─ prod/                 # Production environment
│  │  ├─ providers.tf          # GCP, GitHub, Random providers
│  │  ├─ apis.tf               # GCP services
│  │  ├─ iam.tf                # Permissions
│  │  ├─ service_accounts.tf  # Service accounts
│  │  ├─ storage.tf            # GCS buckets
│  │  ├─ github.tf             # GitHub secrets
│  │  └─ wif.tf                # Workload Identity Federation
│  └─ README.md                # Deployment guide
│
├─ data_ingestion/             # RAG data pipeline
│  ├─ data_ingestion_pipeline/ # Vertex AI Pipeline
│  ├─ pyproject.toml           # Dependencies
│  └─ README.md                # Ingestion guide
│
├─ knowledge-base/             # RAG knowledge base (5GB, 303 files)
│  ├─ google-vertex-ai/        # Vertex AI documentation
│  ├─ iams/                    # Agent system documentation
│  ├─ diagnostic-platform/     # Domain-specific knowledge
│  └─ ...                      # Other knowledge domains
│
├─ notebooks/                  # Jupyter notebooks
│  ├─ adk_app_testing.ipynb    # ADK app testing
│  ├─ evaluating_adk_agent.ipynb  # Agent evaluation
│  └─ intro_agent_engine.ipynb    # Agent Engine introduction
│
├─ claudes-docs/               # AI-generated documentation (flat 000-docs alternative)
│  ├─ 000-INDEX.md             # Index of all Claude-created docs
│  ├─ 004-AT-ARCH-bob-vertex-system-analysis.md
│  ├─ 005-DR-QREF-system-quick-reference.md
│  └─ ...
│
└─ .github/
   └─ workflows/
      ├─ ci.yml                # lint, type-check, unit tests
      ├─ deploy.yml            # on tag: build + deploy to Agent Engine (and Cloud Run if used)
      ├─ pr_checks.yaml        # PR validation
      └─ deploy-slack-webhook.yml  # Slack webhook deployment
```

---

## 🗂️ Current Bob's Brain Structure

**Current Implementation (as of 2025-11-10):**

```
bob-vertex-agent/
├─ app/                        # Agent application code
│  ├─ agent.py                 # Root IAM1 agent
│  ├─ agent_engine_app.py      # Agent Engine entry point
│  ├─ sub_agents.py            # IAM2 specialists
│  ├─ a2a_tools.py             # A2A Protocol
│  ├─ retrievers.py            # RAG pipeline
│  ├─ iam1_config.py           # Business model config
│  └─ templates.py             # Prompt templates
├─ slack-webhook/              # Cloud Function for Slack
│  ├─ main.py                  # Webhook handler
│  └─ requirements.txt
├─ deployment/                 # Infrastructure as Code
│  └─ terraform/
├─ data_ingestion/             # RAG data pipeline
├─ tests/                      # Test suites
│  ├─ unit/
│  ├─ integration/
│  └─ load_test/
├─ notebooks/                  # Jupyter notebooks
├─ claudes-docs/               # AI-generated documentation
├─ knowledge-base/             # RAG knowledge base (5GB, 303 files)
├─ Makefile                    # Development commands
├─ pyproject.toml              # Dependencies (uv)
├─ uv.lock                     # Dependency lock file
├─ deployment_metadata.json    # Current Agent Engine ID
├─ README.md                   # Project overview
└─ DEPLOYMENT_GUIDE.md         # Business model & scenarios
```

---

## 🔄 Migration Mapping

### Current → Recommended

| Current Location | Recommended Location | Notes |
|------------------|---------------------|-------|
| `app/` | `bob_agent/` | Rename for clarity and consistency |
| `app/agent.py` | `bob_agent/agent.py` | No change in functionality |
| `app/a2a_tools.py` | `bob_agent/a2a_manager.py` | Rename for clarity (A2A management) |
| `app/templates.py` | `bob_agent/prompts/system.md` | Extract to markdown for readability |
| `app/iam1_config.py` | `bob_agent/prompts/iam1_config.md` | Extract business rules to markdown |
| `app/retrievers.py` | `bob_agent/retrievers.py` | No change |
| `app/sub_agents.py` | `bob_agent/prompts/sub_agent_prompts.md` | Extract prompts, keep logic in agent.py |
| `slack-webhook/` | `slack_webhook/` | Rename (Python package naming convention) |
| `claudes-docs/` | `000-docs/` | Adopt Document Filing System v2.0 |
| *(new)* | `main.py` | Create FastAPI server with ADK + A2A endpoints |
| *(new)* | `.env.sample` | Document required environment variables |
| *(new)* | `scripts/run_local.sh` | Local development script |
| *(new)* | `scripts/smoke_test.sh` | Quick health check script |

---

## 📋 Key Files Breakdown

### Root Level Files

#### `main.py` - FastAPI Server
**Purpose:** Provides REST API endpoints for agent queries, A2A protocol, and health checks.

**Contents:**
```python
from fastapi import FastAPI, HTTPException
from bob_agent.agent import create_agent
from bob_agent.a2a_manager import AgentCardManager
import uvicorn

app = FastAPI(title="Bob's Brain - Vertex AI Agent Engine")

# Health check
@app.get("/_health")
def health_check():
    return {"status": "ok", "service": "bob-vertex-agent"}

# Agent query endpoint
@app.post("/query")
async def query_agent(query: str):
    agent = create_agent()
    response = agent.run(query)
    return {"response": response}

# A2A Protocol endpoints
@app.get("/.well-known/agent-card")
def get_agent_card():
    manager = AgentCardManager()
    return manager.get_agent_card()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

#### `.env.sample` - Environment Variables Template
**Purpose:** Documents all required environment variables for local development and deployment.

**Contents:**
```bash
# GCP Project Configuration
PROJECT_ID=bobs-brain
LOCATION=us-central1

# Agent Engine Configuration
AGENT_ENGINE_ID=projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448

# A2A Protocol Configuration
PUBLIC_URL=https://bob-vertex-agent-eow2wytafa-uc.a.run.app
PORT=8080

# Observability
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

#### `Makefile` - Development Commands
**Purpose:** Standardized development commands for local testing, deployment, and CI/CD.

**Contents:**
```makefile
.PHONY: dev test deploy-agent deploy-run smoke-test

dev:
	@echo "Starting local development server..."
	./scripts/run_local.sh

test:
	@echo "Running test suite..."
	uv run pytest tests/unit tests/integration -v

deploy-agent:
	@echo "Deploying to Agent Engine..."
	./scripts/deploy_agent_engine.sh

deploy-run:
	@echo "Deploying to Cloud Run..."
	./scripts/deploy_cloud_run.sh

smoke-test:
	@echo "Running smoke tests..."
	./scripts/smoke_test.sh
```

---

## 📂 Module Organization

### `bob_agent/` - Main Agent Module

#### `agent.py` - Core Agent
**Responsibilities:**
- Initialize LlmAgent with Gemini 2.5 Flash
- Wire VertexAiSessionService and VertexAiMemoryBankService
- Register tools (retrieve_docs, route_to_agent, coordinate_with_peer_iam1)
- Define agent routing logic

#### `a2a_manager.py` - A2A Protocol Management
**Responsibilities:**
- Serve AgentCard at `/.well-known/agent-card`
- Handle A2A skill discovery
- Coordinate with peer IAM1 agents
- Manage JSON-RPC 2.0 communication

#### `tools.py` - Custom Tools
**Responsibilities:**
- Implement custom tool functions (e.g., get_current_time_tool)
- Tool wrappers for complex operations
- Tool configuration and registration

#### `retrievers.py` - RAG Pipeline
**Responsibilities:**
- Vertex AI Search datastore queries
- text-embedding-005 embeddings
- Vertex AI Rank re-ranking
- Top-K document retrieval

#### `prompts/` - Prompt Templates
**Purpose:** Keep prompts in markdown for readability and version control.

**Files:**
- `system.md` - Root agent system prompt
- `iam1_config.md` - IAM1 business rules and configuration
- `sub_agent_prompts.md` - IAM2 specialist prompts

---

## 🧪 Testing Structure

### `tests/unit/` - Unit Tests
**Focus:** Individual functions and modules in isolation.

**Examples:**
- `test_agent.py` - Agent initialization, tool registration
- `test_tools.py` - Tool function correctness
- `test_retrievers.py` - RAG retrieval logic

### `tests/integration/` - Integration Tests
**Focus:** Component interactions and external services.

**Examples:**
- `test_a2a_protocol.py` - A2A discovery and coordination
- `test_agent_engine.py` - Agent Engine REST API calls
- `test_slack_webhook.py` - Slack event handling

### `tests/load_test/` - Load Testing
**Focus:** Performance and scalability validation.

**Tools:** Locust, custom load testing scripts

---

## 🚀 Scripts Directory

### `scripts/run_local.sh`
**Purpose:** Start FastAPI development server with live reload.

```bash
#!/bin/bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### `scripts/smoke_test.sh`
**Purpose:** Quick health check after deployment.

```bash
#!/bin/bash
BASE_URL="${1:-http://localhost:8080}"

echo "Testing health endpoint..."
curl -f "$BASE_URL/_health" || exit 1

echo "Testing A2A AgentCard..."
curl -f "$BASE_URL/.well-known/agent-card" || exit 1

echo "✅ Smoke tests passed!"
```

### `scripts/deploy_agent_engine.sh`
**Purpose:** Deploy agent to Vertex AI Agent Engine.

```bash
#!/bin/bash
set -e

PROJECT_ID="${PROJECT_ID:-bobs-brain}"
REGION="${REGION:-us-central1}"

echo "Exporting dependencies..."
uv export --no-hashes --no-dev -o requirements.txt

echo "Deploying to Agent Engine..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/bob-agent

echo "Updating Agent Engine..."
# (Vertex AI Agent Engine deployment commands)

echo "✅ Deployment complete!"
```

### `scripts/deploy_cloud_run.sh`
**Purpose:** Deploy FastAPI server to Cloud Run (optional frontend).

```bash
#!/bin/bash
set -e

PROJECT_ID="${PROJECT_ID:-bobs-brain}"
REGION="${REGION:-us-central1}"

echo "Deploying to Cloud Run..."
gcloud run deploy bob-vertex-agent \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=$PROJECT_ID

echo "✅ Cloud Run deployment complete!"
```

---

## 📖 Documentation Standards

### 000-docs/ Structure
**All documentation follows Document Filing System v2.0:**

**Format:** `NNN-CC-ABCD-description.md`

**Categories (CC):**
- **PP** = Product & Planning
- **AT** = Architecture & Technical
- **TQ** = Testing & Quality
- **OD** = Operations & Deployment
- **LS** = Logs & Status
- **RA** = Reports & Analysis
- **DR** = Documentation & Reference
- **MC** = Meetings & Communication
- **PM** = Project Management

**Document Types (ABCD):**
- **SCAF** = Scaffold/Structure
- **ARCH** = Architecture
- **QREF** = Quick Reference
- **PLAN** = Planning Document
- **SPEC** = Specification
- **GUID** = Guide/Tutorial

**Examples:**
- `001-AT-SCAF-production-agent-structure.md` - This file
- `002-DR-QREF-api-reference.md` - API endpoint reference
- `003-PP-PLAN-deployment-strategy.md` - Deployment planning
- `004-AT-ARCH-system-design.md` - System architecture
- `005-TQ-SPEC-testing-strategy.md` - Testing specification

---

## 🔧 Configuration Files

### `.env.sample`
**Required variables for local development:**
```bash
# GCP Project
PROJECT_ID=bobs-brain
LOCATION=us-central1

# Agent Engine
AGENT_ENGINE_ID=projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448

# A2A Protocol
PUBLIC_URL=https://bob-vertex-agent-eow2wytafa-uc.a.run.app
PORT=8080

# Observability
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true

# Slack (optional)
# SLACK_BOT_TOKEN=xoxb-... (stored in Secret Manager)
# SLACK_SIGNING_SECRET=... (stored in Secret Manager)
```

### `.gitignore`
**Exclude sensitive files:**
```
.env
*.pyc
__pycache__/
.pytest_cache/
.venv/
venv/
*.egg-info/
dist/
build/
.DS_Store
deployment_metadata.json
*.log
```

### `.dockerignore`
**Exclude unnecessary files from Docker builds:**
```
.git/
.github/
tests/
notebooks/
claudes-docs/
000-docs/
*.md
.env
.pytest_cache/
__pycache__/
*.pyc
```

---

## 🎯 Key Benefits

### 1. **Separation of Concerns**
- **Code:** `bob_agent/` module
- **Prompts:** `bob_agent/prompts/` (markdown)
- **Tests:** `tests/` directory
- **Infrastructure:** `deployment/` directory
- **Documentation:** `000-docs/` and `claudes-docs/`

### 2. **Developer Experience**
- **Quick start:** `make dev` to run locally
- **Quick test:** `make test` to run test suite
- **Quick deploy:** `make deploy-agent` to deploy to Agent Engine
- **Quick verify:** `make smoke-test` to verify deployment

### 3. **Maintainability**
- **Markdown prompts:** Easy to read, diff, and version control
- **Flat structure:** No deep nesting, easy navigation
- **Clear naming:** File names indicate purpose
- **Documentation co-located:** 000-docs/ in project root

### 4. **CI/CD Friendly**
- **Makefile targets:** Standardized commands for CI pipelines
- **Scripts:** Reusable deployment scripts
- **Environment variables:** Explicit configuration via .env.sample
- **GitHub Actions:** Pre-configured workflows

---

## 📚 Next Steps

### Phase 1: Documentation Migration (Immediate)
1. ✅ Create `000-docs/` directory
2. ✅ Create this scaffold document (`001-AT-SCAF-production-agent-structure.md`)
3. Move high-value docs from `claudes-docs/` to `000-docs/` with proper naming

### Phase 2: Code Reorganization (Optional)
1. Rename `app/` → `bob_agent/`
2. Extract prompts to `bob_agent/prompts/*.md`
3. Rename `slack-webhook/` → `slack_webhook/`
4. Create `main.py` FastAPI server (optional, if not using Cloud Functions)

### Phase 3: Developer Experience (Optional)
1. Create `scripts/run_local.sh`, `scripts/smoke_test.sh`
2. Expand Makefile with additional targets
3. Create `.env.sample` with all required variables
4. Add `.dockerignore` for optimized builds

### Phase 4: Testing Expansion (Optional)
1. Reorganize tests into `unit/`, `integration/`, `load_test/`
2. Add A2A protocol tests
3. Add Slack webhook integration tests
4. Add load testing with Locust

---

## 🔍 Reference Implementation

**This scaffold is based on:**
- Google ADK best practices
- Vertex AI Agent Engine deployment patterns
- A2A Protocol specification
- FastAPI production conventions
- Google Cloud deployment standards

**Inspired by:**
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- [Google ADK Documentation](https://github.com/google/adk-python)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

---

**Last Updated:** 2025-11-10
**Version:** 1.0
**Status:** Reference Implementation
**Applies To:** Bob's Brain (Vertex AI Agent Engine)
