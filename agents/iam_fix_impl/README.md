# iam-fix-impl - Implementation Specialist

## Overview

The **Implementation Specialist** agent (`iam-fix-impl`) is responsible for converting detailed FixPlan specifications into working, tested, production-ready code.

## Role in the Agent Factory

As part of the iam-* agent team, `iam-fix-impl`:

- **Receives**: FixPlan objects from `iam-fix-plan`
- **Produces**: Implementation artifacts (code, tests, evidence) for `iam-qa`
- **Reports to**: `iam-senior-adk-devops-lead` (foreman)

## Capabilities

### 1. Code Implementation
- Converts FixPlan steps into precise code changes
- Follows ADK patterns and Python best practices
- Writes clear, maintainable, well-documented code
- Uses correct imports (e.g., `from google.adk.agents import LlmAgent`)
- Applies proper error handling and logging

### 2. Test Generation
- Creates unit tests for every code change
- Writes clear test cases with descriptive names
- Uses pytest fixtures and assertions
- Tests both happy path and error conditions
- Achieves 85%+ code coverage

### 3. Compliance Enforcement
Ensures all code complies with Hard Mode rules:
- **R1**: Using google-adk LlmAgent (no LangChain, CrewAI, AutoGen)
- **R2**: Designing for Vertex AI Agent Engine runtime
- **R3**: Keeping gateways as REST proxies (no Runner imports in service/)
- **R4**: CI-only deployments (no manual gcloud commands)
- **R5**: Dual memory wiring (Session + Memory Bank with callbacks)
- **R6**: Single documentation folder (000-docs/ with NNN-CC-ABCD naming)
- **R7**: SPIFFE ID propagation in logs and telemetry
- **R8**: Drift detection compatibility

### 4. Documentation
- Clear docstrings for all functions and classes
- Inline comments for complex logic
- Implementation notes explaining key decisions
- Links to relevant ADK documentation

## Tools

### implement_fix_step
Implements a single step from FixPlan with guidance on patterns.

### validate_implementation
Validates implementation against FixPlan requirements.

### generate_unit_tests
Creates pytest-based test templates for implemented code.

### check_compliance
Verifies Hard Mode compliance (R1-R8).

### document_implementation
Documents implementation decisions and changes.

## Configuration

### Model Configuration
- **Model**: gemini-2.0-flash-exp
- **Temperature**: 0.2 (deterministic for code generation)
- **Max Tokens**: 8192
- **Timeout**: 600 seconds

### Memory Configuration
- **Session Service**: VertexAiSessionService (short-term cache)
- **Memory Bank**: VertexAiMemoryBankService (long-term persistence)
- **Auto-save**: Enabled via after_agent_callback

## Integration

### Upstream Agents
- **iam-fix-plan**: Provides FixPlan specifications

### Downstream Agents
- **iam-qa**: Receives implementation and tests for validation
- **iam-senior-adk-devops-lead**: Receives status updates

### Shared Contracts
- `FixPlan` (input)
- `QAVerdict` (via iam-qa)
- `IssueSpec` (reference)

## Deployment

### Target Environment
- **Runtime**: Vertex AI Agent Engine
- **Container**: iam-fix-impl:0.8.0
- **Region**: us-central1
- **Memory**: 4 GB
- **CPU**: 2 cores

### Deployment Method
```bash
# Via ADK CLI (CI/CD only)
adk deploy agent_engine \
  --agent-path agents/iam_fix_impl \
  --project-id ${PROJECT_ID} \
  --location ${LOCATION} \
  --trace_to_cloud
```

## Monitoring

### Metrics
- `implementations_completed_total`
- `implementation_latency_seconds`
- `tests_generated_total`
- `compliance_violations_found`
- `qa_pass_rate`

### Logs
- Implementation status
- Files modified/created
- Compliance check results
- Test generation results

### Alerts
- Implementation latency > 600 seconds (warning)
- Compliance violations found (critical)
- QA pass rate < 90% (warning)

## Quality Standards

### Code Quality
- **Style**: black + flake8
- **Test Coverage**: 85% minimum
- **Compliance**: All Hard Mode rules enforced
- **Documentation**: Required for all code
- **No TODOs**: Working code only

### Success Metrics
- First-time QA pass rate > 90%
- Compliance violations = 0
- Test coverage achieved > 85%
- Implementation time < 600 seconds
- Rework required < 10%

## Implementation Patterns

### Agent Creation
```python
from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

def get_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash-exp",
        name="agent_name",
        tools=[...],
        instruction="...",
        after_agent_callback=auto_save_session_to_memory
    )

def create_runner() -> Runner:
    # Dual memory wiring (R5)
    session_service = VertexAiSessionService(...)
    memory_service = VertexAiMemoryBankService(...)
    return Runner(agent, session_service, memory_service)

root_agent = get_agent()
```

### Tool Creation
```python
def tool_name(param: str) -> str:
    """
    Tool description.

    Args:
        param: Parameter description

    Returns:
        str: JSON string with results
    """
    try:
        # Implementation
        return json.dumps({"status": "success", "data": result})
    except Exception as e:
        logger.error(f"Error: {e}", extra={"spiffe_id": AGENT_SPIFFE_ID})
        return json.dumps({"status": "error", "message": str(e)})
```

### Gateway Pattern (R3)
```python
# service/gateway/main.py
# NO Runner imports!

@app.post("/invoke")
async def invoke_agent(req: InvokeRequest):
    token = get_gcp_token()
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/{AGENT_ENGINE_NAME}:query"
    # ... proxy to Agent Engine
```

## Files

```
agents/iam_fix_impl/
├── agent.py                    # Main agent implementation
├── __init__.py                 # Module exports
├── agent_card.yaml             # A2A protocol card
├── system-prompt.md            # Role definition
├── README.md                   # This file
└── tools/
    ├── __init__.py
    └── implementation_tools.py # Implementation tools
```

## Usage Example

```python
from agents.iam_fix_impl import get_agent, create_runner

# Get agent for ADK CLI deployment
agent = get_agent()

# Create runner with dual memory (R5)
runner = create_runner()

# Agent is deployed to Vertex AI Agent Engine via CI/CD
# Invoked via REST API by other agents
```

## Development

### Local Testing
```bash
# Syntax check
python3 -m py_compile agents/iam_fix_impl/agent.py

# Import check (requires google-adk)
python3 -c "from agents.iam_fix_impl import get_agent; print(get_agent().name)"

# Unit tests
pytest tests/unit/iam_fix_impl_test.py -v
```

### Adding New Tools
1. Add function to `tools/implementation_tools.py`
2. Add to `tools/__init__.py` exports
3. Import in `agent.py`
4. Add to `tools` list in `get_agent()`
5. Update `agent_card.yaml` with tool schema

## Documentation

- **System Prompt**: [system-prompt.md](./system-prompt.md)
- **Agent Card**: [agent_card.yaml](./agent_card.yaml)
- **Patterns**: See 000-docs/ADK-IMPLEMENTATION-PATTERNS.md

## Links

- **GitHub Workflow**: `.github/workflows/deploy-agent-engine.yml`
- **Runbook**: `000-docs/RUN-IMPLEMENTATION.md`
- **Patterns Doc**: `000-docs/ADK-IMPLEMENTATION-PATTERNS.md`

## Version

**Current Version**: 0.8.0 (Agent Factory Structure)

## License

Part of the bobs-brain ADK Agent Department.
