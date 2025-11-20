# Deployment Runbook: Bob's Brain to Vertex AI Agent Engine

**Date:** 2025-11-19
**Project:** Bob's Brain (bobs-brain)
**Purpose:** Step-by-step operational guide for deploying Bob's Brain to Vertex AI Agent Engine
**Status:** Production-ready

---

## Prerequisites

Before starting deployment, verify:

- [ ] **GCP Project Access** - You have Owner or Editor role on `bobs-brain-dev`
- [ ] **gcloud CLI** - Installed and configured (`gcloud --version`)
- [ ] **Terraform** - Installed (`terraform --version >= 1.6.0`)
- [ ] **GitHub Access** - Admin access to `jeremylongshore/bobs-brain` repository
- [ ] **ADK CLI** - Python 3.12+ available locally (for local testing)

**Verify gcloud auth:**
```bash
gcloud auth list
gcloud config get-value project
# Should show: bobs-brain-dev
```

---

## Deployment Phases

| Phase | Description | Duration | Risk |
|-------|-------------|----------|------|
| 1. Infrastructure Setup | Create staging bucket, verify Terraform state | 15 min | Low |
| 2. GitHub Secrets Configuration | Set up WIF and secrets | 20 min | Low |
| 3. Local Verification | Test agent locally before deploying | 10 min | Low |
| 4. Agent Engine Deployment | Deploy via GitHub Actions | 20 min | Medium |
| 5. Gateway Deployment | Deploy A2A + Slack gateways | 15 min | Medium |
| 6. Telemetry Verification | Verify Cloud Trace, logs, metrics | 10 min | Low |
| 7. Smoke Testing | End-to-end functionality test | 15 min | Medium |
| **Total** | | **~2 hours** | |

---

## Phase 1: Infrastructure Setup (15 min)

### Step 1.1: Navigate to Project

```bash
cd /home/jeremy/000-projects/iams/bobs-brain/
git status
# Ensure you're on main branch and up to date
git pull origin main
```

### Step 1.2: Verify Terraform State

```bash
cd infra/terraform/envs/dev

# Initialize Terraform (if not already done)
terraform init

# Verify current state
terraform show
```

**Expected:** Should show existing resources (service accounts, IAM bindings, etc.)

### Step 1.3: Apply Infrastructure Changes

**IMPORTANT:** This creates the staging bucket required by ADK CLI.

```bash
# Plan changes
terraform plan -var-file="dev.tfvars" -out=tfplan

# Review plan output
# Should show:
# - google_storage_bucket.adk_staging (CREATE)
# - google_storage_bucket_iam_member.adk_staging_admin (CREATE)
# - Outputs: staging_bucket_url, staging_bucket_name

# Apply changes
terraform apply tfplan

# Verify staging bucket created
terraform output staging_bucket_url
# Expected: gs://bobs-brain-dev-adk-staging
```

### Step 1.4: Verify Staging Bucket

```bash
# List bucket
gsutil ls gs://bobs-brain-dev-adk-staging

# Check IAM permissions
gsutil iam get gs://bobs-brain-dev-adk-staging

# Should show agent-engine service account with roles/storage.admin
```

**Checkpoint:**
- ✅ Terraform apply succeeded
- ✅ Staging bucket created: `gs://bobs-brain-dev-adk-staging`
- ✅ IAM permissions configured for agent-engine service account

---

## Phase 2: GitHub Secrets Configuration (20 min)

### Step 2.1: Get Required Values

**WIF Provider:**
```bash
gcloud iam workload-identity-pools providers describe github-oidc \
  --project=bobs-brain-dev \
  --location=global \
  --workload-identity-pool=github-actions \
  --format="value(name)"
```

**Example output:**
```
projects/123456789/locations/global/workloadIdentityPools/github-actions/providers/github-oidc
```

**WIF Service Account:**
```bash
gcloud iam service-accounts list \
  --project=bobs-brain-dev \
  --filter="displayName:GitHub Actions" \
  --format="value(email)"
```

**Example output:**
```
github-actions@bobs-brain-dev.iam.gserviceaccount.com
```

**Project ID:**
```bash
gcloud config get-value project
# Expected: bobs-brain-dev
```

**Staging Bucket URL:**
```bash
terraform output -state=infra/terraform/envs/dev/terraform.tfstate staging_bucket_url
# Expected: gs://bobs-brain-dev-adk-staging
```

### Step 2.2: Configure GitHub Secrets

**Navigate to:**
```
https://github.com/jeremylongshore/bobs-brain/settings/secrets/actions
```

**Click:** "New repository secret"

**Add these secrets:**

| Secret Name | Value |
|-------------|-------|
| `WIF_PROVIDER` | `projects/123.../workloadIdentityPools/github-actions/providers/github-oidc` |
| `WIF_SERVICE_ACCOUNT` | `github-actions@bobs-brain-dev.iam.gserviceaccount.com` |
| `PROJECT_ID` | `bobs-brain-dev` |
| `REGION` | `us-central1` |
| `STAGING_BUCKET` | `gs://bobs-brain-dev-adk-staging` |

**IMPORTANT:** If WIF is not set up yet, follow the complete setup guide in `000-docs/6767-068-OD-CONF-github-secrets-configuration.md`.

**Checkpoint:**
- ✅ All 5 secrets configured in GitHub
- ✅ WIF provider and service account verified
- ✅ No secret values visible in plain text (GitHub masks them)

---

## Phase 3: Local Verification (10 min)

### Step 3.1: Set Up Local Environment

```bash
cd /home/jeremy/000-projects/iams/bobs-brain/

# Create .env file (NEVER commit this)
cp .env.example .env

# Edit .env with real values
nano .env
```

**Required values:**
```bash
PROJECT_ID=bobs-brain-dev
LOCATION=us-central1
AGENT_ENGINE_ID=  # Leave empty for now (will be populated after deployment)
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0
APP_NAME=bobs-brain
APP_VERSION=0.6.0
PUBLIC_URL=  # Leave empty for now
```

### Step 3.2: Install Dependencies

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify ADK installation
pip show google-adk
# Should show version >= 0.1.0
```

### Step 3.3: Test Agent Import

```bash
# Test that agent code imports successfully
python3 -c "
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from my_agent.agent import get_agent, create_runner
from my_agent.agent_engine_app import app
print('✅ All imports successful')
print(f'Runner type: {type(app)}')
"
```

**Expected output:**
```
✅ All imports successful
Runner type: <class 'google.adk.runner.Runner'>
```

### Step 3.4: Run Tests

```bash
# Run unit tests
pytest tests/unit/ -v

# Expected: All tests pass
```

**Checkpoint:**
- ✅ Dependencies installed
- ✅ Agent code imports successfully
- ✅ `agent_engine_app.py` exports `app` variable (Runner instance)
- ✅ Unit tests pass

---

## Phase 4: Agent Engine Deployment (20 min)

### Step 4.1: Trigger GitHub Actions Workflow

**Option A: Push to main (automatic deployment)**
```bash
# From local machine
git push origin main
```

**Option B: Manual workflow dispatch**
1. Go to: https://github.com/jeremylongshore/bobs-brain/actions/workflows/deploy-agent-engine.yml
2. Click "Run workflow"
3. Select branch: `main`
4. Select environment: `dev`
5. Click "Run workflow"

### Step 4.2: Monitor Workflow

**Watch workflow progress:**
```
https://github.com/jeremylongshore/bobs-brain/actions
```

**Expected steps:**
1. ✅ Checkout code
2. ✅ Set up Python 3.12
3. ✅ Install ADK CLI
4. ✅ Authenticate to GCP (WIF)
5. ✅ Set up Cloud SDK
6. ✅ Verify authentication
7. ✅ Deploy to Agent Engine (20-30 seconds)
8. ✅ Verify deployment
9. ✅ Get Agent Engine ID

**Deployment command executed:**
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

### Step 4.3: Capture Agent Engine ID

**From workflow output:**
Look for output like:
```
Fetching Agent Engine ID...
NAME: projects/123456789/locations/us-central1/reasoningEngines/987654321
DISPLAY_NAME: bobs-brain-dev
CREATE_TIME: 2025-11-19T12:34:56Z
UPDATE_TIME: 2025-11-19T12:34:56Z
```

**Extract Agent Engine ID:**
```
987654321
```

**OR get it manually:**
```bash
gcloud ai reasoning-engines list \
  --project=bobs-brain-dev \
  --region=us-central1 \
  --filter="displayName:bobs-brain-dev" \
  --format="value(name)" | awk -F'/' '{print $NF}'
```

### Step 4.4: Update Environment Variables

**Update Terraform tfvars:**
```bash
cd infra/terraform/envs/dev
nano dev.tfvars

# Add/update:
agent_engine_id = "987654321"  # Use actual ID from Step 4.3
```

**Update local .env:**
```bash
cd /home/jeremy/000-projects/iams/bobs-brain/
nano .env

# Update:
AGENT_ENGINE_ID=987654321
```

**Checkpoint:**
- ✅ GitHub Actions workflow completed successfully
- ✅ Agent Engine deployed (name: `bobs-brain-dev`)
- ✅ Agent Engine ID captured
- ✅ Environment variables updated with AGENT_ENGINE_ID

---

## Phase 5: Gateway Deployment (15 min)

### Step 5.1: Apply Terraform for Gateways

```bash
cd infra/terraform/envs/dev

# Plan gateway deployment
terraform plan -var-file="dev.tfvars" -out=tfplan

# Should show:
# - google_cloud_run_service.a2a_gateway (CREATE)
# - google_cloud_run_service.slack_webhook (CREATE)
# - google_cloud_run_service_iam_member (CREATE for public access)

# Apply
terraform apply tfplan
```

### Step 5.2: Get Gateway URLs

```bash
# A2A Gateway URL
terraform output a2a_gateway_url
# Example: https://bobs-brain-a2a-gateway-abc123-uc.a.run.app

# Slack Webhook URL
terraform output slack_webhook_url
# Example: https://bobs-brain-slack-webhook-xyz789-uc.a.run.app
```

### Step 5.3: Test A2A Gateway

```bash
# Test /card endpoint
curl https://bobs-brain-a2a-gateway-abc123-uc.a.run.app/card | jq

# Expected: AgentCard JSON with SPIFFE ID
```

**Example response:**
```json
{
  "name": "bobs-brain",
  "description": "Bob's Brain AI Assistant (SPIFFE: spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0)",
  "url": "https://bobs-brain-a2a-gateway-abc123-uc.a.run.app",
  "skills": [
    {"name": "general_assistance", "description": "Answer questions, provide help"}
  ]
}
```

### Step 5.4: Test Agent Invocation

```bash
# Test /invoke endpoint
curl -X POST https://bobs-brain-a2a-gateway-abc123-uc.a.run.app/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ADK?",
    "session_id": "test-deploy-verification"
  }' | jq
```

**Expected:** Response with agent's answer about ADK.

**Checkpoint:**
- ✅ A2A Gateway deployed and accessible
- ✅ Slack Webhook deployed (if configured)
- ✅ `/card` endpoint returns valid AgentCard
- ✅ `/invoke` endpoint returns agent responses

---

## Phase 6: Telemetry Verification (10 min)

### Step 6.1: Check Cloud Trace

**Open Cloud Trace:**
```
https://console.cloud.google.com/traces/list?project=bobs-brain-dev
```

**What to look for:**
- Recent traces (within last 5 minutes)
- Trace structure shows: Gateway → Agent Engine → LlmAgent → Memory operations
- No error spans (red indicators)

**Filter by SPIFFE ID:**
```
resource.labels.spiffe_id="spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0"
```

### Step 6.2: Check Cloud Logging

**Open Cloud Logging:**
```
https://console.cloud.google.com/logs/query?project=bobs-brain-dev
```

**Query for agent logs:**
```
resource.type="aiplatform.googleapis.com/AgentEngine"
jsonPayload.app_name="bobs-brain"
timestamp >= "2025-11-19T12:00:00Z"
```

**What to look for:**
- "Creating Runner for Agent Engine deployment" log
- "Agent invocation started" logs
- "Successfully saved session to Memory Bank" logs
- SPIFFE ID in every log entry

### Step 6.3: Check Cloud Monitoring

**Open Cloud Monitoring:**
```
https://console.cloud.google.com/monitoring?project=bobs-brain-dev
```

**Verify metrics:**
- Navigate to: **Metrics Explorer**
- Search for: `aiplatform.googleapis.com/reasoning_engine/request_count`
- Filter by: `agent_engine_id = "987654321"`
- Time range: Last 1 hour

**Expected:** Chart shows at least 1-2 requests (from testing)

### Step 6.4: Check Error Reporting

**Open Error Reporting:**
```
https://console.cloud.google.com/errors?project=bobs-brain-dev
```

**Expected:** No error groups OR only expected startup warnings (ignore)

**Checkpoint:**
- ✅ Cloud Trace shows recent traces with full span hierarchy
- ✅ Cloud Logging shows agent invocation logs with SPIFFE ID
- ✅ Cloud Monitoring shows request_count metric > 0
- ✅ Error Reporting shows no critical errors

---

## Phase 7: Smoke Testing (15 min)

### Step 7.1: End-to-End A2A Test

**Test full agent invocation:**
```bash
# Question 1: Simple query
curl -X POST https://bobs-brain-a2a-gateway-abc123-uc.a.run.app/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is your name?",
    "session_id": "smoke-test-1"
  }' | jq -r '.response'

# Expected: "I am Bob's Brain, an AI assistant..."

# Question 2: Context retention (same session)
curl -X POST https://bobs-brain-a2a-gateway-abc123-uc.a.run.app/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I just ask you?",
    "session_id": "smoke-test-1"
  }' | jq -r '.response'

# Expected: Should reference the previous question about name
```

### Step 7.2: Verify Memory Persistence

**Check Memory Bank auto-save:**
```bash
# Open Cloud Logging
https://console.cloud.google.com/logs/query?project=bobs-brain-dev&query=jsonPayload.message:"saved session to Memory Bank"

# Should show logs like:
# "Successfully saved session to Memory Bank"
# with session_id "smoke-test-1"
```

### Step 7.3: Load Test (Optional)

**Send 10 concurrent requests:**
```bash
for i in {1..10}; do
  curl -X POST https://bobs-brain-a2a-gateway-abc123-uc.a.run.app/invoke \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Test request $i\", \"session_id\": \"load-test-$i\"}" &
done
wait

# Check Cloud Monitoring after 2 minutes
# Verify request_count increased by 10
```

### Step 7.4: Slack Integration Test (Optional)

**If Slack webhook configured:**

1. Go to Slack workspace
2. Invite bot to a channel: `/invite @bobs-brain`
3. Send message: `@bobs-brain What is ADK?`
4. **Expected:** Bot responds within 5 seconds

**Verify in Cloud Logging:**
```
resource.type="cloud_run_revision"
resource.labels.service_name="bobs-brain-slack-webhook"
jsonPayload.event_type="message"
```

**Checkpoint:**
- ✅ Agent responds to queries correctly
- ✅ Context retained across turns (same session_id)
- ✅ Memory Bank auto-save working (logs confirm)
- ✅ Concurrent requests handled successfully
- ✅ (Optional) Slack bot responding

---

## Post-Deployment Checklist

Before considering deployment complete:

- [ ] **Agent Engine deployed** and visible in Vertex AI console
- [ ] **A2A Gateway accessible** at public URL
- [ ] **AgentCard endpoint** returns valid JSON with SPIFFE ID
- [ ] **Agent invocation working** (responds to queries)
- [ ] **Cloud Trace enabled** (traces visible within 2 minutes)
- [ ] **Cloud Logging working** (logs show SPIFFE ID)
- [ ] **Cloud Monitoring metrics** (request_count > 0)
- [ ] **Memory Bank auto-save** (logs confirm sessions saved)
- [ ] **Context retention** (multi-turn conversations work)
- [ ] **Error Reporting clean** (no critical errors)
- [ ] **GitHub Secrets configured** (all 5 secrets present)
- [ ] **Terraform state updated** (agent_engine_id in tfvars)
- [ ] **Documentation updated** (CHANGELOG.md, README.md)

---

## Rollback Procedure (If Deployment Fails)

### Step 1: Identify Failure Point

**Check GitHub Actions logs:**
```
https://github.com/jeremylongshore/bobs-brain/actions
```

**Common failure points:**
- WIF authentication failure → Check GitHub Secrets
- ADK deploy timeout → Check staging bucket permissions
- Agent Engine API error → Check IAM permissions

### Step 2: Rollback Agent Engine (If Needed)

**List Agent Engine deployments:**
```bash
gcloud ai reasoning-engines list \
  --project=bobs-brain-dev \
  --region=us-central1 \
  --format="table(name,displayName,createTime,updateTime)"
```

**Delete failed deployment:**
```bash
gcloud ai reasoning-engines delete AGENT_ENGINE_ID \
  --project=bobs-brain-dev \
  --region=us-central1
```

### Step 3: Rollback Gateways (If Needed)

**Delete Cloud Run services:**
```bash
cd infra/terraform/envs/dev

# Target specific resource for deletion
terraform destroy -target=google_cloud_run_service.a2a_gateway
terraform destroy -target=google_cloud_run_service.slack_webhook
```

### Step 4: Fix Issue and Retry

1. Review error logs
2. Fix configuration (GitHub Secrets, Terraform, code)
3. Commit fix to main branch
4. Retry deployment (GitHub Actions triggers automatically)

---

## Monitoring & Maintenance

### Daily Checks

- **Cloud Monitoring Dashboard** - Check request count, error rate, latency
- **Error Reporting** - Review any new error groups
- **Cloud Logging** - Spot check for unusual patterns

### Weekly Maintenance

- **Review telemetry data** - Optimize based on performance metrics
- **Update dependencies** - Check for ADK, google-adk-sdk updates
- **Review Memory Bank size** - Ensure not growing unbounded
- **Check staging bucket** - Verify lifecycle policy cleaning old artifacts

### Monthly Operations

- **Performance review** - Compare to baseline metrics
- **Cost analysis** - Review Agent Engine, gateway, storage costs
- **Security audit** - Review IAM permissions, WIF configuration
- **Documentation update** - Keep runbooks current with changes

---

## Troubleshooting

### Issue: "Agent Engine not found"

**Symptom:** Gateway returns 404 or "Agent Engine ID not found"

**Solution:**
1. Verify AGENT_ENGINE_ID in .env and tfvars
2. Check Agent Engine exists:
   ```bash
   gcloud ai reasoning-engines describe $AGENT_ENGINE_ID \
     --project=bobs-brain-dev \
     --region=us-central1
   ```
3. If missing, redeploy Agent Engine (Phase 4)

### Issue: "No traces in Cloud Trace"

**Symptom:** Cloud Trace shows no data after deployment

**Solution:**
1. Verify `--trace_to_cloud` flag in workflow (should be present)
2. Wait 5 minutes (traces have slight delay)
3. Check Agent Engine tracing config:
   ```bash
   gcloud ai reasoning-engines describe $AGENT_ENGINE_ID \
     --format="value(traceConfig)"
   ```
   Should show tracing enabled

### Issue: "Memory Bank auto-save failing"

**Symptom:** Logs show "Failed to save session to Memory Bank"

**Solution:**
1. Check service account permissions:
   ```bash
   gcloud projects get-iam-policy bobs-brain-dev \
     --flatten="bindings[].members" \
     --filter="bindings.members:serviceAccount:agent-engine@bobs-brain-dev.iam.gserviceaccount.com"
   ```
   Should include `roles/aiplatform.user`

2. If missing, add permission:
   ```bash
   gcloud projects add-iam-policy-binding bobs-brain-dev \
     --member="serviceAccount:agent-engine@bobs-brain-dev.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   ```

### Issue: "WIF authentication failed in GitHub Actions"

**Symptom:** Workflow fails at "Authenticate to GCP" step

**Solution:**
1. Verify all 5 GitHub Secrets are configured
2. Check WIF provider exists:
   ```bash
   gcloud iam workload-identity-pools providers describe github-oidc \
     --project=bobs-brain-dev \
     --location=global \
     --workload-identity-pool=github-actions
   ```
3. If missing, follow WIF setup guide: `000-docs/6767-068-OD-CONF-github-secrets-configuration.md`

---

## References

- **Deployment Plan:** `000-docs/6767-067-PM-PLAN-vertex-ai-deployment-plan.md`
- **GitHub Secrets Setup:** `000-docs/6767-068-OD-CONF-github-secrets-configuration.md`
- **Observability Guide:** `000-docs/6767-069-OD-TELE-observability-telemetry-guide.md`
- **ADK CLI Reference:** `000-docs/google-reference/adk/GOOGLE_ADK_CLI_REFERENCE.md`
- **Hard Mode Rules:** `000-docs/6767-001-PP-ARCH-hard-mode-baseline.md`

---

**Document Status:** Complete ✅
**Last Updated:** 2025-11-19
**Category:** Operations & Deployment - Runbook

**Next Steps:**
1. Execute this runbook to deploy Bob's Brain
2. Monitor telemetry for 24 hours
3. Iterate based on observed performance
4. Update runbook with any lessons learned

---
