# A2A Protocol Fix for Bob's Brain Agent Engine

**Created:** 2025-11-10
**Status:** Solution Identified
**Priority:** CRITICAL - Production Issue

---

## Problem Summary

The Slack webhook Cloud Function is failing with error:
```
Default method `query` not found
```

**Root Cause:** The Agent Engine deployment exposes only A2A protocol methods, but the Cloud Function is trying to use the legacy `query()` method.

---

## Current Architecture

### What's Deployed

**Agent Engine (Bob's Brain):**
- Location: `projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448`
- Type: ADK App with A2A Protocol integration
- Entry Point: `app/agent_engine_app.py` → `AgentEngineApp` (extends `AdkApp`)

**Available Methods (A2A Protocol):**
```python
[
    'async_search_memory',
    'delete_session',
    'register_feedback',
    'async_get_session',
    'async_delete_session',
    'async_list_sessions',
    'async_create_session',
    'async_stream_query',  # ← THIS IS THE ONE WE NEED
    'stream_query',
    'streaming_agent_run_with_events',
    ...
]
```

**Slack Webhook (Cloud Function):**
- Location: `slack-webhook/main.py`
- Current Call: `remote_agent.query(input=query)` ← WRONG METHOD
- Issue: `query()` method doesn't exist in ADK apps

---

## Solution: Use `async_stream_query()` Method

### Method Signature

From `vertexai.agent_engines.templates.adk.AdkApp`:

```python
async def async_stream_query(
    self,
    *,
    message: Union[str, Dict[str, Any]],  # User's message
    user_id: str,                         # Required: User identifier
    session_id: Optional[str] = None,     # Optional: For conversation context
    run_config: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> AsyncIterable[Dict[str, Any]]:
    """
    Streams responses asynchronously from the ADK application.

    Yields:
        Event dictionaries asynchronously (streaming response)
    """
```

### Key Parameters

1. **message**: The user's query (string or Content dict)
2. **user_id**: Slack user ID (e.g., `U12345`)
3. **session_id**: Optional - for maintaining conversation context
   - If omitted, a new session is auto-created
   - Use same session_id for conversation continuity
4. **run_config**: Optional configuration for the run

---

## Implementation Plan

### Option 1: Streaming Response (Recommended)

**Pros:**
- Real-time responses in Slack
- Better user experience for long queries
- Follows ADK best practices

**Implementation:**

```python
import asyncio
from vertexai.preview import reasoning_engines

async def query_agent_engine_streaming(query: str, user_id: str, session_id: str = None):
    """Query Agent Engine with streaming response"""
    try:
        # Get the remote agent
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Collect streaming events
        full_response = []

        async for event in remote_agent.async_stream_query(
            message=query,
            user_id=user_id,
            session_id=session_id  # Pass session for conversation context
        ):
            # Event structure: {"type": "...", "data": {...}}
            if event.get("type") == "content":
                # Extract text from content events
                data = event.get("data", {})
                if "parts" in data:
                    for part in data["parts"]:
                        if "text" in part:
                            full_response.append(part["text"])

        return "".join(full_response)

    except Exception as e:
        logger.error(f"Failed to query agent engine: {e}")
        return f"Sorry, I'm having trouble connecting. Error: {str(e)[:200]}"


def _process_slack_message(text, channel, user, event_id):
    """Background processing of Slack messages"""
    try:
        logger.info(f"Processing Slack message from {user}: {text[:100]}...")

        # Create session_id based on Slack channel + user for conversation context
        session_id = f"slack_{channel}_{user}"

        # Query the Agent Engine with async streaming
        answer = asyncio.run(query_agent_engine_streaming(
            query=text,
            user_id=user,
            session_id=session_id
        ))

        # Send response to Slack
        slack_token = get_secret("slack-bot-token")
        if not slack_token:
            logger.error("Failed to retrieve Slack bot token")
            return

        slack_client = WebClient(token=slack_token)
        slack_client.chat_postMessage(
            channel=channel,
            text=answer,
            unfurl_links=False,
            unfurl_media=False
        )
        logger.info(f"Sent response to Slack channel {channel}")

    except Exception as e:
        logger.error(f"Error processing Slack message: {e}")
```

### Option 2: Non-Streaming (Simpler, but waits for full response)

```python
def query_agent_engine(query: str, user_id: str, session_id: str = None):
    """Query Agent Engine and wait for full response"""
    try:
        from vertexai.preview import reasoning_engines

        # Get the remote agent
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Collect all streaming events into full response
        full_response = []

        # Use stream_query (deprecated but synchronous)
        for event in remote_agent.stream_query(
            message=query,
            user_id=user_id,
            session_id=session_id
        ):
            if event.get("type") == "content":
                data = event.get("data", {})
                if "parts" in data:
                    for part in data["parts"]:
                        if "text" in part:
                            full_response.append(part["text"])

        return "".join(full_response)

    except Exception as e:
        logger.error(f"Failed to query agent engine: {e}")
        return f"Sorry, I'm having trouble connecting. Error: {str(e)[:200]}"
```

---

## Session Management Strategy

### Why Sessions Matter

Sessions enable:
1. **Conversation Context**: Agent remembers previous messages
2. **Memory Bank**: Persistent knowledge across interactions
3. **User-Specific State**: Personalized responses

### Session ID Strategy

```python
# Per-channel conversations (everyone in #general shares context)
session_id = f"slack_channel_{channel}"

# Per-user conversations (each user has isolated context)
session_id = f"slack_user_{user}"

# Per-user-per-channel (isolated context per user per channel)
session_id = f"slack_{channel}_{user}"  # ← RECOMMENDED
```

**Recommendation:** Use `f"slack_{channel}_{user}"` for best isolation.

---

## Event Structure (Streaming Response)

The `async_stream_query()` method yields events like:

```python
# Agent thinking event
{
    "type": "tool_call",
    "data": {
        "tool_name": "retrieve_docs",
        "arguments": {"query": "..."}
    }
}

# Content response event
{
    "type": "content",
    "data": {
        "role": "model",
        "parts": [
            {"text": "Based on the documentation, ..."}
        ]
    }
}

# Tool result event
{
    "type": "tool_response",
    "data": {
        "tool_name": "retrieve_docs",
        "response": "..."
    }
}
```

**Extract text from:**
- `event["type"] == "content"`
- `event["data"]["parts"][0]["text"]`

---

## Updated Cloud Function Code

### Complete `slack-webhook/main.py` Fix

```python
"""
Slack Webhook Integration for Bob's Vertex AI Agent Engine

This Cloud Function receives Slack events and forwards them to Bob's Agent Engine.
"""

import functions_framework
import json
import logging
import os
import threading
import asyncio
import google.auth
from google.cloud import secretmanager
from slack_sdk import WebClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global cache for Slack events to prevent duplicates
_slack_event_cache = {}

# Agent Engine configuration
PROJECT_ID = os.getenv("PROJECT_ID", "bobs-brain")
REGION = "us-central1"
AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"


def get_secret(secret_id):
    """Retrieve secret from Google Secret Manager"""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Failed to retrieve secret {secret_id}: {e}")
        return None


async def query_agent_engine_async(query: str, user_id: str, session_id: str = None):
    """Query the Vertex AI Agent Engine using async streaming"""
    try:
        from vertexai.preview import reasoning_engines

        # Get the remote agent
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Collect streaming response
        full_response = []

        # Use async_stream_query with session management
        async for event in remote_agent.async_stream_query(
            message=query,
            user_id=user_id,
            session_id=session_id  # Maintains conversation context
        ):
            # Extract text content from events
            if event.get("type") == "content":
                data = event.get("data", {})
                if "parts" in data:
                    for part in data["parts"]:
                        if "text" in part:
                            full_response.append(part["text"])
                            logger.info(f"Received content chunk: {part['text'][:50]}...")

        response_text = "".join(full_response)
        logger.info(f"Full agent response: {response_text[:200]}...")
        return response_text

    except Exception as e:
        logger.error(f"Failed to query agent engine: {e}", exc_info=True)
        return f"Sorry, I'm having trouble connecting. Error: {str(e)[:200]}"


def _process_slack_message(text, channel, user, event_id):
    """Background processing of Slack messages"""
    try:
        logger.info(f"Processing Slack message from {user} in {channel}: {text[:100]}...")

        # Create session ID for conversation context (per-user-per-channel)
        session_id = f"slack_{channel}_{user}"

        # Query the Agent Engine with async streaming
        answer = asyncio.run(query_agent_engine_async(
            query=text,
            user_id=user,
            session_id=session_id
        ))

        # Get Slack bot token from Secret Manager
        slack_token = get_secret("slack-bot-token")
        if not slack_token:
            logger.error("Failed to retrieve Slack bot token")
            return

        # Send response to Slack
        slack_client = WebClient(token=slack_token)
        slack_client.chat_postMessage(
            channel=channel,
            text=answer,
            unfurl_links=False,
            unfurl_media=False
        )
        logger.info(f"Sent response to Slack channel {channel}")

    except Exception as e:
        logger.error(f"Error processing Slack message: {e}", exc_info=True)


@functions_framework.http
def slack_events(request):
    """
    Cloud Function entry point for Slack events

    Responds to messages in Slack by forwarding to Vertex AI Agent Engine.
    Returns HTTP 200 immediately to prevent Slack retries.
    """
    payload = request.get_json(silent=True) or {}

    # Handle Slack URL verification (first-time setup)
    if payload.get("type") == "url_verification":
        return ({"challenge": payload.get("challenge")}, 200)

    event = payload.get("event", {})
    event_type = event.get("type")
    event_id = payload.get("event_id", "")

    # Deduplicate: Slack retries if we don't respond fast enough
    if event_id and event_id in _slack_event_cache:
        logger.info(f"Ignoring duplicate event: {event_id}")
        return ({"ok": True}, 200)

    if event_id:
        _slack_event_cache[event_id] = True

    # Ignore bot messages to prevent loops
    if event.get("bot_id") or event.get("user") == "USLACKBOT":
        return ({"ok": True}, 200)

    # Only respond to messages and mentions
    if event_type not in ["message", "app_mention"]:
        return ({"ok": True}, 200)

    text = event.get("text", "")
    channel = event.get("channel")
    user = event.get("user")

    if not text or not channel:
        return ({"ok": True}, 200)

    # Process message in background thread to return HTTP 200 immediately
    thread = threading.Thread(
        target=_process_slack_message,
        args=(text, channel, user, event_id),
        daemon=True
    )
    thread.start()

    # Return HTTP 200 immediately to acknowledge receipt
    logger.info(f"Queued Slack message from {user} for background processing")
    return ({"ok": True}, 200)
```

---

## Testing Plan

### 1. Local Testing (Before Deployment)

```bash
# Test async_stream_query locally
cd /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent

# Create test script
cat > test_a2a_query.py << 'EOF'
import asyncio
from vertexai.preview import reasoning_engines
import vertexai

PROJECT_ID = "bobs-brain"
REGION = "us-central1"
AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"

vertexai.init(project=PROJECT_ID, location=REGION)

async def test_query():
    remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

    print("Querying agent...")
    async for event in remote_agent.async_stream_query(
        message="Hello, who are you?",
        user_id="test_user",
        session_id="test_session_001"
    ):
        print(f"Event: {event.get('type')}")
        if event.get("type") == "content":
            data = event.get("data", {})
            if "parts" in data:
                for part in data["parts"]:
                    if "text" in part:
                        print(f"Response: {part['text']}")

asyncio.run(test_query())
EOF

# Run test
python3 test_a2a_query.py
```

### 2. Deploy Updated Cloud Function

```bash
# Deploy updated Slack webhook
gcloud functions deploy slack-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --source=./slack-webhook \
  --entry-point=slack_events \
  --trigger-http \
  --allow-unauthenticated \
  --project=bobs-brain \
  --set-env-vars=PROJECT_ID=bobs-brain
```

### 3. Test in Slack

```
# In Slack, mention @Bob
@bob Hello, who are you?

# Expected: Bob responds with agent description
# Check Cloud Function logs:
gcloud functions logs read slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --limit=50
```

---

## Verification Checklist

- [ ] Update `slack-webhook/main.py` with new `query_agent_engine_async()` function
- [ ] Add session management (`session_id = f"slack_{channel}_{user}"`)
- [ ] Deploy updated Cloud Function to GCP
- [ ] Test in Slack with `@bob` mention
- [ ] Verify conversation context persists across messages
- [ ] Check Cloud Function logs for successful queries
- [ ] Monitor Agent Engine traces in Cloud Trace

---

## Related Documentation

- **ADK Streaming Guide:** https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/adk#stream-responses
- **A2A Protocol Spec:** https://google.github.io/adk-docs/a2a/
- **Agent Engine Deployment:** `bob-vertex-agent/DEPLOYMENT_GUIDE.md`
- **System Architecture:** `bob-vertex-agent/claudes-docs/004-AT-ARCH-bob-vertex-system-analysis.md`

---

## Next Steps

1. **Immediate:** Update `slack-webhook/main.py` with corrected code
2. **Deploy:** Push updated Cloud Function to production
3. **Test:** Verify Slack integration works end-to-end
4. **Monitor:** Watch Cloud Trace for any performance issues
5. **Document:** Update `bob-vertex-agent/CLAUDE.md` with session management patterns

---

**Created:** 2025-11-10
**Last Updated:** 2025-11-10
**Status:** Ready for Implementation
