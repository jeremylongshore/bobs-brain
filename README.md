# Bob's Brain v5 — Sovereign Agent

[![CI](https://github.com/jeremylongshore/bobs-brain/workflows/CI/badge.svg)](https://github.com/jeremylongshore/bobs-brain/actions)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)

**AI agent that learns and evolves through Circle of Life**

🔄 **Circle of Life Learning**: Evidence-driven continuous improvement
🧠 **Multi-LLM Support**: Claude, Google, OpenRouter, Ollama - your choice
🔧 **Modular Storage**: SQLite, Postgres, Chroma, Neo4j, Redis, S3
⚡ **Skills System**: Drop-in capabilities via `src/skills/`
🔐 **Production Ready**: Auth, rate limiting, monitoring

> **Previous Versions**: Find older implementations on feature branches:
> - `feature/hardened-v5-secure-flask` - Secure Flask app with Google integration
> - Check all branches for different architectural approaches

## 🚀 Quickstart

```bash
# Clone and setup
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain
python -m venv .venv && source .venv/bin/activate

# Install and configure
pip install -r requirements.txt
cp .env.example .env  # edit BB_API_KEY and PROVIDER

# Run
export BB_API_KEY=test
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

🌐 **Server starts at**: http://localhost:8080

## 📡 API Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/` | GET | None | Service info |
| `/health` | GET | None | Health check |
| `/config` | GET | None | Current configuration |
| `/health/backends` | GET | None | Backend status |
| `/metrics` | GET | None | Prometheus metrics |
| `/api/query` | POST | API Key | Intelligence queries |
| `/api/skill` | POST | API Key | Execute skills |
| `/learn` | POST | API Key | Submit corrections |
| `/slack/events` | POST | None | Slack webhook |

### Example Usage

```bash
# Health check
curl http://localhost:8080/health

# Query with Claude
curl -H "X-API-Key: test" \
     -H "Content-Type: application/json" \
     -d '{"query": "How do neural networks work?"}' \
     http://localhost:8080/api/query

# Execute skill
curl -H "X-API-Key: test" \
     -H "Content-Type: application/json" \
     -d '{"name": "web_search", "payload": {"query": "AI news"}}' \
     http://localhost:8080/api/skill

# Submit learning
curl -H "X-API-Key: test" \
     -H "Content-Type: application/json" \
     -d '{"correction": "Actually, transformers use attention mechanisms"}' \
     http://localhost:8080/learn
```

## 🤖 LLM Providers

Switch providers via `.env`:

```bash
# Claude (Anthropic)
PROVIDER=anthropic
MODEL=claude-3-5-sonnet-20240620
ANTHROPIC_API_KEY=your-key

# Google Gemini
PROVIDER=google
MODEL=gemini-2.5-flash
GOOGLE_API_KEY=your-key

# OpenRouter (any model)
PROVIDER=openrouter
MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_API_KEY=your-key

# Local Ollama
PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

## 🏗️ Storage Backends

**State Database**:
```bash
STATE_BACKEND=sqlite  # or postgres
DATABASE_URL=sqlite:///./bb.db
```

**Vector Store**:
```bash
VECTOR_BACKEND=chroma  # or pgvector, pinecone
CHROMA_DIR=.chroma
```

**Graph Database**:
```bash
GRAPH_BACKEND=neo4j  # or none
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

**Cache**:
```bash
CACHE_BACKEND=redis  # or none
REDIS_URL=redis://localhost:6379/0
```

**Artifacts**:
```bash
ARTIFACT_BACKEND=local  # or s3
ARTIFACT_DIR=./artifacts
# or S3_BUCKET, S3_ACCESS_KEY, etc.
```

## 🔄 Circle of Life Learning

**The core of Bob's intelligence** - a continuous learning loop that evolves the agent through real-world feedback.

### How It Works

```
Events → Ingest → Analyze → Generate Insights → Persist → Apply → Better Responses
  ↑                                                                        ↓
  └─────────────────── Feedback Loop ──────────────────────────────────────┘
```

**1. Ingest**: Deduplicates and batches events from:
- User corrections via `/learn` API
- Slack interactions and feedback
- Scheduled system heartbeats
- Custom application events

**2. Analyze**: Groups events by type and patterns:
```python
{
  "counts": {"correction": 5, "slack_message": 12},
  "sample": [{"type": "correction", "text": "Use transformers not RNNs"}]
}
```

**3. Generate Insights**: LLM extracts learnable patterns:
```json
[
  {
    "pattern": "ml_architecture_correction",
    "action": "prefer_transformers_over_rnns",
    "confidence": 0.9
  }
]
```

**4. Persist**: High-confidence insights (≥0.6) saved to Neo4j/storage

**5. Apply**: System behavior updated for future queries

### Configuration

```bash
# Learning thresholds
BB_CONFIDENCE_MIN=0.6    # Only persist insights above this confidence
BB_COL_BATCH=50          # Max events processed per cycle
BB_COL_COOLDOWN=60       # Min seconds between learning cycles

# Automated learning
COL_SCHEDULE=*/5 * * * * # CRON: run every 5 minutes (optional)
```

### Feed the Learning Loop

```bash
# Submit corrections
curl -H "X-API-Key: test" \
     -d '{"correction": "Actually, use attention mechanisms in transformers"}' \
     http://localhost:8080/learn

# View learning metrics
curl http://localhost:8080/health/backends
```

**Result**: Bob gets smarter with every interaction, building a knowledge graph of corrections and improvements.

## ⚡ Skills System

Add capabilities by dropping files in `src/skills/`:

```python
# src/skills/my_skill.py
SKILL_NAME = "my_skill"

def run(payload: dict) -> dict:
    # Your skill logic here
    return {"result": "success"}
```

**Built-in Skills**:
- `web_search` - Web search stub
- `code_runner` - Safe code execution stub

**Usage**:
```bash
curl -H "X-API-Key: test" \
     -d '{"name": "my_skill", "payload": {"input": "data"}}' \
     http://localhost:8080/api/skill
```

## 🔧 Development

```bash
# Format code
make fmt

# Run tests
make test

# Start dev server
make run
```

## 🚀 Deployment

**Cloud Run**:
```bash
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --set-env-vars BB_API_KEY=your-key,PROVIDER=anthropic
```

**Docker**:
```bash
docker build -t bobs-brain .
docker run -p 8080:8080 \
  -e BB_API_KEY=test \
  -e PROVIDER=anthropic \
  bobs-brain
```

## 🔒 Security

- **API Key Auth**: All `/api/*` endpoints protected
- **Rate Limiting**: Configurable per-endpoint limits
- **Input Validation**: Pydantic schema validation
- **CORS**: Configured for API and Slack routes
- **No Hardcoded Secrets**: Everything via environment

## 📊 Monitoring

- **Health**: `/health` with component status
- **Metrics**: Prometheus metrics at `/metrics`
- **Config**: Current setup at `/config`
- **Backends**: Backend status at `/health/backends`

## 🏗️ Architecture

```
src/
├── app.py              # Main Flask application
├── providers.py        # Multi-provider backends
├── circle_of_life.py   # Learning system
├── policy.py           # Request validation
├── skills/             # Pluggable capabilities
│   ├── __init__.py
│   ├── web_search.py
│   └── code_runner.py
└── util.py             # Utilities
```

**Tech Stack**:
- **Framework**: Flask + Gunicorn
- **AI**: Multi-provider (Claude, Google, OpenRouter, Ollama)
- **Storage**: Modular (SQLite, Postgres, Chroma, Neo4j, Redis, S3)
- **Scheduling**: APScheduler
- **Monitoring**: Prometheus + structured logging

## 📚 Configuration

See [CONFIG.md](CONFIG.md) for complete environment variable reference.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built for sovereignty • Designed for modularity • Ready to deploy**
\![CI](https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/actions/workflows/ci.yml/badge.svg?branch=main)
