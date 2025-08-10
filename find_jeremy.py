#!/usr/bin/env python3
"""Find Jeremy's DM channel"""

import os
from slack_sdk import WebClient

token = os.environ.get('SLACK_BOT_TOKEN', '')
client = WebClient(token=token)

print("🔍 Looking for Jeremy's DM channel...")

# Get all users
users = client.users_list()
jeremy_id = None

for user in users['members']:
    if 'jeremy' in user.get('real_name', '').lower() or 'jeremy' in user.get('name', '').lower():
        print(f"Found user: {user['real_name']} (@{user['name']}) - ID: {user['id']}")
        jeremy_id = user['id']

if jeremy_id:
    # Open DM channel
    response = client.conversations_open(users=jeremy_id)
    channel_id = response['channel']['id']
    print(f"\n✅ Jeremy's DM channel: {channel_id}")
    
    # Send test message
    client.chat_postMessage(
        channel=channel_id,
        text="🤖 Bob Ultimate is online! I can receive your messages now. Try saying hello!"
    )
    print("✅ Test message sent to Jeremy!")
else:
    print("Could not find Jeremy user")