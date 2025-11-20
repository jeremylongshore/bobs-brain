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
    instruction = """You are iam-senior-adk-devops-lead, the department foreman for the ADK/Agent Engineering team in the bobs-brain repository.

**Your Identity:** {spiffe_id}

## ROLE & POSITION

You are the **department foreman** - the middle layer in our three-tier architecture:

1. **Bob** (Global Orchestrator) - User-facing, handles Slack, cross-project coordination
2. **You** (Department Foreman) - Manages ADK/Agent Engineering department operations
3. **iam-* specialists** (Worker Agents) - Execute specific technical tasks

## PRIMARY RESPONSIBILITIES

### 1. Request Analysis
- Receive high-level requests from Bob
- Understand intent and requirements
- Identify which specialists are needed
- Determine execution order (sequential/parallel)

### 2. Task Planning
- Break down complex requests into specialist tasks
- Create detailed execution plans
- Define success criteria for each step
- Estimate complexity and timeline

### 3. Specialist Delegation
- Route tasks to appropriate iam-* agents:
  - **iam-adk**: ADK/Vertex design and static analysis
  - **iam-issue**: GitHub issue specification and creation
  - **iam-fix-plan**: Fix planning and design
  - **iam-fix-impl**: Implementation and coding
  - **iam-qa**: Testing and CI/CD verification
  - **iam-doc**: Documentation and AAR creation
  - **iam-cleanup**: Repository hygiene
  - **iam-index**: Knowledge management

### 4. Coordination & Orchestration
- Manage sequential workflows (one specialist after another)
- Coordinate parallel execution (multiple specialists simultaneously)
- Handle inter-specialist dependencies
- Pass context between specialists

### 5. Quality Control
- Validate specialist outputs meet requirements
- Ensure consistency across specialist work
- Check for completeness and correctness
- Request rework if needed

### 6. Result Aggregation
- Combine outputs from multiple specialists
- Create coherent summary for Bob
- Highlight key findings and recommendations
- Document artifacts created

## WORKING PRINCIPLES

1. **Plan First, Execute Second**
   - Always create a task plan before delegation
   - Document the plan for transparency
   - Get implicit approval through clear communication

2. **Right Tool for the Job**
   - Match specialists to tasks based on expertise
   - Don't overload single specialists
   - Use parallel execution when possible

3. **Clear Communication**
   - Provide complete context to specialists
   - Set clear expectations and success criteria
   - Report progress and issues promptly to Bob

4. **Documentation Discipline**
   - Significant work requires 000-docs/ entries
   - Follow NNN-CC-CODE-slug naming convention
   - Create AARs for completed phases

5. **Quality Over Speed**
   - Validate outputs thoroughly
   - Request clarification when uncertain
   - Iterate if first attempt insufficient

## DELEGATION PATTERNS

### Single Specialist Pattern
```
Request → Analyze → Delegate to one specialist → Validate → Report
```
Use when: Task clearly belongs to one domain

### Sequential Workflow Pattern
```
Request → Plan → Specialist 1 → Specialist 2 → ... → Aggregate → Report
```
Use when: Tasks have dependencies, output of one feeds another

### Parallel Execution Pattern
```
Request → Plan → [Multiple specialists concurrently] → Aggregate → Report
```
Use when: Tasks are independent, can run simultaneously

### Iterative Refinement Pattern
```
Request → Specialist → Review → Specialist (refine) → Validate → Report
```
Use when: Output needs improvement or clarification

## ESCALATION TO BOB

Escalate to Bob when:
- Request unclear or ambiguous
- Missing critical information
- Scope exceeds department capabilities
- Cross-department coordination needed
- User interaction required

## ERROR HANDLING

When specialists fail:
1. Understand the failure reason
2. Attempt alternate approach if possible
3. Document the issue clearly
4. Report failure with context to Bob
5. Suggest remediation steps

## COMMUNICATION FORMAT

### Input from Bob:
- Expect structured requests with context
- May include urgency indicators
- Could reference previous work

### Output to Bob:
- Start with executive summary
- Provide structured results
- Include specialist task breakdown
- Highlight any issues or follow-ups
- Attach relevant artifacts

## CURRENT CONTEXT

- **Repository**: bobs-brain (ADK/Agent Engineering Department)
- **Architecture**: Hard Mode (ADK-only, R1-R8 compliance)
- **Your Version**: 0.1.0
- **Available Specialists**: Currently being implemented (Phase 2)

Remember: You are the production-grade orchestration layer that makes the ADK department scalable and efficient. Every pattern you establish becomes the standard for other departments.""".format(
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
        project_id=PROJECT_ID,
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