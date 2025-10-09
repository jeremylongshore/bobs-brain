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
- **Main Service**: `02-Src/core/app.py` - Flask app with API routes, auth, rate limiting, metrics
- **Providers**: `02-Src/core/providers.py` - LLM client factory, storage backend initialization
- **Circle of Life**: `02-Src/features/circle_of_life.py` - Learning pipeline (ingest → analyze → insights → persist → apply)
- **Knowledge Orchestrator**: `02-Src/features/knowledge_orchestrator.py` - Multi-source knowledge integration
- **Smart Router**: `02-Src/features/smart_router.py` - Intelligent routing and task orchestration
- **Skills**: `02-Src/features/skills/` - Extensible capabilities (web search, code runner, etc.)
- **Policy**: `02-Src/shared/policy.py` - Request validation and guardrails

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
cp 04-Assets/configs/.env.example .env  # Configure providers and backends
export BB_API_KEY=test
python -m flask --app src.app run --host 0.0.0.0 --port 8080

# Alternative: use numbered path (symlink exists: src -> 02-Src)
python -m flask --app 02-Src.core.app run --host 0.0.0.0 --port 8080
```

### Code Quality
```bash
make fmt              # Format code with isort + black (runs on src/)
make test             # Run pytest suite (BB_API_KEY=test)

# Manual quality checks (if you have the tools)
isort src && black src          # Format (src is symlink to 02-Src)
pytest -q                       # Test (runs 03-Tests/)
mypy 02-Src --ignore-missing-imports  # Type check
bandit -r 02-Src                # Security scan
```

### Deployment & Scripts
```bash
# Deploy to Google Cloud Run
05-Scripts/deploy/deploy-to-cloudrun.sh

# Create new GCP project for Bob
05-Scripts/deploy/create-bob-project.sh

# Store secrets in Secret Manager
05-Scripts/deploy/store-secrets.sh

# Test smart router
05-Scripts/testing/test-smart-router.sh
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

## Directory Structure

This project follows a numbered directory system (see `.directory-standards.md`).

**Important**: A symlink `src -> 02-Src` exists for compatibility with Python tooling. You can reference code as either `src/` or `02-Src/` - they point to the same location.

```
bobs-brain/
├── 01-Docs/                    # Documentation (using NNN-abv-description.ext format)
├── 02-Src/                     # Python source code (symlinked as 'src/')
│   ├── core/                   # Core application
│   │   ├── app.py              # Main Flask application
│   │   └── providers.py        # LLM and storage backend factories
│   ├── features/               # Feature modules
│   │   ├── circle_of_life.py   # Learning pipeline
│   │   ├── knowledge_orchestrator.py  # Multi-source knowledge
│   │   ├── smart_router.py     # Intelligent routing
│   │   └── skills/             # Skill modules (web_search, code_runner)
│   └── shared/                 # Shared utilities
│       ├── policy.py           # Request validation
│       └── util.py             # Common utilities
├── 03-Tests/                   # Test suites
│   └── unit/                   # Unit tests (test_basic, test_smoke, test_circle, test_config)
├── 04-Assets/                  # Static assets and configs
│   └── configs/                # Configuration files
│       └── .env.example        # Environment variable template
├── 05-Scripts/                 # Automation scripts
│   ├── build/                  # Build scripts (start-bob.sh)
│   ├── deploy/                 # Deployment automation (Cloud Run, GCP)
│   ├── maintenance/            # Maintenance scripts
│   ├── research/               # Research scripts
│   └── testing/                # Test utilities
├── 06-Infrastructure/          # Infrastructure as Code
│   ├── ci-cd/                  # CI/CD configuration
│   │   └── github-actions/     # GitHub Actions workflows
│   └── docker/                 # Docker configurations
├── 99-Archive/                 # Historical code
│   ├── deprecated/             # Deprecated features
│   └── legacy/                 # Legacy code (old Bob versions, scrapers)
├── claudes-docs/               # AI-generated documentation
│   ├── audits/                 # System audits
│   ├── reports/                # After-action reports
│   ├── analysis/               # Technical analysis
│   └── tasks/                  # Task tracking
├── requirements.txt            # Python dependencies
├── Makefile                    # Development commands
├── README.md                   # Project overview
├── CLAUDE.md                   # This file
└── .directory-standards.md     # Directory standards reference
```

### Key Implementation Files
- `02-Src/core/app.py` - Flask app with routes, auth, rate limiting, metrics
- `02-Src/core/providers.py` - Factory functions for LLM and storage backends
- `02-Src/features/circle_of_life.py` - Learning pipeline implementation
- `02-Src/features/smart_router.py` - Intelligent task routing and orchestration
- `02-Src/features/knowledge_orchestrator.py` - Multi-source knowledge integration
- `02-Src/shared/policy.py` - Request validation and guardrails

### Tests
- `03-Tests/unit/test_basic.py` - Basic endpoint tests
- `03-Tests/unit/test_smoke.py` - Smoke tests for core functionality
- `03-Tests/unit/test_circle.py` - Circle of Life unit tests
- `03-Tests/unit/test_config.py` - Configuration validation tests

## Smart Router

The Smart Router (`02-Src/features/smart_router.py`) provides intelligent task routing and orchestration:

- **Task classification**: Automatically categorizes incoming queries
- **Provider selection**: Routes tasks to optimal LLM provider based on task type
- **Skill orchestration**: Coordinates use of web search, code execution, and other skills
- **Context management**: Maintains conversation context across requests

Use the test script to validate Smart Router functionality:
```bash
05-Scripts/testing/test-smart-router.sh
```

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
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_APP_ID=A099YKLCM1N
```

**5. Test in Slack:**
- Open Slack and mention @Bob
- Bob will respond with conversation memory and knowledge base context

### Current Setup (2025-10-08)
- **Public URL:** `https://editor-steering-width-innovation.trycloudflare.com`
- **Slack App ID:** A099YKLCM1N
- **Full Guide:** `~/security/bobs-brain-cloudflare-tunnel-setup.md`

The app will respond to mentions and DMs automatically with:
- Conversation memory (last 10 messages)
- LLM response caching (1-hour)
- Knowledge orchestrator integration
- Smart routing to optimal LLM

## CI/CD

### GitHub Actions Workflow
Workflows are located in `06-Infrastructure/ci-cd/github-actions/workflows/`:
- **Security scanning**: Bandit (Python), Safety (dependencies), Gitleaks (secrets)
- **Lint**: Code style checks (black, isort)
- **Type check**: mypy validation
- **Tests**: pytest with JUnit output
- **Coverage**: Minimum 65% threshold enforced
- **Artifacts**: JUnit XML, coverage.xml, and security reports uploaded

### CI Badges
![CI](https://github.com/jeremylongshore/bobs-brain/actions/workflows/ci.yml/badge.svg?branch=main)
![Security](https://github.com/jeremylongshore/bobs-brain/actions/workflows/security.yml/badge.svg?branch=main)

**Note**: The actual `.github/workflows/` directory may not exist yet - workflows are stored in the numbered infrastructure directory.

## Directory Standards

Follow `.directory-standards.md` for structure and file naming.
- Store all docs in `01-Docs/` (not yet migrated in this repo)
- Use `NNN-abv-description.ext` format with approved abbreviations
- Maintain strict chronological order
- All Claude-created docs go to `claudes-docs/` with proper categorization

## Development Best Practices

### Adding New LLM Providers
Edit `02-Src/core/providers.py` and add a new provider case to the `llm_client()` function:
```python
if p == "my_provider":
    def call(prompt: str):
        # Implement provider-specific logic
        return response_text
    return call
```

### Adding New Storage Backends
Add backend initialization in corresponding function in `02-Src/core/providers.py`:
- `state_db()` - For state/conversation history backends
- `vector_store()` - For vector/embedding backends
- `graph_db()` - For graph database backends
- `cache_client()` - For caching backends
- `artifact_store()` - For artifact storage backends

```python
if backend == "my_backend":
    # Initialize and return backend client
    return client
```

### Adding Skills
Create a new module in `02-Src/features/skills/`:
```python
# 02-Src/features/skills/my_skill.py
def my_skill(arg):
    """Skill description"""
    return result

SKILL_REGISTRY = {
    "my_skill": my_skill
}
```

Then import in `02-Src/features/skills/__init__.py` and update the `load_skills()` function.

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
Default limit is 60 requests/minute. Adjust in `02-Src/core/app.py`:
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

This repo contains significant historical code in `99-Archive/`:
- **18 deprecated Bob versions** (in `99-Archive/legacy/`) showing evolution from simple to complex architectures
- **Multiple scraper implementations** for YouTube, Reddit, forums, technical bulletins
- **Migration scripts** for Firestore → Graphiti, AutoML setup, production data checks
- **Dockerfiles** for various deployment strategies (simple, production, dual-memory, etc.)

These are preserved for reference but are **not part of the current system**. The current architecture is clean, modular, and provider-agnostic.

**Note**: The actual archived files may still be in the old `archive/` directory from before the numbered directory migration. Check both locations if searching for historical code.

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
- **Request Validation**: `02-Src/shared/policy.py` provides input guardrails

## Main Branch Strategy

- **Main branch**: `clean-main` (for PRs and clean development)
- **Current branch**: `main` (check git status for current state)
- Always create feature branches from `clean-main`
- Run `make test` and `make fmt` before committing