#!/usr/bin/env python3
"""Quick test of Bob in Slack"""

import os
import time

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "xoxb-YOUR-TOKEN-HERE")
CHANNEL = "C099A4N4PSN"  # #bobs-brain channel

# Initialize client
slack = WebClient(token=SLACK_BOT_TOKEN)

# Test messages
test_messages = [
    "Hello Bob, are you working?",
    "What's a fair price for brake replacement?",
    "How much data do you have access to?",
]

print("🤖 Testing Bob in #bobs-brain channel...")
print("=" * 50)

for msg in test_messages:
    try:
        print(f"\n📤 Sending: {msg}")

        # Send message
        result = slack.chat_postMessage(channel=CHANNEL, text=msg)

        if result["ok"]:
            print(f"✅ Message sent successfully")

            # Wait a bit for Bob to respond
            time.sleep(3)

            # Get recent messages
            history = slack.conversations_history(channel=CHANNEL, limit=5)

            # Look for Bob's response
            for message in history["messages"]:
                if message.get("bot_id") and message.get("text"):
                    print(f"🤖 Bob replied: {message['text'][:100]}...")
                    break
        else:
            print(f"❌ Failed to send message")

    except SlackApiError as e:
        print(f"❌ Error: {e.response['error']}")

    time.sleep(2)  # Don't spam

print("\n" + "=" * 50)
print("✅ Test complete! Check #bobs-brain channel in Slack")
