# 091-AT-ARCH-org-knowledge-hub-gcs-vertex-search.md

**Date Created:** 2025-11-20
**Category:** AT - Architecture & Technical
**Type:** ARCH - Architecture Document
**Status:** CANONICAL ✅

---

## Executive Summary

This document defines the **canonical org-wide knowledge hub architecture** for Intent Solutions, providing a single source of truth for organizational knowledge accessible by all AI agents across multiple GCP projects via cross-project IAM, eliminating data duplication and enabling unified RAG capabilities through Vertex AI Search.

---

## Architecture Overview

### High-Level Design
```
┌─────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE HUB PROJECT                     │
│                  (intent-knowledge-hub)                      │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              GCS KNOWLEDGE BUCKETS                   │   │
│  │                                                      │   │
│  │  gs://intent-org-knowledge-dev/                     │   │
│  │  ├── bobs-brain/                                    │   │
│  │  ├── iam-agents/                                    │   │
│  │  ├── diagnosticpro/                                 │   │
│  │  ├── pipelinepilot/                                 │   │
│  │  └── shared/                                        │   │
│  │                                                      │   │
│  │  gs://intent-org-knowledge-prod/                    │   │
│  │  └── (same structure)                               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Cross-Project IAM
                              │ (No Data Duplication)
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐     ┌───────▼──────┐     ┌───────▼──────┐
│  bobs-brain  │     │ diagnosticpro│     │ pipelinepilot│
│   PROJECT    │     │   PROJECT    │     │   PROJECT    │
│              │     │              │     │              │
│ Vertex AI    │     │ Future Agent │     │ Future Agent │
│ Search DS    │     │ Integration  │     │ Integration  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Core Principles
1. **Single Source of Truth** - One canonical bucket set for all organizational knowledge
2. **Cross-Project IAM** - Service accounts access via IAM, no data copying
3. **Prefix Isolation** - Each product/project gets its own prefix namespace
4. **Environment Separation** - Dev and prod buckets with identical structure
5. **Vertex AI Search Ready** - Designed for seamless RAG integration

---

## GCP Project Layout

### Knowledge Hub Project
**Project ID Variable:** `intent-knowledge-hub` (configurable via Terraform variable)

**Purpose:** Centralized storage and management of organizational knowledge assets

**Resources:**
- 2x GCS buckets (dev/prod)
- IAM policies for cross-project access
- Monitoring and logging
- Future: Data lifecycle policies

### Bucket Structure

| Environment | Bucket Name | Purpose |
|-------------|------------|---------|
| Development | `gs://intent-org-knowledge-dev` | Testing, staging content |
| Production | `gs://intent-org-knowledge-prod` | Live agent knowledge |

### Internal Prefix Layout
```
gs://intent-org-knowledge-{env}/
├── bobs-brain/           # Bob + iam-* department knowledge
│   ├── adk-docs/         # ADK documentation
│   ├── agent-patterns/   # Agent design patterns
│   └── department-kb/    # Department knowledge base
├── iam-agents/           # IAM agent-specific knowledge
│   ├── templates/        # Agent templates
│   └── runbooks/         # Operational runbooks
├── diagnosticpro/        # DiagnosticPro product knowledge
│   ├── repair-guides/    # Technical repair documentation
│   └── diagnostic-data/  # Diagnostic patterns
├── pipelinepilot/        # PipelinePilot knowledge
│   ├── sales-intel/      # Sales intelligence data
│   └── automation/       # Automation patterns
├── shared/               # Cross-product shared knowledge
│   ├── standards/        # Org-wide standards
│   ├── templates/        # Shared templates
│   └── compliance/       # Compliance documentation
└── archive/              # Deprecated but retained knowledge
```

---

## IAM Model

### Service Account Types

| Account Type | Purpose | Permissions | Scope |
|--------------|---------|-------------|-------|
| **Agent Runtime SA** | Vertex AI Agent Engine runtime | `roles/storage.objectViewer` | Product prefix |
| **Search Service SA** | Vertex AI Search indexing | `roles/storage.objectViewer` | Product prefix |
| **Deployment SA** | CI/CD write access | `roles/storage.objectAdmin` | Product prefix |
| **Backup SA** | Cross-region backup | `roles/storage.objectViewer` | All prefixes |
| **Analytics SA** | Usage analytics | `roles/storage.objectViewer` | Metadata only |

### Cross-Project IAM Pattern

```hcl
# Example IAM binding (Terraform)
resource "google_storage_bucket_iam_member" "bobs_brain_runtime" {
  bucket = google_storage_bucket.knowledge_hub_prod.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.bobs_brain_runtime_sa}"

  # Optional: IAM condition for prefix restriction
  condition {
    title      = "bobs-brain-prefix-only"
    expression = "resource.name.startsWith('projects/_/buckets/intent-org-knowledge-prod/objects/bobs-brain/')"
  }
}
```

### Permission Matrix

| Project | Service Account Type | Bucket | Prefix | Access Level |
|---------|---------------------|---------|---------|--------------|
| bobs-brain | Agent Runtime SA | prod | `/bobs-brain/**` | Read |
| bobs-brain | Search Service SA | prod | `/bobs-brain/**` | Read |
| bobs-brain | Deployment SA | prod | `/bobs-brain/**` | Write |
| diagnosticpro | Agent Runtime SA | prod | `/diagnosticpro/**` | Read |
| pipelinepilot | Agent Runtime SA | prod | `/pipelinepilot/**` | Read |
| All Projects | Analytics SA | prod | `/**` (metadata) | Read |

---

## Vertex AI Search Integration

### Current State (Phase 1)
**Primary Consumers:** Bob + iam-senior-adk-devops-lead

**Implementation:**
```yaml
Vertex AI Search Datastore:
  Project: bobs-brain
  Datastore ID: org-knowledge-datastore
  Type: Unstructured
  Data Source:
    Type: Cloud Storage
    URI Pattern: gs://intent-org-knowledge-prod/bobs-brain/**
  Refresh: Daily (configurable)
```

**Agent Wiring:**
```python
# In agents/shared_tools/local_builtins.py
def get_vertex_ai_search_tool():
    if os.getenv("USE_ORG_KNOWLEDGE", "false") == "true":
        # New org-wide knowledge hub
        datastore_config = {
            "project_id": "bobs-brain",
            "datastore_id": "org-knowledge-datastore",
            "location": "us"
        }
    else:
        # Legacy datastore (fallback)
        datastore_config = {...}

    return VertexAiSearchToolset(**datastore_config)
```

### Bob RAG Path (Concrete Wiring)

**Data Flow:**
```
1. Knowledge Storage:
   └── gs://datahub-intent/bobs-brain/**
       ├── /adk-docs/       # ADK documentation
       ├── /agent-patterns/ # Agent design patterns
       └── /department-kb/  # Department knowledge

2. Vertex AI Search Datastores:
   ├── Production:
   │   └── bobs-brain-prod-rag
   │       ├── Project: bobs-brain (205354194989)
   │       ├── Source: gs://datahub-intent/bobs-brain/**
   │       └── Type: unstructured
   │
   └── Staging:
       └── bobs-brain-staging-rag
           ├── Project: bobs-brain (205354194989)
           ├── Source: gs://datahub-intent-dev/bobs-brain/**
           └── Type: unstructured

3. ADK Tool Integration:
   └── VertexAiSearchToolset
       ├── Bob: Uses based on APP_ENV
       └── Foreman: Same tool, same datastore
```

### Staging vs Production Configuration

| Environment | Bucket | Datastore ID | Project | Use Case |
|------------|---------|--------------|---------|----------|
| **Production** | gs://datahub-intent/bobs-brain/** | bobs-brain-prod-rag | bobs-brain | Live agents |
| **Staging** | gs://datahub-intent-dev/bobs-brain/** | bobs-brain-staging-rag | bobs-brain | Testing |
| **Development** | gs://datahub-intent-dev/bobs-brain/** | bobs-brain-dev-rag | bobs-brain-dev | Local dev |

**Environment Selection:**
- Based on `APP_ENV` environment variable
- Falls back to `ENVIRONMENT` if not set
- Defaults to "staging" if neither set (safe default)

### Future State (Phase 2+)

**Multi-Product Pattern:**
```
Project: diagnosticpro
└── Vertex AI Search Datastore
    └── Data Source: gs://intent-org-knowledge-prod/diagnosticpro/**

Project: pipelinepilot
└── Vertex AI Search Datastore
    └── Data Source: gs://intent-org-knowledge-prod/pipelinepilot/**
```

**Shared Knowledge Access:**
- Products can optionally index `/shared/**` prefix
- Cross-product knowledge graph capabilities
- Federated search across multiple datastores

---

## Migration Strategy

### Phase 1: Foundation (Current)
- [x] Create knowledge hub project (`intent-knowledge-hub` → maps to existing `datahub-intent`)
- [x] Set up bucket structure
- [ ] Configure initial IAM for bobs-brain

### Phase 2: Bob Migration
- [ ] Create org-knowledge-datastore in Vertex AI Search
- [ ] Wire Bob + foreman to new datastore
- [ ] Import existing 8,718 documents
- [ ] Test with feature flag

### Phase 3: Expansion
- [ ] Add diagnosticpro prefix and IAM
- [ ] Add pipelinepilot prefix and IAM
- [ ] Create per-product datastores

### Phase 4: Advanced Features
- [ ] Implement IAM conditions for prefix isolation
- [ ] Add data lifecycle policies
- [ ] Set up cross-region replication
- [ ] Enable audit logging

---

## Security & Compliance

### Data Classification
```
gs://intent-org-knowledge-prod/
├── bobs-brain/          [INTERNAL]
├── iam-agents/          [INTERNAL]
├── diagnosticpro/       [CONFIDENTIAL - Customer Data]
├── pipelinepilot/       [CONFIDENTIAL - Sales Data]
└── shared/compliance/   [RESTRICTED - Compliance Docs]
```

### Security Controls
1. **Uniform Bucket-Level Access** - No ACLs, IAM only
2. **Encryption at Rest** - Google-managed keys (default)
3. **Versioning** - Enabled for prod bucket
4. **Audit Logging** - Cloud Audit Logs for all access
5. **DLP Scanning** - Optional for sensitive prefixes

### Compliance Considerations
- **Data Residency** - Single region (us-central1) or multi-region (us)
- **Retention** - 7-year default, configurable per prefix
- **Right to Delete** - Soft deletes with 30-day recovery
- **Access Reviews** - Quarterly IAM audit

---

## Cost Optimization

### Storage Tiers
```
Active Knowledge (Standard): ~100GB
├── Current documentation
├── Active patterns
└── Recent data

Archive Knowledge (Nearline): ~500GB
├── Historical versions
├── Old patterns
└── Compliance archives

Cold Storage (Archive): ~1TB
└── Long-term compliance only
```

### Estimated Costs
| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| Storage (Standard) | $2.00 | 100GB @ $0.020/GB |
| Storage (Nearline) | $5.00 | 500GB @ $0.010/GB |
| Vertex AI Search | $0.00 | 5GB free tier |
| Network Egress | $10.00 | Cross-region access |
| **Total** | **$17.00** | Per month estimate |

---

## Operational Considerations

### Monitoring & Alerts
```yaml
Alerts:
  - Storage quota > 80%
  - IAM changes (break-glass)
  - Unusual access patterns
  - Vertex AI Search indexing failures

Metrics:
  - Storage usage by prefix
  - Access frequency by SA
  - Search query performance
  - Cost by project allocation
```

### Backup & Recovery
- **RPO:** 24 hours (daily snapshots)
- **RTO:** 1 hour (restore from snapshot)
- **Cross-Region:** Async replication to us-east1
- **Versioning:** 30-day retention

### Maintenance Windows
- **Indexing:** Daily 2 AM PST
- **Lifecycle:** Weekly Sunday 3 AM PST
- **IAM Sync:** On-demand only

---

## Future Enhancements

### Near Term (Q1 2025)
- [ ] Implement IAM conditions for strict prefix isolation
- [ ] Add Cloud DLP scanning for PII detection
- [ ] Enable CMEK for encryption
- [ ] Set up BigQuery external tables for analytics

### Medium Term (Q2 2025)
- [ ] Multi-region active-active setup
- [ ] Implement knowledge graph relationships
- [ ] Add semantic deduplication
- [ ] Create self-service onboarding

### Long Term (2025+)
- [ ] Federated search across all products
- [ ] ML-powered knowledge curation
- [ ] Automated compliance classification
- [ ] Real-time knowledge streaming

---

## Implementation Checklist

### Phase K1 Deliverables ✅
- [x] Architecture document (this file)
- [x] GCP project layout definition
- [x] IAM model specification
- [x] Vertex AI Search integration plan
- [x] Migration strategy

### Phase K2 Deliverables (Next)
- [ ] Terraform knowledge_hub.tf module
- [ ] Variables for cross-project IAM
- [ ] Environment-specific configurations
- [ ] Infrastructure README
- [ ] Deployment runbook

---

## Appendix: Terraform Variable Mappings

For organizations adopting this pattern, use these variable mappings:

| Conceptual Name | Terraform Variable | Example Value |
|----------------|-------------------|---------------|
| Knowledge Hub Project | `var.knowledge_hub_project_id` | `datahub-intent` |
| Dev Bucket | `var.knowledge_bucket_dev` | `intent-org-knowledge-dev` |
| Prod Bucket | `var.knowledge_bucket_prod` | `intent-org-knowledge-prod` |
| Bob Runtime SA | `var.bobs_brain_runtime_sa` | `bob-runtime@bobs-brain.iam` |
| Search Service SA | `var.vertex_search_sa` | `search@bobs-brain.iam` |

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-20
**Status:** Architecture Approved, Implementation Pending
**Owner:** ADK Department Build Captain

---