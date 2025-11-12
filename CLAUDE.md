# CLAUDE.md - Build Captain: ADK + Agent Engine Hard Mode

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role

**Build Captain for jeremylongshore/bobs-brain**

## Repository Overview

**Bob's Brain** - Production Slack AI assistant powered by Google ADK and Vertex AI Agent Engine

**Location:** `/home/jeremy/000-projects/iams/bobs-brain/`
**Status:** Production (Hard Mode - CI-only, ADK+Agent Engine enforced)
**Version:** See VERSION file
**Repository:** https://github.com/jeremylongshore/bobs-brain (public)

**Built from Template:** [iam1-intent-agent-model-vertex-ai](https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai)
- The template repository provides the Hard Mode architecture (R1-R8)
- Bob's Brain is a specific implementation for Slack integration
- Template is the source for new agent projects

---

## HARD RULES (Non-Negotiable)

These rules are ENFORCED in CI. Any violation will fail the build.

### R1: Agent Implementation

**Requirement:** All agents MUST be implemented using `google-adk` (Agent Development Kit).

**Prohibited:**
- ❌ LangChain agents
- ❌ CrewAI agents
- ❌ AutoGen agents
- ❌ Custom agent frameworks
- ❌ Flask/FastAPI agents with direct LLM calls

**Required:** Agent code in `my_agent/agent.py` using `LlmAgent` from `google.adk.agents`.

### R2: Deployed Runtime

**Requirement:** The deployed runtime MUST be Vertex AI Agent Engine.

**Prohibited:**
- ❌ Self-hosted ADK runners
- ❌ Cloud Run with embedded Runner
- ❌ Cloud Functions with embedded Runner
- ❌ Local execution (except CI smoke tests)

**Required:** Container image deployed to Vertex AI Agent Engine via CI.

### R3: Cloud Run Gateway Rules

**Requirement:** Cloud Run is allowed ONLY as a thin protocol gateway.

**Allowed:** HTTP/A2A/Slack webhook endpoints that proxy to Agent Engine via REST API.

**Prohibited:**
- ❌ Importing `google.adk.serving`
- ❌ Constructing or running an ADK `Runner`
- ❌ Direct LLM calls
- ❌ Agent logic in gateway code

**Required:** Gateways in `service/` must call Agent Engine's `:query` endpoint via REST.

### R4: CI-Only Deployments

**Requirement:** ALL deployments MUST go through GitHub Actions with Workload Identity Federation.

**Prohibited:**
- ❌ Manual `gcloud run deploy`
- ❌ Manual `gcloud functions deploy`
- ❌ Local deployment scripts
- ❌ Service account key files
- ❌ `application_default_credentials.json`

**Required:** Deploy via `.github/workflows/deploy.yml` with WIF authentication.

### R5: Dual Memory Wiring

**Requirement:** Agent MUST use both Session Cache and Memory Bank.

**Required in `my_agent/agent.py`:**
```python
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

def create_runner():
    session_service = VertexAiSessionService(
        project_id=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )

    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )

    agent = get_agent()  # LlmAgent with after_agent_callback

    return Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )

def auto_save_session_to_memory(ctx):
    """Callback to persist session to Memory Bank"""
    try:
        ctx._invocation_context.memory_service.add_session_to_memory(
            ctx._invocation_context.session
        )
    except Exception as e:
        logging.error(f"Failed to save session to memory: {e}")
```

### R6: Documentation Structure

**Requirement:** Single documentation folder at root: `000-docs/`

**Prohibited:**
- ❌ Multiple doc folders (`docs/`, `documentation/`, etc.)
- ❌ Nested docs in subdirectories
- ❌ Unnumbered doc files

**Required:** All docs in `000-docs/NNN-CC-ABCD-description.md` format.

### R7: SPIFFE ID Immutability

**Requirement:** Every agent deployment MUST have an immutable SPIFFE ID.

**Format:**
```
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/<env>/<region>/<version>
```

**Examples:**
- `spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/v1.2.3`
- `spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/v0.0.1-dev`

**Required:**
- Environment variable in Agent Engine container
- Environment variable in Cloud Run gateways
- Included in AgentCard description
- Propagated in `x-spiffe-id` response headers
- Logged in structured logs
- Tagged in OpenTelemetry spans

### R8: CI Drift Detection

**Requirement:** CI MUST scan for and block framework drift.

**Prohibited Patterns (CI will fail):**
```python
# ❌ FastAPI serving (gateway only, no Runner)
from google.adk.serving.fastapi

# ❌ Alternative frameworks
from langchain
import langchain
from crewai
import autogen

# ❌ Local credentials
application_default_credentials.json
~/.config/gcloud

# ❌ Manual deployment
gcloud run deploy  # (except in CI)
gcloud functions deploy  # (except in CI)
```

**Required:** `scripts/ci/check_nodrift.sh` runs in CI before tests.

---

## Canonical Structure

```
bobs-brain/
├── .github/              # GitHub Actions workflows, templates
├── 000-docs/             # Documentation (NNN-CC-ABCD-*.md)
├── adk/                  # ADK agent configurations
├── my_agent/             # Agent implementation (ADK only)
│   ├── __init__.py
│   ├── agent.py          # LlmAgent + dual memory wiring
│   ├── a2a_card.py       # AgentCard for A2A protocol
│   └── tools/            # Custom tools
├── service/              # HTTP/A2A/Slack gateways (proxy only)
│   ├── a2a_gateway/      # A2A protocol endpoints
│   │   └── main.py       # FastAPI app (no Runner)
│   └── slack_webhook/    # Slack integration
│       └── main.py       # Slack event handler (no Runner)
├── infra/                # Terraform IaC
│   ├── terraform/
│   │   ├── modules/      # Reusable TF modules
│   │   └── envs/         # Environment configs (dev, prod)
│   └── scripts/          # Infrastructure helpers
├── scripts/              # Helper scripts
│   ├── ci/               # CI-specific scripts
│   │   └── check_nodrift.sh
│   └── deploy/           # Deployment automation
├── tests/                # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── 99-Archive/           # Archived implementations
├── requirements.txt      # Python dependencies
├── Dockerfile            # Agent container image
├── VERSION               # Semantic version (X.Y.Z)
├── CHANGELOG.md          # Version history
├── CLAUDE.md             # This file
├── LICENSE               # MIT License
└── README.md             # Project overview
```

**Enforcement:** If ANY other root-level directory exists, it MUST be archived to `99-Archive/<YYYY-MM-DD>/`.

---

## Agent Core (my_agent/)

### my_agent/agent.py

**Purpose:** Define the LlmAgent with tools, instructions, and memory callbacks.

**Required:**
```python
from google.adk.agents import LlmAgent
from google.adk.runner import Runner
from google.adk.memory import VertexAiSessionService, VertexAiMemoryBankService
import os
import logging

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")
APP_NAME = os.getenv("APP_NAME", "bobs-brain")
AGENT_SPIFFE_ID = os.getenv("AGENT_SPIFFE_ID")

def auto_save_session_to_memory(ctx):
    """After-agent callback to persist session to Memory Bank"""
    try:
        if hasattr(ctx, '_invocation_context'):
            memory_svc = ctx._invocation_context.memory_service
            session = ctx._invocation_context.session
            if memory_svc and session:
                memory_svc.add_session_to_memory(session)
                logging.info(f"Saved session {session.id} to Memory Bank")
    except Exception as e:
        logging.error(f"Failed to save session: {e}")
        # Never block agent execution

def get_agent() -> LlmAgent:
    """Create and configure the LlmAgent"""
    return LlmAgent(
        model="gemini-1.5-pro-001",
        tools=[],  # Add custom tools here
        instruction="You are Bob, a helpful AI assistant.",
        after_agent_callback=auto_save_session_to_memory
    )

def create_runner() -> Runner:
    """Create Runner with dual memory wiring (Session + Memory Bank)"""
    session_service = VertexAiSessionService(
        project_id=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )

    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )

    agent = get_agent()

    return Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )
```

**Prohibited:**
- ❌ No `from google.adk.serving` imports
- ❌ No Flask/FastAPI routes in this file
- ❌ No direct LLM API calls

### my_agent/a2a_card.py

**Purpose:** Minimal AgentCard for A2A protocol discovery.

**Required:**
```python
from google.adk.a2a import AgentCard
import os

APP_NAME = os.getenv("APP_NAME", "bobs-brain")
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
PUBLIC_URL = os.getenv("PUBLIC_URL", "https://example.com")
AGENT_SPIFFE_ID = os.getenv("AGENT_SPIFFE_ID", "spiffe://intent.solutions/agent/bobs-brain/unknown/unknown/unknown")

def get_agent_card() -> AgentCard:
    return AgentCard(
        name=APP_NAME,
        description=f"Bob's Brain AI Assistant (SPIFFE: {AGENT_SPIFFE_ID})",
        url=PUBLIC_URL,
        version=APP_VERSION,
        skills=[]  # Define available skills
    )
```

---

## Gateways (service/)

### Purpose

Thin HTTP/A2A/Slack proxies that call Agent Engine via REST. **NO ADK Runner imports allowed.**

### service/a2a_gateway/main.py

**Allowed:**
```python
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import httpx
import os
import logging

app = FastAPI()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
AGENT_ENGINE_NAME = os.getenv("AGENT_ENGINE_NAME")
AGENT_SPIFFE_ID = os.getenv("AGENT_SPIFFE_ID")

@app.get("/card")
async def get_card():
    """Return AgentCard JSON"""
    # Return static AgentCard (no Runner import)
    return {
        "name": "bobs-brain",
        "description": f"SPIFFE: {AGENT_SPIFFE_ID}",
        "url": os.getenv("PUBLIC_URL"),
        "version": os.getenv("APP_VERSION"),
        "skills": []
    }

class InvokeRequest(BaseModel):
    user_id: str
    session_id: str
    text: str

@app.post("/invoke")
async def invoke_agent(req: InvokeRequest):
    """Proxy to Agent Engine :query endpoint"""
    # Get OAuth token
    token = get_gcp_token()  # Use google.auth

    # Call Agent Engine REST API
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/{AGENT_ENGINE_NAME}:query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "user_id": req.user_id,
        "session_id": req.session_id,
        "text": req.text
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        response.raise_for_status()

    return {
        "response": response.json(),
        "headers": {"x-spiffe-id": AGENT_SPIFFE_ID}
    }
```

**Prohibited:**
```python
# ❌ NEVER import these in gateway code:
from google.adk.runner import Runner
from google.adk.serving import *
from my_agent.agent import create_runner

# ❌ NEVER construct or run an ADK Runner here
runner = Runner(...)
runner.run(...)
```

### service/slack_webhook/main.py

**Purpose:** Slack event handler that proxies to Agent Engine.

**Required Pattern:**
1. Verify Slack signature
2. Return 200 immediately (within 3s)
3. Call Agent Engine `:query` endpoint via REST (background task)
4. Post response back to Slack

**No Runner imports. Only REST API calls to Agent Engine.**

---

## Terraform (infra/)

### Purpose

Infrastructure as Code for all GCP resources. **No `terraform apply` in CI by default** (only `validate`).

### infra/terraform/envs/dev/main.tf

**Required APIs:**
```hcl
locals {
  required_apis = [
    "aiplatform.googleapis.com",
    "run.googleapis.com",
    "cloudfunctions.googleapis.com",
    "artifactregistry.googleapis.com",
    "secretmanager.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "cloudtrace.googleapis.com"
  ]
}

resource "google_project_service" "apis" {
  for_each = toset(local.required_apis)
  service  = each.value
  disable_on_destroy = false
}
```

**Required Service Accounts:**
```hcl
# CI/CD service account
resource "google_service_account" "github_actions" {
  account_id   = "github-actions"
  display_name = "GitHub Actions CI/CD"
}

resource "google_project_iam_member" "github_actions_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/run.admin",
    "roles/artifactregistry.writer",
    "roles/secretmanager.secretAccessor",
    "roles/iam.serviceAccountUser"
  ])
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

# Runtime service account
resource "google_service_account" "app" {
  account_id   = "bobs-brain-app"
  display_name = "Bob's Brain Runtime"
}
```

**Cloud Run Gateway Module:**
```hcl
module "a2a_gateway" {
  source = "../../modules/cloud_run"

  service_name = "bobs-brain-a2a"
  image        = var.gateway_image

  env_vars = {
    PROJECT_ID            = var.project_id
    LOCATION              = var.region
    AGENT_ENGINE_NAME     = var.agent_engine_name
    AGENT_SPIFFE_ID       = var.agent_spiffe_id
    APP_VERSION           = var.app_version
    PUBLIC_URL            = var.public_url
  }

  service_account = google_service_account.app.email
}
```

**Agent Engine Bootstrap (CI-guarded):**
- `null_resource` that calls CI script to upsert Agent Engine
- Only runs when `TF_VAR_allow_agent_engine_bootstrap=true` (set in CI only)

---

## CI/CD (GitHub Actions)

### .github/workflows/ci.yml

**Purpose:** Continuous Integration - run on every PR and push.

**Required Steps:**
1. Install dependencies
2. **Drift check:** Run `scripts/ci/check_nodrift.sh` (fail if violations found)
3. Run unit tests
4. Start ADK `api_server` for smoke test (CI only)
5. Terraform validate

**Example:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Drift check
        run: bash scripts/ci/check_nodrift.sh

      - name: Run tests
        run: pytest tests/

      - name: ADK smoke test (CI only)
        run: |
          # Start api_server in background
          python -m google.adk.serving.api_server &
          sleep 5
          curl http://localhost:8080/health
          kill %1

      - name: Terraform validate
        run: |
          cd infra/terraform/envs/dev
          terraform init -backend=false
          terraform validate
```

### .github/workflows/deploy.yml

**Purpose:** Continuous Deployment - deploy to GCP via WIF.

**Required:**
1. Authenticate with WIF (no service account keys)
2. Build agent container image
3. Push to Artifact Registry
4. Upsert Agent Engine deployment (Python script using Vertex AI SDK)
5. Deploy Cloud Run gateway
6. Deploy Slack webhook (if enabled)
7. **On failure:** Email Claude at `claude.buildcaptain@intentsolutions.io`

**Example:**
```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Build agent image
        run: |
          VERSION=$(cat VERSION)
          gcloud builds submit --tag gcr.io/${{ secrets.PROJECT_ID }}/bobs-brain-agent:$VERSION

      - name: Deploy to Agent Engine
        run: |
          python scripts/deploy/upsert_agent_engine.py \
            --project-id=${{ secrets.PROJECT_ID }} \
            --location=us-central1 \
            --image=gcr.io/${{ secrets.PROJECT_ID }}/bobs-brain-agent:$VERSION

      - name: Deploy Cloud Run gateway
        run: |
          gcloud run deploy bobs-brain-a2a \
            --image=gcr.io/${{ secrets.PROJECT_ID }}/bobs-brain-a2a-gateway:latest \
            --region=us-central1 \
            --allow-unauthenticated \
            --set-env-vars=AGENT_ENGINE_NAME=${{ secrets.AGENT_ENGINE_NAME }},AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/$(cat VERSION)

      - name: Notify Claude on failure
        if: failure()
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.BUILD_ALERT_EMAIL }}
          password: ${{ secrets.BUILD_ALERT_PASSWORD }}
          subject: "❌ Deploy failed: bobs-brain @ ${{ github.sha }}"
          to: claude.buildcaptain@intentsolutions.io
          from: "CI Bot <noreply@intentsolutions.io>"
          body: "Check logs: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

### scripts/ci/check_nodrift.sh

**Purpose:** Detect and block framework drift.

**Required:**
```bash
#!/bin/bash
set -e

echo "🔍 Scanning for framework drift violations..."

VIOLATIONS=0

# Check for forbidden imports
if grep -r "from google\.adk\.serving\.fastapi" service/ 2>/dev/null; then
  echo "❌ VIOLATION: FastAPI serving found in service/ (R3)"
  VIOLATIONS=$((VIOLATIONS + 1))
fi

if grep -r "from langchain\|import langchain\|from crewai\|import autogen" . --exclude-dir=.venv --exclude-dir=99-Archive 2>/dev/null; then
  echo "❌ VIOLATION: Alternative framework imports found (R1)"
  VIOLATIONS=$((VIOLATIONS + 1))
fi

# Check for local credentials
if find . -name "application_default_credentials.json" -o -path "*/.config/gcloud" | grep -v ".venv\|99-Archive"; then
  echo "❌ VIOLATION: Local GCP credentials found (R4)"
  VIOLATIONS=$((VIOLATIONS + 1))
fi

# Check for manual deployment commands (outside CI)
if [ "${GITHUB_ACTIONS:-false}" != "true" ]; then
  if grep -r "gcloud run deploy\|gcloud functions deploy" scripts/ --exclude="scripts/ci/*" 2>/dev/null; then
    echo "❌ VIOLATION: Manual deployment commands in scripts/ (R4)"
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
fi

if [ $VIOLATIONS -gt 0 ]; then
  echo "❌ Found $VIOLATIONS drift violations. Build failed."
  exit 1
fi

echo "✅ No drift violations detected"
exit 0
```

---

## SPIFFE ID Propagation

### Environment Variables

**Required in all environments:**
```bash
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/<env>/<region>/<version>
```

**Examples:**
- Production: `spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/v1.2.3`
- Development: `spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/v0.0.1-dev`

### AgentCard

**Required in `my_agent/a2a_card.py`:**
```python
description=f"Bob's Brain AI Assistant (SPIFFE: {AGENT_SPIFFE_ID})"
```

### HTTP Headers

**Required in all gateway responses:**
```python
response.headers["x-spiffe-id"] = AGENT_SPIFFE_ID
```

### Structured Logs

**Required in all log messages:**
```python
logging.info("Agent invoked", extra={"spiffe_id": AGENT_SPIFFE_ID})
```

### OpenTelemetry

**Required as resource attribute:**
```python
from opentelemetry.sdk.resources import Resource

resource = Resource.create({
    "service.name": APP_NAME,
    "service.version": APP_VERSION,
    "spiffe.id": AGENT_SPIFFE_ID
})
```

---

## Acceptance Checklist

Before merging any PR, verify:

- [ ] Root structure matches canonical tree (only 8 directories)
- [ ] `service/` proxies to Agent Engine (no Runner imports)
- [ ] `my_agent/` wires Session + Memory Bank + after-save callback
- [ ] CI passes: tests + drift scan + terraform validate
- [ ] Deploy workflow pushes container and upserts Agent Engine (CI only)
- [ ] Cloud Run gateway deployed via CI (not manual)
- [ ] SPIFFE ID visible in AgentCard, headers, logs
- [ ] Drift scan passes (`scripts/ci/check_nodrift.sh`)
- [ ] Latest `000-docs/NNN-*` AAR added
- [ ] No other docs folder exists (only `000-docs/`)
- [ ] `CHANGELOG.md` updated
- [ ] `VERSION` bumped (if applicable)

---

## Troubleshooting

### "ImportError: cannot import Runner in service/"

**Cause:** Violates R3 (Cloud Run as proxy only).

**Fix:** Remove all `google.adk.runner` imports from `service/`. Use REST API calls to Agent Engine instead.

### "CI failed: Drift violations detected"

**Cause:** Violates R1 or R3 (forbidden imports found).

**Fix:** Remove forbidden imports. Check `scripts/ci/check_nodrift.sh` output for details.

### "Deploy failed: Agent Engine not found"

**Cause:** Agent Engine hasn't been bootstrapped yet.

**Fix:**
1. Run Terraform with `TF_VAR_allow_agent_engine_bootstrap=true` ONCE (CI only)
2. Verify Agent Engine exists in Vertex AI console

### "Slack events timing out"

**Cause:** Gateway not returning 200 within 3 seconds.

**Fix:** Return 200 immediately, then call Agent Engine in background task.

---

## Quick Commands

```bash
# Run CI checks locally
bash scripts/ci/check_nodrift.sh
pytest tests/

# Validate Terraform
cd infra/terraform/envs/dev
terraform init -backend=false
terraform validate

# Build agent container (CI does this)
VERSION=$(cat VERSION)
docker build -t gcr.io/bobs-brain/bobs-brain-agent:$VERSION .

# Test gateway locally (not for production)
cd service/a2a_gateway
uvicorn main:app --reload
```

---

## References

- **Google ADK Docs:** https://cloud.google.com/vertex-ai/docs/agent-development-kit
- **Vertex AI Agent Engine:** https://cloud.google.com/vertex-ai/docs/agent-engine
- **A2A Protocol:** https://github.com/google/adk-python/blob/main/docs/a2a.md
- **SPIFFE Spec:** https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE.md
- **Workload Identity Federation:** https://cloud.google.com/iam/docs/workload-identity-federation

---

**Last Updated:** 2025-11-11
**Enforcement:** CI (`scripts/ci/check_nodrift.sh`)
**Contact:** claude.buildcaptain@intentsolutions.io (CI alerts only)
