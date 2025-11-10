# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ CRITICAL: Multiple Implementations

This repository contains **FOUR different implementations** of Bob's Brain:

1. **bob-vertex-agent/** (PRODUCTION - USE THIS ONE)
   - Vertex AI Agent Engine + Cloud Functions
   - Deployed to GCP Project: `bobs-brain`
   - Slack webhook: `https://slack-webhook-eow2wytafa-uc.a.run.app`
   - **See: `bob-vertex-agent/CLAUDE.md` for complete documentation**

2. **02-Src/** (Experimental Flask Implementation)
   - Flask app with modular LLM providers
   - Local development and testing
   - Not deployed to production

3. **adk-agent/** (Experimental)
   - Google ADK implementation
   - Reference implementation

4. **genkit-agent/** (Experimental)
   - Genkit implementation
   - Reference implementation

**When working on Bob's Brain production features, use `bob-vertex-agent/` directory!**

---

## Project Overview (Flask Implementation - 02-Src/)

**Note:** This section describes the experimental Flask implementation in `02-Src/`. For the production Vertex AI implementation, see `bob-vertex-agent/CLAUDE.md`.

Bob's Brain (Flask version) is a sovereign modular AI agent with pluggable LLM providers, configurable storage backends, and a Circle-of-Life learning loop. It's designed to be cloned and run anywhere—locally or in the cloud—with Slack integration as an optional feature.

## Architecture

### Core Philosophy
- **Provider-agnostic**: Swap between Claude (Anthropic), Gemini (Google), Groq, OpenRouter, or Ollama via env vars
- **Storage modularity**: State (sqlite/postgres), Vector (chroma/pgvector/pinecone), Graph (none/neo4j), Cache (none/redis), Artifacts (local/s3)
- **Multi-source knowledge**: LlamaIndex integration for ingesting docs, code, and structured data
- **Evidence-driven learning**: Circle-of-Life analyzes interactions, generates LLM insights, persists patterns to graph/analytics
- **API-first**: REST endpoints with API key auth, Prometheus metrics, health checks with backend probes

### Core Components
- **Main Service**: `02-Src/core/app.py` (symlink: `src/core/app.py`) - Flask app with API routes, auth, rate limiting, metrics
- **Providers**: `02-Src/core/providers.py` - LLM client factory, storage backend initialization
- **Circle of Life**: `02-Src/features/circle_of_life.py` - Learning pipeline (ingest → analyze → insights → persist → apply)
- **Knowledge Orchestrator**: `02-Src/features/knowledge_orchestrator.py` - LlamaIndex-powered multi-source knowledge integration
- **Smart Router**: `02-Src/features/smart_router.py` - Intelligent routing and task orchestration
- **Skills**: `02-Src/features/skills/` - Extensible capabilities (web search, code runner, etc.)
- **Policy**: `02-Src/shared/policy.py` - Request validation and guardrails

**Note**: The project uses numbered directories (`02-Src/`, `03-Tests/`, etc.) with a symlink `src -> 02-Src` for import compatibility.

### Technology Stack
- **Runtime**: Python 3.11+, Flask + Gunicorn
- **AI Providers**: Anthropic Claude, Google Gemini, Groq, OpenRouter, Ollama (local)
- **Knowledge Integration**: LlamaIndex 0.14.4 with ChromaDB vector store
- **Storage**: SQLAlchemy (state), Chroma/pgvector/Pinecone (vectors), Neo4j (graph), Redis (cache)
- **Observability**: Prometheus metrics at `/metrics`, structured logging

## Development Commands

### Local Development
```bash
# Start server (quickstart)
make run              # Runs with BB_API_KEY=test on port 8080

# Development workflow
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # If .env.example exists, configure providers and backends
export BB_API_KEY=test
python -m flask --app src.core.app run --host 0.0.0.0 --port 8080
```

### Code Quality & Testing
```bash
make fmt              # Format code with isort + black
make test             # Run pytest suite (BB_API_KEY=test)

# Run specific tests
BB_API_KEY=test pytest 03-Tests/unit/test_basic.py -v
BB_API_KEY=test pytest 03-Tests/unit/ -k "test_imports" -v

# Manual quality checks
isort src && black src          # Format code
pytest -q                       # Run all tests
mypy src --ignore-missing-imports  # Type check
bandit -r src                   # Security scan
```

**Available Makefile Targets:**
- `make run` - Start Flask development server (sets BB_API_KEY=test, port 8080)
- `make fmt` - Format code with isort and black
- `make test` - Run pytest test suite (sets BB_API_KEY=test)

### Testing Endpoints
```bash
# Health checks
curl -s http://localhost:8080/health
curl -s http://localhost:8080/health/backends  # Check all storage backends
curl -s http://localhost:8080/config           # View current provider/storage config

# Status endpoints
curl -s http://localhost:8080/knowledge/status  # Knowledge base statistics
curl -s http://localhost:8080/router/status     # Smart router statistics

# API calls (requires X-API-Key header)
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{"query":"What is the meaning of life?"}'

# Knowledge base query
curl -X POST http://localhost:8080/api/knowledge \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{"query":"authentication flow","top_k":5}'

# Learning endpoint
curl -X POST http://localhost:8080/learn \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{"correction":"Prefer concise answers under 100 words"}'

# Metrics (Prometheus format)
curl -s http://localhost:8080/metrics
```

## Configuration

### LLM Provider Selection
Set these env vars to choose your AI backend:
```bash
# Anthropic Claude
PROVIDER=anthropic
MODEL=claude-3-5-sonnet-20240620
ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini
PROVIDER=google
MODEL=gemini-2.0-flash-exp
GOOGLE_API_KEY=...

# Groq (fast inference)
PROVIDER=groq
MODEL=llama3-70b-8192
GROQ_API_KEY=...

# OpenRouter (multi-model proxy)
PROVIDER=openrouter
MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_API_KEY=...

# Ollama (local models)
PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

### Storage Backends
Mix and match backends based on your needs:

```bash
# State storage (conversation history)
STATE_BACKEND=sqlite          # Local development
DATABASE_URL=sqlite:///./bb.db

STATE_BACKEND=postgres        # Production
DATABASE_URL=postgresql://user:pass@host/db

# Vector storage (embeddings, semantic search)
VECTOR_BACKEND=chroma         # Local
CHROMA_DIR=.chroma

VECTOR_BACKEND=pgvector       # PostgreSQL extension
PG_DSN=postgresql://...

VECTOR_BACKEND=pinecone       # Managed cloud
PINECONE_API_KEY=...

# Graph storage (knowledge graph, insights)
GRAPH_BACKEND=none            # Disabled
GRAPH_BACKEND=neo4j           # Enabled
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=...

# Cache (response caching)
CACHE_BACKEND=none
CACHE_BACKEND=redis
REDIS_URL=redis://localhost:6379/0

# Artifacts (files, outputs)
ARTIFACT_BACKEND=local
ARTIFACT_DIR=./artifacts

ARTIFACT_BACKEND=s3
S3_BUCKET=bobs-brain
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
```

### Circle of Life Tuning
```bash
BB_CONFIDENCE_MIN=0.6    # Min confidence for persisting insights
BB_COL_BATCH=50          # Batch size for processing events
BB_COL_COOLDOWN=60       # Cooldown between runs (seconds)
COL_SCHEDULE="*/5 * * * *"  # Cron schedule (optional scheduler)
```

## API Endpoints

### Public Endpoints (no auth required)
- `GET /` - Service info (name, version, status)
- `GET /health` - Basic health check
- `GET /health/backends` - Probe all storage backends (state, vector, graph, cache, artifacts)
- `GET /config` - Current provider and storage config (no secrets exposed)
- `GET /metrics` - Prometheus metrics (request counts, etc.)
- `GET /knowledge/status` - Knowledge orchestrator status and statistics
- `GET /router/status` - Smart router status and routing statistics
- `POST /slack/events` - Slack webhook (if Slack integration enabled)

### Protected Endpoints (X-API-Key required)
- `POST /api/query` - Send query to LLM, get response
  - Body: `{"query": "your question here"}`
- `POST /learn` - Submit correction for learning
  - Body: `{"correction": "feedback or pattern to learn"}`
- `POST /api/skill` - Execute a specific skill
  - Body: `{"skill": "skill_name", "args": {...}}`
- `POST /api/knowledge` - Query the knowledge base directly
  - Body: `{"query": "search query", "top_k": 5}`

## Directory Structure

**Note:** This project uses numbered directories with a `src -> 02-Src` symlink for import compatibility.

```
bobs-brain/
├── 01-Docs/                    # Project documentation
│   ├── 001-sec-security-policy.md
│   └── 002-ref-contributing-guide.md
├── 02-Src/                     # Python source code (production)
│   ├── core/                   # Core application
│   │   ├── app.py              # Main Flask application
│   │   └── providers.py        # LLM and storage backend factories
│   ├── features/               # Feature modules
│   │   ├── circle_of_life.py   # Learning pipeline
│   │   ├── knowledge_orchestrator.py  # LlamaIndex multi-source knowledge
│   │   ├── smart_router.py     # Intelligent routing
│   │   └── skills/             # Skill modules (web_search, code_runner)
│   └── shared/                 # Shared utilities
│       ├── policy.py           # Request validation
│       └── util.py             # Common utilities
├── 03-Tests/                   # Test suites (pytest)
│   ├── unit/                   # Unit tests
│   │   ├── test_basic.py       # Basic endpoint tests
│   │   ├── test_smoke.py       # Smoke tests
│   │   ├── test_circle.py      # Circle of Life tests
│   │   └── test_config.py      # Configuration tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── 04-Assets/                  # Static assets and configurations
│   └── configs/                # Config files
├── 05-Scripts/                 # Automation scripts
│   ├── build/                  # Build scripts
│   ├── deploy/                 # Deployment automation
│   ├── research/               # Research scripts (ingest docs)
│   └── testing/                # Test utilities
├── 06-Infrastructure/          # Infrastructure as code
│   └── docker/                 # Docker configurations
├── 99-Archive/                 # Historical code (18 old Bob versions, scrapers)
├── adk-agent/                  # Google ADK implementation (alternative)
├── bob-vertex-agent/           # Vertex AI Agent Engine implementation (alternative)
│   ├── app/                    # Agent application code
│   ├── slack-webhook/          # Slack integration via Cloud Functions
│   └── deployment/             # Deployment configurations
├── genkit-agent/               # Genkit implementation (alternative)
├── claudes-docs/               # AI-generated documentation
│   ├── reports/                # After-action reports
│   ├── audits/                 # System audits
│   └── analysis/               # Technical analysis
├── src -> 02-Src               # Symlink for Python imports
├── requirements.txt            # Python dependencies
├── Makefile                    # Development commands (run, fmt, test)
├── README.md                   # Project overview
├── CLAUDE.md                   # This file
└── .env                        # Environment configuration (DO NOT COMMIT)
```

### Key Files Reference
- `src/core/app.py:1` - Flask app entry point, routes, auth (X-API-Key), rate limiting
- `src/core/providers.py:7` - Factory: `llm_client()` selects provider based on PROVIDER env var
- `src/core/providers.py:60` - Storage factories: `state_db()`, `vector_store()`, `graph_db()`, `cache_client()`, `artifact_store()`
- `src/features/circle_of_life.py:1` - Learning pipeline: ingest → analyze → insights → persist → apply
- `src/features/knowledge_orchestrator.py:1` - LlamaIndex integration for multi-source knowledge
- `src/features/smart_router.py:1` - Intelligent task routing based on query classification
- `src/shared/policy.py:1` - Request validation and guardrails

## Knowledge Orchestrator (LlamaIndex)

The Knowledge Orchestrator (`src/features/knowledge_orchestrator.py`) integrates LlamaIndex for multi-source knowledge:

- **Document ingestion**: Load documents, code, markdown, PDFs into vector store
- **Semantic search**: ChromaDB-powered similarity search across knowledge base
- **Multi-source**: Combine multiple data sources (docs, APIs, databases)
- **RAG (Retrieval-Augmented Generation)**: Inject relevant context into LLM queries
- **Status endpoint**: `GET /knowledge/status` shows knowledge base statistics

### Usage
```python
from src.knowledge_orchestrator import KnowledgeOrchestrator

ko = KnowledgeOrchestrator()
ko.ingest_documents(["docs/api.md", "docs/architecture.md"])
results = ko.query("How does authentication work?", top_k=5)
```

### API Endpoints
```bash
# Query knowledge base
curl -X POST http://localhost:8080/api/knowledge \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{"query":"authentication flow","top_k":5}'

# Check knowledge base status
curl -s http://localhost:8080/knowledge/status
```

## Smart Router

The Smart Router (`src/features/smart_router.py`) provides intelligent task routing and orchestration:

- **Task classification**: Automatically categorizes incoming queries
- **Provider selection**: Routes tasks to optimal LLM provider based on task type
- **Skill orchestration**: Coordinates use of web search, code execution, and other skills
- **Context management**: Maintains conversation context across requests
- **Status endpoint**: `GET /router/status` shows routing statistics and performance

## Circle of Life Learning System

The Circle of Life provides continuous learning through an evidence-driven loop:

1. **Ingest**: Collect events (queries, responses, corrections) in batches
2. **Analyze**: Aggregate by type, extract patterns, sample data
3. **Generate Insights**: Use LLM to identify patterns and recommend actions
4. **Persist**: Store high-confidence insights to Neo4j and/or BigQuery
5. **Apply**: Use insights to improve future responses

### Key Features
- **Deduplication**: Content-based hashing prevents duplicate processing
- **Batch processing**: Configurable batch size (default 50)
- **Cooldown**: Prevents excessive runs (default 60s between batches)
- **Confidence filtering**: Only persists insights above threshold (default 0.6)
- **Optional scheduler**: Cron-based automatic runs via `COL_SCHEDULE`

### Usage
```python
from src.circle_of_life import CircleOfLife

col = CircleOfLife(neo4j_driver=graph_db, bq_client=None, llm_call=llm_insights, logger=log)

# Process events
events = [{"type": "query", "text": "..."}, ...]
batch = col.ingest(events)
analysis = col.analyze(batch)
insights = col.generate_insights(analysis)
g_count, bq_count = col.persist(insights)

# Check readiness (respects cooldown)
if col.ready():
    col.heartbeat(fetch_events_fn)
```

## Slack Integration (Optional)

Slack integration is **optional**. To enable:

### Quick Setup with Cloudflare Tunnel

**1. Install Cloudflare Tunnel:**
```bash
curl -sLO https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

**2. Start Tunnel (get public URL):**
```bash
# Foreground (shows URL in terminal)
cloudflared tunnel --url http://localhost:8080

# Background (URL in logs)
nohup cloudflared tunnel --url http://localhost:8080 > /tmp/cloudflared.log 2>&1 &
grep "trycloudflare.com" /tmp/cloudflared.log
```

**3. Configure Slack App:**
- Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
- Enable Events: ON
- Request URL: `https://YOUR-TUNNEL-URL.trycloudflare.com/slack/events`
- Subscribe to bot events: `message.channels`, `message.im`, `app_mention`
- Save Changes

**4. Set environment variables in `.env`:**
```bash
SLACK_BOT_TOKEN=xoxb-...              # Get from Slack App OAuth & Permissions
SLACK_SIGNING_SECRET=...              # Get from Slack App Basic Information
SLACK_APP_ID=A099YKLCM1N              # Your Slack App ID
SLACK_CLIENT_ID=...                   # Optional: for OAuth flow
SLACK_CLIENT_SECRET=...               # Optional: for OAuth flow
```

**Note**: Slack credentials are configured in `.env`. Never commit the `.env` file to git.

**5. Test in Slack:**
- Open Slack and mention @Bob
- Bob will respond with conversation memory and knowledge base context

### Current Setup (2025-10-08)
- **Public URL:** `https://editor-steering-width-innovation.trycloudflare.com`
- **Slack App ID:** A099YKLCM1N
- **Full Guide:** `~/security/bobs-brain-cloudflare-tunnel-setup.md`

### Features
The app will respond to mentions and DMs automatically with:
- **Conversation memory**: Last 10 messages per user
- **LLM response caching**: 1-hour TTL to reduce costs
- **Knowledge orchestrator**: RAG-powered context from ingested documents
- **Smart routing**: Optimal LLM selection based on task type
- **Duplicate prevention**: Immediate HTTP 200 acknowledgment (fixed Oct 2025)

## CI/CD

### GitHub Actions Workflow
- **Security scanning**: Bandit (Python), Safety (dependencies), Gitleaks (secrets)
- **Lint**: Code style checks (black, isort)
- **Type check**: mypy validation
- **Tests**: pytest with JUnit output
- **Coverage**: Minimum 65% threshold enforced
- **Artifacts**: JUnit XML, coverage.xml, and security reports uploaded

### CI Badges
![CI](https://github.com/jeremylongshore/bobs-brain/actions/workflows/ci.yml/badge.svg?branch=main)
![Security](https://github.com/jeremylongshore/bobs-brain/actions/workflows/security.yml/badge.svg?branch=main)

## Directory Standards

This project uses **standard Python conventions** rather than numbered directories. See `.directory-standards.md` for the rationale.
- Source code in `src/` (not `02-Src/`)
- Tests in `tests/` (not `03-Tests/`)
- Documentation in `docs/` (not `01-Docs/`)
- All Claude-created docs go to `claudes-docs/` with proper categorization (audits, reports, analysis, tasks)

## Extending the System

### Adding New LLM Providers
Edit `src/core/providers.py:7` in the `llm_client()` function:
```python
if p == "my_provider":
    def call(prompt: str):
        # Implement provider-specific logic (e.g., API call, local inference)
        return response_text
    return call
```

**Current providers:** anthropic, google, openrouter, ollama, groq

### Adding New Storage Backends
Add backend initialization in `src/core/providers.py:60+`:
- `state_db()` - Conversation history (sqlite, postgres)
- `vector_store()` - Embeddings (chroma, pgvector, pinecone)
- `graph_db()` - Knowledge graph (neo4j)
- `cache_client()` - Response caching (redis)
- `artifact_store()` - File storage (local, s3)

### Adding Skills
1. Create `src/features/skills/my_skill.py` with skill implementation
2. Define `SKILL_REGISTRY = {"my_skill": my_skill_function}`
3. Import in `src/features/skills/__init__.py` and update `load_skills()`

### Ingesting Knowledge (LlamaIndex)
```python
from src.features.knowledge_orchestrator import get_knowledge_orchestrator
ko = get_knowledge_orchestrator()
ko.ingest_directory("docs/")  # Batch ingest directory
ko.ingest_documents(["path/to/doc.md"])  # Single file
```

## Troubleshooting

### Backend Connection Issues
Check backend health:
```bash
curl -s http://localhost:8080/health/backends | jq
```

### LLM Provider Errors
Verify provider configuration:
```bash
curl -s http://localhost:8080/config | jq
```

### Rate Limiting
Default limit is 60 requests/minute. Adjust in `src/core/app.py`:
```python
limiter = Limiter(get_remote_address, app=app, default_limits=["60/minute"])
```

### Slack Duplicate Responses
If seeing duplicate Slack responses, ensure immediate HTTP 200 acknowledgment is enabled. This was fixed in October 2025.

### Circle of Life Not Running
Check cooldown and last run time:
```python
if col.ready():  # Returns False if within cooldown window
    col.heartbeat(fetch_fn)
```

## Important Implementation Notes

### Multiple Agent Implementations
This repository contains **three different implementations** of Bob's Brain:

1. **Flask App (Primary - v5)** - `02-Src/` - Modular Flask-based agent (this is the main implementation)
2. **Vertex AI Agent Engine** - `bob-vertex-agent/` - Google Cloud Vertex AI managed agent implementation
3. **Google ADK** - `adk-agent/` - Agent Development Kit implementation (experimental)
4. **Genkit** - `genkit-agent/` - Full-stack AI framework implementation (experimental)

When working on Bob's Brain, focus on the **Flask App (v5)** in `02-Src/` unless specifically asked about the alternative implementations.

### Archive Directory
The `99-Archive/` directory contains **18 deprecated Bob versions** and historical scrapers. These are preserved for reference only and are **not part of the current v5 system**. Don't modify or reference archived code in new development.

### Security & Authentication
- **API Key Auth**: All `/api/*` routes require `X-API-Key` header matching `BB_API_KEY` env var
- **Rate Limiting**: 60 req/min default (configurable in `src/core/app.py:33`)
- **Slack Signature Verification**: Implemented for production (see `src/core/app.py` for webhook verification)
- **Request Validation**: `src/shared/policy.py` provides input guardrails
- **No secrets in code**: Use `.env` file (never commit `.env`)

### Git Workflow
- **Main branch**: `clean-main` (for PRs and feature development)
- **Current branch**: `main` (check `git status`)
- Create feature branches from `clean-main`
- Run `make fmt` and `make test` before committing

### Performance Targets
- Response time: < 3s typical queries
- Rate limit: 60 req/min (configurable)
- Cost: Provider-dependent (Ollama=free, Claude/Gemini=per-token)