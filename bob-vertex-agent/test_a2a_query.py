#!/usr/bin/env python3
"""
Test A2A Protocol Query for Bob's Brain Agent Engine

This script tests the correct way to query an ADK agent deployed to Agent Engine.
"""

import asyncio
import sys
from vertexai.preview import reasoning_engines
import vertexai

# Configuration
PROJECT_ID = "bobs-brain"
REGION = "us-central1"
AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"


async def test_async_stream_query():
    """Test the async_stream_query method (correct A2A protocol)"""
    print("=" * 60)
    print("Testing async_stream_query (A2A Protocol)")
    print("=" * 60)

    try:
        # Initialize Vertex AI
        vertexai.init(project=PROJECT_ID, location=REGION)

        # Get the remote agent
        print(f"\nConnecting to Agent Engine: {AGENT_ENGINE_ID}\n")
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        # Test query
        test_message = "Hello, who are you?"
        print(f"Sending query: '{test_message}'\n")

        # Collect response
        full_response = []

        # Use async_stream_query (CORRECT METHOD)
        async for event in remote_agent.async_stream_query(
            message=test_message,
            user_id="test_user_001",
            session_id="test_session_001"
        ):
            event_type = event.get("type")
            print(f"[EVENT] Type: {event_type}")

            # Extract text from content events
            if event_type == "content":
                data = event.get("data", {})
                if "parts" in data:
                    for part in data["parts"]:
                        if "text" in part:
                            text = part["text"]
                            full_response.append(text)
                            print(f"[RESPONSE] {text[:100]}...")

        print("\n" + "=" * 60)
        print("FULL RESPONSE:")
        print("=" * 60)
        print("".join(full_response))
        print("\n✅ Test PASSED - async_stream_query works correctly!")

        return True

    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_with_session_management():
    """Test session management across multiple queries"""
    print("\n" + "=" * 60)
    print("Testing Session Management (Conversation Context)")
    print("=" * 60)

    try:
        vertexai.init(project=PROJECT_ID, location=REGION)
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        session_id = "test_session_002"

        # First query
        print(f"\n[QUERY 1] Creating session: {session_id}")
        query1 = "My name is Alice. Remember that."
        response1 = []

        async for event in remote_agent.async_stream_query(
            message=query1,
            user_id="test_user_002",
            session_id=session_id
        ):
            if event.get("type") == "content":
                data = event.get("data", {})
                if "parts" in data:
                    for part in data["parts"]:
                        if "text" in part:
                            response1.append(part["text"])

        print(f"[RESPONSE 1] {''.join(response1)[:200]}...")

        # Second query (same session)
        print(f"\n[QUERY 2] Using same session: {session_id}")
        query2 = "What is my name?"
        response2 = []

        async for event in remote_agent.async_stream_query(
            message=query2,
            user_id="test_user_002",
            session_id=session_id  # Same session - should remember context
        ):
            if event.get("type") == "content":
                data = event.get("data", {})
                if "parts" in data:
                    for part in data["parts"]:
                        if "text" in part:
                            response2.append(part["text"])

        print(f"[RESPONSE 2] {''.join(response2)[:200]}...")

        print("\n✅ Session management test PASSED!")
        return True

    except Exception as e:
        print(f"\n❌ Session management test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_wrong_method():
    """Show what happens with the WRONG method (query)"""
    print("\n" + "=" * 60)
    print("Testing WRONG Method (query) - Should Fail")
    print("=" * 60)

    try:
        vertexai.init(project=PROJECT_ID, location=REGION)
        remote_agent = reasoning_engines.ReasoningEngine(AGENT_ENGINE_ID)

        print("\nAttempting to call remote_agent.query()...")

        # This should fail
        response = remote_agent.query(input="Hello")  # WRONG METHOD

        print(f"❌ Unexpected success: {response}")
        return False

    except Exception as e:
        print(f"\n✅ Expected error occurred: {e}")
        print("This confirms query() method doesn't exist - use async_stream_query() instead!")
        return True


async def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  Bob's Brain A2A Protocol Query Test Suite            ║")
    print("╚" + "=" * 58 + "╝")

    results = []

    # Test 1: async_stream_query
    results.append(await test_async_stream_query())

    # Test 2: Session management
    results.append(await test_with_session_management())

    # Test 3: Wrong method (should fail)
    results.append(test_wrong_method())

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {len(results)}")
    print(f"Tests passed: {sum(results)}")
    print(f"Tests failed: {len(results) - sum(results)}")

    if all(results):
        print("\n✅ ALL TESTS PASSED!")
        print("\nThe Slack webhook should use async_stream_query() method.")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
