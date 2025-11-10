"""
Slack Webhook Integration for Bob's Vertex AI Agent Engine

This Cloud Function receives Slack events and forwards them to Bob's Agent Engine.

Uses Firestore for event deduplication and thread-local connection sessions
to handle concurrent requests reliably.

DEPLOYMENT: 2025-11-10 v2 - Comprehensive fix with Firestore + thread-local sessions
"""

import functions_framework
import json
import logging
import os
import threading
from datetime import datetime, timedelta
import google.auth
from google.cloud import secretmanager, firestore
from slack_sdk import WebClient
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent Engine configuration
PROJECT_ID = os.getenv("PROJECT_ID", "bobs-brain")
REGION = "us-central1"
AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"

# Firestore client for event deduplication
_firestore_client = None

# Thread-local storage for requests sessions
_thread_sessions = threading.local()


def get_firestore_client():
    """Get or create Firestore client (lazy initialization)."""
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = firestore.Client(project=PROJECT_ID)
    return _firestore_client


def is_duplicate_event(event_id: str) -> bool:
    """
    Check if event has already been processed using Firestore.

    Uses atomic document creation to prevent race conditions.
    Returns True if event is duplicate, False if new.
    """
    if not event_id:
        return False

    try:
        db = get_firestore_client()
        doc_ref = db.collection('slack_events').document(event_id)

        # Try to create document atomically
        # If it already exists, this will raise an exception
        doc_ref.create({
            'processed_at': firestore.SERVER_TIMESTAMP,
            'expires_at': datetime.utcnow() + timedelta(hours=1)
        })

        logger.info(f"New event: {event_id}")
        return False  # Successfully created = new event

    except Exception as e:
        # Document already exists = duplicate
        logger.info(f"Duplicate event detected: {event_id}")
        return True


def get_requests_session():
    """
    Get thread-local requests session with retry strategy.

    Each thread gets its own isolated connection pool to prevent
    SSL connection exhaustion under concurrent load.
    """
    if not hasattr(_thread_sessions, 'session'):
        import requests

        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )

        # Configure adapter with isolated connection pool
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=1,  # Only 1 connection per thread
            pool_maxsize=1       # Max 1 connection per thread
        )

        session.mount("https://", adapter)
        _thread_sessions.session = session

        logger.info(f"Created new requests session for thread {threading.current_thread().name}")

    return _thread_sessions.session


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


def query_agent_engine_stream(query: str, user_id: str, session_id: str = None):
    """
    Query the Vertex AI Agent Engine using REST API.

    Uses direct REST API calls with thread-local connection sessions
    to prevent SSL connection exhaustion under concurrent load.
    """
    from google.auth.transport.requests import Request

    try:
        # Get credentials
        credentials, _ = google.auth.default()
        credentials.refresh(Request())

        # Build REST API URL
        url = f"https://us-central1-aiplatform.googleapis.com/v1/{AGENT_ENGINE_ID}:streamQuery"

        # Headers with authentication
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }

        # Payload - do NOT include session_id to let ADK create new sessions
        # This avoids "Invalid Session resource name" errors
        payload = {
            "input": {
                "message": query,
                "user_id": user_id
                # session_id omitted - let ADK handle session creation
            }
        }

        logger.info(f"[{threading.current_thread().name}] Querying Agent Engine for user {user_id}: {query[:50]}...")

        # Get thread-local session with isolated connection pool
        session = get_requests_session()

        # Make streaming request with 60-second timeout
        # Agent Engine typically responds in 10-15 seconds
        response = session.post(url, json=payload, headers=headers, timeout=60, stream=True)

        if response.status_code != 200:
            error_msg = f"Agent Engine returned {response.status_code}: {response.text[:200]}"
            logger.error(error_msg)
            return f"Sorry, I'm having trouble connecting. Error: {response.status_code}"

        # Parse streaming response
        full_response = []
        try:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        logger.info(f"Stream event received: {str(data)[:200]}...")

                        # Extract text from response structure: content.parts[].text
                        if "content" in data and "parts" in data["content"]:
                            for part in data["content"]["parts"]:
                                if "text" in part:
                                    full_response.append(part["text"])

                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse JSON line: {e}")
                        continue
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError) as e:
            # Connection closed normally after streaming - this is expected
            logger.info(f"Stream connection closed (normal): {type(e).__name__}")
        finally:
            # Always close the response to free resources
            response.close()

        response_text = "".join(full_response) if full_response else "I received your message but couldn't generate a response."
        logger.info(f"Agent response ({len(response_text)} chars): {response_text[:200]}...")
        return response_text

    except Exception as e:
        # Catch all exceptions including Timeout and SSLError
        error_type = type(e).__name__
        error_msg = str(e)[:200]

        logger.error(f"[{threading.current_thread().name}] Agent Engine error: {error_type}: {error_msg}", exc_info=True)

        # Return user-friendly error messages
        if "timeout" in error_type.lower() or "timeout" in error_msg.lower():
            return "Sorry, I'm taking too long to respond. Please try again in a moment."
        elif "ssl" in error_type.lower() or "ssl" in error_msg.lower():
            return "Sorry, I'm having connection issues. Please try again."
        else:
            return "Sorry, I encountered an error. Please try again."


def _process_slack_message(text, channel, user, event_id):
    """Background processing of Slack messages"""
    try:
        logger.info(f"Processing Slack message from {user} in {channel}: {text[:100]}...")

        # Create session ID for conversation context (per-user-per-channel)
        session_id = f"slack_{channel}_{user}"

        # Query the Agent Engine with streaming
        answer = query_agent_engine_stream(
            query=text,
            user_id=user,
            session_id=session_id
        )

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
    Cloud Function entry point for Slack events.

    Uses Firestore for atomic event deduplication across instances.
    Returns HTTP 200 immediately to prevent Slack retries.
    """
    payload = request.get_json(silent=True) or {}

    # Handle Slack URL verification (first-time setup)
    if payload.get("type") == "url_verification":
        return ({"challenge": payload.get("challenge")}, 200)

    event = payload.get("event", {})
    event_type = event.get("type")
    event_id = payload.get("event_id", "")

    # Deduplicate using Firestore (atomic, persists across instances)
    if is_duplicate_event(event_id):
        logger.info(f"Ignoring duplicate event: {event_id}")
        return ({"ok": True}, 200)

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
