# First Real Deploy Operator Checklist - Bob's Brain

**Document ID:** 154-NOTE-bobs-brain-first-real-deploy-operator-checklist
**Type:** NOTE (Operator Checklist)
**Created:** 2025-11-23
**Branch:** `claude/phase-21-gcp-setup-01LJYGDWWVQ7hrk8GZFx9Yh3`
**Version:** 0.10.0
**Target Environment:** Dev (bobs-brain project)

---

## Scope

This checklist guides the operator through the first real deployment of the `bob` agent to Vertex AI Agent Engine in the existing `bobs-brain` GCP project (project number: 205354194989). This deployment uses the **6767-INLINE** (inline source) pattern and existing Workload Identity Federation (WIF) setup.

**Key Constraints:**
- ✅ Use existing project `bobs-brain` (do NOT create new project)
- ✅ Use existing WIF configuration (do NOT create new WIF pool)
- ✅ All deployments via GitHub Actions (do NOT run gcloud from local VM)
- ✅ Follow dry-run → apply → smoke test progression (safety gates)

**Prerequisites:**
- GitHub repository admin access (to verify/set secrets)
- GCP project viewer/editor access (to verify APIs and permissions)
- Understanding of CI/CD workflows and rollback procedures

---

## Pre-Flight Checks

Before running the deployment workflow, verify these items in GitHub and GCP:

### GitHub Secrets Check

**Location:** https://github.com/jeremylongshore/bobs-brain/settings/secrets/actions

- [ ] **WIF_PROVIDER** secret exists
  - **Format:** `projects/PROJECT_NUM/locations/global/workloadIdentityPools/POOL/providers/PROVIDER`
  - **Example:** `projects/205354194989/locations/global/workloadIdentityPools/bobs-brain-github-pool/providers/github`
  - **How to verify:** Click "Update" on the secret (you won't see the value, but confirms it exists)
  - **If missing:** Contact GCP admin to create WIF configuration and provide provider resource name

- [ ] **WIF_SERVICE_ACCOUNT** secret exists
  - **Format:** `SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com`
  - **Example:** `bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com`
  - **How to verify:** Click "Update" on the secret
  - **If missing:** Contact GCP admin to create service account and provide email

### GCP APIs Check

**Location:** https://console.cloud.google.com/apis/library?project=bobs-brain

Verify these APIs are **enabled** in project `bobs-brain`:

- [ ] **Vertex AI API** (`aiplatform.googleapis.com`)
  - Required for: Agent Engine deployment and queries
  - Enable command: `gcloud services enable aiplatform.googleapis.com --project=bobs-brain`

- [ ] **Cloud Logging API** (`logging.googleapis.com`)
  - Required for: Agent runtime logs
  - Enable command: `gcloud services enable logging.googleapis.com --project=bobs-brain`

- [ ] **Cloud Storage API** (`storage.googleapis.com`)
  - Required for: Agent Engine internal storage (not used in inline mode, but may be required by API)
  - Enable command: `gcloud services enable storage.googleapis.com --project=bobs-brain`

- [ ] **IAM API** (`iam.googleapis.com`)
  - Required for: WIF authentication
  - Enable command: `gcloud services enable iam.googleapis.com --project=bobs-brain`

**Note:** If any APIs are missing, they must be enabled before deployment. The workflow will fail with 403/404 errors if APIs are disabled.

### Service Account Permissions Check

**Location:** https://console.cloud.google.com/iam-admin/iam?project=bobs-brain

Find the service account used by WIF (e.g., `bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com`) and verify it has these roles:

- [ ] **Vertex AI User** (`roles/aiplatform.user`) OR **Vertex AI Administrator** (`roles/aiplatform.admin`)
  - Required for: Creating/updating reasoning engines
  - **CRITICAL:** Without this, deployment will fail with 403 Permission Denied

- [ ] **Logs Writer** (`roles/logging.logWriter`)
  - Required for: Writing agent runtime logs to Cloud Logging
  - **Optional but recommended** for debugging

- [ ] **Storage Object Viewer** (`roles/storage.objectViewer`)
  - Required for: Reading from staging buckets (if used)
  - **Optional** for inline source deployment (may not be needed)

**How to verify:**
1. Go to IAM page linked above
2. Filter by the service account email
3. Check the "Role" column for the required roles
4. If roles are missing, click "Edit" (pencil icon) and add them

**Assumed:** Service account has been granted permissions to impersonate via WIF (this is part of WIF setup, outside scope of this checklist).

### WIF Configuration Check

**Location:** https://console.cloud.google.com/iam-admin/workload-identity-pools?project=bobs-brain

Verify the Workload Identity Pool exists:

- [ ] **Pool exists:** `bobs-brain-github-pool` (or similar name)
  - If missing: WIF must be configured manually (see Phase 20 docs)
  - **ASSUMPTION:** This was set up before Phase 21

- [ ] **Provider exists:** `github` (within the pool)
  - Maps GitHub Actions OIDC tokens to GCP service account
  - **ASSUMPTION:** Provider trusts the `jeremylongshore/bobs-brain` repository

- [ ] **Service Account Binding:** The pool/provider is bound to the service account
  - This allows GitHub Actions to impersonate the service account
  - **ASSUMPTION:** Binding was created during WIF setup

**Note:** If WIF is not configured, the deployment workflow will fail at the authentication step with errors like "Invalid JWT" or "Workload identity pool not found."

### Budget and Cost Controls (Recommended)

**Location:** https://console.cloud.google.com/billing/budgets?project=bobs-brain

Set up budget alerts to avoid unexpected costs:

- [ ] **Budget alert** configured for project `bobs-brain`
  - **Recommended threshold:** $50/month for dev environment
  - **Alert at:** 50%, 90%, 100% of budget
  - **Notification method:** Email to project owner

**Estimated Costs (Dev Environment):**
- Reasoning Engine (light usage): ~$0.10-$1.00/day
- Cloud Logging (free tier): $0
- Cloud Storage (inline mode): negligible
- **Total:** ~$3-30/month for active development

**Note:** Agent Engine pricing is based on query volume and session duration. Monitor usage in the GCP Billing dashboard.

---

## Phase 21 Deploy Steps (GitHub Actions)

### Step 1: Run Dry-Run Workflow (Validation Only)

**Purpose:** Validate configuration without creating any GCP resources (safe).

1. **Navigate to GitHub Actions:**
   - URL: https://github.com/jeremylongshore/bobs-brain/actions
   - Workflow: **Deploy to Agent Engine (Inline Source - Dev)**

2. **Click "Run workflow"** (button in top-right)

3. **Configure workflow inputs:**
   | Input | Value | Reason |
   |-------|-------|--------|
   | `agent` | `bob` | Start with bob only |
   | `deploy_mode` | `dry-run` | ⚠️ SAFE - No deployment |
   | `smoke_tests_enabled` | `false` | No agents deployed yet |

4. **Click "Run workflow"** (green button in modal)

5. **Monitor the workflow run:**
   - Wait 5-10 seconds for run to appear in list
   - Click on the run to view details
   - Watch these jobs:
     - ✅ **arv-checks** - Must pass (ARV minimum, drift detection)
     - ✅ **deploy-bob** - Should show "Configuration valid (dry-run mode)"
     - ✅ **smoke-tests** - Will run in config-only mode (expected)
     - ✅ **deployment-summary** - Shows summary

6. **Verify success:**
   - Look for this in `deploy-bob` job logs:
     ```
     ✅ Configuration valid (dry-run mode)
        To deploy for real, remove --dry-run flag
     ```
   - All jobs should have green checkmarks
   - No errors in any job logs

**If dry-run fails:**
- Review job logs for specific errors
- Common issues:
  - ARV checks fail: Fix code/config issues, re-run
  - WIF auth fails: Check GitHub secrets exist
  - Import errors: Check agent module structure
- **DO NOT proceed to Step 2** until dry-run passes cleanly

**Expected Duration:** 2-5 minutes

---

### Step 2: Run Real Deployment (Creates GCP Resources)

⚠️ **WARNING:** This step will create actual resources in GCP and may incur costs.

**Prerequisites:**
- ✅ Dry-run (Step 1) completed successfully
- ✅ All pre-flight checks passed
- ✅ Budget alerts configured (recommended)

1. **Navigate to GitHub Actions:**
   - URL: https://github.com/jeremylongshore/bobs-brain/actions
   - Workflow: **Deploy to Agent Engine (Inline Source - Dev)**

2. **Click "Run workflow"**

3. **Configure workflow inputs:**
   | Input | Value | Reason |
   |-------|-------|--------|
   | `agent` | `bob` | Deploy bob agent |
   | `deploy_mode` | `apply` | ⚠️ REAL DEPLOYMENT |
   | `smoke_tests_enabled` | `false` | Enable after first success |

4. **Click "Run workflow"**

5. **Monitor the deployment closely:**

   **Job 1: arv-checks**
   - Must pass before deployment proceeds
   - If fails: Deployment will be cancelled automatically
   - Check: ARV minimum, drift detection, A2A readiness (if available)

   **Job 2: deploy-bob (THE CRITICAL ONE)**
   - Look for these log messages:
     ```
     🚀 Deploying bob to Vertex AI Agent Engine...
        Environment: dev
        Project: bobs-brain
        Region: us-central1

     📦 Loading agent from agents.bob.agent...
     ✅ Agent loaded successfully

     🔄 Creating reasoning engine on Vertex AI...
        This may take 2-3 minutes...

     ✅ Deployment successful!
        Resource Name: projects/205354194989/locations/us-central1/reasoningEngines/1234567890
        Engine ID: 1234567890
     ```

   - **CRITICAL:** Save the **Resource Name** and **Engine ID** from logs!
     - You'll need these for verification and troubleshooting
     - Example: Copy to a text file or GitHub issue comment

   **Job 3: smoke-tests**
   - Will run in config-only mode (expected, since `smoke_tests_enabled=false`)
   - This is safe and won't call deployed agent yet

   **Job 4: deployment-summary**
   - Shows summary with link to GCP console
   - Click link to view deployed reasoning engine

6. **Verify in GCP Console:**
   - Open: https://console.cloud.google.com/vertex-ai/agent-engine?project=bobs-brain
   - Look for reasoning engine with:
     - **Display Name:** `bobs-brain-dev`
     - **Status:** `Active` or `Ready`
     - **Engine ID:** Matches deployment logs

**If deployment fails:**
- Review `deploy-bob` job logs for error message
- Common errors:
  - **403 Permission Denied:** Service account missing `roles/aiplatform.user`
  - **404 Not Found:** API not enabled or project ID incorrect
  - **Import Error:** Agent module not found or malformed
  - **Timeout:** Network issue or Agent Engine service disruption
- See "Validation - Common Errors" section below for fixes
- **Rollback:** See "Rollback / Failure Notes" section if needed

**Expected Duration:** 5-10 minutes (including 2-3 min for Agent Engine deployment)

---

### Step 3: Enable Smoke Tests (Validation)

**Purpose:** Verify deployed agent responds to queries correctly.

**Prerequisites:**
- ✅ Step 2 (real deployment) completed successfully
- ✅ Reasoning engine visible in GCP console with "Active" status

1. **Navigate to GitHub Actions:**
   - URL: https://github.com/jeremylongshore/bobs-brain/actions
   - Workflow: **Deploy to Agent Engine (Inline Source - Dev)**

2. **Click "Run workflow"**

3. **Configure workflow inputs:**
   | Input | Value | Reason |
   |-------|-------|--------|
   | `agent` | `bob` | Test bob agent |
   | `deploy_mode` | `dry-run` | Don't redeploy |
   | `smoke_tests_enabled` | `true` | ⚠️ Enable live tests |

   **Note:** Using `dry-run` for deployment but enabling smoke tests. The smoke tests job will detect an agent is deployed and run live tests against it.

4. **Click "Run workflow"**

5. **Monitor smoke tests job:**
   - Look for `smoke-tests` job logs:
     ```
     ================================================================================
     SMOKE TEST - LIVE MODE
     ================================================================================
     Project: bobs-brain
     Region: us-central1
     Environment: dev

     🧪 Testing bob...
        Resource: projects/205354194989/.../reasoningEngines/1234567890
        ✅ Agent Engine connection established
        📤 Sending: 'What is your name and role?...'
        📥 Response: 'I am Bob, your AI assistant...'
        ✅ bob responded successfully

     ✅ All smoke tests passed!
     ```

6. **Verify success:**
   - Smoke tests job has green checkmark
   - Agent responded with non-empty, coherent message
   - No API errors in logs

**If smoke tests fail:**
- **Connection Error:** Verify reasoning engine ID is correct and status is "Active"
- **Timeout:** Agent may still be initializing (wait 1-2 min, retry)
- **Empty Response:** Check Cloud Logging for agent runtime errors
- **API Error:** Verify service account has correct permissions

**Expected Duration:** 2-5 minutes

---

## Validation - How to Confirm Deployment Succeeded

### Method 1: GCP Console Verification

1. **Open Agent Engine Console:**
   - URL: https://console.cloud.google.com/vertex-ai/agent-engine?project=bobs-brain

2. **Verify reasoning engine exists:**
   - Display Name: `bobs-brain-dev`
   - Status: `Active` or `Ready` (green indicator)
   - Type: `Reasoning Engine` (inline source)
   - Region: `us-central1`

3. **Check details:**
   - Click on the reasoning engine
   - Verify entrypoint: `agents.bob.agent::app`
   - Check creation timestamp (should match deployment time)

### Method 2: Cloud Logging Verification

1. **Open Cloud Logging:**
   - URL: https://console.cloud.google.com/logs/query?project=bobs-brain

2. **Query for agent logs:**
   ```
   resource.type="aiplatform.googleapis.com/ReasoningEngine"
   resource.labels.reasoning_engine_id="ENGINE_ID"
   ```
   - Replace `ENGINE_ID` with the ID from deployment logs

3. **Look for initialization logs:**
   - Should see logs from agent startup
   - No errors during initialization
   - Agent loaded successfully

### Method 3: Smoke Test Verification

- Run smoke tests (Step 3 above)
- ✅ All tests pass
- ✅ Agent responds to queries
- ✅ No API errors

### Method 4: GitHub Actions Workflow History

1. **Navigate to:**
   - URL: https://github.com/jeremylongshore/bobs-brain/actions

2. **Verify workflow run:**
   - Latest run has all green checkmarks
   - `deploy-bob` job completed successfully
   - Deployment logs show "✅ Deployment successful!"
   - Smoke tests passed (if enabled)

**Success Criteria (All Must Be True):**
- [ ] Reasoning engine visible in GCP console
- [ ] Status is "Active" or "Ready"
- [ ] Deployment workflow completed with all green checkmarks
- [ ] Smoke tests pass (if enabled)
- [ ] No errors in Cloud Logging

---

## Rollback / Failure Notes

### When to Rollback

Rollback if:
- Agent fails smoke tests consistently
- Agent produces errors in Cloud Logging
- Deployment introduces breaking changes
- Unexpected costs detected

**Do NOT rollback** if:
- Minor cosmetic issues in agent responses (can be fixed with redeployment)
- Smoke tests fail due to transient network issues (retry first)

### Rollback Option A: Delete via GCP Console (Recommended)

**Use when:** You want to completely remove the deployed agent.

1. **Open Agent Engine Console:**
   - URL: https://console.cloud.google.com/vertex-ai/agent-engine?project=bobs-brain

2. **Select the reasoning engine:**
   - Click checkbox next to `bobs-brain-dev`

3. **Click "Delete"**
   - Confirm deletion in modal
   - Wait for deletion to complete (~30 seconds)

4. **Verify:**
   - Reasoning engine no longer appears in list
   - Smoke tests will fail (expected - no agent deployed)

**Impact:**
- ✅ Agent is completely removed
- ✅ No ongoing costs from this deployment
- ❌ Cannot be undone (must redeploy to restore)

### Rollback Option B: Redeploy Previous Version

**Use when:** You want to restore a previous working version.

1. **Find the last known good commit:**
   - Review GitHub commit history
   - Identify commit hash before breaking change
   - Example: `a2c5edfd` (commit from Phase 21 AAR)

2. **Checkout previous commit locally:**
   ```bash
   git fetch origin
   git checkout COMMIT_HASH
   ```

3. **Push to a rollback branch:**
   ```bash
   git checkout -b rollback/revert-to-COMMIT_HASH
   git push origin rollback/revert-to-COMMIT_HASH
   ```

4. **Run deployment workflow:**
   - Select the rollback branch
   - Run with `deploy_mode=apply`
   - This will **update** the existing reasoning engine to previous code

5. **Verify:**
   - Smoke tests pass
   - Agent behaves as expected
   - Cloud Logging shows no errors

**Impact:**
- ✅ Reasoning engine remains (same Engine ID)
- ✅ Code reverted to previous version
- ⚠️ May take 5-10 minutes for update to complete

### Rollback Option C: Via gcloud CLI (Advanced)

**Use when:** Console is unavailable or scripting is needed.

**Prerequisites:**
- Local `gcloud` CLI installed and authenticated
- Project set to `bobs-brain`

1. **Get Engine ID:**
   - From deployment logs or console
   - Example: `1234567890`

2. **Delete reasoning engine:**
   ```bash
   gcloud ai reasoning-engines delete ENGINE_ID \
     --project=bobs-brain \
     --region=us-central1
   ```

3. **Confirm deletion:**
   - Type `Y` when prompted
   - Wait for confirmation message

**Impact:** Same as Option A (complete removal)

### Common Deployment Errors and Fixes

**Error:** `403 Permission Denied`
- **Cause:** Service account missing `roles/aiplatform.user`
- **Fix:** Add role to service account in IAM console
- **Retry:** Re-run deployment workflow after role added

**Error:** `404 Not Found` (API not found)
- **Cause:** Vertex AI API not enabled
- **Fix:** Enable API via `gcloud services enable aiplatform.googleapis.com`
- **Retry:** Re-run deployment workflow

**Error:** `ImportError: cannot import name 'app'`
- **Cause:** Agent module doesn't export `app` or `get_agent()`
- **Fix:** Check `agents/bob/agent.py` exports correct variable
- **Retry:** Fix code, commit, re-run workflow

**Error:** `Timeout waiting for operation`
- **Cause:** Agent Engine service slow or network issue
- **Fix:** Wait 5 minutes, check GCP status dashboard, retry
- **Retry:** Re-run deployment workflow

**Error:** `Invalid JWT` or `Workload identity pool not found`
- **Cause:** WIF not configured or GitHub secrets incorrect
- **Fix:** Verify WIF setup in GCP, check GitHub secrets
- **Retry:** Fix WIF/secrets, re-run workflow

### Post-Rollback Actions

After rollback:

1. **Document the issue:**
   - Create GitHub issue describing what failed
   - Include deployment logs and error messages
   - Tag with `rollback` and `deployment-failure` labels

2. **Investigate root cause:**
   - Review code changes between working and failing versions
   - Check Cloud Logging for agent errors
   - Test locally if possible

3. **Plan fix:**
   - Create fix branch from last known good commit
   - Apply fix incrementally
   - Test dry-run before real deployment

4. **Redeploy when ready:**
   - Follow Steps 1-3 again with fixed code
   - Monitor closely for same issues

---

## Post-Deployment: Monitoring and Next Steps

### Monitoring Dashboards

Bookmark these URLs for ongoing monitoring:

**Agent Engine Console:**
- https://console.cloud.google.com/vertex-ai/agent-engine?project=bobs-brain
- Shows all deployed reasoning engines
- Check status, view metrics, manage engines

**Cloud Logging:**
- https://console.cloud.google.com/logs/query?project=bobs-brain
- Filter by: `resource.type="aiplatform.googleapis.com/ReasoningEngine"`
- Monitor agent runtime logs and errors

**Cloud Monitoring (Optional):**
- https://console.cloud.google.com/monitoring?project=bobs-brain
- Create custom dashboards for:
  - Query count per day
  - Latency percentiles (p50, p95, p99)
  - Error rates
  - Session duration

**Billing Dashboard:**
- https://console.cloud.google.com/billing?project=bobs-brain
- Monitor costs daily during first week
- Verify costs stay within budget alert threshold

### Deploy Foreman (Optional Next Step)

After `bob` is stable, deploy the foreman agent:

1. **Run deployment workflow:**
   - `agent`: `foreman`
   - `deploy_mode`: `dry-run` (validate first)
   - Verify dry-run passes

2. **Deploy for real:**
   - `agent`: `foreman`
   - `deploy_mode`: `apply`
   - Monitor deployment

3. **Enable smoke tests:**
   - `deploy_mode`: `dry-run`
   - `smoke_tests_enabled`: `true`
   - Verify foreman responds

### Deploy Both Agents Simultaneously (Advanced)

For future deployments, you can deploy both at once:

1. **Run workflow with:**
   - `agent`: `both`
   - `deploy_mode`: `dry-run` → `apply`
   - Both jobs will run in parallel

2. **Monitor both jobs:**
   - `deploy-bob`
   - `deploy-foreman`

3. **Smoke tests will cover both agents**

### Set Up Continuous Deployment (Future)

After manual deployment is stable, consider:

- Auto-deploy on merge to `main` branch
- Separate workflows for dev/staging/prod
- Canary deployments (gradual rollout)
- Automated rollback on smoke test failure

---

## Support and Troubleshooting

### Documentation References

- **Phase 21 AAR:** `000-docs/152-AA-REPT-phase-21-agent-engine-dev-first-live-deploy-and-smoke-tests.md`
- **Deployment Playbook:** `000-docs/153-NOTE-bobs-brain-first-real-agent-engine-deploy-playbook.md`
- **This Checklist:** `000-docs/154-NOTE-bobs-brain-first-real-deploy-operator-checklist.md`

### Command Reference

**List deployed reasoning engines:**
```bash
gcloud ai reasoning-engines list \
  --project=bobs-brain \
  --region=us-central1
```

**Describe specific engine:**
```bash
gcloud ai reasoning-engines describe ENGINE_ID \
  --project=bobs-brain \
  --region=us-central1
```

**View agent logs:**
```bash
gcloud logging read \
  "resource.type=aiplatform.googleapis.com/ReasoningEngine" \
  --project=bobs-brain \
  --limit=50
```

**Check enabled APIs:**
```bash
gcloud services list --enabled --project=bobs-brain
```

### Getting Help

**GitHub Issues:**
- URL: https://github.com/jeremylongshore/bobs-brain/issues
- Create issue for deployment problems
- Include: workflow run URL, logs, error messages

**GCP Support:**
- Use GCP Console support chat (if available)
- For billing questions: Billing support

**Internal Team:**
- Build Captain: `claude.buildcaptain@intentsolutions.io`
- DevOps Lead: (TBD)

---

## Checklist Summary

**Pre-Flight (Before Any Deployment):**
- [ ] WIF_PROVIDER secret exists in GitHub
- [ ] WIF_SERVICE_ACCOUNT secret exists in GitHub
- [ ] Vertex AI API enabled in bobs-brain project
- [ ] Service account has roles/aiplatform.user
- [ ] Budget alert configured (recommended)

**Deployment Sequence:**
- [ ] Step 1: Run dry-run workflow (validation)
- [ ] Step 2: Run real deployment (apply mode)
- [ ] Step 3: Enable smoke tests (validation)
- [ ] Verify in GCP console (reasoning engine exists)
- [ ] Save Resource Name and Engine ID
- [ ] Monitor for first 24 hours

**Post-Deployment:**
- [ ] Bookmark monitoring dashboards
- [ ] Check logs for errors daily (first week)
- [ ] Verify costs stay within budget
- [ ] Document any issues in GitHub
- [ ] Plan next deployment (foreman or both)

---

**End of Operator Checklist**

**Last Updated:** 2025-11-23
**Tested On:** Phase 21 implementation branch (`claude/phase-21-gcp-setup-01LJYGDWWVQ7hrk8GZFx9Yh3`)
**Status:** Ready for first deployment (pending pre-flight checks)
