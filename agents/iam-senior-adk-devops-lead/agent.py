"""
iam-senior-adk-devops-lead - Department Foreman Agent Implementation

This module defines the foreman LlmAgent that orchestrates iam-* specialists.
Follows ADK Hard Mode patterns with dual memory and SPIFFE ID propagation.
"""

from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from agents.shared_tools import FOREMAN_TOOLS  # Use shared tools profile
import os
import logging
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")
APP_NAME = os.getenv("APP_NAME", "iam-senior-adk-devops-lead")
AGENT_SPIFFE_ID = os.getenv(
    "AGENT_SPIFFE_ID",
    "spiffe://intent.solutions/agent/iam-senior-adk-devops-lead/dev/us-central1/0.1.0"
)

# AgentCard location (A2A protocol)
AGENTCARD_PATH = os.path.join(
    os.path.dirname(__file__), ".well-known", "agent-card.json"
)

# Validate required environment variables
if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable is required")
if not LOCATION:
    raise ValueError("LOCATION environment variable is required")
if not AGENT_ENGINE_ID:
    raise ValueError("AGENT_ENGINE_ID environment variable is required")


def auto_save_session_to_memory(ctx):
    """
    After-agent callback to persist session to Memory Bank.

    Enforces R5: Dual memory wiring requirement.
    """
    try:
        if hasattr(ctx, "_invocation_context"):
            invocation_ctx = ctx._invocation_context
            memory_svc = invocation_ctx.memory_service
            session = invocation_ctx.session

            if memory_svc and session:
                memory_svc.add_session_to_memory(session)
                logger.info(
                    f"✅ Saved foreman session {session.id} to Memory Bank",
                    extra={"spiffe_id": AGENT_SPIFFE_ID, "session_id": session.id},
                )
            else:
                logger.warning(
                    "Memory service or session not available",
                    extra={"spiffe_id": AGENT_SPIFFE_ID},
                )
        else:
            logger.warning(
                "Invocation context not available",
                extra={"spiffe_id": AGENT_SPIFFE_ID}
            )
    except Exception as e:
        logger.error(
            f"Failed to save session to Memory Bank: {e}",
            extra={"spiffe_id": AGENT_SPIFFE_ID},
            exc_info=True,
        )
        # Never block agent execution


def get_foreman_instruction() -> str:
    """
    Load the comprehensive foreman instruction.

    Returns the system prompt that defines the foreman's role,
    responsibilities, and working principles.
    """
    instruction = """You are iam-senior-adk-devops-lead, the foreman for department adk iam in the bobs-brain repository.

**Your Identity:** {spiffe_id}

## Role and Responsibilities

You manage the department adk iam by:
1. **Request Analysis:** Understand high-level requests from Bob (global orchestrator)
2. **Task Planning:** Break down complex requests into specialist tasks
3. **Specialist Delegation:** Route tasks to appropriate iam-* workers
4. **Workflow Orchestration:** Manage sequential/parallel specialist execution
5. **Result Aggregation:** Synthesize specialist outputs into coherent reports
6. **Quality Control:** Validate specialist outputs before returning to Bob

## Your Specialists

You coordinate these iam-* specialist agents:
- **iam-adk**: ADK/Vertex pattern analysis and compliance checking
- **iam-issue**: GitHub issue specification and creation
- **iam-fix-plan**: Fix planning and design
- **iam-fix-impl**: Implementation and coding
- **iam-qa**: Testing and CI/CD verification
- **iam-doc**: Documentation and AAR creation
- **iam-cleanup**: Repository hygiene and tech debt
- **iam-index**: Knowledge management and indexing

## Delegation Patterns

### Single Specialist Pattern
Use when task clearly belongs to one domain:
1. Analyze request → 2. Delegate to one specialist → 3. Validate → 4. Report

### Sequential Workflow Pattern
Use when tasks have dependencies (output of one feeds another):
1. Plan workflow → 2. Specialist 1 → 3. Specialist 2 → ... → 4. Aggregate → 5. Report

### Parallel Execution Pattern
Use when tasks are independent and can run simultaneously:
1. Plan tasks → 2. [Multiple specialists concurrently] → 3. Aggregate → 4. Report

## Using RAG and Memory Bank

- **Memory Bank queries:** Retrieve long-term decisions, standards (e.g., Hard Mode rules, department conventions)
- **RAG (via <context>):** You receive retrieved docs from Bob; use them to inform delegation
- **Don't duplicate knowledge:** If a specialist needs ADK docs, they can query RAG themselves

## Output Format

Return structured JSON matching your AgentCard output schema:
```json
{
  "request_id": "echo_of_input_request_id",
  "status": "planning|executing|completed|failed|partial",
  "plan": {
    "pattern": "single|sequential|parallel|mixed",
    "workflow": [...]
  },
  "results": {...},
  "recommendations": [...],
  "issues": [...]
}
```

## Error Handling

- Specialist fails → Retry with alternate approach or escalate with context to Bob
- Ambiguous request → Ask Bob for clarification before proceeding
- Missing context → Request additional information from Bob

## Constraints

- **Never execute specialist work yourself** (always delegate)
- Validate all specialist outputs before aggregating
- Maintain correlation IDs for tracing (pipeline_run_id, request_id)
- Follow department standards documented in Memory Bank
- Query Memory Bank for Hard Mode rules (R1-R8) when validating specialist outputs""".format(
        spiffe_id=AGENT_SPIFFE_ID
    )

    return instruction


def get_agent() -> LlmAgent:
    """
    Create and configure the foreman LlmAgent.

    Follows R1-R8 Hard Mode requirements:
    - R1: ADK LlmAgent only
    - R2: Designed for Vertex AI Agent Engine
    - R5: Dual memory with callback
    - R7: SPIFFE ID propagation
    """
    logger.info(
        f"Creating foreman agent {APP_NAME}",
        extra={"spiffe_id": AGENT_SPIFFE_ID}
    )

    agent = LlmAgent(
        model="gemini-2.0-flash-exp",  # Fast and efficient for orchestration
        name="iam_senior_adk_devops_lead",  # Valid Python identifier
        tools=FOREMAN_TOOLS,  # Use shared tools profile
        instruction=get_foreman_instruction(),
        after_agent_callback=auto_save_session_to_memory,  # R5: Memory persistence
    )

    logger.info(
        "✅ Foreman agent created successfully",
        extra={
            "spiffe_id": AGENT_SPIFFE_ID,
            "model": "gemini-2.0-flash-exp",
            "tools_count": 4
        }
    )

    return agent


def create_runner() -> Runner:
    """
    Create Runner with dual memory wiring (Session + Memory Bank).

    Enforces:
    - R2: Runner for Vertex AI Agent Engine
    - R5: Dual memory services
    - R7: SPIFFE ID in logs
    """
    logger.info(
        f"Creating Runner for foreman {APP_NAME}",
        extra={
            "spiffe_id": AGENT_SPIFFE_ID,
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "agent_engine_id": AGENT_ENGINE_ID,
        }
    )

    # R5: Session Service (short-term cache)
    session_service = VertexAiSessionService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )
    logger.info(
        "✅ Session service initialized",
        extra={"spiffe_id": AGENT_SPIFFE_ID}
    )

    # R5: Memory Bank Service (long-term persistence)
    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )
    logger.info(
        "✅ Memory Bank service initialized",
        extra={"spiffe_id": AGENT_SPIFFE_ID}
    )

    # Get configured agent
    agent = get_agent()

    # Create Runner with dual memory
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    logger.info(
        "✅ Foreman Runner created with dual memory",
        extra={
            "spiffe_id": AGENT_SPIFFE_ID,
            "app_name": APP_NAME,
            "has_session_service": True,
            "has_memory_service": True,
        }
    )

    return runner


# Module-level agent for ADK CLI deployment
root_agent = get_agent()

logger.info(
    "✅ root_agent created for ADK deployment",
    extra={
        "spiffe_id": AGENT_SPIFFE_ID,
        "agent_name": "iam_senior_adk_devops_lead"
    }
)


if __name__ == "__main__":
    """
    Entry point for Agent Engine container.
    Only for CI smoke tests, not production execution.
    """
    import sys

    # R4: CI-only guard
    if os.getenv("GITHUB_ACTIONS") != "true":
        logger.warning(
            "⚠️ Running foreman locally. Production must use "
            "Vertex AI Agent Engine via GitHub Actions (R4).",
            extra={"spiffe_id": AGENT_SPIFFE_ID},
        )

    try:
        runner = create_runner()
        logger.info(
            "🚀 Foreman runner ready",
            extra={"spiffe_id": AGENT_SPIFFE_ID}
        )

        # For local testing only
        if os.getenv("GITHUB_ACTIONS") != "true":
            logger.info(
                "Local test mode - Runner created but not started. "
                "In production, Agent Engine manages the runner lifecycle."
            )
    except Exception as e:
        logger.error(
            f"❌ Failed to create foreman runner: {e}",
            extra={"spiffe_id": AGENT_SPIFFE_ID},
            exc_info=True,
        )
        sys.exit(1)