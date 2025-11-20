# ADK A2A Agent Patterns - Implementation Notes

**Document Type:** DR-IMPL (Documentation & Reference - Implementation)
**Created:** 2025-11-19
**Status:** Active
**Source:** Official Google ADK A2A Documentation

## Overview

Agent-to-Agent (A2A) protocol enables ADK agents to discover and communicate with each other using standardized HTTP endpoints and JSON task messages. This document provides implementation-focused guidance for building A2A-enabled agents with Google ADK.

## Key Concepts

### What is A2A?

A2A is a standardized protocol for agent interoperability:
- **Client Agent** - Discovers and invokes remote agents via HTTP
- **Server Agent** - Exposes ADK agent capabilities via REST API
- **Agent Card** - JSON metadata describing agent capabilities
- **Tasks** - Structured requests sent to agents
- **Messages** - Agent responses and intermediate outputs

### When to Use A2A

Use A2A when:
- Building multi-agent systems with specialized agents
- Enabling agent discovery and composition
- Deploying agents as independent microservices
- Integrating with external agent systems
- Creating agent marketplaces or ecosystems

### How ADK, A2A, and MCP Fit Together

```
┌─────────────────────────────────────────────────────────┐
│ ADK (Agent Development Kit)                             │
│  └─> Defines agents (LlmAgent, SequentialAgent, etc.)  │
│  └─> Provides tools (FunctionTool, AgentTool, etc.)    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ A2A (Agent-to-Agent Protocol)                           │
│  └─> Exposes ADK agents as HTTP services                │
│  └─> Enables agent discovery via Agent Cards            │
│  └─> Standardizes task invocation and messages          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ MCP (Model Context Protocol)                            │
│  └─> Exposes tools/resources to agents                  │
│  └─> Integrates external data sources                   │
│  └─> Provides standardized tool interfaces              │
└─────────────────────────────────────────────────────────┘
```

**Integration Pattern:**
1. Build agent with ADK (LlmAgent + tools)
2. Expose agent via A2A (`to_a2a()` function)
3. Connect tools via MCP (MCPToolset)
4. Deploy to Cloud Run or Agent Engine

## A2A Server Pattern (Exposing Agents)

### Basic Server Setup

Convert an ADK agent to an A2A-compatible HTTP application:

```python
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uvicorn

# Create your ADK agent
root_agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="my_agent",
    instruction="You are a helpful assistant.",
    tools=[...]
)

# Convert to A2A application
a2a_app = to_a2a(root_agent, port=8001)

# Start HTTP server
if __name__ == "__main__":
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)
```

### Automatic Agent Card Generation

The `to_a2a()` function automatically:
- Generates an Agent Card from agent metadata
- Exposes card at `/.well-known/agent.json` endpoint
- Includes agent name, description, capabilities
- Enables automatic discovery by client agents

### Port Strategy

**Local Development:**
```python
# Agent 1: Prime checker
a2a_app = to_a2a(prime_agent, port=8001)

# Agent 2: Dice roller
a2a_app = to_a2a(roll_agent, port=8002)

# Agent 3: Orchestrator
a2a_app = to_a2a(orchestrator, port=8000)
```

**Cloud Run Deployment:**
```python
# Cloud Run assigns PORT environment variable
import os
port = int(os.getenv("PORT", 8080))
a2a_app = to_a2a(root_agent, port=port)
uvicorn.run(a2a_app, host="0.0.0.0", port=port)
```

### Cloud Run Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run will set PORT env var
CMD ["python", "main.py"]
```

**Deploy to Cloud Run:**
```bash
gcloud run deploy agent-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## A2A Client Pattern (Consuming Remote Agents)

### RemoteA2aAgent Usage

Access remote A2A agents from orchestrator agents:

```python
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH
)

# Connect to remote agent via Agent Card
prime_agent = RemoteA2aAgent(
    name="prime_agent",
    description="Agent that checks if numbers are prime.",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}"
)

# Use in orchestrator
from google.adk.agents import Agent

orchestrator = Agent(
    model="gemini-2.0-flash",
    name="orchestrator",
    sub_agents=[prime_agent],  # Mix local and remote agents
    tools=[example_tool]
)
```

### Agent Card Discovery

**Well-Known Path:**
```python
AGENT_CARD_WELL_KNOWN_PATH = "/.well-known/agent.json"
```

**Agent Card Structure:**
```json
{
  "name": "prime_agent",
  "description": "Checks if numbers are prime",
  "version": "1.0.0",
  "capabilities": ["number_theory", "prime_checking"],
  "endpoint": "/a2a/invoke"
}
```

### Multi-Agent Orchestration

Combine local and remote agents:

```python
# Local agent
local_calculator = LlmAgent(
    model="gemini-2.0-flash",
    name="calculator",
    tools=[add_tool, multiply_tool]
)

# Remote agents
prime_checker = RemoteA2aAgent(
    name="prime_checker",
    agent_card="http://prime-service.run.app/.well-known/agent.json"
)

weather_agent = RemoteA2aAgent(
    name="weather_agent",
    agent_card="http://weather-service.run.app/.well-known/agent.json"
)

# Orchestrator coordinates all agents
root_agent = Agent(
    model="gemini-2.0-flash",
    name="orchestrator",
    sub_agents=[local_calculator, prime_checker, weather_agent]
)
```

## Example Patterns

### Pattern 1: Hello World Agent (Minimal)

```python
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uvicorn

agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="hello_agent",
    instruction="Always respond with 'Hello World!'"
)

app = to_a2a(agent, port=8001)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Test:**
```bash
curl -X POST http://localhost:8001/a2a/invoke \
  -H "Content-Type: application/json" \
  -d '{"task": "Say hello"}'
```

### Pattern 2: Weather & Time Agents (Tool-Based)

**Weather Agent:**
```python
from google.adk.tools import FunctionTool

def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"Weather in {location}: Sunny, 72°F"

weather_tool = FunctionTool(get_weather)

weather_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="weather_agent",
    instruction="Provide weather information.",
    tools=[weather_tool]
)

app = to_a2a(weather_agent, port=8001)
```

**Time Agent:**
```python
import datetime

def get_current_time() -> str:
    """Get current time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time_tool = FunctionTool(get_current_time)

time_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="time_agent",
    instruction="Provide current time.",
    tools=[time_tool]
)

app = to_a2a(time_agent, port=8002)
```

### Pattern 3: Event Orchestrator (Sequential Workflow)

```python
from google.adk.agents import SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Connect to remote agents
weather_agent = RemoteA2aAgent(
    name="weather",
    description="Weather information",
    agent_card="http://localhost:8001/.well-known/agent.json"
)

time_agent = RemoteA2aAgent(
    name="time",
    description="Current time",
    agent_card="http://localhost:8002/.well-known/agent.json"
)

# Sequential workflow
event_planner = SequentialAgent(
    name="event_planner",
    sub_agents=[time_agent, weather_agent],  # Execute in order
    instruction="""
    1. Check current time
    2. Check weather for event location
    3. Recommend best event time
    """
)

app = to_a2a(event_planner, port=8000)
```

### Pattern 4: Parallel Agent Execution

```python
from google.adk.agents import ParallelAgent

# Execute agents concurrently
parallel_data_fetcher = ParallelAgent(
    name="data_fetcher",
    sub_agents=[weather_agent, time_agent],  # Run simultaneously
    instruction="Gather all information in parallel"
)

app = to_a2a(parallel_data_fetcher, port=8000)
```

## Environment & Authentication

### Required Environment Variables

```bash
# GCP Configuration
export PROJECT_ID="your-project-id"
export LOCATION="us-central1"

# Agent Engine (if deploying to Agent Engine)
export AGENT_ENGINE_ID="your-agent-engine-id"

# Application Configuration
export APP_NAME="my-agent"
export APP_VERSION="1.0.0"

# Cloud Run (if deploying to Cloud Run)
export PORT=8080
```

### Application Default Credentials (ADC)

**Local Development:**
```bash
gcloud auth application-default login
```

**Cloud Run (Automatic):**
- Uses Cloud Run service account automatically
- No manual credential configuration needed

**Agent Engine (Automatic):**
- Uses Agent Engine service account
- Credentials managed by platform

### Service Account Permissions

Required IAM roles for A2A agents:
```bash
# For Vertex AI model access
roles/aiplatform.user

# For Cloud Run deployment
roles/run.developer

# For Agent Engine deployment
roles/aiplatform.admin
```

## Debugging & Development Tools

### A2A Inspector (Web UI)

Monitor A2A task execution in real-time:

```bash
# Start agent with A2A Inspector
python main.py --enable-inspector
```

Access at: `http://localhost:8001/inspector`

**Features:**
- View incoming tasks
- Inspect agent messages
- Debug task failures
- Monitor performance

### ADK Web UI

Test agents locally with interactive UI:

```bash
adk web my_agent
```

**Features:**
- Chat interface for testing
- View agent reasoning traces
- Inspect tool calls
- Debug multi-agent orchestration

### Local Testing Strategy

```bash
# Terminal 1: Start server agent
python prime_agent.py  # Port 8001

# Terminal 2: Start orchestrator
python orchestrator.py  # Port 8000

# Terminal 3: Test with curl
curl -X POST http://localhost:8000/a2a/invoke \
  -H "Content-Type: application/json" \
  -d '{"task": "Is 17 prime?"}'
```

## Production Deployment Recommendations

### For Bob's Brain Stack

**Current Architecture:**
- **Agent Core:** Vertex AI Agent Engine (R2)
- **Gateways:** Cloud Run (A2A gateway, Slack webhook)
- **Memory:** VertexAiSessionService + VertexAiMemoryBankService (R5)

**A2A Integration Strategy:**

1. **Primary Agent on Agent Engine:**
```python
# my_agent/agent.py (existing)
root_agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="bobs_brain",
    tools=[search_adk_docs, search_vertex_ai, ...]
)
# Deployed via: adk deploy agent_engine
```

2. **A2A Gateway on Cloud Run:**
```python
# service/a2a_gateway/main.py
from fastapi import FastAPI
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

app = FastAPI()

# Connect to Agent Engine via REST API
bob = RemoteA2aAgent(
    name="bobs_brain",
    description="ADK expert assistant",
    agent_card=f"{AGENT_ENGINE_URL}/.well-known/agent.json"
)

@app.get("/.well-known/agent.json")
def get_agent_card():
    """Expose Bob's Agent Card for A2A discovery."""
    return bob.get_card()

@app.post("/a2a/invoke")
async def invoke(request: Request):
    """A2A endpoint - proxy to Agent Engine."""
    task = await request.json()
    return await bob.invoke(task)
```

3. **Deploy A2A Gateway:**
```bash
cd service/a2a_gateway
gcloud run deploy bobs-brain-a2a \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=$PROJECT_ID,AGENT_ENGINE_URL=$AGENT_ENGINE_URL
```

**Benefits:**
- ✅ Maintains Agent Engine deployment (R2)
- ✅ No Runner imports in gateway (R3)
- ✅ Enables A2A discoverability
- ✅ Supports multi-agent orchestration
- ✅ Scales independently from core agent

### Security Considerations

**Authentication:**
```python
from fastapi import Header, HTTPException

@app.post("/a2a/invoke")
async def invoke(
    request: Request,
    authorization: str = Header(None)
):
    """Require API key for A2A invocations."""
    if authorization != f"Bearer {expected_token}":
        raise HTTPException(status_code=401)
    # Process task...
```

**Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/a2a/invoke")
@limiter.limit("10/minute")
async def invoke(request: Request):
    # Process task...
```

**CORS Configuration:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trusted-domain.com"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

## Key Takeaways

1. **Simple Enablement** - `to_a2a(agent, port)` converts any ADK agent to A2A service
2. **Automatic Discovery** - Agent Cards enable zero-config agent discovery
3. **Mix Local & Remote** - Orchestrators can combine local and remote agents seamlessly
4. **Cloud Run Ready** - Deploy A2A agents as independent microservices
5. **Hard Mode Compatible** - A2A gateway pattern maintains R2/R3 compliance for Bob's Brain

## References

- **A2A Protocol Intro:** https://google.github.io/adk-docs/a2a/intro/
- **Exposing Agents:** https://google.github.io/adk-docs/a2a/quickstart-exposing/
- **Consuming Agents:** https://google.github.io/adk-docs/a2a/quickstart-consuming/
- **Agent Cards Spec:** https://google.github.io/adk-docs/a2a/agent-card/

---

**Document Status:** Active
**Last Updated:** 2025-11-19
**Next Review:** After implementing A2A gateway for Bob's Brain
