# Bob's Brain: Quick Reference Card
*Generated: 2025-11-22 | Version: v0.10.0 | Branch: feature/a2a-agentcards-foreman-worker*

---

## 🎯 Purpose

**ADK-based multi-agent department** for Slack AI assistant. Production-grade reference implementation of Google's Agent Development Kit (ADK) with Vertex AI Agent Engine runtime, following strict "Hard Mode" compliance rules (R1-R8).

---

## 🏗️ Architecture At-a-Glance

```
[Slack User] → [Bob (Orchestrator)]
                      ↓
         [iam-senior-adk-devops-lead (Foreman)]
                      ↓
    ┌─────────┬──────────┬──────────┬─────────┐
    ↓         ↓          ↓          ↓         ↓
[iam-adk] [iam-issue] [iam-fix] [iam-qa] [iam-docs]
                      ↓
         [Vertex AI Agent Engine]
                      ↓
            [AgentCard (A2A Protocol)]
```

**Pattern**: Foreman + Workers (Agent Engine inline source deployment, 6767-INLINE)

---

## 🛠️ Tech Stack

| Component | Technology | Version | Local | Production |
|-----------|------------|---------|-------|------------|
| Agents | Python + google-adk | 3.12+ | Local dev | Vertex AI Agent Engine |
| Runtime | Vertex AI Agent Engine | Latest | N/A | Agent Engine (GCP) |
| Infrastructure | Terraform | Latest | Local plan | GCP (bobs-brain) |
| CI/CD | GitHub Actions | N/A | N/A | Workflow dispatch |
| Memory | Vertex AI Session + Memory Bank | Latest | N/A | Agent Engine |
| A2A Protocol | AgentCard JSON | 1.0 | tests/ | .well-known/agent-card.json |

**GCP Project**: `bobs-brain` (Project Number: 205354194989)

---

## 📁 Key Directories

```
bobs-brain/
├── agents/                      # ADK agent implementations
│   ├── bob/                     # Main orchestrator (entry: agent.py::app)
│   │   ├── agent.py            # Bob's LlmAgent definition
│   │   ├── prompts/            # System prompts
│   │   └── .well-known/        # AgentCard for A2A
│   └── iam_senior_adk_devops_lead/  # Foreman agent
│       ├── agent.py            # Foreman's LlmAgent
│       └── .well-known/        # AgentCard
│
├── scripts/                     # Operational scripts
│   ├── deploy_inline_source.py # Agent Engine deployment (NEW Phase 20)
│   ├── smoke_test_agent_engine.py  # Post-deploy health checks
│   └── check_a2a_readiness.py  # A2A compliance validation
│
├── .github/workflows/           # CI/CD pipelines
│   ├── ci.yml                  # Main CI (tests, ARV, drift)
│   └── deploy-containerized-dev.yml  # Dev deployment (dry-run mode)
│
├── infra/terraform/             # Infrastructure as Code
│   ├── iam.tf                  # WIF + service accounts (WIF commented out!)
│   ├── agent_engine.tf         # Agent Engine resources
│   └── envs/dev/dev.tfvars     # Dev environment config
│
├── 000-docs/                    # Documentation (filing standard v3.0)
│   ├── 6767-DR-STND-*.md       # Canonical standards (SOPs)
│   ├── 148-AA-REPT-*.md        # Phase 19 AAR
│   ├── 149-NOTE-*.md           # WIF audit (Phase 20)
│   ├── 150-AA-REPT-*.md        # Phase 20 AAR
│   └── 151-AA-REPT-*.md        # Phase 20 session AAR
│
└── tests/                       # Test suite
    ├── unit/                   # Unit tests (194 passing)
    └── integration/            # Integration tests
```

---

## 🚀 Quick Commands

```bash
# Environment Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Testing
pytest                                    # Run all tests (194 passing baseline)
pytest tests/unit/test_a2a_card.py -v    # Test AgentCards
make check-all                           # All quality checks (ARV + tests + drift)
make check-arv-minimum                   # Agent Readiness Verification

# A2A Compliance
python scripts/check_a2a_readiness.py    # Expected: ALL CHECKS PASSED

# Deployment (Dry-Run Mode - Phase 20)
python scripts/deploy_inline_source.py \
  --agent bob \
  --project-id bobs-brain \
  --region us-central1 \
  --env dev \
  --app-version 0.10.0 \
  --dry-run

# Smoke Tests (Config Validation)
python scripts/smoke_test_agent_engine.py \
  --project bobs-brain \
  --location us-central1 \
  --agent bob \
  --env dev \
  --config-only

# Drift Detection
bash scripts/ci/check_nodrift.sh         # No framework drift allowed (R1)

# Infrastructure
cd infra/terraform
terraform init
terraform plan -var-file="envs/dev/dev.tfvars"
# terraform apply -var-file="envs/dev/dev.tfvars"  # (manual only, requires WIF)
```

---

## 🔑 Environment Variables

```bash
# GCP Configuration
export PROJECT_ID="bobs-brain"           # GCP project (Project Number: 205354194989)
export REGION="us-central1"              # Default region
export ENV="dev"                         # Environment (dev/staging/prod)

# Deployment
export APP_VERSION="0.10.0"              # Current version

# GitHub Actions (Secrets - not set yet!)
# WIF_PROVIDER=projects/205354194989/locations/global/workloadIdentityPools/bobs-brain-github-pool/providers/github
# WIF_SERVICE_ACCOUNT=bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com
```

**Note**: Real deployment blocked - WIF secrets not configured yet (see Manual Setup below).

---

## 🌍 Environments

| Env | Deploy Method | Agent Runtime | Database | Status |
|-----|---------------|---------------|----------|--------|
| Local | pytest, dry-run | Stubbed | N/A | ✅ Working |
| Dev | GitHub Actions (manual trigger) | Vertex AI Agent Engine | Vertex AI Memory | ⏸️ Blocked (WIF not configured) |
| Staging | (Future) | Vertex AI Agent Engine | Vertex AI Memory | 🔜 Not implemented |
| Prod | (Future) | Vertex AI Agent Engine | Vertex AI Memory | 🔜 Not implemented |

**Current State**: Dev deployment workflow runs in **dry-run mode** only (Phase 20 complete).

---

## 🔐 Access & Auth

- **Auth Provider**: Workload Identity Federation (WIF) - **NOT CONFIGURED YET**
- **GCP Project**: `bobs-brain` (205354194989)
- **Service Account**: `bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com` (defined in Terraform, not deployed)
- **WIF Pool**: `bobs-brain-github-pool` (defined in Terraform, **commented out**)
- **GitHub Secrets**: **NOT SET** (blocking real deployment)

**Blocker**: WIF resources commented out in `infra/terraform/iam.tf` (lines 124-152). Must uncomment and apply before real deployment.

---

## 📊 Key APIs/Entrypoints

| Agent | Entrypoint | Pattern | Purpose |
|-------|------------|---------|---------|
| bob | `agents.bob.agent::app` | 6767-LAZY (lazy-loading App) | Main orchestrator, Slack interface |
| iam-senior-adk-devops-lead | `agents.iam_senior_adk_devops_lead.agent::app` | 6767-LAZY | Foreman, A2A orchestrator |
| (Future) iam-adk | TBD | 6767-LAZY | ADK design specialist |
| (Future) iam-issue | TBD | 6767-LAZY | Issue creation specialist |
| (Future) iam-fix-plan | TBD | 6767-LAZY | Fix planning specialist |

**Deployment Pattern**: 6767-INLINE (inline source deployment to Agent Engine)

---

## 🚨 Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| Tests failing | Missing google.adk? | Expected: 26 failures locally (google.adk not installed) |
| Import errors | Wrong module path? | Use underscored paths: `agents.iam_senior_adk_devops_lead.agent` |
| Drift detection fails | LangChain imported? | Remove non-ADK frameworks (R1 violation) |
| Deployment blocked | WIF configured? | Uncomment `infra/terraform/iam.tf` lines 124-152, fill `YOUR_GITHUB_ORG` |
| Dry-run exits 3 | GCP client missing? | Expected: local env doesn't have google-cloud-aiplatform |
| A2A checks fail | AgentCard invalid? | Run `pytest tests/unit/test_a2a_card.py -v` |
| CI workflow fails | Secrets missing? | Add WIF_PROVIDER and WIF_SERVICE_ACCOUNT to GitHub (blocked) |

---

## 📈 Monitoring

- **CI Status**: `.github/workflows/ci.yml` - runs on push/PR
- **Test Baseline**: 194 passing, 26 expected failures (local only)
- **A2A Compliance**: `python scripts/check_a2a_readiness.py` (ALL CHECKS PASSED)
- **Drift Detection**: `bash scripts/ci/check_nodrift.sh` (clean)
- **Deployment Logs**: (Future) Cloud Logging when Agent Engine deployed
- **Agent Metrics**: (Future) Vertex AI Agent Engine console

**Current**: All monitoring via local tests + CI checks. No production deployment yet.

---

## 👥 Team Contacts

| Role | Contact | Area |
|------|---------|------|
| Project Owner | @user | Architecture, ADK patterns |
| DevOps | (TBD) | GCP, WIF, Terraform |
| Documentation | See 000-docs/ | Phase AARs, standards |

---

## 🔗 Essential Links

- **Repo**: `bobs-brain/` (local development)
- **Main Docs**: `000-docs/` (1,800+ lines of documentation)
- **Standards**: `000-docs/6767-*.md` (canonical SOPs)
- **Phase 20 AAR**: `000-docs/150-AA-REPT-phase-20-inline-deploy-script-and-dev-wiring.md`
- **WIF Audit**: `000-docs/149-NOTE-wif-and-github-actions-dev-audit.md`
- **CI/CD**: `.github/workflows/` (ci.yml, deploy-containerized-dev.yml)

---

## ⚡ First Day Checklist

- [ ] Clone repo: `cd /home/jeremy/000-projects/iams/bobs-brain/`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run tests: `pytest` (expect 194 passing)
- [ ] Run A2A checks: `python scripts/check_a2a_readiness.py`
- [ ] Test dry-run deployment: `python scripts/deploy_inline_source.py --help`
- [ ] Read Phase 20 AAR: `000-docs/150-AA-REPT-*.md`
- [ ] Review standards: `000-docs/6767-DR-STND-*.md`
- [ ] Check branch status: `git status` (should be on feature/a2a-agentcards-foreman-worker)

---

## 🎬 Next Steps (Phase 21)

**Goal**: First real deployment to Vertex AI Agent Engine

**Prerequisites** (Manual Setup Required):
1. **Enable GCP APIs**:
   ```bash
   export PROJECT_ID="bobs-brain"
   gcloud config set project "$PROJECT_ID"
   gcloud services enable aiplatform.googleapis.com --project="$PROJECT_ID"
   gcloud services enable storage-api.googleapis.com --project="$PROJECT_ID"
   gcloud services enable iam.googleapis.com --project="$PROJECT_ID"
   gcloud services enable run.googleapis.com --project="$PROJECT_ID"
   ```

2. **Configure WIF** (⚠️ BLOCKER):
   ```bash
   # Edit infra/terraform/iam.tf
   # - Uncomment lines 124-152 (WIF pool, provider, binding)
   # - Replace YOUR_GITHUB_ORG with actual GitHub username/org

   cd infra/terraform
   terraform init
   terraform apply -var-file="envs/dev/dev.tfvars"
   ```

3. **Add GitHub Secrets**:
   - Navigate to: repo Settings → Secrets and variables → Actions
   - Add `WIF_PROVIDER` = `projects/205354194989/locations/global/workloadIdentityPools/bobs-brain-github-pool/providers/github`
   - Add `WIF_SERVICE_ACCOUNT` = `bobs-brain-github-actions@bobs-brain.iam.gserviceaccount.com`

4. **Implement Real Deployment**:
   - Update `scripts/deploy_inline_source.py` lines 309-373
   - Replace TODOs with actual Agent Engine API calls

5. **Deploy**:
   - Remove `--dry-run` from `.github/workflows/deploy-containerized-dev.yml`
   - Trigger workflow: `workflow_dispatch`
   - Deploy bob to dev environment
   - Run smoke tests

**Estimated Time**: 2-3 hours

---

## 📚 Key Standards (6767-series SOPs)

All `000-docs/6767-*.md` files are **Standard Operating Procedures**:

| Standard | Purpose |
|----------|---------|
| 6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md | Hard Mode rules (R1-R8) - MANDATORY |
| 6767-LAZY-DR-STND-adk-lazy-loading-app-pattern.md | Lazy-loading App pattern |
| 6767-INLINE-DR-STND-inline-source-deployment-for-vertex-agent-engine.md | Inline source deployment |
| 127-DR-STND-agent-engine-entrypoints.md | Canonical entrypoints |

---

## 🎯 Hard Mode Rules (R1-R8) - ENFORCED IN CI

1. **R1**: ADK-Only (no LangChain, CrewAI, custom frameworks)
2. **R2**: Vertex AI Agent Engine runtime (no self-hosted runners)
3. **R3**: Gateway separation (Cloud Run proxies only)
4. **R4**: CI-only deployments (GitHub Actions with WIF)
5. **R5**: Dual memory wiring (Session + Memory Bank)
6. **R6**: Single doc folder (`000-docs/` only)
7. **R7**: SPIFFE ID propagation
8. **R8**: Drift detection (runs first in CI)

**Violation = CI failure**

---

## 🚀 Quick Start (5-Minute Setup)

```bash
# 1. Navigate to repo
cd /home/jeremy/000-projects/iams/bobs-brain/

# 2. Activate venv (or create new)
source .venv/bin/activate
# OR: python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest

# 5. Check A2A readiness
python scripts/check_a2a_readiness.py

# 6. Test deployment (dry-run)
python scripts/deploy_inline_source.py \
  --agent bob \
  --project-id bobs-brain \
  --region us-central1 \
  --env dev \
  --app-version 0.10.0 \
  --dry-run

# Expected: All tests pass, A2A checks pass, dry-run succeeds ✅
```

---

## 🔍 Common File Locations

| Need | Location |
|------|----------|
| Agent definitions | `agents/*/agent.py` |
| System prompts | `agents/*/prompts/*.txt` |
| AgentCards (A2A) | `agents/*/.well-known/agent-card.json` |
| Deployment script | `scripts/deploy_inline_source.py` |
| Smoke tests | `scripts/smoke_test_agent_engine.py` |
| CI workflows | `.github/workflows/*.yml` |
| Terraform | `infra/terraform/*.tf` |
| Documentation | `000-docs/*.md` |
| Phase 20 AAR | `000-docs/150-AA-REPT-phase-20-*.md` |

---

## 📊 Current Metrics

- **Version**: v0.10.0
- **Tests**: 194 passing, 26 expected failures (local)
- **Documentation**: 3 AARs (~1,800 lines)
- **Code**: ~460 lines (deployment script)
- **Standards**: 4+ canonical 6767-series SOPs
- **Agents**: 2 implemented (bob, foreman), 5+ planned
- **CI Status**: ✅ All checks passing
- **Deployment Status**: ⏸️ Blocked (awaiting WIF setup)

---

## ⚠️ Known Blockers

1. **WIF Not Configured** - Terraform resources commented out
2. **GitHub Secrets Missing** - WIF_PROVIDER, WIF_SERVICE_ACCOUNT not set
3. **Agent Engine API Stubbed** - Real deployment not implemented
4. **No Production Environment** - Only dev configured

**All blockers documented in**: `000-docs/149-NOTE-wif-and-github-actions-dev-audit.md`

---

## 🎓 Learning Path

1. **Start**: Read `000-docs/150-AA-REPT-phase-20-*.md` (Phase 20 AAR)
2. **Standards**: Review `000-docs/6767-DR-STND-*.md` (Hard Mode rules)
3. **Architecture**: Explore `agents/bob/agent.py` (main orchestrator)
4. **Deployment**: Study `scripts/deploy_inline_source.py` (inline source pattern)
5. **A2A**: Review `agents/*/.well-known/agent-card.json` (agent contracts)
6. **CI/CD**: Examine `.github/workflows/ci.yml` (quality gates)

---

**Generated**: 2025-11-22
**Version**: v0.10.0
**Branch**: feature/a2a-agentcards-foreman-worker
**Status**: Phase 20 Complete, Phase 21 Ready (awaiting WIF setup)
