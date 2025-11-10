# Agent Engine Query Methods - Complete Solution Guide
**Date:** 2025-11-10
**Category:** Testing & Quality (TQ)
**Type:** Solution (SOLV)

## Executive Summary

When querying an ADK agent deployed to Vertex AI Agent Engine, the `stream_query()` method appears to be missing from the `ReasoningEngine` object. This document provides three working solutions to query your deployed agent.

## The Problem

### Symptoms
- `AttributeError: 'ReasoningEngine' object has no attribute 'stream_query'`
- Public methods visible: `create`, `delete`, `list`, `to_dict`, etc. - but no query methods
- `operation_schemas()` shows `stream_query` exists but it's not directly callable
- Warning: "Failed to register API methods: Unsupported api mode: 'async'"

### Root Cause
The Vertex AI SDK uses **dynamic method registration** for agent operations. The `stream_query()` and `query()` methods are registered at runtime based on the agent's operation schemas. This registration can fail or be unavailable in certain contexts (like Cloud Functions).

## Solution 1: Using stream_query() (When Available)

Despite the error you're seeing, `stream_query()` DOES work in many contexts. Your test file proves this works:

```python
from vertexai.preview import reasoning_engines
import vertexai

vertexai.init(
    project="bobs-brain",
    location="us-central1"
)

# Use just the ID, not the full path
AGENT_ENGINE_ID = "5828234061910376448"
remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

# This DOES work despite not appearing in dir(remote_agent)
full_response = []
for event in remote_agent.stream_query(
    input={
        "message": "Hello, Bob!",
        "user_id": "test_user",
        "session_id": "test_session"
    }
):
    if isinstance(event, dict):
        if "output" in event:
            full_response.append(str(event["output"]))
        elif "text" in event:
            full_response.append(event["text"])

response = "".join(full_response)
```

### Why It Works Sometimes
- Methods are dynamically registered based on agent configuration
- Registration happens during `ReasoningEngine` initialization
- May fail in certain environments (Cloud Functions, restricted contexts)

## Solution 2: Direct REST API Call (Most Reliable)

When the SDK methods aren't available, use the REST API directly:

```python
import google.auth
from google.auth.transport.requests import Request
import requests
import json

# Get credentials
credentials, project = google.auth.default()
credentials.refresh(Request())

# Your agent details
AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"

# Build the URL
url = f"https://us-central1-aiplatform.googleapis.com/v1/{AGENT_ENGINE_ID}:streamQuery"

# Headers
headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}

# Payload (matches ADK operation schema)
payload = {
    "input": {
        "message": "What is the hustle project?",
        "user_id": "user123",
        "session_id": "session456"
    }
}

# Make the request
response = requests.post(url, json=payload, headers=headers, timeout=30, stream=True)

# Process streaming response
full_response = []
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line.decode('utf-8'))
            if "output" in data:
                full_response.append(str(data["output"]))
        except json.JSONDecodeError:
            continue

result = "".join(full_response)
```

### Available Endpoints
- `:streamQuery` - Streaming responses (recommended)
- `:query` - Non-streaming (if agent supports it)
- Direct invocation without suffix (varies by agent config)

## Solution 3: Fallback Pattern (Best Practice)

Implement a fallback pattern that tries multiple methods:

```python
def query_agent_with_fallback(query, user_id, session_id=None):
    """
    Robust agent querying with fallback methods.
    """
    # Method 1: Try stream_query
    try:
        from vertexai.preview import reasoning_engines
        remote_agent = reasoning_engines.ReasoningEngine("5828234061910376448")

        response = []
        for event in remote_agent.stream_query(
            input={"message": query, "user_id": user_id, "session_id": session_id}
        ):
            # Process events...
            pass
        return "".join(response)
    except AttributeError:
        pass  # Method not available, try next

    # Method 2: Try REST API
    try:
        # REST API implementation (see Solution 2)
        return query_via_rest_api(query, user_id, session_id)
    except Exception as e:
        logger.error(f"All methods failed: {e}")
        return "Unable to query agent"
```

## Cloud Function Specific Issues

### Problem
In Cloud Functions, the dynamic method registration often fails due to:
- Cold start timing issues
- Limited runtime environment
- Missing dependencies
- Network isolation

### Solution for Cloud Functions
Always use the **REST API method** (Solution 2) in Cloud Functions:

```python
import functions_framework

@functions_framework.http
def query_agent(request):
    """Cloud Function that queries Agent Engine."""
    import google.auth
    from google.auth.transport.requests import Request
    import requests

    # Use REST API directly - most reliable in Cloud Functions
    credentials, _ = google.auth.default()
    credentials.refresh(Request())

    # ... REST API implementation ...
```

## Understanding operation_schemas()

The `operation_schemas()` method shows what operations the agent supports:

```python
remote_agent.operation_schemas()
# Returns:
{
    'stream_query': {
        'name': 'stream_query',
        'api_mode': 'stream',
        'parameters': {...}
    },
    'async_stream_query': {
        'name': 'async_stream_query',
        'api_mode': 'async_stream',
        'parameters': {...}
    }
}
```

### API Modes
- `''` (empty) - Synchronous query
- `'stream'` - Streaming responses
- `'async'` - Asynchronous (not supported by current SDK)
- `'async_stream'` - Async streaming (not supported)

The warning "Unsupported api mode: 'async'" means the SDK can't register async methods, but streaming still works.

## Testing Your Agent

Run the provided test script to verify which methods work:

```bash
cd /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent
python query_agent_solution.py
```

Expected output:
```
METHOD 1: Testing stream_query()...
Response: [Agent response here]...

METHOD 2: Testing REST API...
Response: [Agent response here]...

METHOD 3: Testing query() (if available)...
Response: [Agent response here]...
```

## Troubleshooting

### Issue: stream_query() not found
**Solution:** Use REST API method (Solution 2)

### Issue: REST API returns 404
**Check:**
- Agent ID is correct
- Agent is deployed and running
- Project and region match

### Issue: Authentication errors
**Fix:**
```bash
gcloud auth application-default login
gcloud config set project bobs-brain
```

### Issue: Timeout errors
**Solutions:**
- Increase timeout in requests
- Check agent health in console
- Verify network connectivity

## Best Practices

1. **Always implement fallback methods** - Don't rely on a single approach
2. **Use REST API in Cloud Functions** - Most reliable
3. **Cache agent references** - Avoid re-initializing
4. **Handle streaming properly** - Process events as they arrive
5. **Include session_id** - Maintains conversation context
6. **Set appropriate timeouts** - 30 seconds recommended
7. **Log all errors** - For debugging dynamic registration issues

## Complete Working Example

See `/home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent/query_agent_solution.py` for a complete implementation with all three methods.

## References

- Agent Engine API: https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.reasoningEngines
- ADK Documentation: https://github.com/google/adk-python
- Vertex AI SDK: https://github.com/googleapis/python-aiplatform

---
**Last Updated:** 2025-11-10
**Status:** Solution Verified
**Agent Engine ID:** 5828234061910376448