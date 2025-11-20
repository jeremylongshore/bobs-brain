# 089-AT-ARCH-tools-topology-and-mcp-boundaries.md

**Date Created:** 2025-11-20
**Category:** AT - Architecture & Technical
**Type:** ARCH - Architecture Document
**Status:** CANONICAL ✅

---

## Executive Summary

This document establishes the canonical tool topology and deployment boundaries for the Bob's Brain ADK department. It defines the critical distinction between **local tools** (running in-process within Agent Engine) and **remote tools** (requiring external services like Cloud Run or MCP servers), ensuring clear architectural boundaries and preventing unnecessary service proliferation.

---

## Tool Topology Overview

### Current State (ALL LOCAL)
```
Agent Engine Runtime (In-Process)
├── ADK Built-in Tools
│   ├── GoogleSearchToolset ✅
│   ├── CodeExecutionToolset ✅
│   ├── BigQueryToolset ✅
│   └── VertexAiSearchToolset ✅
├── Custom Function Tools
│   ├── ADK Docs Search ✅
│   ├── Analysis Tools ✅
│   ├── Issue Management ✅
│   └── Planning Tools ✅
└── Future Remote Tools (STUBS ONLY)
    ├── MCP Tools ❌ (no servers deployed)
    └── OpenAPI Tools ❌ (no gateways deployed)
```

**CRITICAL INSIGHT:** All current tools run INSIDE Agent Engine. No external services required.

---

## Tool Categories and Boundaries

### 1. Local Built-in Tools (`local_builtins.py`)
**Location:** `agents/shared_tools/local_builtins.py`
**Execution:** In-process within Agent Engine
**Deployment:** None required (part of agent code)

```python
# These are ADK toolsets that run locally
from google.adk.toolsets import (
    GoogleSearchToolset,      # Web search via Google API
    CodeExecutionToolset,     # Sandboxed code execution
    BigQueryToolset,          # BigQuery API client
    VertexAiSearchToolset     # Vertex AI Search client
)
```

**Key Tools:**
- `get_google_search_tool()` - Web search
- `get_code_execution_tool()` - Python sandbox
- `get_bigquery_toolset()` - Data warehouse queries
- `get_vertex_ai_search_tool()` - Knowledge search (with datahub migration)

### 2. Local Function Tools (`local_functions.py`)
**Location:** `agents/shared_tools/local_functions.py`
**Execution:** In-process Python functions
**Deployment:** None required (pure Python)

```python
# Custom tools written as Python functions
def analyze_code(file_path: str) -> Dict:
    """Pure Python code analysis"""
    # Runs in agent process

def create_issue_spec(title: str) -> IssueSpec:
    """Generate structured issue"""
    # Local object creation
```

**Tool Collections:**
- ADK documentation tools
- Code analysis tools
- Issue management tools
- Planning and fix tools
- QA validation tools
- Documentation generation
- Cleanup and tech debt tools
- Knowledge indexing tools
- Agent delegation tools
- Vertex search status tools

### 3. Remote MCP Tools (`remote_mcp.py`) - FUTURE
**Location:** `agents/shared_tools/remote_mcp.py`
**Execution:** External MCP servers
**Deployment:** Cloud Run services (not deployed)

```python
# STUB ONLY - No MCP servers deployed
def get_mcp_filesystem_tool() -> Optional[Any]:
    """Would connect to MCP server on Cloud Run"""
    # TODO: Deploy server first
    return None  # Not implemented
```

**When to use MCP:**
- Need stateful external services
- Require persistent connections
- Complex protocol implementations
- Multi-agent shared state

### 4. Remote OpenAPI Tools (`remote_openapi.py`) - FUTURE
**Location:** `agents/shared_tools/remote_openapi.py`
**Execution:** Cloud Run API gateways
**Deployment:** Cloud Run services (not deployed)

```python
# STUB ONLY - No gateways deployed
def get_github_api_tool() -> Optional[Any]:
    """Would connect to GitHub API gateway"""
    # TODO: Deploy gateway first
    return None  # Not implemented
```

**When to use OpenAPI gateways:**
- External API rate limiting needed
- Credential management for third-party APIs
- API response caching required
- Complex authentication flows

---

## Deployment Boundaries

### What Runs WHERE

| Component | Location | Why |
|-----------|----------|-----|
| **Agent Code** | Agent Engine | Core agent logic, ADK LlmAgent |
| **Built-in Tools** | Agent Engine | ADK toolsets, API clients |
| **Function Tools** | Agent Engine | Pure Python, no external deps |
| **MCP Servers** | Cloud Run (future) | Stateful services, persistent connections |
| **API Gateways** | Cloud Run (future) | Third-party API proxies |
| **Slack Webhook** | Cloud Run | Event handling, not a tool |
| **A2A Gateway** | Cloud Run | Protocol proxy, not a tool |

### Decision Tree: Local vs Remote

```
Need a new tool?
├── Is it pure Python logic? → LOCAL FUNCTION
├── Is it an ADK built-in? → LOCAL BUILT-IN
├── Does it need external state? → REMOTE MCP
├── Does it proxy an external API? → REMOTE OPENAPI
└── Can it be local? → ALWAYS PREFER LOCAL
```

---

## Migration: Datahub Integration

The Vertex AI Search tool now supports safe migration to datahub-intent:

```python
def get_vertex_ai_search_tool():
    use_datahub = os.getenv("USE_DATAHUB", "false") == "true"

    if use_datahub:
        # New central knowledge hub
        project_id = "datahub-intent"
        datastore_id = "universal-knowledge-store"
    else:
        # Existing Bob datastore (8,718 docs)
        project_id = "bobs-brain"
        datastore_id = "bob-vertex-agent-datastore"
```

**Migration Path:**
1. ✅ Current: Bob uses existing datastore
2. 🟡 Testing: Set `USE_DATAHUB=true` in dev
3. ⏳ Future: Switch production after validation

---

## Anti-Patterns to Avoid

### ❌ DON'T: Create unnecessary Cloud Run services
```python
# BAD: Deploying a service for simple logic
class SimpleCalculatorService:  # Runs on Cloud Run
    def add(a, b):
        return a + b  # This should be local!
```

### ❌ DON'T: Mix Runner imports in gateways
```python
# BAD: Gateway with Runner (violates R3)
# In service/some_gateway/main.py
from google.adk import Runner  # NEVER in gateways!
```

### ✅ DO: Keep it simple and local
```python
# GOOD: Local function tool
def calculate_metrics(data: Dict) -> Dict:
    """Pure Python, runs in Agent Engine"""
    return process_locally(data)
```

---

## Tool Profile Assignment

Each agent gets specific tools via profiles:

```python
# agents/shared_tools/__init__.py
BOB_TOOLS = [
    get_google_search_tool(),      # Web search
    get_vertex_ai_search_tool(),   # Knowledge
    get_adk_docs_tools(),          # ADK patterns
    get_delegation_tools()         # Foreman delegation
]

IAM_ADK_TOOLS = [
    get_adk_docs_tools(),          # ADK expertise
    get_analysis_tools(),          # Pattern analysis
    get_vertex_ai_search_tool()   # Knowledge base
]

# Each agent imports their profile
from agents.shared_tools import BOB_TOOLS
```

---

## Monitoring and Validation

### Tool Health Checks
```bash
# Check which tools are actually available
python3 -c "
from agents.shared_tools import *
print('Local tools:', len(BOB_TOOLS))
print('MCP tools:', len(list_available_mcp_servers()))
print('OpenAPI tools:', len(list_available_openapi_gateways()))
"
```

Expected output:
```
Local tools: 15+
MCP tools: 0  # None deployed
OpenAPI tools: 0  # None deployed
```

---

## Future Considerations

### When to Add Remote Services

Only create remote services when you have:
1. **Stateful requirements** that can't be met locally
2. **External API rate limits** that need management
3. **Shared resources** across multiple agents
4. **Security boundaries** that require isolation
5. **Performance requirements** that need dedicated resources

### MCP vs OpenAPI Decision

| Use MCP When | Use OpenAPI When |
|--------------|------------------|
| Need persistent connections | RESTful API is sufficient |
| Complex bidirectional protocol | Simple request/response |
| Shared agent state | Stateless API proxy |
| Custom tool protocol | Standard HTTP API |

---

## Implementation Files

The complete tool topology implementation:

```
agents/shared_tools/
├── __init__.py           # Tool profiles for all agents
├── custom_tools.py       # Tool collections (imports)
├── local_builtins.py     # ADK built-in tools ✅
├── local_functions.py    # Custom Python tools ✅
├── remote_mcp.py        # MCP stubs (future) ⏳
└── remote_openapi.py    # OpenAPI stubs (future) ⏳
```

---

## Compliance with Hard Mode Rules

This topology ensures compliance with:
- **R1:** ADK-only implementation (all tools via ADK patterns)
- **R2:** Agent Engine runtime (tools run in-engine)
- **R3:** Gateway separation (no Runner in service/)
- **R7:** SPIFFE ID propagation (tools inherit agent identity)

---

## Summary

The Bob's Brain tool topology is **intentionally simple**:
- All current tools run locally in Agent Engine
- No unnecessary external services
- Clear boundaries for future remote tools
- Safe migration path to datahub-intent

This architecture prevents service sprawl, reduces operational complexity, and maintains the ADK/Vertex AI "Hard Mode" compliance required for this canonical department implementation.

---

**Last Updated:** 2025-11-20
**Next Review:** After first remote tool deployment
**Owner:** ADK Department Build Captain

---