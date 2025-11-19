# Bob's Brain: Using `.run_debug()` - Simplified Testing Pattern

**Date:** 2025-11-19
**Source:** Kaggle 5-Day AI Agents Course + ADK Python API Reference
**Purpose:** Simplify local testing with `.run_debug()` method
**Status:** Implementation Guide

---

## Executive Summary

The `.run_debug()` method provides a **simplified way to test agents locally** without manually managing sessions, user IDs, and event handling.

**Key Benefits:**
- ✅ No manual session management
- ✅ Automatic user_id and session_id defaults
- ✅ Returns all events for debugging
- ✅ Perfect for rapid iteration during development

**Important:** This is for **LOCAL TESTING ONLY** - Vertex AI Agent Engine deployment still uses the standard `Runner` pattern.

---

## Current Implementation (Production)

**What Bob Uses Now (Correct for Vertex Engine):**

```python
# my_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

def create_runner() -> Runner:
    """Create Runner with Vertex AI services (for Agent Engine)."""

    agent = get_agent()

    # Manual service wiring (required for production)
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

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )

    return runner
```

**Status:** ✅ **This is CORRECT for Vertex AI Agent Engine deployment**

---

## Simplified Pattern: `.run_debug()` for Local Testing

**Google's Recommended Pattern (from Kaggle 5-Day Course):**

```python
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner

# Create agent
agent = LlmAgent(
    name="Bob",
    model="gemini-2.0-flash-exp",
    tools=[search_web, get_current_time],
    instruction="You are Bob, a helpful assistant."
)

# Simple runner (in-memory, for local testing)
runner = InMemoryRunner(agent=agent)

# Test with run_debug() - simplified!
response = await runner.run_debug("What time is it in Tokyo?")
```

**What `.run_debug()` Does:**
- ✅ Automatically uses `user_id='debug_user_id'`
- ✅ Automatically uses `session_id='debug_session_id'`
- ✅ Returns all events (not just final response)
- ✅ Perfect for debugging tool calls, agent reasoning, etc.

---

## `.run_debug()` Method Signature

```python
async def run_debug(
    self,
    user_messages: str | list[str],
    *,
    user_id: str = 'debug_user_id',
    session_id: str = 'debug_session_id',
    run_config: RunConfig | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> list[Event]:
    """
    Execute in debug mode (returns collected events).

    Args:
        user_messages: Single message or list of messages.
        user_id: Debug user ID (default: 'debug_user_id').
        session_id: Debug session ID (default: 'debug_session_id').
        run_config: Execution configuration.
        quiet: Suppress output (default: False).
        verbose: Enable verbose logging (default: False).

    Returns:
        list[Event]: All conversation events.
    """
```

---

## Comparison: Production vs Local Testing

### Production Pattern (Vertex AI Agent Engine)

```python
# my_agent/agent_engine_app.py

from my_agent.agent import create_runner

# Export Runner with Vertex AI services
app = create_runner()

# Agent Engine calls:
# - app.run_async() for async execution
# - app.run_live() for streaming
```

**Characteristics:**
- ✅ Uses VertexAiSessionService (persistent sessions)
- ✅ Uses VertexAiMemoryBankService (long-term memory)
- ✅ Real session management
- ✅ Production-grade persistence
- ✅ Deployed to Vertex AI Agent Engine

---

### Local Testing Pattern (InMemoryRunner + run_debug)

```python
# scripts/test_local.py

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from my_agent.tools import search_web, get_current_time

async def test_bob():
    """Test Bob locally with run_debug()."""

    # Create agent
    agent = LlmAgent(
        name="Bob",
        model="gemini-2.0-flash-exp",
        tools=[search_web, get_current_time],
        instruction="You are Bob, a helpful assistant."
    )

    # Simple in-memory runner
    runner = InMemoryRunner(agent=agent)

    # Test with run_debug()
    print("Testing Bob locally...")
    events = await runner.run_debug(
        "What's the current time in Tokyo?",
        verbose=True  # See detailed logs
    )

    # Inspect events
    for event in events:
        print(f"Event: {event.type}")
        if event.content:
            print(f"Content: {event.content}")

    await runner.close()

# Run test
import asyncio
asyncio.run(test_bob())
```

**Characteristics:**
- ✅ No manual session management
- ✅ InMemorySessionService (auto-wired)
- ✅ InMemoryMemoryService (auto-wired)
- ✅ Fast iteration
- ⚠️ Data lost on restart (in-memory only)
- ❌ NOT for production

---

## When to Use Each Pattern

### Use Production Pattern (Current Implementation) When:

- ✅ Deploying to Vertex AI Agent Engine
- ✅ Need persistent sessions across restarts
- ✅ Need long-term memory (Memory Bank)
- ✅ Production workloads
- ✅ Real users

**Files:** `my_agent/agent.py`, `my_agent/agent_engine_app.py`

---

### Use `.run_debug()` Pattern When:

- ✅ Local development and testing
- ✅ Debugging tool calls
- ✅ Experimenting with prompts
- ✅ Quick iteration
- ✅ Testing before deployment

**Files:** `scripts/test_local.py`, `tests/integration/`

---

## Recommended Project Structure

### Production Code (DO NOT CHANGE)

```
my_agent/
├── agent.py              # Uses Runner + Vertex services ✅
└── agent_engine_app.py   # Exports app = create_runner() ✅
```

**Status:** ✅ **Keep as-is for Vertex AI Agent Engine**

---

### Add Local Testing Scripts (NEW)

```
scripts/
├── test_local.py         # Uses InMemoryRunner + run_debug()
└── test_tools.py         # Test individual tools
```

**Example: `scripts/test_local.py`**

```python
"""
Local testing script for Bob's Brain using run_debug().

Usage:
    python scripts/test_local.py
"""

import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from my_agent.tools import search_web, get_current_time


async def test_agent():
    """Test Bob's Brain locally."""

    # Create agent (simplified - no dual memory needed for testing)
    agent = LlmAgent(
        name="Bob",
        model="gemini-2.0-flash-exp",
        tools=[search_web, get_current_time],
        instruction="""You are Bob, a helpful assistant.

You have access to:
- search_web: Search the web for information
- get_current_time: Get current time in any timezone

Use these tools when appropriate."""
    )

    # Create in-memory runner
    runner = InMemoryRunner(agent=agent, app_name="bobs-brain")

    # Test queries
    test_queries = [
        "What's the current time in Tokyo?",
        "Search the web for Google ADK documentation",
        "Hello, who are you?"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")

        # Use run_debug() for detailed output
        events = await runner.run_debug(
            query,
            verbose=True  # Show detailed logs
        )

        # Print final response
        for event in events:
            if event.content and event.is_final_response():
                print(f"\nBob: {event.content}")

    # Cleanup
    await runner.close()
    print("\n✅ Testing complete!")


if __name__ == "__main__":
    asyncio.run(test_agent())
```

---

## Testing with `.run_debug()`

### Basic Usage

```python
# Single message
events = await runner.run_debug("Hello!")

# Multiple messages (conversation)
events = await runner.run_debug([
    "What's 2+2?",
    "And what's double that?"
])

# With verbose logging
events = await runner.run_debug(
    "Search for ADK docs",
    verbose=True
)

# Custom session ID (for testing session persistence)
events = await runner.run_debug(
    "Remember this: my name is Alice",
    session_id="test-session-123"
)
```

---

### Inspecting Events

```python
events = await runner.run_debug("What time is it?", verbose=True)

for event in events:
    print(f"Event type: {event.type}")

    # Check for tool calls
    if event.type == "tool_call":
        print(f"  Tool: {event.tool_name}")
        print(f"  Args: {event.tool_args}")

    # Check for tool results
    if event.type == "tool_result":
        print(f"  Result: {event.content}")

    # Check for final response
    if event.is_final_response():
        print(f"  Final: {event.content}")
```

---

### Testing Multi-Turn Conversations

```python
# InMemoryRunner maintains session state
runner = InMemoryRunner(agent=agent)

# Turn 1
await runner.run_debug("My name is Bob", session_id="test-123")

# Turn 2 (same session)
events = await runner.run_debug("What's my name?", session_id="test-123")
# Should respond: "Your name is Bob"
```

---

## Integration Testing Pattern

**Example: `tests/integration/test_agent_tools.py`**

```python
"""Integration tests for Bob's Brain tools."""

import pytest
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from my_agent.tools import search_web, get_current_time


@pytest.mark.asyncio
async def test_time_tool():
    """Test get_current_time tool."""

    agent = LlmAgent(
        name="Bob",
        model="gemini-2.0-flash-exp",
        tools=[get_current_time],
        instruction="Use get_current_time when asked about time."
    )

    runner = InMemoryRunner(agent=agent)

    events = await runner.run_debug("What time is it in New York?")

    # Verify tool was called
    tool_calls = [e for e in events if e.type == "tool_call"]
    assert len(tool_calls) > 0, "Tool should be called"
    assert tool_calls[0].tool_name == "get_current_time"

    # Verify response contains time
    final = [e for e in events if e.is_final_response()][0]
    assert "time" in final.content.lower()

    await runner.close()


@pytest.mark.asyncio
async def test_search_tool():
    """Test search_web tool."""

    agent = LlmAgent(
        name="Bob",
        model="gemini-2.0-flash-exp",
        tools=[search_web],
        instruction="Use search_web when asked to search."
    )

    runner = InMemoryRunner(agent=agent)

    events = await runner.run_debug("Search for Google ADK documentation")

    # Verify tool was called
    tool_calls = [e for e in events if e.type == "tool_call"]
    assert len(tool_calls) > 0, "Search tool should be called"
    assert tool_calls[0].tool_name == "search_web"

    await runner.close()
```

---

## Benefits of `.run_debug()`

### 1. Rapid Development

**Before (manual setup):**
```python
from google.adk import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
runner = Runner(agent=agent, session_service=session_service)
response = await runner.run_async(
    user_messages="Hello",
    user_id="test-user",
    session_id="test-session"
)
```

**After (with run_debug):**
```python
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent)
events = await runner.run_debug("Hello")
```

**Lines of code:** 6 → 2 (67% reduction!)

---

### 2. Better Debugging

```python
# Get ALL events, not just final response
events = await runner.run_debug("Search for X", verbose=True)

# Inspect tool execution
for event in events:
    if event.type == "tool_call":
        print(f"Calling: {event.tool_name}({event.tool_args})")
    if event.type == "tool_result":
        print(f"Result: {event.content}")
```

---

### 3. Testing Without Infrastructure

- ✅ No GCP credentials needed
- ✅ No Agent Engine ID needed
- ✅ No PROJECT_ID needed
- ✅ Works offline (no external services)

---

## Important: When NOT to Use `.run_debug()`

### ❌ DO NOT Use in Production

```python
# ❌ BAD - Don't use in agent_engine_app.py
from google.adk.runners import InMemoryRunner

app = InMemoryRunner(agent=agent)  # ❌ Data lost on restart!
```

**Why:**
- InMemoryRunner loses all data on restart
- No persistent sessions
- No Memory Bank
- Not suitable for real users

### ✅ DO Use Current Pattern

```python
# ✅ GOOD - Keep in agent_engine_app.py
from my_agent.agent import create_runner

app = create_runner()  # Uses VertexAiSessionService + MemoryBankService
```

---

## Summary

### Current Bob's Brain Implementation ✅

**Production (my_agent/):**
- ✅ Runner with VertexAiSessionService
- ✅ VertexAiMemoryBankService
- ✅ Deployed to Agent Engine
- ✅ **DO NOT CHANGE**

### New Capability: Local Testing 🆕

**Add (scripts/):**
- 🆕 InMemoryRunner for testing
- 🆕 `.run_debug()` for quick iteration
- 🆕 Integration tests with pytest

---

## Action Items

**To add `.run_debug()` testing capability:**

1. **Create `scripts/test_local.py`** (shown above)
2. **Add to `.gitignore`:**
   ```
   scripts/__pycache__/
   ```
3. **Test locally:**
   ```bash
   python scripts/test_local.py
   ```
4. **Keep production code unchanged** ✅

---

## References

- **Kaggle 5-Day AI Agents Course:** https://www.kaggle.com/learn-guide/5-day-agents
- **ADK Python API Reference:** `000-docs/google-reference/adk/GOOGLE_ADK_PYTHON_API_REFERENCE.md`
- **InMemoryRunner Docs:** Lines 1-30 in API reference
- **run_debug() Method:** Lines 150-170 in API reference

---

**Document Status:** Complete ✅
**Last Updated:** 2025-11-19
**Category:** Architecture & Technical - Code Pattern
**Implementation Priority:** P2 (Nice to have for development, not blocking deployment)

---
