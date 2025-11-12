# Service Gateways

**Version:** 0.6.0
**Status:** Phase 3 Complete
**Compliance:** R3 (Cloud Run as gateway only)

---

## Overview

The `service/` directory contains **Cloud Run gateway services** that enable external access to Bob's Brain running on **Vertex AI Agent Engine**.

These services enforce **Rule 3 (R3)**: Cloud Run serves as protocol gateways only, proxying requests to Agent Engine via REST API. **No local agent execution.**

---

## Architecture

```
┌──────────────────┐         ┌───────────────────────┐         ┌──────────────────────┐
│  External        │         │  Cloud Run Gateways   │         │  Vertex AI           │
│  Clients         │  HTTPS  │  (service/)           │  REST   │  Agent Engine        │
│                  │────────>│                       │────────>│                      │
│  - A2A Agents    │         │  1. A2A Gateway       │         │  ADK Runner          │
│  - Slack Users   │         │  2. Slack Webhook     │         │  + Dual Memory       │
│                  │<────────│                       │<────────│  + Tools             │
└──────────────────┘         └───────────────────────┘         └──────────────────────┘
```

**Key Principles:**
- **R3 Compliant:** Gateways proxy only (no Runner imports)
- **Protocol Translation:** HTTP/REST → Agent Engine API
- **Separation of Concerns:** Gateways handle protocol, Agent Engine handles logic
- **Independent Deployment:** Each gateway is a separate Cloud Run service

---

## Gateways

### 1. A2A Gateway (`a2a_gateway/`)

**Purpose:** Agent-to-Agent (A2A) protocol communication

**Exposes:**
- `GET /.well-known/agent.json` - AgentCard for discovery (R7)
- `POST /query` - Query endpoint for other agents

**Use Cases:**
- Multi-agent orchestration
- Agent discovery and capability negotiation
- Agent-to-agent delegation

**Documentation:** See `a2a_gateway/README.md`

**Deployment:**
```bash
cd service/a2a_gateway
gcloud run deploy a2a-gateway \
  --image gcr.io/bobs-brain/a2a-gateway:0.6.0 \
  --region us-central1
```

**Public URL:** `https://a2a-gateway-xxx.run.app`

### 2. Slack Webhook (`slack_webhook/`)

**Purpose:** Slack integration for user interactions

**Exposes:**
- `POST /slack/events` - Slack Events API webhook
- Handles: `app_mention`, `message.im`, `message.channels`

**Use Cases:**
- @Bob mentions in Slack channels
- Direct messages to Bob
- Team collaboration with AI agent

**Documentation:** See `slack_webhook/README.md`

**Deployment:**
```bash
cd service/slack_webhook
gcloud run deploy slack-webhook \
  --image gcr.io/bobs-brain/slack-webhook:0.6.0 \
  --region us-central1
```

**Public URL:** `https://slack-webhook-xxx.run.app`

---

## R3 Compliance Matrix

| Aspect | Compliant? | Implementation |
|--------|-----------|----------------|
| **No Runner Import** | ✅ | Neither gateway imports `google.adk.Runner` |
| **REST API Only** | ✅ | Both use `httpx` to call Agent Engine endpoint |
| **Protocol Gateway** | ✅ | HTTP/JSON → Agent Engine REST API |
| **No Local Execution** | ✅ | Agent logic runs only in Agent Engine |
| **AgentCard Only** | ✅ | A2A gateway imports `a2a_card.py` (metadata only) |
| **Cloud Run Deployment** | ✅ | Both deployed as Cloud Run services |

**Verification:**
```bash
# Verify no Runner imports
grep -r "from google.adk import Runner" service/
# Should return no results

grep -r "from google.adk.runner import Runner" service/
# Should return no results
```

---

## Shared Patterns

### 1. Agent Engine Proxy Pattern

Both gateways use the same proxy pattern:

```python
import httpx

AGENT_ENGINE_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}:query"

async def query_agent_engine(query: str, session_id: str) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            AGENT_ENGINE_URL,
            json={"query": query, "session_id": session_id}
        )
        return response.json()["response"]
```

### 2. Environment Configuration

Both gateways require:
```bash
PROJECT_ID=bobs-brain
LOCATION=us-central1
AGENT_ENGINE_ID=xxx
AGENT_ENGINE_URL=https://...  # Optional override
```

### 3. Health Checks

Both expose `/health` for monitoring:
```bash
curl https://a2a-gateway-xxx.run.app/health
curl https://slack-webhook-xxx.run.app/health
```

### 4. Logging

Both use structured logging:
```python
logger.info(
    "Processing request",
    extra={
        "session_id": session_id,
        "query_length": len(query)
    }
)
```

---

## Development

### Local Testing

**Start A2A Gateway:**
```bash
cd service/a2a_gateway
export PROJECT_ID=bobs-brain LOCATION=us-central1 AGENT_ENGINE_ID=xxx
python main.py
# http://localhost:8080
```

**Start Slack Webhook:**
```bash
cd service/slack_webhook
export SLACK_BOT_TOKEN=xoxb-... SLACK_SIGNING_SECRET=...
export PROJECT_ID=bobs-brain LOCATION=us-central1 AGENT_ENGINE_ID=xxx
python main.py
# http://localhost:8080
```

### Testing Endpoints

**A2A Gateway:**
```bash
# AgentCard
curl http://localhost:8080/.well-known/agent.json

# Query
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Hello"}'
```

**Slack Webhook:**
```bash
# Health
curl http://localhost:8080/health

# Challenge (Slack verification)
curl -X POST http://localhost:8080/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test"}'
```

---

## Deployment

### Docker Build & Push

**A2A Gateway:**
```bash
cd service/a2a_gateway
docker build -t gcr.io/bobs-brain/a2a-gateway:0.6.0 .
docker push gcr.io/bobs-brain/a2a-gateway:0.6.0
```

**Slack Webhook:**
```bash
cd service/slack_webhook
docker build -t gcr.io/bobs-brain/slack-webhook:0.6.0 .
docker push gcr.io/bobs-brain/slack-webhook:0.6.0
```

### Cloud Run Deployment

**Manual (gcloud):**
```bash
# A2A Gateway
gcloud run deploy a2a-gateway \
  --image gcr.io/bobs-brain/a2a-gateway:0.6.0 \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=bobs-brain,LOCATION=us-central1,AGENT_ENGINE_ID=xxx

# Slack Webhook
gcloud run deploy slack-webhook \
  --image gcr.io/bobs-brain/slack-webhook:0.6.0 \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SLACK_BOT_TOKEN=xoxb-...,SLACK_SIGNING_SECRET=...,PROJECT_ID=bobs-brain,LOCATION=us-central1,AGENT_ENGINE_ID=xxx
```

**Automated (Phase 4 - Terraform):**
See `infra/terraform/cloud_run.tf` (coming in Phase 4)

---

## Monitoring

### Cloud Run Metrics

```bash
# A2A Gateway metrics
gcloud run services describe a2a-gateway --region us-central1

# Slack Webhook metrics
gcloud run services describe slack-webhook --region us-central1
```

### Logs

```bash
# Real-time logs
gcloud run services logs tail a2a-gateway --region us-central1
gcloud run services logs tail slack-webhook --region us-central1

# Recent logs
gcloud run services logs read a2a-gateway --region us-central1 --limit 50
gcloud run services logs read slack-webhook --region us-central1 --limit 50
```

### Key Metrics

- **Request count**: Total requests per gateway
- **Error rate**: 4xx/5xx errors
- **Latency**: p50, p95, p99 response times
- **Agent Engine calls**: Proxy request count
- **Cold starts**: Container startup time

---

## Troubleshooting

### Gateway Returns 503 "Agent Engine unavailable"

**Cause:** Cannot connect to Agent Engine

**Fix:**
1. Verify Agent Engine is deployed and healthy
2. Check `AGENT_ENGINE_URL` environment variable
3. Verify IAM permissions for Cloud Run service account
4. Check network connectivity (VPC, firewall rules)

### Slack Not Responding

**Cause:** Webhook not receiving events or failing signature verification

**Fix:**
1. Verify Slack webhook URL matches Cloud Run URL
2. Check Cloud Run logs for signature errors
3. Verify `SLACK_SIGNING_SECRET` matches Slack app
4. Test health endpoint: `curl https://slack-webhook-xxx.run.app/health`

### A2A AgentCard Returns 500

**Cause:** Missing environment variables for AgentCard generation

**Fix:**
Ensure all required variables are set in Cloud Run:
- `APP_NAME`
- `APP_VERSION`
- `PUBLIC_URL`
- `AGENT_SPIFFE_ID`

---

## Phase 4 Preview

In **Phase 4 (Terraform Infrastructure)**, these gateways will be deployed via Terraform:

```hcl
# infra/terraform/cloud_run.tf

resource "google_cloud_run_service" "a2a_gateway" {
  name     = "a2a-gateway"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/a2a-gateway:${var.app_version}"
        env { ... }
      }
    }
  }
}

resource "google_cloud_run_service" "slack_webhook" {
  name     = "slack-webhook"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/slack-webhook:${var.app_version}"
        env { ... }
      }
    }
  }
}
```

**Benefits:**
- Infrastructure as Code
- Version control for infrastructure
- CI/CD deployment automation
- Multi-environment support (dev/staging/prod)
- Drift detection (R8)

---

## Related Documentation

- **A2A Gateway:** `a2a_gateway/README.md`
- **Slack Webhook:** `slack_webhook/README.md`
- **Agent Engine:** `my_agent/README.md`
- **Phase 3 Completion:** `000-docs/058-LS-COMP-phase-3-complete.md`
- **Terraform Comparison:** `000-docs/057-AT-COMP-terraform-comparison.md`
- **Hard Mode Rules:** `CLAUDE.md` (R3 section)

---

## Status

- **Phase 3:** Complete ✅
- **A2A Gateway:** Implemented ✅
- **Slack Webhook:** Implemented ✅
- **Local Testing:** Pending ⏳
- **Cloud Run Deployment:** Pending ⏳ (Phase 4 - Terraform)

**Next Phase:** Phase 4 - Terraform Infrastructure

---

**Last Updated:** 2025-11-11
**Version:** 0.6.0
**Category:** Phase 3 - Service Gateways
