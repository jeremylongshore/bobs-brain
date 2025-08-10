#!/usr/bin/env python3
"""Test Slack URL verification for Bob Cloud Run"""

import requests
import json

# Bob's Cloud Run URL
BOB_URL = "https://bobs-brain-157908567967.us-central1.run.app"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BOB_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_url_verification():
    """Test Slack URL verification challenge"""
    print("\nTesting Slack URL verification...")
    
    # This is what Slack sends for URL verification
    payload = {
        "type": "url_verification",
        "challenge": "test_challenge_123456",
        "token": "test_token"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Slack-Request-Timestamp": "1234567890",
        "X-Slack-Signature": "v0=test_signature"
    }
    
    response = requests.post(
        f"{BOB_URL}/slack/events",
        json=payload,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ URL verification endpoint is working!")
        print("Bob should respond with the challenge when Slack verifies the URL")
    else:
        print("❌ URL verification failed - this needs to be fixed")
    
    return response.status_code == 200

def main():
    print("=" * 50)
    print("BOB CLOUD RUN SLACK INTEGRATION TEST")
    print("=" * 50)
    
    # Test health
    health_ok = test_health()
    
    # Test URL verification
    verification_ok = test_url_verification()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"URL Verification: {'✅ READY' if verification_ok else '❌ NOT READY'}")
    
    if not verification_ok:
        print("\n⚠️  IMPORTANT: Bob needs URL verification to work for Slack")
        print("The signature verification might be blocking the test")
        print("But Slack's actual verification should work if configured")
    
    print("\n📝 NEXT STEPS:")
    print("1. Go to https://api.slack.com/apps")
    print("2. Select your Bob app")
    print("3. Go to 'Event Subscriptions'")
    print("4. Set Request URL to:")
    print(f"   {BOB_URL}/slack/events")
    print("5. Wait for 'Verified' status")
    print("6. Save changes")
    print("=" * 50)

if __name__ == "__main__":
    main()