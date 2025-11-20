# LIVE3 Dev Smoke Test Guide

**Document Number:** 121-DR-GUIDE-live3-dev-smoke-test
**Status:** Active
**Date:** 2025-11-20
**Phase:** LIVE3-E2E-DEV
**Author:** Build Captain (Claude)

---

## Purpose

This guide provides operators with a quick, repeatable way to test the complete LIVE3 integration pipeline in the dev environment. The smoke test validates end-to-end functionality across all LIVE3 subsystems: portfolio audits, GCS storage, Slack notifications, and GitHub issue creation.

---

## Quick Reference

### Single Command

```bash
# Run LIVE3 dev smoke test
make live3-dev-smoke

# Run with verbose output
make live3-dev-smoke-verbose

# Run on all local repos
make live3-dev-smoke-all
```

### Expected Duration

- Basic smoke test: 30-60 seconds
- With all features enabled: 2-3 minutes

---

## Prerequisites

### Required Environment Variables

```bash
# Core (always required)
DEPLOYMENT_ENV=dev

# Optional subsystems (enable as needed)
ORG_STORAGE_WRITE_ENABLED=false
SLACK_NOTIFICATIONS_ENABLED=false
GITHUB_ISSUE_CREATION_ENABLED=false
GITHUB_ISSUES_DRY_RUN=true
```

### Optional Configuration

If testing with features **enabled**, also set:

```bash
# For GCS storage testing
ORG_STORAGE_BUCKET=intent-org-knowledge-hub-dev

# For Slack testing
SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# For GitHub testing
GITHUB_TOKEN=ghp_your_token_here
GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain
```

---

## What Gets Tested

The smoke test exercises **4 subsystems**:

| Subsystem | Status | Description |
|-----------|--------|-------------|
| **Portfolio Audit** | Required | Core SWE pipeline via iam-senior-adk-devops-lead |
| **GCS Org Storage** | Optional | Write audit results to org-wide GCS bucket |
| **Slack Notifications** | Optional | Send completion message to Slack channel |
| **GitHub Issues** | Optional | Create issues for findings (respects dry-run) |

### Subsystem Status Indicators

- ✅ **PASS** - Subsystem executed successfully
- ❌ **FAIL** - Subsystem encountered an error
- ⏸️ **SKIPPED** - Subsystem skipped (not applicable)
- ⚫ **DISABLED** - Subsystem disabled via feature flag

---

## Running the Smoke Test

### Test 1: Core Path Only (Default)

**What it tests:** Portfolio audit with all optional features **disabled**

```bash
# Run basic smoke test
make live3-dev-smoke
```

**Expected Output:**
```
====================================================================================
LIVE3 DEV SMOKE TEST SUMMARY
====================================================================================
Started:  2025-11-20 15:30:00
Finished: 2025-11-20 15:30:45
Duration: 45.2s

Subsystem Status:
------------------------------------------------------------------------------------
✅ Portfolio Audit           PASS
⚫ GCS Org Storage           DISABLED
⚫ Slack Notifications       DISABLED
⚫ GitHub Issue Creation     DISABLED
------------------------------------------------------------------------------------

Overall: ✅ PASS
====================================================================================
```

**Interpretation:**
- Core audit succeeded
- Optional subsystems disabled (expected)
- Exit code: 0 (success)

---

### Test 2: GCS Storage Enabled

**What it tests:** Portfolio audit + write to GCS bucket

```bash
# Set environment variables
export DEPLOYMENT_ENV=dev
export ORG_STORAGE_WRITE_ENABLED=true
export ORG_STORAGE_BUCKET=intent-org-knowledge-hub-dev

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Output:**
```
====================================================================================
LIVE3 DEV SMOKE TEST SUMMARY
====================================================================================
...
Subsystem Status:
------------------------------------------------------------------------------------
✅ Portfolio Audit           PASS
   Audited 1 repo(s)
✅ GCS Org Storage           PASS
   Wrote to gs://intent-org-knowledge-hub-dev/portfolio_swe/dev_smoke/...
⚫ Slack Notifications       DISABLED
⚫ GitHub Issue Creation     DISABLED
------------------------------------------------------------------------------------

Overall: ✅ PASS
====================================================================================
```

**Verify in GCS:**
```bash
# List recent smoke test files
gsutil ls gs://intent-org-knowledge-hub-dev/portfolio_swe/dev_smoke/

# View latest file
gsutil cat gs://intent-org-knowledge-hub-dev/portfolio_swe/dev_smoke/$(gsutil ls gs://intent-org-knowledge-hub-dev/portfolio_swe/dev_smoke/ | tail -1)
```

---

### Test 3: Slack Notifications Enabled

**What it tests:** Portfolio audit + Slack message

```bash
# Set environment variables
export DEPLOYMENT_ENV=dev
export SLACK_NOTIFICATIONS_ENABLED=true
export SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Output:**
```
====================================================================================
LIVE3 DEV SMOKE TEST SUMMARY
====================================================================================
...
Subsystem Status:
------------------------------------------------------------------------------------
✅ Portfolio Audit           PASS
   Audited 1 repo(s)
⚫ GCS Org Storage           DISABLED
✅ Slack Notifications       PASS
   Posted to Slack (status: 200)
⚫ GitHub Issue Creation     DISABLED
------------------------------------------------------------------------------------

Overall: ✅ PASS
====================================================================================
```

**Verify in Slack:**
Check the configured Slack channel for a message like:
```
🧪 LIVE3 Dev Smoke Test Completed
✅ Portfolio audit completed: 1 repo(s)
```

---

### Test 4: GitHub Issues (Dry-Run)

**What it tests:** Portfolio audit + GitHub issue creation in dry-run mode

```bash
# Set environment variables
export DEPLOYMENT_ENV=dev
export GITHUB_ISSUE_CREATION_ENABLED=true
export GITHUB_ISSUES_DRY_RUN=true
export GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Output:**
```
====================================================================================
LIVE3 DEV SMOKE TEST SUMMARY
====================================================================================
...
Subsystem Status:
------------------------------------------------------------------------------------
✅ Portfolio Audit           PASS
   Audited 1 repo(s)
⚫ GCS Org Storage           DISABLED
⚫ Slack Notifications       DISABLED
✅ GitHub Issue Creation     PASS
   DRY RUN: Would create N issues
------------------------------------------------------------------------------------

Overall: ✅ PASS
====================================================================================
```

**Note:** No actual GitHub issues are created in dry-run mode.

---

### Test 5: All Features Enabled

**What it tests:** Complete LIVE3 pipeline with all subsystems active

```bash
# Set all environment variables
export DEPLOYMENT_ENV=dev
export ORG_STORAGE_WRITE_ENABLED=true
export ORG_STORAGE_BUCKET=intent-org-knowledge-hub-dev
export SLACK_NOTIFICATIONS_ENABLED=true
export SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
export GITHUB_ISSUE_CREATION_ENABLED=true
export GITHUB_ISSUES_DRY_RUN=false  # ⚠️ CAUTION: Real issues!
export GITHUB_TOKEN=ghp_your_token
export GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Output:**
```
====================================================================================
LIVE3 DEV SMOKE TEST SUMMARY
====================================================================================
...
Subsystem Status:
------------------------------------------------------------------------------------
✅ Portfolio Audit           PASS
✅ GCS Org Storage           PASS
✅ Slack Notifications       PASS
✅ GitHub Issue Creation     PASS
------------------------------------------------------------------------------------

Overall: ✅ PASS
====================================================================================
```

**Verify:**
1. GCS: Check bucket for new file
2. Slack: Check channel for notification
3. GitHub: Check repo for new issues (if dry-run=false)

---

## Interpreting Failures

### Core Subsystem Failure

```
❌ Portfolio Audit           FAIL
   Exception: ...
```

**Meaning:** The core SWE pipeline failed to execute

**Action:**
1. Check environment configuration: `make check-config`
2. Verify ARV checks pass: `make arv-department`
3. Review error details in verbose output
4. Check logs: `less scripts/run_live3_dev_smoke.log`

**Exit Code:** 1 (failure)

---

### Optional Subsystem Failure

```
✅ Portfolio Audit           PASS
❌ GCS Org Storage           FAIL
   Exception: 403 Forbidden

Overall: ✅ PASS  # Core succeeded!
```

**Meaning:** Core pipeline succeeded, but GCS write failed

**Action:**
1. Check GCS bucket exists: `gsutil ls gs://intent-org-knowledge-hub-dev/`
2. Verify IAM permissions: Service account needs `storage.objectCreator`
3. Check bucket name in `.env`: `ORG_STORAGE_BUCKET=...`

**Exit Code:** 0 (core passed, optional failures are OK)

---

### Slack Notification Failure

```
❌ Slack Notifications       FAIL
   Exception: Invalid webhook URL
```

**Action:**
1. Verify webhook URL format: `https://hooks.slack.com/services/...`
2. Test webhook manually: `curl -X POST -H 'Content-type: application/json' --data '{"text":"test"}' $SLACK_SWE_CHANNEL_WEBHOOK_URL`
3. Check Slack app configuration at https://api.slack.com/apps

---

### GitHub Issue Creation Failure

```
❌ GitHub Issue Creation     FAIL
   Exception: 401 Unauthorized
```

**Action:**
1. Verify GitHub token: `echo $GITHUB_TOKEN` (should start with `ghp_`)
2. Check token has `repo` scope
3. Verify repo in allowlist: `echo $GITHUB_ISSUE_CREATION_ALLOWED_REPOS`

---

## CI Integration

The LIVE3 smoke test runs automatically in CI **as a non-blocking job**.

### Viewing CI Results

```bash
# Check GitHub Actions run
gh run list --workflow=ci.yml --limit=1

# View specific run details
gh run view <run-id>

# Download artifacts (if available)
gh run download <run-id>
```

### CI Behavior

- **Runs:** After drift-check passes
- **Blocking:** No - CI succeeds even if smoke test fails
- **Feature Flags:** All disabled in CI by default
- **Artifacts:** Smoke test logs uploaded for debugging

---

## Troubleshooting

### Command Not Found

```bash
# Error: make: *** No rule to make target 'live3-dev-smoke'
```

**Solution:**
```bash
# Verify Makefile has target
grep live3-dev-smoke Makefile

# Run directly if needed
python3 scripts/run_live3_dev_smoke.py --repo bobs-brain --verbose
```

---

### Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'agents'
```

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Verify Python path
echo $PYTHONPATH

# Run from repo root
cd /home/jeremy/000-projects/iams/bobs-brain/
make live3-dev-smoke
```

---

### Permission Denied

```bash
# Error: ./scripts/run_live3_dev_smoke.py: Permission denied
```

**Solution:**
```bash
# Make executable
chmod +x scripts/run_live3_dev_smoke.py

# Or run with python
python3 scripts/run_live3_dev_smoke.py
```

---

## Development Workflow

### Before Committing LIVE3 Changes

```bash
# 1. Run full smoke test
make live3-dev-smoke-verbose

# 2. Verify ARV includes LIVE3
make arv-department-verbose | grep live3

# 3. Run full CI locally (if possible)
make ci
```

### After Enabling New LIVE3 Features

```bash
# Test new feature in isolation first
export SLACK_NOTIFICATIONS_ENABLED=true
make live3-dev-smoke-verbose

# Then test with existing features
export ORG_STORAGE_WRITE_ENABLED=true
make live3-dev-smoke-verbose

# Finally, full integration test
# (enable all features and run)
```

---

## Staging Environment Testing

### Overview

The same smoke test can be run in **staging mode** to validate LIVE3 behavior with staging-specific safety gates. This is critical before promoting to production.

### Key Differences: Dev vs Staging

| Aspect | Dev | Staging |
|--------|-----|---------|
| **DEPLOYMENT_ENV** | `dev` | `staging` |
| **Slack Default** | Enabled if configured | **DISABLED** unless `SLACK_ENABLE_STAGING=true` |
| **GitHub Default** | DRY_RUN | **DRY_RUN** unless `GITHUB_ENABLE_STAGING=true` |
| **Safety Gate** | Permissive | **Strict** (requires explicit override) |

### Running Smoke Test in Staging Mode

#### Test 1: Staging Core Path (All Features Blocked)

```bash
# Set staging environment
export DEPLOYMENT_ENV=staging

# Try to enable features (will be blocked)
export SLACK_NOTIFICATIONS_ENABLED=true
export GITHUB_ISSUE_CREATION_ENABLED=true

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Behavior:**
- Slack: DISABLED (staging requires SLACK_ENABLE_STAGING=true)
- GitHub: DRY_RUN only (staging requires GITHUB_ENABLE_STAGING=true for real)

**Output:**
```
====================================================================================
LIVE3 DEV SMOKE TEST SUMMARY
====================================================================================
Environment: staging
...
Subsystem Status:
------------------------------------------------------------------------------------
✅ Portfolio Audit           PASS
⚫ GCS Org Storage           DISABLED
⚫ Slack Notifications       DISABLED (staging requires SLACK_ENABLE_STAGING=true)
✅ GitHub Issue Creation     DRY_RUN (staging, override not set)
------------------------------------------------------------------------------------

Overall: ✅ PASS
====================================================================================
```

#### Test 2: Staging with Slack Enabled (Explicit Override)

```bash
# Set staging environment
export DEPLOYMENT_ENV=staging

# Enable Slack with staging override
export SLACK_NOTIFICATIONS_ENABLED=true
export SLACK_ENABLE_STAGING=true
export SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/STAGING/WEBHOOK
export SLACK_ENV_LABEL=STAGING  # Optional: custom label

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Behavior:**
- Slack: ENABLED (explicit override granted)
- Messages prefixed with `[STAGING]` (or custom label)

**Output:**
```
✅ Slack Notifications       PASS
   Posted to Slack (status: 200)
   Environment: [STAGING]
```

#### Test 3: Staging with GitHub Real Issues (Use with Caution)

```bash
# Set staging environment
export DEPLOYMENT_ENV=staging

# Enable GitHub with staging override
export GITHUB_ISSUE_CREATION_ENABLED=true
export GITHUB_ENABLE_STAGING=true
export GITHUB_ISSUES_DRY_RUN=false  # ⚠️ Real issues in staging!
export GITHUB_TOKEN=ghp_staging_token
export GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain-staging

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Behavior:**
- GitHub: REAL mode (explicit override granted)
- Creates actual issues in staging repo
- Strong warnings in logs

**Output:**
```
⚠️  GitHub Issue Creation     PASS (REAL - STAGING)
   Created N issues in bobs-brain-staging
   WARNING: Real issues created in staging environment
```

### Staging Safety Checklist

Before running smoke test in staging:

- [ ] Verify `DEPLOYMENT_ENV=staging` is set
- [ ] Confirm you intend to override staging gates (if enabling features)
- [ ] Use staging-specific webhooks/tokens (not dev or prod)
- [ ] Use staging repos for GitHub testing (not prod repos)
- [ ] Set custom `SLACK_ENV_LABEL=STAGING` for clarity
- [ ] Review logs for staging-specific warnings

### Promotion Path: Dev → Staging → Prod

**Recommended testing sequence:**

1. **Dev (Permissive):**
   ```bash
   export DEPLOYMENT_ENV=dev
   # All features work if configured
   ```

2. **Staging (Strict):**
   ```bash
   export DEPLOYMENT_ENV=staging
   export SLACK_ENABLE_STAGING=true
   export GITHUB_ENABLE_STAGING=true
   # Must explicitly override
   ```

3. **Prod (Locked):**
   ```bash
   export DEPLOYMENT_ENV=prod
   export SLACK_ENABLE_PROD=true
   export GITHUB_ENABLE_PROD=true
   # ⚠️ Extreme caution required
   ```

### Staging-Specific Warnings

When running in staging mode, watch for these log messages:

```
⚠️  Slack mode: ENABLED (staging - explicit override)
⚠️  GitHub mode: REAL (STAGING - explicit override)
```

These warnings confirm that staging safety gates were deliberately bypassed.

---

## Related Documentation

- **LIVE3 Architecture:** See LIVE3-related docs in `000-docs/`
- **Feature Flags:** `.env.example` - Complete flag reference
- **ARV Framework:** `117-AA-REPT-iam-department-arv-implementation.md`
- **CI/CD Pipeline:** `118-DR-STND-cicd-pipeline-for-iam-department.md`
- **Deployment Runbook:** `119-RB-OPS-deployment-operator-runbook.md`

---

## Quick Decision Guide

### "Should I run the smoke test?"

**YES, run it:**
- Before committing LIVE3-related changes
- After changing feature flags
- When troubleshooting LIVE3 issues
- Before deploying to staging/prod

**NO, skip it:**
- For non-LIVE3 changes (use `make ci` instead)
- In production (smoke test is dev-only)

### "Which features should I enable?"

**Start with:**
- Core only (all features disabled) - fastest

**Then add:**
- GCS storage - if testing org-wide knowledge hub
- Slack - if testing notification workflow
- GitHub - if testing issue creation (use dry-run first!)

**Avoid enabling:**
- All features at once on first try
- Real GitHub issue creation (dry-run=false) until confident

---

## Summary Checklist

**Before Your First Smoke Test:**
- [ ] Repository cloned: `/home/jeremy/000-projects/iams/bobs-brain/`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Environment configured: `.env` file created from `.env.example`
- [ ] Running from repo root: `pwd` shows bobs-brain directory

**Running the Test:**
- [ ] Start simple: `make live3-dev-smoke` (core only)
- [ ] Check output: Look for "Overall: ✅ PASS"
- [ ] Enable one feature at a time
- [ ] Verify each feature works before adding next

**Interpreting Results:**
- [ ] Core audit must pass (exit code 0)
- [ ] Optional failures are OK (logged but don't fail smoke)
- [ ] Check verbose output for details: `make live3-dev-smoke-verbose`

---

**Status:** ✅ Active
**Owner:** DevOps/Development Team
**Last Updated:** 2025-11-20
**Next Review:** 2025-12-20
