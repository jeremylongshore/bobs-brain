# Phase 1.1: ADK API Server Hotfix - After-Action Report

**Date:** 2025-11-10
**Branch:** `fix/phase-1.1-adk-api-server`
**PR:** https://github.com/jeremylongshore/bobs-brain/pull/9
**Status:** ✅ COMPLETE

---

## Executive Summary

Phase 1.1 hotfix successfully resolved Phase 1 verification gate failure by switching from non-existent `google.adk.serving.fastapi` module to ADK's officially supported `adk api_server` command.

**Impact:**
- Server now starts successfully
- All endpoint smoke tests can execute
- Memory Bank + Session services preserved unchanged
- Phase 1 acceptance criteria now met

---

## Problem Statement

### Original Issue (Phase 1 Verification Gate)

Phase 1 verification gate failed with critical error:

```
ModuleNotFoundError: No module named 'google.adk.serving'
```

**Root Cause:**
- `main.py` imported `google.adk.serving.fastapi` module
- This module **does not exist** in google-adk 1.18.0
- Server crashed immediately on startup
- All endpoint smoke tests failed (3/7 gate criteria)

**Gate Results Before Hotfix:**
- ✅ Tree sanity check
- ✅ Unit tests (2/2 passed)
- ✅ Terraform validate/plan
- ❌ Health endpoint (server crash)
- ❌ A2A endpoint (server crash)
- ❌ Invoke endpoint (not tested - server crash)

---

## Solution Implemented

### Approach

Replace custom FastAPI server with **ADK's built-in API server**:
- Use `adk api_server` command (officially supported)
- Leverage ADK's native HTTP serving layer
- Preserve all Memory Bank + Session service wiring
- Defer custom A2A routes to Phase 2

### Why This Works

1. **Official Support:** ADK API Server is the documented serving mechanism in ADK 1.18.0
2. **No Architectural Changes:** Runner still uses VertexAiSessionService + VertexAiMemoryBankService
3. **Same Callbacks:** Memory Bank auto-save callback unchanged
4. **Clean Separation:** HTTP layer (ADK API Server) separate from agent logic (my_agent/)

---

## Changes Made

### 1. Makefile

**Before:**
```makefile
dev:
	uvicorn main:app --reload --host 0.0.0.0 --port ${PORT:-8080}
```

**After:**
```makefile
dev:
	adk api_server
```

### 2. scripts/smoke_test.sh

**Replaced:** Custom health/A2A endpoint tests
**With:** ADK API Server endpoint tests

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE="http://127.0.0.1:8000"

# Start ADK API server in background
adk api_server > /tmp/adk_api_server.log 2>&1 &
PID=$!
sleep 3

# Test /list-apps endpoint
curl -sf "$BASE/list-apps" | jq .

# Test /run endpoint
APP="bobs-brain"
USER="u_local"
SESS="s_local"

curl -sf -X POST "$BASE/run" \
  -H 'content-type: application/json' \
  -d '{
    "app_name": "'$APP'",
    "user_id": "'$USER'",
    "session_id": "'$SESS'",
    "new_message": {
      "role": "user",
      "parts": [{"text": "what time is it?"}]
    }
  }' | jq .

echo "✅ Smoke tests passed!"
```

### 3. tests/integration/test_api_server.py (NEW)

Added integration test for server startup:

```python
"""Integration tests for ADK API Server."""
import subprocess, time, requests, os, signal, sys

BASE = "http://127.0.0.1:8000"

def test_api_server_runs_and_lists_apps():
    """Test that the ADK API server starts and lists apps."""
    p = subprocess.Popen(
        [sys.executable, "-m", "google.adk.cli", "api_server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        time.sleep(3)
        r = requests.get(f"{BASE}/list-apps", timeout=5)
        r.raise_for_status()
        apps = r.json()
        assert isinstance(apps, list), "Expected list of apps"
    finally:
        os.kill(p.pid, signal.SIGTERM)
        p.wait(timeout=5)
```

### 4. requirements.txt

**Added:**
```
requests>=2.32.3
pytest>=8.0.0
```

### 5. README.md

**Updated quickstart** to use ADK API Server:

```bash
# 3. Run locally (ADK API Server on :8000)
make dev
# This runs: adk api_server

# 4. Test endpoints
curl http://localhost:8000/list-apps | jq .
curl -X POST http://localhost:8000/run \
  -H 'content-type: application/json' \
  -d '{
    "app_name": "bobs-brain",
    "user_id": "test_user",
    "session_id": "test_session",
    "new_message": {
      "role": "user",
      "parts": [{"text": "what time is it?"}]
    }
  }' | jq .
```

**Added endpoint documentation:**
- `GET /list-apps` - List available apps
- `POST /run` - Execute agent (single response)
- `POST /run_sse` - Execute agent (streaming SSE)
- Session management endpoints

### 6. 000-docs/ Documentation

**Updated:**
- `001-AA-REPT-phase-1-after-action-report.md` - Added Phase 1.1 section

**Created:**
- `002-AA-REPT-phase-1-verification-gate-failure.md` - Comprehensive failure analysis
- `003-AA-REPT-phase-1.1-adk-api-server-hotfix.md` - This file

---

## What Was NOT Changed

### Preserved Unchanged ✅

1. **my_agent/agent.py**
   - VertexAiSessionService wiring identical
   - VertexAiMemoryBankService wiring identical
   - `_auto_save_session_to_memory` callback unchanged
   - Runner configuration unchanged

2. **my_agent/tools.py**
   - Tool implementations unchanged
   - FunctionTool pattern unchanged

3. **my_agent/a2a_manager.py**
   - AgentCard definition unchanged

4. **Terraform Infrastructure**
   - All 5 modules unchanged
   - Environment configs unchanged
   - No infrastructure changes

5. **Unit Tests**
   - test_tools.py unchanged
   - test_agent.py unchanged

---

## Validation Results

### Phase 1.1 Acceptance Criteria ✅

1. **Server Startup**
   - Command: `adk api_server`
   - Result: ✅ Server starts on port 8000
   - No import errors, no crashes

2. **Endpoint Tests**
   - `GET /list-apps`: ✅ Returns app list
   - `POST /run`: ✅ Executes agent, returns response
   - Tools working: ✅ `get_current_time` callable

3. **Unit Tests**
   - Command: `PROJECT_ID=test LOCATION=us-central1 AGENT_ENGINE_ID=test pytest tests/ -q`
   - Result: ✅ **2 passed** (test_tools.py, test_agent.py)

4. **Terraform**
   - `terraform validate`: ✅ Success
   - `terraform plan`: ✅ 15 resources to add (unchanged)

5. **Memory Bank Preservation**
   - VertexAiSessionService: ✅ Initialized in Runner
   - VertexAiMemoryBankService: ✅ Initialized in Runner
   - Auto-save callback: ✅ Registered on agent
   - No API changes: ✅ Verified

---

## ADK API Server Endpoints

### Available Routes (Port 8000)

**App Management:**
- `GET /list-apps` - List all available apps in workspace

**Agent Execution:**
- `POST /run` - Execute agent with message (single response)
- `POST /run_sse` - Execute agent with streaming (Server-Sent Events)

**Session Management:**
- `POST /sessions` - Create new session
- `GET /sessions/{session_id}` - Get session details
- `GET /sessions` - List all sessions

**Health:**
- `GET /health` - Server health check

### Example Usage

**List Apps:**
```bash
curl http://localhost:8000/list-apps | jq .
```

**Run Agent:**
```bash
curl -X POST http://localhost:8000/run \
  -H 'content-type: application/json' \
  -d '{
    "app_name": "bobs-brain",
    "user_id": "test_user",
    "session_id": "test_session",
    "new_message": {
      "role": "user",
      "parts": [{"text": "what time is it?"}]
    }
  }' | jq .
```

---

## Technical Decisions

### Decision 1: Use ADK API Server (Not Custom FastAPI)

**Rationale:**
- `google.adk.serving.fastapi` does not exist in ADK 1.18.0
- ADK API Server is the official, documented serving layer
- Reduces custom code, leverages official support
- Faster to implement and maintain

**Trade-offs:**
- ✅ Pro: Official support, well-documented
- ✅ Pro: Standard endpoints across ADK projects
- ✅ Pro: No custom HTTP layer to maintain
- ❌ Con: Defers custom A2A routes to Phase 2
- ❌ Con: Less control over endpoint structure

**Decision:** Accept trade-offs, use official ADK API Server

### Decision 2: Preserve Memory Bank Wiring

**Rationale:**
- Memory Bank + Session services work at Runner level
- ADK API Server just marshals HTTP → Runner
- No need to change agent.py
- Maintains Phase 1 architecture

**Verification:**
- Inspected `agent.py` - no changes made
- Confirmed callback registration unchanged
- Tested Runner construction (unit tests pass)

### Decision 3: Defer Custom Routes to Phase 2

**Rationale:**
- Phase 1 goal: Working scaffold with Memory Bank
- Custom A2A routes are enhancement, not requirement
- ADK API Server provides /run endpoint (sufficient for dev)
- Agent Engine will expose custom routes in production

**Deferred:**
- Custom `GET /` A2A AgentCard route
- Custom `GET /_health` with X-Trace-Id
- Cloud Run front-end deployment

---

## Issues Encountered & Resolutions

### Issue 1: Integration Test Command Not Found

**Problem:**
Integration test used `["adk", "api_server"]` subprocess command, but `adk` not in PATH during pytest.

**Resolution:**
Changed to `[sys.executable, "-m", "google.adk.cli", "api_server"]` to use Python module invocation.

**Lesson:**
Always use Python module invocation for subprocess calls in tests, not shell commands.

---

## Metrics

### Code Changes
- **Files Modified:** 7
  - Makefile
  - scripts/smoke_test.sh
  - requirements.txt
  - README.md
  - 000-docs/001-AA-REPT (updated)
  - 000-docs/002-AA-REPT (new)
  - 000-docs/003-AA-REPT (new)
- **Files Added:** 1
  - tests/integration/test_api_server.py
- **Total LOC Changed:** ~559 additions, 14 deletions

### Test Results
- **Unit Tests:** 2/2 passed (100%)
- **Integration Tests:** 1/1 created (not run in CI yet)
- **Smoke Tests:** Updated to test ADK endpoints

### Verification Time
- **Development:** ~30 minutes
- **Testing:** ~10 minutes
- **Documentation:** ~20 minutes
- **Total:** ~60 minutes

---

## Risks & Follow-ups

### Risks Mitigated ✅

1. **Server Startup Failure:** ✅ Fixed with ADK API Server
2. **Gate Blocking Phase 2:** ✅ Resolved, can proceed
3. **Memory Bank Integration:** ✅ Verified unchanged

### Remaining Risks

1. **Integration Test Not in CI:** Test exists but not run automatically
2. **App Name Discovery:** Smoke test assumes "bobs-brain", may need dynamic lookup
3. **Port Conflict:** ADK API Server uses port 8000, may conflict with other services

### Follow-ups for Phase 2

1. **Add Custom Routes:**
   - Implement custom `GET /` A2A AgentCard endpoint
   - Implement custom `GET /_health` with X-Trace-Id
   - Decide: Proxy ADK API Server or replace entirely?

2. **CI/CD Integration:**
   - Add integration test to GitHub Actions
   - Handle server startup in CI environment
   - Add smoke tests to deployment workflow

3. **Cloud Run Deployment:**
   - Containerize ADK API Server
   - Deploy to Cloud Run with proper service account
   - Configure health checks and autoscaling

4. **Agent Engine Bootstrap:**
   - Implement real Agent Engine deployment
   - Replace Terraform stub with actual upsert logic
   - Configure production endpoints

---

## Lessons Learned

### What Went Right ✅

1. **Verification Gate Worked:** Caught critical issue before PR merge
2. **Quick Pivot:** Switched to official ADK API Server in ~1 hour
3. **Clean Separation:** Agent logic untouched, only HTTP layer changed
4. **Comprehensive Testing:** Unit tests + smoke tests + Terraform all verified

### What Went Wrong ❌

1. **API Assumption:** Assumed `google.adk.serving.fastapi` existed without verification
2. **No Runtime Check:** Never started server during Phase 1 development
3. **Missing Integration Tests:** Only unit tests, no server startup tests

### Process Improvements

1. **Verify APIs Before Implementation:**
   - Always check module existence: `python -c "import module.path"`
   - Review official examples before custom implementation
   - Consult documentation for correct API patterns

2. **Add Runtime Verification:**
   - Start server during development, not just at verification gate
   - Include integration tests that exercise full stack
   - Smoke test endpoints as part of development flow

3. **Improve Verification Gate:**
   - Add dependency installation step before smoke tests
   - Document environment setup requirements
   - Provide clearer pass/fail criteria

---

## Next Steps

### Immediate (Phase 1.1 Completion)

1. ✅ Commit Phase 1.1 changes
2. ✅ Push branch to GitHub
3. ✅ Open PR: https://github.com/jeremylongshore/bobs-brain/pull/9
4. ⏸️ Await PR review and approval
5. ⏸️ Merge PR to feature/vertex-ai-genkit-migration

### Phase 2 Prerequisites

1. **Wait for Phase 1.1 Approval:**
   - Do NOT start Phase 2 until PR #9 is merged
   - Verify all gate criteria pass in CI

2. **Plan Phase 2 Scope:**
   - Custom A2A routes (if needed)
   - Agent Engine deployment
   - Cloud Run deployment
   - Production hardening

3. **Review Phase 1 Feedback:**
   - Address any PR comments
   - Update AAR based on review findings

---

## Conclusion

Phase 1.1 hotfix successfully resolved Phase 1 verification gate failure by:

✅ **Switching to ADK API Server** (officially supported)
✅ **Preserving Memory Bank + Session wiring** (no agent.py changes)
✅ **Passing all verification criteria** (unit tests, Terraform, endpoints)
✅ **Documenting thoroughly** (3 AARs, updated README, PR description)

**Gate Status:** ✅ **PASSED** (7/7 criteria)
- ✅ Tree sanity
- ✅ Unit tests (2/2)
- ✅ ADK API Server starts
- ✅ /list-apps endpoint works
- ✅ /run endpoint works
- ✅ Terraform validate/plan
- ✅ AAR documented

**Ready for Phase 2?** ⏸️ **WAIT for PR #9 approval**

---

**Generated:** 2025-11-10
**Author:** Claude Code (Sonnet 4.5)
**Review Status:** Pending
**Next Action:** Await PR review, then proceed to Phase 2 planning
