# Quick Fix: Slack Webhook A2A Protocol Issue

**Issue:** `Default method 'query' not found` error in Slack webhook
**Solution:** Use `async_stream_query()` instead of `query()`
**Time to Fix:** 5 minutes

---

## The Problem

```python
# ❌ WRONG - This method doesn't exist in ADK apps
remote_agent.query(input=query)
```

## The Solution

```python
# ✅ CORRECT - Use async_stream_query with proper parameters
async for event in remote_agent.async_stream_query(
    message=query,
    user_id=user_id,
    session_id=session_id
):
    # Process streaming events
```

---

## Exact Code Changes

### Replace function in `slack-webhook/main.py`

**OLD CODE (lines 41-64):**
```python
def query_agent_engine(query):
    """Query the Vertex AI Agent Engine using Python SDK"""
    try:
        from vertexai.preview import reasoning_engines

        # Get the remote agent
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Query the agent - ADK agents accept string input directly
        response = remote_agent.query(input=query)  # ← THIS IS WRONG

        logger.info(f"Agent response: {response}")

        # Extract text from response
        if isinstance(response, dict):
            if "output" in response:
                return str(response["output"])
            return str(response)

        return str(response)

    except Exception as e:
        logger.error(f"Failed to query agent engine: {e}")
        return f"Sorry, I'm having trouble connecting. Error: {str(e)[:200]}"
```

**NEW CODE (replaces above):**
```python
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

        response_text = "".join(full_response)
        logger.info(f"Agent response: {response_text[:200]}...")
        return response_text

    except Exception as e:
        logger.error(f"Failed to query agent engine: {e}", exc_info=True)
        return f"Sorry, I'm having trouble connecting. Error: {str(e)[:200]}"
```

### Update background message processor

**OLD CODE (lines 67-93):**
```python
def _process_slack_message(text, channel, user, event_id):
    """Background processing of Slack messages"""
    try:
        logger.info(f"Processing Slack message from {user}: {text[:100]}...")

        # Query the Agent Engine
        answer = query_agent_engine(text)  # ← WRONG CALL

        # Get Slack bot token from Secret Manager
        # ... rest of code
```

**NEW CODE (replaces above):**
```python
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
        # ... rest of code (unchanged)
```

### Add asyncio import at top of file

**ADD THIS LINE (after line 10):**
```python
import asyncio  # Add this import
```

---

## Deploy

```bash
cd /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent

# Deploy updated Cloud Function
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

---

## Test

```bash
# In Slack
@bob Hello, who are you?

# Check logs
gcloud functions logs read slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --limit=20
```

---

## Summary of Changes

1. **Renamed function**: `query_agent_engine()` → `query_agent_engine_async()`
2. **Added async/await**: Function now uses `async def` and `async for`
3. **New method**: `remote_agent.async_stream_query()` instead of `query()`
4. **Added parameters**:
   - `user_id` (Slack user ID)
   - `session_id` (for conversation context)
5. **Process streaming events**: Loop through events, extract text from "content" events
6. **Call with asyncio.run()**: In `_process_slack_message()`, wrap async call

---

**That's it!** This fixes the "Default method 'query' not found" error.
