"""
Reasoning Engine REST Client

This module provides functions to call Vertex AI Reasoning Engine
via REST API (:query and :streamQuery endpoints).

CRITICAL: This is a pure REST client - it does NOT import or run ADK Runner.
The agent runs inside Vertex AI Reasoning Engine, not here.
"""

import os
import json
import requests
from google.auth.transport.requests import Request
import google.auth

# Reasoning Engine API root
_API_ROOT = "https://aiplatform.googleapis.com/v1beta1"


def _auth_headers():
    """
    Get authentication headers using Application Default Credentials.

    Returns:
        dict: Headers with Bearer token for API authentication
    """
    creds, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    if not creds.valid:
        creds.refresh(Request())
    return {"Authorization": f"Bearer {creds.token}"}


def query_engine(engine_name: str, payload: dict) -> dict:
    """
    Call Reasoning Engine :query endpoint (non-streaming).

    Args:
        engine_name: Full resource name (projects/.../reasoningEngines/...)
        payload: Request payload (e.g., {"input": {"text": "..."}})

    Returns:
        dict: JSON response from Reasoning Engine

    Raises:
        requests.HTTPError: If API call fails

    Example:
        >>> result = query_engine(
        ...     "projects/my-proj/locations/us-central1/reasoningEngines/my-engine",
        ...     {"input": {"text": "Hello"}}
        ... )
        >>> print(result["output"])
    """
    url = f"{_API_ROOT}/{engine_name}:query"
    headers = {"Content-Type": "application/json", **_auth_headers()}

    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        timeout=60
    )
    r.raise_for_status()
    return r.json()


def stream_query_engine(engine_name: str, payload: dict):
    """
    Call Reasoning Engine :streamQuery endpoint (Server-Sent Events).

    Args:
        engine_name: Full resource name (projects/.../reasoningEngines/...)
        payload: Request payload (e.g., {"input": {"text": "..."}})

    Yields:
        str: SSE data lines from Reasoning Engine

    Raises:
        requests.HTTPError: If API call fails

    Example:
        >>> for chunk in stream_query_engine(engine_name, payload):
        ...     print(chunk)
    """
    import sseclient

    url = f"{_API_ROOT}/{engine_name}:streamQuery"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        **_auth_headers()
    }

    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        stream=True,
        timeout=300
    )
    r.raise_for_status()

    client = sseclient.SSEClient(r)
    for ev in client.events():
        yield ev.data
