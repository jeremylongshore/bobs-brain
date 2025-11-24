# 130-AA-REPT-phase-5-first-dev-deploy-and-smoke-test

**Status**: PLANNING
**Author**: Build Captain
**Created**: 2025-11-21
**Phase**: Phase 5 (First Dev Inline Deploy + Smoke Test)

---

## Executive Summary

**[TO BE FILLED AFTER ACTUAL DEV DEPLOY]**

This AAR documents the first real inline source deployment of Bob to Vertex AI Agent Engine dev environment and the subsequent smoke test validation.

---

## Preconditions

Phase 5 builds on the foundation established in Phases 1-4:

### ✅ Phase 1-2: Inline Source Deployment Foundation
- Inline source deploy script created (`agents/agent_engine/deploy_inline_source.py`)
- Bob agent follows lazy-loading App pattern
- Deploy script supports multiple agents (bob, foreman, specialists)
- 6767-INLINE standard document established

### ✅ Phase 3: CI Wiring + Dry-Run
- Dry-run mode as default behavior
- CI workflow validates inline deploy config on PRs
- `--execute` flag for opt-in deployment
- Makefile targets: `deploy-inline-dry-run`, `deploy-inline-dev-execute`

### ✅ Phase 4: ARV Gate + Manual Dev Deploy
- ARV check script validates readiness (`scripts/check_inline_deploy_ready.py`)
- Makefile integration with prerequisite enforcement
- Manual dev deploy workflow (`.github/workflows/agent-engine-inline-dev-deploy.yml`)
- Environment safety rules (dev/staging/prod)

### ✅ Phase 5 Preparation (This Phase)
- Smoke test script created (`scripts/smoke_test_bob_agent_engine_dev.py`)
- Makefile target: `smoke-bob-agent-engine-dev`
- Phase 5 documentation in 6767-INLINE standard
- AAR skeleton prepared (this document)

---

## Plan

### Deployment Approach

**[TO BE DETERMINED: GitHub Actions or Local Execution]**

#### Option A: GitHub Actions (Recommended)
- Use `.github/workflows/agent-engine-inline-dev-deploy.yml`
- Trigger: Manual `workflow_dispatch`
- Inputs: agent_name=bob, gcp_project_id=[PROJECT_ID], gcp_location=us-central1
- Advantages: WIF authentication, CI logs, consistent environment
- Requires: WIF secrets configured in GitHub

#### Option B: Local Execution
- Use `make deploy-inline-dev-execute` locally
- Requires: GCP credentials, environment variables, full dependencies
- Advantages: Immediate execution, local debugging
- Requires: `gcloud auth application-default login`

### Step-by-Step Plan

**[TO BE EXECUTED IN PHASE 6]**

1. **Pre-Deployment Validation**
   - [ ] Confirm ARV check passes: `make check-inline-deploy-ready`
   - [ ] Confirm dry-run passes: `make deploy-inline-dry-run`
   - [ ] Verify GCP project ID is correct
   - [ ] Verify GCP credentials are valid

2. **Execute Dev Deployment**
   - [ ] Choose deployment method (GitHub Actions or local)
   - [ ] Execute deployment command
   - [ ] Monitor deployment progress
   - [ ] Capture Agent Engine resource name from output

3. **Post-Deployment Setup**
   - [ ] Copy Agent Engine resource name
   - [ ] Set environment variable: `export BOB_AGENT_ENGINE_NAME_DEV=...`
   - [ ] Verify agent appears in Agent Engine console
   - [ ] Check agent status is "Active"

4. **Smoke Test Execution**
   - [ ] Run: `make smoke-bob-agent-engine-dev`
   - [ ] Verify result: PASS
   - [ ] Check response contains expected markers ("status", "ok")
   - [ ] Review Cloud Logging for errors

5. **Validation**
   - [ ] Agent responding to queries
   - [ ] No errors in Cloud Logging
   - [ ] Smoke test repeatable (run multiple times)
   - [ ] Performance acceptable (response time < 30s)

6. **Documentation**
   - [ ] Update this AAR with actual results
   - [ ] Document any issues encountered and resolutions
   - [ ] Capture deployment artifacts (resource names, logs, screenshots)
   - [ ] Update 6767-INLINE doc if needed

---

## Risks

### Pre-Deployment Risks

1. **Wrong Project ID**
   - Risk: Deploy to wrong GCP project
   - Mitigation: ARV check validates project ID, double-check before execute
   - Rollback: Delete Agent Engine resource if deployed to wrong project

2. **Misconfigured Entrypoint**
   - Risk: Agent deploys but fails to load
   - Mitigation: Dry-run validation checks entrypoint, local testing before deploy
   - Rollback: Fix entrypoint and redeploy

3. **Missing Dependencies**
   - Risk: Agent deploys but crashes due to missing packages
   - Mitigation: `requirements.txt` tested in CI, dependencies validated
   - Rollback: Update requirements and redeploy

### Deployment Risks

4. **WIF Authentication Failure** (GitHub Actions)
   - Risk: Workflow fails to authenticate to GCP
   - Mitigation: Verify WIF secrets configured, test auth step separately
   - Rollback: Use local deployment as fallback

5. **Agent Engine API Errors**
   - Risk: Deployment fails due to API quota, permissions, or service issues
   - Mitigation: Verify API enabled, check quotas, review IAM permissions
   - Rollback: Address API issues and retry deployment

### Post-Deployment Risks

6. **Smoke Test Failure**
   - Risk: Agent deployed but not responding correctly
   - Mitigation: Comprehensive smoke test with clear error messages
   - Rollback: Debug via Cloud Logging, fix and redeploy

7. **Performance Issues**
   - Risk: Agent responds but too slowly
   - Mitigation: Monitor response times, set acceptable thresholds
   - Rollback: Investigate bottlenecks, optimize if needed

---

## Rollback Plan

**[TO BE FILLED AFTER ACTUAL DEV DEPLOY]**

### How to Disable a Misbehaving Dev Agent

1. **Immediate Disable** (if agent is causing issues):
   ```bash
   # Option 1: Delete Agent Engine resource
   gcloud ai reasoning-engines delete AGENT_ID \
     --project=PROJECT_ID \
     --location=us-central1

   # Option 2: Update agent to inactive state (if supported)
   # [Commands TBD based on Agent Engine API]
   ```

2. **Verify Cleanup**:
   - Check Agent Engine console (agent should be gone)
   - Verify no lingering resources (cloud run services, etc.)
   - Clear environment variable: `unset BOB_AGENT_ENGINE_NAME_DEV`

3. **Root Cause Analysis**:
   - Review Cloud Logging for errors
   - Check agent code for bugs
   - Validate entrypoint configuration
   - Test locally before redeploying

---

## Phase 6 – First Actual Dev Inline Deploy & Smoke Test

### Execution Checklist

**Pre-Deployment** (Run locally before triggering workflow):

1. **Confirm Branch Status**
   - [ ] On branch: `feature/a2a-agentcards-foreman-worker`
   - [ ] Working tree clean: `git status`

2. **Run Local Validation**
   - [ ] ARV check passes: `make check-inline-deploy-ready`
   - [ ] Dry-run passes: `make deploy-inline-dry-run`
   - [ ] Capture successful output shape for AAR

3. **Verify GCP Configuration**
   - [ ] GCP Project ID confirmed (e.g., `205354194989`)
   - [ ] GCP Location confirmed (e.g., `us-central1`)
   - [ ] GitHub WIF secrets configured (if using GitHub Actions)

**Deployment Execution**:

4. **Trigger GitHub Actions Workflow** (Recommended)
   - [ ] Navigate to: https://github.com/[YOUR_ORG]/bobs-brain/actions
   - [ ] Select workflow: "Agent Engine Inline Deploy - Dev (Manual)"
   - [ ] Click: "Run workflow"
   - [ ] Select branch: `feature/a2a-agentcards-foreman-worker`
   - [ ] Fill inputs:
     - `agent_name`: bob
     - `gcp_project_id`: [YOUR_PROJECT_ID]
     - `gcp_location`: us-central1
   - [ ] Click: "Run workflow" (green button)
   - [ ] Monitor workflow execution in Actions tab

**OR** (Alternative: Local Execution):

4. **Run Local Deployment**
   - [ ] Authenticate: `gcloud auth application-default login`
   - [ ] Set env vars: `export GCP_PROJECT_ID=... GCP_LOCATION=us-central1`
   - [ ] Execute: `make deploy-inline-dev-execute`
   - [ ] Wait 5 seconds at warning prompt (or Ctrl+C to cancel)

**Post-Deployment Setup**:

5. **Capture Agent Engine Resource Name**
   - [ ] From GitHub Actions logs OR local output, find line:
     ```
     Agent resource name: projects/.../locations/.../reasoningEngines/...
     ```
   - [ ] Copy full resource name

6. **Configure Local Environment**
   - [ ] Add to `.env`:
     ```bash
     BOB_AGENT_ENGINE_NAME_DEV=projects/205354194989/locations/us-central1/reasoningEngines/[AGENT_ID]
     ```
   - [ ] Export for current shell:
     ```bash
     export BOB_AGENT_ENGINE_NAME_DEV=projects/.../reasoningEngines/...
     export GCP_PROJECT_ID=205354194989
     export GCP_LOCATION=us-central1
     ```

7. **Verify Deployment in Console**
   - [ ] Navigate to: https://console.cloud.google.com/vertex-ai/agent-engine
   - [ ] Verify Bob agent appears in list
   - [ ] Check agent status is "Active"

**Smoke Test Execution**:

8. **Run Smoke Test**
   - [ ] Execute: `make smoke-bob-agent-engine-dev`
   - [ ] Wait for response (may take up to 30s for cold start)
   - [ ] Expected output:
     ```
     [SMOKE] RESULT: PASS
     ```

9. **Record Results**
   - [ ] Smoke test result: PASS/FAIL
   - [ ] Copy response snippet
   - [ ] Note any errors or warnings
   - [ ] Check Cloud Logging for agent logs

**Validation**:

10. **Post-Deployment Verification**
    - [ ] Agent responding to queries
    - [ ] No errors in Cloud Logging
    - [ ] Run smoke test multiple times (confirm repeatable)
    - [ ] Response time acceptable (< 30s)

**Documentation**:

11. **Update This AAR**
    - [ ] Paste deployment output into "Deployment Output" section below
    - [ ] Paste smoke test output into "Smoke Test Results" section below
    - [ ] Fill in "Execution Details" (resource name, git commit, workflow URL)
    - [ ] Update "Lessons Learned" with any issues encountered
    - [ ] Change Status from PLANNING → COMPLETE

12. **Commit AAR Updates**
    - [ ] Stage changes: `git add 000-docs/130-AA-REPT-*.md`
    - [ ] Commit: `git commit -m "docs(aar): update Phase 5 AAR with actual dev deploy results"`
    - [ ] Note: Do NOT push to main yet (still on feature branch)

---

### How to Run the First Dev Inline Deploy (Manual)

**GitHub Actions Workflow** (`.github/workflows/agent-engine-inline-dev-deploy.yml`):

**Workflow Details**:
- **Name**: Agent Engine Inline Deploy - Dev (Manual)
- **Trigger**: `workflow_dispatch` (manual run only)
- **Workflow File**: `.github/workflows/agent-engine-inline-dev-deploy.yml`

**Steps to Execute**:

1. **Navigate to GitHub Actions**:
   ```
   https://github.com/[YOUR_ORG]/bobs-brain/actions
   ```

2. **Select Workflow**:
   - In left sidebar, click: "Agent Engine Inline Deploy - Dev (Manual)"

3. **Run Workflow**:
   - Click: "Run workflow" (dropdown button, top right)
   - Branch: `feature/a2a-agentcards-foreman-worker`
   - Inputs:
     - `agent_name`: bob (select from dropdown)
     - `gcp_project_id`: [YOUR_GCP_PROJECT_ID] (e.g., `205354194989`)
     - `gcp_location`: us-central1 (default, can leave as-is)
   - Click: "Run workflow" (green button)

4. **Monitor Execution**:
   - Workflow will appear in the list (may take a few seconds)
   - Click on the workflow run to see live logs
   - Watch for:
     - ✅ ARV checks passing
     - ✅ Dry-run validation passing
     - 🚀 Deployment execution
     - 📊 Deployment summary

5. **Extract Resource Name**:
   - In the final deployment step, look for:
     ```
     🚀 Deploying agent to dev environment...
        Agent: bob
        Project: [PROJECT_ID]
        Location: us-central1

     [... deployment output ...]

     Agent resource name: projects/205354194989/locations/us-central1/reasoningEngines/1234567890123456789
     ```
   - **Copy this full resource name** (you'll need it for smoke testing)

6. **Verify in Console**:
   - Navigate to: https://console.cloud.google.com/vertex-ai/agent-engine
   - Confirm Bob agent appears
   - Check status is "Active"

**What the Workflow Does**:

The workflow executes these steps automatically:
1. Checkout repository (your feature branch)
2. Set up Python 3.12 with pip cache
3. Install dependencies (`google-cloud-aiplatform`, `google-auth`)
4. Authenticate to GCP using Workload Identity Federation (WIF)
5. Set up gcloud CLI
6. **Run ARV checks** (must pass)
7. **Run dry-run validation** (must pass)
8. **Deploy agent with --execute flag** (REAL DEPLOYMENT)
9. Report deployment status with resource name

**Expected Duration**: 3-5 minutes total

**Workflow Guards**:
- ARV check must pass (validates environment, packages, entrypoint)
- Dry-run must pass (validates configuration before execution)
- Uses WIF for secure GCP authentication (no service account keys in repo)
- Dev environment only (cannot accidentally deploy to staging/prod)

---

## Actual Execution

**[TO BE FILLED DURING PHASE 6 EXECUTION]**

### Execution Details (to be filled after first dev deploy)

**Dev Agent Engine Resource**:
```
projects/205354194989/locations/us-central1/reasoningEngines/XXXXXXXXXXXXXXX
```

**Git Commit Deployed**:
```
[GIT_COMMIT_SHA] - [Commit message]
```

**GitHub Actions Run URL** (if used):
```
https://github.com/[YOUR_ORG]/bobs-brain/actions/runs/[RUN_ID]
```

**Deployment Command** (if local):
```bash
[Command used, e.g., make deploy-inline-dev-execute]
```

### Deployment Method Used

**[GitHub Actions / Local Execution]**

**Reason for choice**: [Why this method was chosen]

### Deployment Timeline

- **Started**: [TIMESTAMP]
- **Completed**: [TIMESTAMP]
- **Duration**: [MINUTES]

### Deployment Output

**[PASTE RELEVANT DEPLOYMENT LOGS/OUTPUT]**

```
[Deployment command output]
[Agent Engine resource name]
[Any warnings or errors]
```

**Key Observations**:
- [Observation 1, e.g., deployment completed without errors]
- [Observation 2, e.g., cold start took X seconds]
- [Any warnings or unusual behavior]

### Smoke Test Configuration

**Environment Variables Set**:
```bash
export BOB_AGENT_ENGINE_NAME_DEV=projects/.../reasoningEngines/...
export GCP_PROJECT_ID=205354194989
export GCP_LOCATION=us-central1
```

**Smoke Test Command**:
```bash
make smoke-bob-agent-engine-dev
```

### Smoke Test Results

**[PASTE SMOKE TEST OUTPUT]**

```
[SMOKE] Starting Bob Agent Engine dev smoke test...
[SMOKE] Configuration:
[SMOKE]   Project: ...
[SMOKE]   Location: ...
[SMOKE]   Agent: ...
[SMOKE] ...
[SMOKE] RESULT: [PASS/FAIL]
```

**Response Time**: [SECONDS]

**Response Snippet**:
```
[First 200 characters of response]
```

**Cloud Logging**:
- [Link to Cloud Logging query, if available]
- [Summary of any errors or warnings in logs]

---

## Results

**[TO BE FILLED AFTER ACTUAL DEV DEPLOY AND SMOKE TEST]**

### Success Criteria

- [ ] Deployment succeeded without errors
- [ ] Agent Engine resource created
- [ ] Smoke test passed on first attempt
- [ ] Agent responding to queries correctly
- [ ] No errors in Cloud Logging
- [ ] Performance acceptable (response time < 30s)

### Actual Results

**[FILL IN AFTER EXECUTION]**

1. **Deployment Success**: [YES/NO]
   - Details: [Description]

2. **Smoke Test Result**: [PASS/FAIL]
   - Details: [Response snippet, timing]

3. **Issues Encountered**: [LIST]
   - Issue 1: [Description and resolution]
   - Issue 2: [Description and resolution]

4. **Performance Metrics**:
   - Deployment time: [MINUTES]
   - Smoke test response time: [SECONDS]
   - Agent cold start time: [SECONDS]

---

## Lessons Learned

**[TO BE FILLED AFTER ACTUAL DEV DEPLOY]**

### What Went Well

**[LIST]**

1. [Item]
2. [Item]

### What Could Be Improved

**[LIST]**

1. [Item]
2. [Item]

### Action Items for Future Deploys

**[LIST]**

1. [Item]
2. [Item]

---

## Next Steps

**[TO BE FILLED AFTER SUCCESSFUL DEV DEPLOY AND SMOKE TEST]**

### Immediate (Phase 6)

- [ ] Update this AAR with actual results
- [ ] Update Status to COMPLETE
- [ ] Commit AAR updates to feature branch
- [ ] Prepare for merge to main

### Future Phases

- [ ] **Phase 6+**: Automatic dev deploy on merge to main
- [ ] **Phase 7**: Staging deployment workflow with stricter gates
- [ ] **Phase 8**: Production deployment with approval requirements
- [ ] **Phase 9**: Integration with Agent Engine deployment status API
- [ ] **Phase 10**: Blue/green deployments, canary rollouts, automated rollback

---

## References

**Phase 5 Deliverables**:
- Smoke Test Script: `scripts/smoke_test_bob_agent_engine_dev.py`
- Makefile Target: `smoke-bob-agent-engine-dev`
- Phase 5 Documentation: `000-docs/6767-INLINE-DR-STND-*.md` (Phase 5 section)

**Deployment Scripts**:
- Deploy: `agents/agent_engine/deploy_inline_source.py`
- ARV Check: `scripts/check_inline_deploy_ready.py`

**CI Workflows**:
- Manual Dev Deploy: `.github/workflows/agent-engine-inline-dev-deploy.yml`
- Dry-Run Validation: `.github/workflows/agent-engine-inline-dryrun.yml`

**External References**:
- Tutorial: `000-docs/001-usermanual/tutorial_get_started_with_agent_engine_terraform_deployment.ipynb`
- Discussion: https://discuss.google.dev/t/deploying-agents-with-inline-source-on-vertex-ai-agent-engine/288935
- Vertex AI Agent Engine Docs: https://cloud.google.com/vertex-ai/docs/agent-engine

---

**Maintained by**: Build Captain
**Related Phases**: Phase 1-4 (foundation), Phase 5 (preparation), Phase 6 (execution)
**Branch**: `feature/a2a-agentcards-foreman-worker`
