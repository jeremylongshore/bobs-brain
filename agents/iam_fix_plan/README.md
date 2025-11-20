# iam-fix-plan Agent

**Fix Planning & Implementation Strategy Specialist**

Part of the **iam-*** agent team in the bobs-brain ADK Engineering Department.

## Overview

iam-fix-plan is a specialized ADK agent that converts issue specifications (IssueSpec) into detailed, actionable fix plans (FixPlan).

**Role in the workflow:**
```
iam-adk (Auditor)
    ↓ produces IssueSpec
iam-issue (Author)
    ↓ formats for GitHub
iam-fix-plan (Planner) ← YOU ARE HERE
    ↓ produces FixPlan
iam-fix-impl (Implementer)
    ↓ executes the plan
iam-qa (Validator)
    ↓ tests the implementation
iam-doc (Documenter)
    ↓ writes AAR
```

## What iam-fix-plan Does

### Input: IssueSpec
Receives issue specifications from iam-adk/iam-issue:
- Title, description, component, severity, type
- Reproduction steps and acceptance criteria
- Related links and labels

### Output: FixPlan
Produces detailed implementation plans:
- Clear, step-by-step implementation guidance
- Risk assessment and mitigation strategies
- Comprehensive testing strategy
- Effort estimation and timeline
- Rollout and rollback procedures
- Success metrics and validation criteria

### Key Capabilities

1. **Fix Plan Design**
   - Convert issue specifications to implementation plans
   - Break down complex fixes into manageable steps
   - Identify impacted areas and dependencies
   - Define success criteria

2. **Risk Assessment**
   - Evaluate implementation risks (low/medium/high)
   - Identify potential breaking changes
   - Plan mitigation strategies
   - Determine rollout approach

3. **Testing Strategy**
   - Design unit, integration, and E2E tests
   - Set coverage requirements
   - Plan for edge cases
   - Define test success criteria

4. **Effort Estimation**
   - Estimate implementation hours
   - Account for testing overhead
   - Factor in review and deployment time
   - Provide confidence levels

5. **Rollout Planning**
   - Design safe deployment strategies
   - Plan rollback procedures
   - Define success metrics for deployment
   - Create monitoring requirements

## Directory Structure

```
iam_fix_plan/
├── __init__.py              # Package exports
├── agent.py                 # Main LlmAgent implementation
├── system-prompt.md         # System prompt and instructions
├── agent_card.yaml          # A2A protocol definition
├── README.md                # This file
└── tools/
    ├── __init__.py          # Tool exports
    └── planning_tools.py    # Planning tool implementations
```

## Files

### `agent.py` - Main Agent Implementation
- `get_agent()` - Create LlmAgent instance
- `create_runner()` - Create Runner with dual memory
- `auto_save_session_to_memory()` - Session persistence callback
- `root_agent` - Module-level agent for ADK CLI

**Enforces Hard Mode Rules:**
- R1: ADK-only (no alternative frameworks)
- R2: Vertex AI Agent Engine runtime
- R5: Dual memory (Session + Memory Bank)
- R7: SPIFFE ID propagation in logs

### `system-prompt.md` - Agent Instructions
Comprehensive system prompt defining:
- Agent role and responsibilities
- Input/output specifications
- Planning framework and methodologies
- Risk assessment guidelines
- Testing strategy patterns
- Communication style
- Tool functions and usage

### `agent_card.yaml` - A2A Protocol Card
Agent-to-Agent protocol definition including:
- Input/output schemas
- Capabilities and tools
- Communication patterns
- Hard Mode rule compliance
- Team member relationships
- Metadata

### `tools/planning_tools.py` - Planning Functions

Key functions:

#### `create_fix_plan(issue_data: str) -> str`
Convert IssueSpec to FixPlan
- Analyzes issue characteristics
- Generates implementation steps
- Assesses risk level
- Defines testing strategy
- Estimates effort

#### `validate_fix_plan(plan_data: str) -> str`
Validate FixPlan completeness
- Checks required fields
- Assesses quality
- Identifies gaps
- Provides recommendations

#### `assess_risk_level(issue_data: str, plan_data: str) -> str`
Evaluate risk and justify assessment
- Analyzes scope and complexity
- Identifies risk factors
- Recommends mitigations
- Determines rollout strategy

#### `define_testing_strategy(component: str, issue_type: str, impacted_areas: str) -> str`
Design comprehensive test plan
- Unit test targets
- Integration test scenarios
- E2E test cases
- Regression requirements

#### `estimate_effort(plan_data: str, team_expertise: str = "medium") -> str`
Realistic effort estimation
- Implementation hours
- Testing hours
- Review hours
- Deployment hours
- Total duration and confidence

## Usage

### Creating a Fix Plan

```python
from agents.iam_fix_plan import get_agent
from agents.iam_contracts import IssueSpec

# Create the agent
agent = get_agent()

# Create an IssueSpec
issue = IssueSpec(
    title="Fix agent memory persistence failure",
    description="Memory Bank integration failing in iam-issue agent",
    component="agents",
    severity="high",
    type="bug",
    acceptance_criteria=[
        "Sessions persist to Memory Bank",
        "Sessions retrievable after restart"
    ]
)

# The agent uses its tools to plan the fix:
# agent.create_fix_plan(issue.to_dict())
# agent.assess_risk_level(issue.to_dict(), fix_plan)
# agent.define_testing_strategy(issue.component, issue.type, impacted_areas)
# agent.estimate_effort(fix_plan)
```

### Deployment

```bash
# Deploy to Vertex AI Agent Engine
adk deploy agent_engine agents/iam_fix_plan/agent.py

# Local smoke test (CI-only, not for production)
python3 agents/iam_fix_plan/agent.py
```

## Hard Mode Rules

iam-fix-plan enforces all Hard Mode rules (R1-R8):

| Rule | Status | Notes |
|------|--------|-------|
| R1: ADK-only | ✅ | Uses google-adk LlmAgent exclusively |
| R2: Vertex AI Agent Engine | ✅ | Designed for Agent Engine deployment |
| R3: Gateway separation | ✅ | No Runner in tools; pure planning logic |
| R4: CI-only deployments | ✅ | Via GitHub Actions with WIF |
| R5: Dual memory | ✅ | Session + Memory Bank services |
| R6: Single docs folder | ✅ | All docs in 000-docs/ with NNN-CC-ABCD naming |
| R7: SPIFFE ID | ✅ | Propagated in logs and context |
| R8: Drift detection | ✅ | Subject to R1-R8 enforcement in CI |

## Testing

### Unit Tests
Tests for planning tools in `tests/unit/agents/iam_fix_plan/`:
- Tool function behavior
- JSON schema validation
- Error handling
- Edge cases

### Integration Tests
Tests in `tests/integration/agents/`:
- A2A communication with other agents
- Input/output contract compliance
- Memory persistence

### Example Test
```python
from agents.iam_fix_plan.tools import create_fix_plan
from agents.iam_contracts import IssueSpec

def test_create_fix_plan():
    issue = IssueSpec(
        title="Fix memory persistence",
        description="Sessions not persisting to Memory Bank",
        component="agents",
        severity="high",
        type="bug"
    )

    plan_json = create_fix_plan(json.dumps(issue.to_dict()))
    plan = json.loads(plan_json)

    assert plan["risk_level"] in ["low", "medium", "high"]
    assert len(plan["steps"]) > 0
    assert "testing_strategy" in plan
```

## Team Communication

### Receives from:
- **iam-adk** - IssueSpec (findings from audits)
- **iam-issue** - IssueSpec (for planning before GitHub)
- **iam-senior-adk-devops-lead** - Planning requests

### Sends to:
- **iam-fix-impl** - FixPlan (detailed implementation plan)
- **iam-qa** - FixPlan (testing requirements)
- **iam-doc** - FixPlan (for documentation)
- **iam-senior-adk-devops-lead** - Status and updates

## Development

### Running Locally

```bash
# Set environment variables
export PROJECT_ID="your-project"
export LOCATION="us-central1"
export AGENT_ENGINE_ID="your-engine-id"

# Test imports
python3 -c "from agents.iam_fix_plan import get_agent; print('✅ Imports work')"

# Run smoke test (CI-only)
python3 agents/iam_fix_plan/agent.py
```

### Adding New Tools

1. Add function to `tools/planning_tools.py`
2. Export in `tools/__init__.py`
3. Add to agent.py's `LlmAgent(tools=[...])`
4. Update system-prompt.md with tool description
5. Add tests in `tests/unit/agents/iam_fix_plan/`

## Related Documentation

- **System Prompt**: `system-prompt.md` - Detailed agent instructions
- **Agent Card**: `agent_card.yaml` - A2A protocol definition
- **Contract Specs**: `agents/iam_contracts.py` - FixPlan data structure
- **Planning Tools**: `tools/planning_tools.py` - Tool implementations
- **Hard Mode Rules**: See `CLAUDE.md` in root directory

## Version History

- **0.8.0** (2025-11-19) - Initial iam-fix-plan agent created
  - Fix plan creation from IssueSpec
  - Risk assessment and testing strategy
  - Effort estimation
  - Rollout planning tools

## Support

For issues or questions:
1. Check system-prompt.md for guidance
2. Review agent_card.yaml for protocol details
3. Check agents/iam_contracts.py for data structures
4. Open issue in bobs-brain GitHub repository

---

**Last Updated:** 2025-11-19
**Version:** 0.8.0
**Status:** Active
**Team:** iam-agents (ADK Engineering Department)
