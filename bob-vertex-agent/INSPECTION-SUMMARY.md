# Bob's Brain Agent Engine Inspection Summary

**Date:** 2025-11-10  
**Status:** 🔴 CRITICAL ISSUE IDENTIFIED

---

## The Problem

Your agent is deployed successfully but **cannot be queried** because:

1. **ADK Deployment Uses Different API**
   - ADK agents expose `stream_query()` instead of `query()`
   - Your Slack webhook uses `.query()` which doesn't exist
   - Result: `AttributeError: 'ReasoningEngine' object has no attribute 'query'`

2. **API Method Comparison**

   | Method | Standard Agent Engine | ADK Agents (Your Deployment) |
   |--------|----------------------|------------------------------|
   | `query()` | ✅ Available | ❌ NOT AVAILABLE |
   | `send_message()` | ✅ Available | ❌ NOT AVAILABLE |
   | `stream_query()` | ❌ Not available | ✅ Available (deprecated) |
   | `async_stream_query()` | ❌ Not available | ✅ Available (PREFERRED) |

---

## What's Actually Deployed

```
app/agent.py (Google ADK Agent)
    ↓
app/agent_engine_app.py (AdkApp wrapper)
    ↓
Vertex AI Agent Engine (deployment)
    ↓
Exposed Methods: stream_query(), async_stream_query()
    ↓
slack-webhook/main.py tries to call .query()  ❌ FAILS
```

---

## The Fix

### Option 1: Use REST API (Recommended)

Replace `slack-webhook/main.py:41-64` with:

```python
def query_agent_engine(query):
    """Query ADK agent via REST API (streamQuery operation)"""
    try:
        import requests
        import google.auth
        from google.auth.transport.requests import Request
        
        credentials, _ = google.auth.default()
        credentials.refresh(Request())
        
        url = (
            "https://us-central1-aiplatform.googleapis.com/v1/"
            f"{AGENT_ENGINE_ID}:streamQuery"
        )
        
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "message": query,
            "user_id": "slack_user"
        }
        
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        # Collect streaming response
        full_response = ""
        for line in response.iter_lines():
            if line and line.startswith(b"data: "):
                try:
                    data = json.loads(line[6:])
                    if isinstance(data, dict) and "content" in data:
                        full_response += data["content"]
                except json.JSONDecodeError:
                    continue
        
        return full_response or "No response from agent"
        
    except Exception as e:
        logger.error(f"Failed to query agent engine: {e}")
        return f"Sorry, I'm having trouble connecting. Error: {str(e)[:200]}"
```

### Option 2: Use gRPC Client

```python
def query_agent_engine(query):
    """Query ADK agent via gRPC"""
    from google.cloud.aiplatform_v1 import ReasoningEngineExecutionServiceClient
    
    client = ReasoningEngineExecutionServiceClient()
    
    request = {
        "name": AGENT_ENGINE_ID,
        "input": json.dumps({"message": query, "user_id": "slack_user"})
    }
    
    # Stream responses
    full_response = ""
    for response in client.query_reasoning_engine(request=request):
        full_response += str(response.output)
    
    return full_response
```

---

## Agent Capabilities Summary

### ✅ What Works

- **Memory Bank:** Fully enabled
  - `create_session()` - Track conversations
  - `async_search_memory()` - Search conversation history
  - `async_get_session()` - Retrieve session state
  
- **Feedback System:** `register_feedback()` - Log feedback

- **A2A Protocol:** Implemented at app layer (`app/a2a_tools.py`)

- **Security:** Follows GCP best practices

### ❌ What Doesn't Work

- **Slack Webhook:** Uses wrong API method (`.query()`)
- **Direct Query:** No synchronous query method available

---

## Quick Test

Test the agent via REST API:

```bash
curl -X POST \
  https://us-central1-aiplatform.googleapis.com/v1/projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448:streamQuery \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, this is a test. Please respond with OK.",
    "user_id": "test_user"
  }'
```

---

## Next Steps

1. **IMMEDIATE:** Update `slack-webhook/main.py` with Option 1 (REST API)
2. **TEST:** Deploy updated Cloud Function
3. **VERIFY:** Test Slack integration end-to-end
4. **ENHANCE:** Implement session management for conversation continuity

---

## Full Reports

- **Detailed Inspection:** `claudes-docs/006-RA-INSP-agent-engine-deployment-inspection.md`
- **JSON Report:** `agent_engine_inspection_report.json`
- **Inspection Script:** `inspect_agent_engine.py`

---

**Need Help?** See detailed recommendations in the full inspection report.
