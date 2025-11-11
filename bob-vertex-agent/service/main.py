"""
FastAPI production service for Bob's Brain A2A Agent

This service provides:
- Health checks with distributed tracing
- AgentCard exposure via GET /card
- Agent invocation via POST /invoke
- Optional Slack Bolt integration via POST /slack/events

Environment variables:
- PROJECT_ID: GCP project ID
- LOCATION: GCP region (default: us-central1)
- AGENT_ENGINE_ID: Optional deployed Agent Engine ID
- SLACK_ENABLED: Enable Slack integration (default: false)
- SLACK_BOT_TOKEN: Slack bot token (required if SLACK_ENABLED=true)
- SLACK_SIGNING_SECRET: Slack signing secret (required if SLACK_ENABLED=true)
- PORT: Service port (default: 8080)
"""

import json
import logging
import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from opentelemetry import trace

# Import agent components
from app.agent import app as adk_app
from app.agent_card import get_agent_card

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
PROJECT_ID = os.getenv("PROJECT_ID", "bobs-brain")
LOCATION = os.getenv("LOCATION", "us-central1")
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID", "")
SLACK_ENABLED = os.getenv("SLACK_ENABLED", "false").lower() == "true"

# Initialize FastAPI app
app = FastAPI(
    title="Bob's Brain Service",
    description="Production A2A Agent Service",
    version="2.0.0"
)

# Initialize ADK Runner
logger.info("Initializing ADK Runner...")
runner = adk_app.create_runner()
logger.info("ADK Runner initialized successfully")

# Slack Bolt integration (optional)
_bolt_app = None
_slack_handler = None

if SLACK_ENABLED:
    logger.info("Slack integration enabled, initializing Slack Bolt...")
    try:
        from slack_bolt.async_app import AsyncApp
        from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

        SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
        SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

        if not SLACK_BOT_TOKEN or not SLACK_SIGNING_SECRET:
            logger.warning("SLACK_ENABLED=true but missing SLACK_BOT_TOKEN or SLACK_SIGNING_SECRET")
            SLACK_ENABLED = False
        else:
            _bolt_app = AsyncApp(
                token=SLACK_BOT_TOKEN,
                signing_secret=SLACK_SIGNING_SECRET
            )
            _slack_handler = AsyncSlackRequestHandler(_bolt_app)
            logger.info("Slack Bolt initialized successfully")
    except ImportError:
        logger.warning("slack-bolt not installed, disabling Slack integration")
        SLACK_ENABLED = False
    except Exception as e:
        logger.error(f"Failed to initialize Slack Bolt: {e}")
        SLACK_ENABLED = False


@app.get("/_health")
async def health() -> JSONResponse:
    """
    Health check endpoint with distributed tracing support.

    Returns:
        JSON response with status and X-Trace-Id header
    """
    # Get current trace context
    span = trace.get_current_span()
    ctx = span.get_span_context() if span else None
    trace_id = f"{ctx.trace_id:032x}" if ctx and ctx.is_valid else None

    # Build response headers
    headers = {}
    if trace_id:
        headers["X-Trace-Id"] = trace_id

    return JSONResponse(
        content={"status": "ok"},
        headers=headers
    )


@app.get("/card")
async def card() -> Dict[str, Any]:
    """
    Return AgentCard JSON for A2A protocol discovery.

    Returns:
        AgentCard dictionary with agent metadata and capabilities
    """
    try:
        agent_card = get_agent_card()
        logger.info(f"AgentCard served: {agent_card.get('product_name', 'unknown')}")
        return agent_card
    except Exception as e:
        logger.error(f"Error retrieving AgentCard: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve AgentCard: {str(e)}"
        )


@app.post("/invoke")
async def invoke(request: Request) -> Dict[str, str]:
    """
    Invoke the agent with a query and return the final response.

    Request body:
        {
            "input": "user query",      # Primary input field (required)
            "text": "user query",       # Alternative input field
            "user_id": "user123",       # Optional user identifier
            "session_id": "sess456"     # Optional session identifier
        }

    Returns:
        {
            "output": "agent response text"
        }
    """
    try:
        body = await request.json()

        # Extract parameters with fallbacks
        user_id = body.get("user_id", "web")
        session_id = body.get("session_id", "web")
        prompt = body.get("input") or body.get("text") or ""

        if not prompt:
            raise HTTPException(
                status_code=400,
                detail="Missing required field 'input' or 'text'"
            )

        logger.info(f"Invoke request: user_id={user_id}, session_id={session_id}, prompt={prompt[:100]}...")

        # Run agent and collect final response
        final_response = ""
        async for event in runner.run_async(
            app_name="bobs-brain",
            user_id=user_id,
            session_id=session_id,
            new_message=prompt
        ):
            # Check if this is a final response event
            if hasattr(event, "is_final_response") and callable(event.is_final_response):
                if event.is_final_response():
                    # Extract response content
                    if hasattr(event, "content") and event.content:
                        content = event.content
                        # Handle different content structures
                        if hasattr(content, "parts"):
                            final_response = getattr(content.parts, "text", "")
                        elif hasattr(content, "text"):
                            final_response = content.text
                        else:
                            final_response = str(content)

        logger.info(f"Invoke completed: response_length={len(final_response)}")

        return {"output": final_response or ""}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing invoke request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Slack Bolt integration (optional)
if SLACK_ENABLED and _bolt_app is not None:
    @_bolt_app.event("app_mention")
    async def handle_app_mention(event: Dict[str, Any], say: Any, logger: Any) -> None:
        """Handle @mentions of the bot in Slack channels"""
        try:
            user_id = event["user"]
            text = event.get("text", "")
            session_id = event.get("thread_ts", event["ts"])

            logger.info(f"Slack mention: user_id={user_id}, session_id={session_id}")

            # Run agent
            final_response = ""
            async for event in runner.run_async(
                app_name="bobs-brain",
                user_id=user_id,
                session_id=session_id,
                new_message=text
            ):
                if hasattr(event, "is_final_response") and callable(event.is_final_response):
                    if event.is_final_response():
                        if hasattr(event, "content") and event.content:
                            content = event.content
                            if hasattr(content, "parts"):
                                final_response = getattr(content.parts, "text", "")
                            elif hasattr(content, "text"):
                                final_response = content.text
                            else:
                                final_response = str(content)

            # Send response to Slack
            await say(
                text=final_response or "No response generated",
                thread_ts=session_id
            )

        except Exception as e:
            logger.error(f"Error handling Slack mention: {e}", exc_info=True)
            await say(
                text=f"❌ Error processing request: {str(e)}",
                thread_ts=session_id
            )

    @app.post("/slack/events")
    async def slack_events(request: Request) -> Any:
        """Handle Slack events via Bolt framework"""
        if _slack_handler:
            return await _slack_handler.handle(request)
        else:
            raise HTTPException(
                status_code=503,
                detail="Slack integration not available"
            )
else:
    logger.info("Slack integration disabled")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    logger.info(f"Starting service on port {port}...")

    uvicorn.run(
        "service.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
