# Bob's Brain - Terraform Infrastructure

Complete Infrastructure as Code for deploying Bob's Brain (IAM1 Regional Manager) to Google Cloud Platform.

## Overview

This Terraform configuration provisions all required GCP infrastructure for running a production-ready multi-agent system with:

- **Vertex AI Agent Engine** - Managed agent runtime
- **Vertex AI Search** - RAG knowledge retrieval
- **Cloud Functions** - Slack webhook integration
- **Workload Identity Federation** - Secure GitHub Actions authentication
- **Service Accounts** - Least-privilege IAM permissions
- **Cloud Storage** - RAG data and logs
- **GitHub Secrets** - Automated CI/CD secret management

## Prerequisites

1. **Google Cloud Project**
   ```bash
   gcloud projects create bobs-brain --name="Bob's Brain"
   gcloud config set project bobs-brain
   ```

2. **Enable Billing**
   - Link a billing account to your project in the [GCP Console](https://console.cloud.google.com/billing)

3. **Install Tools**
   ```bash
   # Terraform 1.9+
   wget https://releases.hashicorp.com/terraform/1.9.0/terraform_1.9.0_linux_amd64.zip
   unzip terraform_1.9.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/

   # Google Cloud SDK
   curl https://sdk.cloud.google.com | bash
   gcloud init
   gcloud auth application-default login
   ```

4. **GitHub Personal Access Token**
   - Create a [GitHub PAT](https://github.com/settings/tokens) with `repo` and `admin:repo_hook` scopes
   - Store securely (will be used in terraform.tfvars)

## Quick Start

### 1. Navigate to Environment Directory

```bash
cd deployment/terraform/dev
```

### 2. Create terraform.tfvars

```bash
cat > terraform.tfvars <<EOF
dev_project_id            = "bobs-brain"
dev_region                = "us-central1"
dev_location              = "us"
github_owner              = "jeremylongshore"
github_repository         = "bobs-brain"
github_token              = "ghp_YOUR_GITHUB_TOKEN_HERE"
deployment_target         = "dev"
app_service_account_name  = "bobs-brain-app"
cicd_service_account_name = "github-actions"
state_bucket_name         = "bobs-brain-terraform-state"
project_number            = "205354194989"
EOF
```

**Security Note:** Never commit `terraform.tfvars` - it's in `.gitignore`

### 3. Initialize Terraform

```bash
terraform init
```

This will:
- Download required providers (Google, GitHub, Random)
- Initialize remote state (if configured)
- Validate configuration

### 4. Plan Infrastructure

```bash
terraform plan --var-file vars/env.tfvars --var dev_project_id=bobs-brain
```

Review the plan output carefully. Terraform will show:
- Resources to be created (green +)
- Resources to be modified (yellow ~)
- Resources to be destroyed (red -)

### 5. Apply Infrastructure

```bash
terraform apply --var-file vars/env.tfvars --var dev_project_id=bobs-brain --auto-approve
```

**Note:** Remove `--auto-approve` for production deployments to manually review changes.

## Infrastructure Components

### 1. GCP APIs (apis.tf)

Enables required Google Cloud services:

```hcl
google_project_service:
  - aiplatform.googleapis.com        # Vertex AI
  - discoveryengine.googleapis.com   # Vertex AI Search
  - cloudfunctions.googleapis.com    # Cloud Functions
  - run.googleapis.com              # Cloud Run
  - secretmanager.googleapis.com     # Secret Manager
  - iam.googleapis.com              # IAM
  - iamcredentials.googleapis.com    # Workload Identity
  - cloudresourcemanager.googleapis.com
  - storage-api.googleapis.com       # GCS
  - logging.googleapis.com           # Cloud Logging
  - monitoring.googleapis.com        # Cloud Monitoring
```

**Enable Time:** ~2-5 minutes (some services take longer)

### 2. Service Accounts (service_accounts.tf)

Creates three service accounts with principle of least privilege:

#### CICD Service Account
- **Email:** `github-actions@bobs-brain.iam.gserviceaccount.com`
- **Purpose:** GitHub Actions CI/CD authentication via WIF
- **Permissions:**
  - `roles/aiplatform.user` - Deploy to Vertex AI
  - `roles/cloudfunctions.developer` - Deploy Slack webhook
  - `roles/iam.serviceAccountUser` - Impersonate other SAs
  - `roles/storage.admin` - Manage GCS buckets

#### App Service Account
- **Email:** `bobs-brain-app@bobs-brain.iam.gserviceaccount.com`
- **Purpose:** Agent Engine runtime execution
- **Permissions:**
  - `roles/aiplatform.user` - Invoke Gemini models
  - `roles/discoveryengine.editor` - Query Vertex AI Search
  - `roles/secretmanager.secretAccessor` - Read Slack secrets
  - `roles/storage.objectUser` - Read/write RAG data

#### Pipeline Service Account
- **Email:** `bobs-brain-pipeline@bobs-brain.iam.gserviceaccount.com`
- **Purpose:** Data ingestion pipeline execution
- **Permissions:**
  - `roles/aiplatform.user` - Run Vertex AI Pipelines
  - `roles/storage.admin` - Manage RAG bucket
  - `roles/discoveryengine.editor` - Update datastore

### 3. Cloud Storage (storage.tf)

Creates two GCS buckets:

#### RAG Data Bucket
```hcl
Name: bobs-brain-rag-data
Location: us-central1 (regional)
Storage Class: STANDARD
Lifecycle: Archive after 90 days, delete after 365 days
Versioning: Enabled
Public Access: Blocked
```

**Purpose:** Stores knowledge base documents for Vertex AI Search ingestion

#### Logs Bucket
```hcl
Name: bobs-brain-logs
Location: us-central1 (regional)
Storage Class: NEARLINE (cost-optimized for logs)
Lifecycle: Delete after 30 days
Versioning: Disabled
Public Access: Blocked
```

**Purpose:** Centralized logging and audit trail

### 4. Workload Identity Federation (wif.tf)

Enables keyless authentication from GitHub Actions to GCP:

```hcl
Workload Identity Pool: github-pool
Provider: github-provider
Attribute Mapping:
  - google.subject = assertion.sub
  - attribute.actor = assertion.actor
  - attribute.repository = assertion.repository
  - attribute.repository_owner = assertion.repository_owner

Service Account Binding:
  - Member: principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/jeremylongshore/bobs-brain
  - Role: roles/iam.workloadIdentityUser
```

**Security Benefits:**
- No static service account keys stored in GitHub
- Automatic token rotation
- Fine-grained access control by repository
- Auditable via Cloud Audit Logs

### 5. GitHub Secrets (github.tf)

Automatically creates GitHub repository secrets for CI/CD:

```hcl
Secrets Created:
  - GCP_PROJECT_ID          # GCP project identifier
  - GCP_REGION              # Default deployment region
  - GCP_WIF_PROVIDER        # WIF provider resource name
  - GCP_SA_EMAIL            # CICD service account email
  - AGENT_ENGINE_ID         # Vertex AI Agent Engine resource ID
```

**Access:** View in GitHub repository settings → Secrets and variables → Actions

### 6. IAM Bindings (iam.tf)

Grants permissions to service accounts:

```hcl
github-actions@bobs-brain.iam.gserviceaccount.com:
  - roles/aiplatform.user
  - roles/cloudfunctions.developer
  - roles/iam.serviceAccountUser
  - roles/storage.admin

bobs-brain-app@bobs-brain.iam.gserviceaccount.com:
  - roles/aiplatform.user
  - roles/discoveryengine.editor
  - roles/secretmanager.secretAccessor
  - roles/storage.objectUser

bobs-brain-pipeline@bobs-brain.iam.gserviceaccount.com:
  - roles/aiplatform.user
  - roles/storage.admin
  - roles/discoveryengine.editor
```

## Directory Structure

```
deployment/terraform/
├── dev/                        # Development environment
│   ├── main.tf                 # Provider configuration
│   ├── variables.tf            # Input variables
│   ├── outputs.tf              # Output values
│   ├── terraform.tfvars        # Variable values (GITIGNORED)
│   └── vars/
│       └── env.tfvars          # Environment-specific vars
│
├── apis.tf                     # GCP service API enablement
├── service_accounts.tf         # Service account definitions
├── iam.tf                      # IAM role bindings
├── storage.tf                  # GCS bucket configuration
├── wif.tf                      # Workload Identity Federation
├── github.tf                   # GitHub secrets automation
├── providers.tf                # Terraform providers (GCP, GitHub, Random)
├── versions.tf                 # Provider version constraints
└── README.md                   # This file
```

## State Management

### Local State (Default)

By default, Terraform stores state in `dev/terraform.tfstate`.

**Pros:** Simple, no extra setup
**Cons:** Not suitable for team collaboration

### Remote State (Recommended for Production)

Configure GCS backend for team collaboration:

```hcl
# dev/main.tf
terraform {
  backend "gcs" {
    bucket = "bobs-brain-terraform-state"
    prefix = "dev/state"
  }
}
```

**Pros:**
- Centralized state storage
- State locking prevents concurrent modifications
- Automatic state versioning
- Secure access control

**Setup:**
```bash
# Create state bucket (one-time)
gsutil mb -p bobs-brain -l us-central1 gs://bobs-brain-terraform-state
gsutil versioning set on gs://bobs-brain-terraform-state

# Migrate existing state
terraform init -migrate-state
```

## Common Operations

### View Current Infrastructure

```bash
terraform show
```

### List Resources

```bash
terraform state list
```

### Get Specific Resource

```bash
terraform state show google_project_service.aiplatform
```

### Import Existing Resource

```bash
terraform import google_service_account.app_sa projects/bobs-brain/serviceAccounts/bobs-brain-app@bobs-brain.iam.gserviceaccount.com
```

### Destroy Infrastructure

```bash
# Review destruction plan
terraform plan -destroy

# Execute destruction (DANGEROUS!)
terraform destroy --var-file vars/env.tfvars --var dev_project_id=bobs-brain
```

**Warning:** This will delete ALL resources managed by Terraform. Data loss is permanent.

### Update Single Resource

```bash
# Target specific resource
terraform apply -target=google_storage_bucket.rag_data
```

## Outputs

After successful `terraform apply`, view outputs:

```bash
terraform output
```

**Available Outputs:**
- `project_id` - GCP project identifier
- `region` - Default deployment region
- `app_service_account_email` - App runtime SA
- `cicd_service_account_email` - GitHub Actions SA
- `rag_bucket_name` - RAG data bucket
- `logs_bucket_name` - Logs bucket
- `workload_identity_provider` - WIF provider resource name

**Use in Scripts:**
```bash
export GCP_PROJECT_ID=$(terraform output -raw project_id)
export WIF_PROVIDER=$(terraform output -raw workload_identity_provider)
```

## Cost Estimation

**Monthly Infrastructure Costs (Approximate):**

| Resource | Cost | Notes |
|----------|------|-------|
| Vertex AI Agent Engine | $0-100 | Based on query volume |
| Vertex AI Search | $30-200 | Based on documents + queries |
| Cloud Functions (Slack) | $0-10 | Usually within free tier |
| Cloud Storage (RAG data) | $1-5 | Standard storage |
| Cloud Storage (Logs) | $0.50-2 | Nearline storage |
| Secret Manager | $0.10-1 | Per secret, per month |
| **Total** | **$32-318/month** | Varies with usage |

**Cost Optimization Tips:**
1. Use Vertex AI Search sparingly in development
2. Set lifecycle policies on GCS buckets
3. Archive old logs to Coldline/Archive storage
4. Monitor query volumes with Cloud Monitoring
5. Use committed use discounts for production

## Security Best Practices

### 1. Secrets Management

- Store Slack secrets in Secret Manager (never in code)
- Use Workload Identity Federation (no static keys)
- Rotate secrets regularly
- Enable Secret Manager audit logging

### 2. IAM

- Follow principle of least privilege
- Use custom roles for fine-grained permissions
- Regular access reviews (quarterly recommended)
- Enable Cloud Audit Logs for all IAM changes

### 3. Network Security

- Deploy Cloud Functions with VPC connector (production)
- Use Private Google Access for GCS
- Enable VPC Service Controls (enterprise)
- Restrict public bucket access

### 4. Data Protection

- Enable GCS object versioning
- Configure bucket lifecycle policies
- Regular backups of critical data
- Encryption at rest (default) + in transit (HTTPS)

## Troubleshooting

### API Not Enabled Error

```
Error: Error creating service account: googleapi: Error 403: <SERVICE>.googleapis.com is not enabled
```

**Solution:** Wait 2-5 minutes after `terraform apply` for APIs to fully enable, then retry.

### Permission Denied Error

```
Error: Error creating bucket: googleapi: Error 403: <USER> does not have storage.buckets.create access
```

**Solution:** Ensure you have `Owner` or `Editor` role on the project:
```bash
gcloud projects add-iam-policy-binding bobs-brain \
  --member="user:YOUR_EMAIL" \
  --role="roles/owner"
```

### GitHub Token Expired

```
Error: Error creating repository secret: PUT https://api.github.com/repos/.../actions/secrets/...: 401
```

**Solution:** Generate new GitHub PAT and update `terraform.tfvars`

### State Lock Error

```
Error: Error acquiring the state lock
```

**Solution:** Wait for concurrent operation to complete or force-unlock (use with caution):
```bash
terraform force-unlock <LOCK_ID>
```

## CI/CD Integration

GitHub Actions workflows automatically use Terraform-managed infrastructure:

### Staging Deployment (.github/workflows/staging.yaml)

```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ secrets.GCP_WIF_PROVIDER }}
    service_account: ${{ secrets.GCP_SA_EMAIL }}
```

### Production Deployment (.github/workflows/deploy-to-prod.yaml)

Same authentication, different Agent Engine target.

## Maintenance

### Regular Tasks

- **Weekly:** Review Cloud Logging for errors
- **Monthly:** Review IAM permissions, rotate secrets
- **Quarterly:** Cost optimization review, update Terraform providers
- **Annually:** Disaster recovery drill, security audit

### Provider Updates

```bash
# Check for updates
terraform providers lock -platform=linux_amd64 -platform=darwin_amd64

# Update to latest versions
terraform init -upgrade
```

### Backup State

```bash
# Local state backup
cp terraform.tfstate terraform.tfstate.backup

# Remote state backup (GCS)
gsutil cp gs://bobs-brain-terraform-state/dev/state/default.tfstate ./backup/
```

## Support

- **Terraform Docs:** https://registry.terraform.io/providers/hashicorp/google/latest/docs
- **GCP Documentation:** https://cloud.google.com/docs
- **GitHub Issues:** https://github.com/jeremylongshore/bobs-brain/issues

---

**Last Updated:** 2025-11-10
**Terraform Version:** >= 1.9.0
**Google Provider:** ~> 6.0
