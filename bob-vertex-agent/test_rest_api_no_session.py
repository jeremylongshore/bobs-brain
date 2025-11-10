#!/usr/bin/env python3
"""
Test REST API method WITHOUT session_id.
"""
import google.auth
from google.auth.transport.requests import Request
import requests
import json

# Get credentials
credentials, project = google.auth.default()
credentials.refresh(Request())

FULL_AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"

print("Testing REST API WITHOUT session_id...")
print("-" * 80)

# Build URL
url = f"https://us-central1-aiplatform.googleapis.com/v1/{FULL_AGENT_ENGINE_ID}:streamQuery"

# Headers
headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}

# TEST 1: Without session_id
print("\n[TEST 1] REST API without session_id...")
payload1 = {
    "input": {
        "message": "Hello Bob! Respond with a short greeting.",
        "user_id": "test_user_123"
        # NO session_id
    }
}

print(f"URL: {url}")
print(f"Payload: {json.dumps(payload1, indent=2)}")
print()

response = requests.post(url, json=payload1, headers=headers, timeout=30, stream=True)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print("\n✓ Request successful!")
    print("\nStreaming response:")
    print("-" * 40)

    full_response = []
    for line in response.iter_lines():
        if line:
            print(f"Line: {line[:200]}...")
            try:
                data = json.loads(line.decode('utf-8'))
                print(f"Parsed: {data}")
                if "output" in data:
                    full_response.append(str(data["output"]))
                elif "text" in data:
                    full_response.append(data["text"])
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue

    result = "".join(full_response) if full_response else "No response"
    print(f"\n✓ Final response: {result[:500]}")
else:
    print(f"\n✗ Request failed: {response.status_code}")
    print(f"Response: {response.text}")

# TEST 2: With session_id=None (explicit)
print("\n" + "=" * 80)
print("[TEST 2] REST API with session_id=None (explicit)...")
payload2 = {
    "input": {
        "message": "Hello Bob! Respond with a short greeting.",
        "user_id": "test_user_456",
        "session_id": None  # Explicit None
    }
}

print(f"Payload: {json.dumps(payload2, indent=2)}")
print()

response2 = requests.post(url, json=payload2, headers=headers, timeout=30, stream=True)
print(f"Status Code: {response2.status_code}")

if response2.status_code == 200:
    print("\n✓ Request successful with session_id=None!")
else:
    print(f"\n✗ Failed: {response2.status_code} - {response2.text[:200]}")
