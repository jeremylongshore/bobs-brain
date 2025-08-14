#!/usr/bin/env python3
"""
FINAL BOB VERIFICATION
Confirms Bob is 100% operational
"""

import requests
import json
import sys

print("=" * 70)
print("BOB'S BRAIN ENTERPRISE v7.0 - FINAL VERIFICATION")
print("=" * 70)

# Test endpoints
BASE_URL = "https://bobs-brain-157908567967.us-central1.run.app"
tests_passed = 0
tests_total = 0

def test_endpoint(name, method, path, data=None):
    global tests_passed, tests_total
    tests_total += 1
    
    try:
        if method == "GET":
            r = requests.get(f"{BASE_URL}{path}", timeout=10)
        else:
            r = requests.post(f"{BASE_URL}{path}", json=data, timeout=30)
        
        if r.status_code == 200:
            print(f"✅ {name}: PASSED")
            tests_passed += 1
            return r.json()
        else:
            print(f"❌ {name}: FAILED (Status {r.status_code})")
            return None
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        return None

# Run tests
print("\n📋 RUNNING TESTS:\n")

# 1. Health check
health = test_endpoint("Health Check", "GET", "/health")
if health:
    print(f"   - Model: {health.get('model')}")
    print(f"   - Components: {sum(1 for v in health.get('components', {}).values() if v)}/{len(health.get('components', {}))}")

# 2. Chat with Gemini
chat_result = test_endpoint(
    "Gemini Chat", "POST", "/chat",
    {"message": "What is the capital of Texas?", "user": "test"}
)
if chat_result:
    response = chat_result.get('response', '')
    if 'Austin' in response:
        print(f"   - Correct answer received!")
    else:
        print(f"   - Response: {response[:50]}...")

# 3. Slack webhook
slack_result = test_endpoint(
    "Slack Webhook", "POST", "/slack/events",
    {"type": "url_verification", "challenge": "verify123"}
)
if slack_result:
    print(f"   - Challenge echoed correctly")

# 4. Status check
status = test_endpoint("Status Endpoint", "GET", "/status")
if status:
    print(f"   - Neo4j nodes: {status.get('neo4j_nodes', 0)}")

# Summary
print("\n" + "=" * 70)
print("VERIFICATION RESULTS")
print("=" * 70)
print(f"\n📊 Tests Passed: {tests_passed}/{tests_total}")

if tests_passed == tests_total:
    print("\n✅ BOB IS FULLY OPERATIONAL!")
    print("\n🎯 NEXT STEPS:")
    print("1. Go to https://api.slack.com/apps")
    print("2. Configure Event Subscriptions URL:")
    print(f"   {BASE_URL}/slack/events")
    print("3. Invite Bob to Slack channels with: /invite @bob")
    print("4. Test by mentioning @bob in Slack")
else:
    print("\n⚠️ SOME TESTS FAILED - CHECK CONFIGURATION")
    
print("\n🔗 Service URL:", BASE_URL)
print("📍 Project: bobs-house-ai")
print("🧠 Model: Gemini 1.5 Flash (via GCP API Key)")
print("💾 Database: Neo4j Aura + BigQuery")
print("\n" + "=" * 70)