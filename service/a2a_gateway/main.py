"""
A2A Gateway - FastAPI Proxy to Agent Engine

Enforces R3: Cloud Run as gateway only (proxy to Agent Engine via REST).

This service:
1. Exposes AgentCard at /.well-known/agent.json
2. Proxies queries to Agent Engine via REST API
3. Does NOT import Runner (R3 compliance)
4. Deployed to Cloud Run as gateway

Environment Variables:
- AGENT_ENGINE_URL: Full URL to Agent Engine REST endpoint
- PROJECT_ID: GCP project ID
- LOCATION: GCP region
- AGENT_ENGINE_ID: Agent Engine instance ID
- PORT: Service port (default 8080)
"""

import os
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment configuration
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")
PORT = int(os.getenv("PORT", "8080"))

# Agent Engine REST API endpoint
# Format: https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}:query
AGENT_ENGINE_URL = os.getenv(
    "AGENT_ENGINE_URL",
    f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}:query"
)

# Validate required environment variables
if not all([PROJECT_ID, LOCATION, AGENT_ENGINE_ID]):
    raise ValueError("Missing required environment variables: PROJECT_ID, LOCATION, AGENT_ENGINE_ID")

# Create FastAPI app
app = FastAPI(
    title="Bob's Brain A2A Gateway",
    description="A2A Protocol gateway proxying to Vertex AI Agent Engine",
    version="0.6.0"
)

# Import AgentCard (safe - no Runner import)
# This imports only the card definition, not the agent runtime
from my_agent.a2a_card import get_agent_card, get_agent_card_dict


@app.get("/.well-known/agent.json")
async def agent_card() -> Dict[str, Any]:
    """
    A2A Protocol: Return AgentCard for agent discovery.

    This endpoint is required by the A2A protocol specification
    for agent discovery and capability negotiation.

    Returns:
        dict: AgentCard with agent metadata and capabilities
    """
    try:
        card_dict = get_agent_card_dict()
        logger.info("AgentCard served", extra={"spiffe_id": card_dict.get("spiffe_id")})
        return card_dict
    except Exception as e:
        logger.error(f"Failed to generate AgentCard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate AgentCard")


@app.post("/query")
async def query(request: Request) -> Dict[str, Any]:
    """
    Proxy query to Agent Engine via REST API.

    R3 Compliance: This gateway does NOT run the agent locally.
    It proxies requests to the Agent Engine REST endpoint.

    Body:
        {
            "query": "user question",
            "session_id": "optional-session-id"
        }

    Returns:
        dict: Agent response from Agent Engine
    """
    try:
        # Parse request body
        body = await request.json()
        query_text = body.get("query")
        session_id = body.get("session_id")

        if not query_text:
            raise HTTPException(status_code=400, detail="Missing 'query' field")

        logger.info(
            "Proxying query to Agent Engine",
            extra={
                "query_length": len(query_text),
                "session_id": session_id,
                "agent_engine_url": AGENT_ENGINE_URL
            }
        )

        # Prepare request to Agent Engine
        payload = {
            "query": query_text
        }

        if session_id:
            payload["session_id"] = session_id

        # Call Agent Engine via REST API (R3: no local Runner)
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                AGENT_ENGINE_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )

            response.raise_for_status()
            result = response.json()

        logger.info(
            "Agent Engine response received",
            extra={
                "status_code": response.status_code,
                "session_id": session_id
            }
        )

        return result

    except httpx.HTTPStatusError as e:
        logger.error(
            f"Agent Engine returned error: {e.response.status_code}",
            extra={"detail": e.response.text},
            exc_info=True
        )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Agent Engine error: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to Agent Engine: {e}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail="Agent Engine unavailable"
        )
    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: Service health status
    """
    return {
        "status": "healthy",
        "service": "a2a-gateway",
        "version": "0.6.0",
        "agent_engine_url": AGENT_ENGINE_URL
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint - service info.

    Returns:
        dict: Service metadata
    """
    return {
        "name": "Bob's Brain A2A Gateway",
        "version": "0.6.0",
        "description": "A2A Protocol gateway to Vertex AI Agent Engine",
        "endpoints": {
            "agent_card": "/.well-known/agent.json",
            "query": "/query",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn

    logger.info(
        f"Starting A2A Gateway on port {PORT}",
        extra={
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "agent_engine_id": AGENT_ENGINE_ID
        }
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
