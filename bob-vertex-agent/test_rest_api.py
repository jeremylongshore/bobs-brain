#!/usr/bin/env python3
"""
Test Bob's Brain Agent Engine via REST API (streamQuery).

This demonstrates the CORRECT way to query ADK-deployed agents.
"""

import json
import google.auth
from google.auth.transport.requests import Request
import requests

def test_agent_rest_api():
    """Test Agent Engine via REST API."""

    # Get credentials
    credentials, project_id = google.auth.default()
    credentials.refresh(Request())

    # Agent Engine REST endpoint
    url = (
        "https://us-central1-aiplatform.googleapis.com/v1/"
        "projects/205354194989/locations/us-central1/"
        "reasoningEngines/5828234061910376448:streamQuery"
    )

    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }

    # Test payload
    payload = {
        "message": "Hello, this is a health check test. Please respond with 'OK' to confirm you're working.",
        "user_id": "test_user_rest_api"
    }

    print(f"\n{'='*80}")
    print("TESTING AGENT ENGINE VIA REST API")
    print(f"{'='*80}\n")

    print(f"Endpoint: {url}")
    print(f"User: {payload['user_id']}")
    print(f"Message: {payload['message']}")
    print(f"\n{'='*80}")
    print("RESPONSE:")
    print(f"{'='*80}\n")

    # Make request (streaming)
    response = requests.post(url, json=payload, headers=headers, stream=True)

    if response.status_code != 200:
        print(f"❌ Error: HTTP {response.status_code}")
        print(response.text)
        return

    # Collect streamed response
    full_response = ""

    for line in response.iter_lines():
        if line:
            # Server-Sent Events format: "data: {...}"
            if line.startswith(b"data: "):
                try:
                    data_str = line[6:].decode('utf-8')
                    data = json.loads(data_str)

                    # Print raw event
                    print(f"[Event] {json.dumps(data, indent=2)}")

                    # Extract content
                    if isinstance(data, dict):
                        if "content" in data:
                            full_response += data["content"]
                        elif "output" in data:
                            full_response += str(data["output"])
                        elif "text" in data:
                            full_response += data["text"]
                    elif isinstance(data, str):
                        full_response += data

                except json.JSONDecodeError as e:
                    print(f"[Raw] {line}")
            else:
                # Non-data line
                print(f"[Line] {line}")

    print(f"\n{'='*80}")
    print("FULL RESPONSE:")
    print(f"{'='*80}\n")
    print(full_response or "[No content extracted]")
    print()

    if full_response:
        print("✅ REST API test SUCCESSFUL")
    else:
        print("⚠️  REST API test completed but no content extracted")
        print("   This may be due to unexpected event format")

if __name__ == "__main__":
    test_agent_rest_api()
