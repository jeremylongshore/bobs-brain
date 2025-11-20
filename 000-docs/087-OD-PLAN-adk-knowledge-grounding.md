# 087-OD-PLAN-adk-knowledge-grounding

**Title:** ADK Documentation Grounding for Vertex AI Agents
**Category:** OD (Operations & Deployment)
**Type:** PLAN
**Status:** Active
**Created:** 2025-11-19
**Author:** Build Captain

## Executive Summary

Plan to ingest all ADK documentation and research papers into GCS storage bucket for Vertex AI grounding, enabling Bob and the iam-* agents to access authoritative ADK knowledge directly through their search tools.

## Background

User has identified that all ADK documentation provided needs to be stored in the GCS bucket for grounding. They found:
- App Engine staging bucket: `bob-vertex-agent-datastore`
- Multiple buckets exist in the bobs-brain project
- Need for Vector Search integration with proper knowledge base

## Objectives

1. **Download and organize** all ADK documentation pages
2. **Store in GCS bucket** for Vertex AI grounding
3. **Configure metadata** for optimal search and retrieval
4. **Enable agent access** through existing search tools

## Documentation to Ingest

### ADK Core Documentation
- Tools Overview: https://google.github.io/adk-docs/tools/
- Built-in Tools: https://google.github.io/adk-docs/tools/built-in-tools/
- Custom Tools: https://google.github.io/adk-docs/tools-custom/
- Function Tools: https://google.github.io/adk-docs/tools-custom/function-tools/
- MCP Tools: https://google.github.io/adk-docs/tools-custom/mcp-tools/

### Google Cloud Integrations
- MCP Toolbox for Databases: https://google.github.io/adk-docs/tools/google-cloud/mcp-toolbox-for-databases/

### Research Papers
- Chain-of-Thought Prompting (arXiv:2201.11903): https://arxiv.org/pdf/2201.11903

## Storage Architecture

```
gs://bob-vertex-agent-datastore/
└── adk-grounding/
    ├── manifest.json              # Document manifest and metadata
    ├── tools/                     # Core ADK tools documentation
    │   ├── adk_tools_overview.html
    │   └── adk_builtin_tools.html
    ├── custom-tools/              # Custom tools documentation
    │   ├── adk_custom_tools.html
    │   ├── adk_function_tools.html
    │   └── adk_mcp_tools.html
    ├── gcp-tools/                 # GCP integration documentation
    │   └── mcp_toolbox_databases.html
    └── research/                  # Research papers
        └── chain_of_thought_prompting_2201.11903.pdf
```

## Implementation Steps

### Phase 1: Download Documentation
1. Use web scraping for HTML pages (BeautifulSoup/Playwright)
2. Direct download for PDF papers
3. Extract clean text/markdown from HTML
4. Preserve code examples and structure

### Phase 2: Process and Enrich
1. Add metadata for each document
2. Create searchable indices
3. Tag with relevant agent associations
4. Generate content hashes for versioning

### Phase 3: Upload to GCS
1. Create/verify bucket exists
2. Upload with proper directory structure
3. Set content-type metadata
4. Configure public/private access as needed

### Phase 4: Configure Vertex AI Search
1. Point Vertex AI Search to the GCS bucket
2. Configure indexing parameters
3. Set up refresh schedule
4. Test search functionality

### Phase 5: Wire Agent Access
1. Update IAM_INDEX_TOOLS to access the bucket
2. Configure Bob's search tools for grounding
3. Test knowledge retrieval from agents

## Metadata Schema

Each document will include:
```json
{
  "source_url": "https://...",
  "category": "tools|custom-tools|gcp-tools|research",
  "title": "Document Title",
  "description": "Brief description",
  "ingestion_timestamp": "2025-11-19T...",
  "content_hash": "sha256:...",
  "file_type": "html|pdf",
  "agent_relevance": ["bob", "iam-adk", "iam-index"],
  "tags": ["adk", "google-adk", "vertex-ai", ...]
}
```

## Scripts Created

1. **ingest_adk_docs.py** - Main ingestion orchestrator
2. **download.sh** - Downloads all documentation
3. **upload_to_gcs.sh** - Uploads to GCS bucket

## Success Criteria

- [ ] All 7 ADK documentation pages downloaded
- [ ] Research paper downloaded
- [ ] Documents processed to clean text/markdown
- [ ] Uploaded to GCS bucket with proper structure
- [ ] Metadata attached for searchability
- [ ] Vertex AI Search configured to index bucket
- [ ] Bob can query ADK knowledge through tools
- [ ] iam-index can manage the knowledge base

## Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| HTML scraping complexity | Medium | Use proper parsing libraries |
| Large document size | Low | Chunk documents if needed |
| Stale documentation | Medium | Set up refresh schedule |
| Access permissions | High | Verify IAM roles configured |

## Next Steps

1. Run `python scripts/knowledge_ingestion/ingest_adk_docs.py`
2. Execute download script
3. Process HTML to clean format
4. Upload to GCS
5. Configure Vertex AI Search
6. Test agent knowledge queries

## Notes

- The `bob-vertex-agent-datastore` bucket appears to already exist
- May need to coordinate with existing Vertex AI Search datastores
- Consider versioning strategy for documentation updates
- Plan for incremental updates as ADK docs evolve

---

**Status:** Ready for execution
**Priority:** High (enables proper ADK grounding)
**Dependencies:** GCS bucket access, Vertex AI Search configuration