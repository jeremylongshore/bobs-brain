# Circle of Life & Knowledge Integration Analysis

**Date:** 2025-10-05
**Project:** Bob's Brain v5
**Purpose:** Document Circle of Life system and knowledge graph integration strategy

---

## Executive Summary

Bob's Brain uses a **Circle of Life (CoL)** learning system that ingests events, analyzes patterns, generates LLM insights, persists to Neo4j/BigQuery, and applies learnings. This document analyzes how Jeremy's research knowledge base can integrate with this system.

---

## Circle of Life Architecture

### Current Implementation

**Location:** `src/circle_of_life.py`

**Flow:** ingest → analyze → llm insights → persist → apply

```python
class CircleOfLife:
    """Evidence-driven loop: ingest → analyze → llm insights → persist → apply"""

    def __init__(self, neo4j_driver=None, bq_client=None, llm_call=None, logger=None):
        self.driver = neo4j_driver      # Neo4j for graph storage
        self.bq = bq_client              # BigQuery for analytics (stub)
        self.llm_call = llm_call         # LLM for insight generation
```

### Five-Phase Process

**1. Ingest (Deduplication)**
- Accepts list of events
- Deduplicates using content hash (SHA-256)
- Batches up to 50 events (configurable via `BB_COL_BATCH`)

**2. Analyze (Pattern Detection)**
- Groups events by type
- Counts occurrences
- Samples first 3 for context

**3. Generate Insights (LLM)**
- Sends analysis to LLM
- Requests structured JSON: `[{pattern, action, confidence}]`
- Retries 3 times with exponential backoff

**4. Persist (Storage)**
- **Neo4j:** Stores high-confidence insights (>0.6 default)
- **BigQuery:** Stub for future analytics
- Creates `Insight` nodes with pattern, action, confidence, timestamp

**5. Apply (Execution)**
- Counts insights above confidence threshold
- Returns metrics on what was applied

### Configuration

```bash
# Environment variables
BB_CONFIDENCE_MIN=0.6      # Minimum confidence to persist (default: 0.6)
BB_COL_BATCH=50           # Max events per batch (default: 50)
BB_COL_COOLDOWN=60        # Seconds between runs (default: 60)
```

---

## Current Knowledge Storage

### Backend Architecture

**From `src/providers.py`:**

```python
# Bob's Brain storage backends
STATE_BACKEND = sqlite|postgres      # Conversation state
VECTOR_BACKEND = chroma|pgvector|pinecone  # Semantic search
GRAPH_BACKEND = none|neo4j           # Knowledge graph
CACHE_BACKEND = none|redis           # Fast lookups
ARTIFACT_BACKEND = local|s3          # File storage
```

### Circle of Life Storage

**Neo4j Schema:**
```cypher
(i:Insight {
    id: "<sha256-hash>",
    pattern: "Users ask about X frequently",
    action: "Create FAQ entry for X",
    confidence: 0.85,
    ts: <timestamp>
})
```

---

## Research Knowledge Integration Strategy

### Jeremy's Research Corpus

**Location:** `~/research/`

**Key Documents:**
- `knowledge-graph-research-system-report.md` - ChromaDB vs Neo4j analysis
- `advanced-rag-architecture-analysis.md` - RAG system design
- `ai-token-broker-analysis.md` - LLM gateway patterns
- `modern-multi-agent-architecture-blueprint.md` - Agent design
- Plus 10+ more strategic analysis docs

### Integration Options

#### Option 1: ChromaDB Research Collection (RECOMMENDED)

**Rationale:**
- Bob already uses ChromaDB for vector storage
- Semantic search perfect for research queries
- Fast local queries, zero API costs
- Easy RAG integration

**Implementation:**
```python
# Extend src/providers.py vector_store()
research_collection = chroma_client.create_collection(
    name="jeremy_research",
    metadata={"description": "Strategic AI research documents"}
)

# Index all research docs
for doc in research_docs:
    research_collection.add(
        documents=[doc.content],
        metadatas=[{
            "title": doc.title,
            "date": doc.date,
            "topics": doc.topics,
            "file_path": doc.path
        }],
        ids=[doc.hash]
    )
```

**Bob Enhancement:**
```python
# New endpoint in src/app.py
@app.post("/api/research")
def research_query():
    query = request.json.get("query")
    results = research_collection.query(
        query_texts=[query],
        n_results=5
    )
    return jsonify({"results": results})
```

#### Option 2: Neo4j Research Graph

**Rationale:**
- Complex relationships between research topics
- Temporal tracking of idea evolution
- Integration with Circle of Life insights

**Implementation:**
```cypher
# Research knowledge graph schema
(Research:Paper {
    title: "AI Token Broker Analysis",
    date: "2025-09-12",
    topics: ["llm-gateway", "cost-optimization"],
    file_path: "/home/jeremy/research/ai-token-broker-analysis.md"
})

(Topic:Concept {name: "LLM Gateway"})
(Framework:Architecture {name: "Multi-Agent System"})

(Research)-[:DISCUSSES]->(Topic)
(Research)-[:IMPLEMENTS]->(Framework)
(Topic)-[:PART_OF]->(Framework)
(Research)-[:REFERENCES]->(Research)  # Cross-references
```

**Circle of Life Integration:**
```cypher
# Link insights to research
(Insight)-[:INFORMED_BY]->(Research)
(Insight)-[:APPLIES]->(Topic)
```

#### Option 3: Hybrid System (OPTIMAL)

**ChromaDB:** Semantic search for "find research about X"
**Neo4j:** Relationship tracking for "how does X relate to Y"
**Circle of Life:** Learn which research is most useful

**Flow:**
1. User asks Bob about topic
2. ChromaDB finds relevant research docs
3. Neo4j provides relationship context
4. Circle of Life tracks which research was helpful
5. Future queries prioritize high-value research

---

## Proposed Implementation Plan

### Phase 1: ChromaDB Research Index (Week 1)

**Tasks:**
1. Create research ingestion script
2. Add `jeremy_research` collection to ChromaDB
3. Index all 17 research markdown files
4. Create `/api/research` endpoint
5. Test semantic search queries

**Expected Results:**
- Fast research queries (<100ms)
- Semantic matching (not just keyword)
- Zero API costs

### Phase 2: Circle of Life Enhancement (Week 2)

**Tasks:**
1. Track which research docs are accessed
2. Learn which topics users ask about
3. Pre-load relevant research for common queries
4. Auto-suggest related research

**Circle of Life Events:**
```python
{
    "type": "research_query",
    "query": "LLM gateway patterns",
    "docs_returned": ["ai-token-broker-analysis.md"],
    "user_satisfaction": 0.9
}
```

**Insights Generated:**
```json
{
    "pattern": "Users frequently ask about LLM gateway patterns",
    "action": "Pre-load ai-token-broker-analysis.md for gateway queries",
    "confidence": 0.85
}
```

### Phase 3: Neo4j Knowledge Graph (Week 3-4)

**Tasks:**
1. Extract entities from research docs
2. Build research topic graph
3. Link insights to research sources
4. Create relationship queries

**Benefits:**
- "Show me all research related to multi-agent systems"
- "What papers influenced Bob's architecture?"
- "How does ternary quantization relate to token optimization?"

---

## Technical Implementation

### Research Ingestion Script

**Location:** `scripts/research/ingest-research-docs.py`

```python
#!/usr/bin/env python3
"""Ingest Jeremy's research docs into Bob's knowledge base"""

import os
from pathlib import Path
from src.providers import vector_store

def ingest_research():
    """Index all research markdown files"""
    research_dir = Path.home() / "research"
    chroma = vector_store()

    collection = chroma.get_or_create_collection("jeremy_research")

    for md_file in research_dir.glob("*.md"):
        if md_file.name == "README.md":
            continue

        content = md_file.read_text()

        # Extract metadata from frontmatter or filename
        date = extract_date(md_file.name)
        topics = extract_topics(content)

        collection.add(
            documents=[content],
            metadatas=[{
                "title": md_file.stem,
                "date": date,
                "topics": topics,
                "file_path": str(md_file)
            }],
            ids=[md_file.stem]
        )

    print(f"✅ Indexed {len(list(research_dir.glob('*.md')))} research docs")

if __name__ == "__main__":
    ingest_research()
```

### Bob Research Query Function

**Location:** `src/skills/research.py`

```python
"""Research query skill for Bob's Brain"""

from src.providers import vector_store

def search_research(query: str, n_results: int = 5):
    """Search Jeremy's research knowledge base"""
    chroma = vector_store()
    collection = chroma.get_collection("jeremy_research")

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return {
        "query": query,
        "results": [
            {
                "title": meta["title"],
                "excerpt": doc[:500],
                "relevance": distance,
                "file_path": meta["file_path"]
            }
            for doc, meta, distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    }
```

---

## Expected Benefits

### Immediate (Phase 1)

- ✅ **Fast research access** - Bob can answer questions from Jeremy's research
- ✅ **Semantic search** - Find research by concept, not just keywords
- ✅ **Zero cost** - All local, no API calls
- ✅ **Privacy** - Research stays on your infrastructure

### Medium-term (Phase 2)

- ✅ **Learning system** - Circle of Life tracks valuable research
- ✅ **Predictive loading** - Bob anticipates research needs
- ✅ **Usage analytics** - Know which research is most valuable
- ✅ **Auto-summarization** - Bob summarizes research on demand

### Long-term (Phase 3)

- ✅ **Knowledge graph** - Complex relationship tracking
- ✅ **Insight linking** - Connect Bob's learnings to research sources
- ✅ **Research discovery** - Find related papers automatically
- ✅ **Public sharing** - Optional llms.txt export for public access

---

## Research Docs Relevant to Bob's Brain

### Architecture & Design

**Core Documents:**
- `modern-multi-agent-architecture-blueprint.md` - Bob's architecture inspiration
- `modular-agent-ship-architecture-vision.md` - Modular design patterns
- `optimal-containerized-agent-architecture.md` - Deployment strategies

### Knowledge Systems

**Core Documents:**
- `knowledge-graph-research-system-report.md` - This integration strategy
- `advanced-rag-architecture-analysis.md` - RAG implementation patterns

### Cost Optimization

**Core Documents:**
- `ai-token-broker-analysis.md` - LLM gateway and routing
- `bitcoin-standard-for-ai-compute-economy.md` - Cost modeling
- `standardized-token-cost-index-blueprint.md` - Cost tracking

### Integration Patterns

**Core Documents:**
- `claude-tool-building-methodology.md` - Tool design (Bob's skills)
- `existing-multi-agent-architecture-analysis.md` - Multi-agent coordination

---

## Next Actions

### Immediate (Do First)

1. **Copy research docs to claudes-docs/** ✅ (knowledge graph report copied)
2. **Create research ingestion script** (scripts/research/ingest-research-docs.py)
3. **Test ChromaDB research collection** (verify semantic search works)
4. **Add /api/research endpoint** (src/app.py)

### Short-term (This Week)

5. **Index all 17 research markdown files**
6. **Test research queries via Bob**
7. **Document usage in CLAUDE.md**
8. **Add Circle of Life research tracking**

### Medium-term (Next Sprint)

9. **Build Neo4j research graph**
10. **Link insights to research sources**
11. **Create research recommendation system**
12. **Export llms.txt for public access (optional)**

---

## Success Metrics

**Week 1:**
- ✅ 17+ research docs indexed
- ✅ <100ms research query response time
- ✅ >90% semantic search accuracy

**Week 2:**
- ✅ Circle of Life tracking research usage
- ✅ Auto-suggestions for related research
- ✅ 50+ research queries handled

**Week 3-4:**
- ✅ Neo4j research graph complete
- ✅ Cross-reference queries working
- ✅ Public llms.txt exported (optional)

---

## Conclusion

Bob's Brain's **Circle of Life** system provides the perfect foundation for integrating Jeremy's research knowledge base. By combining:

1. **ChromaDB** for semantic search
2. **Neo4j** for relationship tracking
3. **Circle of Life** for learning which research is valuable

We create a self-improving research-aware AI assistant that learns from Jeremy's strategic analysis while maintaining privacy and zero ongoing costs.

**Status:** Ready for Phase 1 implementation
**Priority:** High - Enhances Bob's knowledge and reduces duplicate research
**Risk:** Low - Extends existing infrastructure

---

**Document Created:** 2025-10-05
**Related Docs:**
- `~/research/knowledge-graph-research-system-report.md`
- `src/circle_of_life.py`
- `src/providers.py`
- `claudes-docs/plans/2025-10-05_ternary-integration-guide.md`
