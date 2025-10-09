# Bob's Brain v5 — Sovereign Modular Agent

![CI](https://github.com/jeremylongshore/bobs-brain/actions/workflows/ci.yml/badge.svg?branch=main)
![Security](https://github.com/jeremylongshore/bobs-brain/actions/workflows/security.yml/badge.svg?branch=main)

**What it is:** A clone-and-run personal agent with pluggable LLMs (Claude, Google, OpenRouter, Ollama), modular storage, and a Circle-of-Life learning loop. Runs local or cloud. Slack optional.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Bob's Brain Agent                         │
├─────────────────────────────────────────────────────────────────┤
│  Flask API (/api/query, /learn, /slack/events, /metrics)        │
└────────────┬────────────────────────────────────┬───────────────┘
             │                                    │
    ┌────────▼─────────┐                 ┌───────▼────────┐
    │  LLM Providers   │                 │    Storage      │
    ├──────────────────┤                 ├────────────────┤
    │ • Anthropic      │                 │ State: SQLite  │
    │ • Google         │                 │        Postgres │
    │ • OpenRouter     │                 │ Vector: Chroma │
    │ • Ollama         │                 │         Pgvector│
    │                  │                 │         Pinecone│
    │ Model: Claude,   │                 │ Graph: Neo4j   │
    │        Gemini,   │                 │ Cache: Redis   │
    │        etc.      │                 │ Artifact: S3   │
    └──────────────────┘                 └────────────────┘
             │                                    │
             └────────────┬───────────────────────┘
                          │
                 ┌────────▼─────────┐
                 │ Circle of Life   │
                 │   Learning Loop  │
                 ├──────────────────┤
                 │ 1. Ingest events │
                 │ 2. Analyze       │
                 │ 3. LLM insights  │
                 │ 4. Persist       │
                 │ 5. Apply         │
                 └──────────────────┘
```

**Key Design Principles:**
- **Provider-agnostic**: Swap LLM/storage without code changes
- **Environment-driven**: Configure via env vars (`.env` or runtime)
- **Stateless API**: Flask + Gunicorn for horizontal scaling
- **Evidence-driven learning**: Circle of Life analyzes interactions
- **Security-first**: API key auth, secret scanning, vulnerability checks

## Features
- **Pluggable LLMs:** `PROVIDER=anthropic|google|openrouter|ollama`, `MODEL=claude-3-5-sonnet-20240620`
- **Storage choices:** State=sqlite|postgres, Vector=chroma|pgvector|pinecone, Graph=none|neo4j, Cache=none|redis, Artifacts=local|s3
- **APIs:** `/api/query`, `/learn`, `/config`, `/health`, `/health/backends`, `/metrics`, `/slack/events`
- **Security:** `X-API-Key` required for `/api/*`
- **Observability:** Prometheus at `/metrics`, CI with coverage floor 65%

## Quickstart (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export BB_API_KEY=test
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

## Public Access (Slack/External)

**Option 1: Cloudflare Tunnel (Recommended for testing)**
```bash
# Install cloudflared
curl -sLO https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Start tunnel (gets random public URL)
cloudflared tunnel --url http://localhost:8080

# For background: nohup cloudflared tunnel --url http://localhost:8080 > cloudflared.log 2>&1 &
```

**Option 2: Deploy to Cloud Run**
```bash
gcloud run deploy bobs-brain --source . --region us-central1
```

**See full setup guide:** `~/security/bobs-brain-cloudflare-tunnel-setup.md`

## Choose your model
```bash
PROVIDER=anthropic|google|openrouter|ollama
MODEL=claude-3-5-sonnet-20240620   # e.g., claude-3-5-sonnet-20240620 or gemini-2.0-flash
# ANTHROPIC_API_KEY or GOOGLE_API_KEY or OPENROUTER_API_KEY or OLLAMA_BASE_URL
```

## Storage backends
```bash
STATE_BACKEND=sqlite|postgres      # DATABASE_URL=sqlite:///./bb.db
VECTOR_BACKEND=chroma|pgvector|pinecone   # CHROMA_DIR=.chroma
GRAPH_BACKEND=none|neo4j           # NEO4J_URI/USER/PASSWORD
CACHE_BACKEND=none|redis           # REDIS_URL=redis://localhost:6379/0
ARTIFACT_BACKEND=local|s3          # ARTIFACT_DIR or S3_* vars
```

## Endpoints
- `GET /` – basic info
- `GET /health` – service health
- `GET /health/backends` – backend probes
- `GET /config` – current provider/storage (no secrets)
- `GET /metrics` – Prometheus metrics
- `POST /api/query` (requires X-API-Key)
- `POST /learn` (requires X-API-Key)
- `POST /slack/events` – optional Slack webhook

## Example calls
```bash
curl -s http://localhost:8080/health
curl -s -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" -H "X-API-Key:$BB_API_KEY" \
  -d '{"query":"hello"}'
curl -s -X POST http://localhost:8080/learn \
  -H "Content-Type: application/json" -H "X-API-Key:$BB_API_KEY" \
  -d '{"correction":"prefer short answers"}'
```

## Circle of Life

Evidence-driven loop: ingest → analyze → LLM insights → persist → apply.
Scheduler (optional): `COL_SCHEDULE="*/5 * * * *"` runs a heartbeat batch.

## Slack (optional)

Create a Slack app and point Events API to `/slack/events`. Add signature verification in production.

## Directory Structure

This project follows professional directory standards (see `.directory-standards.md`).

```
bobs-brain/
├── 01-Docs/                    # Project documentation
│   ├── 001-sec-security-policy.md
│   └── 002-ref-contributing-guide.md
├── 02-Src/                     # Python source code (production)
│   ├── core/                   # Core application
│   │   ├── app.py              # Flask application entry point
│   │   └── providers.py        # Pluggable LLM/storage backends
│   ├── features/               # Feature modules
│   │   ├── circle_of_life.py   # ML learning pipeline
│   │   ├── knowledge_orchestrator.py  # Multi-source knowledge
│   │   └── skills/             # Modular skill system
│   └── shared/                 # Shared utilities
│       ├── policy.py           # Request validation
│       └── util.py             # Common utilities
├── 03-Tests/                   # Test suites (pytest)
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── 04-Assets/                  # Static assets and configurations
│   └── configs/                # Config files (.env.example, pytest.ini, etc.)
├── 05-Scripts/                 # Automation scripts
│   ├── build/                  # Build scripts (start-bob.sh)
│   ├── deploy/                 # Deployment automation (Cloud Run, etc.)
│   ├── research/               # Research scripts (ingest docs)
│   └── testing/                # Test utilities
├── 06-Infrastructure/          # Infrastructure as code
│   ├── ci-cd/                  # CI/CD configuration
│   │   └── github-actions/     # GitHub Actions workflows
│   └── docker/                 # Docker configurations
│       └── Dockerfile          # Main service container
├── 99-Archive/                 # Historical code
│   ├── deprecated/             # Deprecated features
│   └── legacy/                 # Legacy code
├── claudes-docs/               # AI-generated documentation
│   ├── audits/                 # System audits
│   ├── reports/                # After-action reports, test results
│   ├── analysis/               # Technical analysis
│   └── tasks/                  # Task tracking
├── .directory-standards.md     # Directory standards reference
├── requirements.txt            # Python dependencies
├── Makefile                    # Development commands
├── README.md                   # This file
├── CLAUDE.md                   # AI assistant guidance
└── CHANGELOG.md                # Version history
```

## CI/CD

- **GitHub Actions**: lint, type-check, tests, coverage ≥ 65%
- **Security scanning**: Bandit (Python), Safety (dependencies), Gitleaks (secrets)
- **Artifacts**: JUnit + coverage.xml + security reports
- **Badge**: Shows main branch status

**Common Commands:**
```bash
make safe-commit    # Run all checks before committing
make test          # Run test suite
make lint-check    # Code style compliance
make security-check # Security scanning
make deploy        # Deploy to Cloud Run
```

## Config keys

See .env.example or CONFIG.md. Core:

`BB_API_KEY`, `PROVIDER`, `MODEL`, `STATE_BACKEND`, `VECTOR_BACKEND`, `GRAPH_BACKEND`,
`CACHE_BACKEND`, `ARTIFACT_BACKEND`, `COL_SCHEDULE`

## License

MIT.

---
Generated from commit 384275c. Repo: https://github.com/jeremylongshore/bobs-brain