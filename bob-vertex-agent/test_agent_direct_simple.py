#!/usr/bin/env python3
"""
Simple direct test of Agent Engine with minimal dependencies.
"""
import json
import google.auth
from google.auth.transport.requests import Request
import requests

# Get credentials
credentials, project = google.auth.default()
credentials.refresh(Request())

AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"
url = f"https://us-central1-aiplatform.googleapis.com/v1/{AGENT_ENGINE_ID}:streamQuery"

headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}

payload = {
    "input": {
        "message": "Hello! Please respond with just 'Hi' - nothing more.",
        "user_id": "test_user_direct"
    }
}

print(f"Testing Agent Engine at: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\nMaking request...")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=60, stream=True)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("\n✓ SUCCESS - Streaming response:")
        print("-" * 80)

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    print(f"Event: {json.dumps(data, indent=2)}")

                    if "content" in data and "parts" in data["content"]:
                        for part in data["content"]["parts"]:
                            if "text" in part:
                                print(f"\n>>> RESPONSE TEXT: {part['text']}")
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
    else:
        print(f"\n✗ ERROR: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.SSLError as e:
    print(f"\n✗ SSL ERROR: {e}")
    print("\nThis is likely a network/infrastructure issue, not a code issue.")
except requests.exceptions.Timeout as e:
    print(f"\n✗ TIMEOUT: {e}")
except Exception as e:
    print(f"\n✗ UNEXPECTED ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
