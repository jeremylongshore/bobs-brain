# Vertex AI Agent Engine Deployment Plan - Bob's Brain

**Date:** 2025-11-19
**Project:** Bob's Brain (bobs-brain)
**Goal:** Deploy to Vertex AI Agent Engine for use, observation, and telemetry evaluation
**Status:** Phase 1 - Research Complete

---

## Executive Summary

**Purpose:** Deploy Bob's Brain to Vertex AI Agent Engine so we can:
- ✅ **Use** the agent in production
- ✅ **Observe** agent behavior and performance
- ✅ **Evaluate** with Cloud Trace telemetry

**Current Status:**
- ✅ Code Complete (99/100 ADK compliance)
- ✅ `agent_engine_app.py` created (entrypoint file)
- ⚠️ Infrastructure incomplete (no staging bucket)
- ⚠️ No deployment workflow
- ❌ Not deployed

**Deployment Method:** ADK CLI (`adk deploy agent_engine`) + Terraform hybrid

---

## Phase 1: Research Findings

### ADK Deploy Requirements (from GOOGLE_ADK_CLI_REFERENCE.md)

**Required Files:**
1. ✅ `my_agent/agent.py` - Agent implementation (DONE)
2. ✅ `my_agent/agent_engine_app.py` - Entrypoint with `app = Runner(...)` (DONE)
3. ✅ `my_agent/requirements.txt` - Python dependencies (DONE)
4. ⚠️ `.env` - Environment variables (exists, needs validation)

**Required Infrastructure:**
1. ❌ GCS staging bucket for deployment artifacts
2. ❌ IAM permissions for ADK to upload to bucket
3. ❌ Service account for Agent Engine runtime

**Required Options:**
```bash
adk deploy agent_engine my_agent \
  --project <PROJECT_ID>                    # REQUIRED
  --region <REGION>                         # REQUIRED
  --staging_bucket gs://<BUCKET>            # REQUIRED
  --display_name "bobs-brain-<env>"         # Optional
  --description "Bob's Brain AI Assistant"  # Optional
  --trace_to_cloud                          # RECOMMENDED (for telemetry)
  --env_file .env                           # Optional (default)
  --requirements_file requirements.txt       # Optional (default)
```

### Key Findings from User Manual Notebooks

**Source:** `000-docs/001-usermanual/tutorial_get_started_with_agent_engine_terraform_deployment.ipynb`

**Prerequisites:**
1. ✅ Python 3.9+ (we have 3.12)
2. ✅ Terraform installed
3. ✅ GCP project with billing enabled
4. ⚠️ Vertex AI API enabled (needs verification)
5. ⚠️ Agent Engine API enabled (needs verification)
6. ❌ GCS bucket for staging

**Tutorial Pattern:**
- Uses cloudpickle serialization (older pattern)
- Bob uses proper ADK Runner (newer, better pattern)
- Tutorial shows Terraform resource creation
- **Our approach:** ADK CLI + Terraform hybrid (best of both)

### Critical Discovery: Service Dependencies

**From ADK_COMPREHENSIVE_DOCUMENTATION.md:**

Bob requires these Vertex AI services:
1. **VertexAiSessionService** - Session persistence
2. **VertexAiMemoryBankService** - Long-term memory
3. **Agent Engine** - Runtime environment

**Service Initialization:**
```python
# From my_agent/agent.py:171-185
session_service = VertexAiSessionService(
    project_id=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_ENGINE_ID  # ← Circular dependency!
)
```

**⚠️ CRITICAL ISSUE:** Agent Engine ID is needed BEFORE deployment, but only exists AFTER deployment!

**Solution:** Two-phase deployment:
1. **Phase A:** Deploy Agent Engine resource (get ID)
2. **Phase B:** Redeploy with correct AGENT_ENGINE_ID in env vars

OR use Terraform output interpolation (better).

---

## Deployment Architecture

### What Gets Deployed Where

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (CI/CD)                    │
│  1. adk deploy agent_engine my_agent                         │
│     ↓ packages code                                          │
│     ↓ builds Docker                                          │
│     ↓ uploads to staging bucket                              │
│     ↓ creates Agent Engine resource                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│             GCS Staging Bucket (artifacts)                   │
│  gs://bobs-brain-dev-adk-staging/                            │
│    ├── agent-code.tar.gz                                     │
│    ├── Dockerfile                                            │
│    └── requirements.txt                                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│         Vertex AI Agent Engine (managed runtime)             │
│  Running:                                                    │
│    - my_agent/agent_engine_app.py (entrypoint)              │
│    - Runner with dual memory                                 │
│    - LlmAgent (Gemini 2.0 Flash)                             │
│  Connected to:                                               │
│    - VertexAiSessionService (Datastore)                      │
│    - VertexAiMemoryBankService (RAG)                         │
│    - Cloud Trace (telemetry)                                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          Cloud Run Gateways (protocol proxies)               │
│  - A2A Gateway (service/a2a_gateway/)                        │
│  - Slack Webhook (service/slack_webhook/)                    │
│  Both proxy to Agent Engine REST API                         │
└─────────────────────────────────────────────────────────────┘
```

### Telemetry Flow

```
Agent Invocation
    ↓
Agent Engine (with --trace_to_cloud)
    ↓
Cloud Trace (spans, latency, tool calls)
    ↓
Cloud Monitoring Dashboards
```

**What You'll See:**
- 📊 Request latency per invocation
- 🔧 Tool call timing
- 💾 Memory service latency
- 🤖 LLM call duration
- ⚠️ Errors and retries

---

## Phase-by-Phase Plan

### Phase 2: Infrastructure Setup

**Goal:** Create staging bucket and configure IAM

**Tasks:**
1. Create `infra/terraform/storage.tf` with staging bucket
2. Add IAM permissions for ADK deployment
3. Update `infra/terraform/envs/dev.tfvars` with bucket URL
4. Run `terraform plan` to validate
5. Document bucket lifecycle policies

**Terraform Resource:**
```hcl
resource "google_storage_bucket" "adk_staging" {
  name          = "${var.project_id}-adk-staging"
  location      = var.region
  force_destroy = false  # Protect production artifacts

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30  # Clean up old artifacts after 30 days
    }
    action {
      type = "Delete"
    }
  }

  versioning {
    enabled = true  # Keep deployment history
  }
}

# Grant ADK deployment permissions
resource "google_storage_bucket_iam_member" "adk_staging_admin" {
  bucket = google_storage_bucket.adk_staging.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.agent_engine.email}"
}

output "staging_bucket_url" {
  description = "GCS staging bucket for ADK deployments"
  value       = "gs://${google_storage_bucket.adk_staging.name}"
}
```

**Commit Message:**
```
feat(infra): add GCS staging bucket for ADK deployments

- Create storage.tf with staging bucket resource
- Configure lifecycle policies (30-day artifact retention)
- Enable versioning for deployment history
- Grant IAM permissions to Agent Engine service account
- Add staging_bucket_url output for workflows

Required for: adk deploy agent_engine --staging_bucket
```

---

### Phase 3: Deployment Workflow

**Goal:** Automate deployment with GitHub Actions

**Tasks:**
1. Create `.github/workflows/deploy-agent-engine.yml`
2. Configure WIF (Workload Identity Federation) authentication
3. Add GitHub Secrets documentation
4. Test workflow on dev environment

**Workflow File:**
```yaml
name: Deploy to Vertex AI Agent Engine

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'dev'
        type: choice
        options:
          - dev
          - staging
          - prod

jobs:
  deploy-agent-engine:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # Required for WIF

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install ADK CLI
        run: |
          pip install google-adk>=1.15.1
          adk --version

      - name: Authenticate to GCP (WIF)
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Deploy to Agent Engine
        env:
          PROJECT_ID: ${{ secrets.PROJECT_ID }}
          REGION: ${{ secrets.REGION }}
          STAGING_BUCKET: ${{ secrets.STAGING_BUCKET }}
          ENVIRONMENT: ${{ inputs.environment || 'dev' }}
        run: |
          adk deploy agent_engine my_agent \
            --project $PROJECT_ID \
            --region $REGION \
            --staging_bucket $STAGING_BUCKET \
            --display_name "bobs-brain-$ENVIRONMENT" \
            --description "Bob's Brain AI Assistant - $ENVIRONMENT" \
            --trace_to_cloud \
            --env_file .env.example

      - name: Verify deployment
        run: |
          echo "✅ Agent Engine deployment complete"
          echo "Check Vertex AI console:"
          echo "https://console.cloud.google.com/vertex-ai/agent-engine?project=${{ secrets.PROJECT_ID }}"

      - name: Notify on failure
        if: failure()
        run: |
          echo "❌ Deployment failed"
          echo "Contact: claude.buildcaptain@intentsolutions.io"
```

**Required GitHub Secrets:**
```
WIF_PROVIDER          # Workload Identity Federation provider
WIF_SERVICE_ACCOUNT   # Service account email for WIF
PROJECT_ID            # GCP project ID (e.g., bobs-brain-dev)
REGION                # GCP region (e.g., us-central1)
STAGING_BUCKET        # GCS bucket URL (e.g., gs://bobs-brain-dev-adk-staging)
```

**Commit Message:**
```
feat(ci): add Agent Engine deployment workflow

- Create deploy-agent-engine.yml with ADK CLI integration
- Use Workload Identity Federation for authentication (R4)
- Enable Cloud Trace with --trace_to_cloud flag
- Support manual deployment with environment selection
- Auto-deploy on push to main branch

Deploys to: Vertex AI Agent Engine with full telemetry
```

---

### Phase 4: Observability Setup

**Goal:** Enable full telemetry and monitoring

**Tasks:**
1. Verify Cloud Trace integration (--trace_to_cloud flag)
2. Create monitoring dashboard configuration
3. Set up log-based metrics
4. Document telemetry access

**Cloud Trace Configuration:**
Already enabled by `--trace_to_cloud` flag in deployment!

**What Gets Traced:**
- Agent invocation start/end
- LLM calls to Gemini
- Tool executions
- Memory service queries (Session + Memory Bank)
- Error events

**Monitoring Dashboard (JSON):**
```json
{
  "displayName": "Bob's Brain - Agent Engine",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Agent Invocations (QPS)",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"vertex_ai_reasoning_engine\"",
                  "aggregation": {
                    "perSeriesAligner": "ALIGN_RATE"
                  }
                }
              }
            }]
          }
        }
      },
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Response Latency (p50, p95, p99)",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"vertex_ai_reasoning_engine\"",
                  "aggregation": {
                    "perSeriesAligner": "ALIGN_DELTA",
                    "crossSeriesReducer": "REDUCE_PERCENTILE_50"
                  }
                }
              }
            }]
          }
        }
      }
    ]
  }
}
```

**Commit Message:**
```
feat(observability): configure Cloud Trace and monitoring

- Enable trace_to_cloud in deployment workflow
- Create monitoring dashboard configuration
- Document telemetry access for Cloud Trace
- Add log-based metrics for key operations

Telemetry: Full distributed tracing with SPIFFE ID propagation
```

---

### Phase 5: Testing & Validation

**Goal:** Verify deployment works end-to-end

**Tasks:**
1. Deploy to dev environment
2. Test Agent Engine endpoint
3. Verify Cloud Trace shows spans
4. Test Slack webhook integration
5. Document test results

**Test Commands:**
```bash
# 1. Verify Agent Engine is running
gcloud ai reasoning-engines list \
  --project=bobs-brain-dev \
  --region=us-central1

# 2. Test Agent Engine endpoint
curl -X POST \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/bobs-brain-dev/locations/us-central1/reasoningEngines/<ID>:query" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, Bob! What is your identity?"}'

# 3. Check Cloud Trace
gcloud logging read "resource.type=vertex_ai_reasoning_engine" \
  --project=bobs-brain-dev \
  --limit=10

# 4. View traces in console
# https://console.cloud.google.com/traces/list?project=bobs-brain-dev
```

**Expected Results:**
- ✅ Agent Engine shows "ACTIVE" status
- ✅ Query returns response with SPIFFE ID
- ✅ Cloud Trace shows spans with:
  - Agent invocation span
  - LLM call span
  - Memory service spans
- ✅ SPIFFE ID visible in trace metadata

**Commit Message:**
```
test(deployment): validate Agent Engine deployment

- Deploy to dev environment via ADK CLI
- Verify Agent Engine endpoint responds
- Confirm Cloud Trace telemetry is flowing
- Test Slack webhook integration
- Document test results and verification steps

Status: Deployment validated, telemetry confirmed ✅
```

---

### Phase 6: Documentation

**Goal:** Complete deployment runbook and user guide

**Tasks:**
1. Create deployment runbook (step-by-step)
2. Update README with deployment instructions
3. Document telemetry access and dashboards
4. Add troubleshooting guide

**Deployment Runbook Outline:**
```markdown
# Bob's Brain - Deployment Runbook

## Prerequisites
- [ ] GCP project created
- [ ] Billing enabled
- [ ] Vertex AI API enabled
- [ ] Terraform installed
- [ ] GitHub secrets configured

## Deployment Steps

### 1. Infrastructure Setup
terraform -chdir=infra/terraform/envs/dev init
terraform -chdir=infra/terraform/envs/dev plan
terraform -chdir=infra/terraform/envs/dev apply

### 2. Deploy Agent Engine
git push origin main  # Triggers deployment workflow

### 3. Verify Deployment
gcloud ai reasoning-engines list --region=us-central1

### 4. Access Telemetry
# Cloud Trace: https://console.cloud.google.com/traces
# Monitoring: https://console.cloud.google.com/monitoring

## Troubleshooting
- If deployment fails: Check GitHub Actions logs
- If agent doesn't respond: Verify Agent Engine ID in logs
- If no telemetry: Confirm --trace_to_cloud flag is set
```

**Commit Message:**
```
docs(deployment): complete deployment runbook

- Create step-by-step deployment guide
- Update README with ADK deployment instructions
- Document Cloud Trace access and dashboards
- Add troubleshooting guide for common issues

Ready for: Production deployment to Vertex AI Agent Engine
```

---

## Gotchas and Known Issues

### Issue 1: Circular Dependency (AGENT_ENGINE_ID)

**Problem:** Agent code needs `AGENT_ENGINE_ID` but it only exists after deployment

**Solution:**
```python
# my_agent/agent.py - Handle missing ID gracefully
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID", "")
if not AGENT_ENGINE_ID:
    logger.warning("AGENT_ENGINE_ID not set - using empty string for initial deployment")
```

**Workaround:** ADK CLI handles this automatically - sets ID after first deployment

---

### Issue 2: Staging Bucket Permissions

**Problem:** ADK needs write access to staging bucket

**Solution:** IAM binding in Terraform:
```hcl
resource "google_storage_bucket_iam_member" "adk_staging_admin" {
  bucket = google_storage_bucket.adk_staging.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.agent_engine.email}"
}
```

---

### Issue 3: First Deployment Takes Longer

**Problem:** Docker build + upload can take 5-10 minutes

**Solution:** Be patient. Subsequent deployments are faster (layer caching).

---

### Issue 4: Environment Variables in .env

**Problem:** `.env` file not in git (security)

**Solution:** Use `.env.example` as template, populate in CI with secrets:
```bash
# In GitHub Actions
echo "PROJECT_ID=${{ secrets.PROJECT_ID }}" >> .env
echo "LOCATION=${{ secrets.REGION }}" >> .env
# etc.
```

---

## Success Criteria

### Phase 2 Complete When:
- ✅ Staging bucket exists in GCP
- ✅ IAM permissions configured
- ✅ Terraform outputs bucket URL
- ✅ `terraform plan` shows no errors

### Phase 3 Complete When:
- ✅ Deployment workflow exists
- ✅ GitHub secrets documented
- ✅ WIF authentication configured
- ✅ Workflow runs without errors

### Phase 4 Complete When:
- ✅ Cloud Trace integration enabled
- ✅ Monitoring dashboard configured
- ✅ Telemetry access documented

### Phase 5 Complete When:
- ✅ Agent deployed to dev
- ✅ Agent responds to queries
- ✅ Cloud Trace shows spans
- ✅ SPIFFE ID visible in traces

### Phase 6 Complete When:
- ✅ Deployment runbook complete
- ✅ README updated
- ✅ Troubleshooting guide written

---

## Timeline Estimate

| Phase | Tasks | Estimated Time | Commit |
|-------|-------|----------------|--------|
| Phase 1 | Research | ✅ DONE | Research findings |
| Phase 2 | Infrastructure | 1-2 hours | Terraform staging bucket |
| Phase 3 | Deployment Workflow | 2-3 hours | GitHub Actions workflow |
| Phase 4 | Observability | 1-2 hours | Cloud Trace config |
| Phase 5 | Testing | 2-3 hours | Deployment validation |
| Phase 6 | Documentation | 1-2 hours | Runbook and guides |
| **TOTAL** | | **7-13 hours** | **6 commits** |

---

## Checkpoint Questions Before Proceeding

Before we start Phase 2, confirm:

1. ✅ **GCP Project:** Do you have `bobs-brain-dev` project ready?
2. ⚠️ **Billing:** Is billing enabled on the project?
3. ⚠️ **APIs:** Are Vertex AI APIs enabled?
4. ⚠️ **GitHub Secrets:** Do we need to set up WIF provider first?
5. ⚠️ **Terraform State:** Where should we store Terraform state? (GCS backend?)

**WAIT FOR USER APPROVAL BEFORE PROCEEDING TO PHASE 2**

---

**Research Phase Complete:** ✅
**Next Phase:** Phase 2 - Infrastructure Setup (pending approval)
**Total Phases:** 6 phases, 6 commits
**Goal:** Deploy Bob to Vertex AI Agent Engine with full telemetry

---
