# First Real Agent Engine Deploy Playbook - Bob's Brain

**Document ID:** 153-NOTE-bobs-brain-first-real-agent-engine-deploy-playbook
**Type:** NOTE (Operational Playbook)
**Phase:** Phase 21
**Date:** 2025-11-23
**Purpose:** Step-by-step instructions for deploying bob to Vertex AI Agent Engine in the bobs-brain project

---

## Prerequisites Checklist

Before attempting your first real deployment, verify:

- [ ] **GCP Project**: `bobs-brain` (project number: 205354194989) exists and you have access
- [ ] **Vertex AI API**: Enabled in the project
- [ ] **WIF Configured**: Workload Identity Federation pool and provider set up for bobs-brain
- [ ] **GitHub Secrets**: Both secrets configured in repo settings:
  - `WIF_PROVIDER`: `projects/PROJECT_NUM/locations/global/workloadIdentityPools/POOL/providers/PROVIDER`
  - `WIF_SERVICE_ACCOUNT`: `SERVICE_ACCOUNT@bobs-brain.iam.gserviceaccount.com`
- [ ] **Service Account Permissions**: The WIF service account has:
  - `roles/aiplatform.user` (or `roles/aiplatform.admin`)
  - `roles/logging.logWriter`
  - `roles/storage.objectViewer` (if using staging buckets)
- [ ] **Branch**: You're working from a branch with Phase 21 changes merged

---

## Phase 1: Dry-Run Validation (Safe - No Deployment)

This phase validates your configuration without making any changes to GCP.

### Step 1: Navigate to GitHub Actions

1. Go to: https://github.com/jeremylongshore/bobs-brain/actions
2. In the left sidebar, select: **Deploy to Agent Engine (Inline Source - Dev)**
3. Click the **Run workflow** button (top right)

### Step 2: Configure Dry-Run

Configure the workflow inputs:

| Input | Value | Notes |
|-------|-------|-------|
| **agent** | `bob` | Start with bob only |
| **deploy_mode** | `dry-run` | ⚠️ SAFE - No actual deployment |
| **smoke_tests_enabled** | `false` | No agents deployed yet |

### Step 3: Run and Monitor

1. Click **Run workflow**
2. Wait for the workflow to appear in the runs list (~5-10 seconds)
3. Click on the workflow run to view details
4. Monitor the jobs:
   - ✅ **arv-checks**: Should pass (ARV, A2A, drift detection)
   - ✅ **deploy-bob**: Should show "Configuration valid (dry-run mode)"
   - ✅ **smoke-tests**: Should run in config-only mode

### Step 4: Review Output

Look for this in the `deploy-bob` job logs:

```
================================================================================
DEPLOYMENT CONFIGURATION
================================================================================
agent                     bob
environment               dev
project                   bobs-brain
region                    us-central1
agent_module              agents.bob.agent
entrypoint                agents.bob.agent::app
display_name              bobs-brain-dev
description               bobs-brain deployed to dev
dry_run                   True
================================================================================

✅ Configuration valid (dry-run mode)
   To deploy for real, remove --dry-run flag
```

### Success Criteria for Phase 1

- [ ] Workflow completed successfully
- [ ] ARV checks passed
- [ ] Deployment configuration validated
- [ ] No errors in logs

**If Phase 1 fails**: Do NOT proceed to Phase 2. Debug the configuration issues first.

---

## Phase 2: First Real Deployment (LIVE - Creates Resources)

⚠️ **WARNING**: This phase will create actual resources in GCP and may incur costs.

### Step 1: Final Pre-Flight Checks

Before triggering a real deployment:

1. **Verify WIF Authentication**:
   - Check that the dry-run workflow authenticated successfully with WIF
   - Look for this in the logs:
     ```
     Authenticate to GCP (WIF)
     ✓ Successfully authenticated with Google Cloud
     ```

2. **Verify Service Account Permissions**:
   ```bash
   # From your local machine with gcloud configured
   gcloud projects get-iam-policy bobs-brain \
     --flatten="bindings[].members" \
     --filter="bindings.members:serviceAccount:YOUR_WIF_SA@bobs-brain.iam.gserviceaccount.com"
   ```
   - Confirm it has `roles/aiplatform.user` or `roles/aiplatform.admin`

3. **Budget Alert** (Recommended):
   - Set up a budget alert in GCP Console
   - Agent Engine usage is billed per query/session
   - Dev environment should stay within free tier for basic testing

### Step 2: Trigger Real Deployment

1. Go to: https://github.com/jeremylongshore/bobs-brain/actions
2. Select: **Deploy to Agent Engine (Inline Source - Dev)**
3. Click **Run workflow**

Configure with **REAL DEPLOYMENT** settings:

| Input | Value | Notes |
|-------|-------|-------|
| **agent** | `bob` | Deploy bob only |
| **deploy_mode** | `apply` | ⚠️ REAL DEPLOYMENT |
| **smoke_tests_enabled** | `false` | Enable after first success |

### Step 3: Monitor Deployment

Watch these jobs closely:

#### 1. **arv-checks** (Must Pass)
- ARV minimum checks
- A2A readiness checks
- Drift detection
- **If this fails**: Deployment will not proceed (by design)

#### 2. **deploy-bob** (The Real Deployment)

Look for these key log messages:

```
🚀 Deploying bob to Vertex AI Agent Engine...
   Environment: dev
   Project: bobs-brain
   Region: us-central1
   Display Name: bobs-brain-dev

📦 Loading agent from agents.bob.agent...
✅ Agent loaded successfully

🔄 Creating reasoning engine on Vertex AI...
   This may take 2-3 minutes...

✅ Deployment successful!
   Resource Name: projects/205354194989/locations/us-central1/reasoningEngines/1234567890
   Engine ID: 1234567890

🔍 View in Console:
   https://console.cloud.google.com/vertex-ai/agent-engine?project=bobs-brain
```

**CRITICAL**: Save the **Resource Name** and **Engine ID** from the logs!

#### 3. **smoke-tests** (Config-Only for Now)
- Will run in config-only mode since `smoke_tests_enabled=false`
- This is expected and safe

### Step 4: Verify in GCP Console

1. **Open Agent Engine Console**:
   - https://console.cloud.google.com/vertex-ai/agent-engine?project=bobs-brain

2. **Verify Reasoning Engine**:
   - You should see a new reasoning engine with:
     - Display Name: `bobs-brain-dev`
     - Status: `Active` or `Ready`
     - Engine ID matching the deployment logs

3. **Check Cloud Trace** (Optional):
   - https://console.cloud.google.com/traces/list?project=bobs-brain
   - Should see traces from agent initialization (if tracing enabled)

### Success Criteria for Phase 2

- [ ] Deployment workflow completed successfully
- [ ] Resource Name logged in deployment output
- [ ] Reasoning engine visible in GCP console
- [ ] Engine status is "Active" or "Ready"
- [ ] No errors in deployment logs

---

## Phase 3: Enable Live Smoke Tests (Validation)

Now that bob is deployed, test it with live queries.

### Step 1: Re-Run Workflow with Smoke Tests

1. Go to: https://github.com/jeremylongshore/bobs-brain/actions
2. Select: **Deploy to Agent Engine (Inline Source - Dev)**
3. Click **Run workflow**

Configure to SKIP deployment but RUN smoke tests:

| Input | Value | Notes |
|-------|-------|-------|
| **agent** | `bob` | Test bob only |
| **deploy_mode** | `dry-run` | Don't redeploy |
| **smoke_tests_enabled** | `true` | ⚠️ Enable live tests |

**Note**: We're using `dry-run` for deployment but enabling smoke tests. The smoke tests job will detect that an agent is deployed and run live tests against it.

### Step 2: Monitor Smoke Tests

Look for the **smoke-tests** job logs:

```
================================================================================
SMOKE TEST - LIVE MODE
================================================================================
Project: bobs-brain
Region: us-central1
Environment: dev
================================================================================

🧪 Testing bob...
   Resource: projects/205354194989/locations/us-central1/reasoningEngines/1234567890
   ✅ Agent Engine connection established
   📤 Sending: '[SMOKE TEST] What is your name? (Reply briefly)...'
   📥 Response: 'I am Bob, your AI assistant...'
   ✅ bob responded successfully

================================================================================
SMOKE TEST SUMMARY
================================================================================
Total tests: 1
Passed: 1
Failed: 0

✅ All smoke tests passed!
```

### Success Criteria for Phase 3

- [ ] Smoke tests connected to deployed agent
- [ ] Agent responded to test query
- [ ] Response was non-empty and coherent
- [ ] No API errors in logs

---

## What to Do If It Fails

### Deployment Failures

**If ARV checks fail**:
- Review the specific failing check (ARV minimum, A2A readiness, or drift detection)
- Fix the issue in code
- Re-run dry-run until ARV passes

**If WIF authentication fails**:
- Verify `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` secrets exist in GitHub
- Check that the WIF provider trusts GitHub Actions
- Verify the service account exists in the bobs-brain project

**If Agent Engine API fails**:
```
❌ Deployment failed: 403 Permission denied
```
- Check service account has `roles/aiplatform.user`
- Verify Vertex AI API is enabled
- Confirm you're using the correct project ID

**If import fails**:
```
❌ Error: Cannot find 'app' or 'get_agent()' in agents.bob.agent
```
- Check that `agents/bob/agent.py` exports `root_agent` or `app`
- Verify Python import path is correct
- Review agent module structure

### Smoke Test Failures

**If connection fails**:
```
❌ Failed to connect: Resource not found
```
- Verify the reasoning engine was actually created
- Check the resource name in the deployment logs
- Confirm the engine is in "Active" status in GCP console

**If query fails**:
```
❌ Query failed: timeout
```
- Agent Engine may be initializing (wait 1-2 minutes and retry)
- Check Cloud Logging for agent errors
- Verify the agent doesn't require environment variables that aren't set

**If response is empty**:
```
❌ bob returned empty response
```
- Check Cloud Logging for agent runtime errors
- Verify the agent's prompt/instruction is valid
- Test with a different query

### Rollback Procedure

If you need to remove the deployed agent:

#### Option A: Via GCP Console (Recommended)
1. Go to: https://console.cloud.google.com/vertex-ai/agent-engine?project=bobs-brain
2. Select the reasoning engine (bobs-brain-dev)
3. Click **Delete**
4. Confirm deletion

#### Option B: Via gcloud CLI (Local)
```bash
# Get the engine ID from deployment logs
ENGINE_ID=1234567890

# Delete the reasoning engine
gcloud ai reasoning-engines delete $ENGINE_ID \
  --project=bobs-brain \
  --region=us-central1
```

#### Option C: Redeploy Previous Version
1. Find the last known good commit
2. Re-run the deployment workflow from that commit
3. This will update the reasoning engine to the previous code

---

## Post-Deployment: Next Steps

After successful deployment and smoke tests:

### 1. Deploy Foreman (Optional)

If you want to deploy the foreman agent as well:

1. Re-run the workflow with:
   - **agent**: `foreman` or `both`
   - **deploy_mode**: `apply`
   - **smoke_tests_enabled**: `true`

### 2. Set Up Monitoring

Configure monitoring and alerting:

- **Cloud Monitoring**: Set up dashboards for Agent Engine metrics
  - Query count
  - Latency percentiles
  - Error rates

- **Cloud Logging**: Create log-based metrics
  - Agent errors
  - Session creation rate
  - API call volumes

- **Budget Alerts**: Monitor costs
  - Set budget threshold (e.g., $50/month for dev)
  - Enable email alerts

### 3. Integrate with A2A Gateway

Once bob is deployed:

1. Update A2A gateway configuration to point to the deployed reasoning engine
2. Test A2A protocol calls
3. Verify AgentCard is accessible

### 4. Plan Staging Deployment

After dev is stable:

1. Create staging environment configuration
2. Update CI workflow for staging deploys
3. Test staging deployment process

---

## Troubleshooting Commands

### Check Agent Status
```bash
# List all reasoning engines
gcloud ai reasoning-engines list \
  --project=bobs-brain \
  --region=us-central1

# Describe a specific engine
gcloud ai reasoning-engines describe ENGINE_ID \
  --project=bobs-brain \
  --region=us-central1
```

### View Logs
```bash
# View agent logs
gcloud logging read \
  "resource.type=aiplatform.googleapis.com/ReasoningEngine" \
  --project=bobs-brain \
  --limit=50

# View deployment logs
gcloud logging read \
  "resource.type=cloud_build" \
  --project=bobs-brain \
  --limit=20
```

### Test Agent Locally (Development Only)
```bash
# From repo root with .env configured
source .venv/bin/activate
export PROJECT_ID=bobs-brain
export LOCATION=us-central1
export AGENT_ENGINE_ID=bob-agent-dev
# ... other required env vars

python -c "from agents.bob.agent import get_agent; agent = get_agent(); print('Agent loaded')"
```

---

## Cost Estimation

**Dev Environment (Estimated)**:

- **Reasoning Engine**: ~$0.10-$1.00 per day (light testing usage)
- **Cloud Storage**: Negligible for inline source deployment
- **Cloud Logging**: Free tier (first 50 GB/month)
- **Cloud Trace**: Free tier (first 2.5M spans/month)

**Total Estimated Cost**: $3-30/month for active dev environment

**To minimize costs**:
- Delete dev reasoning engines when not in use
- Use dry-run mode for most testing
- Set budget alerts at $10, $25, $50

---

## Support and References

### Documentation
- Phase 21 AAR: `000-docs/152-AA-REPT-phase-21-agent-engine-dev-first-live-deploy-and-smoke-tests.md`
- Deploy Script: `scripts/deploy_inline_source.py --help`
- Smoke Tests: `scripts/smoke_test_agent_engine.py --help`

### External Resources
- [Agent Engine API Reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine)
- [Vertex AI Agent Engine Overview](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)
- [ADK Deployment Guide](https://google.github.io/adk-docs/deploy/agent-engine/)

### Getting Help
- **Build Captain Email**: claude.buildcaptain@intentsolutions.io
- **GitHub Issues**: https://github.com/jeremylongshore/bobs-brain/issues
- **GCP Support**: Use GCP Console support chat (if available)

---

## Appendix: Workflow Input Reference

| Input | Type | Options | Default | Purpose |
|-------|------|---------|---------|---------|
| `agent` | choice | bob, foreman, both | bob | Which agent(s) to deploy |
| `deploy_mode` | choice | dry-run, apply | dry-run | Validation only vs real deployment |
| `smoke_tests_enabled` | boolean | true/false | false | Enable live API tests after deployment |

**Safe Combinations**:
- ✅ `deploy_mode=dry-run`, `smoke_tests_enabled=false`: Pure validation, no API calls
- ✅ `deploy_mode=dry-run`, `smoke_tests_enabled=true`: Test existing deployment without redeploying
- ⚠️ `deploy_mode=apply`, `smoke_tests_enabled=false`: Deploy but don't test (use for first deploy)
- ⚠️ `deploy_mode=apply`, `smoke_tests_enabled=true`: Deploy and test (use after first success)

---

**End of Playbook**

**Last Updated**: 2025-11-23
**Tested On**: Phase 21 implementation branch
