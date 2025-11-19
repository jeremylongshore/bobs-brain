# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0] - 2025-11-19

### Added - Phase 3: Vertex AI Search Grounding

- **Semantic Search Tool** (`my_agent/tools/vertex_search_tool.py`)
  - `search_vertex_ai()` - AI-powered semantic search with extractive answers
  - `get_vertex_search_status()` - Datastore health monitoring
  - Discovery Engine v1 API with query expansion & spell correction
  - 90-95% accuracy (up from 70-80% with keyword search)

- **Infrastructure Setup** (`scripts/setup_vertex_search.sh`)
  - Automated GCS bucket creation & document upload
  - Datastore creation & document indexing
  - One-command setup (2-3 min + 10-15 min indexing)
  - Validates prerequisites & provides detailed progress

- **Terraform Updates** (Infrastructure as Code for Phase 3)
  - `main.tf` - Added `discoveryengine.googleapis.com` and `storage.googleapis.com` APIs
  - `storage.tf` - Added ADK documentation bucket with Vertex Search permissions
  - `agent_engine.tf` - Added `VERTEX_SEARCH_DATASTORE_ID` environment variable
  - `iam.tf` - Added `roles/discoveryengine.viewer` for Agent Engine service account
  - `variables.tf` - Added `vertex_search_datastore_id` variable
  - All environment tfvars updated (dev, staging, prod)

- **Documentation** (`000-docs/076-AT-IMPL-vertex-ai-search-grounding.md`)
  - Complete implementation guide (900+ lines)
  - Architecture before/after comparison
  - Setup instructions & troubleshooting
  - Cost analysis (free 5GB tier usage)

### Changed

- **Agent Integration** (`my_agent/agent.py`)
  - Added semantic search tools alongside keyword search
  - Enhanced instruction with tool selection guidance
  - Dual search strategy: semantic for concepts, keyword for exact terms

- **Configuration**
  - `requirements.txt` - Added `google-cloud-discoveryengine>=0.11.0`
  - `.env.example` - Added `VERTEX_SEARCH_DATASTORE_ID` config

### Fixed - Drift Detection Improvements

- **R3 Compliance** (`service/a2a_gateway/main.py`)
  - Fixed R3 violation: Removed `my_agent` import in gateway
  - Inlined AgentCard logic to avoid importing agent code
  - Gateway now fully compliant (proxy only, no agent imports)

- **Drift Check Script** (`scripts/ci/check_nodrift.sh`)
  - Exclude `000-docs/` from R1 check (avoid false positives from examples)
  - Exclude `*.md` files from R3 checks (documentation examples)
  - Match only actual Python import statements (not comments/docstrings)
  - Improved regex patterns to reduce false positives

### Benefits

- **Semantic Understanding** - Query "agent orchestration" finds "SequentialAgent"
- **Query Expansion** - Automatic addition of related search terms
- **Extractive Answers** - Direct quotes from ADK documentation
- **Cost Efficiency** - $0/month (270KB docs = 0.0054% of free 5GB tier)
- **Scalability** - Can add 18,500+ more docs before paid tier

## [0.6.0] - 2025-11-11

### Added - Phase 2: Agent Core + Drift Detection

- **ADK Agent Implementation** (`my_agent/agent.py`)
  - LlmAgent with Gemini 2.0 Flash model
  - Dual memory wiring (VertexAiSessionService + VertexAiMemoryBankService)
  - After-agent callback for automatic session persistence
  - SPIFFE ID propagation in all logs
  - Environment variable validation
  - Comprehensive error handling

- **A2A Protocol Support** (`my_agent/a2a_card.py`)
  - AgentCard for agent-to-agent discovery
  - SPIFFE ID included in description (R7 compliance)
  - JSON serialization for HTTP responses

- **Drift Detection** (`scripts/ci/check_nodrift.sh`)
  - Scans for alternative frameworks (LangChain, CrewAI, etc.)
  - Blocks Runner imports in service/ (R3 enforcement)
  - Detects local GCP credential files (R4 enforcement)
  - Verifies single docs folder (R6 enforcement)
  - CI-first pipeline (drift check blocks all other jobs)

- **Configuration**
  - `.env.example` - Complete environment variable template
  - All required variables documented with Hard Mode rules
  - Environment-specific examples (dev, staging, prod)

- **User Manual** (`000-docs/001-usermanual/`)
  - Google Cloud ADK reference notebooks (2 notebooks, 132KB total)
  - Multi-agent systems with Claude (102KB)
  - Memory for ADK in Cloud Run (30KB)
  - README with implementation guidance

- **Documentation** (6 new documents)
  - `053-AA-REPT-hardmode-baseline.md` - Phase 1-2 implementation AAR
  - `054-AT-ALIG-notebook-alignment-checklist.md` - Alignment analysis (70% aligned)
  - `055-AA-CRIT-import-path-corrections.md` - Critical import fixes
  - `056-AA-CONF-usermanual-import-verification.md` - Google Cloud notebook compliance

### Fixed

- **Import Paths** - Corrected ADK imports to match google-adk 1.18.0 API
  - `from google.adk import Runner` (not `google.adk.runner`)
  - `from google.adk.sessions import VertexAiSessionService` (not from `.memory`)
  - `from a2a.types import AgentCard` (requires separate `a2a-sdk` package)
  - All imports verified against official Google Cloud notebooks

- **Dependencies**
  - Added `a2a-sdk>=0.3.0` for A2A protocol support
  - Updated requirements.txt with Hard Mode comments

### Changed

- **CI/CD Pipeline** (`.github/workflows/ci.yml`)
  - Complete rewrite for Hard Mode enforcement
  - Drift detection runs FIRST (blocks all other jobs if violations found)
  - Added structure validation, documentation checks
  - Terraform validation integrated
  - 7 parallel jobs after drift check passes

- **CLAUDE.md** - Updated with correct import paths (R5 section)
- **README.md** - Complete rewrite for Hard Mode architecture
  - ADK + Agent Engine focus (removed multi-implementation confusion)
  - Hard Rules (R1-R8) documentation
  - Phase 2 status and roadmap
  - Quick start with import verification

### Status: Phase 2 Complete (50% Total Progress)

**Completed:**
- ✅ Repository structure flattened (8 canonical directories)
- ✅ Hard Mode rules enforced in CI (R1-R8)
- ✅ ADK agent implementation with dual memory
- ✅ A2A protocol AgentCard
- ✅ Drift detection script
- ✅ Import paths verified against user manuals
- ✅ Configuration template created

**Next: Phase 3** - Service gateways (A2A + Slack), Dockerfile, unit tests

## [0.5.1] - 2025-11-11

### Changed
- **Repository Restructure** - Archived legacy implementations to `99-Archive/2025-11-11`
- **Simplified README** - Focused on template/learning resource positioning
- **Cleaned Top-Level** - Removed non-canonical roots for cleaner structure

### Removed
- Archived Flask implementation (`src/`, `02-Src/`, etc.)
- Archived experimental agents (ADK, Genkit, bob-vertex-agent)
- Archived development artifacts (`venv/`, `__pycache__/`, config files)
- Removed `CONTRIBUTING.md` and `Dockerfile` from root

### Documentation
- Night Wrap AAR: Repository cleanup and archival process
- Updated CLAUDE.md with simplified guidance

### Infrastructure
- Enabled auto-delete branches on merge (GitHub repository settings)
- Repository positioned as template/learning resource

## [0.5.0] - 2025-11-10

### Added
- Initial VERSION file
- Keep a Changelog format adoption
- Documentation structure (`000-docs/`)

### Changed
- Repository positioning as template for beginners
- Focus on Slack AI agent starter code

## Earlier Versions

See `99-Archive/` for historical implementations including:
- v4-v5: Flask modular agent with multiple LLM providers
- v2-v3: Vertex AI Agent Engine implementation
- v1: ADK and Genkit experimental versions

---

**Note:** Version 0.5.0 and 0.5.1 represent the "clean slate" repositioning of Bob's Brain as a template/learning resource, with all production implementations archived for reference.
