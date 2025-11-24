# CI1 - Workflow Inventory & Analysis

**Phase:** CICD-DEPT → CI1
**Date:** 2025-11-20
**Status:** Analysis Complete

---

## Executive Summary

Inventoried 6 existing GitHub Actions workflows and assessed alignment with new architecture (ARV-DEPT, config validation, agent factory). Found that **ci.yml is already well-structured** as checks-only workflow, but deployment workflows need:
- ARV gates before deployments
- Environment-aware configurations
- Standardized naming conventions

---

## Existing Workflows

### 1. ci.yml (Main CI Pipeline) ✅ GOOD
- **Triggers:** Push to main/develop/feature/**, PRs to main/develop
- **Jobs:** 10 jobs in dependency chain
  - `drift-check` (first, blocks all if violations)
  - `arv-check` (ARV minimum + engine flags)
  - `arv-department` (comprehensive ARV - NEW from ARV-DEPT phase)
  - `lint`, `test`, `security` (only if drift + ARV pass)
  - `terraform-validate`
  - `documentation-check`
  - `structure-validation`
  - `ci-success` (summary job)

**Assessment:** ✅ **Excellent**
- Already checks-only (no deployment logic)
- ARV-DEPT integrated correctly
- Config validation (CONF2) integrated
- Clear dependency chain
- Blocks dangerous changes early

**Changes Needed:** Minor cleanup only
- Remove or consolidate redundant checks

---

### 2. ci-rag-readiness.yaml (Specialized RAG Gate) ⚠️ REDUNDANT
- **Triggers:** PRs/push on RAG-related paths, manual dispatch
- **Jobs:** Single job `rag-readiness`
  - Validates RAG config and readiness
  - Soft enforcement (continue-on-error: false)

**Assessment:** ⚠️ **Redundant**
- ARV-DEPT now includes `rag-readiness` check
- This creates duplicate RAG validation
- Useful as focused gate for RAG changes, but not necessary

**Changes Needed:** DEPRECATE or merge into ci.yml
- **Recommendation:** Deprecate (covered by ARV-DEPT)
- Alternative: Keep as optional specialized gate for RAG-only changes

---

### 3. deploy-agent-engine.yml (ADK/Agent Engine Deployment) ⚠️ NEEDS WORK
- **Triggers:** Push to main, manual dispatch with environment selection
- **Jobs:** Single job `deploy-agent-engine`
  - Uses WIF authentication ✅
  - Uses ADK CLI ✅
  - Deploys to Vertex AI Agent Engine ✅
  - Supports environment selection (dev/staging/prod) ✅

**Assessment:** ⚠️ **Good pattern, needs ARV gate**
- WIF auth is correct
- ADK CLI deployment is correct
- **Missing:** ARV gate before deployment
- **Missing:** Environment-specific PROJECT_ID/REGION (uses secrets for all envs)
- **Issue:** Deploys `my_agent` (old structure, should be `agents/bob`)

**Changes Needed:** Refactor into deploy-dev.yml
1. Add ARV gate requirement (`needs: [ci-success]` or direct ARV run)
2. Use environment-specific configs from Terraform
3. Update agent path from `my_agent` to `agents/bob`
4. Split into separate workflows per environment

---

### 4. deploy-slack-webhook.yml (Cloud Run Gateway) ⚠️ NEEDS WORK
- **Triggers:** Push to main on service/** paths, manual dispatch
- **Jobs:** Single job `deploy`
  - Deploys Slack webhook to Cloud Run
  - Uses WIF authentication ✅
  - Verifies deployment with endpoint test ✅

**Assessment:** ⚠️ **Good pattern, needs fixes**
- **Issue:** Hardcoded PROJECT_ID and REGION (not environment-aware)
- **Issue:** Path trigger references `bob-vertex-agent/**` (doesn't exist)
- **Missing:** ARV gate before deployment
- Good deployment verification pattern

**Changes Needed:** Include in deploy-dev.yml
1. Fix path triggers (use `service/**` only)
2. Environment-aware PROJECT_ID/REGION
3. Add ARV gate
4. Combine with Agent Engine deployment (single deploy workflow per env)

---

### 5. portfolio-swe.yml (PORT3 Multi-Repo Audit) ✅ SPECIALIZED
- **Triggers:** Nightly schedule (2 AM UTC), manual dispatch
- **Jobs:** Single job `portfolio-audit`
  - Runs ARV portfolio checks
  - Runs portfolio SWE audit
  - Uploads results to artifacts
  - Design-only (LIVE integrations commented out)

**Assessment:** ✅ **Good specialized workflow**
- Purpose-built for multi-repo portfolio audits
- PORT3 phase design-only (LIVE1+ will enable integrations)
- Not part of main CI/CD flow

**Changes Needed:** None (keep as-is)

---

### 6. release.yml (Automated Releases) ✅ GOOD
- **Triggers:** Manual dispatch, push to main/master/clean-main
- **Jobs:** Single job `release`
  - Auto-detects version bump from commits (major/minor/patch)
  - Updates version files, CHANGELOG.md
  - Creates git tags and GitHub releases

**Assessment:** ✅ **Excellent automation**
- Conventional commits pattern (feat:, fix:, BREAKING CHANGE)
- Automatic version management
- Good release workflow

**Changes Needed:** None (keep as-is)

---

## Key Findings

### ✅ Strengths
1. **ci.yml is already checks-only** with ARV-DEPT integrated
2. **WIF authentication pattern exists** in deploy workflows (R4 compliant)
3. **Separation of CI vs deploy** is mostly clean
4. **Good release automation** with conventional commits

### ⚠️ Issues
1. **Deploy workflows lack ARV gates** - deployments can bypass readiness checks
2. **Hardcoded project IDs and regions** - not environment-aware
3. **Redundant RAG validation** - ci-rag-readiness.yaml duplicates ARV-DEPT
4. **Inconsistent naming** - ci.yml vs ci-rag-readiness.yaml vs deploy-*
5. **Outdated path triggers** - deploy-slack-webhook references non-existent paths
6. **Agent path outdated** - deploy-agent-engine uses `my_agent` instead of `agents/bob`

---

## Target Workflow Set

### Core Workflows (Keep/Refactor)

#### 1. ci.yml → **ci.yml** (Keep, minor cleanup)
- **Purpose:** Comprehensive checks gate (blocks bad code)
- **Triggers:** Push to main/develop/feature/**, PRs to main/develop
- **Changes:**
  - Remove redundant checks (if ci-rag-readiness merged)
  - Add CI status badge to outputs
  - Ensure all other workflows depend on this

#### 2. deploy-agent-engine.yml → **deploy-dev.yml** (Refactor)
- **Purpose:** Deploy to dev environment (Agent Engine + gateways)
- **Triggers:** Manual dispatch ONLY (no auto-deploy)
- **Requirements:**
  - `needs: [ci-success]` from ci.yml OR
  - Run ARV-DEPT directly in this workflow
- **Changes:**
  - Add ARV gate (MUST pass before deploy)
  - Use dev-specific configs (PROJECT_ID, REGION from secrets/vars)
  - Update agent path: `agents/bob` (not `my_agent`)
  - Deploy both Agent Engine AND Cloud Run gateways
  - Environment: `dev` (GitHub environment with protection rules)

#### 3. NEW: **deploy-staging.yml** (Skeleton)
- **Purpose:** Deploy to staging environment
- **Triggers:** Manual dispatch, requires approval
- **Requirements:** Same as deploy-dev + manual approval
- **Initial State:** Skeleton only (CICD-DEPT will create)

#### 4. NEW: **deploy-prod.yml** (Skeleton)
- **Purpose:** Deploy to production environment
- **Triggers:** Manual dispatch, requires multiple approvals
- **Requirements:** Same as staging + stricter ARV thresholds
- **Initial State:** Skeleton only (CICD-DEPT will create)

### Specialized Workflows (Keep As-Is)

#### 5. portfolio-swe.yml → **Keep as-is**
- PORT3 specialized workflow
- Not part of main CI/CD flow
- Will be activated in LIVE phases

#### 6. release.yml → **Keep as-is**
- Good automation for version management
- Independent of deploy workflows

### Workflows to Deprecate

#### 7. ci-rag-readiness.yaml → **DEPRECATE**
- Redundant with ARV-DEPT `rag-readiness` check
- Can be deleted after confirming ARV-DEPT covers all cases

---

## Environment-Aware Configuration Strategy

### Current Problem
Deploy workflows use GitHub Secrets for ALL environments:
```yaml
env:
  PROJECT_ID: ${{ secrets.PROJECT_ID }}  # Which project? dev? staging? prod?
  REGION: ${{ secrets.REGION }}
```

### Proposed Solution
Use GitHub Environments with environment-specific secrets/vars:

```yaml
# deploy-dev.yml
environment: dev
env:
  PROJECT_ID: ${{ vars.DEV_PROJECT_ID }}      # dev-specific
  REGION: ${{ vars.DEV_REGION }}
  AGENT_ENGINE_ID: ${{ vars.DEV_AGENT_ENGINE_ID }}

# deploy-staging.yml
environment: staging
env:
  PROJECT_ID: ${{ vars.STAGING_PROJECT_ID }}  # staging-specific
  REGION: ${{ vars.STAGING_REGION }}
  AGENT_ENGINE_ID: ${{ vars.STAGING_AGENT_ENGINE_ID }}
```

**Benefits:**
- Clear separation of dev/staging/prod configs
- Protection rules per environment (approvals, branch restrictions)
- No accidental deploys to wrong environment

---

## Proposed Workflow Dependency Graph

```
┌─────────────────────┐
│      ci.yml         │  ← Runs on: push/PR to main/develop
│   (checks only)    │
│                     │
│ - drift-check       │
│ - arv-check         │
│ - arv-department    │  ← NEW: Comprehensive ARV gate
│ - lint/test/sec     │
│ - terraform-validate│
│ - docs/structure    │
│ - ci-success        │
└──────────┬──────────┘
           │
           │ requires: ci-success
           ├────────────────┬───────────────┬─────────────────┐
           │                │               │                 │
           ▼                ▼               ▼                 ▼
┌──────────────────┐ ┌─────────────┐ ┌──────────────┐ ┌─────────────┐
│ deploy-dev.yml   │ │deploy-stg.yml│ │deploy-prod.yml│ │ release.yml │
│                  │ │              │ │              │ │             │
│ - ARV gate       │ │ - ARV gate   │ │ - ARV gate   │ │ Independent │
│ - Deploy Engine  │ │ - Deploy Eng │ │ - Deploy Eng │ │ automation  │
│ - Deploy gateways│ │ - + gateways │ │ - + gateways │ └─────────────┘
│ - Verify health  │ │ - Approval   │ │ - Approvals  │
└──────────────────┘ └─────────────┘ └──────────────┘

                  ┌──────────────────────┐
                  │ portfolio-swe.yml    │  ← Scheduled (nightly)
                  │ (PORT3 specialized)  │     or manual dispatch
                  └──────────────────────┘
```

---

## Workflow Naming Convention

**Pattern:** `<type>-<scope>.yml`

**Types:**
- `ci` - Continuous Integration (checks only)
- `deploy` - Deployment workflows
- `release` - Release automation
- `portfolio` - Multi-repo operations

**Examples:**
- ✅ `ci.yml` (main checks)
- ✅ `deploy-dev.yml` (dev deployment)
- ✅ `deploy-staging.yml` (staging deployment)
- ✅ `deploy-prod.yml` (prod deployment)
- ✅ `release.yml` (version automation)
- ✅ `portfolio-swe.yml` (multi-repo audit)
- ❌ `ci-rag-readiness.yaml` (inconsistent, redundant)

---

## ARV Gate Requirement

All deployment workflows MUST include ARV gate:

### Option 1: Require ci-success (Recommended)
```yaml
deploy-dev:
  needs: [ci-success]  # From ci.yml workflow
  runs-on: ubuntu-latest
  steps:
    - name: Deploy...
```

**Pros:** DRY (don't repeat ARV checks), clear dependency
**Cons:** Requires ci.yml to run first

### Option 2: Run ARV in Deploy Workflow
```yaml
deploy-dev:
  runs-on: ubuntu-latest
  steps:
    - name: Run ARV Department Check
      run: make arv-department
      env:
        DEPLOYMENT_ENV: dev

    - name: Deploy only if ARV passed
      if: success()
      run: ...
```

**Pros:** Self-contained, works independently
**Cons:** Duplicates ARV checks, longer deploy time

**Recommendation:** Use Option 1 (require ci-success) for main deploys, Option 2 for emergency hotfix workflows.

---

## Next Steps (CI1 Completion)

1. ✅ Inventory complete (this document)
2. 🔄 Define target workflow set (this section)
3. ⏳ Refactor ci.yml (minor cleanup)
4. ⏳ Create deploy-dev.yml (from deploy-agent-engine.yml)
5. ⏳ Create deploy-staging.yml skeleton
6. ⏳ Create deploy-prod.yml skeleton
7. ⏳ Deprecate ci-rag-readiness.yaml
8. ⏳ Update Makefile with deploy targets

---

## Files to Modify (CI1)

### Keep (No Changes)
- `.github/workflows/portfolio-swe.yml` ✅
- `.github/workflows/release.yml` ✅

### Refactor (CI1 + CI2)
- `.github/workflows/ci.yml` (minor cleanup)
- `.github/workflows/deploy-agent-engine.yml` → `deploy-dev.yml`
- `.github/workflows/deploy-slack-webhook.yml` (merge into deploy-dev.yml)

### Deprecate (CI1)
- `.github/workflows/ci-rag-readiness.yaml` (redundant)

### Create (CI2)
- `.github/workflows/deploy-staging.yml` (skeleton)
- `.github/workflows/deploy-prod.yml` (skeleton)

---

**Status:** CI1 analysis complete, ready for CI1 refactoring
**Next Phase:** CI1 refactoring → CI2 deploy wiring
