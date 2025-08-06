#!/usr/bin/env python3
"""Bob Extended Brain - Cloud Run Version"""

import os
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient

# Environment variables for cloud
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Initialize components (without ChromaDB for now)
slack_client = WebClient(token=SLACK_BOT_TOKEN)

def simple_response(text):
    """Generate simple response - cloud version"""
    # For greetings
    if any(word in text.lower() for word in ["hello", "hi", "hey", "there"]):
        return "Yes, I'm here."

    # Default response
    return "I'm working on it."

def handle_message(client, request):
    if request.type == "events_api":
        event = request.payload.get("event", {})
        if event.get("type") == "message" and event.get("text") and not event.get("bot_id"):
            user_text = event.get("text", "")
            channel = event.get("channel")

            print(f"📝 Cloud Bob got message: {user_text}")

            try:
                response = simple_response(user_text)
                slack_client.chat_postMessage(channel=channel, text=response)
                print(f"✅ Cloud Bob replied: {response[:50]}...")
            except Exception as e:
                slack_client.chat_postMessage(channel=channel, text=f"Cloud error: {e}")

    request.ack()

# Start Cloud Bob
print("🌩️ Starting Bob Extended Brain on Cloud Run...")
socket_client = SocketModeClient(app_token=SLACK_APP_TOKEN)
socket_client.socket_mode_request_listeners.append(handle_message)
socket_client.connect()
print("✅ Cloud Bob is ready!")

# Keep running
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("👋 Cloud Bob stopping...")
