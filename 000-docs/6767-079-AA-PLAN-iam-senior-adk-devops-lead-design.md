# Design Plan: iam-senior-adk-devops-lead Department Foreman

**Document ID:** 079-AA-PLAN-iam-senior-adk-devops-lead-design
**Phase:** 1
**Status:** In Design
**Created:** 2025-11-19

---

## Executive Briefing

This document defines the design and implementation plan for `iam-senior-adk-devops-lead`, the department foreman agent that orchestrates the iam-* specialist team within the ADK/Agent Engineering Department.

**Role:** Department foreman - receives high-level requests from Bob (orchestrator) and delegates to specialized iam-* worker agents for execution.

**Position in Hierarchy:**
```
Bob (Global Orchestrator)
    ↓
iam-senior-adk-devops-lead (Department Foreman)
    ↓
iam-* specialists (Worker Agents)
```

---

## Context & Scope

### In Scope
- Design of foreman agent using ADK LlmAgent
- Responsibility boundaries between Bob and foreman
- Delegation patterns to iam-* specialists
- Tool requirements for orchestration
- A2A wiring for agent-to-agent communication
- System prompt and instruction design

### Out of Scope
- Implementation of individual iam-* specialist agents (Phase 2)
- Full Terraform/CI integration (Phase 3)
- Production deployment (later phase)

---

## Design & Decisions

### 1. Foreman Responsibilities

The `iam-senior-adk-devops-lead` agent is responsible for:

**Primary Functions:**
1. **Request Analysis** - Understand and decompose high-level requests from Bob
2. **Task Planning** - Create execution plans using appropriate iam-* specialists
3. **Delegation** - Route tasks to correct specialist agents
4. **Coordination** - Orchestrate multi-agent workflows
5. **Quality Control** - Validate outputs from specialists
6. **Reporting** - Aggregate results back to Bob

**Key Boundaries:**
- Bob handles: User interaction, Slack communication, cross-project orchestration
- Foreman handles: ADK department operations, specialist coordination, technical execution
- Specialists handle: Domain-specific implementation (ADK analysis, issue writing, etc.)

### 2. Agent Architecture

**Base Pattern:** ADK LlmAgent with SequentialAgent orchestration capabilities

```python
# Core structure (following Bob's pattern)
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

def get_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash-exp",  # Fast, efficient for orchestration
        name="iam_senior_adk_devops_lead",
        tools=[...],  # Orchestration tools
        instruction=FOREMAN_INSTRUCTION,
        after_agent_callback=auto_save_session_to_memory
    )
```

### 3. Tool Requirements

The foreman needs specific tools for orchestration:

**Core Tools:**
1. **agent_delegation_tool** - Invoke iam-* specialists via A2A
2. **github_tool** - Read issues, PRs, repository state
3. **filesystem_tool** - Navigate and understand codebase
4. **adk_knowledge_tool** - Query ADK documentation and patterns
5. **task_planning_tool** - Create and manage execution plans

**Communication Tools:**
1. **status_reporter** - Report progress back to Bob
2. **result_aggregator** - Combine outputs from multiple specialists

### 4. Delegation Patterns

**Pattern 1: Single Specialist**
```
Bob: "Analyze this code for ADK compliance"
    ↓
Foreman: Routes to iam-adk
    ↓
iam-adk: Performs analysis
    ↓
Foreman: Returns results to Bob
```

**Pattern 2: Sequential Workflow**
```
Bob: "Fix this ADK pattern violation"
    ↓
Foreman: Creates plan
    ↓
    1. iam-adk: Analyze violation
    2. iam-fix-plan: Create fix plan
    3. iam-fix-impl: Implement fix
    4. iam-qa: Test changes
    ↓
Foreman: Aggregates and returns to Bob
```

**Pattern 3: Parallel Execution**
```
Bob: "Audit the entire codebase"
    ↓
Foreman: Splits work
    ↓
    ├── iam-adk: Pattern analysis
    ├── iam-issue: Find existing issues
    └── iam-doc: Check documentation
    ↓
Foreman: Merges results and reports
```

### 5. System Prompt Design

The foreman's instruction will emphasize:

```markdown
You are iam-senior-adk-devops-lead, the department foreman for the ADK/Agent Engineering team.

ROLE:
- Receive high-level requests from Bob (global orchestrator)
- Analyze, plan, and delegate to iam-* specialist agents
- Coordinate multi-agent workflows
- Ensure quality and completeness
- Report aggregated results back to Bob

SPECIALISTS YOU MANAGE:
- iam-adk: ADK/Vertex design and static analysis
- iam-issue: GitHub issue specification and creation
- iam-fix-plan: Fix planning and design
- iam-fix-impl: Implementation and coding
- iam-qa: Testing and CI/CD verification
- iam-doc: Documentation and AAR creation
- iam-cleanup: Repository hygiene
- iam-index: Knowledge management

WORKING PRINCIPLES:
1. Always create a plan before delegation
2. Choose the right specialist(s) for each task
3. Validate outputs meet requirements
4. Maintain clear communication with Bob
5. Document significant work in 000-docs/
```

### 6. Data Contracts

**Input from Bob:**
```json
{
  "request_id": "req_123",
  "type": "audit|fix|implement|document",
  "description": "High-level request description",
  "context": {
    "repository": "bobs-brain",
    "branch": "main",
    "urgency": "normal|high|critical"
  },
  "constraints": ["time_limit", "scope_limit"]
}
```

**Output to Bob:**
```json
{
  "request_id": "req_123",
  "status": "completed|failed|partial",
  "plan": {
    "steps": [...],
    "specialists_used": [...]
  },
  "results": {
    "summary": "...",
    "details": {...},
    "artifacts": [...]
  },
  "follow_up": ["recommended_actions"]
}
```

### 7. A2A Integration

**AgentCard Configuration:**
```python
from a2a.types import AgentCard

def get_agent_card() -> AgentCard:
    return AgentCard(
        name="iam-senior-adk-devops-lead",
        description="ADK Department Foreman - Orchestrates iam-* specialists",
        url=os.getenv("FOREMAN_A2A_URL"),
        version="0.1.0",
        skills=[
            "task_planning",
            "delegation",
            "coordination",
            "quality_control"
        ]
    )
```

---

## Implementation Approach

### Phase 1A: Scaffold Creation

1. **Directory Structure:**
```
agents/iam-senior-adk-devops-lead/
├── __init__.py
├── agent.py              # LlmAgent implementation
├── a2a_card.py           # A2A protocol support
├── system_prompt.md      # Full foreman instruction
├── tools/
│   ├── __init__.py
│   ├── delegation.py     # Agent delegation tool
│   ├── github.py         # GitHub integration
│   ├── filesystem.py     # Code navigation
│   └── planning.py       # Task planning
└── README.md             # Agent documentation
```

2. **Core Agent Implementation:**
- Follow Bob's pattern for LlmAgent setup
- Implement dual memory (Session + Memory Bank)
- Add SPIFFE ID propagation
- Configure for Vertex AI Agent Engine

3. **Tool Implementation:**
- Start with mock delegation tool (actual A2A in Phase 3)
- Reuse Bob's ADK knowledge tools where appropriate
- Implement basic task planning data structures

### Phase 1B: System Prompt Refinement

1. **Detailed Instruction Creation:**
- Expand role definition with specific scenarios
- Document each specialist's capabilities
- Define escalation patterns to Bob
- Include error handling procedures

2. **Delegation Logic:**
- When to use single vs. multiple specialists
- How to validate specialist outputs
- Aggregation patterns for results

### Phase 1C: Testing Scaffold

1. **Unit Tests:**
```
tests/unit/test_iam_senior_adk_devops_lead.py
- test_agent_creation
- test_tool_availability
- test_delegation_logic
- test_result_aggregation
```

2. **Integration Test Stubs:**
```
tests/integration/test_foreman_orchestration.py
- test_bob_to_foreman_communication
- test_foreman_to_specialist_delegation
- test_multi_agent_workflow
```

---

## Testing & Verification

### Smoke Tests
```bash
# Verify agent can be created
python -c "from agents.iam_senior_adk_devops_lead.agent import get_agent; a = get_agent(); print('✅ Foreman agent created')"

# Verify A2A card
python -c "from agents.iam_senior_adk_devops_lead.a2a_card import get_agent_card; c = get_agent_card(); print(f'✅ A2A: {c.name}')"

# Run unit tests
pytest tests/unit/test_iam_senior_adk_devops_lead.py -v
```

### Validation Criteria
- [ ] Agent follows ADK LlmAgent pattern
- [ ] Dual memory wiring implemented
- [ ] Tools properly registered
- [ ] System prompt comprehensive
- [ ] A2A card configured
- [ ] Unit tests pass
- [ ] Documentation complete

---

## Issues, Risks & Follow-ups

### Known Issues
- Actual iam-* specialists don't exist yet (Phase 2 dependency)
- A2A wiring needs Terraform/Cloud Run setup (Phase 3 dependency)

### Risks
- **Risk:** Delegation patterns may need refinement after specialist implementation
- **Mitigation:** Design flexible delegation interface that can evolve

### Follow-ups
1. Phase 2: Implement iam-* specialist agents
2. Phase 3: Complete A2A wiring and infrastructure
3. Phase 4: Production deployment and testing

---

## Metrics & Impact

### Success Metrics
- Foreman agent successfully created and tested
- Clear separation of concerns (Bob vs. foreman vs. specialists)
- Delegation patterns documented and implemented
- Foundation ready for Phase 2 specialists

### Expected Impact
- Establishes department structure for ADK team
- Creates reusable orchestration pattern
- Enables scalable multi-agent workflows
- Sets standard for other departments

---

## File Creation Summary

**Files to Create:**
```
agents/iam-senior-adk-devops-lead/
├── __init__.py               (50 lines)
├── agent.py                  (300 lines)
├── a2a_card.py               (30 lines)
├── system_prompt.md          (200 lines)
├── tools/
│   ├── __init__.py           (20 lines)
│   ├── delegation.py         (150 lines)
│   ├── github.py             (100 lines)
│   ├── filesystem.py         (100 lines)
│   └── planning.py           (200 lines)
└── README.md                 (150 lines)

tests/unit/
└── test_iam_senior_adk_devops_lead.py (200 lines)

000-docs/
├── 6767-079-AA-PLAN-iam-senior-adk-devops-lead-design.md (this document)
└── 6767-080-AA-REPT-iam-senior-adk-devops-lead-scaffold.md (AAR skeleton)
```

**Total New Lines:** ~1,500 lines of code/documentation

---

## Approval Gate

**Status:** ⏳ Awaiting approval to proceed with implementation

**To Approve:** Confirm this design aligns with department vision

**Next Steps:**
1. Create directory structure
2. Implement agent scaffold
3. Add tools and system prompt
4. Write unit tests
5. Document in AAR

---

**Document Status:** Complete - Ready for implementation
**Phase:** 1
**Created:** 2025-11-19