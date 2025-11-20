# 6767-093-DR-STND-bob-rag-readiness-standard.md

**Date Created:** 2025-11-20
**Category:** DR - Documentation & Reference
**Type:** STND - Standard
**Status:** ENFORCEMENT READY ✅

---

## Executive Summary

This document defines the **RAG Readiness Standard** for Bob and the foreman (iam-senior-adk-devops-lead) in the Bob's Brain ADK department. It establishes the contract that must be met before RAG capabilities are considered production-ready and forms part of the broader Agent Readiness Verification (ARV) gate.

---

## RAG Readiness Criteria

### 1. Configuration Requirements ✓

**Environment Variables:**
- [ ] `VERTEX_SEARCH_PROJECT_ID` or fallback to `PROJECT_ID`
- [ ] `VERTEX_SEARCH_LOCATION` (default: "us")
- [ ] `USE_ORG_KNOWLEDGE` flag defined (true/false)
- [ ] `APP_ENV` or `ENVIRONMENT` for env detection

**Configuration Files:**
- [ ] `config/vertex_search.yaml` exists and is valid YAML
- [ ] Contains `environments` section with at least:
  - `production` configuration
  - `staging` configuration
- [ ] Each environment defines:
  - `datastore.id`
  - `datastore.project_id`
  - `datastore.location`
  - `source.uri_pattern`

**Environment Mapping Rules:**
- [ ] "prod"/"production" → production datastore
- [ ] "dev"/"development" → development datastore
- [ ] Default/other → staging datastore (safe default)

### 2. Code Requirements ✓

**Tool Factory Module:**
- [ ] `agents/shared_tools/vertex_search.py` exists
- [ ] Exports `get_bob_vertex_search_tool(env)`
- [ ] Exports `get_foreman_vertex_search_tool(env)`
- [ ] Exports `get_current_environment()`
- [ ] Exports `get_datastore_info(env)`

**Tool Integration:**
- [ ] Bob's profile includes Vertex Search tool
- [ ] Foreman's profile includes Vertex Search tool
- [ ] Tools handle missing config gracefully (return None/stub)
- [ ] No hardcoded datastore IDs in code

**Import Validation:**
```python
# Must succeed without errors:
from agents.shared_tools.vertex_search import (
    get_bob_vertex_search_tool,
    get_foreman_vertex_search_tool
)
from agents.shared_tools import BOB_TOOLS, FOREMAN_TOOLS
```

### 3. Documentation Requirements ✓

**Architecture Docs:**
- [ ] Knowledge hub doc exists: `6767-*-org-knowledge-hub-*.md`
- [ ] References bucket structure
- [ ] Defines prefix isolation
- [ ] Describes datastore concept

**Integration Docs:**
- [ ] RAG integration doc exists: `6767-*-bob-rag-*.md`
- [ ] Describes when Bob uses search
- [ ] Describes when foreman uses search
- [ ] Includes setup commands

**This Standard:**
- [ ] RAG readiness standard: `6767-093-DR-STND-bob-rag-readiness-standard.md`

### 4. Validation Requirements ✓

**Dry-run Script:**
- [ ] `scripts/print_rag_config.py` exists
- [ ] Shows current configuration without API calls
- [ ] Provides setup commands for datastores
- [ ] Works in all environments

**Readiness Check:**
- [ ] `scripts/check_rag_readiness.py` exists
- [ ] Validates all criteria above
- [ ] Returns clear pass/fail status
- [ ] No network calls required

**CI Integration:**
- [ ] GitHub Actions workflow exists
- [ ] Runs on PR and push to main
- [ ] Can be made blocking when ready

---

## RAG Readiness and ARV

### Relationship to Agent Readiness Verification

RAG readiness is **one sub-gate** of the broader ARV system:

```
Agent Readiness Verification (ARV)
├── Schema Validation
├── Golden Tests
├── RAG Readiness (this standard) ✅
├── Memory Wiring
├── A2A Protocol Compliance
└── Deployment Sanity
```

### Gate Enforcement Levels

| Level | Description | CI Behavior | When to Use |
|-------|-------------|-------------|-------------|
| **0 - Info** | Log results only | Never fails | Initial development |
| **1 - Soft** | Warn on failure | Non-blocking | Testing phase |
| **2 - Hard** | Block on failure | Blocking | Production ready |

Current Level: **1 - Soft** (can be upgraded via CI config)

---

## Running RAG Readiness Checks

### Local Development
```bash
# Quick check
make check-rag-readiness

# Verbose output
python scripts/check_rag_readiness.py --verbose

# Check specific environment
APP_ENV=production make check-rag-readiness
```

### CI Pipeline
```yaml
# Automatically runs on:
- Pull requests to main
- Pushes to main
- Manual trigger

# Job: rag-readiness
# Workflow: .github/workflows/ci-rag-readiness.yaml
```

### Expected Output (Pass)
```
RAG READINESS CHECK
==================
✅ Configuration: VALID
✅ Code: READY
✅ Documentation: COMPLETE
✅ Validation: PASSING

RAG READY: YES
```

### Expected Output (Fail)
```
RAG READINESS CHECK
==================
✅ Configuration: VALID
❌ Code: MISSING TOOLS
✅ Documentation: COMPLETE
❌ Validation: FAILED

RAG READY: NO

Missing Requirements:
- Vertex Search tool not in Bob's profile
- check_rag_readiness.py not found
```

---

## Compliance Checklist

Use this checklist before declaring RAG production-ready:

### Pre-Production
- [ ] All configuration files present
- [ ] Environment variables documented
- [ ] Tool factory tested locally
- [ ] Dry-run script working
- [ ] Readiness check passing
- [ ] CI workflow green

### Production Deployment
- [ ] Datastores created in Vertex AI
- [ ] Knowledge imported to buckets
- [ ] Service accounts configured
- [ ] IAM permissions granted
- [ ] Migration flag tested
- [ ] Rollback plan documented

### Post-Deployment
- [ ] Search latency < 500ms
- [ ] Results relevant
- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] Usage tracked
- [ ] Feedback collected

---

## Enforcement Timeline

| Date | Milestone | Action |
|------|-----------|--------|
| 2025-11-20 | Standard Created | This document |
| 2025-11-21 | Local Checks | `check_rag_readiness.py` |
| 2025-11-22 | CI Integration | Non-blocking workflow |
| 2025-11-25 | Soft Enforcement | Warning on failure |
| 2025-12-01 | Hard Enforcement | Blocking on failure |

---

## Exceptions and Overrides

### Temporary Bypass
```bash
# Skip RAG checks (emergency only)
SKIP_RAG_CHECKS=true make deploy
```

### Permanent Exemption
Must be documented in:
- This standard (with justification)
- `.github/workflows/ci-rag-readiness.yaml`
- Team decision log

---

## Related Documents

- `6767-091-AT-ARCH-org-knowledge-hub-gcs-vertex-search.md`
- `6767-092-AT-ARCH-bob-rag-and-vertex-search-integration.md`
- `CLAUDE.md` - RAG Readiness Check section

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-20
**Status:** Ready for Enforcement
**Owner:** ADK Department Build Captain

---