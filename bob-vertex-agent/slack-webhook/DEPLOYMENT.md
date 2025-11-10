# Slack Webhook Deployment Guide

This document explains the production-ready GitHub Actions workflow for deploying the Slack webhook to Google Cloud Functions.

## Table of Contents

- [Overview](#overview)
- [Workflow Architecture](#workflow-architecture)
- [Version Management](#version-management)
- [Deployment Process](#deployment-process)
- [Security](#security)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The Slack webhook deployment pipeline is a fully automated CI/CD workflow that:

- **Validates** code and scans for security issues
- **Versions** the deployment with semantic versioning
- **Deploys** to Cloud Functions Gen2 with WIF authentication
- **Tests** the deployment with smoke tests
- **Documents** changes in CHANGELOG.md and GitHub releases

**Workflow File:** `.github/workflows/deploy-slack-webhook.yml`

## Workflow Architecture

### 5-Job Pipeline

```
┌─────────────┐
│  1. Validate │  Security scan, secrets check, structure validation
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  2. Version  │  Semantic versioning, changelog generation, git tagging
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  3. Deploy   │  WIF auth, Cloud Functions deployment, metadata creation
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  4. Test     │  Smoke tests, logging verification, trace checking
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  5. Finalize │  README update, deployment summary, GitHub release
└─────────────┘
```

### Triggers

| Trigger | Behavior | Version Bump |
|---------|----------|--------------|
| **Push to main** | Auto-deploy on `slack-webhook/**` changes | Auto (commit-based) |
| **Manual dispatch** | Deploy with manual version bump | User choice (major/minor/patch) |
| **Version tag** | Deploy specific version | Tag version (v1.2.3) |

## Version Management

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features (backward compatible)
- **PATCH** (0.0.1): Bug fixes

### Auto-Detection from Commits

The workflow automatically detects version bumps from commit messages:

| Commit Pattern | Version Bump | Example |
|----------------|--------------|---------|
| `BREAKING CHANGE:` or `major:` | MAJOR | `major: redesign slack integration` |
| `feat:` or `feature:` | MINOR | `feat: add retry logic` |
| Everything else | PATCH | `fix: handle timeout errors` |

### VERSION File

Location: `bob-vertex-agent/slack-webhook/VERSION`

This file stores the current version and is automatically updated on deployment.

```bash
# Current version
cat bob-vertex-agent/slack-webhook/VERSION
# Output: 0.1.0
```

### CHANGELOG.md

Auto-generated changelog entries categorize commits:

- **Added:** New features (`feat:`, `add:`)
- **Changed:** Updates and refactors (`change:`, `update:`, `refactor:`)
- **Fixed:** Bug fixes (`fix:`, `bug:`)

Example:
```markdown
## [0.2.0] - 2025-11-15

### Added
- feat: add retry logic for Agent Engine failures (abc123)

### Changed
- refactor: improve error handling (def456)

### Fixed
- fix: handle timeout errors gracefully (ghi789)
```

### Git Tags

Each deployment creates a git tag:

Format: `slack-webhook-vMAJOR.MINOR.PATCH`

Example: `slack-webhook-v0.2.0`

```bash
# View all slack webhook versions
git tag -l "slack-webhook-v*"
```

## Deployment Process

### 1. Validation Job

**Purpose:** Pre-deployment security and structure checks

**Steps:**
- Install dependencies (including security tools)
- Run Bandit security scan
- Scan for secrets with TruffleHog
- Check for hardcoded secrets (sk-, xoxb-, AIza, credentials.json)
- Validate Cloud Function structure (main.py, requirements.txt, entry point)
- Upload security reports as artifacts

**Failure Conditions:**
- Hardcoded secrets found
- Missing required files
- Entry point function not found

### 2. Version Job

**Purpose:** Manage semantic versioning and changelog

**Steps:**
1. Read current version from `VERSION` file (default: 0.1.0)
2. Determine bump type:
   - Tag trigger: Extract from tag name
   - Manual: Use workflow input
   - Auto: Detect from commit messages
3. Calculate new version
4. Update `VERSION` file
5. Generate changelog entry from commits
6. Commit version changes
7. Create git tag (if not tag-triggered)

**Outputs:**
- `new_version`: Semantic version (e.g., "0.2.0")
- `version_changed`: Boolean (true if version bumped)

### 3. Deploy Job

**Purpose:** Deploy to Cloud Functions with WIF authentication

**Steps:**
1. Checkout code
2. Authenticate via Workload Identity Federation (WIF)
3. Set up Cloud SDK
4. Verify authentication
5. Deploy to Cloud Functions Gen2 with:
   - Runtime: python312
   - Region: us-central1
   - Memory: 512Mi
   - Timeout: 60s
   - Max instances: 10
   - Environment variables:
     - `PROJECT_ID=bobs-brain`
     - `VERSION=<semantic-version>`
     - `LOG_EXECUTION_ID=true`
   - Labels:
     - `version=<version>`
     - `component=slack-webhook`
     - `environment=production`
     - `managed-by=github-actions`
     - `last-deployed=<timestamp>`
6. Get function URL
7. Verify Cloud Logging enabled
8. Create deployment metadata JSON
9. Upload metadata as artifact

**Deployment Metadata Example:**
```json
{
  "version": "0.1.0",
  "deployed_at": "2025-11-10T12:34:56Z",
  "deployed_by": "jeremylongshore",
  "commit_sha": "abc123def456",
  "commit_message": "feat: add retry logic",
  "function_url": "https://slack-webhook-eow2wytafa-uc.a.run.app",
  "region": "us-central1",
  "runtime": "python312",
  "workflow_run": "https://github.com/jeremylongshore/bobs-brain/actions/runs/123456"
}
```

### 4. Smoke Test Job

**Purpose:** Verify deployment success

**Tests:**
1. **URL Verification Test**
   - Send Slack URL verification challenge
   - Verify correct response: `{"challenge":"test_challenge_123"}`

2. **Health Endpoint Test** (optional)
   - Check if `/health` endpoint exists
   - Continue on error (not required)

3. **Cloud Logging Verification**
   - Read recent logs
   - Verify function executed

4. **Cloud Trace Check**
   - Confirm trace collection enabled
   - Display trace URL

**Failure Conditions:**
- URL verification test fails
- No logs found (deployment may have failed silently)

### 5. Finalize Job

**Purpose:** Update documentation and create release

**Steps:**
1. Update README.md with version badge
2. Display deployment summary with:
   - Version, project, region, runtime
   - Next steps for Slack configuration
   - Monitoring links (logs, traces, metrics)
3. Create GitHub Release with:
   - Tag: `slack-webhook-v<version>`
   - Release notes from CHANGELOG
   - Deployment details
   - Monitoring links

**GitHub Release Example:**

```markdown
## Slack Webhook v0.2.0

Deployed to Cloud Functions Gen2 in region `us-central1`.

### Changes
See [CHANGELOG.md](bob-vertex-agent/slack-webhook/CHANGELOG.md) for details.

### Deployment Details
- **Project:** bobs-brain
- **Region:** us-central1
- **Runtime:** python312
- **Deployed by:** @jeremylongshore
- **Commit:** abc123def456

### Monitoring
- [Cloud Logs](https://console.cloud.google.com/logs/query?project=bobs-brain)
- [Cloud Trace](https://console.cloud.google.com/traces/list?project=bobs-brain)
- [Function Metrics](https://console.cloud.google.com/functions/details/us-central1/slack-webhook?project=bobs-brain)
```

## Security

### Workload Identity Federation (WIF)

**No service account keys!** The workflow uses WIF for keyless authentication.

**Configuration:**

```yaml
- name: Authenticate to Google Cloud (WIF)
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: 'projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID'
    service_account: 'SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com'
    token_format: 'access_token'
    access_token_lifetime: '3600s'
```

### Required GitHub Secrets

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `WIF_POOL_ID` | Workload Identity Pool ID | `github-pool` |
| `WIF_PROVIDER_ID` | Workload Identity Provider ID | `github-provider` |
| `GCP_SERVICE_ACCOUNT` | Service account email | `github-actions@bobs-brain.iam.gserviceaccount.com` |
| `GCP_PROJECT_NUMBER` | GCP project number | `205354194989` |
| `PROJECT_ID` | GCP project ID | `bobs-brain` |

**Set via GitHub Settings:**
```
Repository → Settings → Secrets and variables → Actions → New repository secret
```

### Security Scans

**Bandit:** Python security linter
```bash
bandit -r . -f json -o bandit-report.json
```

**TruffleHog:** Secret scanning
```bash
trufflehog --path bob-vertex-agent/slack-webhook/ --only-verified
```

**Hardcoded Secrets Check:**
```bash
grep -r "sk-|xoxb-|AIza|credentials\.json" . --include="*.py"
```

**Failure Policy:** Deployment blocked if secrets found.

## Monitoring

### Cloud Logging

**View logs:**
```bash
gcloud logging read \
  "resource.type=cloud_function AND resource.labels.function_name=slack-webhook" \
  --limit=50 \
  --project=bobs-brain \
  --format=json
```

**Console:** https://console.cloud.google.com/logs/query?project=bobs-brain

### Cloud Trace

Distributed tracing enabled automatically with `LOG_EXECUTION_ID=true`.

**View traces:** https://console.cloud.google.com/traces/list?project=bobs-brain

### Function Metrics

**Console:** https://console.cloud.google.com/functions/details/us-central1/slack-webhook?project=bobs-brain

**Key Metrics:**
- Invocations/minute
- Latency (P50, P95, P99)
- Error rate (%)
- Memory usage
- Active instances

### Deployment Artifacts

Each deployment uploads artifacts:

| Artifact | Retention | Contents |
|----------|-----------|----------|
| `security-reports` | 30 days | Bandit scan results (JSON) |
| `deployment-metadata` | 90 days | Version, timestamp, commit, URL |

**Download artifacts:**
```
GitHub Actions → Workflow run → Artifacts section
```

## Troubleshooting

### Deployment Fails at Validation

**Symptom:** Job 1 (Validate) fails

**Common Causes:**
- Hardcoded secrets detected
- Missing `main.py` or `requirements.txt`
- Entry point function not found

**Solution:**
```bash
# Check for hardcoded secrets
grep -r "sk-\|xoxb-\|AIza" bob-vertex-agent/slack-webhook/ --include="*.py"

# Verify entry point exists
grep "def slack_events" bob-vertex-agent/slack-webhook/main.py

# Validate structure
ls -la bob-vertex-agent/slack-webhook/
# Should have: main.py, requirements.txt, VERSION, CHANGELOG.md
```

### Version Not Bumping

**Symptom:** Job 2 (Version) outputs `version_changed=false`

**Cause:** No commit since last deployment

**Solution:**
- Manual trigger with version bump selection
- Or create new commit with conventional commit message:
  ```bash
  git commit -m "feat: add new feature"  # Minor bump
  git commit -m "fix: resolve bug"       # Patch bump
  git commit -m "BREAKING CHANGE: major update"  # Major bump
  ```

### WIF Authentication Fails

**Symptom:** Job 3 (Deploy) fails with authentication error

**Common Causes:**
- Incorrect GitHub secrets
- WIF not configured in GCP
- Service account lacks permissions

**Solution:**
1. Verify GitHub secrets exist and match GCP configuration
2. Check WIF pool and provider:
   ```bash
   gcloud iam workload-identity-pools describe github-pool \
     --location=global \
     --project=bobs-brain
   ```
3. Verify service account IAM roles:
   ```bash
   gcloud projects get-iam-policy bobs-brain \
     --flatten="bindings[].members" \
     --filter="bindings.members:serviceAccount:github-actions@bobs-brain.iam.gserviceaccount.com"
   ```

### Smoke Tests Fail

**Symptom:** Job 4 (Test) fails on URL verification

**Common Causes:**
- Function not deployed
- Function timeout
- Entry point error

**Solution:**
1. Check function status:
   ```bash
   gcloud functions describe slack-webhook \
     --region=us-central1 \
     --project=bobs-brain \
     --gen2
   ```

2. View function logs:
   ```bash
   gcloud functions logs read slack-webhook \
     --region=us-central1 \
     --project=bobs-brain \
     --limit=20
   ```

3. Test manually:
   ```bash
   curl -X POST https://slack-webhook-eow2wytafa-uc.a.run.app \
     -H "Content-Type: application/json" \
     -d '{"type":"url_verification","challenge":"test"}'
   ```

### GitHub Release Creation Fails

**Symptom:** Job 5 (Finalize) fails at "Create GitHub Release"

**Common Causes:**
- Tag already exists
- Insufficient GitHub token permissions

**Solution:**
1. Delete existing tag (if needed):
   ```bash
   git tag -d slack-webhook-v0.1.0
   git push origin :refs/tags/slack-webhook-v0.1.0
   ```

2. Verify GitHub Actions has write permissions:
   ```yaml
   permissions:
     contents: write  # Required for creating releases
   ```

## Manual Deployment (Bypass Workflow)

If the GitHub Actions workflow is unavailable, deploy manually:

```bash
# 1. Update version
echo "0.2.0" > bob-vertex-agent/slack-webhook/VERSION

# 2. Update CHANGELOG.md manually

# 3. Deploy to Cloud Functions
cd bob-vertex-agent/slack-webhook
gcloud functions deploy slack-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --source=. \
  --entry-point=slack_events \
  --trigger-http \
  --allow-unauthenticated \
  --project=bobs-brain \
  --max-instances=10 \
  --min-instances=0 \
  --memory=512Mi \
  --timeout=60s \
  --set-env-vars="PROJECT_ID=bobs-brain,VERSION=0.2.0,LOG_EXECUTION_ID=true" \
  --set-labels="version=0-2-0,component=slack-webhook,environment=production"

# 4. Test deployment
FUNCTION_URL=$(gcloud functions describe slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --gen2 \
  --format='value(serviceConfig.uri)')

curl -X POST "$FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'

# 5. Create git tag
git tag -a "slack-webhook-v0.2.0" -m "Manual deployment v0.2.0"
git push origin "slack-webhook-v0.2.0"
```

## Best Practices

### Commit Message Format

Use conventional commits for automatic version bumping:

```bash
# Patch bump (bug fixes)
git commit -m "fix: resolve timeout errors"

# Minor bump (new features)
git commit -m "feat: add retry logic for Agent Engine"

# Major bump (breaking changes)
git commit -m "BREAKING CHANGE: redesign webhook architecture"

# Specific component
git commit -m "fix(slack-webhook): handle duplicate events"
```

### Pre-Deployment Checklist

Before pushing to main:

- [ ] Code changes tested locally
- [ ] No hardcoded secrets (use Secret Manager)
- [ ] `requirements.txt` updated
- [ ] Entry point function exists: `slack_events`
- [ ] Conventional commit message used
- [ ] CHANGELOG.md manually reviewed (if needed)

### Post-Deployment Verification

After successful deployment:

1. Check deployment summary in GitHub Actions logs
2. Test in Slack (mention @Bob)
3. Verify Cloud Logs show new version
4. Review GitHub Release notes
5. Update Slack App URL if function URL changed

## Additional Resources

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **WIF Setup Guide:** https://cloud.google.com/iam/docs/workload-identity-federation
- **Cloud Functions Docs:** https://cloud.google.com/functions/docs
- **Semantic Versioning:** https://semver.org/
- **Conventional Commits:** https://www.conventionalcommits.org/

---

**Last Updated:** 2025-11-10
**Workflow Version:** 1.0.0
**Maintained by:** @jeremylongshore
