"""
iam-adk - ADK/Vertex Design & Static Analysis Specialist

This agent specializes in:
- Reviewing ADK agent implementations for pattern compliance
- Analyzing A2A (Agent-to-Agent) communication patterns
- Validating AgentCard schemas and configurations
- Recommending ADK best practices and improvements
- Producing structured AuditReports and IssueSpecs

Enforces:
- R1: Uses google-adk (LlmAgent)
- R2: Designed for Vertex AI Agent Engine runtime
- R5: Dual memory (Session + Memory Bank) with auto-save callback
- R7: SPIFFE ID propagation in logs
"""

from google.adk.agents import LlmAgent
from google.adk import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from .tools.analysis_tools import (
    analyze_agent_code,
    validate_adk_pattern,
    check_a2a_compliance,
)
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Environment variables (R7: SPIFFE ID required)
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")
APP_NAME = os.getenv("APP_NAME", "bobs-brain")
AGENT_SPIFFE_ID = os.getenv(
    "AGENT_SPIFFE_ID",
    "spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.8.0",
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

    This callback is invoked after each agent turn to save the conversation
    session to the Memory Bank for long-term persistence.

    Enforces R5: Dual memory wiring requirement.

    Args:
        ctx: Agent context with invocation_context containing memory_service and session

    Note:
        - Never blocks agent execution (errors are logged but not raised)
        - Includes SPIFFE ID in logs (R7)
    """
    try:
        if hasattr(ctx, "_invocation_context"):
            invocation_ctx = ctx._invocation_context
            memory_svc = invocation_ctx.memory_service
            session = invocation_ctx.session

            if memory_svc and session:
                memory_svc.add_session_to_memory(session)
                logger.info(
                    f"✅ Saved session {session.id} to Memory Bank",
                    extra={"spiffe_id": AGENT_SPIFFE_ID, "session_id": session.id},
                )
            else:
                logger.warning(
                    "Memory service or session not available in context",
                    extra={"spiffe_id": AGENT_SPIFFE_ID},
                )
        else:
            logger.warning(
                "Invocation context not available", extra={"spiffe_id": AGENT_SPIFFE_ID}
            )
    except Exception as e:
        logger.error(
            f"Failed to save session to Memory Bank: {e}",
            extra={"spiffe_id": AGENT_SPIFFE_ID},
            exc_info=True,
        )
        # Never block agent execution


def get_agent() -> LlmAgent:
    """
    Create and configure the iam-adk LlmAgent.

    Enforces:
    - R1: Uses google-adk LlmAgent (no alternative frameworks)
    - R5: Configures after_agent_callback for memory persistence
    - R7: Includes SPIFFE ID in agent description

    Returns:
        LlmAgent: Configured agent instance specialized in ADK pattern analysis

    Note:
        This agent is designed to run in Vertex AI Agent Engine (R2).
        Do NOT instantiate a Runner here - that happens in create_runner().
    """
    logger.info(
        f"Creating iam-adk LlmAgent for {APP_NAME}",
        extra={"spiffe_id": AGENT_SPIFFE_ID},
    )

    # ADK Specialist Instruction
    instruction = f"""You are iam-adk, an expert ADK/Vertex design and static analysis specialist.

**Your Identity:** {AGENT_SPIFFE_ID}

**Your Role:**

You are a specialized agent focused on ensuring ADK pattern compliance and architectural quality. You work as part of the iam-* agent team to:
- Review ADK agent implementations for compliance with Hard Mode rules (R1-R8)
- Analyze Agent-to-Agent (A2A) communication patterns
- Validate AgentCard schemas and configurations
- Identify anti-patterns and suggest improvements
- Produce structured audit reports and issue specifications

**Your Expertise:**

1. **ADK Pattern Analysis:**
   - LlmAgent structure validation (model, name, tools, instruction)
   - Tool implementation patterns (FunctionTool, AgentTool)
   - Memory wiring (VertexAiSessionService + VertexAiMemoryBankService)
   - Agent composition (SequentialAgent, ParallelAgent, LoopAgent)
   - Callback implementations (after_agent_callback, before_agent_callback)

2. **A2A Protocol Compliance:**
   - AgentCard schema validation (name, description, capabilities)
   - Input/output schema definitions
   - Tool-based delegation patterns
   - Sub-agent communication flows
   - SPIFFE ID propagation (R7)

3. **Hard Mode Rules Enforcement:**
   - R1: ADK-only (no LangChain, CrewAI, AutoGen)
   - R2: Vertex AI Agent Engine runtime
   - R3: Gateway separation (no Runner in service/)
   - R4: CI-only deployments
   - R5: Dual memory wiring
   - R6: Single documentation folder (000-docs/)
   - R7: SPIFFE ID propagation
   - R8: Drift detection

4. **Code Quality Assessment:**
   - Import analysis (forbidden frameworks detection)
   - Type hint validation
   - Error handling patterns
   - Logging compliance (SPIFFE ID inclusion)
   - Test coverage adequacy

**Your Outputs:**

You produce structured outputs in these formats:

1. **AuditReport:**
   - compliance_status: COMPLIANT | NON_COMPLIANT | WARNING
   - violations: List of rule violations with severity
   - recommendations: Prioritized improvement suggestions
   - risk_level: LOW | MEDIUM | HIGH | CRITICAL

2. **IssueSpec:**
   - title: Concise issue description
   - severity: LOW | MEDIUM | HIGH | CRITICAL
   - rule_violated: Which Hard Mode rule (if applicable)
   - affected_files: List of files with issues
   - proposed_fix: Concrete code changes or patterns to apply

**Your Communication Style:**

- Be precise and technical - cite specific ADK patterns and rules
- Provide actionable recommendations with code examples
- Reference official ADK documentation and Hard Mode rules
- Use structured output formats (AuditReport, IssueSpec)
- Prioritize issues by impact and effort
- Focus on architectural quality, not nitpicking

**Available Tools:**

You have tools to:
- Analyze agent code structure and imports
- Validate ADK pattern compliance
- Check A2A protocol adherence
- Search ADK documentation for patterns
- Generate structured issue specifications

When analyzing code, be thorough but pragmatic. Focus on violations that impact correctness, security, or maintainability."""

    agent = LlmAgent(
        model="gemini-2.0-flash-exp",  # Fast, cost-effective model
        name="iam_adk",  # Required: Valid Python identifier (no hyphens)
        tools=[
            # ADK Pattern Analysis Tools
            analyze_agent_code,  # Analyze agent.py structure and compliance
            validate_adk_pattern,  # Validate specific ADK patterns
            check_a2a_compliance,  # Check A2A protocol compliance
        ],
        instruction=instruction,
        after_agent_callback=auto_save_session_to_memory,  # R5: Save to Memory Bank
    )

    logger.info(
        "✅ iam-adk LlmAgent created successfully",
        extra={"spiffe_id": AGENT_SPIFFE_ID, "model": "gemini-2.0-flash-exp"},
    )

    return agent


def create_runner() -> Runner:
    """
    Create Runner with dual memory wiring (Session + Memory Bank).

    Enforces:
    - R2: Runner designed for Vertex AI Agent Engine deployment
    - R5: Dual memory wiring (Session + Memory Bank)
    - R7: SPIFFE ID propagation in logs

    Returns:
        Runner: Configured runner with dual memory services

    Note:
        This runner is created in the Agent Engine container.
        Gateway code in service/ MUST NOT import or call this (R3).
    """
    logger.info(
        f"Creating Runner with dual memory for iam-adk",
        extra={
            "spiffe_id": AGENT_SPIFFE_ID,
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "agent_engine_id": AGENT_ENGINE_ID,
        },
    )

    # R5: VertexAiSessionService (short-term conversation cache)
    session_service = VertexAiSessionService(
        project_id=PROJECT_ID, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID
    )
    logger.info("✅ Session service initialized", extra={"spiffe_id": AGENT_SPIFFE_ID})

    # R5: VertexAiMemoryBankService (long-term persistent memory)
    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID
    )
    logger.info(
        "✅ Memory Bank service initialized", extra={"spiffe_id": AGENT_SPIFFE_ID}
    )

    # Get agent with after_agent_callback configured
    agent = get_agent()

    # R5: Wire dual memory to Runner
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    logger.info(
        "✅ Runner created successfully with dual memory",
        extra={
            "spiffe_id": AGENT_SPIFFE_ID,
            "app_name": APP_NAME,
            "has_session_service": True,
            "has_memory_service": True,
        },
    )

    return runner


# Create the root agent for ADK CLI deployment
# ADK CLI expects a variable named 'root_agent' at module level
root_agent = get_agent()

logger.info(
    "✅ root_agent created for ADK deployment (iam-adk)",
    extra={"spiffe_id": AGENT_SPIFFE_ID, "model": "gemini-2.0-flash-exp"},
)


# Entry point for Agent Engine container
if __name__ == "__main__":
    """
    This entry point is used when the container is deployed to
    Vertex AI Agent Engine (R2).

    Do NOT run this locally for production (R4: CI-only deployments).
    Local execution is only for CI smoke tests.
    """
    import sys

    # CI-only guard (R4)
    if os.getenv("GITHUB_ACTIONS") != "true":
        logger.warning(
            "⚠️  Running agent locally. Production deployments must use "
            "Vertex AI Agent Engine via GitHub Actions (R4).",
            extra={"spiffe_id": AGENT_SPIFFE_ID},
        )

    try:
        runner = create_runner()
        logger.info(
            "🚀 Agent Engine runner ready (iam-adk)",
            extra={"spiffe_id": AGENT_SPIFFE_ID},
        )

        # For local testing only - Agent Engine manages this in production
        if os.getenv("GITHUB_ACTIONS") != "true":
            logger.info(
                "Local test mode - Runner created but not started. "
                "In production, Agent Engine manages the runner lifecycle."
            )
    except Exception as e:
        logger.error(
            f"❌ Failed to create runner: {e}",
            extra={"spiffe_id": AGENT_SPIFFE_ID},
            exc_info=True,
        )
        sys.exit(1)
