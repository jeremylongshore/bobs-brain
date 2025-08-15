# 🤖 Bob's Brain - AI Assistant with Vector Search & Knowledge Graph

## Current Development: Semantic Search Integration (August 14, 2025)

Bob's Brain is an intelligent assistant that combines:
- **Gemini 2.5 Flash** for natural language understanding
- **Neo4j Graph Database** for structured equipment knowledge
- **ChromaDB/FAISS** for semantic similarity search (IN PROGRESS)
- **Graphiti** for automatic knowledge extraction from conversations

## Current Working Session (tmux: deez)

```bash
# Attach to active development session
tmux attach -t deez

# Or start fresh with the production agent
cd /home/jeremylongshore/bobs-brain
python3 src/clean_agent.py  # Current production (no vector search yet)
```

## What We're Building Today

### The Problem: Semantic Similarity Gap
Bob currently can't understand when different words mean the same thing:
- User says: "engine won't start"
- Bob misses: "starter motor failure", "cranking issues", "no-start condition"

### The Solution: Hybrid Architecture
```
User Query → Semantic Search (ChromaDB) → Find similar meanings
          ↘ Graph Query (Neo4j) → Find relationships
                    ↓
              Combine contexts
                    ↓
            Gemini generates response
```

## New Vector Search Integration Files (August 14, 2025)

### Just Created Today
- `src/vector_enhanced_agent.py` - Hybrid Neo4j + ChromaDB search
- `src/fully_integrated_agent.py` - Complete Graphiti + Vector + Graph integration
- `src/faiss_comparison_demo.py` - Shows FAISS vs ChromaDB performance

### Current Production
- `src/clean_agent.py` - **CURRENT PRODUCTION** - Works but no vector search
- `src/bob_brain_enterprise.py` - Cloud Run version (Slack issues)

### Existing Infrastructure
- `src/graphiti_integration.py` - Graphiti framework (installed, not wired up)
- `src/graphiti_simple.py` - Simplified Graphiti without AI deps

## Technology Stack Status

### ✅ Installed & Ready
- **ChromaDB 1.0.15** - Vector database for semantic search
- **FAISS-cpu 1.11.0** - Facebook's similarity search (ChromaDB uses this internally)
- **sentence-transformers 5.1.0** - Creates embeddings from text
- **graphiti-core 0.18.5** - Automatic entity/relationship extraction
- **Neo4j** - Graph database with 267 equipment nodes
- **Gemini 2.5 Flash** - Google's latest LLM

### ⚠️ Integration Status
| Component | Installed | Configured | Integrated | Production |
|-----------|-----------|------------|------------|------------|
| Neo4j | ✅ | ✅ | ✅ | ✅ |
| Gemini | ✅ | ✅ | ✅ | ✅ |
| ChromaDB | ✅ | ⚠️ | ❌ | ❌ |
| FAISS | ✅ | N/A | Via ChromaDB | ❌ |
| Graphiti | ✅ | ⚠️ | ❌ | ❌ |
| Sentence Transformers | ✅ | ✅ | ❌ | ❌ |

### 🎯 Next Steps
1. Wire up ChromaDB in `clean_agent.py`
2. Index existing Neo4j data into vectors
3. Enable Graphiti auto-extraction
4. Test semantic search with equipment queries

## Environment Variables

```bash
# Required
SLACK_BOT_TOKEN=xoxb-...        # From api.slack.com

# Optional
SLACK_APP_TOKEN=xapp-...        # For Socket Mode
SLACK_SIGNING_SECRET=...        # For webhooks
GOOGLE_API_KEY=...              # For GenAI fallback
CHROMA_PERSIST_DIR=./chroma_data  # Database location
PORT=8080                       # Health check port
```

## Deployment

### Local Testing
```bash
python3 src/bob_ultimate.py
```

### Cloud Run
```bash
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --project bobs-house-ai \
  --port 8080
```

## Architecture

```
Bob Ultimate
├── Slack Integration
│   ├── Socket Mode (development)
│   └── Webhook Mode (production)
├── AI Engine
│   ├── Vertex AI (primary)
│   └── Google GenAI (fallback)
├── Knowledge Base
│   ├── ChromaDB vectors
│   └── DiagnosticPro context
└── Safety Features
    ├── Duplicate prevention
    ├── Thread safety
    ├── Memory management
    └── Error recovery
```

## Version History

- **v1.0 ULTIMATE** - The final unified version (YOU ARE HERE)
- Previous: bob_unified_v2 (advanced but no AI)
- Previous: bob_production (good safety, complex)
- Previous: bob_solid (simple but limited)
- Previous: 4+ other experimental versions

## Status

✅ **READY TO USE** - Just needs Slack tokens!

Get tokens from: https://api.slack.com/apps

---

**CTO Decision**: This is THE Bob. All other versions are deprecated.
