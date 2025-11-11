# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Bob's Vertex Agent** (IAM1 Regional Manager) is a production-deployed hierarchical multi-agent system on Google Cloud's Vertex AI Agent Engine. This is the **ACTUAL DEPLOYED VERSION** of Bob's Brain, not the experimental Flask implementation.

## ⚠️ CRITICAL: This is the Production System

When working on Bob's Brain, you are working on **bob-vertex-agent/** which is deployed to:
- **Project:** `bobs-brain` (GCP Project ID: 205354194989)
- **Agent Engine ID:** `projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448`
- **Slack Webhook:** `https://slack-webhook-eow2wytafa-uc.a.run.app` (Cloud Functions Gen2)
- **Region:** us-central1

## Architecture

```
Slack Events → Cloud Function → Vertex AI Agent Engine (Bob - IAM1)
                (slack-webhook)   └─→ Sub-Agents (IAM2s: Research, Code, Data, Slack)
                                  └─→ RAG (Vertex AI Search + Rank)
                                  └─→ A2A Protocol (6 peer IAM1s)
```

### Core Components

1. **Root Agent (IAM1 - Bob)** - `app/agent.py`
   - Model: Gemini 2.5 Flash
   - 3 tools: `retrieve_docs` (RAG), `route_to_agent` (delegation), `coordinate_with_peer_iam1` (A2A)
   - Decision framework with 5 routing patterns

2. **Sub-Agents (IAM2 Specialists)** - `app/sub_agents.py`
   - Research Agent (Gemini 2.5 Flash)
   - Code Agent (Gemini 2.0 Flash)
   - Data Agent (Gemini 2.5 Flash)
   - Slack Agent (Gemini 2.0 Flash)

3. **RAG System** - `app/retrievers.py`
   - Vertex AI Search datastore
   - text-embedding-005 embeddings
   - Vertex AI Rank for re-ranking (top 5 docs)
   - Data ingestion via Vertex AI Pipelines

4. **Slack Integration** - `slack-webhook/main.py`
   - Cloud Functions Gen2 (Python 3.12)
   - Immediate HTTP 200 response
   - Background thread processing
   - Event deduplication cache

5. **A2A Protocol** - `app/a2a_tools.py`
   - 6 peer domains (Engineering, Sales, Operations, Marketing, Finance, HR)
   - JSON-RPC 2.0 communication
   - 30-second timeout per request

## Technology Stack

- **Framework:** Google ADK 1.15.0+
- **LLMs:** Gemini 2.5/2.0 Flash
- **Knowledge:** Vertex AI Search + Rank
- **Integration:** LangChain 0.3.24+
- **Observability:** Cloud Trace + Cloud Logging + OpenTelemetry
- **Package Manager:** uv 0.8.13
- **Infrastructure:** Terraform (deployment/terraform/)
- **CI/CD:** GitHub Actions with Workload Identity Federation

## Quick Start

### Local Development

```bash
# Install dependencies
make install

# Launch playground (Streamlit UI)
make playground

# Run tests
make test
```

### Deploy Agent to Vertex AI

```bash
# Deploy to Agent Engine
make deploy

# This will:
# 1. Export dependencies to requirements.txt
# 2. Upload code to Agent Engine
# 3. Update deployment_metadata.json
# 4. Return new Agent Engine ID
```

### Deploy Slack Webhook

```bash
# Deploy Cloud Function
gcloud functions deploy slack-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --source=./slack-webhook \
  --entry-point=slack_events \
  --trigger-http \
  --allow-unauthenticated \
  --project=bobs-brain \
  --set-env-vars=PROJECT_ID=bobs-brain

# Get webhook URL
gcloud functions describe slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --gen2 \
  --format='value(serviceConfig.uri)'
```

## Slack Integration Setup

**Current Deployment:**
- **Cloud Function URL:** `https://slack-webhook-eow2wytafa-uc.a.run.app`
- **Slack App ID:** `A099YKLCM1N`

### Configure Slack App

1. **Go to Event Subscriptions:**
   ```
   https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
   ```

2. **Set Request URL:**
   ```
   https://slack-webhook-eow2wytafa-uc.a.run.app
   ```

3. **Subscribe to Bot Events:**
   - `message.channels` - Messages in public channels
   - `message.im` - Direct messages
   - `app_mention` - When @bob is mentioned

4. **Required OAuth Scopes (OAuth & Permissions page):**
   - `chat:write` - Send messages
   - `chat:write.public` - Send to public channels
   - `channels:history` - Read messages
   - `channels:read` - View channels
   - `app_mentions:read` - Know when mentioned
   - `users:read` - View user info

5. **Install App to Workspace:**
   - Go to OAuth & Permissions page
   - Click "Install to Workspace"
   - Copy Bot User OAuth Token (xoxb-...)
   - Store in Google Secret Manager:
     ```bash
     echo "xoxb-YOUR-TOKEN" | gcloud secrets create slack-bot-token \
       --data-file=- \
       --project=bobs-brain
     ```

### Test Slack Integration

```bash
# Test URL verification
curl -X POST https://slack-webhook-eow2wytafa-uc.a.run.app \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'

# Should return: {"challenge":"test123"}
```

Then in Slack:
- Mention @Bob in any channel
- Send Bob a direct message
- Bob will respond via the Agent Engine

## Infrastructure Setup

### Terraform Deployment

```bash
# Navigate to terraform directory
cd deployment/terraform/dev

# Initialize Terraform
terraform init

# Plan infrastructure changes
terraform plan --var-file vars/env.tfvars --var dev_project_id=bobs-brain

# Apply infrastructure
terraform apply --var-file vars/env.tfvars --var dev_project_id=bobs-brain --auto-approve
```

**Creates:**
- Service accounts (CICD, app, pipeline)
- GCS buckets (RAG, logs)
- IAM bindings
- Workload Identity Federation
- GitHub repository secrets
- Vertex AI Search datastore

### Data Ingestion (RAG)

```bash
# Run data ingestion pipeline
make data-ingestion

# This will:
# 1. Upload docs from knowledge-base/ to GCS
# 2. Run Vertex AI Pipeline for ingestion
# 3. Update Vertex AI Search datastore
# 4. Generate embeddings with text-embedding-005
```

## Directory Structure

```
bob-vertex-agent/
├── app/                          # Agent application code
│   ├── agent.py                  # Root agent (IAM1)
│   ├── agent_engine_app.py       # Agent Engine entry point
│   ├── sub_agents.py             # IAM2 specialists
│   ├── a2a_tools.py              # A2A Protocol
│   ├── retrievers.py             # RAG pipeline
│   ├── iam1_config.py            # Business model config
│   └── templates.py              # Prompt templates
├── slack-webhook/                # Cloud Function for Slack
│   ├── main.py                   # Webhook handler
│   └── requirements.txt          # Dependencies
├── deployment/                   # Infrastructure as Code
│   ├── terraform/                # Terraform modules
│   │   ├── dev/                  # Dev environment
│   │   ├── providers.tf          # GCP, GitHub, Random
│   │   ├── apis.tf               # GCP services
│   │   ├── iam.tf                # Permissions
│   │   ├── service_accounts.tf  # Service accounts
│   │   ├── storage.tf            # GCS buckets
│   │   ├── github.tf             # GitHub secrets
│   │   └── wif.tf                # Workload Identity
│   └── README.md                 # Deployment guide
├── data_ingestion/               # RAG data pipeline
│   └── data_ingestion_pipeline/  # Vertex AI Pipeline
├── tests/                        # Test suites
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── load_test/                # Load testing (Locust)
├── notebooks/                    # Jupyter notebooks
├── claudes-docs/                 # AI-generated documentation
│   ├── 004-AT-ARCH-bob-vertex-system-analysis.md
│   └── 005-DR-QREF-system-quick-reference.md
├── .github/workflows/            # CI/CD pipelines
│   ├── pr_checks.yaml            # PR validation
│   ├── staging.yaml              # Deploy to staging
│   ├── deploy-to-prod.yaml       # Production deployment
│   ├── deploy-slack-webhook.yml  # Slack webhook deployment
│   └── daily-data-ingestion.yml  # Daily RAG updates
├── Makefile                      # Development commands
├── pyproject.toml                # Dependencies (uv)
├── uv.lock                       # Dependency lock file
├── deployment_metadata.json      # Current Agent Engine ID
├── README.md                     # Project overview
└── DEPLOYMENT_GUIDE.md           # Business model & scenarios
```

## Key Files Reference

- `app/agent.py:1` - Root IAM1 agent (Gemini 2.5 Flash orchestrator)
- `app/sub_agents.py:1` - IAM2 specialists (Research, Code, Data, Slack)
- `app/a2a_tools.py:1` - A2A Protocol for peer IAM1 coordination
- `app/retrievers.py:1` - RAG retrieval pipeline (Vertex AI Search + Rank)
- `app/agent_engine_app.py:1` - Agent Engine entry point
- `slack-webhook/main.py:27` - Agent Engine ID (hardcoded)
- `deployment/terraform/` - Complete infrastructure as code
- `.github/workflows/` - CI/CD pipelines
- `deployment_metadata.json` - Current deployment info

## CI/CD Pipeline

### GitHub Actions Workflows

**PR Checks** (`.github/workflows/pr_checks.yaml`)
- Runs on pull requests
- Validates: lint, tests, type checking

**Staging Deployment** (`.github/workflows/staging.yaml`)
- Triggers on: push to main, manual
- Steps:
  1. Deploy agent to staging Agent Engine
  2. Run load tests (Locust)
  3. Trigger production deployment (if tests pass)

**Production Deployment** (`.github/workflows/deploy-to-prod.yaml`)
- Triggers: manual approval required
- Steps:
  1. Deploy agent to production Agent Engine
  2. Update deployment metadata
  3. Notify stakeholders

**Slack Webhook** (`.github/workflows/deploy-slack-webhook.yml`)
- Triggers on: slack-webhook/ changes
- Deploys Cloud Function to us-central1

### Workload Identity Federation (WIF)

**No static secrets!** All GitHub Actions authenticate via WIF:
- Workload Identity Pool: `github-pool`
- Provider: `github-provider`
- Service Account: `github-actions@bobs-brain.iam.gserviceaccount.com`

## Environment Variables

### Required for Agent Deployment

```bash
# GCP Project
PROJECT_ID=bobs-brain
REGION=us-central1

# Agent Engine (set by deployment)
AGENT_ENGINE_ID=projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448

# Observability
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

### Required for Slack Webhook

```bash
# GCP Project
PROJECT_ID=bobs-brain

# Slack (stored in Secret Manager)
# slack-bot-token → xoxb-...
```

## Business Model

**Three Product Tiers:**

1. **IAM1 Basic** - Base price/month
   - Conversational AI with Gemini 2.5 Flash
   - RAG knowledge grounding (Vertex AI Search)
   - Slack integration

2. **IAM1 + IAM2 Team** - + $200/month per specialist
   - IAM1 Basic +
   - Research Agent ($200/month)
   - Code Agent ($200/month)
   - Data Agent ($200/month)
   - Task delegation to specialists

3. **Multi-IAM1 Enterprise** - Custom pricing
   - Multiple IAM1 deployments (per department/client)
   - A2A coordination between IAM1s
   - Each IAM1 can have IAM2 teams
   - Client-isolated knowledge bases

## Agent Capabilities

### Root Agent (IAM1) Decision Framework

**5 Routing Patterns:**

1. **Simple Question** → Direct response (no delegation)
2. **Research Required** → Delegate to Research Agent
3. **Code/Technical** → Delegate to Code Agent
4. **Data/Analytics** → Delegate to Data Agent
5. **Cross-Domain** → Coordinate with peer IAM1 via A2A

### Sub-Agents (IAM2) Specializations

**Research Agent:**
- Knowledge synthesis
- Multi-source research
- Summarization
- Comparative analysis

**Code Agent:**
- Programming assistance
- Code review
- Debugging
- Technical documentation

**Data Agent:**
- SQL query generation
- Data analysis
- Visualization recommendations
- Statistical analysis

**Slack Agent:**
- Message formatting
- Markdown conversion
- Thread management
- Emoji selection

### RAG Retrieval Pipeline

**Process:**
1. User query → text-embedding-005 embedding
2. Query Vertex AI Search datastore
3. Retrieve top 10 candidate documents
4. Re-rank with Vertex AI Rank → top 5 documents
5. Inject into agent context
6. Agent generates response with citations

## Testing

### Run Tests Locally

```bash
# Unit tests
uv run pytest tests/unit

# Integration tests
uv run pytest tests/integration

# All tests
make test
```

### Load Testing

```bash
# Navigate to load test directory
cd tests/load_test

# Run Locust load test
locust -f load_test.py --host=<AGENT_ENGINE_URL>
```

**Targets:**
- 100 concurrent users
- 1000 requests/minute
- P95 latency < 5 seconds
- Error rate < 1%

## Monitoring & Observability

### Cloud Logging

```bash
# View agent logs
gcloud logging read "resource.type=aiplatform.googleapis.com/ReasoningEngine" \
  --project=bobs-brain \
  --limit=50 \
  --format=json

# View Slack webhook logs
gcloud functions logs read slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --limit=50
```

### Cloud Trace

**View traces in Console:**
```
https://console.cloud.google.com/traces/list?project=bobs-brain
```

### Key Metrics

- **Agent invocations/day** - Query volume
- **P50/P95/P99 latency** - Response times
- **RAG retrieval accuracy** - Relevance of retrieved docs
- **Sub-agent delegation rate** - % of queries delegated
- **A2A coordination requests** - Cross-IAM1 communication
- **Error rate** - Failed queries
- **Cost per query** - Token usage + compute

## Cost Estimation

**Per 1000 Queries:**

- **Gemini 2.5 Flash (IAM1):** $0.10 - $0.30
- **Gemini 2.0 Flash (IAM2s):** $0.05 - $0.15 per specialist
- **Vertex AI Search:** $0.50 - $1.50
- **Vertex AI Rank:** $0.20 - $0.50
- **Cloud Functions:** $0.01 - $0.05
- **Embeddings (text-embedding-005):** $0.05 - $0.15

**Total:** ~$1.00 - $3.00 per 1000 queries (without sub-agents)

**With IAM2 Team:** +$0.50 - $1.50 per 1000 queries (depending on delegation rate)

## Troubleshooting

### Agent Not Responding

```bash
# Check Agent Engine status
gcloud ai reasoning-engines describe 5828234061910376448 \
  --project=bobs-brain \
  --region=us-central1

# Check Cloud Function status
gcloud functions describe slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --gen2
```

### Slack Events Not Received

```bash
# Test webhook endpoint
curl -X POST https://slack-webhook-eow2wytafa-uc.a.run.app \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'

# Check function logs
gcloud functions logs read slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --limit=20
```

### RAG Not Retrieving Relevant Docs

```bash
# Check datastore status
gcloud discoveryengine data-stores describe bob-vertex-agent-datastore \
  --location=us \
  --project=bobs-brain

# Re-run data ingestion
make data-ingestion
```

### Deployment Fails

```bash
# Check service account permissions
gcloud projects get-iam-policy bobs-brain \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:github-actions@bobs-brain.iam.gserviceaccount.com"

# Verify WIF configuration
gcloud iam workload-identity-pools describe github-pool \
  --location=global \
  --project=bobs-brain
```

## Important Implementation Notes

### Multiple Implementations in Parent Directory

The parent directory (`/home/jeremy/000-projects/iams/bobs-brain/`) contains **FOUR different implementations**:

1. **bob-vertex-agent/** (THIS ONE - PRODUCTION) - Vertex AI Agent Engine + Cloud Functions
2. **02-Src/** - Flask app with modular LLM providers (experimental)
3. **adk-agent/** - Google ADK implementation (experimental)
4. **genkit-agent/** - Genkit implementation (experimental)

**ALWAYS work on bob-vertex-agent/** when developing Bob's Brain production features.

### Deployment Metadata

Current deployment info is stored in `deployment_metadata.json`:
```json
{
  "remote_agent_engine_id": "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448",
  "deployment_timestamp": "2025-11-09T17:04:54.512515"
}
```

**Update this file after every deployment!**

### Security Best Practices

- **No static secrets in code** - Use Secret Manager
- **WIF for CI/CD** - No service account keys in GitHub
- **IAM principle of least privilege** - Minimal permissions per SA
- **Client isolation** - Separate projects per client
- **Audit logging** - Cloud Audit Logs enabled

### Git Workflow

- **Main branch:** `feature/vertex-ai-genkit-migration` (current)
- **Production branch:** TBD (set up after MVP)
- Create feature branches from current branch
- Run `make test` and `make lint` before committing

## Performance Targets

- **Agent response time:** < 5s (P95)
- **RAG retrieval:** < 2s
- **Slack response:** < 7s end-to-end
- **Uptime:** 99.9% (managed by Vertex AI)
- **Error rate:** < 1%

## Documentation References

- **System Analysis:** `claudes-docs/004-AT-ARCH-bob-vertex-system-analysis.md`
- **Quick Reference:** `claudes-docs/005-DR-QREF-system-quick-reference.md`
- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **Business Model:** `DEPLOYMENT_GUIDE.md` (Scenarios section)
- **README:** `README.md` (IAM1 Regional Manager overview)

## Support & Resources

- **GCP Project:** https://console.cloud.google.com/home/dashboard?project=bobs-brain
- **Agent Engine:** https://console.cloud.google.com/vertex-ai/reasoning-engines?project=bobs-brain
- **Slack App:** https://api.slack.com/apps/A099YKLCM1N
- **GitHub Actions:** https://github.com/jeremylongshore/bobs-brain/actions
- **Terraform State:** GCS bucket `bobs-brain-terraform-state`

---

**Last Updated:** 2025-11-09
**Current Deployment:** Agent Engine ID 5828234061910376448
**Slack Webhook:** https://slack-webhook-eow2wytafa-uc.a.run.app
**Status:** Production Active
