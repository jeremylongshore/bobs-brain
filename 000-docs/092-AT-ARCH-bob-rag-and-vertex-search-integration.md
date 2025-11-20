# 092-AT-ARCH-bob-rag-and-vertex-search-integration.md

**Date Created:** 2025-11-20
**Category:** AT - Architecture & Technical
**Type:** ARCH - Architecture Document
**Status:** IMPLEMENTATION READY ✅

---

## Executive Summary

This document describes the concrete RAG (Retrieval Augmented Generation) implementation for Bob and the foreman (iam-senior-adk-devops-lead) using Vertex AI Search and the org-wide knowledge hub. It defines the exact wiring, tool integration, and environment management for production-ready RAG capabilities.

---

## RAG Architecture Overview

### Data Flow
```
1. Knowledge Sources → GCS Bucket → Vertex AI Search → ADK Tool → Agent Response

Specifically:
- Source: gs://datahub-intent/bobs-brain/**
- Index: Vertex AI Search Datastore (bobs-brain-prod-rag)
- Tool: VertexAiSearchToolset (ADK)
- Agents: Bob + Foreman
```

### Key Components

| Component | Production | Staging | Development |
|-----------|-----------|---------|-------------|
| **Bucket** | gs://datahub-intent | gs://datahub-intent-dev | gs://datahub-intent-dev |
| **Prefix** | /bobs-brain/ | /bobs-brain/ | /bobs-brain/ |
| **Datastore** | bobs-brain-prod-rag | bobs-brain-staging-rag | bobs-brain-dev-rag |
| **Project** | bobs-brain (205354194989) | bobs-brain | bobs-brain-dev |
| **Refresh** | Daily | Hourly | Manual |

---

## Tool Integration

### Bob's RAG Usage Pattern

**When Bob should use Vertex Search:**
1. **Architecture questions** - "How should I structure an ADK agent?"
2. **Pattern lookups** - "What's the best practice for X?"
3. **Department knowledge** - "What did we decide about Y?"
4. **Historical context** - "What was the outcome of phase Z?"

**Tool invocation flow:**
```python
# Bob's thought process (conceptual)
if user_asks_about_architecture or patterns or best_practices:
    results = vertex_search_tool.search(query)
    context = summarize(results)
    response = generate_with_context(context, user_question)
```

### Foreman's RAG Usage Pattern

**When foreman should use Vertex Search:**
1. **ADK compliance audits** - Checking patterns against docs
2. **Design reviews** - Validating architectural decisions
3. **Knowledge updates** - Finding what needs indexing
4. **Department standards** - Ensuring consistency

**Tool invocation flow:**
```python
# Foreman's audit process (conceptual)
if conducting_audit or design_review:
    standard = vertex_search_tool.search("ADK pattern for " + topic)
    actual = analyze_code(repository)
    drift = compare(standard, actual)
    return IssueSpec(drift) if drift else "Compliant"
```

---

## Implementation Details

### 1. Vertex Search Tool Factory
**Location:** `agents/shared_tools/vertex_search.py`

**Key Functions:**
- `get_bob_vertex_search_tool(env)` - Returns configured tool for Bob
- `get_foreman_vertex_search_tool(env)` - Returns configured tool for foreman
- `get_current_environment()` - Determines env from APP_ENV/ENVIRONMENT

**Configuration Source:** `config/vertex_search.yaml`

### 2. Tool Profile Integration
**Location:** `agents/shared_tools/__init__.py`

**Bob's Tools:**
```python
BOB_TOOLS = [
    get_google_search_tool(),        # Web search
    get_bob_vertex_search_tool(),    # RAG (org hub)
    get_adk_docs_tools(),            # ADK patterns
    get_delegation_tools()           # Foreman delegation
]
```

**Foreman's Tools:**
```python
FOREMAN_TOOLS = [
    get_foreman_vertex_search_tool(), # RAG (same as Bob)
    get_delegation_tools(),          # Specialist delegation
    get_google_search_tool()         # Web search
]
```

### 3. Environment Selection

**Priority Order:**
1. `APP_ENV` environment variable
2. `ENVIRONMENT` environment variable
3. Default: "staging" (safe default)

**Normalization:**
- "prod", "production" → "production"
- "dev", "development" → "development"
- Everything else → "staging"

---

## Migration Strategy

### Phase 1: Legacy Support (Current)
```bash
# Default behavior - use existing datastore
export USE_ORG_KNOWLEDGE=false
# Bob uses: bob-vertex-agent-datastore (8,718 docs)
```

### Phase 2: Testing New Hub
```bash
# Enable org knowledge hub
export USE_ORG_KNOWLEDGE=true
export APP_ENV=staging
# Bob uses: bobs-brain-staging-rag → gs://datahub-intent-dev
```

### Phase 3: Production Rollout
```bash
# Production with org hub
export USE_ORG_KNOWLEDGE=true
export APP_ENV=production
# Bob uses: bobs-brain-prod-rag → gs://datahub-intent
```

---

## Datastore Setup Commands

### Create Datastores
```bash
# Production datastore
gcloud ai search datastores create bobs-brain-prod-rag \
    --location=us \
    --project=bobs-brain \
    --type=unstructured

# Staging datastore
gcloud ai search datastores create bobs-brain-staging-rag \
    --location=us \
    --project=bobs-brain \
    --type=unstructured
```

### Import Knowledge
```bash
# Import to production
gcloud ai search documents import \
    --datastore=bobs-brain-prod-rag \
    --location=us \
    --project=bobs-brain \
    --gcs-uri=gs://datahub-intent/bobs-brain/**

# Import to staging
gcloud ai search documents import \
    --datastore=bobs-brain-staging-rag \
    --location=us \
    --project=bobs-brain \
    --gcs-uri=gs://datahub-intent-dev/bobs-brain/**
```

---

## Configuration Verification

### Dry-Run Script
Use the provided script to verify configuration without API calls:

```bash
python scripts/print_rag_config.py

# Expected output:
Environment: staging
Datastore: bobs-brain-staging-rag
Project: bobs-brain
Source: gs://datahub-intent-dev/bobs-brain/**
```

### Tool Availability Check
```python
from agents.shared_tools import BOB_TOOLS

# Check if Vertex Search is configured
vertex_tools = [t for t in BOB_TOOLS if t.get("type") == "vertex_search"]
print(f"Vertex Search configured: {len(vertex_tools) > 0}")
```

---

## Monitoring & Validation

### Key Metrics
- **Search latency** - Should be < 500ms
- **Result relevance** - Track user feedback
- **Index freshness** - Monitor last update time
- **Query volume** - Track usage patterns

### Validation Checks
1. **Environment correct:** `echo $APP_ENV`
2. **Migration flag:** `echo $USE_ORG_KNOWLEDGE`
3. **Datastore exists:** `gcloud ai search datastores describe DATASTORE_ID`
4. **Documents indexed:** Check document count in console

---

## Troubleshooting

### Common Issues

**"No Vertex Search tool available"**
- Check: `USE_ORG_KNOWLEDGE` environment variable
- Check: `config/vertex_search.yaml` exists and valid
- Check: `APP_ENV` is set correctly

**"No results from search"**
- Verify: Datastore has documents imported
- Check: GCS bucket has content at expected prefix
- Confirm: Search patterns match document content

**"Wrong environment datastore"**
- Verify: `APP_ENV` is set correctly
- Check: No hardcoded datastore IDs in code
- Confirm: Config file has all environments defined

---

## Security Considerations

1. **Read-only access** - Agents only read from buckets
2. **Prefix isolation** - Each project limited to its prefix
3. **No credentials in code** - All via environment/IAM
4. **Audit logging** - All searches logged in Cloud Audit

---

## Future Enhancements

### Near Term
- [ ] Add search result caching
- [ ] Implement relevance scoring
- [ ] Add query rewriting for better results

### Long Term
- [ ] Multi-modal search (code + docs)
- [ ] Semantic deduplication
- [ ] Cross-project knowledge federation

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-20
**Status:** Ready for Implementation
**Owner:** ADK Department Build Captain

---