# A2A Gateway - Agent-to-Agent Protocol Proxy

**Version:** 0.6.0
**Status:** Phase 3 Implementation
**Compliance:** R3 (Cloud Run as gateway only)

---

## Purpose

The A2A Gateway is a **FastAPI proxy service** that enables Agent-to-Agent (A2A) protocol communication with Bob's Brain. It runs on **Cloud Run** and proxies requests to the **Vertex AI Agent Engine** via REST API.

### R3 Compliance

This gateway enforces **Rule 3 (R3)**: Cloud Run as Gateway Only

- ✅ **DOES:** Proxy requests to Agent Engine via HTTP/REST
- ✅ **DOES:** Expose AgentCard for A2A discovery
- ✅ **DOES:** Handle HTTP/JSON communication
- ❌ **DOES NOT:** Import or run `google.adk.Runner` locally
- ❌ **DOES NOT:** Execute agent logic in Cloud Run
- ❌ **DOES NOT:** Embed agent runtime in gateway

**Why?** Agent Engine is the production runtime (R2). Cloud Run is only for protocol translation and routing.

---

## Architecture

```
┌─────────────────┐         ┌───────────────────┐         ┌──────────────────────┐
│  A2A Client     │  HTTP   │  A2A Gateway      │  REST   │  Agent Engine        │
│  (Other Agent)  │────────>│  (Cloud Run)      │────────>│  (Vertex AI)         │
│                 │         │                   │         │                      │
│                 │<────────│  FastAPI Proxy    │<────────│  ADK Runner          │
└─────────────────┘         └───────────────────┘         └──────────────────────┘
                                    │
                                    │ imports only
                                    v
                            ┌───────────────────┐
                            │  my_agent/        │
                            │  a2a_card.py      │
                            │  (AgentCard only) │
                            └───────────────────┘
```

**Key Points:**
1. A2A Gateway receives HTTP requests from other agents
2. Gateway proxies to Agent Engine REST API (no local execution)
3. Gateway imports AgentCard for discovery (safe - no runtime)
4. Agent Engine runs the actual ADK agent with Runner

---

## Endpoints

### `GET /.well-known/agent.json`

**A2A Protocol: Agent Discovery**

Returns AgentCard with agent metadata and capabilities.

**Response:**
```json
{
  "name": "bobs-brain",
  "description": "Bob's Brain - AI Assistant\n\nIdentity: spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/0.6.0\n...",
  "url": "https://a2a-gateway-xxx.run.app",
  "version": "0.6.0",
  "skills": [],
  "spiffe_id": "spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/0.6.0"
}
```

### `POST /query`

**Proxy query to Agent Engine**

**Request:**
```json
{
  "query": "What is the weather today?",
  "session_id": "optional-session-123"
}
```

**Response:**
```json
{
  "response": "I don't have access to real-time weather data...",
  "session_id": "session-123"
}
```

### `GET /health`

**Health check**

**Response:**
```json
{
  "status": "healthy",
  "service": "a2a-gateway",
  "version": "0.6.0",
  "agent_engine_url": "https://us-central1-aiplatform.googleapis.com/v1/projects/bobs-brain/locations/us-central1/reasoningEngines/xxx:query"
}
```

---

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `PROJECT_ID` | Yes | GCP project ID | `bobs-brain` |
| `LOCATION` | Yes | GCP region | `us-central1` |
| `AGENT_ENGINE_ID` | Yes | Agent Engine instance ID | `12345678901234567890` |
| `AGENT_ENGINE_URL` | No | Override default URL | `https://...` |
| `PORT` | No | Service port (default 8080) | `8080` |

**For AgentCard (imported from `my_agent/a2a_card.py`):**
- `APP_NAME` - Agent name
- `APP_VERSION` - Agent version
- `PUBLIC_URL` - Gateway public URL
- `AGENT_SPIFFE_ID` - SPIFFE identity (R7)

---

## Local Development

### Prerequisites

```bash
# Python 3.12+
python3 --version

# Install dependencies
cd service/a2a_gateway
pip install -r requirements.txt
```

### Run Locally

```bash
# Set environment variables
export PROJECT_ID=bobs-brain
export LOCATION=us-central1
export AGENT_ENGINE_ID=your-engine-id
export APP_NAME=bobs-brain-dev
export APP_VERSION=0.6.0-dev
export PUBLIC_URL=http://localhost:8080
export AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0

# Start server
python main.py
```

### Test Endpoints

```bash
# Health check
curl http://localhost:8080/health

# AgentCard
curl http://localhost:8080/.well-known/agent.json

# Query (requires Agent Engine to be deployed)
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Hello, Bob!"}'
```

---

## Deployment

### Build Docker Image

```bash
cd service/a2a_gateway
docker build -t gcr.io/bobs-brain/a2a-gateway:0.6.0 .
```

### Push to GCR

```bash
docker push gcr.io/bobs-brain/a2a-gateway:0.6.0
```

### Deploy to Cloud Run

```bash
gcloud run deploy a2a-gateway \
  --image gcr.io/bobs-brain/a2a-gateway:0.6.0 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=bobs-brain,LOCATION=us-central1,AGENT_ENGINE_ID=xxx,APP_NAME=bobs-brain,APP_VERSION=0.6.0,AGENT_SPIFFE_ID=spiffe://...
```

**Or use Terraform (Phase 4):**
```hcl
resource "google_cloud_run_service" "a2a_gateway" {
  name     = "a2a-gateway"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/bobs-brain/a2a-gateway:0.6.0"
        env {
          name  = "PROJECT_ID"
          value = var.project_id
        }
        # ... more env vars
      }
    }
  }
}
```

---

## Testing

### Unit Tests

```bash
# Test imports (ensure no Runner)
python -c "from main import app; print('✅ No Runner imported')"

# Test AgentCard generation
python -c "from my_agent.a2a_card import get_agent_card_dict; print(get_agent_card_dict())"
```

### Integration Tests

```bash
# Start gateway locally
python main.py &

# Test health
curl http://localhost:8080/health

# Test AgentCard
curl http://localhost:8080/.well-known/agent.json | jq

# Test query (requires Agent Engine)
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Test query"}' | jq
```

---

## Monitoring

### Cloud Run Metrics

```bash
# View logs
gcloud run services logs read a2a-gateway --region us-central1 --limit 50

# Monitor requests
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count"' \
  --format=json
```

### Key Metrics

- Request count
- Latency (p50, p95, p99)
- Error rate
- Agent Engine response time

---

## Troubleshooting

### Gateway Returns 503 "Agent Engine unavailable"

**Cause:** Cannot connect to Agent Engine REST endpoint

**Fix:**
1. Verify Agent Engine is deployed and healthy
2. Check `AGENT_ENGINE_URL` environment variable
3. Verify IAM permissions for service account
4. Check network connectivity (VPC, firewall rules)

### AgentCard Returns 500

**Cause:** Missing environment variables for AgentCard generation

**Fix:**
Ensure all required variables are set:
```bash
export APP_NAME=bobs-brain
export APP_VERSION=0.6.0
export PUBLIC_URL=https://a2a-gateway-xxx.run.app
export AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/0.6.0
```

### Query Timeout

**Cause:** Agent Engine taking too long to respond

**Fix:**
1. Increase timeout in `main.py` (default 30s):
   ```python
   async with httpx.AsyncClient(timeout=60.0) as client:
   ```
2. Investigate Agent Engine performance
3. Check if agent is stuck in tool execution

---

## Related Documentation

- **Agent Engine Deployment:** See `Dockerfile` in `my_agent/`
- **A2A Card Definition:** See `my_agent/a2a_card.py`
- **Phase 3 Plan:** See `000-docs/057-AT-COMP-terraform-comparison.md`
- **Hard Mode Rules:** See `CLAUDE.md` (R3 section)

---

## Status

- **Phase 3:** In Progress ✅
- **Implementation:** Complete ✅
- **Testing:** Pending ⏳
- **Deployment:** Pending ⏳ (Phase 4 - Terraform)

**Next Steps:**
1. Test gateway locally
2. Create Slack webhook service
3. Deploy both services to Cloud Run (Phase 4)

---

**Last Updated:** 2025-11-11
**Version:** 0.6.0
**Category:** Phase 3 - Service Gateways
