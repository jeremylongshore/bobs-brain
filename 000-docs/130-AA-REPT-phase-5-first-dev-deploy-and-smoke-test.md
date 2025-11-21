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

## Actual Execution

**[TO BE FILLED DURING PHASE 6 EXECUTION]**

### Deployment Method Used

**[GitHub Actions / Local Execution]**

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

### Smoke Test Results

**[PASTE SMOKE TEST OUTPUT]**

```
[SMOKE] Starting Bob Agent Engine dev smoke test...
[SMOKE] ...
[SMOKE] RESULT: [PASS/FAIL]
```

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
