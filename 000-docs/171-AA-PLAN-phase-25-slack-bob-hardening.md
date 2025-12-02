# 171-AA-PLAN: Phase 25 - Slack Bob Hardening

**Document Type:** Phase Planning (AA-PLAN)
**Phase:** 25 - Slack Bob Hardening (Lock Gateway Pattern)
**Created:** 2025-11-29
**Status:** In Progress
**Author:** Build Captain

---

## Executive Summary

**Goal:** Kill all legacy deploy paths and harden Slack gateway to **Terraform+CI only** deployments.

**Why This Matters:**
- Enforces R4 (CI-only deployments, no manual gcloud)
- Eliminates orphaned service accounts and configuration drift
- Makes system truly observable and repeatable
- Prevents "works on my machine" deploy disasters

**Success Criteria:**
- ✅ No manual deploy paths exist (no scripts, no docs showing manual deploys)
- ✅ CI workflows for Slack gateway (dev + prod) via Terraform only
- ✅ Documentation reflects Terraform-first pattern
- ✅ ARV checks Slack gateway config before deployments

---

## Background

**Current State (Pre-Phase 25):**
- Slack gateway exists in `service/slack_gateway/`
- Can be deployed via Terraform (good)
- Documentation may reference manual deploys (bad)
- No CI workflow specifically for Slack gateway deployments
- No validation checks for Slack gateway configuration

**Problem:**
Manual deploy paths create:
- Configuration drift (dev vs prod mismatch)
- Orphaned service accounts (created manually, never cleaned up)
- Deployment failures (missing env vars, wrong regions)
- Lack of audit trail (who deployed what, when?)
- Cannot sleep and delegate (requires tribal knowledge)

**Solution:**
Lock Slack gateway to **Terraform+CI only** - make manual deploys impossible.

---

## Phase Scope

### 1. Remove Manual Deploy Paths

**Audit for:**
- ✅ `deploy.sh` scripts in `service/slack_gateway/`
- ✅ `gcloud run deploy` commands in docs
- ✅ Manual deployment instructions in README.md
- ✅ Quickstart guides that bypass CI

**Actions:**
- Delete any `deploy.sh` or similar scripts
- Remove manual deploy examples from `000-docs/`
- Update README.md to ONLY show CI-based deploys
- Add warnings about R4 violation for manual deploys

---

### 2. Strengthen CI Guardrails

**Create Two New Workflows:**

#### A. `deploy-slack-gateway-dev.yml`
- **Trigger:** Manual dispatch OR push to `main` (Slack gateway changes only)
- **Authentication:** WIF-only (Workload Identity Federation)
- **Steps:**
  1. Checkout code
  2. Authenticate via WIF (no service account keys)
  3. Terraform init (backend: GCS)
  4. Terraform plan (validate changes)
  5. Terraform apply (deploy to dev)
  6. Smoke test (health check endpoint)
  7. Post-deploy validation (ARV checks)

#### B. `deploy-slack-gateway-prod.yml`
- **Trigger:** Manual dispatch ONLY (manual approval required)
- **Authentication:** WIF-only
- **Steps:**
  1. Checkout code
  2. Require manual approval gate (GitHub Environments)
  3. Authenticate via WIF
  4. Terraform init (backend: GCS)
  5. Terraform plan (validate changes, require human review)
  6. Manual approval (second gate)
  7. Terraform apply (deploy to prod)
  8. Smoke test (health check endpoint)
  9. Post-deploy validation (ARV checks)
  10. Notify on success/failure (Slack webhook)

**Key Requirements:**
- ✅ WIF-only (no `GOOGLE_APPLICATION_CREDENTIALS` secret)
- ✅ Terraform state in GCS backend (shared across team)
- ✅ Manual approval gates for prod
- ✅ Post-deploy smoke tests (verify endpoint responds)
- ✅ ARV validation (check configuration matches standards)

---

### 3. Documentation Updates

**Update Three Key Docs:**

#### A. Update `126-AA-AUDT-appaudit-devops-playbook.md`
- Remove manual deploy steps
- Add section: "Slack Gateway Deployments (Terraform+CI Only)"
- Reference new workflows: `deploy-slack-gateway-dev.yml`, `deploy-slack-gateway-prod.yml`
- Add troubleshooting section for failed deploys

#### B. Create `6767-122-DR-STND-slack-gateway-deploy-pattern.md` (NEW)
**Content:**
- Canonical Slack gateway deployment pattern (Terraform+CI only)
- How to configure Terraform vars for Slack gateway
- How to trigger deploys via GitHub Actions
- How to validate deploys (smoke tests, ARV checks)
- How to rollback failed deploys
- What NOT to do (manual gcloud deploys)

#### C. Update `README.md`
- Remove quickstart deploy shortcuts (if any)
- Add section: "Deploying Slack Gateway"
  - Link to workflows
  - Link to 6767-122 SOP
  - Emphasize Terraform+CI only

---

### 4. ARV Integration

**Add Validation Checks:**

#### A. Create `make check-slack-gateway-config` target
**Validates:**
- Terraform vars file exists (`service/slack_gateway/terraform.tfvars`)
- Required vars present:
  - `project_id`
  - `region`
  - `slack_signing_secret` (from Secret Manager, not hardcoded)
  - `slack_bot_token` (from Secret Manager, not hardcoded)
- No hardcoded secrets in Terraform files
- Service account follows naming convention
- Environment labels present (dev/prod)

**Implementation:**
```makefile
.PHONY: check-slack-gateway-config
check-slack-gateway-config:
	@echo "Validating Slack gateway Terraform configuration..."
	@python3 scripts/ci/check_slack_gateway_config.py
```

#### B. Create `scripts/ci/check_slack_gateway_config.py`
**Checks:**
- Terraform vars file syntax (valid HCL)
- Required variables present
- No hardcoded secrets (regex check for API keys, tokens)
- Service account naming convention (`slack-gateway-sa@...`)
- Environment labels (`env=dev` or `env=prod`)

**Exit codes:**
- 0 - All checks passed
- 1 - Validation errors found
- 2 - Script error (file not found, etc.)

#### C. Integrate into `ci.yml`
**Add new job:**
```yaml
slack-gateway-validation:
  runs-on: ubuntu-latest
  needs: drift-check  # Only run if drift check passes
  steps:
    - uses: actions/checkout@v4
    - name: Validate Slack gateway config
      run: make check-slack-gateway-config
```

---

## Implementation Steps

### Step 1: Audit Repo (Day 1, Morning)
1. Search for `deploy.sh` scripts:
   ```bash
   find . -name "deploy.sh" -o -name "*deploy*.sh" | grep -v node_modules
   ```
2. Search docs for manual deploy references:
   ```bash
   grep -r "gcloud run deploy" 000-docs/ README.md
   ```
3. Document findings in this PLAN doc (update section below)

### Step 2: Remove Manual Paths (Day 1, Afternoon)
1. Delete identified scripts (if any)
2. Update docs to remove manual deploy examples
3. Commit: `chore(deploy): remove manual Slack gateway deploy paths (R4 compliance)`

### Step 3: Create Dev Workflow (Day 1, Evening)
1. Create `.github/workflows/deploy-slack-gateway-dev.yml`
2. Configure WIF authentication
3. Add Terraform init/plan/apply steps
4. Add smoke test (health check)
5. Commit: `ci(workflows): add Terraform-based Slack gateway dev deploy`

### Step 4: Create Prod Workflow (Day 2, Morning)
1. Create `.github/workflows/deploy-slack-gateway-prod.yml`
2. Configure manual approval gates (GitHub Environments)
3. Add Terraform init/plan/apply steps
4. Add smoke test + ARV validation
5. Commit: `ci(workflows): add Terraform-based Slack gateway prod deploy with approval gates`

### Step 5: Add ARV Checks (Day 2, Afternoon)
1. Create `scripts/ci/check_slack_gateway_config.py`
2. Add `make check-slack-gateway-config` target
3. Integrate into `ci.yml`
4. Test locally: `make check-slack-gateway-config`
5. Commit: `ci(arv): add Slack gateway config validation checks`

### Step 6: Update Documentation (Day 2, Evening)
1. Create `6767-122-DR-STND-slack-gateway-deploy-pattern.md`
2. Update `126-AA-AUDT-appaudit-devops-playbook.md`
3. Update `README.md`
4. Commit: `docs(000-docs): add Slack gateway deploy pattern SOP and update playbook`

---

## Deliverables

**Code:**
- ✅ `.github/workflows/deploy-slack-gateway-dev.yml` (new)
- ✅ `.github/workflows/deploy-slack-gateway-prod.yml` (new)
- ✅ `scripts/ci/check_slack_gateway_config.py` (new)
- ✅ `Makefile` (updated with `check-slack-gateway-config` target)

**Docs:**
- ✅ `6767-122-DR-STND-slack-gateway-deploy-pattern.md` (new SOP)
- ✅ `126-AA-AUDT-appaudit-devops-playbook.md` (updated)
- ✅ `README.md` (updated)
- ✅ `171-AA-PLAN-phase-25-slack-bob-hardening.md` (this document)
- ✅ `172-AA-REPT-phase-25-slack-bob-hardening.md` (AAR, created at end)

**Deleted:**
- ❌ Any `deploy.sh` scripts (if found)
- ❌ Manual deploy references in docs

---

## Testing Plan

### Manual Testing (Local)
1. **Validate ARV Check:**
   ```bash
   make check-slack-gateway-config
   # Expected: PASS (if config valid) or FAIL (with clear errors)
   ```

2. **Validate Terraform Plan:**
   ```bash
   cd service/slack_gateway
   terraform init
   terraform plan
   # Expected: No errors, shows planned changes
   ```

### CI Testing (GitHub Actions)
1. **Trigger Dev Deploy:**
   - Push to main (with Slack gateway changes)
   - OR manually dispatch `deploy-slack-gateway-dev.yml`
   - Expected: Workflow runs, deploys to dev, smoke test passes

2. **Trigger Prod Deploy:**
   - Manually dispatch `deploy-slack-gateway-prod.yml`
   - Approve at manual gates
   - Expected: Workflow runs, deploys to prod, smoke test passes

3. **Validate ARV Integration:**
   - Push commit with invalid Slack config (missing var)
   - Expected: CI fails at `slack-gateway-validation` job

---

## Risk Mitigation

### Risk 1: Existing Manual Deploys Break
**Mitigation:**
- Audit existing Slack gateway deployments (dev/prod)
- Document current state (service account, env vars, region)
- Ensure Terraform matches current state before applying

### Risk 2: WIF Authentication Fails
**Mitigation:**
- Test WIF auth in dev environment first
- Have fallback plan (service account key in GitHub Secrets - temporary only)
- Document WIF setup in 6767-122 SOP

### Risk 3: Approval Gates Block Emergency Deploys
**Mitigation:**
- Document emergency override procedure (break glass)
- Have ops runbook for manual Terraform apply (via WIF, not gcloud)
- Keep approval gates in place (don't bypass for convenience)

---

## Success Metrics

**Phase 25 Complete When:**
- ✅ No manual deploy paths exist (scripts deleted, docs updated)
- ✅ CI workflows for dev + prod Slack gateway deploys
- ✅ ARV checks Slack gateway config in CI
- ✅ 6767-122 SOP created and published
- ✅ DevOps playbook updated
- ✅ README.md reflects Terraform+CI only pattern
- ✅ All tests passing (local + CI)

**"I Can Sleep and Delegate" Check:**
- ✅ New team member can deploy Slack gateway by reading 6767-122 SOP
- ✅ No tribal knowledge required (everything documented)
- ✅ Failed deploys are recoverable via runbook
- ✅ Manual approval gates prevent accidental prod deploys

---

## Audit Trail (Pre-Phase 25)

**Current Deploy Paths (to be removed):**
- [ ] TBD (audit in Step 1)

**Current Documentation References (to be updated):**
- [ ] TBD (audit in Step 1)

**Current CI Coverage:**
- [ ] No Slack gateway-specific workflows (general Terraform workflow only)
- [ ] No ARV checks for Slack gateway config

---

## Next Phase After This

**Phase 26: Agent Engine Dev Deployment**
- Deploy bob + foreman to dev Agent Engine
- Integrate dev Slack → Agent Engine
- Smoke tests and validation

**Dependency:**
Phase 26 requires Phase 25 complete (Slack gateway locked down and observable).

---

## Appendix A: Terraform+CI Pattern (Reference)

**Canonical Pattern for Slack Gateway:**
```
1. Developer updates service/slack_gateway/main.tf
2. Developer commits to feature branch
3. CI runs ARV checks (including check-slack-gateway-config)
4. Developer creates PR to main
5. Code review + approval
6. Merge to main
7. GitHub Actions triggers deploy-slack-gateway-dev.yml
8. Terraform applies changes to dev
9. Smoke test verifies deployment
10. For prod: Manual dispatch of deploy-slack-gateway-prod.yml
11. Manual approval gates (2x)
12. Terraform applies changes to prod
13. Smoke test + ARV validation
```

**What This Prevents:**
- ❌ `gcloud run deploy slack-webhook ...` (R4 violation)
- ❌ Manual env var updates (drift from IaC)
- ❌ Orphaned service accounts (Terraform manages lifecycle)
- ❌ Undocumented deploys (all via CI, audit trail in GitHub Actions)

---

## Document Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-11-29 | Initial phase plan created | Build Captain |

---

**Next Action:** Begin Step 1 (Audit repo for manual deploy paths).
