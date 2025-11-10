"""
Bob's ADK Agent Definition

Implements the correct Vertex AI Agent Engine architecture with:
- PreloadMemoryTool for automatic memory retrieval
- after_agent_callback for automatic memory persistence
"""

from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
import logging

logger = logging.getLogger(__name__)


async def auto_save_session_to_memory_callback(callback_context):
    """
    After-agent callback that saves the completed session to Memory Bank.

    This is called automatically by the ADK Runner after the agent's
    final response. The Memory Bank will asynchronously extract facts
    from the conversation.
    """
    try:
        session_id = callback_context._invocation_context.session.id
        logger.info(f"[Callback] Saving session {session_id} to Memory Bank...")

        await callback_context._invocation_context.memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )

        logger.info(f"[Callback] Session {session_id} saved successfully")

    except Exception as e:
        # Log error but don't block user response
        logger.error(f"[Callback] Error saving to Memory Bank: {e}", exc_info=True)


def get_agent():
    """
    Initialize and return Bob's ADK agent with memory capabilities.

    Returns:
        LlmAgent: Configured agent with memory tools and callbacks
    """

    # PreloadMemoryTool automatically retrieves relevant long-term memories
    # at the START of each agent turn
    memory_tool = PreloadMemoryTool()

    return LlmAgent(
        name="battalion-commander-bob",  # Required by ADK 1.18.0+
        model="gemini-2.5-flash",  # Current production model

        instruction="""
        You are Battalion Commander Bob, the Lead Intel Commander.

        You have two types of memory:
        1. **Session History** (Working Memory): The current conversation thread
        2. **Long-Term Memory** (Memory Bank): Facts extracted from past conversations

        When a user asks a question, relevant long-term memories will be
        automatically provided to you via the PreloadMemoryTool.

        Use these memories to:
        - Provide personalized responses
        - Maintain continuity across sessions
        - Reference past conversations naturally

        Communication Guidelines:
        - Use Slack-compatible markdown (*bold*, `code`, etc.)
        - Be concise and actionable
        - Format responses for readability
        - Reference past context when relevant

        Your role is to be helpful, knowledgeable, and maintain context
        across all user interactions.
        """,

        tools=[memory_tool],

        # This callback runs AFTER the agent's response
        # It saves the session to Memory Bank for fact extraction
        after_agent_callback=auto_save_session_to_memory_callback,
    )
