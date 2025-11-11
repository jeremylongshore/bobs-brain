#!/usr/bin/env python3
"""
Minimal test case to reproduce stream_query() hanging issue.
Tests Agent Engine directly without Cloud Function context.
"""
import os
import sys
from datetime import datetime

# Set up GCP credentials and project
os.environ["GOOGLE_CLOUD_PROJECT"] = "bobs-brain"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

print(f"[{datetime.now().isoformat()}] Starting minimal stream_query test...")
print(f"Project: {os.environ['GOOGLE_CLOUD_PROJECT']}")
print(f"Location: {os.environ['GOOGLE_CLOUD_LOCATION']}")

# Initialize Vertex AI
try:
    import vertexai
    from vertexai.preview import reasoning_engines

    vertexai.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ["GOOGLE_CLOUD_LOCATION"]
    )
    print(f"[{datetime.now().isoformat()}] ✓ Vertex AI initialized")
except Exception as e:
    print(f"[{datetime.now().isoformat()}] ✗ Failed to initialize Vertex AI: {e}")
    sys.exit(1)

# Agent Engine ID from deployment
AGENT_ENGINE_ID = "5828234061910376448"

print(f"\n[{datetime.now().isoformat()}] Getting remote agent: {AGENT_ENGINE_ID}")

try:
    remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)
    print(f"[{datetime.now().isoformat()}] ✓ Got remote agent reference")
except Exception as e:
    print(f"[{datetime.now().isoformat()}] ✗ Failed to get remote agent: {e}")
    sys.exit(1)

# Test query
test_query = "Hello, Bob! This is a minimal test. Please respond with a short greeting."
test_user_id = "test_user_123"
test_session_id = "test_session_456"

print(f"\n[{datetime.now().isoformat()}] Testing stream_query() with:")
print(f"  Query: {test_query}")
print(f"  User ID: {test_user_id}")
print(f"  Session ID: {test_session_id}")
print(f"\n[{datetime.now().isoformat()}] Calling stream_query()...")
print("-" * 80)

try:
    full_response = []
    event_count = 0

    # Call stream_query with timeout monitoring
    for event in remote_agent.stream_query(
        input={
            "message": test_query,
            "user_id": test_user_id,
            "session_id": test_session_id
        }
    ):
        event_count += 1
        print(f"[{datetime.now().isoformat()}] Event {event_count}: {event}")

        # Extract text from event
        if isinstance(event, dict):
            if "output" in event:
                full_response.append(str(event["output"]))
            elif "text" in event:
                full_response.append(event["text"])
            else:
                full_response.append(str(event))

    print("-" * 80)
    print(f"\n[{datetime.now().isoformat()}] ✓ Stream completed")
    print(f"  Total events: {event_count}")

    response_text = "".join(full_response) if full_response else "No response"
    print(f"\n[{datetime.now().isoformat()}] Final response:")
    print(response_text)

    print(f"\n[{datetime.now().isoformat()}] ✓ TEST PASSED - Agent responded successfully")
    sys.exit(0)

except KeyboardInterrupt:
    print(f"\n[{datetime.now().isoformat()}] ✗ TEST INTERRUPTED - User cancelled")
    sys.exit(2)

except Exception as e:
    print(f"\n[{datetime.now().isoformat()}] ✗ TEST FAILED - Exception occurred:")
    print(f"  Type: {type(e).__name__}")
    print(f"  Message: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
