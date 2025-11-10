# ADR-001: Terraform Infrastructure as Code Migration

**Date:** 2025-10-06
**Status:** Approved
**Decision Makers:** DevOps Team, Platform Engineering
**Related Documents:**
- PRD: `054-prd-terraform-infrastructure-migration.md`
- Tasks: `055-ref-terraform-migration-tasks.md`

---

## Context and Problem Statement

DiagnosticPro infrastructure is currently managed manually through Google Cloud Console, leading to:
- **Configuration Drift**: Manual changes not tracked in version control
- **Deployment Inconsistency**: 8-hour manual deployments with 3-5 configuration errors per month
- **Disaster Recovery Risk**: No automated infrastructure rebuild capability (8+ hour recovery time)
- **Lack of Auditability**: Infrastructure changes not versioned or peer-reviewed
- **Team Bottleneck**: Single-person knowledge dependency for infrastructure management

**Current Infrastructure Scope:**
- 3 Cloud Run services (diagnosticpro-vertex-ai-backend, diagnosticpro-stripe-webhook, simple-diagnosticpro)
- 8 Secret Manager secrets (stripe-secret, vertex-ai-api-key, firebase-admin-sdk, etc.)
- 3 Cloud Storage buckets (reports, frontend, terraform-state)
- 12 service accounts with complex IAM role bindings
- 1 Firestore database with composite indexes
- 1 API Gateway (diagpro-gw-3tbssksx)
- VPC networking and firewall rules

**Decision Required:** Select an Infrastructure as Code (IaC) tool to codify and automate DiagnosticPro GCP infrastructure management.

---

## Decision Drivers

1. **Zero Downtime Requirement**: Must import existing production resources without recreation
2. **GCP Native Support**: First-class support for Google Cloud Platform services
3. **Team Familiarity**: Leverage existing Terraform research in `08-features/09-terraform-research/`
4. **State Management**: Reliable state backend with encryption and locking
5. **CI/CD Integration**: Automated validation and deployment pipelines
6. **Community Support**: Active ecosystem for GCP-specific modules and troubleshooting
7. **Declarative Syntax**: Infrastructure defined as desired state, not imperative scripts
8. **Cost**: Open-source or cost-effective solution

---

## Alternatives Considered

### Option 1: Terraform (SELECTED ✅)

**Description:** HashiCorp's open-source IaC tool with declarative HCL syntax and extensive GCP provider support.

**Pros:**
- ✅ **Existing Team Research**: Modules already built in `08-features/09-terraform-research/` (cloud-run, iam, firestore, storage)
- ✅ **Mature GCP Provider**: 1000+ GCP resources supported with active development
- ✅ **Import-First Migration**: `terraform import` allows zero-downtime migration strategy
- ✅ **State Backend**: GCS backend with encryption and state locking (bucket already exists: `diagnostic-pro-prod-terraform-state`)
- ✅ **CI/CD Ready**: GitHub Actions integrations for `terraform plan` (PR) and `terraform apply` (merge)
- ✅ **Community Modules**: Extensive public registry for reusable patterns
- ✅ **Declarative HCL**: Easy to read and understand infrastructure definitions

**Cons:**
- ⚠️ Learning curve for advanced features (state management, module composition)
- ⚠️ Manual state management required for complex operations

**Decision Rationale:**
- Leverages existing team investment in Terraform research
- GCS state backend already configured and tested
- Import commands identified for all 3 Cloud Run services, 8 secrets, 3 buckets, 12 service accounts
- Clear migration path with zero downtime

---

### Option 2: Google Cloud Deployment Manager

**Description:** Google's native IaC tool for GCP resources using YAML/Python/Jinja2.

**Pros:**
- Native GCP integration (no third-party providers)
- Direct support from Google Cloud
- YAML-based configuration (familiar to team)

**Cons:**
- ❌ **GCP-Only**: Cannot manage multi-cloud or external services (Stripe webhooks, external APIs)
- ❌ **Limited Community**: Smaller ecosystem compared to Terraform
- ❌ **No Existing Research**: Would require starting from scratch (vs. existing Terraform modules)
- ❌ **Import Limitations**: Weaker import capabilities for existing resources
- ❌ **Less Mature**: Fewer production-ready examples and best practices

**Why Not Selected:**
- Discards existing Terraform research investment
- GCP-only limitation prevents managing external integrations
- Weaker community support for troubleshooting

---

### Option 3: Pulumi

**Description:** Modern IaC platform using programming languages (TypeScript, Python, Go) instead of DSL.

**Pros:**
- Full programming language flexibility (TypeScript/Python)
- Strong type checking and IDE support
- Modern architecture and design

**Cons:**
- ❌ **No Existing Work**: Would require complete rewrite from scratch
- ❌ **Learning Curve**: Team would need to learn Pulumi SDK and concepts
- ❌ **State Management**: Requires Pulumi Cloud subscription or self-hosted backend setup
- ❌ **Migration Complexity**: Import process less mature than Terraform
- ❌ **Cost**: Pulumi Cloud pricing for team collaboration features

**Why Not Selected:**
- Higher learning curve with no existing team knowledge
- Requires new state backend infrastructure
- Discards all existing Terraform research

---

### Option 4: AWS CloudFormation / CDK (Cross-Cloud)

**Description:** AWS native IaC tool with cross-cloud capabilities through third-party extensions.

**Pros:**
- Mature infrastructure-as-code platform
- CDK allows programming language usage

**Cons:**
- ❌ **AWS-Centric**: Designed for AWS, GCP support is second-class
- ❌ **Poor GCP Coverage**: Limited GCP resource support
- ❌ **Wrong Ecosystem**: Team expertise is in GCP, not AWS
- ❌ **Migration Complexity**: Would require extensive custom development

**Why Not Selected:**
- DiagnosticPro is 100% Google Cloud Platform
- No AWS infrastructure or future AWS migration plans
- Poor fit for GCP-native architecture

---

### Option 5: Manual GCP Console Management (Status Quo)

**Description:** Continue managing infrastructure manually through Google Cloud Console.

**Pros:**
- No migration effort required
- Immediate changes without code review

**Cons:**
- ❌ **Configuration Drift**: Manual changes not tracked or versioned
- ❌ **Slow Deployments**: 8-hour manual deployments with high error rate (3-5 errors/month)
- ❌ **Disaster Recovery**: 8+ hour recovery time with manual rebuild
- ❌ **No Auditability**: Infrastructure changes not peer-reviewed or documented
- ❌ **Single Point of Failure**: One person knows infrastructure setup
- ❌ **Scalability Issues**: Cannot scale to multi-environment (dev/staging/prod)

**Why Not Selected:**
- Unacceptable operational risk for production system
- Does not meet PRD success metrics (15-minute deployments, 30-minute DR recovery)

---

## Decision Outcome

**Selected Option:** Terraform Infrastructure as Code

**Rationale:**
1. **Leverages Existing Investment**: `08-features/09-terraform-research/` contains validated modules (cloud-run, iam, firestore, storage) ready for production use
2. **Zero-Downtime Migration**: Import-only strategy using `terraform import` commands for all existing resources (no resource recreation)
3. **Proven GCP Support**: Terraform's Google Cloud provider supports 1000+ resource types with active development
4. **State Backend Ready**: GCS bucket `diagnostic-pro-prod-terraform-state` already configured with encryption and state locking
5. **CI/CD Integration**: GitHub Actions workflows for automated `terraform plan` (PR comments) and `terraform apply` (merge to main)
6. **Team Familiarity**: DevOps engineer has existing Terraform research to build upon
7. **Community Support**: Extensive Terraform + GCP ecosystem for troubleshooting and best practices

---

## Implementation Strategy

### Phase 1: Project Setup & Module Migration (Sprint 1: Oct 7-18)
- Move research modules from `08-features/09-terraform-research/modules/` to `terraform/modules/`
- Initialize Terraform backend with GCS state bucket
- Validate modules with `terraform validate` and `tfsec` security scanning

### Phase 2: Cloud Run Services Import (Sprint 1: Oct 7-18)
- Import 3 Cloud Run services: `diagnosticpro-vertex-ai-backend`, `diagnosticpro-stripe-webhook`, `simple-diagnosticpro`
- Validate with `terraform plan` (expect 0 changes - state matches reality)
- Test backend service health endpoints

### Phase 3: Firestore, Secrets, Storage (Sprint 2: Oct 21-Nov 1)
- Import 8 Secret Manager secrets (stripe-secret, vertex-ai-api-key, firebase-admin-sdk, etc.)
- Import Firestore database with composite indexes
- Import 3 Cloud Storage buckets with lifecycle policies
- Verify backend `secrets.js` still works with Terraform-managed secrets

### Phase 4: IAM, Networking, API Gateway (Sprint 3: Nov 4-15)
- Import 12 service accounts with IAM role bindings
- Import VPC networking and firewall rules
- Import API Gateway configuration (`diagpro-gw-3tbssksx`)

### Phase 5: CI/CD & Disaster Recovery (Sprint 3: Nov 4-15)
- Create `.github/workflows/terraform.yml` for automated plan/apply
- Generate disaster recovery runbook: `01-docs/059-gde-terraform-disaster-recovery.md`
- Test infrastructure rebuild: `terraform destroy && terraform apply` (dev environment)

---

## Consequences

### Positive Consequences ✅

1. **Version Control**: All infrastructure changes tracked in Git with peer review
2. **Deployment Speed**: 8-hour manual deployments → 15-minute automated deployments (96.9% improvement)
3. **Disaster Recovery**: 8+ hour manual rebuild → 30-minute automated rebuild (93.75% improvement)
4. **Configuration Drift**: Eliminated - infrastructure defined in code, changes require PR approval
5. **Auditability**: Full audit trail of infrastructure changes with Git history
6. **Multi-Environment**: Foundation for dev/staging/prod environment parity
7. **Team Knowledge**: Infrastructure documented in code, reducing single-person dependency
8. **Error Reduction**: 3-5 configuration errors/month → 0 errors (automated validation)

### Negative Consequences ⚠️

1. **Initial Migration Effort**: 60 story points across 3 sprints (Oct 7 - Nov 15)
2. **Learning Curve**: Team must learn Terraform state management and module patterns
3. **State Management Complexity**: GCS state backend requires careful handling for concurrent changes
4. **Ongoing Maintenance**: Terraform code must be updated when infrastructure changes
5. **CI/CD Dependency**: Infrastructure changes now require GitHub Actions pipeline (adds latency)

### Mitigation Strategies

1. **Migration Effort**: Import-only strategy (no resource recreation) minimizes risk
2. **Learning Curve**: Existing research in `08-features/09-terraform-research/` provides foundation
3. **State Management**: GCS backend with state locking prevents concurrent modification
4. **Maintenance**: Terraform code auto-documentation with `terraform-docs` reduces documentation burden
5. **CI/CD Latency**: Manual approval gate for `terraform apply` maintains control

---

## Compliance and Security

### Security Measures
- **State Encryption**: GCS backend with encryption at rest and in transit
- **Secret Management**: Terraform manages secret metadata only (NOT secret values) - values stored in Google Secret Manager
- **IAM Principle of Least Privilege**: Service accounts granted minimum required permissions
- **Security Scanning**: `tfsec` runs on every PR to catch security issues before merge
- **Audit Logging**: All Terraform changes tracked in Git with commit author and timestamp

### Compliance Requirements
- **No Secret Values in Code**: Terraform manages secret metadata, Secret Manager stores actual values
- **Peer Review**: All infrastructure changes require PR approval before `terraform apply`
- **Disaster Recovery Testing**: Monthly DR test (documented in `059-gde-terraform-disaster-recovery.md`)
- **Backup Strategy**: Terraform state backed up in GCS bucket with versioning enabled

---

## Success Metrics

| Metric | Current (Manual) | Target (Terraform) | Improvement |
|--------|------------------|-------------------|-------------|
| **Deployment Time** | 8 hours | 15 minutes | 96.9% faster |
| **Configuration Errors** | 3-5 per month | 0 per month | 100% reduction |
| **Disaster Recovery Time** | 8+ hours | 30 minutes | 93.75% faster |
| **Infrastructure Audit Trail** | None | Git history | 100% coverage |
| **Environment Parity** | Manual setup | Code-defined | Automated |

---

## Related Decisions

- **ADR-002**: Secret Manager Integration (completed Oct 3, 2025 - see `057-gde-secret-manager-integration.md`)
- **ADR-003**: Firebase Migration (completed Sep 24-25, 2025 - see `046-ref-claude-code-guide.md`)
- **Future**: Multi-environment strategy (dev/staging/prod) after Terraform migration completes

---

## References

- **PRD**: `054-prd-terraform-infrastructure-migration.md` - Product requirements and user stories
- **Task List**: `055-ref-terraform-migration-tasks.md` - 47 detailed implementation sub-tasks
- **Existing Research**: `08-features/09-terraform-research/` - Validated Terraform modules
- **Backend Integration**: `02-src/backend/services/backend/secrets.js` - Secret Manager usage
- **Terraform Documentation**: https://registry.terraform.io/providers/hashicorp/google/latest/docs
- **GCS State Backend**: https://developer.hashicorp.com/terraform/language/settings/backends/gcs

---

**Decision Status:** ✅ **APPROVED**
**Implementation Start:** Sprint 1 begins Oct 7, 2025
**Expected Completion:** Nov 15, 2025 (3 sprints, 60 story points)

---

**Last Updated:** 2025-10-06
**Next Review:** After Sprint 1 completion (Oct 18, 2025)
