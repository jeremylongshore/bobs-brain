#!/usr/bin/env python3
"""Quick Bob diagnostic"""

import requests
import json
import time

print("=" * 60)
print("BOB'S BRAIN QUICK DIAGNOSTIC")
print("=" * 60)

# 1. Check health
print("\n1. HEALTH CHECK:")
try:
    r = requests.get("https://bobs-brain-sytrh5wz5q-uc.a.run.app/health", timeout=10)
    health = r.json()
    print(f"  Status: {health.get('status')}")
    print(f"  Model: {health.get('model')}")
    print(f"  Slack: {health.get('components', {}).get('slack')}")
    print(f"  Gemini: {health.get('components', {}).get('gemini')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 2. Test chat
print("\n2. CHAT TEST:")
try:
    r = requests.post(
        "https://bobs-brain-sytrh5wz5q-uc.a.run.app/chat",
        json={"message": "What is 2+2?", "user": "test"},
        timeout=30
    )
    result = r.json()
    response = result.get('response', 'No response')
    print(f"  Response: {response[:100]}...")
    print(f"  Model used: {result.get('model')}")
except Exception as e:
    print(f"  ERROR: {e}")

# 3. Test Slack webhook
print("\n3. SLACK WEBHOOK TEST:")
try:
    r = requests.post(
        "https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events",
        json={"type": "url_verification", "challenge": "test123"},
        timeout=10
    )
    print(f"  Status: {r.status_code}")
    print(f"  Response: {r.json()}")
except Exception as e:
    print(f"  ERROR: {e}")

# 4. Test Slack event
print("\n4. SLACK EVENT TEST:")
event = {
    "type": "event_callback",
    "event": {
        "type": "message",
        "text": "Hey Bob, are you there?",
        "user": "test_user",
        "channel": "C12345",
        "ts": str(time.time())
    }
}
try:
    r = requests.post(
        "https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events",
        json=event,
        timeout=10
    )
    print(f"  Status: {r.status_code}")
    print(f"  Response: {r.text[:100]}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("If Bob isn't responding in Slack:")
print("1. Check Slack app Event Subscriptions URL is set to:")
print("   https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events")
print("2. Ensure bot is invited to channels")
print("3. Check tokens are correctly set in Cloud Run env vars")
print("=" * 60)