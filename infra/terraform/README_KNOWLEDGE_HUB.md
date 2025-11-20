# Knowledge Hub Infrastructure

## Overview

This module defines the **org-wide knowledge hub** pattern for Intent Solutions. It provides a central GCS bucket repository that all AI agents across multiple GCP projects can access via cross-project IAM.

**Key Principle:** Share knowledge via IAM, not data duplication.

## Architecture

```
datahub-intent (Knowledge Hub Project)
└── gs://datahub-intent/ (Production Bucket)
    ├── bobs-brain/      → Bob + iam-* agents
    ├── iam-agents/      → IAM agent templates
    ├── diagnosticpro/   → DiagnosticPro knowledge
    ├── pipelinepilot/   → PipelinePilot data
    └── shared/          → Cross-product knowledge
```

## Current State

The knowledge hub infrastructure exists in two forms:

1. **Manually Created** (Active):
   - Project: `datahub-intent` ✅
   - Bucket: `gs://datahub-intent/` ✅
   - Status: Created via scripts, operational

2. **Terraform Managed** (Future):
   - File: `knowledge_hub.tf` (stub/template)
   - Status: Ready for import when needed

## Usage

### For New Projects

To connect a new project to the knowledge hub:

1. **Get Service Account Emails**:
   ```bash
   # Get your project's runtime SA
   gcloud iam service-accounts list --project=YOUR_PROJECT
   ```

2. **Update Terraform Variables**:
   ```hcl
   # In envs/prod.tfvars
   consumer_service_accounts = [
     {
       email  = "agent-runtime@YOUR_PROJECT.iam.gserviceaccount.com"
       prefix = "your-project/"
     }
   ]
   ```

3. **Grant Access** (Manual for now):
   ```bash
   gsutil iam ch serviceAccount:YOUR_SA@YOUR_PROJECT.iam.gserviceaccount.com:objectViewer \
     gs://datahub-intent
   ```

### For Bob's Brain

Bob is already connected and can switch via feature flag:

```bash
# Use existing datastore (default)
export USE_DATAHUB=false

# Switch to datahub (when ready)
export USE_DATAHUB=true
```

## Migration Path

### Phase 1: Manual Setup ✅
- Created `datahub-intent` project
- Created main bucket with structure
- Connected Bob's service accounts

### Phase 2: Vertex AI Search (Next)
```bash
# Create the universal datastore
gcloud ai search datastores create universal-knowledge-store \
  --location=us \
  --project=bobs-brain \
  --type=unstructured

# Import knowledge
gcloud ai search documents import \
  --datastore=universal-knowledge-store \
  --location=us \
  --project=bobs-brain \
  --gcs-uri=gs://datahub-intent/bobs-brain/**
```

### Phase 3: Terraform Import (Future)
```bash
# When ready to manage via Terraform
terraform import google_storage_bucket.knowledge_hub_prod datahub-intent
```

## Security Model

### Access Levels
- **Read Only**: All agent runtime service accounts
- **Write**: CI/CD deployment pipelines only
- **Admin**: Terraform service account

### Prefix Isolation
Each project gets its own prefix:
- `gs://datahub-intent/bobs-brain/` - Bob's knowledge only
- `gs://datahub-intent/diagnosticpro/` - DiagnosticPro only

Future: IAM conditions will enforce prefix boundaries.

## Cost Management

### Storage Classes
- **Standard** (0-90 days): Active knowledge
- **Nearline** (90-365 days): Archived knowledge
- **Archive** (365+ days): Compliance only

### Estimated Costs
- Storage: ~$20/month for 1TB
- Vertex AI Search: Free (5GB tier)
- Network: ~$10/month cross-region

## Monitoring

### Key Metrics
- Storage usage by prefix
- Access frequency by SA
- Search query performance
- Cost allocation by project

### Alerts (To Configure)
```yaml
- Storage > 80% quota
- Unauthorized access attempts
- Search indexing failures
- Unusual cost spike
```

## Troubleshooting

### Common Issues

**Can't access bucket from agent**:
```bash
# Check IAM binding
gsutil iam get gs://datahub-intent | grep YOUR_SA

# Grant access if missing
gsutil iam ch serviceAccount:YOUR_SA:objectViewer gs://datahub-intent
```

**Vertex AI Search not finding documents**:
```bash
# Check import status
gcloud ai search operations list \
  --location=us \
  --project=bobs-brain

# Re-import if needed
gcloud ai search documents import ...
```

**Feature flag not working**:
```bash
# Verify environment variable
echo $USE_DATAHUB

# Check agent code uses the flag
grep USE_DATAHUB agents/shared_tools/local_builtins.py
```

## Important Notes

1. **DO NOT** duplicate data across projects
2. **DO NOT** grant write access to runtime SAs
3. **DO NOT** bypass the prefix structure
4. **ALWAYS** use cross-project IAM for access
5. **ALWAYS** test with dev bucket first

## Contact

- **Owner**: ADK Department Build Captain
- **Project**: datahub-intent
- **Documentation**: See 6767-091-AT-ARCH-org-knowledge-hub-gcs-vertex-search.md

---

Last Updated: 2025-11-20