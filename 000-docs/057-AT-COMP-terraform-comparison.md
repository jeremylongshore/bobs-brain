# Terraform Comparison - Google Notebook vs Bob's Brain

**Date:** 2025-11-11
**Category:** 057-AT-COMP (Architecture Technical Comparison)
**Status:** Analysis

---

## Current State

### What We Have ✅
- `infra/` directory created
- `infra/README.md` with placeholder
- Dockerfile ready for Agent Engine deployment
- my_agent/ code ready to deploy

### What We DON'T Have Yet ❌
- No Terraform files (`.tf`)
- No variable definitions
- No provider configuration
- No Agent Engine resource definitions

---

## Google Notebook Pattern Analysis

**Source:** `tutorial_get_started_with_agent_engine_terraform_deployment.ipynb`

### Key Resources Used:

1. **Terraform Provider**
   ```hcl
   terraform {
     required_providers {
       google = {
         source  = "hashicorp/google"
         version = "7.6.0"
       }
     }
   }
   ```

2. **GCS Bucket** (for agent code storage)
   ```hcl
   resource "google_storage_bucket" "bucket" {
     name                        = var.gcs_bucket_name
     location                    = var.region
     uniform_bucket_level_access = true
     force_destroy               = true
   }
   ```

3. **Upload Agent Files to GCS**
   ```hcl
   resource "google_storage_bucket_object" "bucket_obj_requirements_txt" {
     name    = "requirements.txt"
     bucket  = google_storage_bucket.bucket.id
     source  = "./requirements.txt"
   }
   ```

4. **Vertex AI Reasoning Engine** (Agent Engine)
   ```hcl
   resource "google_vertex_ai_reasoning_engine" "agent_engine" {
     # Agent Engine configuration
   }
   ```

---

## Bob's Brain Requirements (Hard Mode)

### R4: CI-Only Deployments
- ❌ Notebook uses manual `terraform apply`
- ✅ Bob's Brain: Must use GitHub Actions + WIF

### R2: Vertex AI Agent Engine Runtime
- ✅ Notebook uses `google_vertex_ai_reasoning_engine`
- ✅ Bob's Brain: Same resource needed

### Docker Container Approach
- ⚠️ Notebook uploads code to GCS directly
- ✅ Bob's Brain: Uses Docker container (better for Hard Mode)

---

## What Bob's Brain Needs

### Directory Structure:
```
infra/
├── terraform/
│   ├── main.tf                    # Main resources
│   ├── variables.tf               # Variable definitions
│   ├── outputs.tf                 # Output values
│   ├── provider.tf                # Google Cloud provider config
│   ├── agent_engine.tf            # Vertex AI Agent Engine resource
│   ├── storage.tf                 # GCS buckets (if needed)
│   ├── iam.tf                     # Service accounts, IAM bindings
│   ├── cloud_run.tf               # Gateways (A2A + Slack)
│   └── envs/
│       ├── dev.tfvars             # Dev environment
│       ├── staging.tfvars         # Staging environment
│       └── prod.tfvars            # Production environment
```

### Core Resources Needed:

1. **Provider Configuration** (`provider.tf`)
   - Google Cloud provider
   - Project ID, region
   - Workload Identity Federation credentials (for CI)

2. **Agent Engine** (`agent_engine.tf`)
   - `google_vertex_ai_reasoning_engine` resource
   - Docker container image reference
   - Compute resources (CPU, memory)
   - Environment variables (PROJECT_ID, AGENT_SPIFFE_ID, etc.)

3. **IAM** (`iam.tf`)
   - Service account for Agent Engine
   - Service account for GitHub Actions (WIF)
   - IAM bindings for Agent Engine to access services

4. **Cloud Run Gateways** (`cloud_run.tf`)
   - A2A gateway service
   - Slack webhook service
   - Both configured to call Agent Engine via REST (R3 compliance)

5. **Storage** (`storage.tf`) - Optional
   - GCS bucket for agent artifacts
   - Or rely on Container Registry for Docker images

---

## Key Differences: Notebook vs Hard Mode

| Aspect | Google Notebook | Bob's Brain Hard Mode |
|--------|-----------------|----------------------|
| **Deployment Method** | Manual `terraform apply` | GitHub Actions + WIF (R4) |
| **Agent Packaging** | Upload code to GCS | Docker container (R2) |
| **Runtime** | Reasoning Engine | Vertex AI Agent Engine |
| **Gateways** | Not covered | Cloud Run proxies (R3) |
| **Drift Detection** | Not covered | CI scans Terraform (R8) |
| **Environment Management** | Single config | Dev/staging/prod tfvars |
| **State Management** | Local state | GCS backend (recommended) |

---

## Next Steps (Phase 4)

### 1. Create Terraform Structure ⏳
```bash
mkdir -p infra/terraform/envs
touch infra/terraform/{main,variables,outputs,provider,agent_engine,iam,cloud_run}.tf
touch infra/terraform/envs/{dev,staging,prod}.tfvars
```

### 2. Implement Core Resources ⏳
- Provider configuration with WIF support
- Agent Engine resource pointing to Docker image
- Service accounts and IAM bindings
- Cloud Run gateways (Phase 3 code deployed)

### 3. Configure Environments ⏳
- Dev: bobs-brain-dev project
- Staging: bobs-brain-staging project
- Prod: bobs-brain project

### 4. Add GitHub Actions Workflow ⏳
- Terraform plan on PR
- Terraform apply on merge to main
- WIF authentication (no service account keys)

### 5. Drift Detection Integration ⏳
- Add Terraform validation to CI
- Scan for manual changes outside Terraform
- Block deployments if drift detected

---

## Implementation Priority

### Phase 3 (NOW) - Service Gateways
Before Terraform, we need the gateway code:
1. Create `service/a2a_gateway/` (FastAPI proxy)
2. Create `service/slack_webhook/` (Slack event handler)
3. Both must call Agent Engine REST API (R3)
4. Write tests for gateways

### Phase 4 (AFTER Phase 3) - Terraform Infrastructure
Once gateways exist:
1. Write Terraform to deploy Agent Engine
2. Write Terraform to deploy Cloud Run gateways
3. Configure GitHub Actions for CI/CD
4. Test end-to-end deployment

---

## Comparison Summary

**Google Notebook Approach:**
- ✅ Good starting point for basic Agent Engine
- ✅ Shows core Terraform resources needed
- ❌ Not production-ready (manual deploys)
- ❌ Missing CI/CD integration
- ❌ Missing gateway patterns

**Bob's Brain Hard Mode:**
- ✅ CI-only deploys (R4)
- ✅ Docker containers (R2)
- ✅ Gateway separation (R3)
- ✅ Drift detection (R8)
- ✅ Multi-environment support
- ⏳ Needs Phase 3 first (gateways)
- ⏳ Then Phase 4 (Terraform)

---

## Recommendation

**DO Phase 3 FIRST** (service/ gateways), **THEN** Phase 4 (Terraform).

Why?
1. Terraform deploys what exists (gateways don't exist yet)
2. Can't test end-to-end without gateways
3. Gateway code informs Terraform configuration

**After Phase 3 completes:**
- Use notebook as reference for Agent Engine resource
- Adapt to Docker container approach
- Add Cloud Run gateway resources
- Integrate with GitHub Actions + WIF

---

**Status:** Ready to start Phase 3 (service/ gateways)
**Next Action:** Create A2A gateway FastAPI proxy

**Last Updated:** 2025-11-11
