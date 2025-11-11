"""
Bob's Brain Gateway - Cloud Run FastAPI Proxy

This gateway proxies requests to Vertex AI Reasoning Engine via REST API.
CRITICAL: This does NOT run the agent - it calls the remote Reasoning Engine.

Features:
- OpenTelemetry instrumentation with Cloud Trace export
- Non-streaming (/invoke) and streaming (/invoke/stream) endpoints
- A2A protocol endpoints (/card, /.well-known/agent-card.json)
- Health checks with trace headers
- No ADK Runner imports (architectural boundary)

Environment Variables:
    AGENT_ENGINE_NAME: Full resource name (projects/.../reasoningEngines/...)
    AGENT_ENGINE_ID: Alternative to AGENT_ENGINE_NAME
    PROJECT_ID: GCP project ID
    LOCATION: GCP region (default: us-central1)
    ENGINE_MODE: agent_engine (prod) - do NOT use adk_local here
    A2A_NAME: Agent name for A2A card
    A2A_DESC: Agent description
    A2A_VERSION: Agent version
"""

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.gcp_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from gateway.engine_client import query_engine, stream_query_engine

# Configuration
ENGINE_NAME = os.getenv("AGENT_ENGINE_NAME") or os.getenv("AGENT_ENGINE_ID")
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "us-central1")
MODE = os.getenv("ENGINE_MODE", "agent_engine")  # Do not run ADK here

# OpenTelemetry setup for Cloud Trace
provider = TracerProvider(
    resource=Resource.create({"service.name": "bobs-brain-gateway"})
)
provider.add_span_processor(BatchSpanProcessor(CloudTraceSpanExporter()))
trace.set_tracer_provider(provider)

# Instrument FastAPI and requests
FastAPIInstrumentor().instrument()
RequestsInstrumentor().instrument()

# FastAPI application
app = FastAPI(title="Bob Gateway", version="4.0.0")

# A2A Card configuration
A2A_NAME = os.getenv("A2A_NAME", "Bob's Brain")
A2A_DESC = os.getenv(
    "A2A_DESC",
    "A2A gateway. Agent runs on Vertex AI Reasoning Engine."
)
A2A_VERSION = os.getenv("A2A_VERSION", "4.0.0")

CARD = {
    "name": A2A_NAME,
    "description": A2A_DESC,
    "version": A2A_VERSION,
    "capabilities": {"streaming": True},
    "skills": [
        {
            "id": "get_time",
            "name": "Get Current Time",
            "description": "UTC clock"
        }
    ],
    "engine": {
        "name": ENGINE_NAME,
        "location": LOCATION
    }
}


def trace_headers():
    """
    Extract trace ID from current OpenTelemetry span.

    Returns:
        dict: Headers with X-Trace-Id for distributed tracing
    """
    span = trace.get_current_span()
    ctx = span.get_span_context() if span else None
    if ctx and ctx.is_valid:
        return {"X-Trace-Id": f"{ctx.trace_id:032x}"}
    return {}


@app.get("/_health")
def health():
    """
    Health check endpoint with trace headers.

    Returns:
        JSONResponse: Status, mode, and engine information
    """
    return JSONResponse(
        {
            "status": "ok",
            "mode": MODE,
            "engine": ENGINE_NAME
        },
        headers=trace_headers()
    )


@app.get("/card")
def card():
    """A2A AgentCard metadata endpoint."""
    return CARD


@app.get("/.well-known/agent-card.json")
def well_known_card():
    """A2A AgentCard discovery endpoint (well-known URI)."""
    return CARD


@app.post("/invoke")
async def invoke(req: Request):
    """
    Non-streaming proxy to Reasoning Engine :query endpoint.

    Request body:
        {
            "text": "user query",
            "input": {...}  # Alternative format
        }

    Response:
        JSON response from Reasoning Engine with trace headers

    Raises:
        HTTPException: If ENGINE_NAME not configured or API call fails
    """
    if not ENGINE_NAME:
        raise HTTPException(500, "AGENT_ENGINE_NAME or AGENT_ENGINE_ID not set")

    body = await req.json()

    # Build payload - support both text and input formats
    payload = {
        "input": body.get("input") or {"text": body.get("text") or ""}
    }

    # Call Reasoning Engine
    out = query_engine(ENGINE_NAME, payload)

    return JSONResponse(out, headers=trace_headers())


@app.post("/invoke/stream")
async def invoke_stream(req: Request):
    """
    Streaming proxy to Reasoning Engine :streamQuery endpoint.

    Request body:
        {
            "text": "user query",
            "input": {...}  # Alternative format
        }

    Response:
        Server-Sent Events (SSE) stream from Reasoning Engine

    Raises:
        HTTPException: If ENGINE_NAME not configured or API call fails
    """
    if not ENGINE_NAME:
        raise HTTPException(500, "AGENT_ENGINE_NAME or AGENT_ENGINE_ID not set")

    body = await req.json()

    # Build payload
    payload = {
        "input": body.get("input") or {"text": body.get("text") or ""}
    }

    def gen():
        """Generator for SSE streaming."""
        for line in stream_query_engine(ENGINE_NAME, payload):
            yield f"data: {line}\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers=trace_headers()
    )
