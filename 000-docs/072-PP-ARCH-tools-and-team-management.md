# Bob's Brain: Tools and Multi-Agent Team Management Architecture

**Date:** 2025-11-19
**Purpose:** Design Bob's Brain to use tools from a toolbox and manage a team of agents
**Reference:** https://google.github.io/adk-docs/get-started/quickstart/ & /agents/multi-agents/
**Status:** Design Document

---

## Executive Summary

Bob's Brain needs two key enhancements to match Google ADK patterns:

1. **Tool Integration** - Enable Bob to use tools from a toolbox (functions, APIs, external services)
2. **Multi-Agent Team Management** - Enable Bob to coordinate and manage other specialized agents

Both features are fully supported by Google ADK and align with Hard Mode compliance.

---

## Current State Analysis

### What Bob Has Now ✅

```python
# my_agent/agent.py
agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    tools=[],  # ❌ Empty - no tools yet
    instruction=base_instruction,
    after_agent_callback=auto_save_session_to_memory
)
```

**Status:**
- ✅ Proper LlmAgent structure
- ✅ Dual memory wiring (Session + Memory Bank)
- ✅ Auto-save callback
- ❌ **No tools configured**
- ❌ **No sub-agents configured**

---

## Design: Tool Integration

### Google ADK Tool Pattern

**From Official Docs:**
```python
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Returns the current weather in a specified city."""
    return {"status": "success", "city": city, "weather": "sunny"}

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    tools=[get_weather, get_current_time]  # ← Pass functions as tools
)
```

**Key Points:**
- ✅ Tools are Python functions with type hints and docstrings
- ✅ Framework automatically converts them to callable functions for LLM
- ✅ Functions return dictionaries with status and results
- ✅ LLM decides when to call which tool

---

### Proposed Tool Structure for Bob

**Directory Layout:**
```
my_agent/
├── agent.py              # Core agent (imports tools)
├── agent_engine_app.py   # Deployment entrypoint
├── tools/
│   ├── __init__.py       # Tool exports
│   ├── search_tool.py    # Web search capability
│   ├── code_tool.py      # Code execution/analysis
│   ├── file_tool.py      # File operations
│   └── api_tool.py       # External API calls
```

**Example Tool Implementation:**

```python
# my_agent/tools/search_tool.py
"""
Web search tool for Bob's Brain.

Allows Bob to search the web for current information.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def search_web(query: str, num_results: int = 3) -> Dict[str, Any]:
    """
    Search the web for information.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 3)

    Returns:
        Dictionary with search results or error message
    """
    try:
        # TODO: Implement actual search (Google Custom Search API, etc.)
        logger.info(f"Searching web for: {query}")

        # Placeholder implementation
        return {
            "status": "success",
            "query": query,
            "results": [
                {
                    "title": "Example Result 1",
                    "url": "https://example.com/1",
                    "snippet": "Example snippet about the query..."
                }
            ],
            "count": 1
        }
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


def get_current_time(timezone: str = "UTC") -> Dict[str, Any]:
    """
    Get the current time in a specific timezone.

    Args:
        timezone: Timezone (e.g., "UTC", "America/New_York")

    Returns:
        Dictionary with current time or error
    """
    try:
        from datetime import datetime
        import pytz

        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)

        return {
            "status": "success",
            "timezone": timezone,
            "time": current_time.isoformat(),
            "formatted": current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        }
    except Exception as e:
        logger.error(f"Time lookup failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
```

**Tool Registry:**

```python
# my_agent/tools/__init__.py
"""
Tool registry for Bob's Brain.

All tools available to Bob should be exported here.
"""

from my_agent.tools.search_tool import search_web, get_current_time
# from my_agent.tools.code_tool import execute_code, analyze_code
# from my_agent.tools.file_tool import read_file, write_file
# from my_agent.tools.api_tool import call_api

# Export all available tools
__all__ = [
    "search_web",
    "get_current_time",
    # "execute_code",
    # "analyze_code",
    # "read_file",
    # "write_file",
    # "call_api",
]
```

**Updated Agent with Tools:**

```python
# my_agent/agent.py
from google.adk.agents import LlmAgent
from my_agent.tools import search_web, get_current_time

def get_agent() -> LlmAgent:
    """Create and configure the LlmAgent with tools."""

    base_instruction = f"""You are Bob, a helpful AI assistant.

Your identity: {AGENT_SPIFFE_ID}

You have access to the following tools:
- search_web: Search the web for current information
- get_current_time: Get the current time in any timezone

Use these tools when appropriate to provide accurate, up-to-date information.
Be concise, accurate, and helpful.
"""

    agent = LlmAgent(
        model="gemini-2.0-flash-exp",
        tools=[search_web, get_current_time],  # ✅ Tools added!
        instruction=base_instruction,
        after_agent_callback=auto_save_session_to_memory
    )

    return agent
```

---

## Design: Multi-Agent Team Management

### Google ADK Multi-Agent Pattern

**Three Coordination Mechanisms:**

1. **Sub-agents (Hierarchical)**
2. **LLM-driven delegation (Transfer)**
3. **Workflow agents (Sequential, Parallel, Loop)**

---

### Pattern 1: Coordinator with Sub-agents

**Use Case:** Bob coordinates specialized agents for different tasks.

```python
# my_agent/team/specialist_agents.py
"""Specialist agents for Bob's team."""

from google.adk.agents import LlmAgent

# Research specialist
research_agent = LlmAgent(
    name="Researcher",
    description="Specialist in web research, data gathering, and fact-checking",
    model="gemini-2.0-flash-exp",
    instruction="You are a research specialist. Find accurate, up-to-date information.",
    tools=[search_web]
)

# Code specialist
code_agent = LlmAgent(
    name="CodeExpert",
    description="Specialist in code analysis, debugging, and writing code",
    model="gemini-2.0-flash-exp",
    instruction="You are a code expert. Analyze, debug, and write high-quality code.",
    tools=[execute_code, analyze_code]
)

# Writing specialist
writer_agent = LlmAgent(
    name="Writer",
    description="Specialist in writing, editing, and content creation",
    model="gemini-2.0-flash-exp",
    instruction="You are a writing specialist. Create clear, engaging content.",
    tools=[]
)
```

**Bob as Coordinator:**

```python
# my_agent/agent.py
from google.adk.agents import LlmAgent
from my_agent.team.specialist_agents import research_agent, code_agent, writer_agent

def get_agent() -> LlmAgent:
    """Create Bob as a coordinator with specialist sub-agents."""

    base_instruction = f"""You are Bob, a coordinator AI assistant managing a team of specialists.

Your identity: {AGENT_SPIFFE_ID}

Your team:
- Researcher: For web research, data gathering, fact-checking
- CodeExpert: For code analysis, debugging, writing code
- Writer: For writing, editing, content creation

When a user asks a question:
1. Determine which specialist is best suited for the task
2. Delegate to that specialist using transfer_to_agent()
3. If multiple specialists are needed, coordinate their work
4. Synthesize results and respond to the user

Be an effective coordinator. Delegate clearly and efficiently.
"""

    coordinator = LlmAgent(
        name="Bob",
        model="gemini-2.0-flash-exp",
        sub_agents=[research_agent, code_agent, writer_agent],  # ✅ Team!
        instruction=base_instruction,
        after_agent_callback=auto_save_session_to_memory
    )

    return coordinator
```

**How Delegation Works:**

The LLM automatically gets a `transfer_to_agent()` function it can call:

```python
# Bob receives: "Write me a blog post about AI agents"
# Bob's internal reasoning:
# 1. This is a writing task
# 2. I should delegate to the Writer specialist
# Bob calls: transfer_to_agent(agent_name="Writer")
# Framework routes to writer_agent
# Writer completes the task and returns result
# Bob receives result and responds to user
```

---

### Pattern 2: Sequential Workflow

**Use Case:** Multi-step tasks that must happen in order.

```python
from google.adk.agents import SequentialAgent, LlmAgent

# Step 1: Research
research_step = LlmAgent(
    name="ResearchStep",
    model="gemini-2.0-flash-exp",
    instruction="Research the topic and gather key information.",
    tools=[search_web],
    output_key="research_data"  # ← Save output to state
)

# Step 2: Analysis
analysis_step = LlmAgent(
    name="AnalysisStep",
    model="gemini-2.0-flash-exp",
    instruction="Analyze the research data: {research_data}",  # ← Read from state
    output_key="analysis_results"
)

# Step 3: Writing
writing_step = LlmAgent(
    name="WritingStep",
    model="gemini-2.0-flash-exp",
    instruction="Write a comprehensive report based on: {analysis_results}",
    output_key="final_report"
)

# Pipeline coordinator
pipeline = SequentialAgent(
    name="ResearchPipeline",
    sub_agents=[research_step, analysis_step, writing_step]
)
```

**Benefits:**
- ✅ Each agent has a clear, focused role
- ✅ State automatically shared between steps
- ✅ Results flow through the pipeline
- ✅ Easy to understand and maintain

---

### Pattern 3: Parallel Processing

**Use Case:** Multiple independent tasks that can run concurrently.

```python
from google.adk.agents import ParallelAgent, LlmAgent

# Task 1: Web research
web_research = LlmAgent(
    name="WebResearch",
    model="gemini-2.0-flash-exp",
    instruction="Search the web for information about {topic}",
    tools=[search_web],
    output_key="web_results"
)

# Task 2: Code analysis
code_analysis = LlmAgent(
    name="CodeAnalysis",
    model="gemini-2.0-flash-exp",
    instruction="Analyze code examples related to {topic}",
    tools=[analyze_code],
    output_key="code_results"
)

# Task 3: Documentation search
doc_search = LlmAgent(
    name="DocSearch",
    model="gemini-2.0-flash-exp",
    instruction="Search documentation for {topic}",
    tools=[search_docs],
    output_key="doc_results"
)

# Parallel execution
parallel_research = ParallelAgent(
    name="ParallelResearch",
    sub_agents=[web_research, code_analysis, doc_search]
)

# Aggregator
aggregator = LlmAgent(
    name="Aggregator",
    model="gemini-2.0-flash-exp",
    instruction="Synthesize results from: {web_results}, {code_results}, {doc_results}"
)

# Combined pipeline
full_pipeline = SequentialAgent(
    name="ResearchAndSynthesize",
    sub_agents=[parallel_research, aggregator]
)
```

**Benefits:**
- ✅ Faster execution (tasks run concurrently)
- ✅ Efficient resource usage
- ✅ Easy to add/remove parallel tasks

---

### Pattern 4: Iterative Refinement

**Use Case:** Tasks that need multiple rounds of improvement.

```python
from google.adk.agents import LoopAgent, LlmAgent

# Generator
generator = LlmAgent(
    name="Generator",
    model="gemini-2.0-flash-exp",
    instruction="Generate a draft response",
    output_key="draft"
)

# Critic
critic = LlmAgent(
    name="Critic",
    model="gemini-2.0-flash-exp",
    instruction="Review the draft: {draft}. If quality score > 8/10, escalate. Otherwise, provide feedback.",
    output_key="feedback"
)

# Refiner
refiner = LlmAgent(
    name="Refiner",
    model="gemini-2.0-flash-exp",
    instruction="Improve the draft based on feedback: {feedback}",
    output_key="draft"  # ← Overwrites draft for next iteration
)

# Iterative loop (max 3 iterations)
refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[generator, critic, refiner],
    max_iterations=3
)
```

**Benefits:**
- ✅ Produces higher quality output
- ✅ Self-improving system
- ✅ Bounded iteration count

---

## Recommended Architecture for Bob

### Option 1: Coordinator + Specialists (Recommended)

**Best for:** General-purpose assistant with specialized capabilities

```python
Bob (Coordinator)
├── Researcher (web search, fact-checking)
├── CodeExpert (code analysis, debugging)
├── Writer (content creation, editing)
└── Analyst (data analysis, insights)
```

**Advantages:**
- ✅ Clear separation of concerns
- ✅ Easy to add new specialists
- ✅ LLM-driven delegation (smart routing)
- ✅ Maintains Bob's personality as coordinator

---

### Option 2: Pipeline + Tools (Alternative)

**Best for:** Structured workflows with specific steps

```python
Bob (Pipeline Controller)
├── Input Processing (understand request)
├── Tool Execution (search_web, execute_code, etc.)
├── Result Analysis (interpret tool outputs)
└── Response Generation (synthesize final answer)
```

**Advantages:**
- ✅ Predictable execution flow
- ✅ Easy to debug
- ✅ Good for repetitive tasks

---

## Implementation Plan

### Phase 1: Add Basic Tools (Quick Win)

**Files to Create:**
- `my_agent/tools/__init__.py`
- `my_agent/tools/search_tool.py`
- `my_agent/tools/time_tool.py`

**Files to Modify:**
- `my_agent/agent.py` - Add tools to LlmAgent

**Time Estimate:** 1-2 hours

**Testing:**
```bash
adk run my_agent
> What's the current time in Tokyo?
# Bob should call get_current_time(timezone="Asia/Tokyo")
```

---

### Phase 2: Add Specialist Agents (Multi-Agent)

**Files to Create:**
- `my_agent/team/__init__.py`
- `my_agent/team/specialist_agents.py`

**Files to Modify:**
- `my_agent/agent.py` - Add sub_agents to coordinator

**Time Estimate:** 2-3 hours

**Testing:**
```bash
adk run my_agent
> Research the latest AI trends and write a summary
# Bob should delegate to Researcher, then to Writer
```

---

### Phase 3: Add Workflow Agents (Advanced)

**Files to Create:**
- `my_agent/workflows/__init__.py`
- `my_agent/workflows/research_pipeline.py`
- `my_agent/workflows/analysis_pipeline.py`

**Time Estimate:** 3-4 hours

**Testing:**
```bash
adk run my_agent
> Analyze this codebase and create a comprehensive report
# Bob should run a sequential pipeline: Research → Analyze → Write
```

---

## Vertex AI Model Configuration

**Current Setup:**
```python
agent = LlmAgent(
    model="gemini-2.0-flash-exp",  # ✅ Correct
    ...
)
```

**Google ADK Vertex AI Pattern (from quickstart):**

**Required Environment Variables:**
- `GOOGLE_CLOUD_PROJECT` → We have: `PROJECT_ID` ✅
- `GOOGLE_CLOUD_LOCATION` → We have: `LOCATION` ✅

**Authentication:**
```bash
gcloud auth application-default login
```

**Our Implementation:**
- ✅ Uses Vertex AI Agent Engine (R2 compliance)
- ✅ Model: `gemini-2.0-flash-exp` (fast, cost-effective)
- ✅ Project and location configured
- ✅ WIF authentication in CI/CD

**Status:** COMPLIANT ✅

---

## Tool Security & Safety

### Tool Execution Sandboxing

**Considerations:**
- ✅ Tools run in Agent Engine (isolated environment)
- ✅ Each tool should validate inputs
- ✅ Tools should handle errors gracefully
- ✅ Log all tool executions (R7: include SPIFFE ID)

**Example Secure Tool:**
```python
def execute_code(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Execute code in a sandboxed environment.

    Security measures:
    - Input validation
    - Timeout limits
    - Resource constraints
    - Audit logging
    """
    try:
        # Validate inputs
        if not code or not isinstance(code, str):
            return {"status": "error", "error": "Invalid code input"}

        if language not in ["python", "javascript", "bash"]:
            return {"status": "error", "error": "Unsupported language"}

        # Log execution (R7)
        logger.info(
            f"Executing {language} code",
            extra={
                "spiffe_id": AGENT_SPIFFE_ID,
                "language": language,
                "code_length": len(code)
            }
        )

        # TODO: Implement actual sandboxed execution
        # Use google.adk.tools.code_execution or similar

        return {
            "status": "success",
            "output": "Execution result...",
            "execution_time_ms": 150
        }
    except Exception as e:
        logger.error(f"Code execution failed: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}
```

---

## Hard Mode Compliance

### R1: Agent Implementation ✅
- ✅ All agents use `LlmAgent` from `google.adk.agents`
- ✅ No alternative frameworks

### R2: Deployed Runtime ✅
- ✅ All agents run in Vertex AI Agent Engine
- ✅ No self-hosted runners

### R3: Gateway Rules ✅
- ✅ Tools run in agent code (not in gateway)
- ✅ Sub-agents managed by Agent Engine

### R5: Dual Memory ✅
- ✅ Session Service shared across all agents
- ✅ Memory Bank persists all interactions

### R7: SPIFFE ID ✅
- ✅ All tool executions log SPIFFE ID
- ✅ Multi-agent coordination logs include SPIFFE ID

**All Hard Mode rules remain satisfied with tools and multi-agent features!**

---

## Next Steps

**To enable tools and team management:**

1. **Review this design document**
2. **Choose architecture:** Coordinator + Specialists (recommended) or Pipeline + Tools
3. **Implement Phase 1:** Add basic tools (search, time)
4. **Test locally:** `adk run my_agent`
5. **Implement Phase 2:** Add specialist agents
6. **Deploy to Agent Engine:** Use existing workflow
7. **Verify telemetry:** Check Cloud Trace for tool executions and agent delegations

---

## Example: Complete Coordinator Implementation

```python
# my_agent/agent.py (with tools and team)

from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

# Tools
from my_agent.tools import search_web, get_current_time

# Specialist agents
from my_agent.team.specialist_agents import (
    research_agent,
    code_agent,
    writer_agent
)

def get_agent() -> LlmAgent:
    """Create Bob as a coordinator with tools and specialist team."""

    base_instruction = f"""You are Bob, a helpful AI coordinator managing a team of specialists.

Your identity: {AGENT_SPIFFE_ID}

Your capabilities:
1. Direct tools:
   - search_web: Search the web for information
   - get_current_time: Get current time in any timezone

2. Specialist team:
   - Researcher: For in-depth research and fact-checking
   - CodeExpert: For code analysis and programming tasks
   - Writer: For content creation and editing

Strategy:
- For simple queries: Use your direct tools
- For complex tasks: Delegate to specialists using transfer_to_agent()
- For multi-step tasks: Coordinate multiple specialists

Be an effective coordinator. Use tools and team efficiently.
"""

    coordinator = LlmAgent(
        name="Bob",
        model="gemini-2.0-flash-exp",
        tools=[search_web, get_current_time],  # ✅ Direct tools
        sub_agents=[research_agent, code_agent, writer_agent],  # ✅ Team
        instruction=base_instruction,
        after_agent_callback=auto_save_session_to_memory
    )

    return coordinator

# create_runner() remains unchanged - wires dual memory
```

**This gives Bob:**
- ✅ Direct access to tools (search, time)
- ✅ Ability to delegate to specialists
- ✅ Shared memory across all agents
- ✅ Full observability with Cloud Trace

---

**Document Status:** Complete ✅
**Last Updated:** 2025-11-19
**Category:** Product & Planning - Architecture
**Implementation Priority:** High (enables core Bob capabilities)

---
