#!/usr/bin/env python3
"""Test calling agent directly without :query"""
import google.auth
from google.auth.transport.requests import Request
import requests
import json

credentials, project = google.auth.default()
credentials.refresh(Request())

AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"
REGION = "us-central1"

headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}

# Test calling the agent's default endpoint (no :query)
base_url = f"https://{REGION}-aiplatform.googleapis.com/v1/{AGENT_ENGINE_ID}"

# Try different approaches
tests = [
    (f"{base_url}", {"input": {"query": "What is the hustle project?"}}),
    (f"{base_url}:stream", {"input": {"query": "What is the hustle project?"}}),
]

for url, payload in tests:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:700]}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS!")
            break
    except Exception as e:
        print(f"Error: {e}")

