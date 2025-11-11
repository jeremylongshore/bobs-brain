"""Integration tests for ADK API Server."""
import subprocess
import time
import requests
import os
import signal
import sys

BASE = "http://127.0.0.1:8000"


def test_api_server_runs_and_lists_apps():
    """Test that the ADK API server starts and lists apps."""
    # Start ADK API server using python -m google.adk.cli
    p = subprocess.Popen(
        [sys.executable, "-m", "google.adk.cli", "api_server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Give server time to start
        time.sleep(3)

        # Test /list-apps endpoint
        r = requests.get(f"{BASE}/list-apps", timeout=5)
        r.raise_for_status()

        # Should return a list of apps
        apps = r.json()
        assert isinstance(apps, list), "Expected list of apps"

    finally:
        # Clean up: kill server
        os.kill(p.pid, signal.SIGTERM)
        p.wait(timeout=5)
