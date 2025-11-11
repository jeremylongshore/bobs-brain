"""
Integration test for A2A peer registry endpoint.

Tests the /a2a/peers endpoint with file-backed registry.
"""

import subprocess
import time
import requests
import os
import json
import tempfile


def test_peers_endpoint():
    """Test /a2a/peers endpoint with custom registry file."""
    # Create temporary peers registry
    peers = [
        {
            "name": "Eng Agent",
            "version": "1.0.0",
            "skills": ["code_review", "testing"]
        },
        {
            "name": "Data Agent",
            "version": "1.0.0",
            "skills": ["bigquery"]
        }
    ]

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        json.dump(peers, f)
        registry_path = f.name

    try:
        # Set up environment
        env = os.environ.copy()
        env["A2A_REGISTRY_PATH"] = registry_path
        env["AGENT_ENGINE_NAME"] = "projects/test/locations/us-central1/reasoningEngines/test"

        # Start gateway
        p = subprocess.Popen(
            ["uvicorn", "gateway.main:app", "--host", "127.0.0.1", "--port", "8085"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            # Wait for gateway to start
            time.sleep(2)

            # Test /a2a/peers endpoint
            r = requests.get("http://127.0.0.1:8085/a2a/peers", timeout=5)
            assert r.status_code == 200, f"Expected 200, got {r.status_code}"

            data = r.json()
            assert "peers" in data, "Response missing 'peers' key"
            assert "count" in data, "Response missing 'count' key"
            assert data["count"] == 2, f"Expected 2 peers, got {data['count']}"

            # Verify first peer
            assert data["peers"][0]["name"] == "Eng Agent"
            assert "code_review" in data["peers"][0]["skills"]

            # Verify second peer
            assert data["peers"][1]["name"] == "Data Agent"
            assert "bigquery" in data["peers"][1]["skills"]

            # Verify X-Trace-Id header presence
            assert "X-Trace-Id" in r.headers or "x-trace-id" in r.headers, \
                "Missing X-Trace-Id header"

            print(f"✅ A2A registry test passed: {data['count']} peers found")

        finally:
            p.terminate()
            p.wait(timeout=5)

    finally:
        # Clean up temp file
        os.unlink(registry_path)


def test_peers_endpoint_empty_registry():
    """Test /a2a/peers endpoint with non-existent registry (should return empty list)."""
    env = os.environ.copy()
    env["A2A_REGISTRY_PATH"] = "/tmp/nonexistent-registry.json"
    env["AGENT_ENGINE_NAME"] = "projects/test/locations/us-central1/reasoningEngines/test"

    p = subprocess.Popen(
        ["uvicorn", "gateway.main:app", "--host", "127.0.0.1", "--port", "8086"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)

        r = requests.get("http://127.0.0.1:8086/a2a/peers", timeout=5)
        assert r.status_code == 200

        data = r.json()
        assert data["peers"] == [], "Expected empty peers list"
        assert data["count"] == 0, "Expected count of 0"

        print("✅ Empty registry test passed")

    finally:
        p.terminate()
        p.wait(timeout=5)


def test_peers_endpoint_invalid_json():
    """Test /a2a/peers endpoint with invalid JSON (should gracefully return empty list)."""
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        f.write("{invalid json content")
        registry_path = f.name

    try:
        env = os.environ.copy()
        env["A2A_REGISTRY_PATH"] = registry_path
        env["AGENT_ENGINE_NAME"] = "projects/test/locations/us-central1/reasoningEngines/test"

        p = subprocess.Popen(
            ["uvicorn", "gateway.main:app", "--host", "127.0.0.1", "--port", "8087"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            time.sleep(2)

            r = requests.get("http://127.0.0.1:8087/a2a/peers", timeout=5)
            assert r.status_code == 200

            data = r.json()
            # Should gracefully return empty list on JSON error
            assert data["peers"] == [], "Expected empty peers list on invalid JSON"
            assert data["count"] == 0

            print("✅ Invalid JSON test passed (graceful degradation)")

        finally:
            p.terminate()
            p.wait(timeout=5)

    finally:
        os.unlink(registry_path)
