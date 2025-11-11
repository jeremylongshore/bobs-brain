# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**BrightStream** is a positive news platform built on Google Cloud's Agent Development Kit (ADK), featuring 11 AI agents that collaborate to aggregate, score, generate, and publish uplifting news content daily.

**Location:** `/home/jeremy/000-projects/iams/iamnews/brightstream/`
**GCP Project:** `brightstream-news`
**Region:** `us-central1`
**Status:** ⚠️ Infrastructure deployed, ADK compliance fixes in progress

## Architecture Hierarchy

BrightStream operates within a three-tier architecture:

```
iams/                    # Tier 1: All agent systems (parent directory)
└── iamnews/             # Tier 2: News agent TEMPLATE (reusable)
    └── brightstream/    # Tier 3: BrightStream INSTANCE (this project)
```

**Critical Understanding:** BrightStream is an INSTANCE of the iamNews template. Generic patterns belong in `../templates/`, BrightStream-specific customizations stay here. See `ARCHITECTURE-CLARITY.md` for complete explanation.

## Multi-Agent System Design

BrightStream uses 11 specialized agents in a sequential pipeline with parallel media generation:

**Sequential Pipeline:**
- **Agent 0** (Root Orchestrator) - Coordinates entire workflow, always-on
- **Agent 1** (News Aggregator) - Fetches 20-30 stories from RSS feeds
- **Agent 2** (Story Scorer) - Multi-agent debate scoring (positivity-weighted)
- **Agent 3** (Content Orchestrator) - Generates 500+ word article

**Parallel Media Generation:**
- **Agent 4** (Lyria Audio) - Audio narration (DISABLED for simplicity)
- **Agent 5** (Imagen Image) - Hero image ($0.02/image)
- **Agent 6** (Veo Video) - Video content (DISABLED - saves $1,500/month)

**Post-Processing:**
- **Agent 7** (QA Verification) - 4-layer anti-hallucination verification
- **Agent 8** (Publishing) - Firebase/X/Email distribution + Google Sheets logging
- **Agent 9** (Analytics) - Performance tracking
- **Agent 10** (Evaluation) - Continuous improvement

**State Management:** All workflow state stored in Firestore (agents are stateless). Agent 0 manages recovery with exponential backoff.

### Data Flow Through the System

```
User Trigger (Manual/Scheduled/API)
    ↓
Agent 0: Load session context → Generate workflowId
    ↓
Agent 1: Fetch RSS feeds → Return 20-30 candidate stories
    ↓
Agent 2: Score each story (relevance 25%, quality 25%, positivity 35%, timeliness 15%)
    ↓
    Select top story (score > 75)
    ↓
Agent 3: Generate article (title + 500+ words)
    ↓
Agent 5: Generate hero image (Imagen 3)
    ↓
Agent 7: QA verification (4 layers: factual, tone, format, hallucination check)
    ↓
    If approved → Continue
    If rejected → Retry Agent 3 OR terminate
    ↓
Agent 0: Aggregate all data into 18-column sheet format
    ↓
Agent 8: Publish to Firebase + X/Twitter + Email + Google Sheets
    ↓
Agent 9: Log analytics (views, engagement, scores)
    ↓
Agent 10: Evaluate performance → Improve future runs
```

**Key Data Points (18 columns in Google Sheets):**
- Workflow metadata (workflowId, timestamp, status)
- Story info (sourceUrl, originalTitle, selectedStory)
- Generated content (generatedTitle, articleContent, imageUrl)
- Scores (relevanceScore, qualityScore, positivityScore, timelinessScore, overallScore)
- QA results (qaApproved, qaFeedback)
- Publishing (firebaseUrl, twitterUrl, emailsSent)

## Agent Quick Reference

| Agent | Name | Purpose | Resources | Port (Local) |
|-------|------|---------|-----------|--------------|
| **Agent 0** | Root Orchestrator | Coordinates entire workflow | 4 CPU, 4Gi RAM, always-on | 8080 |
| **Agent 1** | News Aggregator | Fetch 20-30 stories from RSS feeds | 2 CPU, 2Gi RAM | 8081 |
| **Agent 2** | Story Scorer | Multi-agent debate scoring (positivity 35%) | 4 CPU, 4Gi RAM | 8082 |
| **Agent 3** | Content Orchestrator | Generate 500+ word article | 4 CPU, 4Gi RAM | 8083 |
| **Agent 4** | Lyria Audio | Audio narration (DISABLED) | 2 CPU, 2Gi RAM | 8084 |
| **Agent 5** | Imagen Image | Hero image generation | 2 CPU, 2Gi RAM | 8085 |
| **Agent 6** | Veo Video | Video generation (DISABLED) | N/A | N/A |
| **Agent 7** | QA Verification | 4-layer anti-hallucination checks | 4 CPU, 4Gi RAM | 8087 |
| **Agent 8** | Publishing | Firebase/X/Email distribution + Google Sheets | 2 CPU, 2Gi RAM | 8088 |
| **Agent 9** | Analytics | Performance tracking | 1 CPU, 1Gi RAM | 8089 |
| **Agent 10** | Evaluation | Continuous improvement | 2 CPU, 2Gi RAM | 8090 |

## Important File Locations

**Agent Configurations:**
- `agents/agent_N_*.yaml` - ADK Agent Config YAMLs (10 agents)
- `tools/agent_N_tools.py` - Python tool implementations (10 files)
- `prompts/` - Agent prompt templates

**Infrastructure:**
- `agent_engine_app.py` - ADK app entry point for deployment
- `terraform.tfvars` - BrightStream GCP configuration
- `terraform/vertex-ai.tf` - Vertex AI infrastructure
- `dockerfiles/Dockerfile.agent-N` - Docker images for each agent
- `Makefile` - Build and deployment commands

**Configuration:**
- `requirements.txt` - Python dependencies (Google ADK 1.17.0)
- `GOOGLE_SHEETS_AUTH_SETUP.md` - Google Sheets API setup
- `.github/workflows/deploy-brightstream-vertex-genai.yml` - CI/CD pipeline

**Testing:**
- `test_rss_feeds.py` - Test all RSS feeds
- `test_updated_feeds.py` - Test specific feeds
- `find_replacement_feeds.py` - Find new RSS feeds

**Documentation:**
- `000-docs/` - BrightStream product documentation (8 files)
- `README.md` - Project overview
- `ARCHITECTURE-CLARITY.md` - Three-tier architecture explanation
- `IMPLEMENTATION-STATUS.md` - Current development status

## Common Development Commands

### Prerequisites & Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_CLOUD_PROJECT=brightstream-news
export GOOGLE_CLOUD_REGION=us-central1
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Authenticate with GCP
gcloud auth application-default login
gcloud config set project brightstream-news
```

### Infrastructure Setup (First Time)

```bash
# Set up GCP project and enable APIs
make setup-gcp          # Initialize project, create buckets, enable APIs

# Deploy infrastructure with Terraform (from parent directory)
cd /home/jeremy/000-projects/iams/iamnews/
terraform init
terraform plan -var-file="brightstream/terraform.tfvars"
terraform apply -var-file="brightstream/terraform.tfvars"
```

### Local Development & Testing

```bash
# Start all agents locally with Docker Compose
make docker-up          # Agents run on ports 8080-8090
make docker-logs        # View all agent logs
make docker-down        # Stop all agents

# ADK web playground for testing agent configs
make local-test         # Launch interactive agent testing UI
make local-run          # Run Agent 0 locally
```

### Build & Deploy

```bash
# Build Docker images for all agents
make build-all          # Build all 10 agent images
make build-agent-0      # Build specific agent (0-10)

# Push to Artifact Registry
make push-all           # Push all images
make push-agent-0       # Push specific agent

# Deploy to Vertex AI Agent Engine
make deploy-all         # Deploy all agents (5s delay between each)
make deploy-agent-0     # Deploy specific agent
```

**Important:** Always deploy Agent 0 last since it coordinates all other agents.

### Testing & Monitoring

```bash
# Test deployed agents
make test-agent-0       # Test root orchestrator with curl
make test-eval          # Run ADK evaluation suite

# Test individual components
python test_rss_feeds.py              # Test all RSS feeds
python test_updated_feeds.py          # Test specific feeds
python find_replacement_feeds.py      # Find new RSS feeds

# View production status
make status             # List deployed agents
make logs               # View Agent 0 Cloud Run logs
make clean              # Remove build artifacts

# Monitor specific agents
gcloud logging read "resource.labels.service_name=agent_1_news_aggregator" --limit=20 --project=brightstream-news
gcloud logging read "resource.labels.service_name=agent_2_story_scorer" --limit=20 --project=brightstream-news
```

## Critical Implementation Status

### ⚠️ ADK Compliance (CRITICAL)

**Current Score:** 2/10 - Not production ready

**Key Blockers:**
1. Agent Config YAMLs missing `$schema` field and ADK-compliant structure
2. Tools not wrapped with `FunctionTool` from `google.adk.tools`
3. Sub-agent routing not implemented in Agent 0
4. ParallelAgent wrapper missing for Agents 4-5
5. No confirmation policies for risky tools

**Reference:** `000-docs/002-TQ-AUDT-adk-vertex-compliance-audit.md` for complete audit

### ✅ What's Working

- GCP infrastructure fully deployed
- 10 agent YAML configs created (need schema fixes)
- 10 Python tool files implemented (need FunctionTool wrapping)
- Docker Compose for local multi-agent testing
- Comprehensive Makefile with all deployment commands

## Agent Configuration Pattern

Each agent requires two components:

**1. Agent Config YAML** (`agents/agent_N_name.yaml`):
```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/google/adk-python/refs/heads/main/src/google/adk/agents/config_schemas/AgentConfig.json
name: agent_N_name
agent_class: LlmAgent
model: gemini-2.0-flash
description: Brief agent purpose
instruction: |
  Detailed multi-line prompt with:
  - Role definition
  - Input/output specification
  - Constraints and guidelines

tools:
  - name: agent_N_tools

sub_agents:  # For Agent 0 only
  - config_path: ./agents/agent_1_name.yaml
```

**2. Python Tool File** (`tools/agent_N_tools.py`):
```python
from google.adk.tools import FunctionTool

async def tool_name(param: str) -> Dict[str, Any]:
    """Tool description for LLM."""
    # Implementation with type hints
    return {"status": "success", "data": {}}
```

## Technology Stack

**Infrastructure:**
- Google Cloud Platform (Vertex AI Agent Engine, Firestore, Cloud Storage, Cloud Run)
- Terraform 1.5+ (Infrastructure as Code)
- Docker + Docker Compose (containerization)

**AI Models:**
- Gemini 2.5 Flash (primary LLM, free tier: 15 RPM, 4,080 articles/month)
- Lyria (audio narration)
- Imagen 3 (image generation)

**Framework:**
- Google ADK (Agent Development Kit) - Python 3.12+
- Agent Engine deployment via `adk deploy agent_engine`

## Cost Budget: $168/month

| Component | Monthly Cost | Configuration |
|-----------|--------------|---------------|
| Agent 0 (always-on) | $33 | 4 CPU, 4Gi RAM, min=1, max=5 |
| Agents 1-10 (scale-to-zero) | $15 | Combined on-demand |
| Gemini 2.5 Flash | $0 | Free tier (15 RPM limit) |
| Lyria Audio | $60 | $0.02 × 100/day × 30 days |
| Imagen Images | $60 | $0.02 × 100/day × 30 days |

**Total:** $168/month (Agent 6 video disabled to save $1,500/month)

## Resource Allocation

- **Agent 0:** 4 CPU, 4Gi RAM, min=1, max=5 (always-on orchestrator)
- **Agents 1-3:** 2-4 CPU, 2-4Gi RAM, min=0, max=3 (sequential pipeline)
- **Agents 4-5:** 2 CPU, 2Gi RAM, min=0, max=5 (parallel media generation)
- **Agents 7-10:** 1-4 CPU, 1-4Gi RAM, min=0, max=2-3 (post-processing)

## Development Guidelines

### Agent Design Principles

1. **Stateless agents** - All workflow state in Firestore, not agent memory
2. **Idempotent tools** - Safe to retry any operation without side effects
3. **Timeout management** - All external calls have explicit timeouts
4. **Error recovery** - Exponential backoff with circuit breaker patterns
5. **Type hints required** - All functions must have complete type annotations
6. **Async by default** - Use `async/await` for all I/O operations

### Adding a New Tool

```bash
# 1. Define async function in tools/agent_N_tools.py
async def new_tool(param: str) -> Dict[str, Any]:
    """Tool description."""
    return {"status": "success"}

# 2. Wrap with FunctionTool
from google.adk.tools import FunctionTool
new_tool_wrapped = FunctionTool(new_tool)

# 3. Register in agents/agent_N_name.yaml
tools:
  - name: agent_N_tools

# 4. Test locally
make local-test

# 5. Deploy
make deploy-agent-N
```

## Security & Deployment

- **Secrets:** Use Google Secret Manager, never commit credentials
- **Authentication:** OAuth "controlling user" model for Agent 0 public endpoint
- **Rate limiting:** Respect Gemini free tier (15 RPM, 1,500 RPD)
- **Deployment order:** Deploy supporting agents first, Agent 0 last
- **Cost monitoring:** Check GCP billing dashboard weekly to stay within $168/month budget

## Key Documentation Files

**In This Directory:**
- `README.md` - BrightStream product overview and setup instructions
- `ARCHITECTURE-CLARITY.md` - Three-tier architecture explanation (TEMPLATE vs INSTANCE)
- `PROJECT-STRUCTURE-SCAFFOLD.md` - Recommended directory reorganization plan
- `000-docs/002-TQ-AUDT-adk-vertex-compliance-audit.md` - ADK compliance audit (critical reading)

**Parent Directory (iamNews Template):**
- `../README.md` - How to use iamNews template for new platforms
- `../TEMPLATE-SEPARATION-STRATEGY.md` - Migration strategy for extracting generic patterns
- `../ULTRATHINK-SUMMARY.md` - Quick architecture overview

## Template vs Instance Separation

**⚠️ Important:** BrightStream is currently in migration. Many files in this directory should move to `../templates/`:

**Move to Template (`../templates/`):**
- Generic agent YAML structure → `templates/agent-configs/*.yaml.template`
- Generic Python tools → `templates/agent-tools/*.py.template`
- Generic prompts → `templates/prompts/*.md.template`
- Generic Dockerfiles/Makefile → `templates/infrastructure/`

**Keep in BrightStream:**
- `terraform.tfvars` (BrightStream GCP project configuration)
- `customizations/` (positivity-focused scoring, branding)
- `000-docs/` (BrightStream product documentation only)

**Goal:** Enable creating new platforms (TechStream, BizStream) in 30 minutes vs 3 weeks by reusing templates.

## Deployment Methods

BrightStream supports two deployment approaches:

### Method 1: ADK Agent Engine Deployment (Primary)
**Use for:** Production deployment to Vertex AI Agent Engine with managed hosting

```bash
# Deploy using ADK CLI (recommended for production)
source .venv/bin/activate
adk deploy agent_engine \
  --project=brightstream-news \
  --region=us-central1 \
  --staging_bucket=gs://brightstream-news-agent-staging \
  --adk_app=agent_engine_app.py \
  agents/agent_0_root_orchestrator.yaml
```

**Benefits:** Managed hosting, auto-scaling, built-in monitoring

### Method 2: Docker + Makefile Deployment
**Use for:** Custom Cloud Run deployment or local testing

```bash
# Build and deploy using Makefile
make build-all          # Build Docker images
make push-all           # Push to Artifact Registry
make deploy-all         # Deploy to Vertex AI (uses adk deploy under the hood)
```

**Benefits:** More control over containerization, easier local testing

### Recommended Approach
1. Use `make` commands for building and testing locally
2. Use `adk deploy` directly for production deployment (cleaner, more reliable)
3. GitHub Actions for CI/CD (automatic on push to main)

## Troubleshooting

### Common Issues & Solutions

**Issue: `ImportError: cannot import name 'FunctionTool'`**
```bash
# Solution: Ensure google-adk is installed first
pip uninstall google-cloud-aiplatform google-adk
pip install google-adk==1.17.0
pip install -r requirements.txt
```

**Issue: ADK deployment fails with "schema validation error"**
```bash
# Solution: Check agent YAML has correct $schema field
# Line 1 of agent YAML must be:
# yaml-language-server: $schema=https://raw.githubusercontent.com/google/adk-python/refs/heads/main/src/google/adk/agents/config_schemas/AgentConfig.json
```

**Issue: `gcloud auth` errors during deployment**
```bash
# Solution: Re-authenticate and set project
gcloud auth application-default login
gcloud config set project brightstream-news
```

**Issue: Docker build fails with "permission denied"**
```bash
# Solution: Ensure Docker daemon is running and authenticate to Artifact Registry
sudo systemctl start docker
gcloud auth configure-docker us-central1-docker.pkg.dev
```

**Issue: RSS feed test failures**
```bash
# Solution: Test individual feeds to find broken ones
python test_updated_feeds.py
python find_replacement_feeds.py  # Find replacements for broken feeds
```

**Issue: Firestore permission denied**
```bash
# Solution: Check service account has Firestore permissions
gcloud projects add-iam-policy-binding brightstream-news \
  --member="serviceAccount:brightstream-vertex-sa@brightstream-news.iam.gserviceaccount.com" \
  --role="roles/datastore.user"
```

**Issue: Agent 0 deployed but sub-agents not found**
```bash
# Solution: Deploy all sub-agents BEFORE deploying Agent 0
make deploy-agent-1
make deploy-agent-2
# ... deploy agents 3-10 ...
make deploy-agent-0  # Deploy orchestrator last
```

**Issue: Local Docker Compose agents can't communicate**
```bash
# Solution: Ensure all agents are on same network
docker-compose down
docker-compose up -d
docker network inspect brightstream_default  # Verify network
```

## Current Priorities

1. **Fix ADK compliance issues** (agents/tools need schema updates and FunctionTool wrapping)
2. **Complete template extraction** (move generic patterns to `../templates/`)
3. **Local testing** (validate multi-agent workflow with Docker Compose)
4. **Production deployment** (after ADK compliance fixes)

## Vertex AI Generative AI Engine Deployment

### GitHub Actions Workflow
The project includes a comprehensive CI/CD pipeline for deploying to Vertex AI:
- `.github/workflows/deploy-brightstream-vertex-genai.yml` - Full deployment pipeline
- Builds Vertex AI-optimized containers for each agent
- Deploys to Vertex AI Model Registry and Endpoints
- Configures Vertex AI Search with generative features
- Sets up monitoring and alerting

### Key Deployment Commands
```bash
# Deploy to Vertex AI using GitHub Actions
git push origin main  # Triggers automatic deployment

# Manual deployment of specific agent
python scripts/vertex-ai/deploy_agent.py \
  --agent-id 0 \
  --project-id brightstream-news \
  --location us-central1

# Verify deployment
python scripts/vertex-ai/verify_deployment.py \
  --project-id brightstream-news \
  --location us-central1

# Deploy Terraform infrastructure
cd terraform
terraform apply -var-file="../brightstream/terraform.tfvars"
```

### Vertex AI Configuration Files
- `configs/vertex-ai/vertex-ai-config.yaml` - Complete Vertex AI configuration
- `terraform/vertex-ai.tf` - Terraform resources for Vertex AI
- `dockerfiles/Dockerfile.vertex-agent-*` - Vertex AI optimized containers

## External Resources

- **Google ADK:** https://github.com/google/adk-python
- **Vertex AI Agent Engine:** https://cloud.google.com/vertex-ai/docs/agents
- **Vertex AI Generative AI:** https://cloud.google.com/vertex-ai/generative-ai/docs
- **Gemini Free Tier:** https://ai.google.dev/pricing
- **ADK Agent Config Schema:** https://raw.githubusercontent.com/google/adk-python/refs/heads/main/src/google/adk/agents/config_schemas/AgentConfig.json

---

**Last Updated:** 2025-10-30 (Enhanced with troubleshooting, data flow diagram, and deployment clarifications)
**Status:** Infrastructure deployed, ADK compliance fixes in progress
**Next Action:** Fix ADK compliance issues, then deploy to Vertex AI Agent Engine
