# Terraform Research Materials - Location Reference

**Date:** 2025-10-07
**Type:** Reference Document
**Status:** Active

---

## Location

All Terraform research materials, configurations, and documentation are located at:

```
06-Infrastructure/terraform-research/
```

---

## Contents

### Documentation
- `README.md` - Research overview and index
- `firebase-migration-plan.md` - Firebase to native GCP migration plan
- `migration-assessment.md` - Migration readiness assessment
- `migration-plan.md` - Detailed migration execution plan
- `gcp-discovery-questionnaire.md` - GCP resource discovery questionnaire
- `terraform-learning-guide.md` - Terraform learning resources and guides
- `atlantis-terragrunt-guide.md` - Atlantis/Terragrunt integration guide

### Working Terraform Configurations
- `main.tf` - Main Terraform configuration
- `main-native-gcp.tf` - Native GCP infrastructure (no Firebase)
- `backend.tf` - Backend configuration
- `providers.tf` - Provider configurations
- `variables.tf` - Variable definitions
- `outputs.tf` - Output definitions
- `versions.tf` - Version constraints

### Modules
```
modules/
├── cloud-run/          # Cloud Run service module
├── database/           # Cloud SQL database module
├── iam/                # IAM service account module
└── media-processing/   # Media processing pipeline module
```

### Scripts
```
scripts/
└── import-production.sh   # Production resource import script
```

### Environments
```
environments/
└── [environment configurations]
```

---

## Related Documentation

- **PRD:** 003-prd-terraform-infrastructure.md
- **Tasks:** 004-tsk-terraform-migration.md
- **ADR:** 005-adr-terraform-iac.md
- **Guide:** 006-gde-terraform-ai-collab.md

---

## Purpose

This file maintains the flat structure requirement for `01-Docs/` per MASTER DIRECTORY STANDARDS while providing quick reference to the actual Terraform research location in `06-Infrastructure/`.

---

**Total Size:** ~152KB of research materials
**Last Updated:** 2025-10-07
**Maintained By:** Platform infrastructure team
