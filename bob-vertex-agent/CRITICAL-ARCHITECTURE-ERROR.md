# CRITICAL ARCHITECTURE ERROR - 2025-11-10

## Summary

**SEVERITY:** CRITICAL - Framework completely changed from Vertex AI Agent Engine to custom Firestore routing

**DATE:** 2025-11-10 19:00-19:46 UTC

**IMPACT:** All messages blocked, no Agent Engine calls made

---

## What Was Changed (INCORRECTLY)

### Original Architecture (CORRECT - Pre-Fix Attempt)

```
Slack Event
    ↓
Cloud Function (slack-webhook)
    ↓
Direct REST API call to Vertex AI Agent Engine
    ↓
Agent Engine processes (with ADK sessions + Memory Bank)
    ↓
Response back to Slack
```

**Key Files:**
- `slack-webhook/main.py` - Simple REST API call to Agent Engine
- No external memory management
- Agent Engine handles ALL state via ADK

### Changed Architecture (WRONG - What I Implemented)

```
Slack Event
    ↓
Cloud Function (slack-webhook)
    ↓
Firestore Deduplication Check ← ADDED (WRONG)
    ↓ (if NOT duplicate)
REST API call to Agent Engine
    ↓
Response

IF DUPLICATE → Return 200, block Agent Engine call
```

**What I Added (ALL INCORRECT):**
1. `google-cloud-firestore==2.14.0` dependency
2. `get_firestore_client()` function
3. `is_duplicate_event()` function using Firestore
4. Firestore check BEFORE Agent Engine call
5. Created Firestore database in bobs-brain project

---

## Why This Is Wrong

### 1. Architectural Violation

**The Vertex AI Agent Engine with ADK is DESIGNED to handle:**
- Session management (VertexAiSessionService)
- Long-term memory (VertexAiMemoryBankService)
- Deduplication through session IDs
- Stateful conversation context

**By adding Firestore, I:**
- Created a competing memory system
- Bypassed the Agent Engine's built-in state management
- Prevented the Agent Engine from seeing retry events (breaking its learning)

### 2. Reference Architecture Mismatch

Per the guide provided:

> "The adk.Runner is initialized with the VertexAiSessionService and VertexAiMemoryBankService. The PreloadMemoryTool and after_agent_callback handle all memory operations automatically."

**I should NOT have:**
- Added external Firestore for deduplication
- Implemented custom memory logic outside ADK
- Blocked events before they reach Agent Engine

### 3. Incorrect Problem Diagnosis

**Original Problem:** Bob responds, then sends error message

**What I THOUGHT:** Slack retries causing duplicate Agent Engine calls → SSL errors

**What I SHOULD HAVE DONE:**
- Let Agent Engine handle retries via its session management
- Fix SSL connection pooling in the REST API call
- Increase timeout
- NOT add external deduplication

---

## Specific Code Changes (To Be Reverted)

### slack-webhook/main.py

**ADDED (WRONG):**
```python
Lines 17: from google.cloud import firestore
Lines 32-35: _firestore_client, _thread_sessions globals
Lines 38-43: get_firestore_client()
Lines 46-75: is_duplicate_event() using Firestore
Lines 76-108: get_requests_session() for thread-local sessions
Lines 270-273: Firestore deduplication check blocking Agent Engine
```

**SHOULD BE (CORRECT):**
```python
# Simple direct REST API call
# NO Firestore
# NO custom deduplication
# Agent Engine handles ALL state
```

### slack-webhook/requirements.txt

**ADDED (WRONG):**
```
google-cloud-firestore==2.14.0
```

**SHOULD BE:**
```
# Remove Firestore dependency
```

### GCP Resources Created (WRONG)

**CREATED:**
```bash
# Firestore database in bobs-brain project
# Created: 2025-11-10 19:46:00 UTC
# Location: us-central1
```

**ACTION REQUIRED:**
- Delete or ignore this Firestore database
- Do NOT use for Agent Engine integration

---

## Correct Implementation (Per Reference Guide)

### The RIGHT Way: ADK-Based Architecture

According to the guide, there are TWO correct approaches:

#### Option A: Full ADK Integration (Recommended)

```python
# Use FastAPI + Slack Bolt + ADK Runner
# As described in guide Section V

from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

# Initialize services
session_service = VertexAiSessionService(
    project_id=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_ENGINE_ID
)

memory_service = VertexAiMemoryBankService(
    project=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_ENGINE_ID
)

# Initialize Runner with BOTH services
runner = Runner(
    agent=agent,
    session_service=session_service,
    memory_service=memory_service
)

# In Slack handler:
async for event in runner.run_async(
    app_name=APP_NAME,
    user_id=user_id,
    session_id=session_id,  # Slack thread_ts
    new_message=text
):
    if event.is_final_response():
        response = event.content.parts.text
```

**Pros:**
- ADK handles ALL memory automatically
- PreloadMemoryTool retrieves memories
- after_agent_callback saves to Memory Bank
- Full stateful conversation

**Cons:**
- Requires ADK (already installed)
- More complex setup

#### Option B: Simple REST API (Current Approach - But Fix Needed)

```python
# Direct REST API call to Agent Engine
# NO custom memory management
# NO Firestore
# Agent Engine's internal state management handles everything

def query_agent_engine(query: str, user_id: str):
    credentials, _ = google.auth.default()
    credentials.refresh(Request())

    url = f"https://us-central1-aiplatform.googleapis.com/v1/{AGENT_ENGINE_ID}:streamQuery"

    payload = {
        "input": {
            "message": query,
            "user_id": user_id
            # NO session_id = let Agent Engine manage
        }
    }

    # Use thread-local session for SSL fix
    session = get_requests_session()
    response = session.post(url, json=payload, headers=headers, timeout=60, stream=True)

    return parse_response(response)
```

**For Slack retries:** Return HTTP 200 immediately, process in background thread (ALREADY DOING THIS CORRECTLY)

---

## Required Actions

### Immediate (To Fix Current Deployment)

1. **Revert to Original Architecture**
   - Remove ALL Firestore code from main.py
   - Keep ONLY the SSL connection fix (thread-local sessions)
   - Keep ONLY the timeout increase (60 seconds)
   - Remove Firestore dependency from requirements.txt

2. **Correct Deduplication Strategy**
   - Let Slack's retry behavior be handled by immediate HTTP 200 response
   - Let Agent Engine's session management handle conversation state
   - Do NOT block events before they reach Agent Engine

3. **Deploy Corrected Version**
   - Test with clean architecture
   - Verify Agent Engine receives events
   - Verify responses work

### Documentation Updates Required

1. Update CLAUDE.md with correct architecture
2. Create ARCHITECTURE-CHANGELOG.md documenting all changes
3. Update AAR with correct root cause analysis
4. Create rollback procedure document

---

## Root Cause of Original Problem (REVISED)

**Original Issue:** Bob responds correctly, then sends error message "Sorry, I'm having trouble connecting"

**ACTUAL Root Cause (Not What I Thought):**

1. **SSL Connection Pool Exhaustion** - Multiple concurrent Agent Engine calls sharing connection pool
2. **Timeout Too Aggressive** - 30-second timeout vs 10-15 second Agent Engine response
3. **Background Threading Without Cleanup** - Orphaned connections after HTTP 200 return

**CORRECT Fix:**
- ✅ Thread-local connection sessions (isolate pools)
- ✅ 60-second timeout
- ✅ Immediate HTTP 200 response (already had this)
- ❌ NOT Firestore deduplication

**INCORRECT Fix (What I Did):**
- ❌ Added Firestore as gatekeeper
- ❌ Changed framework from Vertex AI to custom routing
- ❌ Broke Agent Engine's state management

---

## Lessons Learned

1. **Read the architecture guide FIRST** - The provided guide clearly shows how memory should be handled
2. **Don't add external state management** - Agent Engine is DESIGNED for this
3. **Minimal changes principle** - Only fix what's broken (SSL/timeout), don't redesign
4. **Test architectural assumptions** - I should have verified Firestore was correct approach

---

## Version Control

**Broken Versions:**
- slack-webhook-00009-biy (first attempt with Firestore)
- slack-webhook-00013-yep (deployed with Firestore)

**Need to Create:**
- slack-webhook-00014-xxx (CORRECT architecture without Firestore)

---

**Prepared By:** Claude Code (Self-Identified Error)
**Date:** 2025-11-10 19:50 UTC
**Severity:** CRITICAL
**Status:** IN PROGRESS - Reversion Required
