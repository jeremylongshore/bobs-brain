#!/usr/bin/env python3
"""Test Slack connection directly"""

from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN

print("🧪 Testing Slack connections...")

# Test WebClient
try:
    web_client = WebClient(token=SLACK_BOT_TOKEN)
    response = web_client.auth_test()
    print(f"✅ Web client works: {response['user']} in {response['team']}")
except Exception as e:
    print(f"❌ Web client failed: {e}")

# Test Socket Mode
try:
    socket_client = SocketModeClient(app_token=SLACK_APP_TOKEN)

    def handle_message(client, req):
        print(f"🔥 SOCKET MESSAGE: {req.type}")
        print(f"🔥 PAYLOAD: {req.payload}")
        req.ack()

    socket_client.socket_mode_request_listeners.append(handle_message)
    print("🔌 Connecting socket mode...")
    socket_client.connect()
    print("✅ Socket mode connected! Send a message to Bob...")

    import time
    time.sleep(30)  # Wait 30 seconds for messages

except Exception as e:
    print(f"❌ Socket mode failed: {e}")
    import traceback
    traceback.print_exc()
