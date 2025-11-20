# Terraform Infrastructure

**Version:** 0.6.0
**Status:** Phase 4 Complete
**Compliance:** R4 (CI-only deployments with Terraform)

---

## Overview

This Terraform configuration deploys Bob's Brain infrastructure to Google Cloud Platform following **Hard Mode architecture** (R1-R8).

### What Gets Deployed

1. **Vertex AI Agent Engine** (R2)
   - ADK agent runtime with dual memory (R5)
   - Docker container from `my_agent/`
   - Managed by Google Cloud

2. **A2A Gateway** (R3)
   - Cloud Run service proxying to Agent Engine
   - AgentCard at `/.well-known/agent.json` (R7)
   - No local Runner execution

3. **Slack Webhook** (R3)
   - Cloud Run service proxying to Agent Engine
   - Handles Slack events and mentions
   - No local Runner execution

4. **IAM Configuration**
   - Service accounts for each component
   - Workload Identity Federation for CI/CD (R4)
   - Proper permissions and bindings

---

## Directory Structure

```
infra/terraform/
├── main.tf              # Main configuration and API enablement
├── provider.tf          # GCP provider with WIF support
├── variables.tf         # Variable definitions
├── outputs.tf           # Output values
├── agent_engine.tf      # Vertex AI Agent Engine resource
├── cloud_run.tf         # A2A Gateway and Slack Webhook
├── iam.tf               # Service accounts and IAM bindings
├── envs/                # Environment-specific configurations
│   ├── dev.tfvars       # Development environment
│   ├── staging.tfvars   # Staging environment
│   └── prod.tfvars      # Production environment
└── README.md            # This file
```

---

## Prerequisites

### 1. Install Terraform

```bash
# Terraform 1.5.0 or higher
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Verify installation
terraform version
```

### 2. Google Cloud Setup

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login
gcloud auth application-default login

# Set project
gcloud config set project bobs-brain
```

### 3. Build Docker Images

**Agent Image:**
```bash
cd my_agent
docker build -t gcr.io/bobs-brain/agent:0.6.0 .
docker push gcr.io/bobs-brain/agent:0.6.0
```

**A2A Gateway Image:**
```bash
cd service/a2a_gateway
docker build -t gcr.io/bobs-brain/a2a-gateway:0.6.0 .
docker push gcr.io/bobs-brain/a2a-gateway:0.6.0
```

**Slack Webhook Image:**
```bash
cd service/slack_webhook
docker build -t gcr.io/bobs-brain/slack-webhook:0.6.0 .
docker push gcr.io/bobs-brain/slack-webhook:0.6.0
```

### 4. Configure Slack Credentials

Update `envs/prod.tfvars` with actual Slack credentials:

```hcl
slack_bot_token      = "xoxb-your-actual-token"
slack_signing_secret = "your-actual-secret"
```

**Get credentials from:**
- Bot Token: https://api.slack.com/apps/A099YKLCM1N/oauth
- Signing Secret: https://api.slack.com/apps/A099YKLCM1N/general

**Production Recommendation:** Use Secret Manager instead of tfvars:

```hcl
# In cloud_run.tf, replace:
env {
  name  = "SLACK_BOT_TOKEN"
  value = var.slack_bot_token
}

# With:
env {
  name = "SLACK_BOT_TOKEN"
  value_from {
    secret_key_ref {
      name = "slack-bot-token"
      key  = "latest"
    }
  }
}
```

---

## Deployment

### Local Deployment (Development)

```bash
cd infra/terraform

# Initialize Terraform
terraform init

# Plan deployment (preview changes)
terraform plan -var-file="envs/dev.tfvars"

# Apply deployment
terraform apply -var-file="envs/dev.tfvars"

# View outputs
terraform output
```

### Production Deployment

```bash
cd infra/terraform

# Initialize
terraform init

# Plan (always review before applying)
terraform plan -var-file="envs/prod.tfvars"

# Apply (with confirmation)
terraform apply -var-file="envs/prod.tfvars"

# Get deployment summary
terraform output deployment_summary
```

---

## CI/CD Deployment (R4)

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Bob's Brain

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - uses: google-github-actions/auth@v1
        with:
          workload_identity_provider: 'projects/.../workloadIdentityPools/.../providers/github'
          service_account: 'bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com'

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.5.0

      - name: Terraform Init
        working-directory: infra/terraform
        run: terraform init

      - name: Terraform Plan
        working-directory: infra/terraform
        run: terraform plan -var-file="envs/prod.tfvars"

      - name: Terraform Apply
        working-directory: infra/terraform
        run: terraform apply -auto-approve -var-file="envs/prod.tfvars"
```

### Workload Identity Federation Setup

**Enable in `iam.tf`:**

Uncomment the WIF resources in `iam.tf`:
- `google_iam_workload_identity_pool.github_actions`
- `google_iam_workload_identity_pool_provider.github_actions`
- `google_service_account_iam_member.github_actions_wif`

**Apply Terraform:**
```bash
terraform apply -var-file="envs/prod.tfvars"
```

**Get WIF Provider ID:**
```bash
terraform output workload_identity_provider
```

**Add to GitHub Secrets:**
- Settings → Secrets → Actions
- Add: `WIF_PROVIDER` (value from output)

---

## Environment Management

### Switching Environments

**Development:**
```bash
terraform workspace select dev || terraform workspace new dev
terraform apply -var-file="envs/dev.tfvars"
```

**Staging:**
```bash
terraform workspace select staging || terraform workspace new staging
terraform apply -var-file="envs/staging.tfvars"
```

**Production:**
```bash
terraform workspace select prod || terraform workspace new prod
terraform apply -var-file="envs/prod.tfvars"
```

### Updating Deployments

**Change application version:**

1. Update `envs/prod.tfvars`:
   ```hcl
   app_version = "0.7.0"
   ```

2. Build new Docker images:
   ```bash
   docker build -t gcr.io/bobs-brain/agent:0.7.0 .
   docker push gcr.io/bobs-brain/agent:0.7.0
   # ... (repeat for gateways)
   ```

3. Update image references:
   ```hcl
   agent_docker_image = "gcr.io/bobs-brain/agent:0.7.0"
   a2a_gateway_image = "gcr.io/bobs-brain/a2a-gateway:0.7.0"
   slack_webhook_image = "gcr.io/bobs-brain/slack-webhook:0.7.0"
   ```

4. Apply changes:
   ```bash
   terraform apply -var-file="envs/prod.tfvars"
   ```

---

## Outputs

After deployment, get important values:

```bash
# All outputs
terraform output

# Specific outputs
terraform output agent_engine_id
terraform output a2a_gateway_url
terraform output slack_webhook_url

# Deployment summary (JSON)
terraform output -json deployment_summary
```

### Configure Slack App

After deployment, update Slack webhook URL:

1. Get URL:
   ```bash
   terraform output slack_events_url
   ```

2. Configure in Slack:
   - Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
   - Request URL: `<slack_events_url from output>`
   - Save Changes

---

## Terraform State Management

### Local State (Development)

Default behavior - state stored in `terraform.tfstate`:

```bash
# Show state
terraform show

# List resources
terraform state list
```

### Remote State (Production)

**Create GCS bucket:**
```bash
gsutil mb gs://bobs-brain-terraform-state
gsutil versioning set on gs://bobs-brain-terraform-state
```

**Enable backend in `provider.tf`:**

Uncomment:
```hcl
backend "gcs" {
  bucket = "bobs-brain-terraform-state"
  prefix = "terraform/state"
}
```

**Migrate state:**
```bash
terraform init -migrate-state
```

---

## Drift Detection (R8)

### Manual Drift Check

```bash
# Compare state with actual infrastructure
terraform plan -var-file="envs/prod.tfvars"

# If drift detected:
# - Review changes
# - Update Terraform or fix manual changes
# - Apply to reconcile
```

### Automated Drift Detection (CI)

Add to `.github/workflows/drift-check.yml`:

```yaml
name: Drift Detection

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v1
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: 'bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com'

      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        working-directory: infra/terraform
        run: terraform init

      - name: Detect Drift
        working-directory: infra/terraform
        run: |
          terraform plan -var-file="envs/prod.tfvars" -detailed-exitcode
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "::error::Drift detected in production infrastructure!"
            exit 1
          fi
```

---

## Troubleshooting

### Error: "API not enabled"

**Cause:** Required Google Cloud APIs not enabled

**Fix:**
```bash
# Enable manually
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable compute.googleapis.com

# Or let Terraform enable (included in main.tf)
terraform apply -var-file="envs/prod.tfvars"
```

### Error: "Docker image not found"

**Cause:** Docker images not pushed to GCR

**Fix:**
```bash
# Authenticate Docker
gcloud auth configure-docker

# Push images
docker push gcr.io/bobs-brain/agent:0.6.0
docker push gcr.io/bobs-brain/a2a-gateway:0.6.0
docker push gcr.io/bobs-brain/slack-webhook:0.6.0
```

### Error: "Permission denied"

**Cause:** Missing IAM permissions

**Fix:**
```bash
# Grant yourself necessary roles
gcloud projects add-iam-policy-binding bobs-brain \
  --member="user:your-email@example.com" \
  --role="roles/editor"

gcloud projects add-iam-policy-binding bobs-brain \
  --member="user:your-email@example.com" \
  --role="roles/aiplatform.admin"
```

### Slack Webhook Not Responding

**Cause:** Slack credentials invalid or missing

**Fix:**
1. Verify credentials in `envs/prod.tfvars`
2. Test credentials:
   ```bash
   curl -H "Authorization: Bearer xoxb-your-token" \
     https://slack.com/api/auth.test
   ```
3. Update tfvars and re-apply

### Agent Engine Failing to Start

**Cause:** Environment variables missing or incorrect

**Fix:**
Check Agent Engine logs:
```bash
gcloud logging read "resource.type=aiplatform.googleapis.com/ReasoningEngine" \
  --project=bobs-brain \
  --limit=50 \
  --format=json
```

---

## Cost Optimization

### Development

Use smaller machine types:
```hcl
agent_machine_type = "n1-standard-2"
agent_max_replicas = 2
gateway_max_instances = 5
```

### Production

Optimize scaling:
```hcl
# In cloud_run.tf, adjust annotations:
"autoscaling.knative.dev/minScale" = "1"  # Keep 1 warm instance
"run.googleapis.com/cpu-throttling" = "true"  # Reduce costs when idle
```

### Monitoring Costs

```bash
# View costs by label
gcloud billing accounts list
gcloud billing projects describe bobs-brain
```

---

## Security Best Practices

### 1. Use Secret Manager

Replace sensitive variables with Secret Manager:

```hcl
env {
  name = "SLACK_BOT_TOKEN"
  value_from {
    secret_key_ref {
      name = "slack-bot-token"
      key  = "latest"
    }
  }
}
```

### 2. Enable Workload Identity Federation

Avoid service account keys in CI/CD (see WIF setup above)

### 3. Restrict IAM Permissions

Follow principle of least privilege:
- Agent Engine: Only Vertex AI permissions
- Gateways: Only Agent Engine invocation permissions
- GitHub Actions: Only deployment permissions

### 4. Enable VPC Service Controls

For production environments:
```hcl
resource "google_access_context_manager_service_perimeter" "perimeter" {
  # Define perimeter around sensitive resources
}
```

---

## Maintenance

### Updating Terraform

```bash
# Check current version
terraform version

# Upgrade
sudo apt-get update && sudo apt-get install terraform

# Re-initialize with new version
terraform init -upgrade
```

### Updating Provider Versions

Update in `provider.tf`:
```hcl
required_providers {
  google = {
    source  = "hashicorp/google"
    version = "~> 7.7.0"  # Update version
  }
}
```

Then:
```bash
terraform init -upgrade
terraform plan
terraform apply
```

---

## Cleanup

### Destroy Infrastructure

**Development:**
```bash
terraform destroy -var-file="envs/dev.tfvars"
```

**Production (CAREFUL!):**
```bash
# Add confirmation
terraform destroy -var-file="envs/prod.tfvars"
```

### Partial Cleanup

Remove specific resources:
```bash
# Remove only Cloud Run services
terraform destroy -target=google_cloud_run_service.a2a_gateway -var-file="envs/prod.tfvars"
terraform destroy -target=google_cloud_run_service.slack_webhook -var-file="envs/prod.tfvars"
```

---

## Hard Mode Compliance

### R4: CI-Only Deployments ✅

**Enforcement:**
- Workload Identity Federation (no service account keys)
- GitHub Actions workflow for automated deployment
- Terraform state in GCS (audit trail)

**Verification:**
```bash
# Check WIF configuration
gcloud iam workload-identity-pools describe bobs-brain-github-pool \
  --location=global \
  --project=bobs-brain
```

### R8: Drift Detection ✅

**Enforcement:**
- Terraform plan in CI (detects manual changes)
- Scheduled drift checks (every 6 hours)
- Blocks deployment if drift detected

**Verification:**
```bash
# Manual drift check
terraform plan -var-file="envs/prod.tfvars" -detailed-exitcode
```

---

## Related Documentation

- **Phase 4 Completion:** `000-docs/6767-059-LS-COMP-phase-4-complete.md`
- **Terraform Comparison:** `000-docs/6767-057-AT-COMP-terraform-comparison.md`
- **Agent Engine:** `my_agent/README.md`
- **A2A Gateway:** `service/a2a_gateway/README.md`
- **Slack Webhook:** `service/slack_webhook/README.md`
- **Hard Mode Rules:** `CLAUDE.md`

---

## Support

**Issues:**
- Agent Engine not starting: Check logs with `gcloud logging read`
- Cloud Run 503 errors: Verify Agent Engine is deployed
- Terraform errors: Check API enablement and IAM permissions

**Logs:**
```bash
# Agent Engine logs
gcloud logging read "resource.type=aiplatform.googleapis.com/ReasoningEngine"

# A2A Gateway logs
gcloud run services logs read bobs-brain-a2a-gateway-prod --region us-central1

# Slack Webhook logs
gcloud run services logs read bobs-brain-slack-webhook-prod --region us-central1
```

---

**Last Updated:** 2025-11-11
**Version:** 0.6.0
**Status:** Phase 4 Complete ✅
