# Bob's Brain v5 — Sovereign Modular Agent

![CI](https://github.com/jeremylongshore/bobs-brain/actions/workflows/ci.yml/badge.svg?branch=main)

**What it is:** A clone-and-run personal agent with pluggable LLMs (Claude, Google, OpenRouter, Ollama), modular storage, and a Circle-of-Life learning loop. Runs local or cloud. Slack optional.

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

## CI
- GitHub Actions: lint, type-check, tests, coverage ≥ 65%
- Artifacts: JUnit + coverage.xml
- Badge shows main branch status.

## Config keys

See .env.example or CONFIG.md. Core:

`BB_API_KEY`, `PROVIDER`, `MODEL`, `STATE_BACKEND`, `VECTOR_BACKEND`, `GRAPH_BACKEND`,
`CACHE_BACKEND`, `ARTIFACT_BACKEND`, `COL_SCHEDULE`

## License

MIT.

---
Generated from commit 384275c. Repo: https://github.com/jeremylongshore/bobs-brain