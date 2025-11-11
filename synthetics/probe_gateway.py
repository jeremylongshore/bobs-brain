#!/usr/bin/env python3
"""
Synthetic probe for Bob's Brain gateway.

Runs health check and basic invoke test to validate gateway availability.
Exits with code 0 on success, code 2 on failure.
"""
import os
import sys
import json
import time
import requests

BASE_URL = os.environ.get("GATEWAY_URL")
HEALTH_TIMEOUT = int(os.environ.get("HEALTH_TIMEOUT_S", "5"))
INVOKE_TIMEOUT = int(os.environ.get("INVOKE_TIMEOUT_S", "15"))


def fail(msg, extra=None):
    """Print failure JSON and exit with code 2."""
    result = {
        "ok": False,
        "error": msg,
        "extra": extra or {},
        "timestamp": time.time()
    }
    print(json.dumps(result))
    sys.exit(2)


def success(checks):
    """Print success JSON and exit with code 0."""
    result = {
        "ok": True,
        "checks": checks,
        "timestamp": time.time()
    }
    print(json.dumps(result))
    sys.exit(0)


def main():
    if not BASE_URL:
        fail("GATEWAY_URL environment variable not set")

    checks = []

    # Check 1: Health endpoint
    try:
        start = time.time()
        r = requests.get(f"{BASE_URL}/_health", timeout=HEALTH_TIMEOUT)
        latency_ms = int((time.time() - start) * 1000)

        if r.status_code != 200:
            fail(
                "Health endpoint returned non-200",
                {"status": r.status_code, "latency_ms": latency_ms}
            )

        health_data = r.json()
        if health_data.get("status") != "ok":
            fail(
                "Health endpoint status not 'ok'",
                {"health": health_data, "latency_ms": latency_ms}
            )

        checks.append({
            "name": "health",
            "status": "ok",
            "latency_ms": latency_ms,
            "mode": health_data.get("mode"),
            "engine": health_data.get("engine", "").split("/")[-1] if health_data.get("engine") else None
        })

    except requests.Timeout:
        fail(
            f"Health endpoint timeout (>{HEALTH_TIMEOUT}s)",
            {"timeout_s": HEALTH_TIMEOUT}
        )
    except Exception as e:
        fail(
            "Health endpoint request failed",
            {"error": str(e)}
        )

    # Check 2: Invoke endpoint (basic ping)
    try:
        start = time.time()
        r = requests.post(
            f"{BASE_URL}/invoke",
            json={"text": "ping"},
            headers={"Content-Type": "application/json"},
            timeout=INVOKE_TIMEOUT
        )
        latency_ms = int((time.time() - start) * 1000)

        if r.status_code != 200:
            fail(
                "Invoke endpoint returned non-200",
                {"status": r.status_code, "latency_ms": latency_ms}
            )

        # Don't validate response content - just check it returns JSON
        try:
            invoke_data = r.json()
        except:
            fail(
                "Invoke endpoint returned invalid JSON",
                {"latency_ms": latency_ms}
            )

        checks.append({
            "name": "invoke",
            "status": "ok",
            "latency_ms": latency_ms
        })

    except requests.Timeout:
        fail(
            f"Invoke endpoint timeout (>{INVOKE_TIMEOUT}s)",
            {"timeout_s": INVOKE_TIMEOUT}
        )
    except Exception as e:
        fail(
            "Invoke endpoint request failed",
            {"error": str(e)}
        )

    # Check 3: Card endpoint (A2A discovery)
    try:
        start = time.time()
        r = requests.get(f"{BASE_URL}/card", timeout=HEALTH_TIMEOUT)
        latency_ms = int((time.time() - start) * 1000)

        if r.status_code != 200:
            fail(
                "Card endpoint returned non-200",
                {"status": r.status_code, "latency_ms": latency_ms}
            )

        card_data = r.json()
        if "name" not in card_data:
            fail(
                "Card endpoint missing 'name' field",
                {"card": card_data, "latency_ms": latency_ms}
            )

        checks.append({
            "name": "card",
            "status": "ok",
            "latency_ms": latency_ms,
            "agent_name": card_data.get("name")
        })

    except requests.Timeout:
        fail(
            f"Card endpoint timeout (>{HEALTH_TIMEOUT}s)",
            {"timeout_s": HEALTH_TIMEOUT}
        )
    except Exception as e:
        fail(
            "Card endpoint request failed",
            {"error": str(e)}
        )

    # All checks passed
    success(checks)


if __name__ == "__main__":
    main()
