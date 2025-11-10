# Product Requirements Document (PRD)

**Feature:** DiagnosticPro Infrastructure Migration to Terraform
**Version:** 1.0
**Status:** Approved
**Created:** 2025-10-06
**Owner:** DevOps Team (Sarah Chen, David Kim, Alex Martinez)

---

## 1. Introduction/Overview

**Problem Statement:**
DiagnosticPro's production infrastructure (`diagnostic-pro-prod`) is currently managed manually through the Google Cloud Console, creating significant operational risks including configuration drift, lack of disaster recovery capability, knowledge silos, and inability to version control infrastructure changes. With the platform serving $4.99 diagnostics to customers, infrastructure reliability is critical.

**Feature Goal:**
Convert DiagnosticPro's manual GCP infrastructure into versioned, reproducible Infrastructure as Code (IaC) using Terraform, leveraging existing research modules in `08-features/09-terraform-research/`. This enables consistent deployments, disaster recovery, and eliminates manual configuration errors.

**Target Users:**
- **DevOps Team:** Sarah Chen (Lead), David Kim (Platform Engineer), Alex Martinez (DevOps Engineer)
- **Developers:** Frontend and backend developers needing infrastructure changes
- **Stakeholders:** Engineering Director (budget approval, escalations)

---

## 2. Goals

### Primary Goals
1. **Achieve 100% Infrastructure as Code coverage** for diagnostic-pro-prod
2. **Enable disaster recovery** with <30 minute full infrastructure rebuild capability
3. **Eliminate configuration drift** between manual changes and documented state
4. **Reduce deployment time** from 8 hours (manual) to 15 minutes (automated)
5. **Establish version control** for all infrastructure changes via Git

### Secondary Goals
6. Create reusable Terraform modules for future environment expansion (dev/staging)
7. Document infrastructure architecture for new team members
8. Integrate Terraform into CI/CD pipeline (GitHub Actions)
9. Establish disaster recovery runbooks and monthly testing procedures

---

## 3. User Stories

### US-001: DevOps Engineer Imports Existing Infrastructure
**As a** DevOps Engineer (Sarah Chen)
**I want to** import existing Cloud Run services into Terraform state
**So that** I can manage them with IaC without recreating/disrupting production

**Acceptance Criteria:**
- Import all 3 Cloud Run services (diagnosticpro-vertex-ai-backend, diagnosticpro-stripe-webhook, simple-diagnosticpro)
- `terraform plan` shows 0 changes after import (state matches reality)
- No production downtime during import process

### US-002: DevOps Team Manages Secrets via Terraform
**As a** DevOps Team
**I want to** manage Secret Manager secrets metadata in Terraform
**So that** secret rotation policies and access controls are version controlled

**Acceptance Criteria:**
- All 8 Secret Manager secrets defined in Terraform (stripe-secret, vertex-ai-api-key, etc.)
- Secret values NOT stored in Terraform code (metadata only)
- Rotation policies configured for 90-day rotation

### US-003: Platform Engineer Deploys New Cloud Run Service
**As a** Platform Engineer (David Kim)
**I want to** deploy a new Cloud Run service using reusable Terraform modules
**So that** I can self-service infrastructure without manual GCP Console work

**Acceptance Criteria:**
- Cloud Run module accepts parameters (image, memory, CPU, env vars)
- Service deployed successfully via `terraform apply`
- Service account and IAM roles automatically configured

### US-004: DevOps Lead Recovers from Disaster
**As a** DevOps Lead (Sarah Chen)
**I want to** rebuild entire infrastructure from Terraform code
**So that** we can recover from catastrophic failures in <30 minutes

**Acceptance Criteria:**
- `terraform destroy && terraform apply` rebuilds all infrastructure
- Firestore data preserved (database not destroyed, only imported)
- All Cloud Run services, IAM, networking restored correctly

### US-005: Developer Understands Infrastructure
**As a** Frontend Developer (new team member)
**I want to** read Terraform documentation to understand infrastructure
**So that** I can debug deployment issues without waiting for DevOps

**Acceptance Criteria:**
- Auto-generated documentation (terraform-docs) in README.md
- Architecture diagrams showing resource dependencies
- Runbooks for common operations (deploy, rollback, disaster recovery)

---

## 4. Functional Requirements

### Core Infrastructure Migration
1. **Terraform must manage all Cloud Run services** (diagnosticpro-vertex-ai-backend, diagnosticpro-stripe-webhook, simple-diagnosticpro) with configuration for image, memory, CPU, min/max instances, environment variables
2. **Terraform must manage Firestore database** with composite indexes (diagnosticSubmissions, orders, emailLogs collections)
3. **Terraform must manage Secret Manager secrets** (metadata only: stripe-secret, stripe-webhook-secret, vertex-ai-api-key, gmail-app-password, firebase-admin-sdk, firestore-service-account, github-webhook-secret, slack-webhook-url)
4. **Terraform must manage Cloud Storage buckets** (diagnostic-pro-prod-reports-us-central1, diagnostic-pro-prod-frontend, diagnostic-pro-terraform-state) with lifecycle rules
5. **Terraform must manage IAM service accounts** (diagnosticpro-vertex-ai-backend-sa, terraform-automation-sa, github-actions-sa, etc.) and role bindings
6. **Terraform must manage API Gateway** (diagpro-gw-3tbssksx) with backend routing to Cloud Run services
7. **Terraform must manage VPC networking** (default VPC, Cloud NAT, firewall rules for Cloud Run ingress)

### State Management
8. **Terraform state must be stored in GCS bucket** `diagnostic-pro-prod-terraform-state` with encryption (Customer-Managed Encryption Key)
9. **State bucket must have versioning enabled** with 30 version retention for rollback capability
10. **State locking must be enabled** via GCS metadata to prevent concurrent applies
11. **State file must NOT contain secret values** (use `data.google_secret_manager_secret_version` for references)

### Module Architecture
12. **Cloud Run module must be reusable** across all Cloud Run services with parameters for image, memory, CPU, env vars, service account
13. **Firestore module must manage database and indexes** with validation for composite index definitions
14. **Secret Manager module must manage secret metadata** (NOT values) with rotation policies
15. **IAM module must manage service accounts and role bindings** following least-privilege principle
16. **Storage module must manage buckets with lifecycle rules** (30-day retention for reports, versioning for state)

### Import Strategy (Zero Downtime)
17. **Existing resources must be imported** using `terraform import` (NOT recreated)
18. **Import validation must confirm** `terraform plan` shows 0 changes after import
19. **Production traffic must not be disrupted** during import process
20. **Import must be idempotent** (can be run multiple times safely)

### CI/CD Integration
21. **GitHub Actions workflow must run** `terraform plan` on every pull request
22. **Terraform plan output must be posted** as PR comment for review
23. **Terraform apply must run** on merge to main branch (with manual approval gate)
24. **Deployment failures must trigger rollback** automatically via GitHub Actions

### Documentation & Testing
25. **Infrastructure documentation must be auto-generated** using `terraform-docs` in README.md
26. **Disaster recovery runbook must be tested** monthly via scheduled `terraform destroy && terraform apply` in dev environment
27. **All modules must have examples** demonstrating usage with realistic parameters
28. **Security scanning must run** via `tfsec` in CI/CD pipeline (fail on high/critical issues)

---

## 5. Non-Goals (Out of Scope)

### Explicitly NOT Included in v1.0
- ❌ **Multi-region deployment** (future Sprint 4+)
- ❌ **Dev/staging environment creation** (production only for now)
- ❌ **Kubernetes migration** (Cloud Run is sufficient)
- ❌ **Cross-cloud provider support** (AWS/Azure) - GCP only
- ❌ **Database migration automation** (Firestore data preserved, not migrated)
- ❌ **Cost optimization analysis** (focus on IaC first, cost second)
- ❌ **Automated secret rotation** (rotation policies defined, but manual rotation)
- ❌ **Terraform Cloud migration** (GCS state backend sufficient)

---

## 6. Design Considerations

### Existing Terraform Research
**Location:** `08-features/09-terraform-research/`

**Already Built Modules:**
- `modules/cloud-run/` - Cloud Run service with IAM, autoscaling, env vars
- `modules/iam/` - Service accounts and role bindings
- `modules/firestore/` - Firestore database (placeholder, needs composite indexes)
- `modules/storage/` - Cloud Storage buckets with lifecycle rules
- `modules/api-gateway/` - API Gateway configuration (needs validation)
- `modules/database/` - Generic database module (evaluate if needed)
- `modules/media-processing/` - Media processing module (evaluate if needed)

**Backend Configuration:**
```hcl
# backend.tf (already exists)
terraform {
  backend "gcs" {
    bucket = "diagnostic-pro-prod-terraform-state"
    prefix = "terraform/state"
  }
}
```

**Migration Strategy:**
1. **Phase 1 (Sprint 1):** Move research modules to production (`/terraform/modules/`)
2. **Phase 2 (Sprint 1):** Import Cloud Run services (3 services)
3. **Phase 3 (Sprint 2):** Import Firestore, Secrets, Storage (core data layer)
4. **Phase 4 (Sprint 3):** Import IAM, networking, API Gateway (advanced resources)

### UI/UX Considerations
- **Developer Experience:** Clear module documentation, examples, error messages
- **CI/CD Integration:** Visible terraform plan in PR comments, manual approval gates
- **Disaster Recovery:** One-command infrastructure rebuild (`terraform apply`)

---

## 7. Technical Considerations

### Dependencies
- **GCS State Bucket:** `diagnostic-pro-prod-terraform-state` (already exists)
- **Service Account:** `terraform-automation-sa@diagnostic-pro-prod.iam.gserviceaccount.com` with `roles/editor`
- **GitHub Actions:** Existing CI/CD pipeline for frontend/backend deployment
- **Terraform Version:** 1.9.5+ (specify in `versions.tf`)
- **Google Provider:** 6.0+ (specify in `versions.tf`)

### Integration Points
- **Secret Manager Integration:** `secrets.js` (backend) must work with Terraform-managed secrets
- **GitHub Actions Integration:** Existing workflows must add Terraform plan/apply steps
- **Cloud Run Deployment:** Current backend deployment must use Terraform-managed services
- **Monitoring Integration:** Cloud Monitoring dashboards must reference Terraform-managed resources

### Security Requirements
- **No Secrets in Code:** Use `data.google_secret_manager_secret_version` for secret references
- **Least-Privilege IAM:** Service accounts follow principle of least privilege
- **State Encryption:** Customer-Managed Encryption Keys (CMEK) for state bucket
- **Pre-commit Hooks:** `detect-secrets` prevents accidental secret commits
- **Security Scanning:** `tfsec` runs in CI/CD pipeline

### Known Constraints
- **Production Uptime:** Zero downtime tolerance (import-only, no recreation)
- **Budget:** <$500/month additional Terraform Cloud costs (use GCS backend to avoid)
- **Team Expertise:** Basic Terraform knowledge (2-day training workshop Oct 7-8)
- **Timeline:** 6-week implementation (3 sprints: Oct 7 - Nov 15)

---

## 8. Success Metrics

### Deployment Efficiency
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| **Infrastructure Deployment Time** | 8 hours (manual) | 15 minutes (terraform apply) | GitHub Actions execution time |
| **Deployment Success Rate** | 75% (manual errors) | 99% (automated validation) | Terraform apply success/failure ratio |

### Reliability & Recovery
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| **Disaster Recovery Time** | 8+ hours (manual rebuild) | 30 minutes (terraform apply) | Disaster recovery drill execution time |
| **Environment Consistency** | 65% (manual drift) | 100% (terraform-managed) | terraform plan shows 0 drift |

### Operational Efficiency
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| **Configuration Errors** | 3-5 per month (manual) | 0 (validation catches) | Incident reports (infrastructure-related) |
| **Developer Onboarding Time** | 2 weeks (manual setup) | 2 days (documented infrastructure) | New team member time-to-productivity |
| **Infrastructure Documentation** | 0% (tribal knowledge) | 100% (auto-generated) | terraform-docs coverage |

### Team Productivity
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| **DevOps Time on Infrastructure** | 40 hours/month (manual changes) | 8 hours/month (automated) | Time tracking (manual vs automated tasks) |
| **Self-Service Infrastructure** | 0% (DevOps-only) | 80% (developer self-service) | % of infrastructure changes by developers |

---

## 9. Open Questions

### Technical Questions
1. **Q:** Should we migrate the `modules/media-processing/` module from research, or is it unused?
   **Status:** 🟡 Needs review (check if media processing is implemented)

2. **Q:** Do we need separate Terraform workspaces for environments, or single production workspace?
   **Status:** ✅ Resolved - Single production workspace (diagnostic-pro-prod only)

3. **Q:** Should API Gateway OpenAPI spec be managed in Terraform, or separate YAML file?
   **Status:** 🟡 Needs decision (evaluate Terraform vs YAML maintenance)

4. **Q:** Do we need Terraform Cloud for remote state management, or is GCS sufficient?
   **Status:** ✅ Resolved - GCS backend sufficient (cost optimization)

### Process Questions
5. **Q:** Who has final approval authority for terraform apply in production?
   **Status:** 🟡 Needs confirmation (likely Sarah Chen or Engineering Director)

6. **Q:** What is the rollback procedure if terraform apply fails in production?
   **Status:** 🟡 Needs documentation (manual GCP Console rollback vs terraform state rollback)

7. **Q:** How do we handle Firestore composite index changes (terraform vs manual)?
   **Status:** 🟡 Needs testing (Firestore index deployment can take hours)

### Security Questions
8. **Q:** Who has access to `diagnostic-pro-terraform-state` GCS bucket?
   **Status:** 🟡 Needs IAM audit (limit to terraform-automation-sa + DevOps team)

9. **Q:** Should Terraform state be encrypted with Customer-Managed Keys (CMEK)?
   **Status:** ✅ Resolved - Yes, use CMEK for compliance (defined in backend.tf)

10. **Q:** How do we rotate the `terraform-automation-sa` service account key?
    **Status:** 🟡 Needs procedure (service account key rotation policy)

---

## 📝 Additional Notes

### Related Documentation
- **Existing Research:** `/08-features/09-terraform-research/` (modules already prototyped)
- **Secret Manager Integration:** `/02-src/backend/services/backend/secrets.js` (Oct 3, 2025)
- **Current Infrastructure:** Documented in `CLAUDE.md` (5 Cloud Run services, 8 secrets, 3 buckets)
- **DevOps Automation:** `DEVELOPER-ONBOARDING.md`, `SECRET-MANAGER-SETUP.md`

### Implementation Timeline
**Sprint 1 (Oct 7-18):** Cloud Run services migration (30 SP)
**Sprint 2 (Oct 21-Nov 1):** Firestore + Secrets + Storage (18 SP)
**Sprint 3 (Nov 4-15):** IAM + Networking + Disaster Recovery (12 SP)

### Risk Mitigation
- **Zero Downtime:** Import-only strategy (no resource recreation)
- **State Backup:** GCS versioning (30 versions) + daily backups
- **Team Training:** 2-day Terraform workshop (Oct 7-8)
- **Gradual Rollout:** Test in dev environment first (if available)

---

**Status:** ✅ Ready for task generation
**Next Steps:** Generate task list (`tasks-prd-terraform-migration.md`) with parent tasks → wait for "Go" → generate sub-tasks
**Owner:** Sarah Chen (DevOps Lead)
**Contact:** sarah.chen@diagnosticpro.io / Slack: @sarah.chen
