"""
Slack Webhook Integration for Bob's Vertex AI Agent Engine

This Cloud Function receives Slack events and forwards them to Bob's Agent Engine.
"""

import functions_framework
import json
import logging
import os
import threading
import asyncio
import google.auth
from google.cloud import secretmanager
from slack_sdk import WebClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global cache for Slack events to prevent duplicates
_slack_event_cache = {}

# Agent Engine configuration
PROJECT_ID = os.getenv("PROJECT_ID", "bobs-brain")
REGION = "us-central1"
AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"


def get_secret(secret_id):
    """Retrieve secret from Google Secret Manager"""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Failed to retrieve secret {secret_id}: {e}")
        return None


async def query_agent_engine_async(query: str, user_id: str, session_id: str = None):
    """Query the Vertex AI Agent Engine using async streaming"""
    try:
        from vertexai.preview import reasoning_engines

        # Get the remote agent
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Collect streaming response
        full_response = []

        # Use async_stream_query with session management
        async for event in remote_agent.async_stream_query(
            message=query,
            user_id=user_id,
            session_id=session_id  # Maintains conversation context
        ):
            # Extract text content from events
            if event.get("type") == "content":
                data = event.get("data", {})
                if "parts" in data:
                    for part in data["parts"]:
                        if "text" in part:
                            full_response.append(part["text"])

        response_text = "".join(full_response)
        logger.info(f"Agent response: {response_text[:200]}...")
        return response_text

    except Exception as e:
        logger.error(f"Failed to query agent engine: {e}", exc_info=True)
        return f"Sorry, I'm having trouble connecting. Error: {str(e)[:200]}"


def _process_slack_message(text, channel, user, event_id):
    """Background processing of Slack messages"""
    try:
        logger.info(f"Processing Slack message from {user} in {channel}: {text[:100]}...")

        # Create session ID for conversation context (per-user-per-channel)
        session_id = f"slack_{channel}_{user}"

        # Query the Agent Engine with async streaming
        answer = asyncio.run(query_agent_engine_async(
            query=text,
            user_id=user,
            session_id=session_id
        ))

        # Get Slack bot token from Secret Manager
        slack_token = get_secret("slack-bot-token")
        if not slack_token:
            logger.error("Failed to retrieve Slack bot token")
            return

        # Send response to Slack
        slack_client = WebClient(token=slack_token)
        slack_client.chat_postMessage(
            channel=channel,
            text=answer,
            unfurl_links=False,
            unfurl_media=False
        )
        logger.info(f"Sent response to Slack channel {channel}")

    except Exception as e:
        logger.error(f"Error processing Slack message: {e}")


@functions_framework.http
def slack_events(request):
    """
    Cloud Function entry point for Slack events

    Responds to messages in Slack by forwarding to Vertex AI Agent Engine.
    Returns HTTP 200 immediately to prevent Slack retries.
    """
    payload = request.get_json(silent=True) or {}

    # Handle Slack URL verification (first-time setup)
    if payload.get("type") == "url_verification":
        return ({"challenge": payload.get("challenge")}, 200)

    event = payload.get("event", {})
    event_type = event.get("type")
    event_id = payload.get("event_id", "")

    # Deduplicate: Slack retries if we don't respond fast enough
    if event_id and event_id in _slack_event_cache:
        logger.info(f"Ignoring duplicate event: {event_id}")
        return ({"ok": True}, 200)

    if event_id:
        _slack_event_cache[event_id] = True

    # Ignore bot messages to prevent loops
    if event.get("bot_id") or event.get("user") == "USLACKBOT":
        return ({"ok": True}, 200)

    # Only respond to messages and mentions
    if event_type not in ["message", "app_mention"]:
        return ({"ok": True}, 200)

    text = event.get("text", "")
    channel = event.get("channel")
    user = event.get("user")

    if not text or not channel:
        return ({"ok": True}, 200)

    # Process message in background thread to return HTTP 200 immediately
    thread = threading.Thread(
        target=_process_slack_message,
        args=(text, channel, user, event_id),
        daemon=True
    )
    thread.start()

    # Return HTTP 200 immediately to acknowledge receipt
    logger.info(f"Queued Slack message from {user} for background processing")
    return ({"ok": True}, 200)
