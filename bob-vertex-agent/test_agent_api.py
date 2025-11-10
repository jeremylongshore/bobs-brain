#!/usr/bin/env python3
"""Test script to find correct Agent Engine API format"""
import google.auth
from google.auth.transport.requests import Request
import requests
import json

# Get credentials
credentials, project = google.auth.default()
credentials.refresh(Request())

AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"
REGION = "us-central1"

headers = {
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json"
}

# Test different payload formats
payloads = [
    {"input": "What is the hustle project?"},
    {"query": "What is the hustle project?"},
    {"input": {"query": "What is the hustle project?"}},
    {"input": {"text": "What is the hustle project?"}},
]

for i, payload in enumerate(payloads, 1):
    print(f"\n{'='*60}")
    print(f"Test {i}: {json.dumps(payload, indent=2)}")
    print(f"{'='*60}")
    
    url = f"https://{REGION}-aiplatform.googleapis.com/v1/{AGENT_ENGINE_ID}:query"
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! This format works:")
            print(json.dumps(payload, indent=2))
            break
    except Exception as e:
        print(f"Error: {e}")

