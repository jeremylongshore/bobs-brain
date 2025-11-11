# Bob's Brain

Production Cloud Run gateway that proxies to Vertex AI Reasoning Engine with OpenTelemetry tracing and blue/green deployments.

## Architecture (Phase 4)

Bob's Brain uses a clean proxy pattern where the gateway runs on Cloud Run and calls the remote Reasoning Engine:

```
┌───────────────────────────────────────────────────────────────┐
│                        Bob's Brain                             │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  Client  ────▶  Cloud Run Gateway  ────▶  Reasoning Engine   │
│                 (FastAPI Proxy)            (Vertex AI)         │
│                 • REST Client              • ADK Agent         │
│                 • OpenTelemetry            • Memory Bank       │
│                 • No Runner!               • RAG               │
│                                                                 │
└───────────────────────────────────────────────────────────────┘
```

**CRITICAL**: Gateway does NOT run the agent - it proxies REST calls to Vertex AI Reasoning Engine.

### Components

1. **Cloud Run Gateway** (`gateway/`)
   - FastAPI application deployed to Cloud Run
   - Proxies to Reasoning Engine via REST API (`:query` and `:streamQuery`)
   - OpenTelemetry instrumentation with Cloud Trace export
   - Health checks, A2A protocol, streaming support
   - **NO ADK Runner imports** - pure REST proxy

2. **Reasoning Engine** (Vertex AI)
   - Managed service where agent executes
   - Built with Google ADK
   - Memory Bank for conversation persistence
   - RAG capabilities

3. **Infrastructure** (`infra/terraform/`)
   - Terraform IaC for Cloud Run deployment
   - IAM: `aiplatform.user` + `cloudtrace.agent` roles
   - Health probes and auto-scaling

4. **CI/CD** (`.github/workflows/`)
   - Blue/green deployment with canary rollout
   - 10% canary → health checks → 100% promotion
   - Auto-rollback on failure

## Quick Start

### Prerequisites
- GCP project with Reasoning Engine deployed
- Reasoning Engine ID (e.g., `bobs-brain-engine`)
- Docker and Terraform installed

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export AGENT_ENGINE_NAME="projects/YOUR_PROJECT/locations/us-central1/reasoningEngines/YOUR_ENGINE_ID"
export ENGINE_MODE=agent_engine

# Start gateway
uvicorn gateway.main:app --host 127.0.0.1 --port 8080
```

### Test Endpoints

```bash
# Health check (with trace headers)
curl http://localhost:8080/_health

# A2A card
curl http://localhost:8080/card

# Non-streaming invoke
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, how are you?"}'

# Streaming invoke (SSE)
curl -N -X POST http://localhost:8080/invoke/stream \
  -H "Content-Type: application/json" \
  -d '{"text":"Tell me a story"}'
```

## Deployment

### Build and Push Image

```bash
export PROJECT_ID=your-gcp-project
IMG="gcr.io/${PROJECT_ID}/bobs-brain-gateway:$(git rev-parse --short HEAD)"
gcloud builds submit --tag "$IMG"
```

### Deploy with Terraform

```bash
cd infra/terraform/envs/dev

# Initialize
terraform init

# Deploy
terraform apply \
  -var "project_id=$PROJECT_ID" \
  -var "image=$IMG" \
  -var "engine_id=bobs-brain-engine"

# Get gateway URL
terraform output gateway_url
```

### Test Deployed Gateway

```bash
GATEWAY_URL=$(terraform -chdir=infra/terraform/envs/dev output -raw gateway_url)

# Health check
curl $GATEWAY_URL/_health

# Invoke agent
curl -X POST $GATEWAY_URL/invoke \
  -H "Content-Type: application/json" \
  -d '{"text":"ping"}'
```

## API Endpoints

### Health & Discovery

- `GET /_health` - Health check with trace headers
  ```json
  {"status":"ok","mode":"agent_engine","engine":"projects/.../reasoningEngines/..."}
  ```

- `GET /card` - A2A AgentCard metadata
- `GET /.well-known/agent-card.json` - A2A discovery endpoint

### Invocation

- `POST /invoke` - Non-streaming agent invocation
  ```bash
  curl -X POST $URL/invoke \
    -H "Content-Type: application/json" \
    -d '{"text":"What is 2+2?"}'
  ```

- `POST /invoke/stream` - Streaming agent invocation (SSE)
  ```bash
  curl -N -X POST $URL/invoke/stream \
    -H "Content-Type: application/json" \
    -d '{"text":"Tell me a joke"}'
  ```

## OpenTelemetry Tracing

All responses include `X-Trace-Id` headers for distributed tracing:

```bash
curl -v http://localhost:8080/_health
# < X-Trace-Id: 4bf92f3577b34da6a3ce929d0e0e4736
```

**View traces in Cloud Trace:**
```
https://console.cloud.google.com/traces/list?project=YOUR_PROJECT
```

Instrumentation includes:
- FastAPI requests/responses
- Outbound HTTP calls to Reasoning Engine
- Automatic span creation and propagation

## CI/CD: Blue/Green Deployment

The CI pipeline implements safe canary rollouts:

1. **Build** - Build and push image to GCR
2. **Deploy** - Terraform apply with new image
3. **Canary** - Shift 10% traffic to new revision
4. **Health Checks** - Test `/_health`, `/invoke`, `/card`
5. **Promote** - If checks pass, shift 100% traffic
6. **Rollback** - If checks fail, revert to previous revision

**Workflow:** `.github/workflows/deploy-gateway-bluegreen.yml`

**Triggers:** Push to `main` affecting `gateway/` or `infra/`

**Required Secrets:**
- `GCP_PROJECT_ID` - GCP project
- `GCP_WIF_PROVIDER` - Workload Identity Federation provider
- `GCP_WIF_SA` - Service account email
- `ENGINE_ID` - Reasoning Engine ID
- `CANARY_PERCENT` - Canary percentage (default: 10)

## Environment Variables

### Gateway Configuration

- `AGENT_ENGINE_NAME` - Full resource name (projects/.../reasoningEngines/...)
- `AGENT_ENGINE_ID` - Alternative to AGENT_ENGINE_NAME
- `ENGINE_MODE` - Always `agent_engine` (prod proxy mode)
- `PROJECT_ID` - GCP project ID
- `LOCATION` - GCP region (default: us-central1)

### A2A Card (Optional)

- `A2A_NAME` - Agent name (default: "Bob's Brain")
- `A2A_DESC` - Agent description
- `A2A_VERSION` - Agent version (default: "4.0.0")

## Project Structure

```
.
├── 000-docs/                     # Documentation and AARs
├── gateway/                      # Cloud Run gateway (NO ADK)
│   ├── main.py                   # FastAPI app with OpenTelemetry
│   ├── engine_client.py          # REST client for Reasoning Engine
│   └── Dockerfile                # Container build
├── infra/terraform/              # Infrastructure as Code
│   ├── modules/
│   │   ├── cloud_run_gateway/    # Cloud Run deployment + IAM
│   │   └── agent_engine/         # Engine resource name construction
│   └── envs/
│       └── dev/                  # Development environment
├── tests/integration/            # Integration tests
│   └── test_gateway_invoke_local.py
├── .github/workflows/            # CI/CD
│   └── deploy-gateway-bluegreen.yml
└── requirements.txt              # Python dependencies
```

## IAM Roles

The Cloud Run service account requires:

- `roles/aiplatform.user` - Call Reasoning Engine API
- `roles/cloudtrace.agent` - Export traces to Cloud Trace

Granted automatically by Terraform module.

## Testing

```bash
# Run integration tests
pytest tests/integration/ -v

# Run specific test
pytest tests/integration/test_gateway_invoke_local.py::test_invoke_non_stream -v
```

Tests verify:
- Gateway starts successfully
- Health endpoint returns 200 OK
- Trace headers present on responses
- Card endpoints return valid structure

## Monitoring

### Health Checks

Cloud Run performs automatic health checks:
- **Startup probe** - `/_health` endpoint, 10s initial delay
- **Liveness probe** - `/_health` endpoint, 30s initial delay, 10s period

### Traces

View distributed traces in Cloud Trace:
1. Go to Cloud Console → Trace
2. Search for `service.name: bobs-brain-gateway`
3. Click trace to see spans and latencies

### Logs

View logs in Cloud Logging:
```bash
gcloud logging read "resource.type=cloud_run_revision \
  AND resource.labels.service_name=bobs-brain-gateway" \
  --limit 50 \
  --format json
```

## Development Commands

```bash
# Local development
uvicorn gateway.main:app --reload --host 127.0.0.1 --port 8080

# Build image
docker build -f gateway/Dockerfile -t bobs-brain-gateway .

# Run container
docker run -p 8080:8080 \
  -e AGENT_ENGINE_NAME="projects/.../reasoningEngines/..." \
  -e ENGINE_MODE=agent_engine \
  bobs-brain-gateway

# Run tests
pytest tests/integration/ -v

# Terraform validate
terraform -chdir=infra/terraform/envs/dev validate
```

## Troubleshooting

### Gateway Returns 500 on /invoke

**Cause:** AGENT_ENGINE_NAME not set or invalid

**Fix:**
```bash
# Check environment
curl $GATEWAY_URL/_health | jq .engine

# Update Terraform
terraform apply \
  -var "engine_id=correct-engine-id"
```

### Traces Not Appearing in Cloud Trace

**Cause:** Service account missing `cloudtrace.agent` role

**Fix:** Terraform module grants this automatically. If missing:
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/cloudtrace.agent"
```

### Canary Deployment Fails

**Cause:** Health checks failing

**Fix:** Check logs:
```bash
gcloud run revisions describe REVISION_NAME \
  --region us-central1 \
  --format="value(status.conditions)"
```

## Documentation

See `000-docs/` for detailed documentation:
- Architecture diagrams
- After-Action Reports (AARs)
- Deployment runbooks
- Troubleshooting guides

## Contributing

1. Create feature branch from `main`
2. Make changes
3. Run tests: `pytest tests/`
4. Create pull request
5. CI will run blue/green deployment on merge

## License

See LICENSE file for details.
