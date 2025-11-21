# ADK Spec to Implementation and ARV Mapping

**Document ID:** 121-DR-MAP-adk-spec-to-implementation-and-arv
**Phase:** SPEC-ALIGN-ARV-EXPANSION (S2)
**Status:** Active (Repo-Local)
**Created:** 2025-11-20
**Purpose:** Map each rule from the canonical ADK/Agent Engine spec (`6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md`) to its implementation in this repo, ARV check scripts, and test coverage.

---

## I. Executive Summary

This document provides **concrete mappings** from the abstract specification in the 6767 ADK/Agent Engine spec to:
1. **Implementation Locations**: Where in the repo each rule is implemented
2. **ARV Check Scripts**: Which scripts enforce each rule
3. **Test Coverage**: Which tests validate each rule
4. **Manual Review**: Rules that require human judgment

**Key Audiences:**
- **Build Captains**: Understand where rules live and how they're checked
- **ARV Engineers**: Know what to implement or extend
- **Future Claude Sessions**: Find relevant code quickly

---

## II. Hard Mode Rules (R1-R8) Mapping

### R1: ADK-Only Implementation

**Rule:** All agents MUST be built with ADK primitives.

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/bob/agent.py`<br>`agents/iam_*/agent.py`<br>All use `from google.adk.agents import LlmAgent` |
| **ARV Script** | `scripts/ci/check_nodrift.sh` (detects alternative frameworks)<br>**TODO**: `scripts/check_arv_agents.py` (validate ADK imports) |
| **Test Coverage** | **TODO**: `tests/unit/test_arv_agents.py` |
| **Manual Review** | Code review for new agents |
| **Status** | ✅ Implemented<br>⚠️ ARV check partial (nodrift.sh)<br>❌ Dedicated ARV script missing<br>❌ Tests missing |
| **Priority** | HIGH - Core architectural rule |

**Evidence of Implementation:**
- `agents/bob/agent.py:5` - `from google.adk.agents import LlmAgent`
- `agents/iam_issue/agent.py:7` - `from google.adk.agents import LlmAgent`
- `agents/iam_senior_adk_devops_lead/agent.py:6` - ADK patterns

**What to Check:**
- ❌ No `import langchain`
- ❌ No `import crewai`
- ❌ No `import autogen`
- ✅ All agents import from `google.adk`
- ✅ Tools use ADK tool system

---

### R2: Vertex AI Agent Engine Runtime

**Rule:** Agents MUST be deployed to Agent Engine, not self-hosted.

| Aspect | Details |
|--------|---------|
| **Implementation** | `.github/workflows/ci.yml` (deployment jobs)<br>`infra/terraform/agent_engine.tf` (Agent Engine resources)<br>`agents/config/agent_engine.py` (Agent Engine config) |
| **ARV Script** | `scripts/check_arv_engine_flags.py` (validates Agent Engine config)<br>`scripts/ci/check_nodrift.sh` (detects self-hosted patterns) |
| **Test Coverage** | **TODO**: `tests/integration/test_agent_engine_deployment.py` |
| **Manual Review** | Deployment logs (ADK CLI output) |
| **Status** | ✅ Implemented<br>✅ ARV check exists (check_arv_engine_flags.py)<br>❌ Integration tests missing |
| **Priority** | HIGH - Production deployment requirement |

**Evidence of Implementation:**
- `infra/terraform/agent_engine.tf:1-50` - Agent Engine resource definitions
- `.github/workflows/ci.yml:deploy-*` - ADK CLI deployment jobs
- `agents/config/agent_engine.py` - Centralized Agent Engine config

**What to Check:**
- ✅ Deployment via `adk deploy agent_engine`
- ❌ No self-hosted Runners on VMs
- ❌ No embedded Runners in application code
- ✅ Agent Engine IDs in config, not hard-coded

---

### R3: Gateway Separation

**Rule:** Cloud Run services are REST proxies only, never run Runners.

| Aspect | Details |
|--------|---------|
| **Implementation** | `service/a2a_gateway/main.py` (REST proxy to Agent Engine)<br>`service/slack_webhook/main.py` (Slack → Agent Engine proxy) |
| **ARV Script** | `scripts/ci/check_nodrift.sh` (detects Runner imports in service/)<br>**TODO**: `scripts/check_arv_services.py` (dedicated service checks) |
| **Test Coverage** | **TODO**: `tests/unit/test_arv_services.py` |
| **Manual Review** | Code review for new services |
| **Status** | ✅ Implemented<br>⚠️ ARV check partial (nodrift.sh)<br>❌ Dedicated ARV script missing<br>❌ Tests missing |
| **Priority** | HIGH - Gateway separation is core pattern |

**Evidence of Implementation:**
- `service/a2a_gateway/main.py:1-200` - No Runner imports, only REST calls
- `service/slack_webhook/main.py:1-300` - No Runner imports, calls Agent Engine

**What to Check:**
- ❌ No `from google.adk import Runner` in service/
- ❌ No `LlmAgent` construction in service/
- ❌ No direct `model.generate_content()` calls
- ✅ Only REST API calls to Agent Engine
- ✅ OAuth2 token authentication

---

### R4: CI-Only Deployments

**Rule:** All deployments MUST go through GitHub Actions with WIF.

| Aspect | Details |
|--------|---------|
| **Implementation** | `.github/workflows/ci.yml` (GitHub Actions workflows)<br>`.github/workflows/deploy-*.yml` (Environment-specific deployments)<br>`infra/terraform/iam.tf` (WIF configuration) |
| **ARV Script** | **Manual Review**: CI logs and WIF configuration<br>**TODO**: `scripts/check_arv_ci.py` (validate workflow structure) |
| **Test Coverage** | **Manual Review**: Deployment audit logs |
| **Manual Review** | ✅ Required - validate no local deployments |
| **Status** | ✅ Implemented<br>⚠️ No automated ARV check (hard to automate)<br>❌ CI structure validation missing |
| **Priority** | MEDIUM - Enforced by WIF, harder to violate |

**Evidence of Implementation:**
- `.github/workflows/ci.yml:1-200` - All deployment jobs use WIF
- `infra/terraform/iam.tf:50-100` - Workload Identity Federation setup
- No `.json` service account key files in repo

**What to Check:**
- ✅ All deployments via GitHub Actions
- ❌ No service account key files (`.json`)
- ✅ WIF authentication configured
- ❌ No manual `gcloud deploy` in prod/staging

---

### R5: Dual Memory Wiring

**Rule:** Agents use VertexAiSessionService + VertexAiMemoryBankService.

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/bob/agent.py:auto_save_session_to_memory()` callback<br>`agents/bob/agent.py:get_agent()` - memory wiring<br>`agents/config/memory.py` - memory configuration |
| **ARV Script** | **TODO**: `scripts/check_arv_memory.py` (validate memory patterns)<br>**Manual Review**: Code review for agent memory setup |
| **Test Coverage** | **TODO**: `tests/integration/test_memory_persistence.py` |
| **Manual Review** | ✅ Required - validate session persistence works |
| **Status** | ✅ Implemented<br>❌ ARV check missing (hard to automate fully)<br>❌ Tests missing |
| **Priority** | MEDIUM - Validated via integration tests |

**Evidence of Implementation:**
- `agents/bob/agent.py:15-30` - `from google.adk.sessions import VertexAiSessionService`
- `agents/bob/agent.py:40-50` - `from google.adk.memory import VertexAiMemoryBankService`
- `agents/bob/agent.py:100-120` - `after_agent_callback=auto_save_session_to_memory`

**What to Check:**
- ✅ VertexAiSessionService used for conversations
- ✅ VertexAiMemoryBankService used for long-term knowledge
- ✅ after_agent_callback wired for session persistence
- ❌ No global variable state
- ❌ No custom memory systems bypassing ADK

---

### R6: Single Documentation Folder

**Rule:** All docs in `000-docs/` with NNN-CC-ABCD naming.

| Aspect | Details |
|--------|---------|
| **Implementation** | `000-docs/` directory structure<br>All documentation files follow naming convention |
| **ARV Script** | **TODO**: `scripts/check_arv_docs.py` (validate naming, structure, 6767 IDs) |
| **Test Coverage** | **TODO**: `tests/unit/test_arv_docs.py` |
| **Manual Review** | Code review for new docs |
| **Status** | ✅ Implemented<br>❌ ARV check missing<br>❌ Tests missing |
| **Priority** | LOW - Easy to enforce in review |

**Evidence of Implementation:**
- `000-docs/*.md` - All docs in single folder
- `000-docs/6767-*.md` - Canonical standards with 6767 prefix
- `000-docs/NNN-CC-ABCD-*.md` - Repo-local docs with sequential numbers

**What to Check:**
- ✅ All docs in `000-docs/`
- ❌ No multiple doc folders (no `docs/`, `documentation/`, etc.)
- ✅ Naming convention: `NNN-CC-ABCD-description.md`
- ✅ 6767 prefix for canonical standards
- ❌ No duplicate 6767 IDs
- ✅ Sequential NNN numbers for repo-local docs

---

### R7: SPIFFE ID Propagation

**Rule:** Immutable agent identity in all telemetry and logs.

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/bob/a2a_card.py:spiffe_id` field<br>`agents/utils/logging.py:log_*()` functions include SPIFFE ID<br>`agents/a2a/adapter.py` - SPIFFE ID in A2A calls |
| **ARV Script** | **TODO**: `scripts/check_arv_spiffe.py` (validate SPIFFE format and usage)<br>**Manual Review**: Log samples |
| **Test Coverage** | **TODO**: `tests/unit/test_spiffe_id_format.py` |
| **Manual Review** | ✅ Required - validate logs include SPIFFE ID |
| **Status** | ⚠️ Partially implemented<br>❌ ARV check missing<br>❌ Tests missing |
| **Priority** | MEDIUM - Important for observability |

**Evidence of Implementation:**
- `agents/bob/a2a_card.py:20-30` - SPIFFE ID defined
- `agents/utils/logging.py:50-100` - Structured logging with SPIFFE ID
- Format: `spiffe://intent.solutions/agent/bobs-brain/<env>/<region>/<version>`

**What to Check:**
- ✅ SPIFFE ID format matches spec
- ✅ SPIFFE ID in AgentCard metadata
- ✅ SPIFFE ID in structured logs
- ✅ SPIFFE ID in A2A calls
- ❌ No mutable agent identifiers
- ❌ No generic agent names without environment

---

### R8: Drift Detection

**Rule:** ARV checks run FIRST in CI and block on violations.

| Aspect | Details |
|--------|---------|
| **Implementation** | `.github/workflows/ci.yml:drift-check` job (runs first)<br>`scripts/ci/check_nodrift.sh` - main drift detection script |
| **ARV Script** | ✅ `scripts/ci/check_nodrift.sh` (enforces R1, R2, R3) |
| **Test Coverage** | **TODO**: `tests/integration/test_ci_workflow_order.py` |
| **Manual Review** | CI job execution order |
| **Status** | ✅ Implemented<br>✅ ARV check exists<br>❌ Tests missing |
| **Priority** | CRITICAL - First line of defense |

**Evidence of Implementation:**
- `.github/workflows/ci.yml:30-50` - drift-check job runs before all others
- `scripts/ci/check_nodrift.sh:1-200` - Detects alternative frameworks, Runner in services, hard-coded credentials

**What to Check:**
- ✅ drift-check job runs first in CI
- ✅ Blocks on alternative frameworks (LangChain, etc.)
- ✅ Blocks on Runner in service/
- ✅ Blocks on local credentials
- ✅ Clear error messages on violations
- ✅ All downstream jobs depend on drift-check passing

---

## III. ADK Agent Expectations Mapping

### Agent Construction

**Expectation:** All agents use `LlmAgent` with proper factory pattern.

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/bob/agent.py:get_agent()` factory<br>`agents/iam_*/agent.py:get_agent()` factories<br>`agents/*/agent.py:root_agent` for ADK CLI |
| **ARV Script** | **TODO**: `scripts/check_arv_agents.py` (validate agent structure) |
| **Test Coverage** | **TODO**: `tests/unit/test_agent_construction.py` |
| **Manual Review** | Code review for new agents |
| **Status** | ✅ Implemented<br>❌ ARV check missing<br>❌ Tests missing |
| **Priority** | HIGH - Core pattern |

**What to Check:**
- ✅ Each agent has `get_agent()` factory
- ✅ Each agent exports `root_agent` for CLI
- ✅ Uses `LlmAgent` constructor
- ✅ Tools registered via `tools=[]` parameter
- ❌ No direct model API calls

---

### Tool System

**Expectation:** All tools use ADK tool system (built-ins or FunctionTool).

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/bob/tools/*.py` - ADK FunctionTool wrappers<br>`agents/iam_*/tools/*.py` - Custom tools as FunctionTool |
| **ARV Script** | **TODO**: `scripts/check_arv_tools.py` (validate tool patterns) |
| **Test Coverage** | **TODO**: `tests/unit/test_tools.py` |
| **Manual Review** | Code review for new tools |
| **Status** | ✅ Implemented<br>❌ ARV check missing<br>❌ Tests missing |
| **Priority** | MEDIUM - Enforced by ADK at runtime |

**What to Check:**
- ✅ Tools wrapped as FunctionTool
- ✅ Proper docstrings (ADK introspects)
- ✅ Type hints (ADK generates schemas)
- ❌ No custom tool frameworks

---

### A2A Communication

**Expectation:** Use standardized A2A contracts (A2AAgentCall, A2AAgentResult).

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/a2a/contracts.py` - A2AAgentCall/Result dataclasses<br>`agents/a2a/adapter.py` - Unified routing adapter<br>`service/a2a_gateway/main.py` - A2A HTTP endpoint |
| **ARV Script** | **TODO**: `scripts/check_arv_a2a.py` (validate A2A usage) |
| **Test Coverage** | **TODO**: `tests/integration/test_a2a_protocol.py` |
| **Manual Review** | Code review for inter-agent calls |
| **Status** | ✅ Implemented<br>❌ ARV check missing<br>❌ Tests missing |
| **Priority** | MEDIUM - Important for multi-agent coordination |

**What to Check:**
- ✅ All A2A calls use A2AAgentCall/Result contracts
- ✅ Adapter pattern (local vs engine routing)
- ✅ Correlation IDs propagated
- ✅ SPIFFE IDs included
- ❌ No direct HTTP calls between agents

---

## IV. Department-Wide Conventions Mapping

### File Layout

**Convention:** Standardized directory structure.

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/` - All agents<br>`service/` - Gateways only<br>`infra/terraform/` - IaC<br>`scripts/` - Automation<br>`tests/` - Test suites<br>`000-docs/` - Single docs root |
| **ARV Script** | **TODO**: `scripts/check_arv_structure.py` (validate directory structure) |
| **Test Coverage** | **TODO**: `tests/unit/test_directory_structure.py` |
| **Manual Review** | Code review for new directories |
| **Status** | ✅ Implemented<br>❌ ARV check missing<br>❌ Tests missing |
| **Priority** | LOW - Structural, easy to spot |

**What to Check:**
- ✅ All agents in `agents/`
- ✅ All gateways in `service/`
- ✅ All docs in `000-docs/`
- ❌ No multiple agent directories
- ❌ No scattered doc folders

---

### Feature Flag Defaults

**Convention:** External integrations default OFF, dry-run default ON.

| Aspect | Details |
|--------|---------|
| **Implementation** | `agents/config/github_features.py` - GitHub flags<br>`agents/config/notifications.py` - Slack flags<br>`agents/config/storage.py` - Org storage flags<br>`.env.example` - Default values |
| **ARV Script** | ✅ `scripts/check_config_all.py` (validates config defaults)<br>**TODO**: `scripts/check_arv_config.py` (dedicated config ARV) |
| **Test Coverage** | **TODO**: `tests/unit/test_config_defaults.py` |
| **Manual Review** | Code review for new features |
| **Status** | ✅ Implemented<br>⚠️ ARV check partial (check_config_all.py)<br>❌ Dedicated ARV missing<br>❌ Tests missing |
| **Priority** | HIGH - Safety critical |

**What to Check:**
- ✅ New features default `ENABLED=false`
- ✅ Dry-run modes default `DRY_RUN=true`
- ✅ Destructive operations default OFF
- ❌ No hard-coded enable flags for new features

---

## V. ARV Script Inventory

### Existing Scripts

| Script | Purpose | Rules Enforced | Status |
|--------|---------|----------------|--------|
| `scripts/ci/check_nodrift.sh` | Drift detection | R1, R2, R3, R8 | ✅ Active |
| `scripts/check_arv_minimum.py` | Baseline ARV requirements | Logging, correlation IDs, agent structure | ✅ Active |
| `scripts/check_arv_engine_flags.py` | Agent Engine config validation | R2 (partial) | ✅ Active |
| `scripts/check_config_all.py` | Config validation | Feature flag defaults (partial) | ✅ Active |
| `scripts/run_arv_department.py` | Department-wide ARV orchestrator | Aggregates all ARV checks | ✅ Active |

### Missing Scripts (S3 TODO)

| Script (Planned) | Purpose | Rules to Enforce | Priority |
|------------------|---------|------------------|----------|
| `scripts/check_arv_agents.py` | Agent structure validation | R1, Agent construction | HIGH |
| `scripts/check_arv_services.py` | Gateway separation validation | R3, Gateway patterns | HIGH |
| `scripts/check_arv_docs.py` | Documentation structure | R6, Doc naming | LOW |
| `scripts/check_arv_config.py` | Feature flag defaults | Config defaults, safety | HIGH |
| `scripts/check_arv_memory.py` | Memory pattern validation | R5, Dual memory | MEDIUM |
| `scripts/check_arv_spiffe.py` | SPIFFE ID validation | R7, Identity propagation | MEDIUM |
| `scripts/check_arv_tools.py` | Tool system validation | Tool patterns | MEDIUM |
| `scripts/check_arv_a2a.py` | A2A protocol validation | A2A contracts | MEDIUM |
| `scripts/check_arv_structure.py` | Directory structure | File layout conventions | LOW |
| `scripts/check_arv_ci.py` | CI workflow validation | R4, R8 (CI order) | LOW |

---

## VI. Test Coverage Inventory

### Existing Tests

| Test Suite | Coverage | Status |
|------------|----------|--------|
| `tests/unit/` | Unit tests for utilities | ⚠️ Sparse |
| `tests/integration/` | Integration tests | ❌ None for ARV |

### Missing Tests (S3 TODO)

| Test Suite (Planned) | Purpose | Priority |
|-----------------------|---------|----------|
| `tests/unit/test_arv_agents.py` | Test agent structure checks | HIGH |
| `tests/unit/test_arv_services.py` | Test gateway separation checks | HIGH |
| `tests/unit/test_arv_docs.py` | Test doc naming checks | LOW |
| `tests/unit/test_config_defaults.py` | Test feature flag defaults | HIGH |
| `tests/integration/test_memory_persistence.py` | Test session persistence | MEDIUM |
| `tests/integration/test_a2a_protocol.py` | Test A2A communication | MEDIUM |
| `tests/integration/test_agent_engine_deployment.py` | Test ADK CLI deployment | LOW |

---

## VII. Manual Review Requirements

Some rules are **impossible or impractical to automate fully** and require human judgment:

| Rule/Aspect | Why Manual Review Needed | Review Process |
|-------------|--------------------------|----------------|
| **R4 (CI-Only Deployments)** | Hard to detect manual `gcloud` commands outside CI | Audit deployment logs, WIF enforces |
| **R5 (Dual Memory Wiring)** | Memory usage is runtime behavior | Integration tests + code review |
| **R7 (SPIFFE ID Propagation)** | Need to sample logs | Sample Cloud Logging, check SPIFFE IDs present |
| **System Prompt Quality** | Subjective, domain-specific | Code review by domain experts |
| **Tool Docstring Quality** | ADK introspects but doesn't validate quality | Code review for clarity |
| **A2A Protocol Usage** | Complex runtime interactions | Integration tests + manual testing |

---

## VIII. CI Workflow Integration

### Current CI Order (from `.github/workflows/ci.yml`)

```
1. drift-check (scripts/ci/check_nodrift.sh) - FIRST, blocks all if fails
   ├── Enforces R1, R2, R3, R8
   └── Detects alternative frameworks, Runner in services, credentials

2. arv-check (scripts/check_arv_minimum.py, check_arv_engine_flags.py)
   ├── Enforces baseline ARV requirements
   ├── Validates Agent Engine config
   └── Blocks downstream if fails

3. config-check (scripts/check_config_all.py)
   ├── Validates configuration defaults
   └── Warnings don't block

4. lint, test, security (parallel, only if above pass)

5. deploy (only if all pass, manual approval for prod)
```

### Planned CI Order (Post-S3)

```
1. drift-check (R8 enforcement - FIRST)

2. arv-spec-check (NEW - all R1-R7 checks)
   ├── check_arv_agents.py (R1)
   ├── check_arv_services.py (R3)
   ├── check_arv_docs.py (R6)
   ├── check_arv_config.py (Config defaults)
   ├── check_arv_memory.py (R5)
   ├── check_arv_spiffe.py (R7)
   └── Other ARV checks

3. config-check (existing, enhanced)

4. lint, test, security (parallel)

5. deploy (Agent Engine via ADK CLI)
```

---

## IX. Status Summary

### Coverage Overview

| Category | Implemented | ARV Check | Tests | Priority |
|----------|-------------|-----------|-------|----------|
| **R1: ADK-Only** | ✅ | ⚠️ Partial | ❌ | HIGH |
| **R2: Agent Engine** | ✅ | ✅ | ❌ | HIGH |
| **R3: Gateway Sep** | ✅ | ⚠️ Partial | ❌ | HIGH |
| **R4: CI-Only** | ✅ | ⚠️ Manual | ⚠️ Manual | MEDIUM |
| **R5: Dual Memory** | ✅ | ❌ | ❌ | MEDIUM |
| **R6: Single Docs** | ✅ | ❌ | ❌ | LOW |
| **R7: SPIFFE ID** | ⚠️ Partial | ❌ | ❌ | MEDIUM |
| **R8: Drift Check** | ✅ | ✅ | ❌ | CRITICAL |
| **Agent Construction** | ✅ | ❌ | ❌ | HIGH |
| **Tool System** | ✅ | ❌ | ❌ | MEDIUM |
| **A2A Protocol** | ✅ | ❌ | ❌ | MEDIUM |
| **File Layout** | ✅ | ❌ | ❌ | LOW |
| **Config Defaults** | ✅ | ⚠️ Partial | ❌ | HIGH |

### Key Gaps (To Address in S3)

**HIGH Priority:**
1. ❌ `scripts/check_arv_agents.py` - R1 enforcement (ADK-only agents)
2. ❌ `scripts/check_arv_services.py` - R3 enforcement (gateway separation)
3. ❌ `scripts/check_arv_config.py` - Config defaults enforcement
4. ❌ Unit tests for ARV scripts

**MEDIUM Priority:**
5. ❌ `scripts/check_arv_memory.py` - R5 validation (dual memory)
6. ❌ `scripts/check_arv_spiffe.py` - R7 validation (SPIFFE IDs)
7. ❌ Integration tests for memory and A2A
8. ⚠️ Complete SPIFFE ID implementation (R7)

**LOW Priority:**
9. ❌ `scripts/check_arv_docs.py` - R6 validation (doc structure)
10. ❌ `scripts/check_arv_structure.py` - File layout validation

---

## X. Related Documentation

**Source Spec:**
- `000-docs/6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md` - Canonical ADK/Agent Engine spec

**Implementation:**
- `.github/workflows/ci.yml` - CI workflow with ARV checks
- `scripts/ci/check_nodrift.sh` - Main drift detection (R8)
- `scripts/check_arv_*.py` - Individual ARV checks
- `agents/config/*.py` - Centralized configuration

**Future (S3):**
- `scripts/check_arv_agents.py` - To be created
- `scripts/check_arv_services.py` - To be created
- `scripts/check_arv_docs.py` - To be created
- `tests/unit/test_arv_*.py` - To be created

**Future (S4):**
- `000-docs/122-LS-SITR-adk-spec-alignment-and-arv-expansion.md` - SITREP

---

**Last Updated:** 2025-11-20
**Phase:** SPEC-ALIGN-ARV-EXPANSION (S2)
**Status:** Active (Repo-Local)
**Next Action:** S3 (Implement missing ARV scripts and tests)
