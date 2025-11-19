# ADK Tools Reference - Complete Catalog

**Created:** 2025-11-19
**Status:** Comprehensive reference for all ADK tool types
**Audience:** Developers building agents with Google ADK

---

## Table of Contents

1. [Overview](#overview)
2. [Tool Categories](#tool-categories)
3. [Built-in Tools](#built-in-tools)
4. [Custom Tools](#custom-tools)
5. [Google Cloud Tools](#google-cloud-tools)
6. [Third-Party Tools](#third-party-tools)
7. [Tool Selection Guide](#tool-selection-guide)
8. [Architecture Patterns](#architecture-patterns)
9. [Best Practices](#best-practices)
10. [Limitations](#limitations)

---

## Overview

The Agent Development Kit (ADK) provides a modular tool system that extends agent capabilities. Tools are executable functions that agents invoke during runtime to perform tasks ranging from web searches to database queries to custom business logic.

### What are Tools?

Tools transform agent conversations into actionable operations. When an agent needs to:
- Search the web → Use Google Search tool
- Execute calculations → Use Code Execution tool
- Query databases → Use BigQuery/Spanner tools
- Call REST APIs → Use OpenAPI tools
- Implement custom logic → Use Function tools

### Tool Architecture

```
Agent (LlmAgent)
  ├─ Model (Gemini 2.5 Flash)
  └─ Tools (List of callable tools)
      ├─ Built-in Tools (Google Search, Code Execution)
      ├─ Custom Tools (Function, MCP, OpenAPI)
      └─ Cloud Tools (BigQuery, Vertex AI Search, etc.)
```

Tools integrate seamlessly with the agent's reasoning loop, allowing the LLM to:
1. **Detect** when a tool is needed
2. **Select** the appropriate tool
3. **Invoke** the tool with parameters
4. **Process** the tool's response
5. **Continue** reasoning with results

---

## Tool Categories

The ADK organizes tools into three primary categories:

### 1. Gemini Tools (Built-in)
Pre-integrated capabilities leveraging Gemini models directly:
- **Google Search** - Web search with grounding
- **Code Execution** - Python code execution (built-in or GKE-sandboxed)

**Availability:** Python v0.1.0+, Go v0.1.0+, Java v0.2.0+

### 2. Google Cloud Tools (Enterprise)
Enterprise integrations for Google Cloud services:
- **BigQuery** - Dataset/table queries, SQL execution, forecasting
- **Spanner** - Schema management, SQL queries, similarity search
- **Bigtable** - Instance/table listing, metadata, SQL queries
- **Vertex AI RAG Engine** - Private RAG corpus retrieval
- **Vertex AI Search** - Private data store search
- **MCP Toolbox for Databases** - 30+ data source connectors
- **BigQuery Agent Analytics** - Agent behavior monitoring
- **Apigee API Hub** - Documented API tool conversion
- **Application Integration** - 100+ pre-built enterprise connectors

**Use Cases:** Federated search, workflow automation, secure on-premise access

### 3. Third-Party Tools
External integrations for specialized tasks:
- **Web Scraping:** AgentQL, Firecrawl, Browserbase
- **Search Platforms:** Exa, Tavily
- **Productivity Apps:** GitHub, Notion, Hugging Face

### 4. Custom Tools
Build proprietary tools for specific workflows:
- **Function Tools** - Custom Python functions
- **MCP Tools** - Model Context Protocol server integration
- **OpenAPI Tools** - REST API integration via OpenAPI specs

---

## Built-in Tools

### Google Search

**Purpose:** Web search with Gemini grounding for up-to-date information retrieval.

**Requirements:**
- Compatible only with Gemini 2 models
- Must display "Search suggestions" in production applications
- UI code returned as `renderedContent` in response

**Implementation:**

```python
from google.adk.tools import google_search
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="search_agent",
    model="gemini-2.0-flash",
    tools=[google_search],
    preamble="You are a research assistant with web search access."
)
```

**When to Use:**
- Real-time information retrieval
- Fact-checking current events
- Finding documentation or resources
- Grounding responses in web data

**Limitations:**
- Requires Gemini 2 models
- Must display search suggestions UI
- Subject to Google Search quotas

---

### Code Execution

**Purpose:** Execute Python code for calculations, data manipulation, and algorithmic tasks.

**Variants:**

#### 1. Built-In Code Executor
Runs code directly within the agent environment.

```python
from google.adk.tools import code_execution
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="math_agent",
    model="gemini-2.0-flash",
    tools=[code_execution],
    preamble="You can execute Python code for calculations."
)
```

**Use Cases:**
- Mathematical calculations
- Data transformations
- Algorithm execution
- Quick prototyping

#### 2. GKE Code Executor (Python v1.14.0+)
Executes code in isolated gVisor-sandboxed Kubernetes pods for enhanced security.

```python
from google.adk.tools import GKECodeExecutor

gke_executor = GKECodeExecutor(
    namespace="agent-sandbox",
    timeout=30,  # seconds
    cpu_limit="1",
    memory_limit="512Mi"
)

agent = LlmAgent(
    name="secure_code_agent",
    model="gemini-2.0-flash",
    tools=[gke_executor]
)
```

**Requirements:**
- GKE cluster with gVisor-enabled node pool
- RBAC permissions for pod creation
- Install: `pip install google-adk[gke]`

**When to Use GKE Executor:**
- Production environments requiring isolation
- Untrusted or user-provided code
- Compliance requirements for sandboxing
- Resource-intensive computations

**Configuration Parameters:**
- `namespace` - Kubernetes namespace for pod creation
- `timeout` - Maximum execution time (seconds)
- `cpu_limit` - CPU resource limit
- `memory_limit` - Memory resource limit

---

## Custom Tools

### Function Tools

**Purpose:** Convert Python functions into agent-callable tools with automatic schema generation.

**How it Works:**
The ADK inspects function signatures (name, docstring, parameters, type hints, defaults) and generates LLM-compatible schemas automatically.

**Basic Example:**

```python
def get_weather(city: str, unit: str = "Celsius") -> dict:
    """Retrieves current weather data for a city.

    Args:
        city (str): The city name (e.g., 'San Francisco').
        unit (str): Temperature unit ('Celsius' or 'Fahrenheit'). Defaults to Celsius.

    Returns:
        dict: Weather data with temperature, conditions, and status.
    """
    # Simulate API call
    return {
        "city": city,
        "temperature": 22,
        "unit": unit,
        "conditions": "Sunny",
        "status": "success"
    }

# Auto-wrapped as FunctionTool
agent = LlmAgent(
    name="weather_agent",
    model="gemini-2.0-flash",
    tools=[get_weather]
)
```

**See:** `ADK-FUNCTION-TOOLS-GUIDE.md` for comprehensive implementation guide.

---

### MCP Tools

**Purpose:** Integrate Model Context Protocol servers as agent tools, enabling standardized communication with external data sources.

**What is MCP?**
An open standard for LLM communication with external applications, data sources, and tools via a client-server architecture.

**Two Integration Patterns:**

#### 1. ADK Agent as MCP Client
Consume tools from external MCP servers:

```python
from google.adk.tools import MCPToolset
from google.adk.agents import LlmAgent

# Connect to MCP server
mcp_toolset = MCPToolset(
    server_url="http://localhost:8080",
    connection_type="http"
)

agent = LlmAgent(
    name="mcp_client_agent",
    model="gemini-2.0-flash",
    tools=[mcp_toolset]
)
```

#### 2. ADK Tools as MCP Server
Expose ADK tools to any MCP client by building custom MCP servers.

**Connection Types:**
- **Stdio:** Local process communication (development, single-tenant)
- **HTTP/SSE:** Network-based (production, scalability)

**Critical Deployment Requirement:**
The agent and MCPToolset must be defined **synchronously** in `agent.py`. Deployment environments require synchronous instantiation.

**See:** `ADK-MCP-TOOLS-GUIDE.md` for detailed integration patterns.

---

### OpenAPI Tools

**Purpose:** Automatically generate agent tools from OpenAPI specifications for REST API integration.

**How it Works:**
The `OpenAPIToolset` parses OpenAPI specs (JSON/YAML) and creates `RestApiTool` instances for each API operation.

**Basic Example:**

```python
from google.adk.tools.openapi_tool.openapi_spec_parser import OpenAPIToolset
from google.adk.agents import LlmAgent
import json

# Load OpenAPI spec
with open("api_spec.json") as f:
    openapi_spec = json.load(f)

# Create toolset
toolset = OpenAPIToolset(
    spec_str=json.dumps(openapi_spec),
    spec_str_type='json',
    auth_scheme='bearer',
    auth_credential='YOUR_API_TOKEN'
)

agent = LlmAgent(
    name="api_agent",
    model="gemini-2.0-flash",
    tools=[toolset]
)
```

**Process:**
1. **Parsing** - Accepts specs as dict, JSON, or YAML; resolves `$ref`
2. **Discovery** - Identifies operations (GET, POST, PUT, DELETE)
3. **Generation** - Creates RestApiTool per operation with:
   - Name from `operationId` (snake_case, max 60 chars)
   - Description from `summary` or `description`
   - Dynamic schema from parameters and request body

**Authentication:**
Configure globally via `auth_scheme` and `auth_credential` parameters.

**See:** `ADK-OPENAPI-TOOLS-GUIDE.md` for comprehensive REST API integration guide.

---

## Google Cloud Tools

### BigQuery Toolset

**Purpose:** Query datasets, execute SQL, forecast time series, and extract data insights.

**Capabilities:**
- Dataset and table queries
- SQL execution
- Time series forecasting
- Data insights generation

**Example:**

```python
from google.adk.tools import BigQueryToolset
from google.adk.agents import LlmAgent

bq_toolset = BigQueryToolset(
    project_id="my-project",
    dataset_id="analytics"
)

agent = LlmAgent(
    name="data_analyst_agent",
    model="gemini-2.0-flash",
    tools=[bq_toolset]
)
```

**Use Cases:**
- Ad-hoc data analysis
- Business intelligence queries
- Predictive analytics
- Data exploration

---

### Spanner Toolset

**Purpose:** Manage schemas, execute SQL queries, and perform similarity searches on Cloud Spanner databases.

**Capabilities:**
- Table schema management
- SQL query execution
- Similarity search operations

**Example:**

```python
from google.adk.tools import SpannerToolset

spanner_toolset = SpannerToolset(
    instance_id="my-instance",
    database_id="my-database"
)

agent = LlmAgent(
    name="spanner_agent",
    model="gemini-2.0-flash",
    tools=[spanner_toolset]
)
```

**Use Cases:**
- Global database queries
- Schema introspection
- Vector similarity search

---

### Bigtable Toolset

**Purpose:** List instances/tables, retrieve metadata, and execute SQL queries on Bigtable.

**Capabilities:**
- Instance and table listing
- Metadata retrieval
- SQL query execution

**Use Cases:**
- NoSQL data retrieval
- Wide-column store queries
- Real-time analytics

---

### Vertex AI RAG Engine

**Purpose:** Retrieve information from pre-configured private RAG corpora.

**Requirements:**
- Pre-configured RAG corpus in Vertex AI
- Corpus ID for connection

**Example:**

```python
from google.adk.tools import VertexAiRagEngineTool

rag_tool = VertexAiRagEngineTool(
    corpus_id="projects/PROJECT_ID/locations/LOCATION/ragCorpora/CORPUS_ID"
)

agent = LlmAgent(
    name="rag_agent",
    model="gemini-2.0-flash",
    tools=[rag_tool]
)
```

**Use Cases:**
- Private document search
- Enterprise knowledge retrieval
- Domain-specific Q&A

---

### Vertex AI Search

**Purpose:** Search configured private data stores using Google Cloud Vertex AI.

**Requirements:**
- Pre-configured Vertex AI Search data store
- Data store ID for connection

**Example:**

```python
from google.adk.tools import VertexAiSearchTool

search_tool = VertexAiSearchTool(
    data_store_id="my-data-store",
    bypass_multi_tools_limit=True  # Allows use with other tools
)

agent = LlmAgent(
    name="search_agent",
    model="gemini-2.0-flash",
    tools=[search_tool]
)
```

**Use Cases:**
- Enterprise document search
- Private data retrieval
- Custom search experiences

---

### Apigee API Hub Tools

**Purpose:** Convert documented APIs from Apigee API Hub into agent tools.

**Authentication Support:**
- Token-based (API keys, bearer tokens)
- Service accounts
- OpenID Connect

**Use Cases:**
- Custom API access
- Apigee-hosted services
- Managed API catalogs

---

### Application Integration Toolset

**Purpose:** Access 100+ pre-built connectors for enterprise systems.

**Supported Systems:**
- Salesforce
- ServiceNow
- SAP
- On-premise applications
- SaaS applications

**Authentication:**
- Dynamic OAuth2 support
- Service account authentication (production recommended)

**Integration Methods:**
- **Integration Connectors:** Entity operations and custom actions
- **Application Workflows:** Invoke existing workflow automations

**Use Cases:**
- Federated search across enterprise systems
- Workflow automation via agents
- Secure on-premise system access
- Multi-system data queries

---

## Third-Party Tools

### Web Scraping Tools
- **AgentQL** - AI-powered web scraping
- **Firecrawl** - Web page content extraction
- **Browserbase** - Headless browser automation

### Search Platforms
- **Exa** - Semantic search API
- **Tavily** - AI-optimized search

### Productivity Apps
- **GitHub** - Repository management and code search
- **Notion** - Workspace and document access
- **Hugging Face** - Model and dataset integration

---

## Tool Selection Guide

### Decision Matrix

| Use Case | Recommended Tool Type | Rationale |
|----------|----------------------|-----------|
| Web search for current info | Google Search | Built-in grounding, real-time data |
| Execute calculations | Code Execution | Fast, native Python support |
| Query structured data | BigQuery/Spanner/Bigtable | Direct database integration |
| Search private documents | Vertex AI Search/RAG Engine | Enterprise data security |
| Call REST APIs | OpenAPI Tools | Auto-generated from specs |
| Custom business logic | Function Tools | Full control, Python native |
| Integrate external systems | MCP Tools | Standardized protocol |
| Connect to SaaS apps | Application Integration | Pre-built connectors |
| Web scraping | Third-party tools (AgentQL) | Specialized capabilities |

### Multi-Tool Scenarios

**Pattern 1: Research Assistant**
```python
agent = LlmAgent(
    name="research_agent",
    tools=[
        google_search,           # Web search
        VertexAiSearchTool(...), # Private docs (bypass_multi_tools_limit=True)
        BigQueryToolset(...)     # Data analysis
    ]
)
```

**Pattern 2: Customer Service Agent**
```python
agent = LlmAgent(
    name="support_agent",
    tools=[
        get_customer_info,       # Function tool
        search_knowledge_base,   # Function tool
        create_support_ticket    # Function tool
    ]
)
```

**Pattern 3: Data Engineer Agent**
```python
agent = LlmAgent(
    name="data_agent",
    tools=[
        BigQueryToolset(...),    # Query data
        code_execution,          # Transform data
        SpannerToolset(...)      # Update schemas
    ]
)
```

---

## Architecture Patterns

### Tool Registration Pattern

```python
from google.adk.agents import LlmAgent

# Method 1: Direct registration
agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash",
    tools=[tool1, tool2, tool3]
)

# Method 2: Dynamic registration
tools = []
if needs_search:
    tools.append(google_search)
if needs_data:
    tools.append(BigQueryToolset(...))

agent = LlmAgent(name="dynamic_agent", model="gemini-2.0-flash", tools=tools)
```

### Tool Composition Pattern

```python
# Combine multiple toolsets
all_tools = [
    google_search,                   # Built-in
    get_user_data,                   # Function tool
    OpenAPIToolset(...),             # REST API
    MCPToolset(...),                 # MCP server
    BigQueryToolset(...)             # Cloud tool
]

agent = LlmAgent(
    name="composed_agent",
    model="gemini-2.0-flash",
    tools=all_tools
)
```

### Tool Inheritance Pattern (Sub-Agents)

```python
# Root agent with comprehensive tools
root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.0-flash",
    tools=[
        research_agent,  # Sub-agent for research
        data_agent,      # Sub-agent for data
        api_agent        # Sub-agent for API calls
    ]
)

# Sub-agents have specialized tools
research_agent = LlmAgent(
    name="researcher",
    tools=[google_search, VertexAiSearchTool(...)]
)
```

**Note:** Built-in tools (except Google Search/Vertex AI Search with `bypass_multi_tools_limit=True`) cannot be used in sub-agents.

---

## Best Practices

### 1. Tool Design Principles

**Minimize Parameters:**
- Keep parameter counts low (ideally 3-5)
- Reduce LLM confusion and token usage

**Use Simple Data Types:**
- Favor primitives: `str`, `int`, `float`, `bool`
- Avoid custom classes or complex objects

**Meaningful Naming:**
- Choose descriptive function/parameter names
- Avoid generic labels like `do_stuff()` or `param1`

**Parallel Execution:**
- Design functions for asynchronous operation
- Enable multiple tool calls simultaneously

**Descriptive Returns:**
- Return dictionaries with structured data
- Include human-readable explanations, not just error codes
- Always include a "status" field ("success", "error")

### 2. Documentation Standards

**Comprehensive Docstrings:**
```python
def analyze_sentiment(text: str, language: str = "en") -> dict:
    """Analyzes the sentiment of given text.

    Evaluates emotional tone (positive, negative, neutral) using NLP.

    Args:
        text (str): The text to analyze. Should be at least 10 characters.
        language (str): ISO 639-1 language code (e.g., 'en', 'es', 'fr').
                       Defaults to English ('en').

    Returns:
        dict: Sentiment analysis results containing:
            - sentiment (str): 'positive', 'negative', or 'neutral'
            - confidence (float): Confidence score (0.0 to 1.0)
            - status (str): 'success' or 'error'
            - message (str): Human-readable explanation

    Example:
        >>> analyze_sentiment("I love this product!", "en")
        {"sentiment": "positive", "confidence": 0.95, "status": "success"}
    """
    pass
```

### 3. Error Handling

**Return Status Fields:**
```python
def get_user(user_id: str) -> dict:
    """Retrieves user information."""
    try:
        user = database.get_user(user_id)
        return {
            "user": user,
            "status": "success",
            "message": f"Successfully retrieved user {user_id}"
        }
    except UserNotFoundError:
        return {
            "status": "error",
            "message": f"User {user_id} not found in database"
        }
    except DatabaseError as e:
        return {
            "status": "error",
            "message": f"Database error: {str(e)}"
        }
```

**Avoid Raising Exceptions:**
- Return error dictionaries instead of raising exceptions
- Include actionable error messages for the LLM

### 4. State Management

**Use Temporary State for Data Sharing:**
```python
from google.adk.sessions import InvocationContext

def tool1(ctx: InvocationContext, query: str) -> dict:
    """First tool stores results in temp state."""
    results = perform_search(query)
    ctx.session.state.put("temp:search_results", results)
    return {"status": "success", "count": len(results)}

def tool2(ctx: InvocationContext) -> dict:
    """Second tool retrieves results from temp state."""
    results = ctx.session.state.get("temp:search_results")
    processed = process_results(results)
    return {"status": "success", "data": processed}
```

**Temp State Rules:**
- Use `temp:` prefix for single-invocation data
- All tools in one agent turn share the same `InvocationContext`
- Temp state cleared after agent turn completes

### 5. Authentication Management

**Centralized Configuration:**
```python
# OpenAPI tools - set auth globally
toolset = OpenAPIToolset(
    spec_str=spec,
    spec_str_type='json',
    auth_scheme='bearer',
    auth_credential=os.getenv("API_TOKEN")
)

# Function tools - use environment variables
def call_api(endpoint: str) -> dict:
    """Calls external API with auth."""
    headers = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()
```

**Never Hardcode Credentials:**
- Use environment variables or secret managers
- Configure auth at toolset level when possible

### 6. Performance Optimization

**Async Operations:**
```python
import asyncio

async def fetch_data_async(source: str) -> dict:
    """Async tool for parallel execution."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/{source}")
        return response.json()
```

**Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
    """Cached exchange rate lookup."""
    rate = fetch_rate(from_currency, to_currency)
    return {"rate": rate, "status": "success"}
```

### 7. Testing Tools

**Unit Testing:**
```python
import pytest

def test_get_weather():
    result = get_weather("San Francisco", "Celsius")
    assert result["status"] == "success"
    assert "temperature" in result
    assert result["unit"] == "Celsius"

def test_get_weather_invalid_city():
    result = get_weather("InvalidCity123", "Celsius")
    assert result["status"] == "error"
    assert "not found" in result["message"].lower()
```

**Integration Testing:**
```python
def test_agent_with_tool():
    agent = LlmAgent(
        name="test_agent",
        model="gemini-2.0-flash",
        tools=[get_weather]
    )

    response = agent.send_message("What's the weather in Paris?")
    assert "temperature" in response.text.lower()
```

---

## Limitations

### Built-in Tool Restrictions

**Single Built-in Tool Limit:**
Currently, for each root agent or single agent, only one built-in tool is supported. No other tools of any type can be used in the same agent.

**Exception:** In Python, `GoogleSearchTool` and `VertexAiSearchTool` can use `bypass_multi_tools_limit=True` to work with other tools.

**Sub-Agent Restrictions:**
Built-in tools cannot be used within sub-agents (except the noted exception with `bypass_multi_tools_limit=True`).

### Model Compatibility

**Google Search:**
- Compatible only with Gemini 2 models
- Requires displaying search suggestions UI in production

**Code Execution (GKE):**
- Requires GKE cluster setup and configuration
- Additional RBAC permissions needed
- Install requirement: `pip install google-adk[gke]`

### Deployment Constraints

**MCP Tools:**
- Agent and MCPToolset must be defined synchronously in `agent.py`
- `adk web` allows async agent creation, but deployment requires synchronous

**Authentication:**
- Some tools require pre-configured credentials
- Service account setup may be needed for Google Cloud tools

### Performance Considerations

**Quotas and Rate Limits:**
- Google Search subject to quotas
- Cloud tools subject to GCP service limits
- Third-party tools have their own rate limits

**Latency:**
- Tool execution adds latency to agent responses
- Network calls (REST APIs, MCP servers) increase response time
- Consider async operations for parallel tool execution

### Functionality Gaps

**Variadic Parameters:**
- `*args` and `**kwargs` are ignored by ADK
- Not available to LLM for invocation

**Complex Data Types:**
- Custom classes not recommended
- Stick to JSON-serializable types

---

## Quick Reference

### Tool Type Comparison

| Tool Type | Best For | Complexity | Setup Time | Flexibility |
|-----------|----------|------------|------------|-------------|
| Built-in | Web search, code execution | Low | Immediate | Low |
| Function Tools | Custom logic | Low | Minutes | High |
| OpenAPI Tools | REST APIs | Medium | Hours | Medium |
| MCP Tools | Standardized integrations | Medium | Hours | Medium |
| Cloud Tools | GCP services | Medium | Hours | Medium |
| Third-party | Specialized tasks | Variable | Variable | Variable |

### Common Patterns

```python
# Pattern 1: Single built-in tool
agent = LlmAgent(tools=[google_search])

# Pattern 2: Multiple function tools
agent = LlmAgent(tools=[tool1, tool2, tool3])

# Pattern 3: Toolset
agent = LlmAgent(tools=[OpenAPIToolset(...)])

# Pattern 4: Mixed (with bypass)
agent = LlmAgent(tools=[
    VertexAiSearchTool(bypass_multi_tools_limit=True),
    function_tool1,
    function_tool2
])

# Pattern 5: Sub-agents
orchestrator = LlmAgent(tools=[specialist_agent1, specialist_agent2])
```

### Next Steps

1. **Function Tools:** See `ADK-FUNCTION-TOOLS-GUIDE.md` for detailed implementation
2. **MCP Tools:** See `ADK-MCP-TOOLS-GUIDE.md` for server integration
3. **OpenAPI Tools:** See `ADK-OPENAPI-TOOLS-GUIDE.md` for REST API integration
4. **Official Docs:** https://google.github.io/adk-docs/tools/

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Related Documents:**
- ADK-FUNCTION-TOOLS-GUIDE.md
- ADK-MCP-TOOLS-GUIDE.md
- ADK-OPENAPI-TOOLS-GUIDE.md
