#!/usr/bin/env python3
"""
Complete solution for querying ADK agent deployed to Vertex AI Agent Engine.
This shows multiple methods that work.
"""

import os
import json
import logging
from typing import Optional, Dict, Any

# Configure environment
os.environ["GOOGLE_CLOUD_PROJECT"] = "bobs-brain"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

# Your Agent Engine ID
AGENT_ENGINE_ID = "5828234061910376448"
FULL_AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# METHOD 1: Using stream_query (Streaming Response)
# ============================================================================
def query_agent_streaming(query: str, user_id: str, session_id: Optional[str] = None) -> str:
    """
    Query the agent using stream_query for streaming responses.
    This is what your Slack webhook uses and it works!
    """
    try:
        import vertexai
        from vertexai.preview import reasoning_engines

        # Initialize Vertex AI
        vertexai.init(
            project=os.environ["GOOGLE_CLOUD_PROJECT"],
            location=os.environ["GOOGLE_CLOUD_LOCATION"]
        )

        # Get the remote agent - use just the ID, not the full path
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Collect streaming response
        full_response = []

        # Call stream_query - this method IS available, but dynamically registered
        for event in remote_agent.stream_query(
            input={
                "message": query,
                "user_id": user_id,
                "session_id": session_id or f"session_{user_id}"
            }
        ):
            # Process streaming events
            if isinstance(event, dict):
                if "output" in event:
                    full_response.append(str(event["output"]))
                elif "text" in event:
                    full_response.append(event["text"])
                else:
                    full_response.append(str(event))

        return "".join(full_response) if full_response else "No response received"

    except AttributeError as e:
        # If stream_query isn't available, fall back to REST API
        logger.error(f"stream_query not available: {e}")
        return query_agent_rest_api(query, user_id, session_id)
    except Exception as e:
        logger.error(f"Streaming query failed: {e}")
        return f"Error: {str(e)}"


# ============================================================================
# METHOD 2: Using Direct REST API Call (Most Reliable)
# ============================================================================
def query_agent_rest_api(query: str, user_id: str, session_id: Optional[str] = None) -> str:
    """
    Query the agent using direct REST API call.
    This bypasses SDK issues and directly calls the Agent Engine API.
    """
    import google.auth
    from google.auth.transport.requests import Request
    import requests

    try:
        # Get credentials
        credentials, project = google.auth.default()
        credentials.refresh(Request())

        # Build the URL for streaming
        url = f"https://us-central1-aiplatform.googleapis.com/v1/{FULL_AGENT_ENGINE_ID}:streamQuery"

        # Headers with authentication
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }

        # Payload matching the ADK schema
        payload = {
            "input": {
                "message": query,
                "user_id": user_id,
                "session_id": session_id or f"session_{user_id}"
            }
        }

        # Make the request
        response = requests.post(url, json=payload, headers=headers, timeout=30, stream=True)

        if response.status_code != 200:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return f"API Error: {response.status_code}"

        # Process streaming response
        full_response = []
        for line in response.iter_lines():
            if line:
                try:
                    # Parse JSON from each line
                    data = json.loads(line.decode('utf-8'))
                    if "output" in data:
                        full_response.append(str(data["output"]))
                    elif "text" in data:
                        full_response.append(data["text"])
                except json.JSONDecodeError:
                    # Some lines might not be JSON
                    continue

        return "".join(full_response) if full_response else "No response received"

    except Exception as e:
        logger.error(f"REST API call failed: {e}")
        return f"Error: {str(e)}"


# ============================================================================
# METHOD 3: Using query() for Non-Streaming (if available)
# ============================================================================
def query_agent_non_streaming(query: str, user_id: str, session_id: Optional[str] = None) -> str:
    """
    Query the agent using non-streaming query method.
    Note: This may not be available for all agent configurations.
    """
    try:
        import vertexai
        from vertexai.preview import reasoning_engines

        # Initialize Vertex AI
        vertexai.init(
            project=os.environ["GOOGLE_CLOUD_PROJECT"],
            location=os.environ["GOOGLE_CLOUD_LOCATION"]
        )

        # Get the remote agent
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Try to use query() method if available
        result = remote_agent.query(
            input={
                "message": query,
                "user_id": user_id,
                "session_id": session_id or f"session_{user_id}"
            }
        )

        # Extract response
        if isinstance(result, dict):
            return result.get("output", str(result))
        else:
            return str(result)

    except AttributeError:
        # query() not available, use streaming instead
        return query_agent_streaming(query, user_id, session_id)
    except Exception as e:
        logger.error(f"Non-streaming query failed: {e}")
        return f"Error: {str(e)}"


# ============================================================================
# CLOUD FUNCTION IMPLEMENTATION
# ============================================================================
def cloud_function_query_agent(request):
    """
    Example Cloud Function implementation that queries the agent.
    This shows how to use the above methods in a Cloud Function context.
    """
    import functions_framework

    # Parse request
    request_json = request.get_json(silent=True) or {}

    query = request_json.get("query", "Hello, Bob!")
    user_id = request_json.get("user_id", "cloud_function_user")
    session_id = request_json.get("session_id")

    # Try methods in order of preference
    response = None

    # Method 1: Try streaming (most feature-rich)
    try:
        response = query_agent_streaming(query, user_id, session_id)
        method_used = "streaming"
    except Exception as e:
        logger.warning(f"Streaming failed: {e}")

        # Method 2: Fall back to REST API
        try:
            response = query_agent_rest_api(query, user_id, session_id)
            method_used = "rest_api"
        except Exception as e:
            logger.error(f"All methods failed: {e}")
            response = "Sorry, I'm unable to process your request at this time."
            method_used = "failed"

    # Return response
    return {
        "response": response,
        "method_used": method_used,
        "agent_id": AGENT_ENGINE_ID
    }


# ============================================================================
# TEST THE METHODS
# ============================================================================
if __name__ == "__main__":
    test_query = "What is the hustle project?"
    test_user_id = "test_user_123"
    test_session_id = "test_session_456"

    print("=" * 80)
    print("TESTING AGENT ENGINE QUERY METHODS")
    print("=" * 80)
    print(f"Agent ID: {AGENT_ENGINE_ID}")
    print(f"Query: {test_query}")
    print(f"User ID: {test_user_id}")
    print(f"Session ID: {test_session_id}")
    print()

    # Test Method 1: Streaming
    print("METHOD 1: Testing stream_query()...")
    print("-" * 40)
    response1 = query_agent_streaming(test_query, test_user_id, test_session_id)
    print(f"Response: {response1[:500]}...")
    print()

    # Test Method 2: REST API
    print("METHOD 2: Testing REST API...")
    print("-" * 40)
    response2 = query_agent_rest_api(test_query, test_user_id, test_session_id)
    print(f"Response: {response2[:500]}...")
    print()

    # Test Method 3: Non-streaming
    print("METHOD 3: Testing query() (if available)...")
    print("-" * 40)
    response3 = query_agent_non_streaming(test_query, test_user_id, test_session_id)
    print(f"Response: {response3[:500]}...")
    print()

    print("=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)