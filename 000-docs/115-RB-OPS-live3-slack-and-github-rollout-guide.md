# LIVE3 Slack and GitHub Rollout Guide

**Document Number:** 115-RB-OPS-live3-slack-and-github-rollout-guide
**Status:** Active
**Date:** 2025-11-20
**Phase:** LIVE3-STAGE-PROD-SAFETY
**Author:** Build Captain (Claude)

---

## Purpose

This runbook provides operators with a **safe, step-by-step guide** for rolling out LIVE3 features (Slack notifications + GitHub issue creation) across environments: dev → staging → prod.

**Key Principles:**
- Environment-aware safety gates prevent accidental production activation
- Explicit override flags required for staging/prod
- Progressive rollout with validation at each stage
- Easy rollback if issues are detected

---

## Quick Reference

### Environment Readiness Matrix

| Environment | Slack Default | GitHub Default | Override Required |
|-------------|---------------|----------------|-------------------|
| **Dev** | Enabled if configured | DRY_RUN | No (permissive) |
| **Staging** | **DISABLED** | DRY_RUN | **YES** (SLACK_ENABLE_STAGING) |
| **Prod** | **DISABLED** | **DISABLED** | **YES** (SLACK_ENABLE_PROD) |

### Safety Flags Summary

```bash
# Staging Override Flags
SLACK_ENABLE_STAGING=true       # Allow Slack in staging
GITHUB_ENABLE_STAGING=true      # Allow real GitHub issues in staging

# Production Override Flags (⚠️ Use with extreme caution)
SLACK_ENABLE_PROD=true          # Allow Slack in prod
GITHUB_ENABLE_PROD=true         # Allow real GitHub issues in prod
```

---

## Prerequisites

Before starting rollout:

- [ ] **ARV checks pass** in target environment
- [ ] **Smoke test passes** in dev with all features enabled
- [ ] **Staging resources ready** (webhook URLs, tokens, test repos)
- [ ] **Prod resources ready** (webhook URLs, tokens, prod repos)
- [ ] **Rollback plan documented** (how to disable features quickly)
- [ ] **Team notified** of rollout schedule and expected behavior

---

## Phase 1: Dev Environment Validation

### Goal
Validate LIVE3 features work correctly in dev before promoting to staging.

### Steps

#### 1.1 Verify Dev Configuration

```bash
# Check environment detection
make check-config | grep DEPLOYMENT_ENV
# Expected: DEPLOYMENT_ENV=dev

# Verify ARV passes with LIVE3 checks
make arv-department-verbose | grep live3
# Expected: ✅ LIVE3 config check PASS
```

#### 1.2 Enable and Test Slack (Dev)

```bash
# Set environment variables
export DEPLOYMENT_ENV=dev
export SLACK_NOTIFICATIONS_ENABLED=true
export SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/DEV/WEBHOOK

# Run smoke test
make live3-dev-smoke-verbose

# Verify Slack message received in dev channel
```

**Expected Output:**
```
✅ Slack Notifications       PASS
   Posted to Slack (status: 200)
   Environment: [DEV]
```

#### 1.3 Enable and Test GitHub (Dev - Dry-Run)

```bash
# Enable GitHub in dry-run mode (no real issues)
export GITHUB_ISSUE_CREATION_ENABLED=true
export GITHUB_ISSUES_DRY_RUN=true
export GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain

# Run smoke test
make live3-dev-smoke-verbose
```

**Expected Output:**
```
✅ GitHub Issue Creation     PASS
   DRY RUN: Would create N issues
```

#### 1.4 Enable GitHub Real Issues (Dev Only)

⚠️ **Only do this after dry-run testing succeeds**

```bash
# Enable real GitHub issue creation in dev
export GITHUB_ISSUES_DRY_RUN=false
export GITHUB_TOKEN=ghp_dev_token

# Run smoke test (creates real issues)
make live3-dev-smoke-verbose

# Verify issues created in GitHub
gh issue list --repo bobs-brain --limit 5
```

**Rollback:**
```bash
# If issues detected, immediately disable
export GITHUB_ISSUES_DRY_RUN=true
# Re-run smoke test to confirm dry-run mode
make live3-dev-smoke
```

#### 1.5 Dev Validation Checklist

- [ ] Slack messages arrive in dev channel with `[DEV]` prefix
- [ ] GitHub dry-run logs show expected issues (no API calls)
- [ ] GitHub real mode creates actual issues in dev repo
- [ ] All ARV checks pass
- [ ] Smoke test reports all subsystems PASS

**Exit Criteria:**
- Dev environment fully working with all LIVE3 features
- No errors in logs or smoke test output
- Team comfortable with behavior

---

## Phase 2: Staging Environment Rollout

### Goal
Deploy LIVE3 to staging with explicit safety overrides, validate behavior matches dev.

### Steps

#### 2.1 Prepare Staging Resources

**Create staging-specific resources:**

```bash
# 1. Create staging Slack webhook (separate from dev/prod)
# Go to: https://api.slack.com/apps → Incoming Webhooks
# Create webhook for staging channel: #staging-alerts

# 2. Verify staging GitHub token has repo access
gh auth status

# 3. Confirm staging repo exists (or use test repo)
gh repo view bobs-brain-staging
```

#### 2.2 Configure Staging Environment Variables

**In staging deployment config (e.g., GitHub Secrets for staging environment):**

```bash
# Environment detection
DEPLOYMENT_ENV=staging

# Slack configuration (staging-specific)
SLACK_NOTIFICATIONS_ENABLED=true
SLACK_ENABLE_STAGING=true  # ⚠️ Explicit override required!
SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/STAGING/WEBHOOK
SLACK_ENV_LABEL=STAGING

# GitHub configuration (dry-run by default)
GITHUB_ISSUE_CREATION_ENABLED=true
GITHUB_ISSUES_DRY_RUN=true  # Start with dry-run for safety
GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain-staging

# If testing real issues in staging:
# GITHUB_ENABLE_STAGING=true
# GITHUB_ISSUES_DRY_RUN=false
# GITHUB_TOKEN=<staging-token>
```

#### 2.3 Deploy to Staging

```bash
# Trigger staging deployment via GitHub Actions
gh workflow run deploy-staging.yml

# Monitor deployment
gh run watch

# Check deployment logs for LIVE3 warnings
gh run view --log | grep "Slack mode\|GitHub mode"
```

**Expected Log Messages:**
```
⚠️  Slack mode: ENABLED (staging - explicit override)
✅  GitHub mode: DRY_RUN (staging, override not set)
```

#### 2.4 Validate Staging Behavior

**Run smoke test in staging:**

```bash
# SSH to staging environment or run in CI
export DEPLOYMENT_ENV=staging
export SLACK_ENABLE_STAGING=true
export SLACK_NOTIFICATIONS_ENABLED=true
export GITHUB_ISSUE_CREATION_ENABLED=true

# Run smoke test
make live3-dev-smoke-verbose
```

**Verify:**
- [ ] Slack messages arrive in **staging channel** (not dev/prod)
- [ ] Messages prefixed with `[STAGING]`
- [ ] GitHub dry-run mode active (no real issues created)
- [ ] ARV reports staging readiness

#### 2.5 Enable Real GitHub Issues in Staging (Optional)

⚠️ **Only if needed for full staging validation**

```bash
# Add staging override
export GITHUB_ENABLE_STAGING=true
export GITHUB_ISSUES_DRY_RUN=false
export GITHUB_TOKEN=ghp_staging_token

# Run smoke test (creates real issues in staging repo)
make live3-dev-smoke-verbose

# Verify issues in staging repo
gh issue list --repo bobs-brain-staging
```

#### 2.6 Staging Validation Checklist

- [ ] Slack messages go to **staging channel only**
- [ ] Messages clearly labeled with `[STAGING]`
- [ ] GitHub dry-run mode works as expected
- [ ] Real GitHub issues (if enabled) only affect staging repo
- [ ] No cross-contamination with dev or prod
- [ ] Logs show staging-specific warnings
- [ ] ARV staging checks pass

**Exit Criteria:**
- Staging behaves identically to dev
- Safety gates properly enforced (overrides required)
- Team confident in promotion to prod

**Hold Point:** Do not proceed to prod until staging runs successfully for at least 1-2 days.

---

## Phase 3: Production Environment Rollout

### Goal
Deploy LIVE3 to production with **maximum caution** and explicit approval.

⚠️ **CRITICAL:** Production rollout requires:
- Successful staging run for 1-2 days minimum
- Explicit approval from team lead
- Rollback plan tested and ready

### Steps

#### 3.1 Pre-Production Checklist

**Before enabling LIVE3 in prod:**

- [ ] **Staging validated** for 1-2 days with no issues
- [ ] **Team approval** obtained (email/meeting confirmation)
- [ ] **Prod resources ready** (prod webhook, prod tokens, prod repos)
- [ ] **Rollback plan tested** in staging
- [ ] **Monitoring configured** (alerts for failures)
- [ ] **Team on-call** during rollout window

#### 3.2 Configure Production Environment Variables

**In production deployment config (GitHub Secrets for prod environment):**

```bash
# Environment detection
DEPLOYMENT_ENV=prod

# Slack configuration (prod-specific)
SLACK_NOTIFICATIONS_ENABLED=true
SLACK_ENABLE_PROD=true  # ⚠️⚠️⚠️ EXTREME CAUTION REQUIRED
SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/PROD/WEBHOOK
SLACK_ENV_LABEL=PROD

# GitHub configuration (start with DRY_RUN for safety)
GITHUB_ISSUE_CREATION_ENABLED=true
GITHUB_ISSUES_DRY_RUN=true  # ⚠️ Keep dry-run until confident
GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain  # Prod repo

# If enabling real issues (ONLY after dry-run validation):
# GITHUB_ENABLE_PROD=true
# GITHUB_ISSUES_DRY_RUN=false
# GITHUB_TOKEN=<prod-token>
```

#### 3.3 Gradual Production Rollout

**Phase 3a: Prod with Slack Only (GitHub Dry-Run)**

```bash
# Deploy to prod with:
# - SLACK_ENABLE_PROD=true (real Slack messages)
# - GITHUB_ISSUES_DRY_RUN=true (no real issues yet)

gh workflow run deploy-prod.yml

# Monitor logs intensely
gh run view --log | grep "PROD\|mode:"
```

**Expected Log Messages:**
```
⚠️  Slack mode: ENABLED (PRODUCTION - explicit override)
✅  GitHub mode: DRY_RUN (prod, override not set)
```

**Validation:**
- [ ] Slack messages arrive in **prod channel only**
- [ ] Messages prefixed with `[PROD]`
- [ ] GitHub still in dry-run (no real issues)
- [ ] No errors in production logs
- [ ] Monitoring shows normal behavior

**Hold for 24 hours** - Monitor production Slack channel for any issues.

**Phase 3b: Prod with GitHub Real Issues (If Needed)**

⚠️ **ONLY enable after 24-hour successful Slack-only operation**

```bash
# Add GitHub prod override
GITHUB_ENABLE_PROD=true
GITHUB_ISSUES_DRY_RUN=false
GITHUB_TOKEN=<prod-token>

# Deploy with extreme caution
gh workflow run deploy-prod.yml

# Monitor GitHub issue creation closely
gh issue list --repo bobs-brain --limit 10
```

**Expected Log Messages:**
```
🚨 GitHub mode: REAL (PRODUCTION - explicit override - USE WITH EXTREME CAUTION)
```

#### 3.4 Production Validation

**After 24-48 hours of prod operation:**

- [ ] Slack notifications working as expected
- [ ] GitHub issues (if enabled) are appropriate and useful
- [ ] No duplicate issues or spam
- [ ] Production logs show no errors
- [ ] Monitoring alerts remain normal
- [ ] Team satisfied with behavior

#### 3.5 Production Rollback Procedure

**If issues detected in prod:**

**Emergency Rollback (Immediate):**

```bash
# Option 1: Disable via environment variables (fastest)
# In prod deployment config:
SLACK_ENABLE_PROD=false
GITHUB_ENABLE_PROD=false

# Redeploy immediately
gh workflow run deploy-prod.yml

# Or Option 2: Disable at feature flag level
SLACK_NOTIFICATIONS_ENABLED=false
GITHUB_ISSUE_CREATION_ENABLED=false
```

**Verification:**

```bash
# Confirm features disabled
gh run view --log | grep "mode: DISABLED"

# Run ARV check
make arv-department-verbose | grep live3
```

**Post-Rollback Actions:**

1. Document what went wrong (create incident report)
2. Fix issues in dev/staging
3. Re-validate completely before re-attempting prod rollout

---

## Monitoring & Maintenance

### Daily Checks (First Week of Prod)

```bash
# 1. Check for failed Slack notifications
# Look for HTTP errors in logs:
gh run list --workflow=ci.yml --limit 5 | grep FAIL

# 2. Check GitHub issues created
gh issue list --repo bobs-brain --created=today

# 3. Check ARV status
make arv-department | grep live3
```

### Weekly Checks (Ongoing)

- [ ] Review Slack channel for noise or spam
- [ ] Review GitHub issues for duplicates
- [ ] Check logs for warnings or errors
- [ ] Verify environment variables haven't drifted

### Alerts to Configure

**Set up monitoring for:**

- LIVE3 subsystem failures (Slack, GitHub API errors)
- Abnormal issue creation volume (>10 issues/hour)
- Webhook failures (4xx/5xx responses)
- Environment variable drift (unexpected values)

---

## Troubleshooting

### Issue: Slack Messages Not Arriving

**Symptoms:**
- Smoke test reports Slack PASS
- No message in Slack channel

**Diagnosis:**
```bash
# 1. Verify environment detection
make check-config | grep DEPLOYMENT_ENV

# 2. Check Slack mode
python3 -c "from agents.config.notifications import get_slack_mode; print(get_slack_mode())"

# 3. Test webhook directly
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test from runbook"}' \
  $SLACK_SWE_CHANNEL_WEBHOOK_URL
```

**Resolution:**
- Verify `SLACK_ENABLE_STAGING=true` or `SLACK_ENABLE_PROD=true` is set
- Check webhook URL is correct for environment
- Confirm Slack app is installed and has permissions

---

### Issue: GitHub Issues Not Created (Real Mode)

**Symptoms:**
- Smoke test reports GitHub PASS
- No issues appear in repository

**Diagnosis:**
```bash
# 1. Verify GitHub mode
python3 -c "from agents.config.github_features import get_github_mode; print(get_github_mode('bobs-brain'))"

# 2. Check token and permissions
gh auth status
```

**Resolution:**
- Verify `GITHUB_ENABLE_STAGING=true` or `GITHUB_ENABLE_PROD=true` is set
- Check `GITHUB_ISSUES_DRY_RUN=false` (if real mode desired)
- Confirm repo is in allowlist: `GITHUB_ISSUE_CREATION_ALLOWED_REPOS`
- Verify token has `repo` scope

---

### Issue: Wrong Environment Detected

**Symptoms:**
- Dev features enabled in staging/prod
- Environment label incorrect in Slack

**Diagnosis:**
```bash
# Check environment detection
python3 -c "from agents.config.features import get_current_environment; print(get_current_environment())"

# Check environment variable
echo $DEPLOYMENT_ENV
```

**Resolution:**
- Explicitly set `DEPLOYMENT_ENV=staging` or `DEPLOYMENT_ENV=prod`
- Verify Terraform/deployment configs set environment correctly
- Check Cloud Run services have `DEPLOYMENT_ENV` environment variable

---

## Rollback Scenarios

### Scenario 1: Slack Messages Too Noisy

**Problem:** Slack channel flooded with messages

**Quick Fix:**
```bash
# Disable Slack temporarily
SLACK_NOTIFICATIONS_ENABLED=false

# Or reduce frequency (implement in code)
# Add throttling/batching logic
```

**Long-term Fix:**
- Implement message batching
- Add "summary only" mode
- Filter low-severity notifications

---

### Scenario 2: Duplicate GitHub Issues

**Problem:** Same issue created multiple times

**Quick Fix:**
```bash
# Switch to dry-run immediately
GITHUB_ISSUES_DRY_RUN=true

# Or disable completely
GITHUB_ISSUE_CREATION_ENABLED=false
```

**Long-term Fix:**
- Implement deduplication logic
- Add issue similarity checking
- Cache recent issues to prevent duplicates

---

### Scenario 3: Wrong Repo Targeted

**Problem:** Issues created in wrong repository

**Quick Fix:**
```bash
# Disable immediately
GITHUB_ISSUE_CREATION_ENABLED=false

# Close incorrect issues
gh issue close <issue-number> -c "Created in wrong repo by automation error"
```

**Long-term Fix:**
- Review allowlist configuration
- Add environment-specific repo validation
- Test with staging repos before prod

---

## Related Documentation

- **ARV Framework:** `117-AA-REPT-iam-department-arv-implementation.md`
- **Smoke Test Guide:** `121-DR-GUIDE-live3-dev-smoke-test.md`
- **Feature Flags:** `.env.example` - Complete flag reference
- **Config Standard:** `116-DR-STND-config-and-feature-flags-standard-v1.md`
- **Deployment Runbook:** `119-RB-OPS-deployment-operator-runbook.md`

---

## Appendix A: Complete Environment Variable Reference

### Dev Environment

```bash
DEPLOYMENT_ENV=dev
SLACK_NOTIFICATIONS_ENABLED=true
SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/DEV/WEBHOOK
GITHUB_ISSUE_CREATION_ENABLED=true
GITHUB_ISSUES_DRY_RUN=false  # Can be false in dev
GITHUB_TOKEN=ghp_dev_token
GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain
```

### Staging Environment

```bash
DEPLOYMENT_ENV=staging
SLACK_NOTIFICATIONS_ENABLED=true
SLACK_ENABLE_STAGING=true  # Required!
SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/STAGING/WEBHOOK
SLACK_ENV_LABEL=STAGING
GITHUB_ISSUE_CREATION_ENABLED=true
GITHUB_ENABLE_STAGING=true  # Required for real issues
GITHUB_ISSUES_DRY_RUN=true  # Recommended: start with dry-run
GITHUB_TOKEN=ghp_staging_token
GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain-staging
```

### Production Environment

```bash
DEPLOYMENT_ENV=prod
SLACK_NOTIFICATIONS_ENABLED=true
SLACK_ENABLE_PROD=true  # ⚠️ Required!
SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/PROD/WEBHOOK
SLACK_ENV_LABEL=PROD
GITHUB_ISSUE_CREATION_ENABLED=true
GITHUB_ENABLE_PROD=true  # ⚠️⚠️ Required for real issues
GITHUB_ISSUES_DRY_RUN=false  # Only after extensive validation
GITHUB_TOKEN=<prod-token-from-secrets>
GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain
```

---

## Appendix B: Emergency Contacts

**During LIVE3 rollout, have these contacts available:**

- **Team Lead:** [Name] - Approval authority for prod rollout
- **DevOps Lead:** [Name] - Infrastructure and deployment support
- **On-Call Engineer:** [Name/Rotation] - Emergency rollback execution
- **Slack Admin:** [Name] - Slack webhook and channel management
- **GitHub Admin:** [Name] - Repository and permissions management

---

**Status:** ✅ Active
**Owner:** DevOps/Operations Team
**Last Updated:** 2025-11-20
**Next Review:** 2025-12-20
**Approval Required:** Team Lead (before prod rollout)
