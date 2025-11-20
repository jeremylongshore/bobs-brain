"""
Slack Webhook - FastAPI Proxy to Agent Engine

Enforces R3: Cloud Run as gateway only (proxy to Agent Engine via REST).

This service:
1. Receives Slack events (mentions, DMs)
2. Proxies to Agent Engine via REST API
3. Does NOT import Runner (R3 compliance)
4. Returns responses to Slack

Environment Variables:
- SLACK_BOT_TOKEN: Slack bot OAuth token (xoxb-...)
- SLACK_SIGNING_SECRET: Slack app signing secret
- AGENT_ENGINE_URL: Full URL to Agent Engine REST endpoint
- PROJECT_ID: GCP project ID
- LOCATION: GCP region
- AGENT_ENGINE_ID: Agent Engine instance ID
- PORT: Service port (default 8080)
- SLACK_SWE_PIPELINE_MODE: Routing mode (local|engine) - Phase AE2
- A2A_GATEWAY_URL: A2A gateway URL (for engine mode) - Phase AE2
"""

import os
import logging
import hashlib
import hmac
import time
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Environment configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")
PORT = int(os.getenv("PORT", "8080"))

# Agent Engine REST API endpoint
AGENT_ENGINE_URL = os.getenv(
    "AGENT_ENGINE_URL",
    f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}:query",
)

# Phase AE2: SWE Pipeline Mode Configuration
# Controls how SWE pipeline commands are routed
SLACK_SWE_PIPELINE_MODE = os.getenv("SLACK_SWE_PIPELINE_MODE", "local").lower()
# Options:
#   - "local" (default): Forward directly to Agent Engine (current behavior)
#   - "engine": Call a2a_gateway for SWE pipeline orchestration (Phase AE3)

# A2A Gateway URL (for future Option B in Phase AE3)
A2A_GATEWAY_URL = os.getenv(
    "A2A_GATEWAY_URL",
    "https://a2a-gateway-SERVICE_HASH-uc.a.run.app"  # Placeholder
)

# Validate required environment variables
if not all(
    [SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, PROJECT_ID, LOCATION, AGENT_ENGINE_ID]
):
    raise ValueError("Missing required environment variables")

# Create FastAPI app
app = FastAPI(
    title="Bob's Brain Slack Webhook",
    description="Slack event handler proxying to Vertex AI Agent Engine",
    version="0.6.0",
)

# Slack API client
slack_client = httpx.AsyncClient(
    base_url="https://slack.com/api",
    headers={
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json",
    },
)


def verify_slack_signature(body: bytes, timestamp: str, signature: str) -> bool:
    """
    Verify Slack request signature.

    Args:
        body: Raw request body
        timestamp: X-Slack-Request-Timestamp header
        signature: X-Slack-Signature header

    Returns:
        bool: True if signature is valid
    """
    # Prevent replay attacks (timestamp > 5 min old)
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    # Compute expected signature
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    expected_signature = (
        "v0="
        + hmac.new(
            SLACK_SIGNING_SECRET.encode(), sig_basestring.encode(), hashlib.sha256
        ).hexdigest()
    )

    # Compare signatures (constant-time)
    return hmac.compare_digest(expected_signature, signature)


@app.post("/slack/events")
async def slack_events(
    request: Request,
    x_slack_request_timestamp: str = Header(None),
    x_slack_signature: str = Header(None),
) -> Dict[str, Any]:
    """
    Handle Slack events.

    Receives events from Slack (mentions, DMs) and proxies to Agent Engine.

    R3 Compliance: Does NOT run agent locally - proxies via REST.

    Events handled:
    - app_mention: @Bob mentions
    - message.im: Direct messages
    - message.channels: Channel messages

    Returns:
        dict: Slack-formatted response
    """
    try:
        # Read raw body for signature verification
        body = await request.body()

        # Verify Slack signature (production security)
        if x_slack_request_timestamp and x_slack_signature:
            if not verify_slack_signature(
                body, x_slack_request_timestamp, x_slack_signature
            ):
                logger.warning("Invalid Slack signature")
                raise HTTPException(status_code=401, detail="Invalid signature")

        # Parse JSON
        data = await request.json()

        # Slack URL verification challenge
        if data.get("type") == "url_verification":
            logger.info("Slack URL verification challenge received")
            return {"challenge": data.get("challenge")}

        # Handle event callback
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            event_type = event.get("type")

            # Ignore bot messages (prevent loops)
            if event.get("bot_id"):
                logger.info("Ignoring bot message")
                return {"ok": True}

            # Ignore retry attempts (Slack retries if no 200 within 3s)
            if request.headers.get("x-slack-retry-num"):
                logger.info("Ignoring Slack retry")
                return {"ok": True}

            # Extract message text
            text = event.get("text", "")
            user_id = event.get("user")
            channel_id = event.get("channel")
            thread_ts = event.get("thread_ts") or event.get("ts")

            logger.info(
                f"Slack event: {event_type}",
                extra={
                    "user": user_id,
                    "channel": channel_id,
                    "text_length": len(text),
                },
            )

            # Remove bot mention from text
            text = text.replace("<@U07NRCYJX8A>", "").strip()  # Bob's user ID

            if not text:
                logger.info("Empty message after mention removal")
                return {"ok": True}

            # Query Agent Engine via REST (R3: no local Runner)
            agent_response = await query_agent_engine(
                query=text, session_id=f"{user_id}_{channel_id}"
            )

            # Post response to Slack
            await post_slack_message(
                channel=channel_id, text=agent_response, thread_ts=thread_ts
            )

            return {"ok": True}

        logger.warning(f"Unhandled Slack event type: {data.get('type')}")
        return {"ok": True}

    except Exception as e:
        logger.error(f"Slack event processing failed: {e}", exc_info=True)
        # Return 200 to Slack to prevent retries
        return {"ok": True}


async def query_agent_engine(query: str, session_id: str) -> str:
    """
    Query Agent Engine via REST API.

    R3 Compliance: Proxies to Agent Engine, does not run locally.

    Phase AE2: Added Option B path (commented) for future SWE pipeline mode.
    When SLACK_SWE_PIPELINE_MODE=engine, queries will route through a2a_gateway
    instead of directly to Agent Engine.

    Args:
        query: User query text
        session_id: Session identifier for memory

    Returns:
        str: Agent response text
    """
    try:
        # ===========================================================================
        # PHASE AE2: OPTION B PATH (COMMENTED - NOT YET ENABLED)
        # ===========================================================================
        # Phase AE3 will enable this path for SWE pipeline commands
        #
        # if SLACK_SWE_PIPELINE_MODE == "engine":
        #     # Option B: Route through a2a_gateway for multi-agent orchestration
        #     logger.info(
        #         "Routing to a2a_gateway (Option B - SWE Pipeline Mode)",
        #         extra={"query_length": len(query), "session_id": session_id}
        #     )
        #
        #     # Build A2A call payload
        #     a2a_payload = {
        #         "agent_role": "foreman",  # Route to iam-senior-adk-devops-lead
        #         "prompt": query,
        #         "session_id": session_id,
        #         "caller_spiffe_id": "spiffe://intent.solutions/slack/webhook",
        #         "env": os.getenv("DEPLOYMENT_ENV", "prod"),
        #     }
        #
        #     async with httpx.AsyncClient(timeout=60.0) as client:
        #         response = await client.post(
        #             f"{A2A_GATEWAY_URL}/a2a/run",
        #             json=a2a_payload,
        #             headers={"Content-Type": "application/json"}
        #         )
        #         response.raise_for_status()
        #         result = response.json()
        #
        #     return result.get("response", "No response from A2A gateway")
        # else:
        #     # Option A (default): Direct Agent Engine proxy (current behavior)
        #     logger.info(
        #         "Routing directly to Agent Engine (Option A - current)",
        #         extra={"query_length": len(query), "session_id": session_id}
        #     )
        # ===========================================================================

        # CURRENT BEHAVIOR (Option A): Direct Agent Engine proxy
        payload = {"query": query, "session_id": session_id}

        logger.info(
            "Querying Agent Engine",
            extra={"agent_engine_url": AGENT_ENGINE_URL, "session_id": session_id},
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                AGENT_ENGINE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            response.raise_for_status()
            result = response.json()

        # Extract response text (adjust based on Agent Engine response format)
        response_text = result.get("response", "I couldn't generate a response.")

        logger.info(
            "Agent Engine response received",
            extra={"response_length": len(response_text), "session_id": session_id},
        )

        return response_text

    except httpx.HTTPStatusError as e:
        logger.error(
            f"Agent Engine returned error: {e.response.status_code}",
            extra={"detail": e.response.text},
            exc_info=True,
        )
        return "Sorry, I encountered an error processing your request."

    except httpx.RequestError as e:
        logger.error(f"Failed to connect to Agent Engine: {e}", exc_info=True)
        return "Sorry, I'm having trouble connecting to my backend."

    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        return "Sorry, something went wrong."


async def post_slack_message(channel: str, text: str, thread_ts: str = None) -> None:
    """
    Post message to Slack channel.

    Args:
        channel: Slack channel ID
        text: Message text
        thread_ts: Thread timestamp (for replies)
    """
    try:
        payload = {"channel": channel, "text": text}

        if thread_ts:
            payload["thread_ts"] = thread_ts

        response = await slack_client.post("/chat.postMessage", json=payload)
        response.raise_for_status()

        logger.info(
            "Message posted to Slack",
            extra={"channel": channel, "thread_ts": thread_ts},
        )

    except Exception as e:
        logger.error(f"Failed to post Slack message: {e}", exc_info=True)


@app.get("/health")
async def health() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: Service health status
    """
    return {
        "status": "healthy",
        "service": "slack-webhook",
        "version": "0.6.0",
        "agent_engine_url": AGENT_ENGINE_URL,
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint - service info.

    Returns:
        dict: Service metadata
    """
    return {
        "name": "Bob's Brain Slack Webhook",
        "version": "0.6.0",
        "description": "Slack event handler proxying to Vertex AI Agent Engine",
        "endpoints": {"events": "/slack/events", "health": "/health"},
    }


if __name__ == "__main__":
    import uvicorn

    logger.info(
        f"Starting Slack Webhook on port {PORT}",
        extra={
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "agent_engine_id": AGENT_ENGINE_ID,
        },
    )

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
