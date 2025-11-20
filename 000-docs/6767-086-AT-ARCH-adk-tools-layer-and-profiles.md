# ADK Shared Tools Layer Architecture

**Document ID:** 6767-086-AT-ARCH-adk-tools-layer-and-profiles
**Date:** 2025-11-19
**Author:** claude.buildcaptain@intentsolutions.io
**Category:** Architecture & Technical
**Status:** Implementation Ready

## Overview

This document defines the shared tools layer architecture for the Bob's Brain ADK department. It establishes centralized tool profiles for all agents, ensuring consistent access control and enabling future infrastructure integrations.

## Architecture

### Module Structure

```
agents/shared_tools/
├── __init__.py         # Tool profiles and exports
├── adk_builtin.py      # ADK built-in tools and stubs
└── custom_tools.py     # Custom tool aggregation
```

### Design Principles

1. **Principle of Least Privilege**
   - Each agent gets only the tools it needs
   - No universal access to all tools

2. **ADK-First**
   - Prefer ADK built-in tools when available
   - Follow ADK patterns for custom tools

3. **Future-Ready**
   - Stubs for upcoming infrastructure (Vertex Search, GCS, BigQuery)
   - Clear TODO markers for future wiring

4. **No Secrets**
   - No credentials or API keys in tool definitions
   - All auth handled at runtime via environment

## Tool Profiles

### Bob - Global Orchestrator
**Profile:** `BOB_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_bob_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Google Search | ADK built-in | Web search capability | Active |
| ADK Docs Search | Custom | Search ADK documentation | Active |
| ADK API Reference | Custom | Get detailed API docs | Active |
| List ADK Docs | Custom | Browse documentation | Active |
| Vertex AI Search | Custom | Semantic search | Active |
| Vertex Search Status | Custom | Check datastore status | Active |
| Repository Search | Stub | Search codebase | TODO |

### iam-senior-adk-devops-lead - Foreman
**Profile:** `FOREMAN_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_foreman_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Delegate to Specialist | Custom | Task delegation | Active |
| Aggregate Results | Custom | Collect specialist outputs | Active |
| Verify ADK Compliance | Custom | Check patterns | Active |
| Manage Department | Custom | Orchestration | Active |
| Google Search | ADK built-in | Research | Active |
| Repository Search | Stub | Code analysis | TODO |

### iam-adk - ADK Pattern Specialist
**Profile:** `IAM_ADK_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_adk_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Analyze Agent Code | Custom | Code review | Active |
| Validate ADK Pattern | Custom | Pattern checking | Active |
| Check A2A Compliance | Custom | Protocol validation | Active |
| ADK Docs Tools | Custom | Documentation access | Active |
| Google Search | ADK built-in | Research | Active |

### iam-issue - Issue Management
**Profile:** `IAM_ISSUE_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_issue_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Create Issue Spec | Custom | Issue creation | Active |
| Analyze Problem | Custom | Problem analysis | Active |
| Categorize Issue | Custom | Classification | Active |
| Estimate Severity | Custom | Priority assessment | Active |
| Suggest Labels | Custom | GitHub labels | Active |
| Format GitHub Issue | Custom | Markdown formatting | Active |
| Google Search | ADK built-in | Research | Active |

### iam-fix-plan - Solution Planning
**Profile:** `IAM_FIX_PLAN_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_fix_plan_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Create Fix Plan | Custom | Solution design | Active |
| Analyze Dependencies | Custom | Impact analysis | Active |
| Estimate Effort | Custom | Time estimation | Active |
| Identify Risks | Custom | Risk assessment | Active |
| Suggest Alternatives | Custom | Option analysis | Active |
| Validate Approach | Custom | Feasibility check | Active |
| Google Search | ADK built-in | Research | Active |
| ADK Docs Tools | Custom | Reference | Active |

### iam-fix-impl - Implementation
**Profile:** `IAM_FIX_IMPL_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_fix_impl_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Implement Fix | Custom | Code changes | Active |
| Generate Code | Custom | Code creation | Active |
| Apply Patch | Custom | Patch application | Active |
| Refactor Code | Custom | Code improvement | Active |
| Add Tests | Custom | Test generation | Active |
| Update Documentation | Custom | Doc updates | Active |
| ADK Docs Tools | Custom | Reference | Active |
| Code Execution | Stub | Sandboxed execution | TODO |

### iam-qa - Quality Assurance
**Profile:** `IAM_QA_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_qa_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Run Tests | Custom | Test execution | Active |
| Validate Fix | Custom | Fix verification | Active |
| Check Regression | Custom | Regression testing | Active |
| Verify Requirements | Custom | Requirement check | Active |
| Generate Test Report | Custom | Reporting | Active |
| Suggest Test Cases | Custom | Test design | Active |
| ADK Docs Tools | Custom | Validation reference | Active |

### iam-doc - Documentation
**Profile:** `IAM_DOC_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_doc_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Create Documentation | Custom | Doc generation | Active |
| Update README | Custom | README updates | Active |
| Generate API Docs | Custom | API documentation | Active |
| Create Runbook | Custom | Operational docs | Active |
| Update Changelog | Custom | Change tracking | Active |
| Format Markdown | Custom | Formatting | Active |
| Google Search | ADK built-in | Research | Active |
| ADK Docs Tools | Custom | Reference | Active |

### iam-cleanup - Technical Debt
**Profile:** `IAM_CLEANUP_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_cleanup_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Identify Tech Debt | Custom | Debt detection | Active |
| Remove Dead Code | Custom | Code cleanup | Active |
| Optimize Imports | Custom | Import cleanup | Active |
| Standardize Formatting | Custom | Code formatting | Active |
| Update Dependencies | Custom | Dependency management | Active |
| Archive Old Files | Custom | File archival | Active |
| Google Search | ADK built-in | Research | Active |

### iam-index - Knowledge Management
**Profile:** `IAM_INDEX_TOOLS`
**Location:** `agents/shared_tools/__init__.py::get_iam_index_tools()`

| Tool | Source | Purpose | Status |
|------|--------|---------|--------|
| Index ADK Docs | Custom | Doc indexing | Active |
| Index Project Docs | Custom | Project indexing | Active |
| Query Knowledge Base | Custom | KB search | Active |
| Sync Vertex Search | Custom | Search sync | Active |
| Generate Index Entry | Custom | Entry creation | Active |
| Analyze Knowledge Gaps | Custom | Gap analysis | Active |
| Google Search | ADK built-in | Research | Active |
| Vertex Search Tools | Custom | Semantic search | Active |

## Future Infrastructure Integrations

### Planned Tool Additions

| Tool | Target Agents | Requirements | Priority |
|------|--------------|--------------|----------|
| Repository Search | Bob, Foreman, iam-adk | Code indexing | High |
| Code Execution Sandbox | iam-fix-impl, iam-qa | Agent Engine config | Medium |
| BigQuery Toolset | iam-index | GCP credentials | Low |
| GCS Toolset | iam-doc, iam-index | Bucket permissions | Low |
| MCP Toolset | All agents | MCP server config | Future |

### Wiring Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 3 | ✅ Complete | Shared tools layer created |
| Phase 4 | ✅ Complete | All agents wired to profiles |
| Phase 5 | 📅 Planned | Vertex Search integration |
| Phase 6 | 📅 Planned | Repository indexing |

## Security Considerations

### Access Control
- Tool profiles enforce least privilege access
- No agent has universal tool access
- Delegation tools restricted to foreman only

### Credential Management
- No credentials stored in tool definitions
- All auth via environment variables
- Service accounts managed at runtime

### Audit Trail
- All tool calls logged with agent SPIFFE ID
- Tool profile loading logged at startup
- Stub tool calls tracked for future wiring

## Implementation Guide

### Using Tool Profiles in Agents

```python
# In agent.py
from agents.shared_tools import BOB_TOOLS

agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="bobs_brain",
    tools=BOB_TOOLS,  # Use shared profile
    instruction=instruction,
    after_agent_callback=auto_save_session_to_memory,
)
```

### Adding New Tools

1. **For ADK built-ins:** Add to `adk_builtin.py`
2. **For custom tools:** Add to `custom_tools.py`
3. **Update profiles** in `__init__.py`
4. **Document** in this file

### Stubbing Future Tools

```python
def get_new_tool_stub() -> Any:
    """Get the New Tool (currently stubbed)."""
    return create_tool_stub(
        "new_tool",
        "Description of what it will do",
        "Requirements for activation"
    )
```

## Migration Status

| Agent | Old Tool Wiring | New Profile | Status |
|-------|-----------------|-------------|--------|
| Bob | Local imports | BOB_TOOLS | ✅ Wired |
| Foreman | Local imports | FOREMAN_TOOLS | ✅ Wired |
| iam-adk | Local imports | IAM_ADK_TOOLS | ✅ Wired |
| iam-issue | Local imports | IAM_ISSUE_TOOLS | ✅ Wired |
| iam-fix-plan | Local imports | IAM_FIX_PLAN_TOOLS | ✅ Wired |
| iam-fix-impl | Local imports | IAM_FIX_IMPL_TOOLS | ✅ Wired |
| iam-qa | Local imports | IAM_QA_TOOLS | ✅ Wired |
| iam-doc | Local imports | IAM_DOC_TOOLS | ✅ Wired |
| iam-cleanup | Local imports | IAM_CLEANUP_TOOLS | ✅ Wired |
| iam-index | Local imports | IAM_INDEX_TOOLS | ✅ Wired |

## Maintenance

### Quarterly Review
- [ ] Audit tool usage per agent
- [ ] Review stub tools for activation
- [ ] Update profiles based on usage patterns
- [ ] Remove deprecated tools

### Tool Lifecycle
1. **Stub Phase:** Placeholder with TODO
2. **Implementation:** Wire to actual service
3. **Active:** In production use
4. **Deprecated:** Marked for removal
5. **Removed:** Deleted from profiles

## References

- **ADK Documentation:** `agents/bob/tools/adk_tools.py`
- **Vertex Search:** `agents/bob/tools/vertex_search_tool.py`
- **Hard Mode Rules:** `000-docs/6767-053-AA-REPT-hardmode-baseline.md`
- **Department Structure:** `000-docs/6767-082-AT-ARCH-department-complete-structure.md`

---

**Next Steps:**
1. ✅ ~~Wire all agents to use shared profiles (Phase 4)~~ **COMPLETE**
2. Activate repository search when indexed
3. Configure code execution sandbox
4. Enable BigQuery/GCS toolsets with credentials
5. Add ADK documentation to storage bucket for grounding