# Task List: Terraform Migration

**PRD:** `054-prd-terraform-infrastructure-migration.md`
**Status:** Phase 2 Complete - Ready for Implementation
**Sprint Timeline:** Oct 7 - Nov 15 (3 sprints, 60 SP total)
**Total Tasks:** 5 parent tasks, 47 sub-tasks

---

## Relevant Files

**Existing Terraform Research (to be moved/updated):**
- `08-features/09-terraform-research/main.tf` - Root module with API enablement, module calls (needs production values)
- `08-features/09-terraform-research/backend.tf` - GCS state backend configuration (production-ready)
- `08-features/09-terraform-research/versions.tf` - Terraform and provider version constraints
- `08-features/09-terraform-research/variables.tf` - Input variables (environment, region, project_id)
- `08-features/09-terraform-research/outputs.tf` - Output values (service URLs, bucket names)
- `08-features/09-terraform-research/providers.tf` - Google provider configuration

**Existing Terraform Modules (to be validated/updated):**
- `08-features/09-terraform-research/modules/cloud-run/main.tf` - Cloud Run service resource
- `08-features/09-terraform-research/modules/cloud-run/variables.tf` - Module input variables
- `08-features/09-terraform-research/modules/cloud-run/outputs.tf` - Module outputs (service URL)
- `08-features/09-terraform-research/modules/iam/main.tf` - Service accounts and IAM role bindings
- `08-features/09-terraform-research/modules/iam/variables.tf` - IAM module inputs
- `08-features/09-terraform-research/modules/iam/outputs.tf` - Service account emails
- `08-features/09-terraform-research/modules/firestore/main.tf` - Firestore database (needs composite indexes)
- `08-features/09-terraform-research/modules/storage/main.tf` - Cloud Storage buckets with lifecycle rules

**New Files to Create:**
- `terraform/` - Production Terraform directory (move from 08-features/09-terraform-research/)
- `terraform/modules/secret-manager/main.tf` - Secret Manager secret metadata module
- `terraform/modules/secret-manager/variables.tf` - Secret module inputs (secret_id, rotation_policy)
- `terraform/modules/secret-manager/outputs.tf` - Secret names for reference
- `terraform/modules/api-gateway/main.tf` - API Gateway configuration (from research, needs validation)
- `terraform/environments/prod/main.tf` - Production environment configuration
- `terraform/environments/prod/terraform.tfvars` - Production variable values
- `.github/workflows/terraform.yml` - CI/CD pipeline for terraform plan/apply
- `docs/terraform/README.md` - Auto-generated documentation (terraform-docs)
- `docs/terraform/disaster-recovery-runbook.md` - DR procedures and testing

**Integration Points:**
- `02-src/backend/services/backend/secrets.js` - Backend Secret Manager integration (must work with Terraform-managed secrets)
- `.github/workflows/backend-deploy.yml` - Backend deployment workflow (update to use Terraform-managed Cloud Run)
- `.github/workflows/frontend-deploy.yml` - Frontend deployment workflow (update to use Terraform-managed Firebase Hosting)

### Notes

- Terraform state will be stored in existing GCS bucket: `diagnostic-pro-prod-terraform-state`
- All resources will be imported (NOT recreated) to avoid production downtime
- Modules from `08-features/09-terraform-research/` will be moved to `terraform/modules/` and validated
- Use `terraform plan` before every `terraform apply` to validate changes
- Run `tfsec` security scanning before committing Terraform code

---

## Tasks

- [ ] **1.0 Project Setup & Module Migration**
  - [ ] 1.1 Create production Terraform directory structure (`terraform/`, `terraform/modules/`, `terraform/environments/prod/`)
  - [ ] 1.2 Move existing research modules from `08-features/09-terraform-research/modules/` to `terraform/modules/`
  - [ ] 1.3 Copy root Terraform files (`backend.tf`, `versions.tf`, `providers.tf`) to `terraform/` directory
  - [ ] 1.4 Update `backend.tf` to ensure GCS bucket `diagnostic-pro-prod-terraform-state` is configured correctly
  - [ ] 1.5 Run `terraform init` to initialize backend and download providers
  - [ ] 1.6 Validate all modules with `terraform validate` in each module directory
  - [ ] 1.7 Run `tfsec terraform/` to identify security issues in modules
  - [ ] 1.8 Fix any security issues flagged by tfsec (no high/critical issues allowed)

- [ ] **2.0 Cloud Run Services Migration (Import Existing)**
  - [ ] 2.1 Create `terraform/environments/prod/main.tf` with module calls for 3 Cloud Run services
  - [ ] 2.2 Create `terraform/environments/prod/terraform.tfvars` with production values (project_id, region, service names)
  - [ ] 2.3 Import `diagnosticpro-vertex-ai-backend` service: `terraform import module.vertex_ai_backend.google_cloud_run_service.main projects/diagnostic-pro-prod/locations/us-central1/services/diagnosticpro-vertex-ai-backend`
  - [ ] 2.4 Import `diagnosticpro-stripe-webhook` service: `terraform import module.stripe_webhook.google_cloud_run_service.main projects/diagnostic-pro-prod/locations/us-central1/services/diagnosticpro-stripe-webhook`
  - [ ] 2.5 Import `simple-diagnosticpro` service: `terraform import module.simple_diagnosticpro.google_cloud_run_service.main projects/diagnostic-pro-prod/locations/us-central1/services/simple-diagnosticpro`
  - [ ] 2.6 Run `terraform plan` and verify 0 changes (state matches reality)
  - [ ] 2.7 Test backend service health endpoint: `curl https://diagnosticpro-vertex-ai-backend-<hash>.run.app/healthz`
  - [ ] 2.8 Document Cloud Run module usage in `terraform/modules/cloud-run/README.md` (use terraform-docs)

- [ ] **3.0 Firestore, Secrets, and Storage Migration**
  - [ ] 3.1 Create Secret Manager module: `terraform/modules/secret-manager/main.tf` (manages metadata only, NOT values)
  - [ ] 3.2 Add 8 Secret Manager secrets to `terraform/environments/prod/main.tf` (stripe-secret, stripe-webhook-secret, vertex-ai-api-key, gmail-app-password, firebase-admin-sdk, firestore-service-account, github-webhook-secret, slack-webhook-url)
  - [ ] 3.3 Import all 8 secrets: `terraform import module.stripe_secret.google_secret_manager_secret.main projects/diagnostic-pro-prod/secrets/stripe-secret`
  - [ ] 3.4 Configure 90-day rotation policy for stripe-secret and stripe-webhook-secret
  - [ ] 3.5 Add Firestore database to `terraform/environments/prod/main.tf` using firestore module
  - [ ] 3.6 Import Firestore database: `terraform import module.firestore.google_firestore_database.main projects/diagnostic-pro-prod/databases/(default)`
  - [ ] 3.7 Define 4 composite indexes in Firestore module (diagnosticSubmissions, orders, emailLogs queries)
  - [ ] 3.8 Add 3 Cloud Storage buckets to `terraform/environments/prod/main.tf` (diagnostic-pro-prod-reports-us-central1, diagnostic-pro-prod-frontend, diagnostic-pro-terraform-state)
  - [ ] 3.9 Import all 3 buckets: `terraform import module.reports_bucket.google_storage_bucket.main diagnostic-pro-prod-reports-us-central1`
  - [ ] 3.10 Configure 30-day lifecycle rule for reports bucket
  - [ ] 3.11 Run `terraform plan` and verify 0 changes
  - [ ] 3.12 Verify backend `secrets.js` still works with Terraform-managed secrets (test Secret Manager access)

- [ ] **4.0 IAM, Networking, and API Gateway Migration**
  - [ ] 4.1 Add 12 service accounts to `terraform/environments/prod/main.tf` using IAM module (diagnosticpro-vertex-ai-backend-sa, terraform-automation-sa, github-actions-sa, etc.)
  - [ ] 4.2 Import all 12 service accounts: `terraform import module.backend_sa.google_service_account.main projects/diagnostic-pro-prod/serviceAccounts/diagnosticpro-vertex-ai-backend-sa@diagnostic-pro-prod.iam.gserviceaccount.com`
  - [ ] 4.3 Define IAM role bindings for each service account (Secret Manager accessor, Cloud Run invoker, Firestore user, etc.)
  - [ ] 4.4 Import IAM role bindings: `terraform import module.backend_sa.google_project_iam_member.roles["secretmanager.secretAccessor"] "diagnostic-pro-prod roles/secretmanager.secretAccessor serviceAccount:diagnosticpro-vertex-ai-backend-sa@diagnostic-pro-prod.iam.gserviceaccount.com"`
  - [ ] 4.5 Add VPC networking resources (default VPC, Cloud NAT, firewall rules)
  - [ ] 4.6 Import VPC: `terraform import google_compute_network.default projects/diagnostic-pro-prod/global/networks/default`
  - [ ] 4.7 Add API Gateway configuration to `terraform/environments/prod/main.tf` (diagpro-gw-3tbssksx)
  - [ ] 4.8 Import API Gateway: `terraform import module.api_gateway.google_api_gateway_gateway.main projects/diagnostic-pro-prod/locations/us-central1/gateways/diagpro-gw-3tbssksx`
  - [ ] 4.9 Run `terraform plan` and verify 0 changes
  - [ ] 4.10 Test API Gateway webhook endpoint: `curl https://diagpro-gw-3tbssksx-3tbssksx.uc.gateway.dev/healthz`

- [ ] **5.0 CI/CD Integration & Disaster Recovery**
  - [ ] 5.1 Create `.github/workflows/terraform.yml` with terraform plan on PR and terraform apply on merge
  - [ ] 5.2 Configure GitHub Actions secrets (GOOGLE_CREDENTIALS with terraform-automation-sa key JSON)
  - [ ] 5.3 Add terraform plan comment to PR (use hashicorp/setup-terraform action)
  - [ ] 5.4 Add manual approval gate for terraform apply (environment protection rules)
  - [ ] 5.5 Test CI/CD: Create PR with terraform comment change, verify plan output in PR comment
  - [ ] 5.6 Create disaster recovery runbook: `01-docs/059-gde-terraform-disaster-recovery.md`
  - [ ] 5.7 Document full infrastructure rebuild procedure: `terraform destroy && terraform apply`
  - [ ] 5.8 Test disaster recovery in dev environment (if available) or document-only for production
  - [ ] 5.9 Auto-generate infrastructure documentation: Run `terraform-docs markdown table terraform/modules/cloud-run > terraform/modules/cloud-run/README.md`
  - [ ] 5.10 Create monthly disaster recovery test reminder (calendar event or cron job)
  - [ ] 5.11 Update `046-ref-claude-code-guide.md` (CLAUDE.md) with Terraform workflow documentation
  - [ ] 5.12 Tag Terraform v1.0 release: `git tag terraform-v1.0 && git push origin terraform-v1.0`

---

## Phase 2 Complete: Detailed Sub-Tasks Generated

**Total Sub-Tasks:** 47 actionable items across 5 parent tasks

**Sprint 1 (Oct 7-18, 30 SP):** Tasks 1.0 (8 sub-tasks) + 2.0 (8 sub-tasks) = 16 sub-tasks
**Sprint 2 (Oct 21-Nov 1, 18 SP):** Tasks 3.0 (12 sub-tasks) = 12 sub-tasks
**Sprint 3 (Nov 4-15, 12 SP):** Tasks 4.0 (10 sub-tasks) + 5.0 (12 sub-tasks) = 22 sub-tasks

**Critical Path:**
1. Setup → Cloud Run import → Validate zero drift
2. Secrets → Storage → Firestore import
3. IAM → Networking → API Gateway import
4. CI/CD → DR testing → Documentation

**Next Steps:**
1. Start with Task 1.1 (create directory structure)
2. After completing each sub-task, mark it `[x]`
3. Run `terraform plan` after each import to verify zero drift
4. Commit after completing each parent task (1.0, 2.0, 3.0, 4.0, 5.0)

**Remember:** Ask for permission before starting each parent task! Only work on one sub-task at a time.
