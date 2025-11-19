# GitHub Secrets Configuration for Deployment

**Date:** 2025-11-19
**Project:** Bob's Brain (bobs-brain)
**Purpose:** Configure GitHub Secrets for Vertex AI Agent Engine deployment
**Workflow:** `.github/workflows/deploy-agent-engine.yml`

---

## Required GitHub Secrets

These secrets must be configured in GitHub repository settings before deployment:

**Path:** Settings → Secrets and variables → Actions → New repository secret

### 1. WIF_PROVIDER (Workload Identity Federation Provider)

**Name:** `WIF_PROVIDER`

**Format:**
```
projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/<POOL_ID>/providers/<PROVIDER_ID>
```

**Example:**
```
projects/123456789/locations/global/workloadIdentityPools/github-actions/providers/github-oidc
```

**How to get:**
```bash
gcloud iam workload-identity-pools providers describe github-oidc \
  --project=bobs-brain-dev \
  --location=global \
  --workload-identity-pool=github-actions \
  --format="value(name)"
```

**Note:** If WIF is not configured yet, follow the setup guide below.

---

### 2. WIF_SERVICE_ACCOUNT (Service Account Email)

**Name:** `WIF_SERVICE_ACCOUNT`

**Format:**
```
<SERVICE_ACCOUNT_NAME>@<PROJECT_ID>.iam.gserviceaccount.com
```

**Example:**
```
github-actions@bobs-brain-dev.iam.gserviceaccount.com
```

**How to get:**
```bash
gcloud iam service-accounts list \
  --project=bobs-brain-dev \
  --filter="displayName:GitHub Actions" \
  --format="value(email)"
```

---

### 3. PROJECT_ID (GCP Project ID)

**Name:** `PROJECT_ID`

**Value:** `bobs-brain-dev` (or your project ID)

**How to get:**
```bash
gcloud config get-value project
```

---

### 4. REGION (GCP Region)

**Name:** `REGION`

**Value:** `us-central1` (or your preferred region)

**Available regions for Vertex AI:**
- `us-central1` (Iowa)
- `us-east1` (South Carolina)
- `us-west1` (Oregon)
- `europe-west1` (Belgium)
- `asia-northeast1` (Tokyo)

---

### 5. STAGING_BUCKET (GCS Bucket URL)

**Name:** `STAGING_BUCKET`

**Format:**
```
gs://<PROJECT_ID>-adk-staging
```

**Example:**
```
gs://bobs-brain-dev-adk-staging
```

**Note:** This bucket is created by Terraform (`infra/terraform/storage.tf`)

**How to verify:**
```bash
terraform output -state=infra/terraform/envs/dev/terraform.tfstate staging_bucket_url
```

Or:
```bash
gsutil ls gs://bobs-brain-dev-adk-staging
```

---

## Workload Identity Federation Setup

If WIF is not configured yet, set it up following these steps:

### Step 1: Create Workload Identity Pool

```bash
gcloud iam workload-identity-pools create github-actions \
  --project=bobs-brain-dev \
  --location=global \
  --display-name="GitHub Actions Pool"
```

### Step 2: Create OIDC Provider

```bash
gcloud iam workload-identity-pools providers create-oidc github-oidc \
  --project=bobs-brain-dev \
  --location=global \
  --workload-identity-pool=github-actions \
  --display-name="GitHub OIDC Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

### Step 3: Create Service Account

```bash
gcloud iam service-accounts create github-actions \
  --project=bobs-brain-dev \
  --display-name="GitHub Actions Deployment"
```

### Step 4: Grant Permissions

```bash
# Vertex AI Admin (for Agent Engine deployment)
gcloud projects add-iam-policy-binding bobs-brain-dev \
  --member="serviceAccount:github-actions@bobs-brain-dev.iam.gserviceaccount.com" \
  --role="roles/aiplatform.admin"

# Storage Admin (for staging bucket)
gcloud projects add-iam-policy-binding bobs-brain-dev \
  --member="serviceAccount:github-actions@bobs-brain-dev.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Service Account User (to act as Agent Engine SA)
gcloud projects add-iam-policy-binding bobs-brain-dev \
  --member="serviceAccount:github-actions@bobs-brain-dev.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

### Step 5: Bind Service Account to Pool

```bash
gcloud iam service-accounts add-iam-policy-binding \
  github-actions@bobs-brain-dev.iam.gserviceaccount.com \
  --project=bobs-brain-dev \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/github-actions/attribute.repository/jeremylongshore/bobs-brain"
```

**Note:** Replace `<PROJECT_NUMBER>` with your project number and update the repository path.

**Get project number:**
```bash
gcloud projects describe bobs-brain-dev --format="value(projectNumber)"
```

---

## Verification

### 1. Verify WIF Provider

```bash
gcloud iam workload-identity-pools providers describe github-oidc \
  --project=bobs-brain-dev \
  --location=global \
  --workload-identity-pool=github-actions
```

### 2. Verify Service Account

```bash
gcloud iam service-accounts describe \
  github-actions@bobs-brain-dev.iam.gserviceaccount.com
```

### 3. Test Authentication Locally

```bash
gcloud auth application-default login
gcloud config set project bobs-brain-dev
adk deploy agent_engine my_agent \
  --project=bobs-brain-dev \
  --region=us-central1 \
  --staging_bucket=gs://bobs-brain-dev-adk-staging
```

---

## Troubleshooting

### Error: "Invalid WIF Provider"

**Solution:** Verify the provider path is correct:
```bash
gcloud iam workload-identity-pools providers list \
  --project=bobs-brain-dev \
  --location=global \
  --workload-identity-pool=github-actions
```

### Error: "Permission denied on staging bucket"

**Solution:** Verify IAM permissions:
```bash
gsutil iam get gs://bobs-brain-dev-adk-staging
```

Grant permissions if missing:
```bash
gsutil iam ch \
  serviceAccount:github-actions@bobs-brain-dev.iam.gserviceaccount.com:admin \
  gs://bobs-brain-dev-adk-staging
```

### Error: "Agent Engine API not enabled"

**Solution:** Enable required APIs:
```bash
gcloud services enable aiplatform.googleapis.com \
  --project=bobs-brain-dev

gcloud services enable compute.googleapis.com \
  --project=bobs-brain-dev
```

---

## Security Best Practices

1. ✅ **Use WIF instead of service account keys** (R4 compliant)
2. ✅ **Limit service account permissions** to minimum required
3. ✅ **Restrict WIF binding** to specific repository only
4. ✅ **Rotate credentials** regularly (WIF auto-handles this)
5. ✅ **Use environment-specific secrets** for dev/staging/prod
6. ✅ **Never commit secrets** to git (use .env.example only)

---

## Summary

**Secrets to Configure:**

| Secret Name | Example Value | How to Get |
|-------------|---------------|------------|
| `WIF_PROVIDER` | `projects/123.../workloadIdentityPools/...` | gcloud WIF describe |
| `WIF_SERVICE_ACCOUNT` | `github-actions@bobs-brain-dev.iam.gserviceaccount.com` | gcloud sa list |
| `PROJECT_ID` | `bobs-brain-dev` | gcloud config get |
| `REGION` | `us-central1` | Choose from list |
| `STAGING_BUCKET` | `gs://bobs-brain-dev-adk-staging` | terraform output |

**Next Steps:**
1. Configure secrets in GitHub (Settings → Secrets)
2. Run Terraform to create staging bucket
3. Trigger deployment workflow (push to main or manual dispatch)
4. Verify Agent Engine deployment in GCP console
5. Check Cloud Trace for telemetry

---

**Document Status:** Complete ✅
**Last Updated:** 2025-11-19
**Category:** Operations & Deployment Configuration

---
