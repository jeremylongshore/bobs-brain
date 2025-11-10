# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**PipelinePilot** is a B2B sales automation platform that orchestrates external data providers (Clay, Apollo, Clearbit, Crunchbase) through a Vertex AI Reasoning Engine deployed on Google Cloud Platform. It uses a serverless-first architecture with Firebase Functions Gen2 as the gateway and Vertex AI for AI-powered orchestration.

**Location:** `/home/jeremy/000-projects/iams/pipelinepilot/`
**Status:** Phase 1 Foundation Complete
**Type:** Agent System Implementation (Tier 3 in IAMS architecture)

## Architecture Overview

```
Firebase Functions Gen2 (Node 20 ESM)
       ↓
Vertex AI Reasoning Engine (Python ADK)
       ↓
External APIs (Clay, Apollo, Clearbit, Crunchbase)
       ↓
Firestore (Campaign logs & data)
```

### Key Components

1. **Firebase Functions** (`pipelinepilot-dashboard/functions/`) - Node 20 ESM serverless gateway
2. **Orchestrator Wrapper** (`src/orchestrator_wrapper.py`) - ADK-compliant sync wrapper with `query(**kwargs)` method
3. **Tool Functions** (`src/agents/tools.py`) - Async API integrations for external providers
4. **Terraform Templates** (`tf-pipeline/`, `tf-pipeline-multicloud/`) - Infrastructure as Code for GCP/AWS/Azure

### Critical Design Principles

1. **ADK Compliance** - Reasoning Engine requires synchronous `query(**kwargs)` method
2. **ESM Modules** - Firebase Functions Gen2 with `"type": "module"` in package.json
3. **BYO Keys** - Users supply their own API keys via Secret Manager (per-campaign isolation)
4. **Multi-Cloud Ready** - Terraform templates support GCP, AWS, and Azure deployments

## Common Development Commands

### Node.js Development

```bash
# ARV validation (Agent Runtime Validation)
npm run arv                  # Validates agent YAML configs and JSON schemas

# Type checking
npm run typecheck            # TypeScript compilation check (no emit)

# Build
npm run build                # Compile TypeScript to JavaScript

# Demo
npm run demo                 # Run NewsFeed demo (generates MD/HTML output)
```

### Python Development

```bash
# Create virtual environment with pinned dependencies
python3 -m venv venv-deploy
source venv-deploy/bin/activate
pip install cloudpickle==3.1.1  # Pinned for Vertex AI Reasoning Engine
pip install -e .

# Deploy orchestrator to Vertex AI
python src/deploy_with_wrapper.py

# Local smoke test (no deployment)
python scripts/smoke_orchestrator.py
```

### Firebase Functions

```bash
# Navigate to functions directory
cd pipelinepilot-dashboard/functions/

# Install dependencies
npm install

# Build TypeScript
npm run build

# Deploy function
firebase deploy --only functions:startCampaign

# View logs
firebase functions:log
```

### Terraform Deployment

```bash
# GCP deployment
cd tf-pipeline/
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your GCP project details
terraform init
terraform plan
terraform apply

# Multi-cloud comparison
cd tf-pipeline-multicloud/
cat QUICKSTART.md  # Decision tree for cloud provider selection
cat README.md      # Service mapping and cost comparison
```

### Infrastructure Setup

```bash
# Enable Firestore and required APIs
npm run enable:firestore
# OR
./scripts/enable_firestore.sh

# Deploy all agents
npm run deploy:agents
# OR
./scripts/deploy_agents.sh
```

### Testing & Validation

```bash
# Smoke test deployed Firebase Function
export PROJECT_ID="pipelinepilot-prod"
export LOCATION="us-central1"
./scripts/smoke.sh

# Mock mode (allows missing API keys)
export SMOKE_ALLOW_MISSING_KEYS=1
./scripts/smoke.sh

# Validate YAML configs
yamllint agents/*.yaml

# Check JSON schemas
jq . newsfeed-demo/news_story.schema.json
jq . agents/_schemas/AgentConfig.schema.json
```

## Architecture Deep Dive

### 1. Firebase Functions Gateway (ESM)

**Location:** `pipelinepilot-dashboard/functions/src/index.ts`

**Critical Pattern:**
```typescript
import { initializeApp, applicationDefault } from "firebase-admin/app";
initializeApp({ credential: applicationDefault() });  // Must include credential
```

**Why ESM?**
- Firebase Functions Gen2 + Node 20 + ESM is the industry standard
- `"type": "module"` in package.json enables ESM
- `tsconfig.json` uses `"module": "NodeNext"` for proper ESM compilation

**Common Pitfall:** `initializeApp is not a function`
- **Cause:** Missing `applicationDefault()` credential in ESM mode
- **Fix:** Always import and pass `applicationDefault()` explicitly

### 2. Orchestrator Wrapper (ADK Compliance)

**Location:** `src/orchestrator_wrapper.py`

**Required Pattern:**
```python
class OrchestratorWrapper:
    def query(self, **kwargs) -> Dict[str, Any]:
        # MUST be synchronous
        # MUST return JSON-serializable dict
        # Wraps async tools with asyncio.run()
        pass
```

**Why This Pattern?**
- Vertex AI Agent Engine requires `query(**kwargs)` method
- Must be synchronous (no async/await)
- Async tools wrapped with `asyncio.run()` for compatibility

**Deployment:**
```bash
python src/deploy_with_wrapper.py  # Deploys OrchestratorWrapper class
```

### 3. Tool Functions (Async API Integration)

**Location:** `src/agents/tools.py`

**Available Tools:**
- `clay_lookup(domain)` - Company data from Clay API
- `apollo_people(query)` - Contact search via Apollo.io
- `clearbit_enrich(email)` - Contact enrichment from Clearbit
- `crunchbase_company(name)` - Funding data from Crunchbase

**Key Features:**
- All tools are async functions
- Secrets fetched from Google Secret Manager
- Error handling returns `{"error": true, "message": "..."}` instead of raising exceptions
- Timeout defaults to 30 seconds

### 4. Secret Management

**Pattern:** Per-workspace isolation

```bash
# Store workspace-specific API keys
echo -n "sk_clay_..." | gcloud secrets create workspace-123-clay-key --data-file=-
echo -n "..." | gcloud secrets create workspace-123-apollo-key --data-file=-
echo -n "..." | gcloud secrets create workspace-123-clearbit-key --data-file=-
echo -n "..." | gcloud secrets create workspace-123-crunchbase-key --data-file=-

# Verify secret exists
gcloud secrets list | grep workspace-123
gcloud secrets versions access latest --secret="workspace-123-clay-key"
```

**Security Model:**
- ✅ API keys never in source code
- ✅ Per-workspace isolation (no cross-contamination)
- ✅ User-provided keys (BYO Keys policy)
- ❌ Never store keys in Firestore or plaintext

## IAMS Tier Context

PipelinePilot is a **Tier 3** implementation in the IAMS architecture:

- **Tier 1:** `/home/jeremy/000-projects/iams/` - General agent patterns
- **Tier 2:** Domain templates (e.g., `iamnews/`, `iamsdr/`)
- **Tier 3:** `pipelinepilot/` ← YOU ARE HERE

**Documentation Placement:**
- General agent patterns → `iams/000-docs/`
- Domain-specific patterns → `iam[domain]/000-docs/`
- PipelinePilot-specific → `pipelinepilot/000-docs/`

## File Organization

```
pipelinepilot/
├── 000-docs/                        # Documentation (v2.0 filing system)
│   ├── 6767-PP-SOP-*.md            # ESM/ADK standard procedures
│   └── 9999-DR-EXEC-*.md           # Executive summaries
│
├── pipelinepilot-dashboard/         # Firebase Frontend + Functions
│   └── functions/                   # Gen2 Functions (Node 20 ESM)
│       ├── src/index.ts            # startCampaign function
│       ├── package.json            # "type": "module" for ESM
│       └── tsconfig.json           # NodeNext module system
│
├── src/                             # Python Orchestrator
│   ├── agents/                     # Agent tools (async)
│   │   └── tools.py                # clay_lookup, apollo_people, etc.
│   ├── orchestrator_wrapper.py     # ADK wrapper (sync query method)
│   └── deploy_with_wrapper.py      # Reasoning Engine deployment
│
├── tf-pipeline/                     # GCP Terraform
│   ├── main.tf                     # Firebase, Vertex AI, Firestore
│   ├── variables.tf                # Configurable inputs
│   └── outputs.tf                  # Deployment outputs
│
├── tf-pipeline-multicloud/          # Multi-Cloud Templates
│   ├── README.md                   # Service mapping & cost comparison
│   ├── QUICKSTART.md               # Quick decision tree
│   ├── aws/                        # AWS templates (S3, Lambda, Bedrock)
│   ├── azure/                      # Azure templates
│   └── gcp/                        # GCP reference implementation
│
├── scripts/                         # Utilities
│   ├── smoke.sh                    # End-to-end smoke test
│   └── enable_firestore.sh         # GCP setup script
│
├── .github/workflows/               # CI/CD
│   ├── arv-gate.yml                # ARV validation gate
│   ├── adk-guard.yml               # ADK compliance check
│   └── policy.yml                  # Policy enforcement
│
├── package.json                     # Node dependencies + scripts
├── pyproject.toml                   # Python dependencies
└── tsconfig.json                    # TypeScript configuration
```

## Troubleshooting

### Firebase Functions Issues

**Error:** `initializeApp is not a function`
```bash
# Check package.json has "type": "module"
grep '"type"' pipelinepilot-dashboard/functions/package.json

# Verify ESM import pattern in index.ts
grep -A 2 'initializeApp' pipelinepilot-dashboard/functions/src/index.ts
# Should see: initializeApp({ credential: applicationDefault() })
```

**Error:** `setGlobalOptions is not exported from 'firebase-functions/v2'`
```typescript
// WRONG
import { setGlobalOptions } from "firebase-functions/v2";

// CORRECT
import { setGlobalOptions } from "firebase-functions/v2/options";
```

### Reasoning Engine Issues

**Error:** `Class must have a query method`
```bash
# Verify orchestrator_wrapper.py has query(**kwargs) method
grep -A 5 'def query' src/orchestrator_wrapper.py

# Deploy with correct wrapper
python src/deploy_with_wrapper.py
```

**Error:** `cloudpickle version mismatch`
```bash
# Use pinned version
pip install cloudpickle==3.1.1

# Verify version
python -c "import cloudpickle; print(cloudpickle.__version__)"
# Should output: 3.1.1
```

### Secret Manager Issues

**Error:** `Secret not found`
```bash
# List all secrets
gcloud secrets list

# Create missing secret
echo -n "your-api-key" | gcloud secrets create workspace-123-clay-key --data-file=-

# Test access
gcloud secrets versions access latest --secret="workspace-123-clay-key"
```

### ARV Validation Failures

```bash
# Check YAML syntax
yamllint agents/*.yaml

# Check JSON schemas
npm run arv

# Expected output:
# ✅ PASSED (5):
#    ✓ schema_reference
#    ✓ function_tool_wrappers
#    ✓ sub_agent_routing
#    ✓ json_schema_validity
#    ✓ connector_not_configured
```

### Background Process Management

**Check running background processes:**
```bash
# List all background shell processes
/bashes

# Check specific process output
# BashOutput tool with bash_id from /bashes command

# Kill stale/unwanted processes
# KillShell tool with shell_id
```

**Common scenarios:**
- Multiple video generation scripts running (NWSL project)
- Firebase deployment hanging (check bash 929321)
- Cloud Run deployments in progress (check bash e66ac2)

## CI/CD Pipeline

### GitHub Actions Workflows

1. **arv-gate.yml** - Validates agent configs and JSON schemas on every PR
2. **adk-guard.yml** - Ensures ADK compliance patterns
3. **policy.yml** - Enforces security and compliance policies
4. **ci-deploy.yml** - Continuous deployment to GCP
5. **deploy.yml** - Manual deployment trigger

## Phase 1 Status

**Completed ✅**
- Vertex AI Reasoning Engine deployed (3 successful deployments)
- Firebase Hosting live at pipelinepilot-prod.web.app
- Firestore database configured with security rules
- 4 async tool functions (Clay, Apollo, Clearbit, Crunchbase)
- Terraform templates for GCP deployment
- Multi-cloud architecture documentation (AWS/Azure)
- ARV validation system
- CI/CD workflows (policy.yml, adk-guard.yml, arv-gate.yml)
- Comprehensive documentation (11+ docs in 000-docs/)

**Known Issues 🔴**
- **Firebase Functions Gen2 deployment blocked** at Cloud Build infrastructure level
  - Affects: Dashboard API gateway
  - Status: Escalated to GCP Support with Build IDs
  - Workaround: Consider Cloud Run microservice alternative
  - Details: See `000-docs/0024-AA-AAR-functions-gen2-investigation.md`
- **Multiple code-level issues detected** (as of 2025-11-02):
  - `admin.initializeApp` import error in Functions
  - Orchestrator ADK compliance error (missing `query()` method pattern)
  - 16+ background processes need cleanup

**Not Included (Future Phases) ⏳**
- Billing/metering system
- Multi-tenant authentication
- Web UI dashboard
- CRM integrations (HubSpot, Salesforce)
- Email sending (Sendgrid, Mailgun)
- Advanced agents (ICP scorer, list builder)

## Support Resources

### Internal Documentation
- **Full Index:** [000-docs/000-INDEX.md](000-docs/000-INDEX.md)
- **ESM/ADK SOP:** [000-docs/6767-PP-SOP-Functions-ESM-Orchestrator-Query.md](000-docs/6767-PP-SOP-Functions-ESM-Orchestrator-Query.md)
- **System Analysis:** [000-docs/9999-DR-EXEC-complete-system-analysis.md](000-docs/9999-DR-EXEC-complete-system-analysis.md)

### Related Projects
- **iamNews Template:** `/home/jeremy/000-projects/iams/iamnews/`
- **BrightStream:** `/home/jeremy/000-projects/iams/iamnews/brightstream/`

### External Resources
- Google ADK: https://github.com/google/adk-python
- Vertex AI Agent Engine: https://cloud.google.com/vertex-ai/docs/agent-builder
- Firebase Functions Gen2: https://firebase.google.com/docs/functions/gen2
- Terraform: https://www.terraform.io/docs

---

---

**Last Updated:** 2025-11-07
**Version:** 1.0.0-phase1
**Status:** Phase 1 Foundation Complete

## Recent Changes

### 2025-11-07
- Archived Phase 1 migration artifacts to `000-docs/archive-2025-11-07/`
- Archived marketing assets (PNG images and campaign docs)
- Removed temporary files (ARV-LAST.json, ids.md)
- Cleaned up 000-docs directory structure
