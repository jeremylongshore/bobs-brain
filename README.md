# Bob's Brain v5 — Clone and Run

[![CI](https://github.com/jeremylongshore/bobs-brain/workflows/CI/badge.svg)](https://github.com/jeremylongshore/bobs-brain/actions)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)

**Secure AI Assistant with Memory and Continuous Learning**

Clean, production-ready Flask API with Slack integration, Neo4j memory, and Circle of Life learning loop. No scrapers, no diagnostics - just pure AI intelligence.

## 🚀 Quickstart

```bash
# Clone and setup
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure (copy and edit)
cp .env.example .env

# Run locally
export BB_API_KEY=test
python -m flask --app src.bob_brain_v5 run --host 0.0.0.0 --port 8080
```

Server starts at http://localhost:8080

## 📡 API Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/health` | GET | None | Service health check |
| `/api/query` | POST | API Key | Direct intelligence queries |
| `/learn` | POST | API Key | Submit learning corrections |
| `/slack/events` | POST | None | Slack webhook handler |
| `/metrics` | GET | None | Prometheus metrics |
| `/circle-of-life/metrics` | GET | API Key | Learning system metrics |

### Example Usage

```bash
# Health check
curl http://localhost:8080/health

# Query Bob's intelligence
curl -H "X-API-Key: test" \
     -H "Content-Type: application/json" \
     -d '{"query": "How do I deploy to Cloud Run?"}' \
     http://localhost:8080/api/query

# Submit learning correction
curl -H "X-API-Key: test" \
     -H "Content-Type: application/json" \
     -d '{"correction": "Actually, use --source . for buildpacks"}' \
     http://localhost:8080/learn
```

## 🧠 Circle of Life Learning

Evidence-driven learning loop with no external scrapers:

1. **Ingest** → Events from `/learn` API and Slack messages
2. **Analyze** → Pattern recognition and grouping
3. **Generate** → LLM insights with confidence scoring
4. **Persist** → High-confidence learnings to Neo4j/BigQuery
5. **Apply** → Continuous improvement of responses

**Triggers**: User corrections, Slack interactions, feedback APIs
**Safeguards**: Deduplication, confidence thresholds, rate limiting

## 🔧 Development

```bash
# Format code
make fmt

# Run all checks
make check-all

# Run tests
make test

# Local development server
make dev-run
```

## 🚀 Deployment

### Cloud Run (Recommended)
```bash
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --memory 1Gi \
  --vpc-connector bob-vpc-connector \
  --set-env-vars BB_API_KEY=your-secure-key
```

### Docker
```bash
docker build -t bobs-brain .
docker run -p 8080:8080 -e BB_API_KEY=test bobs-brain
```

## 🔒 Security Features

- **API Key Authentication** - All endpoints except health/metrics protected
- **Rate Limiting** - Prevents abuse with configurable limits
- **Input Validation** - Pydantic schema validation on all inputs
- **CORS Protection** - Configured origins for API and Slack routes
- **Structured Logging** - JSON logs with event tracking
- **No Hardcoded Secrets** - All sensitive data via environment variables

## 📊 Monitoring

- **Health Checks**: `/health` with component status
- **Metrics**: Prometheus metrics at `/metrics`
- **Logging**: Structured JSON logs with Google Cloud Logging integration
- **Error Tracking**: Comprehensive error handlers with logging

## 🧪 Testing

```bash
# Run test suite
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_circle.py -v
```

**Test Coverage**: API endpoints, Circle of Life learning, authentication, error handling

## 📚 Configuration

See [CONFIG.md](CONFIG.md) for complete environment variable documentation.

**Required**: `BB_API_KEY`, `GCP_PROJECT`
**Optional**: Neo4j, Slack, Circle of Life tuning parameters

## 🏗️ Architecture

- **Framework**: Flask with Gunicorn WSGI
- **AI**: Google Gemini 2.5 Flash via Vertex AI
- **Memory**: Neo4j graph database + BigQuery warehouse
- **Integration**: Slack SDK for real-time messaging
- **Learning**: Circle of Life continuous improvement loop

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built for production • Secure by design • Ready to learn**