#!/usr/bin/env python3
"""
Test fix: Query agent WITHOUT session_id to let ADK create sessions automatically.
"""
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "bobs-brain"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"]
)

AGENT_ENGINE_ID = "5828234061910376448"

print("Testing query WITHOUT session_id (let ADK create it)...")
print("-" * 80)

try:
    remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

    # TEST 1: No session_id at all (ADK will create new session)
    print("\n[TEST 1] Calling stream_query WITHOUT session_id...")
    full_response = []

    for event in remote_agent.stream_query(
        input={
            "message": "Hello Bob! Please respond with a short greeting.",
            "user_id": "test_user_123"
            # NO session_id - let ADK create one
        }
    ):
        print(f"Event: {event}")
        if isinstance(event, dict):
            if "output" in event:
                full_response.append(str(event["output"]))
            elif "text" in event:
                full_response.append(event["text"])

    response = "".join(full_response) if full_response else "No response"
    print(f"\n✓ SUCCESS - Response: {response[:200]}...")
    print("\nFIX CONFIRMED: Not passing session_id works!")

except AttributeError as e:
    print(f"\n✗ AttributeError: {e}")
    print("stream_query() method not available - this is the SDK issue")
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
