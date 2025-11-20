# iam-index - Knowledge Management Specialist

**Version:** 0.1.0
**Status:** In Development
**Type:** Knowledge Management & Search Specialist

## Overview

The `iam-index` agent serves as the Knowledge Management Specialist for the ADK/Agent Engineering Department. It manages documentation indexing, maintains the knowledge base, and provides search capabilities through Vertex AI Search integration.

## Position in Department

```
iam-senior-adk-devops-lead (Foreman)
    ↓
iam-index (Knowledge Management) ← You are here
    ↓
Provides knowledge to all iam-* agents
```

## Responsibilities

### Primary Functions
1. **Documentation Indexing** - Index ADK docs and project documentation
2. **Knowledge Queries** - Answer search queries from all agents
3. **Pattern Cataloging** - Maintain searchable code patterns
4. **Gap Analysis** - Identify missing or outdated knowledge
5. **Search Optimization** - Maintain high relevance and performance

### Knowledge Sources
- Official ADK documentation
- Vertex AI documentation
- Project documentation (000-docs/)
- Agent implementations and patterns
- A2A protocol specifications

## Tools Available

### 1. index_adk_docs
Index official ADK documentation for semantic search.
```python
result = index_adk_docs("google.github.io/adk-docs")
# Returns: Indexing status and statistics
```

### 2. index_project_docs
Index project-specific documentation from 000-docs/.
```python
result = index_project_docs("000-docs")
# Returns: List of indexed documents with metadata
```

### 3. query_knowledge_base
Search the indexed knowledge base.
```python
result = query_knowledge_base("dual memory wiring", max_results=5)
# Returns: Ranked search results with snippets
```

### 4. sync_vertex_search
Synchronize with Vertex AI Search datastore.
```python
result = sync_vertex_search("adk-documentation")
# Returns: Sync status and statistics
```

### 5. generate_index_entry
Create IndexEntry objects for new content.
```python
result = generate_index_entry(
    title="A2A Protocol Guide",
    source="000-docs/6767-045-AT-ARCH-a2a-protocol.md",
    content_type="doc",
    summary="Complete A2A implementation guide"
)
# Returns: IndexEntry object
```

### 6. analyze_knowledge_gaps
Identify missing or outdated documentation.
```python
result = analyze_knowledge_gaps(scope="agents")
# Returns: Gap analysis report with recommendations
```

## Technical Implementation

### Base Architecture
- **Framework:** Google ADK LlmAgent
- **Model:** Gemini 2.0 Flash
- **Memory:** Dual memory (Session + Memory Bank)
- **Runtime:** Vertex AI Agent Engine
- **Search:** Vertex AI Search integration

### Configuration
```bash
# Required environment variables
PROJECT_ID=your-gcp-project
LOCATION=us-central1
AGENT_ENGINE_ID=your-engine-id
APP_NAME=iam-index
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/iam-index/dev/us-central1/0.1.0

# Optional
VERTEX_SEARCH_DATASTORE_ID=adk-documentation
```

## Quality Standards

### Performance Metrics
- **Query Response:** < 1 second
- **Search Relevance:** > 90% accuracy
- **Index Freshness:** < 24 hours
- **Coverage:** 100% of core docs

### Data Quality
- Proper metadata for all entries
- Clear source attribution
- Accurate timestamps
- Relevant keywords and tags

## Integration Points

### Provides Knowledge To
- **iam-adk** - ADK patterns and examples
- **iam-fix-plan** - Solution patterns
- **iam-qa** - Test patterns and guidelines
- **iam-doc** - Gap reports for documentation
- **All agents** - On-demand knowledge queries

### Knowledge Sources From
- ADK official documentation
- Project 000-docs/
- Agent implementations
- Vertex AI documentation

## Hard Mode Compliance (R1-R8)

| Rule | Status | Implementation |
|------|--------|---------------|
| R1 | ✅ | ADK-only with LlmAgent |
| R2 | ✅ | Vertex AI Agent Engine runtime |
| R3 | ✅ | No Runner in service layers |
| R4 | ✅ | CI-only deployment guard |
| R5 | ✅ | Dual memory wiring |
| R6 | ✅ | Single 000-docs folder |
| R7 | ✅ | SPIFFE ID in all logs |
| R8 | ✅ | Drift detection compatible |

## Development Status

### Current Phase
- [x] Agent scaffold created
- [x] Tools implemented (6/6)
- [x] System prompt defined
- [x] A2A card configured
- [ ] Vertex AI Search wiring
- [ ] Production indexing
- [ ] Integration tests

### Next Steps
1. Wire actual Vertex AI Search datastore
2. Index all ADK documentation
3. Create knowledge update pipeline
4. Add monitoring and metrics
5. Implement caching layer

## Testing

### Smoke Test
```python
from agents.iam_index.agent import get_agent
agent = get_agent()
print(f"✅ iam-index agent created")
```

### Tool Testing
```python
from agents.iam_index.tools import query_knowledge_base
result = query_knowledge_base("ADK memory patterns")
print(f"Found {len(result['results'])} results")
```

## Deployment

### Via ADK CLI
```bash
adk deploy agent_engine agents.iam_index \
  --project bobs-brain-dev \
  --region us-central1 \
  --staging_bucket gs://bobs-brain-dev-adk-staging
```

### Via GitHub Actions
Automatic deployment on push to main branch.

## Monitoring

### Key Metrics
- Query latency (p50, p95, p99)
- Search relevance scores
- Index freshness
- Coverage percentage
- Gap detection rate

### Alerts
- Query latency > 2s
- Relevance score < 0.8
- Index staleness > 48h
- Coverage < 95%

## Troubleshooting

### Common Issues

**Issue:** Low search relevance
- Check index freshness
- Review query preprocessing
- Verify keyword extraction

**Issue:** Slow query response
- Check Vertex AI Search quota
- Review index size
- Optimize query patterns

**Issue:** Missing documentation
- Run gap analysis
- Check indexing logs
- Verify source accessibility

## Related Documentation

- [IndexEntry Contract](../iam_contracts.py)
- [Vertex AI Search Setup](../../scripts/deployment/setup_vertex_search.sh)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [000-docs Index](../../000-docs/README.md)

## Support

- **Department:** ADK/Agent Engineering
- **Repository:** bobs-brain
- **Status:** Active development