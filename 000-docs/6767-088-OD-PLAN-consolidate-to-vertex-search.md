# 6767-088-OD-PLAN-consolidate-to-vertex-search

**Title:** Consolidate All Data to Single Vertex AI Search Datastore
**Category:** OD (Operations & Deployment)
**Type:** PLAN
**Status:** Active
**Created:** 2025-11-19
**Author:** Build Captain

## Executive Summary

Consolidate all scattered GCS buckets into the existing Vertex AI Search datastore (`bob-vertex-agent-datastore`) to eliminate data duplication and provide a single source of truth for agent grounding.

## Current State

### Vertex AI Search Datastore (KEEP)
- **ID:** `bob-vertex-agent-datastore`
- **Status:** Active with 8,718 documents, 109.87 MiB
- **Type:** Structured data, US region
- **Purpose:** Central knowledge base for all agents

### GCS Buckets (TO CONSOLIDATE/DELETE)
| Bucket | Size | Status | Action |
|--------|------|--------|--------|
| bobs-brain-bob-vertex-agent-rag | 115 MB | Has data | Import to Vertex AI Search, then delete |
| bobs-brain-knowledge | 0 B | Empty | Delete |
| bobs-brain-adk-staging | 0 B | Empty | Delete |
| bobs-brain-bob-vertex-agent-logs | 0 B | Empty | Delete |
| *Unknown large bucket* | 77,000+ items | Has massive data | **HANDLE LAST** - Needs investigation |

### Issues Found
- 326 files across buckets with some duplicates
- Data scattered across multiple buckets
- Empty buckets consuming namespace

## Consolidation Plan

### Phase 1: Import RAG Data
1. Import 115 MB from `bobs-brain-bob-vertex-agent-rag` to Vertex AI Search
2. Use incremental mode to avoid overwriting existing 8,718 documents
3. Verify import success in console

### Phase 2: Add ADK Documentation
Import these ADK docs to the datastore:
- ADK Tools documentation (6 pages)
- Chain-of-Thought research paper
- All stored under structured categories

### Phase 3: Delete Empty Buckets
After verification:
```bash
gsutil rm -r gs://bobs-brain-knowledge
gsutil rm -r gs://bobs-brain-adk-staging
gsutil rm -r gs://bobs-brain-bob-vertex-agent-logs
```

### Phase 4: Delete RAG Bucket
After confirming import:
```bash
gsutil rm -r gs://bobs-brain-bob-vertex-agent-rag
```

## Final Architecture

```
bob-vertex-agent-datastore (Vertex AI Search)
├── Existing documents (8,718)
├── RAG documents (from bucket import)
├── ADK documentation
│   ├── Tools docs
│   ├── Custom tools docs
│   └── GCP integration docs
└── Research papers
```

**Result:** ONE datastore, NO duplicate buckets

## Scripts Created

1. **verify_no_duplicates.sh** - Check for duplicate data
2. **consolidate_to_vertex_search.sh** - Consolidation commands
3. **import_to_vertex_search.py** - Python import script
4. **cleanup_empty_buckets.sh** - Safe bucket deletion

## Execution Steps

```bash
# Step 1: Verify current state
bash scripts/bucket_consolidation/verify_no_duplicates.sh

# Step 2: Import to Vertex AI Search
python3 scripts/bucket_consolidation/import_to_vertex_search.py

# Step 3: Clean up empty buckets
bash scripts/bucket_consolidation/cleanup_empty_buckets.sh

# Step 4: After verifying import, delete RAG bucket
gsutil rm -r gs://bobs-brain-bob-vertex-agent-rag
```

## Success Criteria

- [ ] All RAG data imported to Vertex AI Search
- [ ] ADK documentation added to datastore
- [ ] Empty buckets deleted
- [ ] RAG bucket deleted after import
- [ ] Zero GCS buckets with "bobs-brain" prefix (except system buckets)
- [ ] All agents using Vertex AI Search for grounding

## Benefits

1. **Single source of truth** - All knowledge in one place
2. **No duplication** - Eliminates redundant data
3. **Cost savings** - No empty bucket overhead
4. **Better search** - Vertex AI Search provides better retrieval
5. **Simplified management** - One datastore to maintain

## Risks and Mitigation

| Risk | Mitigation |
|------|------------|
| Data loss during migration | Use incremental import, verify before deletion |
| Import failures | Check permissions, use Python client as backup |
| Accidental deletion | Multi-step confirmation in scripts |

## Console Links

- [Vertex AI Search Datastore](https://console.cloud.google.com/vertex-ai/search/dataStores/bob-vertex-agent-datastore)
- [GCS Buckets](https://console.cloud.google.com/storage/browser?project=bobs-brain)

---

**Status:** Ready to execute
**Priority:** High (eliminates data sprawl)
**Impact:** Consolidates ~115 MB data, deletes 4 buckets