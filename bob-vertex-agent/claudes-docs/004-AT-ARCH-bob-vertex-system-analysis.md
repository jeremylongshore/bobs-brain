# Bob's Vertex Agent - Complete System Architecture Analysis

**Status:** ✅ Production-Ready Deployment  
**Last Updated:** 2025-11-09  
**System Version:** 2.0.1 (IAM1 Regional Manager)  
**Analyst:** Claude Code  

---

## EXECUTIVE SUMMARY

Bob's Vertex Agent is a **production-deployed hierarchical multi-agent system** built on Google Cloud's Vertex AI Agent Engine. It implements the **IAM1 (Intent Agent Manager Level 1)** regional manager architecture, enabling sovereign AI agents that can:

- **Orchestrate subordinate agents** (IAM2 specialists)
- **Coordinate with peer agents** (other IAM1s via A2A Protocol)
- **Ground decisions** in private knowledge bases (Vertex AI Search RAG)
- **Scale horizontally** across clients/departments

**Key Characteristics:**
- Language: Python 3.10+
- Framework: Google ADK 1.15.0+
- Platform: Vertex AI Agent Engine (managed)
- LLM: Gemini 2.5 Flash (IAM1) + Gemini 2.0 Flash (IAM2s)
- Knowledge: Vertex AI Search with custom embeddings
- Deployment: Terraform IaC across staging + production
- Slack Integration: Cloud Functions webhook

---

## 1. DEPLOYMENT ARCHITECTURE

### 1.1 High-Level Infrastructure

```
┌─────────────────────────────────────────────────────────────────┐
│                     GOOGLE CLOUD PLATFORM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          VERTEX AI AGENT ENGINE (Managed)                │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  IAM1 BOB ORCHESTRATOR (Root Agent)                │  │  │
│  │  │  - Gemini 2.5 Flash                                │  │  │
│  │  │  - Conversation + Orchestration                    │  │  │
│  │  │  - RAG retrieval (via retrieve_docs tool)          │  │  │
│  │  │  - Agent routing (via route_to_agent tool)         │  │  │
│  │  │  - A2A coordination (via coordinate_with_peer_iam1)│  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                          │                                │  │
│  │                ┌─────────┼─────────┬──────────┐           │  │
│  │                ▼         ▼         ▼          ▼           │  │
│  │  ┌──────────┐ ┌────────┐ ┌──────┐ ┌───────┐             │  │
│  │  │Research  │ │Code    │ │Data  │ │Slack  │  (IAM2s)    │  │
│  │  │Agent     │ │Agent   │ │Agent │ │Agent  │             │  │
│  │  │(IAM2)    │ │(IAM2)  │ │(IAM2)│ │(IAM2) │             │  │
│  │  └──────────┘ └────────┘ └──────┘ └───────┘             │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                     │
│        ┌─────────────────┼─────────────────┐                  │
│        ▼                 ▼                 ▼                  │
│   ┌─────────┐      ┌──────────┐      ┌──────────┐            │
│   │VERTEX AI│      │VERTEX AI │      │CLOUD     │            │
│   │SEARCH   │      │RANK      │      │FUNCTIONS│            │
│   │(RAG)    │      │(Re-rank) │      │(Slack)  │            │
│   │         │      │          │      │         │            │
│   └─────────┘      └──────────┘      └──────────┘            │
│        │                                      │               │
│        ▼                                      ▼               │
│   ┌─────────────────┐              ┌──────────────────────┐ │
│   │VERTEX AI SEARCH │              │SLACK WEBHOOK CONFIG  │ │
│   │DATA STORE       │              │FROM SECRET MANAGER   │ │
│   │(embeddings)     │              └──────────────────────┘ │
│   └─────────────────┘                                        │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         SUPPORTING SERVICES                              │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │ • BigQuery (Data source)                            │ │  │
│  │  │ • Cloud Storage (Artifacts, RAG source documents)   │ │  │
│  │  │ • Cloud Logging (Telemetry)                         │ │  │
│  │  │ • Cloud Trace (Distributed tracing)                 │ │  │
│  │  │ • Secret Manager (Slack tokens)                     │ │  │
│  │  │ • Vertex AI Pipelines (Data ingestion)              │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Deployment Tiers

**Tier 1: CICD Runner Project**
- Location: `var.cicd_runner_project_id`
- Purpose: Runs deployment pipelines via GitHub Actions
- Service Account: `bob-vertex-agent-cicd-runner`
- Roles: Cloud Build admin, service deployment, workload identity federation

**Tier 2: Staging Project**
- Location: `var.staging_project_id`
- Purpose: Pre-production testing and validation
- Data Store: `bob-vertex-agent-datastore-staging`
- Load Testing: Locust with 2 concurrent users for 30 seconds
- Artifacts Bucket: `{project_id}-bob-vertex-agent-rag-staging`

**Tier 3: Production Project**
- Location: `var.prod_project_id`
- Purpose: Live customer deployments
- Data Store: `bob-vertex-agent-datastore-prod`
- Artifacts Bucket: `{project_id}-bob-vertex-agent-rag-prod`

### 1.3 GCP APIs Enabled (Per Project)

```python
cicd_services = [
    "cloudbuild.googleapis.com",
    "discoveryengine.googleapis.com",    # Vertex AI Search
    "aiplatform.googleapis.com",          # Vertex AI + Agent Engine
    "serviceusage.googleapis.com",
    "bigquery.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudtrace.googleapis.com"
]

deploy_project_services = [
    "aiplatform.googleapis.com",
    "run.googleapis.com",                 # Cloud Run (Cloud Functions runtime)
    "discoveryengine.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "bigquery.googleapis.com",
    "serviceusage.googleapis.com",
    "logging.googleapis.com",
    "cloudtrace.googleapis.com"
]
```

---

## 2. AGENT ARCHITECTURE

### 2.1 Root Agent (IAM1 - Bob Orchestrator)

**Location:** `app/agent.py` (lines 211-218)

```python
root_agent = Agent(
    name="bob_orchestrator",
    model="gemini-2.5-flash",
    instruction=instruction,  # 200+ lines of role definition
    tools=[retrieve_docs, route_to_agent, coordinate_with_peer_iam1],
)
```

**Identity:**
- **Name:** Bob / IAM1 Regional Manager
- **Tier:** IAM1 (Regional Manager)
- **Sovereignty:** Within domain only
- **Reporting:** Sovereign (no higher authority)

**Capabilities:**

| Capability | Tool | Description |
|-----------|------|-------------|
| Knowledge Retrieval | `retrieve_docs` | Query Vertex AI Search, re-rank with Vertex AI Rank |
| Task Delegation | `route_to_agent` | Route to IAM2 specialists (research, code, data, slack) |
| Peer Coordination | `coordinate_with_peer_iam1` | A2A Protocol communication with peer IAM1s |
| Conversation | Native | Gemini 2.5 Flash conversational abilities |
| Decision Making | Native | Step-by-step routing logic per decision framework |

**Decision Framework (lines 189-194):**
```
1. Simple questions → Answer directly
2. Knowledge questions → Use retrieve_docs (RAG)
3. Cross-domain info → Coordinate_with_peer_iam1 (A2A)
4. Specialized tasks → Route_to_agent (to IAM2)
5. Multi-step tasks → Coordinate multiple agents
```

### 2.2 Sub-Agents (IAM2 Specialists)

**Location:** `app/sub_agents.py` (lines 63-210)

#### IAM2-Research (research_agent)
- **Model:** Gemini 2.5 Flash
- **Expertise:** Deep research, knowledge synthesis, multi-source gathering
- **Tools:** `retrieve_docs` (access knowledge base)
- **Deliverables:** Executive summary + evidence + citations + recommendations
- **Use Case:** "Research best practices for X", comparative analysis, documentation review

#### IAM2-Code (code_agent)
- **Model:** Gemini 2.0 Flash
- **Expertise:** Code generation, debugging, refactoring, best practices
- **Tools:** None yet (future: code execution)
- **Deliverables:** Clean code + usage examples + edge cases + testing recommendations
- **Use Case:** "Write function to do X", "Debug this error", code review

#### IAM2-Data (data_agent)
- **Model:** Gemini 2.5 Flash
- **Expertise:** SQL queries, data analysis, visualization, statistics
- **Tools:** None yet (future: BigQuery access)
- **Deliverables:** SQL query + results interpretation + insights + recommendations
- **Use Case:** "Query database for X", data insights, analytics reporting

#### IAM2-Slack (slack_agent)
- **Model:** Gemini 2.0 Flash
- **Expertise:** Slack formatting, channel management, workflow optimization
- **Tools:** None yet (future: Slack API)
- **Deliverables:** Formatted Slack message + alternative formats + reaction suggestions
- **Use Case:** "Format this for Slack", channel operations, user management

**Agent Registry (lines 213-219):**
```python
AGENT_REGISTRY = {
    "research": research_agent,
    "code": code_agent,
    "data": data_agent,
    "slack": slack_agent,
}
```

### 2.3 Agent2Agent (A2A) Framework

**Location:** `app/a2a_tools.py` (lines 24-178)

**Peer IAM1 Registry (lines 14-21):**
```python
PEER_IAM1_REGISTRY = {
    "engineering": os.getenv("IAM1_ENGINEERING_URL", ""),
    "sales": os.getenv("IAM1_SALES_URL", ""),
    "operations": os.getenv("IAM1_OPERATIONS_URL", ""),
    "marketing": os.getenv("IAM1_MARKETING_URL", ""),
    "finance": os.getenv("IAM1_FINANCE_URL", ""),
    "hr": os.getenv("IAM1_HR_URL", ""),
}
```

**A2A Protocol Version:** 0.3.0 (specified in pyproject.toml)

**Coordination Pattern:**
1. Validate domain (engineering, sales, ops, etc.)
2. Check if peer URL configured
3. Initialize A2A client with authentication
4. Create message with request text
5. Send via A2A Protocol (JSON-RPC 2.0)
6. Wait for completion (30-second timeout)
7. Extract response from artifacts

**Important:** IAM1 agents **coordinate** (share info) but **cannot command** peers. This maintains sovereignty.

---

## 3. KNOWLEDGE GROUNDING (RAG)

### 3.1 Retrieval Pipeline

**Location:** `app/retrievers.py` (lines 25-83)

**Retriever Configuration:**
```python
VertexAISearchRetriever(
    project_id=project_id,
    data_store_id=data_store_id,          # e.g., "bob-vertex-agent-datastore"
    location_id=data_store_region,         # e.g., "us"
    engine_data_type=1,                    # Unstructured data
    custom_embedding_ratio=0.5,            # 50% custom, 50% default embeddings
    custom_embedding=embedding,            # VertexAIEmbeddings (text-embedding-005)
    custom_embedding_field_path="embedding",
    max_documents=10,                      # Fetch 10 docs before re-rank
    beta=True,
)
```

**Embedding Model:** `text-embedding-005` (Vertex AI Embeddings)

**Compression/Re-ranking:**
```python
VertexAIRank(
    project_id=project_id,
    location_id="global",
    ranking_config="default_ranking_config",
    title_field="id",
    top_n=5,                               # Return top 5 after re-ranking
)
```

### 3.2 RAG Document Processing

**Location:** `app/agent.py` (lines 63-86)

```python
def retrieve_docs(query: str) -> str:
    """
    Retrieve relevant documents based on a query.
    
    1. Use retriever.invoke(query) to fetch docs from Vertex AI Search
    2. Re-rank with Vertex AI Rank for better relevance
    3. Format into consistent structure for LLM consumption
    """
    try:
        retrieved_docs = retriever.invoke(query)                    # Step 1
        ranked_docs = compressor.compress_documents(                # Step 2
            documents=retrieved_docs, query=query
        )
        formatted_docs = format_docs.format(docs=ranked_docs)       # Step 3
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"
    
    return formatted_docs
```

**Document Format Template** (`app/templates.py` lines 15-28):
```jinja2
## Context provided:
{% for doc in docs %}
<Document {{ loop.index0 }}>
{{ doc.page_content | safe }}
</Document {{ loop.index0 }}>
{% endfor %}
```

### 3.3 Data Ingestion Pipeline

**Location:** `data_ingestion/` directory

**Purpose:** Automate data loading → chunking → embedding → Vertex AI Search import

**Workflow:**
1. Load documents from Cloud Storage
2. Chunk into manageable segments
3. Generate embeddings (Vertex AI Embeddings)
4. Import into Vertex AI Search datastore
5. Optional: Schedule periodic runs

**Execution:**
```bash
make data-ingestion  # Runs submit_pipeline.py with environment config
```

**Configuration:**
- Project ID: `var.prod_project_id` / `var.staging_project_id`
- Region: `us-central1` (Agent Engine), `us` (Vertex AI Search)
- Data Store ID: `bob-vertex-agent-datastore-{staging|prod}`
- Service Account: `bob-vertex-agent-rag@{project_id}.iam.gserviceaccount.com`
- Pipeline Root: `gs://{project_id}-bob-vertex-agent-rag/`

---

## 4. SLACK INTEGRATION

### 4.1 Slack Webhook (Cloud Function)

**Location:** `slack-webhook/main.py` (lines 90-141)

**Deployment:** Cloud Functions (Python 3.12, Gen 2)
- **Trigger:** HTTP (publicly accessible for Slack webhook)
- **Region:** us-central1
- **Runtime:** Python 3.12

**Slack Event Flow:**

```
Slack User mentions @Bob
        │
        ▼
Slack sends HTTP POST to webhook URL
        │
        ├─► Handler validates Slack signature (implicit)
        │
        ├─► Deduplicates event (prevent retry loops)
        │
        ├─► Returns HTTP 200 immediately (acknowledgment)
        │
        └─► Background thread processes message
                    │
                    ├─► Query Agent Engine (reasoning engine)
                    │
                    ├─► Get Slack bot token from Secret Manager
                    │
                    └─► Post response to Slack channel
```

### 4.2 Key Implementation Details

**Event Deduplication** (lines 109-115):
```python
_slack_event_cache = {}  # Global in-memory cache

if event_id and event_id in _slack_event_cache:
    logger.info(f"Ignoring duplicate event: {event_id}")
    return ({"ok": True}, 200)

if event_id:
    _slack_event_cache[event_id] = True
```

**Immediate HTTP 200 Response** (lines 132-141):
```python
# Process message in background thread to return HTTP 200 immediately
thread = threading.Thread(
    target=_process_slack_message,
    args=(text, channel, user, event_id),
    daemon=True
)
thread.start()

# Return HTTP 200 immediately to acknowledge receipt
return ({"ok": True}, 200)
```

**Agent Engine Query** (lines 45-59):
```python
from vertexai.preview import reasoning_engines

AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"

def query_agent_engine(query):
    remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)
    response = remote_agent.query(input=query)
    return str(response)
```

### 4.3 Slack Secret Management

**Secret Retrieval** (lines 33-42):
```python
def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage:
slack_token = get_secret("slack-bot-token")
slack_client = WebClient(token=slack_token)
```

**Slack Configuration** (deployment workflow, lines 56-68):
```yaml
- name: Display Slack Configuration
  run: |
    echo "1. Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions"
    echo "2. Update Request URL to: ${{ steps.get-url.outputs.function_url }}"
    echo "3. Subscribe to bot events:"
    echo "   - message.channels"
    echo "   - message.im"
    echo "   - app_mention"
```

---

## 5. CI/CD PIPELINE

### 5.1 GitHub Actions Workflows

**Location:** `.github/workflows/`

#### 5.1.1 PR Checks (`pr_checks.yaml`)
- Trigger: Pull requests
- Actions: Code quality checks, tests
- Purpose: Validate changes before merge

#### 5.1.2 Deploy to Staging (`staging.yaml`)
- Trigger: Push to main (changes to app/, data_ingestion/, tests/, deployment/, uv.lock)
- Steps:
  1. Authenticate to GCP (Workload Identity Federation)
  2. Deploy data ingestion pipeline
  3. Install dependencies
  4. Export requirements
  5. Deploy to Vertex AI Agent Engine (staging)
  6. Fetch auth token
  7. Run Locust load test (2 users, 30 seconds)
  8. Export load test results to GCS
  9. **Trigger production workflow** (if successful)

#### 5.1.3 Deploy to Production (`deploy-to-prod.yaml`)
- Trigger: Manual `workflow_dispatch` or called from staging
- Environment: production (manual approval available)
- Steps:
  1. Checkout code
  2. Setup Python 3.12
  3. Authenticate to GCP
  4. Deploy data ingestion pipeline (production)
  5. Deploy to Vertex AI Agent Engine (production)
  6. Set production environment variables

#### 5.1.4 Deploy Slack Webhook (`deploy-slack-webhook.yml`)
- Trigger: Push to main (changes in slack-webhook/)
- Steps:
  1. Checkout code
  2. Authenticate to GCP
  3. Deploy Cloud Function (gen2, Python 3.12)
  4. Get function URL
  5. Display Slack configuration instructions

### 5.2 Deployment Authentication

**Method:** Workload Identity Federation (WIF)
```yaml
workload_identity_provider: 'projects/${{ vars.GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/${{ secrets.WIF_POOL_ID }}/providers/${{ secrets.WIF_PROVIDER_ID }}'
service_account: '${{ secrets.GCP_SERVICE_ACCOUNT }}'
```

**Service Account:** `bob-vertex-agent-cicd-runner`

**Required Roles:**
- `roles/aiplatform.admin` (Agent Engine deployment)
- `roles/run.developer` (Cloud Functions)
- `roles/storage.admin` (Artifacts/logs bucket)
- `roles/secretmanager.secretAccessor` (Slack tokens)
- `roles/iam.serviceAccountTokenCreator` (WIF)
- `roles/iam.serviceAccountUser` (Self-impersonation)

### 5.3 Environment Variables (GitHub Secrets/Vars)

**Required Secrets:**
- `WIF_POOL_ID` - Workload Identity Pool ID
- `WIF_PROVIDER_ID` - Workload Identity Provider ID
- `GCP_SERVICE_ACCOUNT` - CICD service account email

**Required Variables:**
- `GCP_PROJECT_NUMBER` - GCP project number
- `CICD_PROJECT_ID` - CICD runner project
- `STAGING_PROJECT_ID` - Staging deployment project
- `PROD_PROJECT_ID` - Production deployment project
- `REGION` - Deployment region (us-central1)
- `DATA_STORE_REGION` - Vertex AI Search region (us)
- `DATA_STORE_ID_STAGING` / `DATA_STORE_ID_PROD` - Search datastores
- `PIPELINE_GCS_ROOT_STAGING` / `PIPELINE_GCS_ROOT_PROD` - Pipeline roots
- `LOGS_BUCKET_NAME_STAGING` / `LOGS_BUCKET_NAME_PROD` - Logging buckets
- `PIPELINE_SA_EMAIL_STAGING` / `PIPELINE_SA_EMAIL_PROD` - Pipeline service accounts
- `PIPELINE_NAME` - Data ingestion pipeline name
- `PIPELINE_CRON_SCHEDULE` - Optional cron for data ingestion

---

## 6. INFRASTRUCTURE AS CODE (TERRAFORM)

### 6.1 Project Structure

```
deployment/terraform/
├── providers.tf          # Provider configuration (Google, GitHub, Random)
├── locals.tf             # Local variables (services, projects)
├── apis.tf               # API enablement
├── iam.tf                # IAM roles and permissions
├── service_accounts.tf   # Service account definitions
├── storage.tf            # GCS buckets
├── github.tf             # GitHub secrets + WIF setup
├── wif.tf                # Workload Identity Federation
├── log_sinks.tf          # Cloud Logging configuration
├── variables.tf          # Variable definitions
├── vars/                 # Variable value files
│   └── env.tfvars
└── dev/                  # Development environment config
    ├── main.tf
    └── ...
```

### 6.2 Service Accounts

**CICD Service Account** (`bob-vertex-agent-cicd-runner`)
- Project: CICD runner project
- Roles:
  - `roles/cloudbuild.admin` (run builds)
  - `roles/aiplatform.admin` (deploy agents)
  - `roles/storage.admin` (access artifacts)
  - `roles/secretmanager.secretAccessor` (Slack tokens)
  - `roles/iam.serviceAccountTokenCreator` (WIF token creation)
  - `roles/iam.serviceAccountUser` (self-impersonation)

**Application Service Account** (per project, e.g., `bob-vertex-agent-app`)
- Projects: Staging + Production
- Roles:
  - `roles/aiplatform.user` (run agent)
  - `roles/discoveryengine.viewer` (query Vertex AI Search)
  - `roles/bigquery.dataViewer` (read BigQuery)
  - `roles/logging.logWriter` (write logs)
  - `roles/cloudtrace.agent` (write traces)
  - `roles/secretmanager.secretAccessor` (Slack token)

**Pipeline Service Account** (per project, e.g., `bob-vertex-agent-rag`)
- Projects: Staging + Production
- Roles:
  - `roles/aiplatform.user` (run pipelines)
  - `roles/storage.admin` (read/write pipeline data)
  - `roles/discoveryengine.admin` (manage datastore)
  - `roles/compute.serviceAgent` (Vertex AI compute)

### 6.3 Storage Configuration

**Artifacts Bucket** (per project)
- Name: `{project_id}-bob-vertex-agent-rag`
- Purpose: Store RAG source documents, pipeline outputs
- Retention: Standard
- Access: Service account only

**Logs/Results Bucket** (per environment)
- Name: `{project_id}-bob-vertex-agent-logs-{staging|prod}`
- Purpose: Load test results, deployment logs
- Retention: 30 days (lifecycle policy)
- Access: CICD service account

### 6.4 API Services Enabled

See section 1.3 for complete list.

---

## 7. ENTRY POINTS & EXECUTION FLOW

### 7.1 Agent Engine Entry Point

**File:** `app/agent_engine_app.py` (lines 32-74)

```python
class AgentEngineApp(AdkApp):
    def set_up(self) -> None:
        """Set up logging and tracing for the agent engine app."""
        super().set_up()
        logging.basicConfig(level=logging.INFO)
        
        # Cloud Logging client
        logging_client = google_cloud_logging.Client()
        self.logger = logging_client.logger(__name__)
        
        # OpenTelemetry tracing to Cloud Trace
        provider = TracerProvider()
        processor = export.BatchSpanProcessor(
            CloudTraceLoggingSpanExporter(
                project_id=os.environ.get("GOOGLE_CLOUD_PROJECT")
            )
        )
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

    def register_feedback(self, feedback: dict[str, Any]) -> None:
        """Collect and log feedback."""
        feedback_obj = Feedback.model_validate(feedback)
        self.logger.log_struct(feedback_obj.model_dump(), severity="INFO")

    def register_operations(self) -> dict[str, list[str]]:
        """Registers operations including feedback."""
        operations = super().register_operations()
        operations[""] = operations.get("", []) + ["register_feedback"]
        return operations

# Initialize and expose for Agent Engine
agent_engine = AgentEngineApp(
    app=adk_app,                           # ADK App from agent.py
    artifact_service_builder=artifact_service_builder,
)
```

**Deployment Target:** `--entrypoint-object=agent_engine`

### 7.2 Local Development Entry Point

**Command:** `make playground`

```bash
uv run adk web . --port 8501 --reload_agents
```

Starts a web interface at `http://localhost:8501` for interactive testing.

### 7.3 Slack Webhook Entry Point

**File:** `slack-webhook/main.py` (lines 90-141)

```python
@functions_framework.http
def slack_events(request):
    """Cloud Function entry point for Slack events"""
    # Handles: url_verification, message, app_mention
    # Returns HTTP 200 immediately
    # Processes message in background thread
```

**Deployment Target:** Cloud Functions with `--entry-point=slack_events`

---

## 8. TECHNOLOGY STACK

### 8.1 Core Dependencies

**Framework & Agent Development:**
- `google-adk>=1.15.0,<2.0.0` - Agent Development Kit
- `a2a-sdk~=0.3.9` - Agent2Agent Protocol

**Language Models & AI:**
- `langchain~=0.3.24` - LLM orchestration
- `langchain-core~=0.3.55` - Core abstractions
- `langchain-google-vertexai~=2.0.7` - Vertex AI integration
- `langchain-google-community[vertexaisearch]~=2.0.7` - Vertex AI Search

**Observability:**
- `opentelemetry-exporter-gcp-trace>=1.9.0,<2.0.0` - Cloud Trace export
- `google-cloud-logging>=3.12.0,<4.0.0` - Cloud Logging
- `google-cloud-aiplatform[evaluation,agent-engines]>=1.118.0,<2.0.0` - Vertex AI SDK

**Utilities:**
- `Jinja2~=3.1.6` - Template rendering
- `nest-asyncio>=1.6.0,<2.0.0` - Async support
- `protobuf>=6.31.1,<7.0.0` - Protocol buffers

### 8.2 Development/Testing Dependencies

- `pytest>=8.3.4,<9.0.0` - Testing framework
- `pytest-asyncio>=0.23.8,<1.0.0` - Async test support
- `ruff>=0.4.6,<1.0.0` - Code linting/formatting
- `mypy>=1.15.0,<2.0.0` - Type checking
- `codespell>=2.2.0,<3.0.0` - Spell checking

### 8.3 Deployment Tools

- `uv==0.8.13` - Python package manager
- `terraform>=1.0.0` - Infrastructure as Code
- `gcloud` - Google Cloud SDK
- `locust>=2.31.1` - Load testing (staging)

---

## 9. BUSINESS MODEL (IAM1 ARCHITECTURE)

### 9.1 Product Tiers

**Tier 1: IAM1 Basic - Regional Manager**
- Standalone conversational AI
- RAG knowledge grounding (Vertex AI Search)
- Slack integration
- Client-specific knowledge base
- Context management
- Price: $X/month per deployment
- Use Case: Single department/business unit AI assistant

**Tier 2: IAM1 + IAM2 Team - Managed Specialists**
- Everything in IAM1 Basic +
- IAM2 specialists (Research, Code, Data)
- Task delegation and routing
- Team coordination and quality control
- Price: IAM1 $X + IAM2 $200/month each
- Use Case: Department needs specialized AI capabilities

**Tier 3: Multi-IAM1 Enterprise - Regional Coordination**
- Multiple IAM1 deployments
- Agent-to-Agent (A2A) communication
- Cross-regional coordination
- Each IAM1 can have IAM2 teams
- Enterprise observability
- Price: Per IAM1 + per IAM2 + coordination fees
- Use Case: Multi-department/multi-location enterprise

### 9.2 Deployment Scenarios

**Scenario 1: Single Client, Single Department**
- 1 GCP project per client
- 1 IAM1 deployment
- Client-isolated knowledge base
- Revenue: IAM1 subscription

**Scenario 2: Single Client, Multiple Departments**
- 3 GCP projects (Sales, Eng, Support) OR 1 project with multiple agents
- Multiple IAM1 deployments
- A2A coordination between departments
- Revenue: 3x IAM1 subscriptions

**Scenario 3: IAM1 + IAM2 Team**
- 1 IAM1 + multiple IAM2 specialists
- Task routing from IAM1 → IAM2s
- Revenue: IAM1 + (N x IAM2)

### 9.3 Key Differentiators

1. **Sovereignty:** Each IAM1 is sovereign in its domain; peer IAM1s coordinate but cannot command
2. **Isolation:** Complete data isolation per client/department
3. **Scalability:** Deploy horizontally (more IAM1s) or vertically (more IAM2s)
4. **Coordination:** A2A Protocol enables enterprise-wide collaboration
5. **Grounding:** Private knowledge bases prevent data leakage between clients

---

## 10. CONFIGURATION & ENVIRONMENT

### 10.1 Required Environment Variables (Deployed)

**Agent Engine Deployment:**
```bash
GOOGLE_CLOUD_PROJECT="{project_id}"
GOOGLE_CLOUD_LOCATION="global"
GOOGLE_GENAI_USE_VERTEXAI="True"

DATA_STORE_REGION="us"                    # Vertex AI Search region
DATA_STORE_ID="bob-vertex-agent-datastore-{staging|prod}"

ARTIFACTS_BUCKET_NAME="{project_id}-bob-vertex-agent-rag"

COMMIT_SHA="{github.sha}"                 # For versioning

GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY="true"
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="true"
```

**A2A Peer Configuration (Optional):**
```bash
IAM1_ENGINEERING_URL="https://..."       # For A2A coordination
IAM1_SALES_URL="https://..."
IAM1_OPERATIONS_URL="https://..."
IAM1_MARKETING_URL="https://..."
IAM1_FINANCE_URL="https://..."
IAM1_HR_URL="https://..."

IAM1_A2A_API_KEY="{api_key}"              # For A2A authentication
```

**Slack Webhook:**
```bash
PROJECT_ID="{project_id}"
```

### 10.2 Makefile Commands

```makefile
install                  # Install dependencies (uv sync)
playground             # Start local dev web interface
deploy                 # Deploy to Vertex AI Agent Engine
backend                # Alias for 'deploy'
setup-dev-env          # Create dev infrastructure (Terraform)
data-ingestion         # Run RAG data ingestion pipeline
test                   # Run pytest suite
lint                   # Run code quality checks
register-gemini-enterprise  # Register agent to Gemini Enterprise
```

---

## 11. TESTING & QUALITY ASSURANCE

### 11.1 Test Structure

```
tests/
├── unit/
│   └── test_dummy.py
├── integration/
│   ├── test_agent.py
│   └── test_agent_engine_app.py
└── load_test/
    ├── README.md
    └── load_test.py
```

### 11.2 Load Testing

**Tool:** Locust
**Execution:** Staging deployment via GitHub Actions

**Configuration:**
```bash
locust -f tests/load_test/load_test.py \
  --headless \
  -t 30s \              # 30 seconds duration
  -u 2 \                # 2 concurrent users
  -r 0.5 \              # 0.5 spawn rate
  --csv=results \       # CSV export
  --html=report.html    # HTML report
```

**Results Export:**
```bash
gcloud storage cp --recursive tests/load_test/.results \
  gs://{LOGS_BUCKET}/load-test-results/results-${TIMESTAMP}
```

### 11.3 Code Quality Checks

**Linting & Formatting:**
- `ruff check .` - Linting
- `ruff format .` - Code formatting
- `codespell` - Spell checking

**Type Checking:**
- `mypy .` - Static type analysis

---

## 12. MONITORING & OBSERVABILITY

### 12.1 Logging

**Implementation:** Cloud Logging
```python
logging_client = google_cloud_logging.Client()
self.logger = logging_client.logger(__name__)
```

**Feedback Registration:**
```python
def register_feedback(self, feedback: dict[str, Any]) -> None:
    feedback_obj = Feedback.model_validate(feedback)
    self.logger.log_struct(feedback_obj.model_dump(), severity="INFO")
```

### 12.2 Distributed Tracing

**Implementation:** OpenTelemetry → Cloud Trace
```python
provider = TracerProvider()
processor = export.BatchSpanProcessor(
    CloudTraceLoggingSpanExporter(project_id=project_id)
)
provider.add_span_processor(processor)
```

**Configuration:**
- `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true`
- `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`

### 12.3 Metrics

- Agent response time (latency)
- Task delegation success rate
- RAG retrieval quality (document relevance)
- A2A coordination success rate
- Slack webhook processing time
- Load test results (RPS, response times, errors)

---

## 13. KNOWN LIMITATIONS & FUTURE ENHANCEMENTS

### 13.1 Current Limitations

1. **IAM2 Tool Access:**
   - Code Agent: No code execution yet
   - Data Agent: No BigQuery access yet
   - Slack Agent: No Slack API integration yet

2. **A2A Scalability:**
   - 6 peer domains configured (extensible)
   - 30-second timeout per request
   - No request queuing/priority

3. **RAG Storage:**
   - Currently documents in Cloud Storage
   - No streaming ingestion
   - Manual data upload required

4. **Slack Integration:**
   - In-memory event deduplication (lost on restart)
   - No persistent conversation history with Slack

### 13.2 Future Enhancements

1. **Add tool implementations:**
   - Code Agent: Add code_executor tool
   - Data Agent: Add bigquery_query tool
   - Slack Agent: Add slack_api tool

2. **Advanced RAG:**
   - Multi-modal document support
   - Streaming document ingestion
   - Real-time knowledge base updates

3. **A2A Protocol:**
   - Request queuing
   - Priority-based routing
   - Multi-hop A2A coordination

4. **Persistence:**
   - Firestore for conversation history
   - Vector database for embedding cache
   - Redis for event deduplication

5. **Enterprise Features:**
   - Custom fine-tuning per client
   - White-labeling support
   - SLA monitoring & alerting

---

## 14. DEPLOYMENT CHECKLIST

### For New IAM1 Deployment:

- [ ] Create GCP project: `{client}-{domain}-iam1`
- [ ] Enable billing
- [ ] Configure Terraform variables (projects, regions, etc.)
- [ ] Deploy Terraform: `make setup-dev-env`
- [ ] Upload client knowledge base to Cloud Storage
- [ ] Run data ingestion pipeline: `make data-ingestion`
- [ ] Deploy IAM1: `make deploy`
- [ ] Configure Slack workspace
- [ ] Configure Slack secrets in Secret Manager
- [ ] Deploy Slack webhook: Push to main (slack-webhook/)
- [ ] Test basic chat functionality
- [ ] Test knowledge retrieval (RAG)
- [ ] (Optional) Configure A2A peer URLs
- [ ] (Optional) Deploy IAM2 specialists
- [ ] Enable production approval in GitHub environment settings
- [ ] Test end-to-end in staging
- [ ] Trigger production deployment

---

## 15. QUICK REFERENCE

### File Locations

| Component | File | Lines |
|-----------|------|-------|
| Root Agent | app/agent.py | 211-218 |
| Sub-Agents | app/sub_agents.py | 63-210 |
| A2A Protocol | app/a2a_tools.py | 24-178 |
| RAG Retriever | app/retrievers.py | 25-83 |
| Agent Engine Entry | app/agent_engine_app.py | 32-74 |
| Slack Webhook | slack-webhook/main.py | 90-141 |
| Deployment | app/app_utils/deploy.py | - |
| IAM1 Config | app/iam1_config.py | 1-127 |

### Key Models

| Model | Purpose | Tier |
|-------|---------|------|
| Gemini 2.5 Flash | Root agent (IAM1) | Primary |
| Gemini 2.5 Flash | Research agent (IAM2) | Specialist |
| Gemini 2.0 Flash | Code agent (IAM2) | Specialist |
| Gemini 2.5 Flash | Data agent (IAM2) | Specialist |
| Gemini 2.0 Flash | Slack agent (IAM2) | Specialist |
| text-embedding-005 | Document embeddings (RAG) | Utility |

### Key APIs

| API | Purpose |
|-----|---------|
| Vertex AI Agent Engine | Agent hosting |
| Vertex AI Search | RAG knowledge retrieval |
| Vertex AI Rank | Document re-ranking |
| Cloud Functions | Slack webhook |
| Vertex AI Pipelines | Data ingestion orchestration |
| Cloud Trace | Distributed tracing |
| Cloud Logging | Centralized logging |
| Cloud Run | Container runtime (Cloud Functions gen2) |

---

## APPENDIX A: Architecture Decision Records

### Decision 1: Gemini 2.5 Flash for Root Agent
- **Rationale:** Best balance of performance, cost, and reasoning capability
- **Trade-offs:** Slightly higher latency than 2.0 Flash, but better instruction-following
- **Reversible:** Yes, model can be changed in agent.py line 213

### Decision 2: A2A Protocol vs Direct Integration
- **Rationale:** Enables peer coordination without coupling; maintains sovereignty
- **Trade-offs:** Additional HTTP overhead, 30-second timeout
- **Alternative:** Could use pub/sub for async coordination

### Decision 3: Vertex AI Search vs Custom Vector DB
- **Rationale:** Fully managed, built-in re-ranking, multi-modal support
- **Trade-offs:** Less control, potential cost at scale
- **Alternative:** Could use Weaviate, Pinecone, or Milvus

### Decision 4: Cloud Functions for Slack Integration
- **Rationale:** Serverless, minimal ops overhead, fast cold start
- **Trade-offs:** Limited execution time (~15 minutes), requires background thread
- **Alternative:** Cloud Run for longer-running tasks

---

**End of Analysis**

Generated: 2025-11-09  
System Version Analyzed: 2.0.1  
Analyzer: Claude Code  
