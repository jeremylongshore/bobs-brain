# Bob's Vertex Agent - Quick Reference Guide

**Date:** 2025-11-09 | **Version:** 2.0.1 | **Type:** Reference Guide

---

## SYSTEM OVERVIEW (30 SECONDS)

**What:** IAM1 Regional Manager - hierarchical multi-agent system on Vertex AI Agent Engine

**Who:** Bob (root agent) + 4 IAM2 specialists + peer IAM1s via A2A Protocol

**Where:** Google Cloud (Vertex AI Agent Engine, Slack integration)

**Why:** Orchestrate AI teams grounded in private knowledge bases

**How:** Python 3.10+ with Google ADK, Gemini LLMs, Vertex AI Search RAG

---

## ARCHITECTURE AT A GLANCE

```
USER INTERACTION
├─ Slack Webhook (Cloud Functions) → Background query
├─ Playground UI (local dev) → Direct testing
└─ Agent Engine API → REST access

ROOT AGENT (IAM1 - Bob)
├─ Model: Gemini 2.5 Flash
├─ Decision: Route to right tool/agent
└─ Tools:
    ├─ retrieve_docs → Vertex AI Search (RAG)
    ├─ route_to_agent → IAM2 specialists
    └─ coordinate_with_peer_iam1 → A2A Protocol

SUB-AGENTS (IAM2 Specialists)
├─ Research: Gemini 2.5 Flash (deep analysis)
├─ Code: Gemini 2.0 Flash (programming)
├─ Data: Gemini 2.5 Flash (analytics)
└─ Slack: Gemini 2.0 Flash (formatting)

KNOWLEDGE GROUNDING
├─ Vertex AI Search: Custom embeddings + ranking
├─ Data Ingestion: Cloud Storage → Pipeline → Datastore
└─ Re-ranking: Vertex AI Rank (top 5 documents)
```

---

## KEY FILES MAP

| Purpose | File | Key Lines |
|---------|------|-----------|
| Root Agent | `app/agent.py` | 211-218 |
| Sub-Agents | `app/sub_agents.py` | 63-210 |
| A2A Protocol | `app/a2a_tools.py` | 24-178 |
| RAG Retriever | `app/retrievers.py` | 25-83 |
| Agent Engine | `app/agent_engine_app.py` | 32-74 |
| Slack Webhook | `slack-webhook/main.py` | 90-141 |
| IAM Config | `app/iam1_config.py` | 1-127 |
| Makefile | `Makefile` | - |
| Dependencies | `pyproject.toml` | - |

---

## DEPLOYMENT PIPELINE

```
COMMIT TO MAIN (push)
   │
   ├─► Staging Workflow (staging.yaml)
   │   ├─ Deploy data pipeline
   │   ├─ Deploy Agent Engine (staging)
   │   ├─ Run load test (2 users, 30s)
   │   └─ Trigger production (if success)
   │
   └─► Production Workflow (deploy-to-prod.yaml) [Manual approval]
       ├─ Deploy data pipeline
       └─ Deploy Agent Engine (production)

SLACK CHANGES (push slack-webhook/)
   │
   └─► Deploy Slack webhook (deploy-slack-webhook.yml)
       ├─ Deploy Cloud Function (gen2, Python 3.12)
       └─ Display Slack configuration
```

---

## QUICK COMMANDS

```bash
# Development
make install              # Install dependencies
make playground          # Start local dev UI (port 8501)
make test                # Run tests
make lint                # Code quality checks

# Deployment
make setup-dev-env       # Create infrastructure (Terraform)
make deploy              # Deploy to Agent Engine
make data-ingestion      # Run RAG data ingestion

# Manual Overrides
uv run adk web . --port 8501  # Direct playground command
```

---

## ENVIRONMENT VARIABLES

### Required (Deployed)
```bash
GOOGLE_CLOUD_PROJECT          # Auto-set by GCP
DATA_STORE_ID                 # bob-vertex-agent-datastore-{staging|prod}
DATA_STORE_REGION             # us (Vertex AI Search)
ARTIFACTS_BUCKET_NAME         # {project_id}-bob-vertex-agent-rag
```

### Optional (A2A Peer Coordination)
```bash
IAM1_ENGINEERING_URL          # Peer agent endpoints
IAM1_SALES_URL
IAM1_OPERATIONS_URL
IAM1_MARKETING_URL
IAM1_FINANCE_URL
IAM1_HR_URL
IAM1_A2A_API_KEY              # Authentication for A2A
```

### GitHub Secrets (CI/CD)
```
WIF_POOL_ID                   # Workload Identity Pool
WIF_PROVIDER_ID               # Workload Identity Provider
GCP_SERVICE_ACCOUNT           # CICD service account email
```

### GitHub Variables (CI/CD)
```
GCP_PROJECT_NUMBER            # Project number (from gcloud)
CICD_PROJECT_ID               # CI/CD runner project
STAGING_PROJECT_ID            # Staging deployment project
PROD_PROJECT_ID               # Production deployment project
REGION                        # us-central1
DATA_STORE_REGION             # us
DATA_STORE_ID_STAGING         # Staging datastore
DATA_STORE_ID_PROD            # Production datastore
PIPELINE_GCS_ROOT_STAGING     # gs://{project}-bob-vertex-agent-rag-staging
PIPELINE_GCS_ROOT_PROD        # gs://{project}-bob-vertex-agent-rag-prod
LOGS_BUCKET_NAME_STAGING      # {project}-bob-vertex-agent-logs-staging
LOGS_BUCKET_NAME_PROD         # {project}-bob-vertex-agent-logs-prod
PIPELINE_SA_EMAIL_STAGING     # bob-vertex-agent-rag@{project}.iam.gserviceaccount.com
PIPELINE_SA_EMAIL_PROD        # bob-vertex-agent-rag@{project}.iam.gserviceaccount.com
PIPELINE_NAME                 # data-ingestion-pipeline
PIPELINE_CRON_SCHEDULE        # 0 2 * * * (optional, for daily runs)
```

---

## GCP SERVICES REQUIRED

| Service | Purpose | Region |
|---------|---------|--------|
| Vertex AI Agent Engine | Agent hosting | us-central1 |
| Vertex AI Search | RAG knowledge | us |
| Vertex AI Rank | Document re-ranking | global |
| Cloud Functions | Slack webhook | us-central1 |
| Vertex AI Pipelines | Data ingestion | us-central1 |
| Cloud Logging | Centralized logs | global |
| Cloud Trace | Distributed tracing | global |
| Cloud Storage | RAG docs & artifacts | us |
| BigQuery | Data source (future) | us |
| Secret Manager | Slack tokens | global |

---

## AGENT DECISION TREE

```
USER ASKS BOB...

1. Simple greeting? 
   → Answer directly (no tools)

2. Need knowledge/facts?
   → Use retrieve_docs (RAG)
   → Query Vertex AI Search
   → Re-rank results
   → Return to user

3. Need specialized work?
   → route_to_agent {research|code|data|slack}
   → IAM2 specialist handles
   → Return results

4. Need cross-domain info?
   → coordinate_with_peer_iam1
   → Send A2A Protocol request
   → Wait 30 seconds max
   → Merge response

5. Complex multi-step task?
   → Orchestrate multiple agents
   → Combine results
   → Synthesize final answer
```

---

## SLACK INTEGRATION FLOW

```
@Bob: What's the API documentation?
  │
  ├─ SLACK EVENT WEBHOOK (Cloud Function)
  │  ├─ Slack sends HTTP POST
  │  ├─ Function deduplicates (prevent retries)
  │  └─ Returns HTTP 200 immediately
  │
  ├─ BACKGROUND THREAD (processing)
  │  ├─ Query Agent Engine (blocking call)
  │  ├─ Get Slack token from Secret Manager
  │  └─ Post response to channel
  │
  └─ RESULT: @Bob responds with answer in thread
```

---

## RAG PIPELINE

```
1. SOURCE DATA (in Cloud Storage)
   └─ gs://{project}-bob-vertex-agent-rag/knowledge-base/

2. DATA INGESTION PIPELINE (Vertex AI Pipelines)
   ├─ Load documents from Cloud Storage
   ├─ Chunk into segments
   ├─ Generate embeddings (text-embedding-005)
   └─ Import into Vertex AI Search datastore

3. RETRIEVAL (retrieve_docs tool)
   ├─ User query
   ├─ Vertex AI Search returns ~10 documents
   ├─ Vertex AI Rank re-ranks → top 5
   └─ Formatted docs to LLM

4. LLM CONSUMPTION
   └─ Included as context in Gemini prompt
```

---

## TERRAFORM STRUCTURE

```
deployment/terraform/
├─ providers.tf           → GCP + GitHub + Random
├─ locals.tf              → Service list, project mapping
├─ apis.tf                → Enable Google Cloud APIs
├─ iam.tf                 → Service account permissions
├─ service_accounts.tf    → Create CICD + app + pipeline SAs
├─ storage.tf             → GCS buckets (artifacts, logs)
├─ github.tf              → GitHub secrets + WIF
├─ wif.tf                 → Workload Identity Federation setup
├─ log_sinks.tf           → Cloud Logging configuration
├─ variables.tf           → Variable definitions
├─ vars/env.tfvars        → Variable values
└─ dev/                   → Dev environment specifics
```

**Key Service Accounts:**
- `bob-vertex-agent-cicd-runner` - Runs deployments
- `bob-vertex-agent-app` - Runs agent (per project)
- `bob-vertex-agent-rag` - Runs data pipeline (per project)

---

## MODELS USED

| Component | Model | Purpose | Temperature |
|-----------|-------|---------|-------------|
| IAM1 (Root) | Gemini 2.5 Flash | Orchestration, reasoning | Default |
| IAM2 Research | Gemini 2.5 Flash | Deep analysis | Default |
| IAM2 Code | Gemini 2.0 Flash | Code generation | Default |
| IAM2 Data | Gemini 2.5 Flash | SQL, analytics | Default |
| IAM2 Slack | Gemini 2.0 Flash | Formatting | Default |
| Embeddings | text-embedding-005 | Document vectors | N/A |

---

## DEPENDENCIES (CRITICAL)

```
google-adk>=1.15.0          # Agent Development Kit
a2a-sdk~=0.3.9              # Agent2Agent Protocol
langchain~=0.3.24           # LLM orchestration
langchain-google-vertexai   # Vertex AI integration
google-cloud-aiplatform     # Vertex AI SDK + Agent Engine
opentelemetry-exporter-gcp-trace  # Cloud Trace
google-cloud-logging        # Cloud Logging
```

---

## TESTING STRATEGY

| Level | Tool | Scope | Trigger |
|-------|------|-------|---------|
| Unit | pytest | Individual functions | PR checks |
| Integration | pytest | Agent interactions | PR checks |
| Load | Locust | Performance (2 users, 30s) | Staging deploy |
| Code Quality | ruff + mypy | Linting + types | PR checks |
| Spelling | codespell | Typos | PR checks |

---

## DEPLOYMENT CHECKLIST

- [ ] Terraform variables configured (projects, regions)
- [ ] GCP APIs enabled
- [ ] Service accounts created with correct roles
- [ ] GitHub secrets configured (WIF, service account)
- [ ] GitHub variables configured (projects, regions, buckets)
- [ ] RAG knowledge base uploaded to Cloud Storage
- [ ] Data ingestion pipeline run successfully
- [ ] Agent deployed to staging
- [ ] Load test passed (staging)
- [ ] Manual approval configured (production)
- [ ] Slack app configured + token in Secret Manager
- [ ] Slack webhook deployed
- [ ] A2A peer URLs configured (if multi-IAM1)
- [ ] Production deployment approved + successful

---

## TROUBLESHOOTING

| Problem | Cause | Solution |
|---------|-------|----------|
| Agent not responding | Deployment failed | Check Cloud Build logs |
| RAG returns empty | Data not ingested | Run `make data-ingestion` |
| Slack no response | Webhook URL wrong | Update in Slack app settings |
| A2A timeout | Peer agent down | Check peer IAM1 deployment |
| Load test fails | Staging agent overloaded | Increase quota or wait |
| Auth error | Service account perms | Check IAM roles in Terraform |

---

## COSTS (ESTIMATE)

| Component | Cost Factor | Typical Cost |
|-----------|-------------|--------------|
| Agent Engine | Per request | $0.02-0.05 per request |
| Vertex AI Search | Per document + queries | $0.10-0.50 per 1K docs |
| Cloud Functions | Invocations + compute | $0.40 per 1M invocations |
| Cloud Logging | Per GB | $0.50 per GB |
| Cloud Storage | Per GB | $0.020 per GB |
| **Monthly (small)** | Estimated | **$50-150** |
| **Monthly (large)** | Estimated | **$500-2000** |

---

## PERFORMANCE TARGETS

- Agent response time: < 3 seconds (typical)
- RAG retrieval: < 1 second
- Slack integration: < 5 seconds (with background processing)
- Load test: 2 users × 30 seconds
- Data ingestion: Hourly cron (configurable)
- Uptime: 99.9% (GCP managed services)

---

## SECURITY CHECKLIST

- ✅ Service accounts follow principle of least privilege
- ✅ Slack tokens in Secret Manager (not in code)
- ✅ Workload Identity Federation for GitHub Actions (no static keys)
- ✅ Cloud Logging for audit trail
- ✅ Data isolated per client/project
- ✅ A2A authentication via API keys
- ✅ No hardcoded credentials

---

## BUSINESS MODEL SUMMARY

| Tier | Price (est.) | Includes |
|------|--------------|----------|
| IAM1 Basic | $500/mo | Conversational AI + RAG + Slack |
| +IAM2 Specialist | +$200/mo each | Task delegation to expert agents |
| Multi-IAM1 | +$300/mo coordination | Cross-domain A2A protocol |

**Revenue:** Per IAM1 deployment + per IAM2 + coordination fees

---

## KEY CONTACTS & RESOURCES

| Item | Location |
|------|----------|
| Architecture Docs | `claudes-docs/004-AT-ARCH-bob-vertex-system-analysis.md` |
| Deployment Guide | `DEPLOYMENT_GUIDE.md` |
| Makefile | `Makefile` |
| README | `README.md` |
| Terraform | `deployment/terraform/` |
| GitHub Workflows | `.github/workflows/` |

---

## NEXT STEPS

1. **Short-term:** Implement IAM2 tool actions (code execution, BigQuery, Slack API)
2. **Medium-term:** Add streaming RAG ingestion + persistent conversation history
3. **Long-term:** Multi-modal RAG + fine-tuning per client + advanced A2A coordination

---

**Version:** 2.0.1  
**Last Updated:** 2025-11-09  
**Maintained By:** Claude Code
