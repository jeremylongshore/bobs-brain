# Bob's Brain: Grounding in ADK Documentation - Become an ADK Expert

**Date:** 2025-11-19
**Purpose:** Ground Bob in comprehensive ADK documentation to become a source of knowledge for creating agents
**Priority:** HIGH - Core capability for Bob's value proposition
**Status:** Planning

---

## Executive Summary

**Goal:** Transform Bob into an **ADK Expert** who can help developers create, deploy, and troubleshoot ADK agents by grounding him in all current ADK documentation.

**Strategy:** Use Google ADK's built-in **grounding capabilities** to connect Bob to:
1. Local ADK reference documentation (symlinked in `000-docs/google-reference/adk/`)
2. Live web documentation (https://google.github.io/adk-docs)
3. Memory Bank for learned patterns and examples
4. Code execution for testing agent code

**Outcome:** Bob becomes a reliable source for:
- ✅ Creating new ADK agents
- ✅ Debugging agent issues
- ✅ Best practices and patterns
- ✅ Deployment guidance
- ✅ Tool integration help

---

## Current State Analysis

### What Bob Has Now

**Documentation Available (Symlinked):**
```
000-docs/google-reference/adk/
├── ADK_COMPREHENSIVE_DOCUMENTATION.md (46KB)
├── GOOGLE_ADK_PYTHON_API_REFERENCE.md (78KB)
├── GOOGLE_ADK_CLI_REFERENCE.md (10KB)
├── ADK_QUICK_REFERENCE.md (11KB)
└── ... (10 total files, ~270KB)
```

**Bob's Current Capabilities:**
- ✅ LlmAgent with Gemini 2.0 Flash
- ✅ Dual memory (Session + Memory Bank)
- ✅ Auto-save callback
- ❌ **No grounding/RAG configured**
- ❌ **No tools to access documentation**
- ❌ **No ADK-specific instructions**

---

## Grounding Strategies (3 Approaches)

### Option 1: File-Based Grounding (Simplest)

**How it works:**
- Bob has a tool that reads local ADK documentation files
- LLM decides when to use the tool
- Returns relevant sections from docs

**Implementation:**
```python
# my_agent/tools/adk_docs_tool.py

def search_adk_docs(query: str, doc_type: str = "all") -> Dict[str, Any]:
    """
    Search ADK documentation for information.

    Args:
        query: Search query (e.g., "how to deploy agent engine")
        doc_type: Type of doc (all, api, cli, comprehensive, quickstart)

    Returns:
        Relevant documentation sections
    """
    import os
    from pathlib import Path

    docs_dir = Path("000-docs/google-reference/adk/")

    # Map doc types to files
    doc_map = {
        "api": "GOOGLE_ADK_PYTHON_API_REFERENCE.md",
        "cli": "GOOGLE_ADK_CLI_REFERENCE.md",
        "comprehensive": "ADK_COMPREHENSIVE_DOCUMENTATION.md",
        "quickstart": "ADK_QUICK_REFERENCE.md"
    }

    results = []

    # Search relevant files
    if doc_type == "all":
        files = list(docs_dir.glob("*.md"))
    else:
        files = [docs_dir / doc_map.get(doc_type, "ADK_COMPREHENSIVE_DOCUMENTATION.md")]

    for file_path in files:
        content = file_path.read_text()

        # Simple keyword search (can be improved with embeddings)
        if query.lower() in content.lower():
            # Extract relevant section
            lines = content.split('\n')
            relevant_lines = []

            for i, line in enumerate(lines):
                if query.lower() in line.lower():
                    # Get context (10 lines before and after)
                    start = max(0, i - 10)
                    end = min(len(lines), i + 10)
                    relevant_lines.append('\n'.join(lines[start:end]))

            results.append({
                "file": file_path.name,
                "matches": relevant_lines[:3]  # Top 3 matches
            })

    return {
        "status": "success",
        "query": query,
        "results": results[:5]  # Top 5 files
    }
```

**Pros:**
- ✅ Simple to implement
- ✅ Works offline
- ✅ No external dependencies

**Cons:**
- ⚠️ Basic keyword search (not semantic)
- ⚠️ May miss relevant context

---

### Option 2: Vertex AI Search Grounding (Recommended)

**How it works:**
- Use Vertex AI Search & Conversation for semantic search
- Index ADK documentation in Vertex AI
- Bob uses grounding API to search

**Implementation:**
```python
# my_agent/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools.google_cloud import VertexAiSearchTool

# Create Vertex AI Search tool
adk_search_tool = VertexAiSearchTool(
    project_id=PROJECT_ID,
    location=LOCATION,
    search_engine_id="adk-documentation",  # Created in Vertex AI Console
    name="search_adk_docs",
    description="Search ADK documentation for agent development guidance"
)

agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    tools=[adk_search_tool],  # Bob can search ADK docs
    instruction=f"""You are Bob, an ADK Expert AI assistant.

You help developers create, deploy, and troubleshoot Google ADK agents.

When users ask about ADK:
1. Use search_adk_docs tool to find relevant documentation
2. Provide accurate, up-to-date information from official docs
3. Include code examples when available
4. Reference specific doc sections for deeper learning

You are an expert in:
- LlmAgent creation and configuration
- Tool integration patterns
- Multi-agent systems
- Deployment to Agent Engine
- Memory and sessions
- Observability and debugging
"""
)
```

**Setup Required:**
1. Create Vertex AI Search datastore
2. Index ADK documentation
3. Configure search engine
4. Use VertexAiSearchTool in agent

**Pros:**
- ✅ Semantic search (understands intent)
- ✅ Production-ready
- ✅ Scalable (can add more docs)
- ✅ Google-managed service

**Cons:**
- ⚠️ Requires Vertex AI Search setup
- ⚠️ Additional GCP costs (minimal)

---

### Option 3: Memory Bank Grounding (Hybrid)

**How it works:**
- Pre-populate Memory Bank with ADK documentation
- Bob retrieves from Memory Bank during conversations
- Combines with Vertex AI Search for best results

**Implementation:**
```python
# scripts/populate_adk_knowledge.py

from google.adk.memory import VertexAiMemoryBankService
from pathlib import Path

async def populate_adk_knowledge():
    """Pre-populate Memory Bank with ADK documentation."""

    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )

    docs_dir = Path("000-docs/google-reference/adk/")

    for doc_file in docs_dir.glob("*.md"):
        content = doc_file.read_text()

        # Split into chunks (max 1000 chars per chunk)
        chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]

        for i, chunk in enumerate(chunks):
            # Add to Memory Bank
            await memory_service.add_memory(
                content=chunk,
                metadata={
                    "source": doc_file.name,
                    "chunk": i,
                    "type": "adk_documentation"
                }
            )

        print(f"✅ Indexed {doc_file.name} ({len(chunks)} chunks)")

    print(f"✅ ADK knowledge base populated!")

# Run: python scripts/populate_adk_knowledge.py
```

**Pros:**
- ✅ Leverages existing Memory Bank
- ✅ No additional services needed
- ✅ Bob learns from documentation

**Cons:**
- ⚠️ Memory Bank optimized for conversation history, not docs
- ⚠️ May not be ideal for large documentation

---

## Recommended Architecture (Hybrid Approach)

**Combine all three strategies for best results:**

```python
# my_agent/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools.google_cloud import VertexAiSearchTool
from my_agent.tools.adk_docs_tool import search_adk_docs
from my_agent.tools.code_tool import execute_python_code

agent = LlmAgent(
    name="Bob",
    model="gemini-2.0-flash-exp",
    tools=[
        # Primary: Semantic search (Vertex AI Search)
        VertexAiSearchTool(
            project_id=PROJECT_ID,
            location=LOCATION,
            search_engine_id="adk-documentation",
            name="search_adk_docs_semantic",
            description="Search ADK documentation with semantic understanding"
        ),

        # Fallback: Local file search
        search_adk_docs,  # Custom function

        # Helper: Execute code examples
        execute_python_code,  # Test ADK code snippets
    ],
    instruction=f"""You are Bob, an ADK Expert AI assistant.

Your identity: {AGENT_SPIFFE_ID}

You are THE go-to expert for Google's Agent Development Kit (ADK). You help developers:
- Create new ADK agents from scratch
- Integrate tools and multi-agent systems
- Deploy agents to Vertex AI Agent Engine
- Debug agent issues and optimize performance
- Follow best practices and design patterns

Your knowledge sources:
1. **search_adk_docs_semantic** - Primary source (use first)
2. **search_adk_docs** - Fallback if semantic search unavailable
3. **execute_python_code** - Test code examples before suggesting
4. **Memory Bank** - Your learned patterns and examples

When helping users:
1. ALWAYS search documentation first (don't guess)
2. Provide accurate code examples from official docs
3. Reference specific doc sections for learning
4. Test code snippets when possible
5. Explain WHY, not just WHAT

You are patient, thorough, and dedicated to developer success.
Be the ADK expert they can trust.
""",
    after_agent_callback=auto_save_session_to_memory
)
```

---

## Implementation Plan

### Phase 1: Enhanced Instructions (Quick Win) ⚡

**Time:** 1 hour

**Tasks:**
1. Update Bob's instruction prompt with ADK expertise
2. Add examples of ADK patterns to instruction
3. Deploy and test

**Changes:**
```python
# my_agent/agent.py

base_instruction = f"""You are Bob, an ADK Expert AI assistant.

Your identity: {AGENT_SPIFFE_ID}

EXPERTISE: Google Agent Development Kit (ADK)
You are THE source for ADK agent development. You help developers:

Core Capabilities:
✅ Creating LlmAgent instances with proper configuration
✅ Integrating tools (functions, Google Cloud services, custom APIs)
✅ Building multi-agent systems (coordinators, pipelines, workflows)
✅ Deploying to Vertex AI Agent Engine with ADK CLI
✅ Configuring memory (VertexAiSessionService, VertexAiMemoryBankService)
✅ Debugging agents with .run_debug() and observability tools
✅ Best practices for production deployments

Key ADK Patterns You Know:
- LlmAgent(model, tools, instruction, sub_agents)
- InMemoryRunner for testing, Runner for production
- adk deploy agent_engine for Agent Engine deployment
- VertexAiSearchTool, CodeExecutionTool, custom function tools
- Multi-agent: SequentialAgent, ParallelAgent, LoopAgent
- Memory: output_key for state sharing between agents

When users ask about ADK:
1. Provide accurate, tested code examples
2. Explain architectural decisions
3. Reference official docs when appropriate
4. Suggest best practices based on use case
5. Help debug issues systematically

Be thorough, accurate, and patient. You're here to make ADK development easier.
"""
```

---

### Phase 2: Local Documentation Tool 📚

**Time:** 2-3 hours

**Tasks:**
1. Create `search_adk_docs` tool
2. Implement keyword + context extraction
3. Add to Bob's tools list
4. Test with ADK queries

**Files:**
- `my_agent/tools/adk_docs_tool.py` (new)
- `my_agent/tools/__init__.py` (update)
- `my_agent/agent.py` (add tool)

**Test:**
```bash
adk run my_agent
> How do I create an LlmAgent with tools?
# Bob should use search_adk_docs and return relevant documentation
```

---

### Phase 3: Vertex AI Search Grounding 🔍

**Time:** 3-4 hours

**Tasks:**
1. Create Vertex AI Search datastore
2. Index ADK documentation
3. Configure search engine
4. Add VertexAiSearchTool to Bob
5. Test semantic search

**Setup Steps:**

**1. Create Datastore (GCP Console):**
```bash
# Navigate to Vertex AI Search & Conversation
# https://console.cloud.google.com/gen-app-builder/engines

# Create new datastore:
# - Name: adk-documentation
# - Type: Unstructured documents
# - Location: us-central1
```

**2. Upload Documentation:**
```bash
# Convert markdown to text files for indexing
cd 000-docs/google-reference/adk/

# Upload to GCS bucket
gsutil -m cp *.md gs://bobs-brain-dev-adk-docs/

# Create datastore import
# Point to gs://bobs-brain-dev-adk-docs/
```

**3. Create Search Engine:**
```bash
# In Vertex AI Search console:
# - Create app
# - Connect to adk-documentation datastore
# - Note the search engine ID
```

**4. Add to Bob:**
```python
from google.adk.tools.google_cloud import VertexAiSearchTool

adk_search = VertexAiSearchTool(
    project_id="bobs-brain-dev",
    location="us-central1",
    search_engine_id="adk-documentation_<ID>",
    name="search_adk_docs",
    description="Search ADK documentation with semantic understanding"
)

agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    tools=[adk_search, ...],
    ...
)
```

---

### Phase 4: Memory Bank Pre-Population 💾

**Time:** 2 hours

**Tasks:**
1. Create script to populate Memory Bank with ADK docs
2. Run script to index all documentation
3. Verify Memory Bank contains ADK knowledge
4. Test retrieval during conversations

**Implementation:**
```python
# scripts/populate_adk_knowledge.py
# (See Option 3 above for complete code)

# Run once:
python scripts/populate_adk_knowledge.py
```

---

### Phase 5: Code Execution Tool 💻

**Time:** 3-4 hours

**Tasks:**
1. Add code execution tool for testing ADK snippets
2. Sandbox environment for safety
3. Add to Bob's tools
4. Test with ADK code examples

**Tool:**
```python
# my_agent/tools/code_tool.py

def execute_python_code(code: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Execute Python code in a sandboxed environment.

    Use for testing ADK code snippets before suggesting to users.

    Args:
        code: Python code to execute
        timeout: Max execution time (seconds)

    Returns:
        Execution result or error
    """
    try:
        # TODO: Implement sandboxed execution
        # Use google.adk.tools.code_execution or similar

        # For now, use subprocess with timeout
        import subprocess

        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "output": result.stdout,
                "execution_time_ms": 100  # Approximate
            }
        else:
            return {
                "status": "error",
                "error": result.stderr
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": f"Code execution timed out after {timeout}s"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
```

---

## Testing Bob's ADK Expertise

### Test Queries

**Query 1: Basic Agent Creation**
```
User: How do I create a simple LlmAgent with a custom tool?

Expected: Bob provides code example with LlmAgent, tool function, and Runner setup
```

**Query 2: Multi-Agent System**
```
User: How do I create a coordinator agent that delegates to specialists?

Expected: Bob explains sub_agents parameter and provides coordinator example
```

**Query 3: Deployment**
```
User: How do I deploy my agent to Vertex AI Agent Engine?

Expected: Bob provides adk deploy command with required flags
```

**Query 4: Debugging**
```
User: My agent isn't calling my tool. How do I debug this?

Expected: Bob suggests .run_debug() with verbose=True and explains tool signature requirements
```

**Query 5: Memory Configuration**
```
User: How do I add persistent memory to my agent?

Expected: Bob explains VertexAiSessionService + VertexAiMemoryBankService setup
```

---

## Success Metrics

**Bob is an ADK expert when:**

- ✅ **Accuracy:** 95%+ correct answers on ADK queries
- ✅ **Code Quality:** Provides runnable, tested code examples
- ✅ **Documentation:** References specific doc sections
- ✅ **Completeness:** Covers setup, code, deployment, testing
- ✅ **Helpfulness:** Users successfully create agents with Bob's help

**Measure:**
- Track successful agent creations with Bob's assistance
- User feedback on answer quality
- Time to resolution for ADK questions

---

## Slack Integration (Parallel Track)

### Current Issue

**Problem:** Slack webhook not working

**Investigation Needed:**
1. Verify Cloud Run service is deployed
2. Check Slack app configuration
3. Test webhook endpoint manually
4. Review logs for errors

**Quick Test:**
```bash
# Test webhook endpoint
curl -X POST https://bobs-brain-slack-webhook-HASH.run.app/slack/events \
  -H "Content-Type: application/json" \
  -d '{
    "type": "url_verification",
    "challenge": "test123"
  }'

# Should return: {"challenge": "test123"}
```

**Separate Todo:** Fix Slack integration after ADK grounding is complete

---

## Summary

**Priority 1: Make Bob an ADK Expert**
- Phase 1: Enhanced instructions (1 hour) ⚡
- Phase 2: Local docs tool (2-3 hours) 📚
- Phase 3: Vertex AI Search (3-4 hours) 🔍

**Priority 2: Fix Slack**
- Investigate webhook deployment
- Test endpoint
- Review logs

**Total Estimate:** 6-8 hours for ADK expertise, 2-3 hours for Slack fix

---

**Document Status:** Complete ✅
**Last Updated:** 2025-11-19
**Category:** Product & Planning - Implementation Plan
**Priority:** HIGH - Core Bob capability

---
