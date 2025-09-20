#!/usr/bin/env python3
"""
BOB BRAIN v5.0 - Secure AI Assistant with Memory and Learning
Clean, clone-and-run Flask app with Slack integration and Circle of Life learning loop.
"""

import json
import logging
import os
import time
from typing import Any, Dict

from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from src.circle_of_life import get_circle_of_life

# Import validation and circle of life
from src.validation import LearnBody, QueryBody

# Configure logging
if os.getenv("RUNNING_IN_CLOUD_RUN"):
    try:
        import google.cloud.logging as gcl

        gcl.Client().setup_logging()
    except ImportError:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("bobs_brain")


def log_event(event: str, **kwargs):
    """Structured logging helper"""
    log.info(json.dumps({"event": event, "timestamp": time.time(), **kwargs}))


# External service connections (lazy initialization)
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
GCP_PROJECT = os.getenv("GCP_PROJECT")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")

# Initialize Neo4j driver if configured
neo4j_driver = None
if NEO4J_URI and NEO4J_USER and NEO4J_PASSWORD:
    try:
        from neo4j import GraphDatabase

        neo4j_driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD), max_connection_pool_size=10, connection_timeout=30
        )
        log_event("neo4j_connected", uri=NEO4J_URI)
    except Exception as e:
        log.warning(f"Neo4j initialization failed: {e}")

# Initialize BigQuery client if configured
bq_client = None
if GCP_PROJECT:
    try:
        from google.cloud import bigquery

        bq_client = bigquery.Client(project=GCP_PROJECT)
        log_event("bigquery_connected", project=GCP_PROJECT)
    except Exception as e:
        log.warning(f"BigQuery initialization failed: {e}")

# Initialize Slack client if configured
slack_client = None
if SLACK_BOT_TOKEN:
    try:
        from slack_sdk import WebClient

        slack_client = WebClient(token=SLACK_BOT_TOKEN, timeout=30)
        log_event("slack_connected")
    except Exception as e:
        log.warning(f"Slack initialization failed: {e}")

# Initialize Gemini AI client if configured
gemini_client = None
if GCP_PROJECT and GCP_LOCATION:
    try:
        import google.auth
        import google.generativeai as genai

        credentials, _ = google.auth.default()
        gemini_client = genai.Client(vertexai=True, project=GCP_PROJECT, location=GCP_LOCATION)
        log_event("gemini_connected", project=GCP_PROJECT, location=GCP_LOCATION)
    except Exception as e:
        log.warning(f"Gemini initialization failed: {e}")


def llm_call(payload: Dict[str, Any]) -> list:
    """LLM wrapper for Circle of Life"""
    if not gemini_client:
        # Return mock insight for testing when no LLM configured
        return [
            {
                "pattern": "test_pattern",
                "confidence": 0.9,
                "description": f"Mock insight for: {payload.get('task', 'unknown')}",
                "meta": payload.get("analysis", {}),
            }
        ]

    try:
        prompt = f"""
        Task: {payload.get('task', 'analyze')}
        Analysis: {json.dumps(payload.get('analysis', {}), indent=2)}

        Generate insights as JSON list with fields: pattern, confidence (0-1), description.
        Only include insights with confidence >= {payload.get('min_confidence', 0.6)}.
        """

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.GenerateContentConfig(temperature=0.3, max_output_tokens=1024),
        )

        if response and response.candidates:
            text = response.candidates[0].content.parts[0].text
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return [
                    {
                        "pattern": "parsing_error",
                        "confidence": 0.5,
                        "description": f"Failed to parse LLM response: {text[:100]}...",
                    }
                ]
    except Exception as e:
        log.error(f"LLM call failed: {e}")
        return []


# Flask app setup
app = Flask(__name__)

# CORS configuration
CORS(app, resources={r"/api/*": {"origins": "*"}, r"/slack/*": {"origins": "*"}})

# Rate limiting
limiter = Limiter(key_func=get_remote_address, app=app, default_limits=["60/minute"])

# API key authentication
API_KEY = os.getenv("BB_API_KEY")
OPEN_PATHS = {"/", "/health", "/metrics", "/slack/events"}


@app.before_request
def require_api_key():
    """Require API key for non-public endpoints"""
    if request.path in OPEN_PATHS:
        return

    key = request.headers.get("X-API-Key")
    if not API_KEY or key != API_KEY:
        log_event("unauthorized_access", path=request.path, ip=request.remote_addr)
        return jsonify({"error": "unauthorized"}), 401


# Metrics
REQUESTS = Counter("bb_requests_total", "Total requests", ["route"])
ERRORS = Counter("bb_errors_total", "Total errors", ["route", "type"])


@app.after_request
def count_requests(response):
    """Count requests for metrics"""
    try:
        REQUESTS.labels(request.path).inc()
        if response.status_code >= 400:
            ERRORS.labels(request.path, "http_error").inc()
    except Exception:
        pass
    return response


# Initialize Circle of Life
circle_of_life = get_circle_of_life(neo4j_driver=neo4j_driver, bq_client=bq_client, llm_call=llm_call, logger=log)


# Routes
@app.route("/", methods=["GET"])
def root():
    """Root endpoint with basic service info"""
    return jsonify(
        {
            "name": "bobs-brain",
            "version": "5.0",
            "status": "ok",
            "endpoints": ["/health", "/api/query", "/learn", "/slack/events", "/metrics"],
        }
    )


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    status = {
        "status": "ok",
        "timestamp": time.time(),
        "services": {
            "neo4j": bool(neo4j_driver),
            "bigquery": bool(bq_client),
            "slack": bool(slack_client),
            "gemini": bool(gemini_client),
        },
    }

    # Test Neo4j connection
    if neo4j_driver:
        try:
            with neo4j_driver.session() as session:
                session.run("RETURN 1")
            status["services"]["neo4j_connected"] = True
        except Exception as e:
            status["services"]["neo4j_connected"] = False
            status["services"]["neo4j_error"] = str(e)[:100]

    return jsonify(status)


@app.route("/metrics", methods=["GET"])
def metrics():
    """Prometheus metrics endpoint"""
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


@app.route("/api/query", methods=["POST"])
@limiter.limit("10/minute")
def api_query():
    """Direct intelligence query endpoint"""
    try:
        body = QueryBody.model_validate(request.get_json(force=True))
        log_event("api_query", query_length=len(body.query))

        # For now, return echo response
        # In production, this would use the full Bob Brain intelligence
        response = {"ok": True, "answer": f"Echo: {body.query}", "context": body.context, "timestamp": time.time()}

        return jsonify(response)

    except Exception as e:
        log.error(f"API query failed: {e}")
        ERRORS.labels("/api/query", "processing_error").inc()
        return jsonify({"error": "query processing failed"}), 500


@app.route("/learn", methods=["POST"])
@limiter.limit("5/minute")
def learn():
    """Submit learning correction data"""
    try:
        body = LearnBody.model_validate(request.get_json(force=True))
        log_event("learning_correction", correction_length=len(body.correction))

        # Trigger Circle of Life learning cycle
        events = [
            {
                "type": "correction",
                "correction": body.correction,
                "context": body.context,
                "timestamp": time.time(),
                "user_id": "api_user",
            }
        ]

        result = circle_of_life.run_once(events)

        return jsonify({"ok": True, "circle_of_life": result})

    except Exception as e:
        log.error(f"Learning failed: {e}")
        ERRORS.labels("/learn", "processing_error").inc()
        return jsonify({"error": "learning processing failed"}), 500


@app.route("/slack/events", methods=["POST"])
@limiter.limit("30/minute")
def slack_events():
    """Slack event webhook handler"""
    try:
        # In production, verify Slack signature here
        payload = request.get_json(silent=True) or {}

        # Handle URL verification challenge
        if payload.get("type") == "url_verification":
            return jsonify({"challenge": payload.get("challenge")})

        # Extract message from event
        event = payload.get("event", {})
        text = event.get("text", "")
        user = event.get("user", "unknown")

        if text:
            log_event("slack_message", user=user, text_length=len(text))

            # Trigger Circle of Life learning
            events = [
                {
                    "type": "slack_message",
                    "text": text,
                    "user_id": user,
                    "timestamp": time.time(),
                    "channel": event.get("channel"),
                }
            ]

            col_result = circle_of_life.run_once(events)

            # In production, would generate AI response and send back to Slack
            return jsonify({"ok": True, "handled": True, "circle_of_life": col_result})

        return jsonify({"ok": True, "handled": False})

    except Exception as e:
        log.error(f"Slack event processing failed: {e}")
        ERRORS.labels("/slack/events", "processing_error").inc()
        return jsonify({"error": "event processing failed"}), 500


@app.route("/circle-of-life/metrics", methods=["GET"])
def col_metrics():
    """Get Circle of Life metrics"""
    # Return basic metrics about the learning system
    return jsonify(
        {
            "ready": circle_of_life.ready(),
            "last_run": circle_of_life._last_run,
            "processed_hashes": len(circle_of_life._processed_hashes),
            "config": {
                "confidence_min": float(os.getenv("BB_CONFIDENCE_MIN", "0.6")),
                "batch_size": int(os.getenv("BB_COL_BATCH", "50")),
                "cooldown_sec": int(os.getenv("BB_COL_COOLDOWN", "60")),
            },
        }
    )


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "bad request"}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "unauthorized"}), 401


@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({"error": "rate limit exceeded"}), 429


@app.errorhandler(500)
def internal_error(error):
    log.error(f"Internal server error: {error}")
    return jsonify({"error": "internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    log_event("starting_server", port=port)
    app.run(host="0.0.0.0", port=port, debug=False)
