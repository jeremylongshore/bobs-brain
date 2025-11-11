# Structure Migration Plan

**Last Updated:** 2025-11-10
**Category:** Project Management
**Type:** Migration Plan
**Status:** In Progress

---

## Overview

Migrate bob-vertex-agent from current ad-hoc structure to production-ready scaffold defined in `001-AT-SCAF-production-agent-structure.md`.

**Goal:** Clean, maintainable structure matching FastAPI + ADK + A2A best practices.

---

## Current State vs. Target State

### Current Structure
```
bob-vertex-agent/
├─ app/                        # Agent code
│  ├─ agent.py
│  ├─ a2a_tools.py
│  ├─ retrievers.py
│  ├─ templates.py             # Prompts in Python
│  └─ sub_agents.py
├─ slack-webhook/              # Cloud Functions (kebab-case)
├─ deployment/terraform/
├─ tests/                      # Flat test directory
├─ knowledge-base/
└─ 000-docs/
```

### Target Structure
```
bob-vertex-agent/
├─ main.py                     # FastAPI server (NEW)
├─ .env.sample                 # Environment template (NEW)
├─ Dockerfile                  # Container config (NEW)
│
├─ bob_agent/                  # Renamed from app/
│  ├─ agent.py
│  ├─ a2a_manager.py           # Renamed from a2a_tools.py
│  ├─ tools.py
│  ├─ retrievers.py
│  ├─ prompts/                 # NEW - Extract from templates.py
│  │  ├─ system.md
│  │  ├─ iam1_config.md
│  │  └─ sub_agent_prompts.md
│  └─ resources/               # NEW
│     ├─ examples/
│     │  └─ a2a_examples.json
│     └─ schemas/
│        └─ agent_card.json
│
├─ slack_webhook/              # Renamed from slack-webhook/
├─ scripts/                    # NEW
│  ├─ run_local.sh
│  ├─ smoke_test.sh
│  ├─ deploy_agent_engine.sh
│  └─ deploy_cloud_run.sh
│
├─ tests/                      # Reorganized
│  ├─ unit/
│  ├─ integration/
│  └─ load_test/
│
├─ deployment/terraform/
├─ knowledge-base/
└─ 000-docs/
```

---

## Migration Phases

### Phase 1: Create New Files (Non-Breaking) ✅
**Status:** Ready to execute
**Risk:** Low - creates new files alongside existing ones

Tasks:
1. ✅ Create `main.py` (FastAPI server)
2. ✅ Create `.env.sample` (environment template)
3. ✅ Create `Dockerfile`
4. ✅ Create `scripts/` directory with 4 scripts
5. ✅ Create `bob_agent/prompts/` directory
6. ✅ Create `bob_agent/resources/` directory

### Phase 2: Extract Prompts to Markdown (Non-Breaking) ✅
**Status:** Ready to execute
**Risk:** Low - doesn't change existing code

Tasks:
1. ✅ Extract prompts from `app/templates.py` → `bob_agent/prompts/system.md`
2. ✅ Extract config from `app/iam1_config.py` → `bob_agent/prompts/iam1_config.md`
3. ✅ Extract sub-agent prompts from `app/sub_agents.py` → `bob_agent/prompts/sub_agent_prompts.md`
4. ✅ Create `bob_agent/resources/schemas/agent_card.json`
5. Keep original files for backwards compatibility

### Phase 3: Reorganize Tests (Non-Breaking) 🔄
**Status:** Ready to execute
**Risk:** Low - creates new structure alongside existing

Tasks:
1. Create `tests/unit/`, `tests/integration/`, `tests/load_test/`
2. Move existing tests to appropriate subdirectories
3. Keep originals until verified

### Phase 4: Rename Directories (Breaking - Do Last) ⚠️
**Status:** Deferred until Phases 1-3 complete
**Risk:** Medium - changes import paths

Tasks:
1. Rename `app/` → `bob_agent/`
2. Rename `slack-webhook/` → `slack_webhook/`
3. Rename `app/a2a_tools.py` → `bob_agent/a2a_manager.py`
4. Update all imports
5. Update deployment scripts
6. Update CI/CD workflows

---

## Phase 1 Implementation: Create New Files

### Task 1.1: Create main.py (FastAPI Server)

**File:** `bob-vertex-agent/main.py`

```python
"""
Bob's Brain - FastAPI Server
Provides REST API endpoints for agent queries, A2A protocol, and health checks.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
import os

# Will import from bob_agent/ after Phase 4 migration
# from bob_agent.agent import create_agent
# from bob_agent.a2a_manager import AgentCardManager

app = FastAPI(
    title="Bob's Brain - Vertex AI Agent Engine",
    description="Production AI assistant with Google ADK + Slack integration",
    version="0.4.0"
)

@app.get("/_health")
def health_check():
    """Basic health check endpoint"""
    return {
        "status": "ok",
        "service": "bob-vertex-agent",
        "version": "0.4.0"
    }

@app.get("/")
def root():
    """Root endpoint with service info"""
    return {
        "name": "Bob's Brain",
        "version": "0.4.0",
        "agent_engine_id": os.getenv("AGENT_ENGINE_ID", "Not configured"),
        "endpoints": {
            "health": "/_health",
            "agent_card": "/.well-known/agent-card",
            "query": "/query (POST)"
        }
    }

@app.get("/.well-known/agent-card")
def get_agent_card():
    """
    A2A Protocol: Return agent capabilities card

    After Phase 4 migration, this will use:
    manager = AgentCardManager()
    return manager.get_agent_card()
    """
    # Placeholder until migration complete
    return {
        "agent_name": "Bob's Brain",
        "description": "Production AI assistant with Vertex AI Agent Engine",
        "capabilities": ["conversation", "knowledge_retrieval", "slack_integration"],
        "skills": ["retrieve_docs", "route_to_agent", "coordinate_with_peer_iam1"]
    }

@app.post("/query")
async def query_agent(request: Request):
    """
    Execute agent query

    After Phase 4 migration, this will use:
    agent = create_agent()
    response = agent.run(query)
    """
    body = await request.json()
    query = body.get("query", "")

    if not query:
        raise HTTPException(status_code=400, detail="Query required")

    # Placeholder until migration complete
    return {
        "query": query,
        "response": "Migration in progress - use Agent Engine REST API directly for now",
        "agent_engine_id": os.getenv("AGENT_ENGINE_ID", "Not configured")
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Task 1.2: Create .env.sample

**File:** `bob-vertex-agent/.env.sample`

```bash
# ============================================
# Bob's Brain - Environment Configuration
# ============================================

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

# Slack Integration (optional - stored in Secret Manager)
# SLACK_BOT_TOKEN=xoxb-... (retrieve from Secret Manager)
# SLACK_SIGNING_SECRET=... (retrieve from Secret Manager)

# Development Settings
ENV=development
DEBUG=false
```

### Task 1.3: Create Dockerfile

**File:** `bob-vertex-agent/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run FastAPI server
CMD ["uv", "run", "python", "main.py"]
```

### Task 1.4: Create scripts/

**File:** `bob-vertex-agent/scripts/run_local.sh`

```bash
#!/bin/bash
# Start FastAPI development server with live reload

set -e

echo "Starting Bob's Brain development server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

**File:** `bob-vertex-agent/scripts/smoke_test.sh`

```bash
#!/bin/bash
# Quick health check after deployment

set -e

BASE_URL="${1:-http://localhost:8080}"

echo "Running smoke tests against $BASE_URL..."

echo "✓ Testing health endpoint..."
curl -f "$BASE_URL/_health" || { echo "✗ Health check failed"; exit 1; }

echo "✓ Testing A2A AgentCard..."
curl -f "$BASE_URL/.well-known/agent-card" || { echo "✗ AgentCard failed"; exit 1; }

echo "✓ Testing root endpoint..."
curl -f "$BASE_URL/" || { echo "✗ Root endpoint failed"; exit 1; }

echo ""
echo "✅ All smoke tests passed!"
```

**File:** `bob-vertex-agent/scripts/deploy_agent_engine.sh`

```bash
#!/bin/bash
# Deploy agent to Vertex AI Agent Engine

set -e

PROJECT_ID="${PROJECT_ID:-bobs-brain}"
REGION="${REGION:-us-central1}"

echo "Deploying to Vertex AI Agent Engine..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

# Use existing Makefile deployment
cd "$(dirname "$0")/.."
make deploy

echo "✅ Agent Engine deployment complete!"
```

**File:** `bob-vertex-agent/scripts/deploy_cloud_run.sh`

```bash
#!/bin/bash
# Deploy FastAPI server to Cloud Run (optional frontend)

set -e

PROJECT_ID="${PROJECT_ID:-bobs-brain}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="bob-vertex-agent"

echo "Deploying FastAPI server to Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=$PROJECT_ID \
  --project $PROJECT_ID

echo "✅ Cloud Run deployment complete!"
```

---

## Phase 2 Implementation: Extract Prompts

### Task 2.1: Extract System Prompt

**File:** `bob-vertex-agent/bob_agent/prompts/system.md`

Extract main system prompt from `app/templates.py` into markdown for readability.

### Task 2.2: Extract IAM1 Config

**File:** `bob-vertex-agent/bob_agent/prompts/iam1_config.md`

Extract business rules and configuration from `app/iam1_config.py`.

### Task 2.3: Extract Sub-Agent Prompts

**File:** `bob-vertex-agent/bob_agent/prompts/sub_agent_prompts.md`

Extract IAM2 specialist prompts from `app/sub_agents.py`.

### Task 2.4: Create Agent Card Schema

**File:** `bob-vertex-agent/bob_agent/resources/schemas/agent_card.json`

Define A2A AgentCard JSON schema.

---

## Phase 3 Implementation: Reorganize Tests

### Task 3.1: Create Test Structure

```bash
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/load_test
```

### Task 3.2: Move Existing Tests

- `test_agent_*.py` → `tests/unit/`
- `test_a2a_*.py` → `tests/integration/`
- Existing `load_test/` → `tests/load_test/`

---

## Phase 4 Implementation: Rename Directories (Deferred)

**DO NOT EXECUTE UNTIL PHASES 1-3 COMPLETE**

This phase changes import paths and requires comprehensive testing.

---

## Execution Order

1. ✅ Execute Phase 1 (create new files)
2. ✅ Execute Phase 2 (extract prompts)
3. 🔄 Execute Phase 3 (reorganize tests)
4. ⚠️ **STOP and test** - verify everything works
5. Only after successful testing → Execute Phase 4

---

## Rollback Plan

All phases are non-breaking until Phase 4:
- Phase 1-3 create NEW files alongside existing ones
- Existing code continues to work
- Easy rollback: delete new files, keep existing structure
- Phase 4 requires migration commit that can be reverted if needed

---

## Success Criteria

### Phase 1 Complete
- ✅ `main.py` runs and responds to health checks
- ✅ Scripts are executable and documented
- ✅ `.env.sample` documents all required variables
- ✅ Dockerfile builds successfully

### Phase 2 Complete
- ✅ All prompts extracted to markdown
- ✅ Prompts are readable and well-formatted
- ✅ Original files remain for backwards compatibility

### Phase 3 Complete
- ✅ Tests organized into unit/integration/load_test
- ✅ All tests still pass
- ✅ Test discovery works correctly

### Phase 4 Complete (Future)
- All imports updated
- All tests passing
- CI/CD workflows updated
- Deployment successful
- No broken references

---

**Last Updated:** 2025-11-10
**Next Action:** Execute Phase 1 - Create new files
**Status:** Ready to begin
