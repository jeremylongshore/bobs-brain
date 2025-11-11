"""
Bob's Slack Integration via FastAPI + Slack Bolt + ADK Runner

This is the CORRECT architecture for Vertex AI Agent Engine integration.
It follows the reference guide provided by the user.

Key Components:
1. FastAPI - Web server
2. Slack Bolt AsyncRequestHandler - Slack event handling
3. ADK Runner - Agent orchestration
4. VertexAiSessionService - Working memory (session history)
5. VertexAiMemoryBankService - Long-term memory (fact extraction)
"""

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp

from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

from .agent import get_agent

# --- Configuration ---
load_dotenv()

PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["LOCATION"]
AGENT_ENGINE_ID = os.environ["AGENT_ENGINE_ID"]
APP_NAME = os.environ["APP_NAME"]

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Initialize Slack Bolt ---
logger.info("Initializing Slack Bolt application...")
app_handler = AsyncSlackRequestHandler(
    AsyncApp(
        token=SLACK_BOT_TOKEN,
        signing_secret=SLACK_SIGNING_SECRET
    )
)
slack_app = app_handler.app
logger.info("Slack Bolt initialized")

# --- Initialize ADK Services ---
logger.info(f"Initializing ADK Services for {PROJECT_ID}/{LOCATION}...")

# VertexAiSessionService: Manages working memory (session history)
# This connects to Vertex AI Agent Engine Sessions backend
session_service = VertexAiSessionService(
    project=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_ENGINE_ID
)
logger.info("VertexAiSessionService initialized")

# VertexAiMemoryBankService: Manages long-term memory (persistent facts)
# This connects to Vertex AI Memory Bank for fact extraction
memory_service = VertexAiMemoryBankService(
    project=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_ENGINE_ID
)
logger.info("VertexAiMemoryBankService initialized")

# --- Initialize ADK Runner ---
logger.info("Initializing ADK Runner with agent and memory services...")
agent = get_agent()

runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service,  # Working memory
    memory_service=memory_service     # Long-term memory
)
logger.info("ADK Runner initialized successfully")

# --- Initialize FastAPI ---
fastapi_app = FastAPI(
    title="Bob Battalion Commander - Slack Integration",
    description="Vertex AI Agent Engine + ADK + Slack Bolt",
    version="1.0.0"
)

@fastapi_app.post("/slack/events")
async def slack_events_endpoint(req: Request):
    """
    Main webhook endpoint for Slack events.

    Slack sends events here, and Slack Bolt handles:
    - Signature verification
    - Event parsing
    - Routing to handlers
    """
    return await app_handler.handle(req)

@fastapi_app.get("/_health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {
        "status": "healthy",
        "service": "bob-slack-integration",
        "version": "1.0.0",
        "components": {
            "slack_bolt": "initialized",
            "adk_runner": "initialized",
            "session_service": "connected",
            "memory_service": "connected"
        }
    }

# --- Slack Event Handlers ---

@slack_app.event("app_mention")
async def handle_app_mention(event, say, logger_bolt):
    """
    Handles @mention events in Slack.

    This is the main entry point for user interactions.

    Flow:
    1. Extract user_id, text, and session_id (thread_ts)
    2. Call ADK Runner with these parameters
    3. Runner orchestrates:
       - PreloadMemoryTool retrieves long-term memories
       - SessionService retrieves session history
       - Agent generates response
       - after_agent_callback saves to Memory Bank
    4. Send response back to Slack
    """
    try:
        # Extract event data
        user_id = event["user"]
        text = event["text"]

        # Use Slack thread_ts as the persistent session_id
        # This maintains conversation context within a thread
        session_id = event.get("thread_ts", event["ts"])

        logger.info(
            f"[Slack Event] Received mention from {user_id} "
            f"in session {session_id}"
        )
        logger.info(f"[Slack Event] Message: {text}")

        # --- Run ADK Agent ---
        logger.info(f"[ADK] Starting runner for session {session_id}...")

        final_response = ""

        # runner.run_async() is an async generator that yields events
        # We iterate through tool calls, thoughts, etc., but only care
        # about the final agent response
        async for event in runner.run_async(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
            new_message=text
        ):
            # Check if this is the final response event
            if event.is_final_response() and event.content:
                final_response = event.content.parts.text
                logger.info(
                    f"[ADK] Final response received "
                    f"({len(final_response)} chars)"
                )

        # --- Send Response to Slack ---
        if final_response:
            logger.info(f"[Slack] Sending response to thread {session_id}")
            await say(text=final_response, thread_ts=session_id)
            logger.info(f"[Slack] Response sent successfully")
        else:
            logger.warning(
                f"[ADK] No final response generated for session {session_id}"
            )
            await say(
                text="Sorry, I encountered an issue and couldn't generate a response.",
                thread_ts=session_id
            )

        logger.info(f"[Complete] Successfully handled mention in session {session_id}")

    except Exception as e:
        logger.error(f"[Error] Exception in handle_app_mention: {e}", exc_info=True)

        # Send error message to user
        error_session = event.get("thread_ts", event["ts"])
        await say(
            text=f"An error occurred while processing your request: {str(e)}",
            thread_ts=error_session
        )


@slack_app.event("message")
async def handle_direct_message(event, say, logger_bolt):
    """
    Handle direct messages to Bob.

    Similar to app_mention, but for DMs.
    """
    # Only process if it's a DM (no channel, and not from a bot)
    if event.get("channel_type") == "im" and not event.get("bot_id"):
        # Reuse the same logic as app_mention
        await handle_app_mention(event, say, logger_bolt)


# --- Application Entry Point ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
