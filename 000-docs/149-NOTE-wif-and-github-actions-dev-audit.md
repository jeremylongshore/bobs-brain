# 149-NOTE-wif-and-github-actions-dev-audit

**Document Type**: Reality Audit – Repository Only (GCP Not Inspected)
**Created**: 2025-11-22
**Status**: Current State Snapshot
**Scope**: WIF and GitHub Actions configuration for dev deployment

---

## GCP Project Note

Throughout this document, `bobs-brain-dev` was used as a **placeholder** GCP project ID.

**We are NOT creating a new project.** Instead, we are reusing the **existing** GCP project:
- **Project ID**: `bobs-brain`
- **Project Number**: `205354194989`
- **Project Name**: Bobs Brain

All commands and Terraform configs use this existing project ID.

Any `gcloud projects create bobs-brain-dev ...` snippets in this document are **obsolete** and should be treated as historical/example-only, not as instructions.

---

## Executive Summary

This document audits the **current state of Workload Identity Federation (WIF) and GitHub Actions workflows** in the bobs-brain repository as of Phase 19/20. The audit is based on **repository files only**; actual GCP project state and GitHub secrets cannot be verified from this context.

**Key Findings**:
- ✅ Multiple deployment workflows exist with WIF integration points
- ⚠️  WIF Terraform resources are **defined but COMMENTED OUT** (not deployed)
- ⚠️  Two naming conventions for WIF secrets exist (`WIF_*` vs `GCP_WORKLOAD_IDENTITY_PROVIDER`)
- ✅ Service account definitions exist in Terraform (ready to deploy)
- ⏸️  **All deployment workflows are manual-trigger only** (`workflow_dispatch`)
- ⏸️  Actual WIF pool/provider must be created manually in GCP before workflows can authenticate

**Impact on Phase 20**: Development deployment can proceed with `--dry-run` mode. Real deployment requires manual GCP/WIF setup first (documented in Phase 19 AAR).

---

## Findings

### 1. GitHub Actions Workflows

#### 1.1 Deployment Workflows (WIF-Enabled)

**Primary Dev Deployment Workflow** (Phase 19 Updated):
- **File**: `.github/workflows/deploy-containerized-dev.yml`
- **Trigger**: `workflow_dispatch` (manual only)
- **WIF Secrets Used**:
  - `WIF_PROVIDER` (workload identity provider resource name)
  - `WIF_SERVICE_ACCOUNT` (service account email for GitHub Actions)
- **Jobs**:
  1. `arv-gate`: ARV checks (drift, A2A readiness, minimum requirements)
  2. `build-and-push`: Docker images (experimental, not required for inline deploy)
  3. `deploy-inline-source`: **Currently stubbed** with manual setup instructions
     - Checks for WIF_PROVIDER and WIF_SERVICE_ACCOUNT secrets
     - Exits with error if secrets missing
     - Intended to call `scripts/deploy_inline_source.py` (not yet created)
  4. `smoke-tests`: Post-deployment health checks
     - Conditional on `SMOKE_TEST_ENABLED` repository variable
     - Calls `scripts/smoke_test_agent_engine.py`
- **Status**: Wired for WIF, but **deployment is stubbed pending script creation**

**Other Agent Engine Workflows**:
- **agent-engine-inline-deploy.yml**: Workflow_dispatch only, uses `WIF_PROVIDER`
- **agent-engine-inline-dev-deploy.yml**: Workflow_dispatch only, uses `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT`
- **agent-engine-inline-dryrun.yml**: Workflow_dispatch only

**Legacy/Alternative Workflows** (Older WIF Naming):
- **deploy-dev.yml**: Uses `GCP_WORKLOAD_IDENTITY_PROVIDER` (older naming convention)
- **deploy-staging.yml**: Workflow_dispatch only
- **deploy-prod.yml**: Workflow_dispatch only
- **deploy-agent-engine.yml**: Uses `GCP_WORKLOAD_IDENTITY_PROVIDER`

**Naming Convention Discrepancy**:
- **Newer workflows** (deploy-containerized-dev.yml, agent-engine-inline-*.yml): Use `WIF_PROVIDER`
- **Older workflows** (deploy-dev.yml, deploy-agent-engine.yml): Use `GCP_WORKLOAD_IDENTITY_PROVIDER`
- **Impact**: GitHub secrets must be configured for both naming patterns if using multiple workflows

#### 1.2 CI/CD Workflows (Non-Deployment)

**Main CI Workflow**:
- **File**: `.github/workflows/ci.yml`
- **Trigger**: push, pull_request (on main, develop, feature/* branches)
- **WIF**: Not used (checks only, no GCP deployment)
- **Jobs**: drift-check, arv-check, arv-department, a2a-contracts, lint, test, security, terraform-validate, documentation-check, structure-validation, live3-dev-smoke, ci-success

**Other Non-Deployment Workflows**:
- **a2a-compliance.yml**: Manual only, no WIF (local checks)
- **ci-rag-readiness.yaml**: RAG readiness checks (deprecated per ci.yml comments)
- **portfolio-swe.yml**: Commented-out WIF auth
- **release.yml**: Manual trigger, no WIF
- **deploy-slack-webhook.yml**: Uses `GCP_WORKLOAD_IDENTITY_PROVIDER`

---

### 2. WIF Expectations (From Terraform and Workflows)

#### 2.1 WIF Pool and Provider (Terraform)

**File**: `infra/terraform/iam.tf`

**Status**: **COMMENTED OUT** (lines 124-152)

**Expected Configuration** (if uncommented):
```hcl
# Workload Identity Pool
resource "google_iam_workload_identity_pool" "github_actions" {
  workload_identity_pool_id = "${var.app_name}-github-pool"
  display_name              = "Bob's Brain GitHub Actions Pool"
  description               = "Workload Identity Pool for GitHub Actions"
  project                   = var.project_id
}

# Workload Identity Provider (OIDC)
resource "google_iam_workload_identity_pool_provider" "github_actions" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_actions.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name                       = "GitHub Actions Provider"
  project                            = var.project_id

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Bind WIF to GitHub Actions Service Account
resource "google_service_account_iam_member" "github_actions_wif" {
  service_account_id = google_service_account.github_actions.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_actions.name}/attribute.repository/YOUR_GITHUB_ORG/bobs-brain"
}
```

**Required Manual Edits**:
- Replace `YOUR_GITHUB_ORG` with actual GitHub organization or username
- Uncomment all three resources
- Run `terraform apply` to create WIF infrastructure

**Expected Resource Names** (based on Terraform and `dev.tfvars`):
- **Pool ID**: `bobs-brain-github-pool`
- **Provider ID**: `github`
- **Full Provider Resource Name** (for `WIF_PROVIDER` secret):
  ```
  projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/bobs-brain-github-pool/providers/github
  ```

#### 2.2 Service Accounts (Terraform)

**File**: `infra/terraform/iam.tf`

**Status**: **DEFINED** (not commented out, ready to deploy)

**Service Accounts Created**:

1. **GitHub Actions Service Account**:
   - **Account ID**: `${var.app_name}-github-actions` → `bobs-brain-github-actions`
   - **Email** (for `WIF_SERVICE_ACCOUNT` secret):
     ```
     bobs-brain-github-actions@bobs-brain-dev.iam.gserviceaccount.com
     ```
   - **Roles Granted**:
     - `roles/editor` (broad project permissions)
     - `roles/run.admin` (Cloud Run deployments)
     - `roles/aiplatform.admin` (Agent Engine operations)
     - `roles/storage.admin` (GCS for Terraform state, Docker images)

2. **Agent Engine Service Account**:
   - **Account ID**: `${var.app_name}-agent-engine-${var.environment}` → `bobs-brain-agent-engine-dev`
   - **Email**: `bobs-brain-agent-engine-dev@bobs-brain-dev.iam.gserviceaccount.com`
   - **Roles Granted**:
     - `roles/aiplatform.user` (Vertex AI access)
     - `roles/ml.developer` (ML development)
     - `roles/logging.logWriter` (logging)
     - `roles/discoveryengine.viewer` (Vertex AI Search)

3. **A2A Gateway Service Account**:
   - **Account ID**: `bobs-brain-a2a-gateway-dev`
   - **Roles**: `roles/aiplatform.user`, `roles/logging.logWriter`

4. **Slack Webhook Service Account**:
   - **Account ID**: `bobs-brain-slack-webhook-dev`
   - **Roles**: `roles/aiplatform.user`, `roles/logging.logWriter`

**Note**: Service accounts will be created by Terraform apply, but **WIF binding** (commented out resource `github_actions_wif`) must be uncommented first.

---

### 3. Gaps / Open Questions

#### 3.1 WIF Configuration Gaps

**What Exists**:
- ✅ Terraform definitions for WIF pool, provider, and binding (commented out)
- ✅ Service account definitions with correct IAM roles
- ✅ Workflow configurations expecting WIF secrets

**What's Missing**:
- ❌ **Actual WIF pool/provider in GCP** (Terraform resources are commented out)
- ❌ **WIF binding to GitHub repo** (requires GitHub org/username to be filled in)
- ❌ **GitHub secrets configured**:
  - `WIF_PROVIDER` = `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/bobs-brain-github-pool/providers/github`
  - `WIF_SERVICE_ACCOUNT` = `bobs-brain-github-actions@bobs-brain-dev.iam.gserviceaccount.com`

**Blockers**:
1. **GCP project must exist**: `bobs-brain-dev` (or other project ID)
2. **Terraform backend must be configured**: GCS bucket for state
3. **WIF Terraform resources must be uncommented and configured**:
   - Edit `YOUR_GITHUB_ORG` placeholder
   - Run `terraform apply`
4. **GitHub secrets must be added manually**:
   - Navigate to repo Settings → Secrets and variables → Actions
   - Add `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` secrets
5. **Optional: Repository variable for smoke tests**:
   - Add `SMOKE_TEST_ENABLED=true` in repository variables (not secrets)

#### 3.2 Deployment Script Gap

**What Exists**:
- ✅ `scripts/smoke_test_agent_engine.py` (smoke test script)
- ✅ `tests/integration/test_agent_engine_smoke.py` (pytest wrapper)
- ✅ Workflow step that would call deploy script

**What's Missing**:
- ❌ **`scripts/deploy_inline_source.py`** (the actual deployment script)
  - Expected to accept CLI args: `--agent`, `--project-id`, `--region`, `--env`, `--app-version`, `--dry-run`
  - Expected to call Vertex AI Agent Engine API with inline source configuration
  - **This is the primary objective of Phase 20**

**Current Workflow Behavior** (deploy-containerized-dev.yml):
- `deploy-inline-source` job currently runs stub messages
- Explains manual setup requirements
- Does NOT call any deployment script (script doesn't exist yet)

#### 3.3 Naming Convention Inconsistency

**Issue**: Two different secret naming patterns in use:
1. **Newer workflows**: `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`
2. **Older workflows**: `GCP_WORKLOAD_IDENTITY_PROVIDER`

**Recommendation**:
- Standardize on `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` (Phase 19 pattern)
- Update or deprecate older workflows using `GCP_WORKLOAD_IDENTITY_PROVIDER`
- OR: Add both sets of secrets to GitHub for backward compatibility

---

### 4. Impact on Phase 20

#### 4.1 What Can Be Done Now (Without GCP/WIF Setup)

**Safe Operations** ✅:
1. **Create `scripts/deploy_inline_source.py`** with:
   - CLI argument parsing
   - `--dry-run` mode that validates inputs and prints config
   - Stubbed deployment logic that clearly states "GCP client not available"
2. **Wire script into `deploy-inline-source` job**:
   - Call script with `--dry-run` flag by default
   - Validate that workflow can run end-to-end in dry-run mode
3. **Test smoke test infrastructure** in config-only mode:
   - Verify `scripts/smoke_test_agent_engine.py` can validate inputs
   - Consider adding `--config-only` flag for non-deployed testing
4. **Run CI checks locally**:
   - `pytest tests/` (expected: 194 passed, 26 failed due to missing google.adk)
   - `python scripts/check_a2a_readiness.py` (expected: ALL CHECKS PASSED)
   - `terraform validate` (expected: Success)

#### 4.2 What Requires Manual GCP/WIF Setup

**Blocked Operations** ⏸️:
1. **Real Agent Engine deployment**:
   - Requires WIF pool/provider in GCP
   - Requires GitHub secrets configured
   - Requires `scripts/deploy_inline_source.py` to call actual Vertex AI API
   - **Cannot be done until manual setup complete**
2. **Real smoke tests**:
   - Requires agents deployed to Agent Engine
   - Requires `SMOKE_TEST_ENABLED=true` in repository variables
   - **Can be wired but will skip/fail until agents deployed**
3. **Removing `--dry-run` from workflow**:
   - Safe to keep `--dry-run` in Phase 20
   - Remove flag only after confirming GCP/WIF setup works

#### 4.3 Phase 20 Success Criteria (Achievable Without GCP)

**Phase 20 can be considered "complete" when**:
1. ✅ `scripts/deploy_inline_source.py` exists with full CLI interface
2. ✅ Script runs successfully in `--dry-run` mode
3. ✅ Workflow calls script with `--dry-run` (can run in CI without GCP)
4. ✅ Smoke test infrastructure remains wired and can be enabled when ready
5. ✅ AAR documents:
   - What's implemented (script, workflow integration)
   - What's stubbed (actual Agent Engine API calls)
   - What's blocked (real deployment, requires manual GCP setup)
6. ✅ All tests remain green (194 passing baseline maintained)
7. ✅ A2A readiness continues to pass

**Future Phase** (requires manual GCP setup):
- Phase 21 or later: Complete manual GCP/WIF setup, run first real deployment, capture actual smoke test results

---

## Manual Setup Checklist (Reference)

**From Phase 19 AAR** (`000-docs/148-AA-REPT-phase-19-agent-engine-dev-deployment.md`):

### One-Time GCP Setup:

1. **Select Existing GCP Project**:
   ```bash
   # Use existing bobs-brain project (Project Number: 205354194989)
   export PROJECT_ID="bobs-brain"
   gcloud config set project "$PROJECT_ID"

   # Verify project is active
   gcloud config list project
   ```

2. **Enable APIs**:
   ```bash
   export PROJECT_ID="bobs-brain"

   gcloud services enable aiplatform.googleapis.com        --project="$PROJECT_ID"
   gcloud services enable storage-api.googleapis.com       --project="$PROJECT_ID"
   gcloud services enable iam.googleapis.com               --project="$PROJECT_ID"
   gcloud services enable run.googleapis.com               --project="$PROJECT_ID"
   ```

3. **Uncomment and Configure WIF in Terraform**:
   - Edit `infra/terraform/iam.tf`
   - Replace `YOUR_GITHUB_ORG` with actual GitHub org/username
   - Uncomment WIF pool, provider, and binding resources
   - Run `terraform apply`

4. **Get WIF Provider Resource Name**:
   ```bash
   export PROJECT_ID="bobs-brain"

   gcloud iam workload-identity-pools providers describe github \
     --project="$PROJECT_ID" \
     --location=global \
     --workload-identity-pool=bobs-brain-github-pool \
     --format="value(name)"
   ```
   Expected output:
   ```
   projects/205354194989/locations/global/workloadIdentityPools/bobs-brain-github-pool/providers/github
   ```

5. **Add GitHub Secrets**:
   - Go to repo Settings → Secrets and variables → Actions
   - Add secrets:
     - `WIF_PROVIDER` = `projects/205354194989/locations/global/workloadIdentityPools/bobs-brain-github-pool/providers/github`
     - `WIF_SERVICE_ACCOUNT` = `bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com`

6. **Configure Terraform Backend** (for state management):
   ```bash
   export PROJECT_ID="bobs-brain"

   gsutil mb -p "$PROJECT_ID" -l us-central1 gs://"$PROJECT_ID"-terraform-state
   gsutil versioning set on gs://"$PROJECT_ID"-terraform-state
   ```
   - Update `infra/terraform/main.tf` with backend config

7. **Enable Smoke Tests** (after agents deployed):
   - Go to repo Settings → Secrets and variables → Actions → Variables
   - Add variable: `SMOKE_TEST_ENABLED` = `true`

---

## Summary

**WIF & GitHub Actions State**:
- **Workflows**: ✅ Exist and are wired for WIF authentication
- **Terraform WIF**: ⏸️ Defined but commented out (not deployed)
- **Service Accounts**: ✅ Defined in Terraform (ready to deploy)
- **GitHub Secrets**: ⏸️ Expected but not verifiable from repo
- **Deployment Script**: ❌ Does not exist yet (Phase 20 objective)

**Phase 20 Scope**:
- ✅ Can build deployment script with `--dry-run` mode
- ✅ Can wire script into workflow (run with `--dry-run`)
- ✅ Can maintain smoke test infrastructure (skip until agents deployed)
- ⏸️ Cannot perform real deployment (requires manual GCP/WIF setup)

**Next Steps**:
1. **Immediate** (Phase 20): Create `scripts/deploy_inline_source.py`, wire into workflow with `--dry-run`
2. **Future** (Phase 21+): Complete manual GCP/WIF setup, remove `--dry-run`, execute first real deployment

---

**Document**: 149-NOTE-wif-and-github-actions-dev-audit.md
**Created**: 2025-11-22
**Audit Scope**: Repository files only (Terraform, workflows, scripts)
**GCP State**: Not inspected (assumed not configured based on commented Terraform)
**Status**: Current snapshot as of Phase 19/20 boundary
