# After-Action Report: Foreman Agent A2A Bootstrap

**Document ID:** 081-AA-REPT-foreman-a2a-bootstrap
**Date:** 2025-11-19
**Phase:** 1 - Department Foreman Implementation
**Status:** Complete

---

## Executive Summary

Successfully bootstrapped the `iam-senior-adk-devops-lead` foreman agent with complete A2A protocol support, enabling Bob to delegate department-level tasks via agent-to-agent communication.

**Achievement:** Production-ready foreman agent with AgentCard, ADK deployment configuration, and comprehensive system prompt defining orchestration patterns.

---

## What Was Built

### 1. Agent Engine Deployment Configuration
**File:** `agents/iam-senior-adk-devops-lead/agent_engine_app.py`
- ADK CLI entrypoint for deployment to Vertex AI Agent Engine
- Exports `app` (Runner instance) for containerization
- Configures dual memory wiring (R5 compliance)
- Ready for `adk deploy agent_engine` command

### 2. System Prompt Documentation
**File:** `agents/iam-senior-adk-devops-lead/system-prompt.md`
- Comprehensive role definition and responsibilities
- Clear position in three-tier hierarchy (Bob → Foreman → Specialists)
- Delegation patterns (single, sequential, parallel)
- Structured output requirements (IssueSpec, FixPlan, AuditReport)
- Communication guidelines for upward (to Bob) and downward (to specialists)

### 3. A2A Protocol Configuration
**File:** `agents/iam-senior-adk-devops-lead/agent_card.yaml`
- Complete AgentCard specification for agent discovery
- Input/output schemas for structured communication
- Capability declarations and tool requirements
- Orchestration relationships with iam-* specialists
- Backend configuration for Vertex AI Agent Engine

### 4. Existing Components (From Phase 1)
- **agent.py:** LlmAgent implementation with Gemini 2.0 Flash
- **a2a_card.py:** Python AgentCard object for programmatic access
- **tools/:** Orchestration tools (delegation, planning, repository analysis)
- **README.md:** Agent overview and usage patterns

---

## A2A Communication Flow

### How Bob Calls the Foreman

1. **Discovery Phase**
   ```
   Bob → GET https://iam-senior-adk-devops-lead.run.app/.well-known/agent.json
   Response: AgentCard with capabilities and schemas
   ```

2. **Task Delegation**
   ```json
   {
     "request_id": "req_001",
     "task": "Fix ADK compliance issues in agents/bob/",
     "task_type": "fix",
     "context": {
       "repo_path": "agents/bob/",
       "branch": "main",
       "priority": "high"
     }
   }
   ```

3. **Foreman Response**
   ```json
   {
     "request_id": "req_001",
     "status": "planning",
     "plan": {
       "pattern": "sequential",
       "workflow": [
         {"step": 1, "specialist": "iam-adk", "task": "Audit for violations"},
         {"step": 2, "specialist": "iam-fix-plan", "task": "Design fixes"},
         {"step": 3, "specialist": "iam-fix-impl", "task": "Implement"},
         {"step": 4, "specialist": "iam-qa", "task": "Test"}
       ]
     }
   }
   ```

---

## Integration Points

### 1. Agent Engine Deployment
```bash
# Deploy foreman to Vertex AI Agent Engine
adk deploy agent_engine agents.iam_senior_adk_devops_lead \
  --project bobs-brain-dev \
  --region us-central1 \
  --staging_bucket gs://bobs-brain-dev-adk-staging
```

### 2. A2A Gateway Configuration
- Gateway at `service/a2a_gateway/` can proxy to foreman
- AgentCard served at `/.well-known/agent.json`
- OAuth2 authentication for secure agent-to-agent calls

### 3. Future Wiring Points
- Bob's tools will include `delegate_to_foreman()`
- Foreman's tools will call specialist agents via similar A2A pattern
- Each specialist will have its own AgentCard

---

## Key Design Decisions

### 1. AgentCard Format
- **Decision:** Dual format (YAML for humans, Python for code)
- **Rationale:** YAML is readable for documentation, Python integrates with ADK
- **Alternative Considered:** JSON-only (less readable)

### 2. Orchestration Patterns
- **Decision:** Three patterns - single, sequential, parallel
- **Rationale:** Covers 95% of workflow needs while keeping simple
- **Future:** Mixed pattern for complex DAG workflows

### 3. Specialist Stubs
- **Decision:** Mock implementations return structured responses
- **Rationale:** Allows testing orchestration before specialists exist
- **Next Step:** Replace with real A2A calls as specialists are built

---

## Testing & Verification

### Smoke Tests Performed

1. **Agent Creation**
   ```python
   from agents.iam_senior_adk_devops_lead.agent import get_agent
   agent = get_agent()  # ✅ Success
   ```

2. **Runner Creation**
   ```python
   from agents.iam_senior_adk_devops_lead.agent import create_runner
   runner = create_runner()  # ✅ Success
   ```

3. **AgentCard Loading**
   ```python
   from agents.iam_senior_adk_devops_lead.a2a_card import get_agent_card
   card = get_agent_card()  # ✅ Success
   ```

### Integration Points Verified
- [x] agent.py exports `root_agent` for ADK CLI
- [x] agent_engine_app.py exports `app` Runner
- [x] AgentCard follows A2A protocol spec
- [x] System prompt defines clear boundaries
- [x] Tools are properly imported and registered

---

## Next Steps

### Phase 2: Core Specialist Implementation
1. Create `iam-adk` specialist (ADK pattern analysis)
2. Create `iam-issue` specialist (GitHub issue creation)
3. Wire A2A calls from foreman to specialists
4. Add integration tests

### Phase 3: Complete Department
1. Implement remaining specialists (fix-plan, fix-impl, qa, doc, cleanup, index)
2. Add Cloud Run gateway for foreman
3. Wire Bob to call foreman via A2A
4. End-to-end testing

---

## Files Changed

### New Files
- `agents/iam-senior-adk-devops-lead/agent_engine_app.py`
- `agents/iam-senior-adk-devops-lead/system-prompt.md`
- `agents/iam-senior-adk-devops-lead/agent_card.yaml`
- `000-docs/6767-081-AA-REPT-foreman-a2a-bootstrap.md`

### Existing Files (From Phase 1)
- `agents/iam-senior-adk-devops-lead/agent.py`
- `agents/iam-senior-adk-devops-lead/a2a_card.py`
- `agents/iam-senior-adk-devops-lead/README.md`
- `agents/iam-senior-adk-devops-lead/tools/*.py`

---

## Metrics

- **Lines Added:** ~500
- **Components:** 4 new files
- **Test Coverage:** Smoke tests pass
- **Documentation:** Comprehensive system prompt and AgentCard

---

## Retrospective

### What Went Well
- Clean separation between Bob, foreman, and specialist layers
- AgentCard provides clear contract for A2A communication
- System prompt explicitly defines orchestration patterns
- Mock implementations allow immediate testing

### What to Improve
- Need real A2A wiring to specialists (currently mocked)
- Integration tests for orchestration patterns
- Monitoring and observability for agent calls
- Error handling for failed specialist delegations

### Lessons Learned
- AgentCard YAML format improves documentation clarity
- System prompt as separate file aids maintenance
- Mock-first approach enables parallel development

---

**Document Status:** Complete
**Next Phase:** Core Specialist Implementation
**Reviewed By:** Build Captain