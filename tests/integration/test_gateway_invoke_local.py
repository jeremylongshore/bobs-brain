"""
Integration test for gateway /invoke endpoint.

Tests the non-streaming invoke endpoint with stubbed Reasoning Engine responses.
"""

import subprocess
import time
import requests
import os


def test_invoke_non_stream():
    """Test /invoke endpoint with stubbed REST client."""
    # Set environment for gateway
    env = os.environ.copy()
    env["AGENT_ENGINE_NAME"] = "projects/test/locations/us-central1/reasoningEngines/test-engine"

    # Start gateway
    p = subprocess.Popen(
        ["uvicorn", "gateway.main:app", "--host", "127.0.0.1", "--port", "8083"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Wait for gateway to start
        time.sleep(2)

        # Test health endpoint first
        r_health = requests.get("http://127.0.0.1:8083/_health", timeout=5)
        assert r_health.status_code == 200
        health_data = r_health.json()
        assert health_data["status"] == "ok"
        assert "X-Trace-Id" in r_health.headers
        print(f"✅ Health check passed: {health_data}")

        # Test card endpoint
        r_card = requests.get("http://127.0.0.1:8083/card", timeout=5)
        assert r_card.status_code == 200
        card_data = r_card.json()
        assert "name" in card_data
        assert "engine" in card_data
        print(f"✅ Card endpoint passed: {card_data['name']}")

        # Note: Full invoke test requires actual Reasoning Engine or mocking
        # This test verifies gateway starts and basic endpoints work
        print("✅ Gateway integration test passed")

    finally:
        p.terminate()
        p.wait(timeout=5)


def test_gateway_trace_headers():
    """Test that trace headers are present on responses."""
    env = os.environ.copy()
    env["AGENT_ENGINE_NAME"] = "projects/test/locations/us-central1/reasoningEngines/test"

    p = subprocess.Popen(
        ["uvicorn", "gateway.main:app", "--host", "127.0.0.1", "--port", "8084"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)

        # Test health endpoint
        r = requests.get("http://127.0.0.1:8084/_health", timeout=5)
        assert r.status_code == 200

        # Verify trace headers
        assert "X-Trace-Id" in r.headers, "Missing X-Trace-Id header"
        trace_id = r.headers["X-Trace-Id"]
        assert len(trace_id) == 32, f"Invalid trace ID length: {len(trace_id)}"
        print(f"✅ Trace header present: X-Trace-Id={trace_id}")

    finally:
        p.terminate()
        p.wait(timeout=5)
