"""
Bob's Brain - Core Agent Implementation

This module defines the LlmAgent with dual memory wiring:
- VertexAiSessionService (short-term conversation cache)
- VertexAiMemoryBankService (long-term persistent memory)

Enforces:
- R1: Uses google-adk (LlmAgent)
- R2: Designed for Vertex AI Agent Engine runtime
- R5: Dual memory (Session + Memory Bank) with auto-save callback
- R7: SPIFFE ID propagation in logs
"""

from google.adk.agents import LlmAgent
from google.adk.runner import Runner
from google.adk.memory import VertexAiSessionService, VertexAiMemoryBankService
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables (R7: SPIFFE ID required)
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")
APP_NAME = os.getenv("APP_NAME", "bobs-brain")
AGENT_SPIFFE_ID = os.getenv("AGENT_SPIFFE_ID")

# Validate required environment variables
if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable is required")
if not LOCATION:
    raise ValueError("LOCATION environment variable is required")
if not AGENT_ENGINE_ID:
    raise ValueError("AGENT_ENGINE_ID environment variable is required")
if not AGENT_SPIFFE_ID:
    raise ValueError("AGENT_SPIFFE_ID environment variable is required (R7)")


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
        if hasattr(ctx, '_invocation_context'):
            invocation_ctx = ctx._invocation_context
            memory_svc = invocation_ctx.memory_service
            session = invocation_ctx.session

            if memory_svc and session:
                memory_svc.add_session_to_memory(session)
                logger.info(
                    f"✅ Saved session {session.id} to Memory Bank",
                    extra={"spiffe_id": AGENT_SPIFFE_ID, "session_id": session.id}
                )
            else:
                logger.warning(
                    "Memory service or session not available in context",
                    extra={"spiffe_id": AGENT_SPIFFE_ID}
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
            exc_info=True
        )
        # Never block agent execution


def get_agent() -> LlmAgent:
    """
    Create and configure the LlmAgent.

    Enforces:
    - R1: Uses google-adk LlmAgent (no alternative frameworks)
    - R5: Configures after_agent_callback for memory persistence
    - R7: Includes SPIFFE ID in agent description

    Returns:
        LlmAgent: Configured agent instance

    Note:
        This agent is designed to run in Vertex AI Agent Engine (R2).
        Do NOT instantiate a Runner here - that happens in create_runner().
    """
    logger.info(
        f"Creating LlmAgent for {APP_NAME}",
        extra={"spiffe_id": AGENT_SPIFFE_ID}
    )

    # Base instruction with SPIFFE identity
    base_instruction = f"""You are Bob, a helpful AI assistant.

Your identity: {AGENT_SPIFFE_ID}

You help users with:
- Answering questions
- Providing information
- Executing tasks through available tools

Be concise, accurate, and helpful. Use tools when appropriate to provide
accurate information rather than guessing.
"""

    agent = LlmAgent(
        model="gemini-2.0-flash-exp",  # Fast, cost-effective model
        tools=[],  # Add custom tools here (see my_agent/tools/)
        instruction=base_instruction,
        after_agent_callback=auto_save_session_to_memory  # R5: Save to Memory Bank
    )

    logger.info(
        "✅ LlmAgent created successfully",
        extra={"spiffe_id": AGENT_SPIFFE_ID, "model": "gemini-2.0-flash-exp"}
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
        f"Creating Runner with dual memory for {APP_NAME}",
        extra={
            "spiffe_id": AGENT_SPIFFE_ID,
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "agent_engine_id": AGENT_ENGINE_ID
        }
    )

    # R5: VertexAiSessionService (short-term conversation cache)
    session_service = VertexAiSessionService(
        project_id=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )
    logger.info("✅ Session service initialized", extra={"spiffe_id": AGENT_SPIFFE_ID})

    # R5: VertexAiMemoryBankService (long-term persistent memory)
    memory_service = VertexAiMemoryBankService(
        project=PROJECT_ID,
        location=LOCATION,
        agent_engine_id=AGENT_ENGINE_ID
    )
    logger.info("✅ Memory Bank service initialized", extra={"spiffe_id": AGENT_SPIFFE_ID})

    # Get agent with after_agent_callback configured
    agent = get_agent()

    # R5: Wire dual memory to Runner
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )

    logger.info(
        "✅ Runner created successfully with dual memory",
        extra={
            "spiffe_id": AGENT_SPIFFE_ID,
            "app_name": APP_NAME,
            "has_session_service": True,
            "has_memory_service": True
        }
    )

    return runner


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
            extra={"spiffe_id": AGENT_SPIFFE_ID}
        )

    try:
        runner = create_runner()
        logger.info(
            "🚀 Agent Engine runner ready",
            extra={"spiffe_id": AGENT_SPIFFE_ID}
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
            exc_info=True
        )
        sys.exit(1)
