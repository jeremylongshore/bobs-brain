# GitHub Actions Setup Guide

**Date:** 2025-11-11
**Type:** Operations & Deployment Guide
**Status:** ✅ Active

---

## Overview

This guide explains how to configure GitHub Secrets for automated Cloud Run deployments via GitHub Actions.

## Required GitHub Secrets

Go to: `https://github.com/jeremylongshore/bobs-brain/settings/secrets/actions`

### 1. Google Cloud Authentication

#### Option A: Workload Identity Federation (Recommended)
```
GCP_WORKLOAD_IDENTITY_PROVIDER=projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
GCP_SERVICE_ACCOUNT=github-actions@bobs-brain.iam.gserviceaccount.com
```

**Setup Steps:**
1. Create Workload Identity Pool:
```bash
gcloud iam workload-identity-pools create github-pool \
  --project=bobs-brain \
  --location=global \
  --display-name="GitHub Actions Pool"
```

2. Create Provider:
```bash
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --project=bobs-brain \
  --location=global \
  --workload-identity-pool=github-pool \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

3. Create Service Account:
```bash
gcloud iam service-accounts create github-actions \
  --project=bobs-brain \
  --display-name="GitHub Actions"
```

4. Grant Permissions:
```bash
# Cloud Run Admin
gcloud projects add-iam-policy-binding bobs-brain \
  --member="serviceAccount:github-actions@bobs-brain.iam.gserviceaccount.com" \
  --role="roles/run.admin"

# Service Account User
gcloud projects add-iam-policy-binding bobs-brain \
  --member="serviceAccount:github-actions@bobs-brain.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Artifact Registry Reader
gcloud projects add-iam-policy-binding bobs-brain \
  --member="serviceAccount:github-actions@bobs-brain.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

5. Allow GitHub to impersonate service account:
```bash
gcloud iam service-accounts add-iam-policy-binding github-actions@bobs-brain.iam.gserviceaccount.com \
  --project=bobs-brain \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/jeremylongshore/bobs-brain"
```

#### Option B: Service Account Key (Not Recommended)
```
GCP_SA_KEY=<base64-encoded-service-account-key-json>
```

### 2. Slack Credentials

**Get from:** https://api.slack.com/apps/A099YKLCM1N

```
SLACK_SIGNING_SECRET=***
SLACK_BOT_TOKEN=xoxb-***
```

**Required Scopes:**
- `app_mentions:read`
- `chat:write`
- `im:history`
- `channels:history`
- `groups:history`
- `mpim:history`

## Workflow Files

### 1. Deploy Slack Webhook
**File:** `.github/workflows/deploy-slack-webhook.yml`

**Triggers:**
- Push to `main` branch (when relevant files change)
- Manual workflow dispatch

**What it does:**
1. Authenticates to Google Cloud
2. Verifies required secrets exist
3. Updates Cloud Run service with environment variables
4. Tests the `/slack/events` endpoint
5. Posts deployment summary

### 2. CI Pipeline
**File:** `.github/workflows/ci.yml`

**Triggers:**
- Pull requests
- Push to main

**What it does:**
- Runs tests
- Lints code
- Type checking
- Security scans

### 3. Release Automation
**File:** `.github/workflows/release.yml`

**Triggers:**
- Push to `main`, `master`, or `clean-main`
- Manual workflow dispatch

**What it does:**
- Auto-versioning (semver)
- CHANGELOG generation
- GitHub releases
- Git tag creation

## Testing the Workflow

### Manual Trigger
1. Go to: `https://github.com/jeremylongshore/bobs-brain/actions/workflows/deploy-slack-webhook.yml`
2. Click "Run workflow"
3. Select environment (production/staging)
4. Click "Run workflow"

### Automatic Trigger
```bash
# Make a change to relevant files
echo "# Update" >> bob-vertex-agent/README.md
git add bob-vertex-agent/README.md
git commit -m "feat: update agent documentation"
git push origin main
```

Workflow will automatically trigger and deploy to Cloud Run.

## Monitoring Deployments

### GitHub Actions UI
- View runs: `https://github.com/jeremylongshore/bobs-brain/actions`
- Check logs: Click on any workflow run → Click job → View step logs

### Cloud Run Console
- Service: `https://console.cloud.google.com/run/detail/us-central1/slack-webhook`
- Logs: `https://console.cloud.google.com/logs/query`

### Command Line
```bash
# View workflow runs
gh run list --workflow=deploy-slack-webhook.yml --limit=5

# View specific run logs
gh run view <RUN_ID> --log

# Check Cloud Run service
gcloud run services describe slack-webhook \
  --project=bobs-brain \
  --region=us-central1
```

## Troubleshooting

### Workflow Fails: Authentication Error
**Error:** `Failed to obtain access token`

**Fix:**
1. Verify Workload Identity Federation is set up correctly
2. Check service account permissions
3. Confirm GitHub secrets are set

### Workflow Fails: Missing Secrets
**Error:** `SLACK_SIGNING_SECRET not set`

**Fix:**
1. Go to GitHub repository settings → Secrets → Actions
2. Add required secrets (see "Required GitHub Secrets" above)

### Deployment Succeeds but Bot Doesn't Respond
**Possible causes:**
1. Slack Event Subscriptions URL is incorrect
2. Environment variables not properly set on Cloud Run
3. Slack app permissions incomplete

**Verify:**
```bash
# Check env vars on Cloud Run
gcloud run services describe slack-webhook \
  --project=bobs-brain \
  --region=us-central1 \
  --format="yaml(spec.template.spec.containers[0].env)"

# Test endpoint
curl -X POST https://slack-webhook-205354194989.us-central1.run.app/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test"}'
```

## Security Best Practices

### 1. Rotate Secrets Regularly
- Slack tokens: Every 90 days
- Service account keys: Every 90 days (if using keys)
- Update GitHub Secrets after rotation

### 2. Principle of Least Privilege
- Service account only has Cloud Run permissions
- No broader GCP permissions granted
- Slack bot only has required scopes

### 3. Audit Logs
```bash
# View Cloud Run deployments
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-webhook" \
  --project=bobs-brain \
  --limit=10 \
  --format=json

# View GitHub Actions audit log
gh api /repos/jeremylongshore/bobs-brain/actions/runs
```

### 4. Branch Protection
Require:
- Status checks to pass before merging
- Code review approval
- Up-to-date branches

## Rollback Procedure

### If Deployment Breaks Production

**Option 1: Revert via GitHub**
```bash
# Revert the commit
git revert <BAD_COMMIT_SHA>
git push origin main

# Workflow will auto-deploy the reverted version
```

**Option 2: Manual Rollback via Cloud Run**
```bash
# List revisions
gcloud run revisions list \
  --service=slack-webhook \
  --project=bobs-brain \
  --region=us-central1

# Rollback to previous revision
gcloud run services update-traffic slack-webhook \
  --project=bobs-brain \
  --region=us-central1 \
  --to-revisions=<PREVIOUS_REVISION>=100
```

**Option 3: Re-run Previous Workflow**
1. Go to successful previous workflow run
2. Click "Re-run all jobs"

## References

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Cloud Run Docs:** https://cloud.google.com/run/docs
- **Workload Identity Federation:** https://cloud.google.com/iam/docs/workload-identity-federation
- **Slack API:** https://api.slack.com/apps/A099YKLCM1N

---

**Last Updated:** 2025-11-11
**Maintained By:** DevOps Team
**Next Review:** 2025-12-11
