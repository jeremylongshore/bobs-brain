# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bob's Brain is a sovereign modular AI agent with pluggable LLM providers, configurable storage backends, and a Circle-of-Life learning loop. It's designed to be cloned and run anywhere—locally or in the cloud—with Slack integration as an optional feature.

## Architecture

### Core Philosophy
- **Provider-agnostic**: Swap between Claude (Anthropic), Gemini (Google), OpenRouter, or Ollama via env vars
- **Storage modularity**: State (sqlite/postgres), Vector (chroma/pgvector/pinecone), Graph (none/neo4j), Cache (none/redis), Artifacts (local/s3)
- **Evidence-driven learning**: Circle-of-Life analyzes interactions, generates LLM insights, persists patterns to graph/analytics
- **API-first**: REST endpoints with API key auth, Prometheus metrics, health checks with backend probes

### Core Components
- **Main Service**: `src/app.py` - Flask app with API routes, auth, rate limiting, metrics
- **Providers**: `src/providers.py` - LLM client factory, storage backend initialization
- **Circle of Life**: `src/circle_of_life.py` - Learning pipeline (ingest → analyze → insights → persist → apply)
- **Skills**: `src/skills/` - Extensible capabilities (web search, code runner, etc.)
- **Policy**: `src/policy.py` - Request validation and guardrails

### Technology Stack
- **Runtime**: Python 3.11+, Flask + Gunicorn
- **AI Providers**: Anthropic Claude, Google Gemini, OpenRouter, Ollama (local), Vertex AI (stub)
- **Storage**: SQLAlchemy (state), Chroma/pgvector/Pinecone (vectors), Neo4j (graph), Redis (cache)
- **Observability**: Prometheus metrics at `/metrics`, structured logging
- **CI/CD**: GitHub Actions with 65% coverage floor

## Development Commands

### Local Development
```bash
# Start server (quickstart)
make run              # Runs with BB_API_KEY=test on port 8080

# Development workflow
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure providers and backends
export BB_API_KEY=test
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

### Code Quality
```bash
make fmt              # Format code with isort + black
make test             # Run pytest suite (BB_API_KEY=test)

# Manual quality checks (if you have the tools)
isort src && black src          # Format
pytest -q                       # Test
mypy src --ignore-missing-imports  # Type check
bandit -r src                   # Security scan
```

### Testing Endpoints
```bash
# Health checks
curl -s http://localhost:8080/health
curl -s http://localhost:8080/health/backends  # Check all storage backends
curl -s http://localhost:8080/config           # View current provider/storage config

# API calls (requires X-API-Key header)
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{"query":"What is the meaning of life?"}'

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
- `POST /slack/events` - Slack webhook (if Slack integration enabled)

### Protected Endpoints (X-API-Key required)
- `POST /api/query` - Send query to LLM, get response
  - Body: `{"query": "your question here"}`
- `POST /learn` - Submit correction for learning
  - Body: `{"correction": "feedback or pattern to learn"}`

## Key File Locations

### Source Code
- `src/app.py` - Main Flask application, routing, auth, metrics
- `src/providers.py` - LLM and storage backend factory functions
- `src/circle_of_life.py` - Learning pipeline implementation
- `src/policy.py` - Request validation and guardrails
- `src/util.py` - Utility functions
- `src/skills/` - Extensible skill modules (web_search, code_runner)

### Tests
- `tests/test_basic.py` - Basic endpoint tests
- `tests/test_smoke.py` - Smoke tests for core functionality
- `tests/test_circle.py` - Circle of Life unit tests
- `tests/test_config.py` - Configuration validation tests

### Configuration
- `.env.example` - Template for environment variables
- `requirements.txt` - Python dependencies
- `Makefile` - Common development commands

### Archive
- `archive/deprecated_bobs/` - Legacy Bob versions (18 files)
- `archive/old_scrapers/` - Previous scraper implementations
- `archive/old_versions/` - Historical code and migrations

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

1. Create a Slack app at https://api.slack.com/apps
2. Add Event Subscriptions pointing to `/slack/events`
3. Set environment variables:
   ```bash
   SLACK_BOT_TOKEN=xoxb-...
   SLACK_SIGNING_SECRET=...
   ```
4. Enable signature verification in production

The app will respond to mentions and DMs automatically.

## CI/CD

### GitHub Actions Workflow
- **Lint**: Code style checks (black, isort)
- **Type check**: mypy validation
- **Tests**: pytest with JUnit output
- **Coverage**: Minimum 65% threshold enforced
- **Artifacts**: JUnit XML and coverage.xml uploaded

### Badge
![CI](https://github.com/jeremylongshore/bobs-brain/actions/workflows/ci.yml/badge.svg?branch=main)

## Directory Standards

Follow `.directory-standards.md` for structure and file naming.
- Store all docs in `01-Docs/` (not yet migrated in this repo)
- Use `NNN-abv-description.ext` format with approved abbreviations
- Maintain strict chronological order
- All Claude-created docs go to `claudes-docs/` with proper categorization

## Development Best Practices

### Adding New LLM Providers
Edit `src/providers.py` and add a new provider case:
```python
if p == "my_provider":
    def call(prompt: str):
        # Implement provider-specific logic
        return response_text
    return call
```

### Adding New Storage Backends
Add backend initialization in corresponding function (`state_db()`, `vector_store()`, etc.):
```python
if backend == "my_backend":
    # Initialize and return backend client
    return client
```

### Adding Skills
Create a new module in `src/skills/`:
```python
# src/skills/my_skill.py
def my_skill(arg):
    """Skill description"""
    return result

SKILL_REGISTRY = {
    "my_skill": my_skill
}
```

Then import in `src/skills/__init__.py`.

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
Default limit is 60 requests/minute. Adjust in `src/app.py`:
```python
limiter = Limiter(get_remote_address, app=app, default_limits=["60/minute"])
```

### Circle of Life Not Running
Check cooldown and last run time:
```python
if col.ready():  # Returns False if within cooldown window
    col.heartbeat(fetch_fn)
```

## Archive Notes

This repo contains significant historical code in `archive/`:
- **18 deprecated Bob versions** showing evolution from simple to complex architectures
- **Multiple scraper implementations** for YouTube, Reddit, forums, technical bulletins
- **Migration scripts** for Firestore → Graphiti, AutoML setup, production data checks
- **Dockerfiles** for various deployment strategies (simple, production, dual-memory, etc.)

These are preserved for reference but are **not part of the current system**. The current architecture is clean, modular, and provider-agnostic.

## Performance & Cost Targets

- **Response time**: < 3s for typical queries
- **Uptime**: Target 99.5%+ for production deployments
- **Cost**: Depends on provider choice (Ollama = free, Anthropic/Google = per-token)
- **Throughput**: 60 req/min default rate limit (configurable)

## Security Considerations

- **API Key Authentication**: All `/api/*` routes require `X-API-Key` header
- **Rate Limiting**: 60 requests/minute default (Flask-Limiter)
- **No Secrets in Code**: Use environment variables for all credentials
- **CORS**: Enabled for `/api/*` and `/slack/*` routes (configure as needed)
- **Request Validation**: `src/policy.py` provides input guardrails

## Main Branch Strategy

- **Main branch**: `clean-main` (for PRs and clean development)
- **Current branch**: `main` (check git status for current state)
- Always create feature branches from `clean-main`
- Run `make test` and `make fmt` before committing