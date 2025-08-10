#!/usr/bin/env python3
"""Test Bob's Slack connection"""

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Set tokens
token = os.environ.get('SLACK_BOT_TOKEN', '')

client = WebClient(token=token)

try:
    # Test auth
    response = client.auth_test()
    print("✅ Bot authenticated successfully!")
    print(f"Bot Name: {response['user']}")
    print(f"Bot ID: {response['user_id']}")
    print(f"Team: {response['team']}")
    print(f"URL: {response['url']}")
    
    # List channels
    print("\n📢 Channels Bob can see:")
    channels = client.conversations_list(types="public_channel,private_channel,im,mpim")
    for channel in channels['channels'][:5]:
        print(f"  - {channel['name'] if 'name' in channel else 'DM'} (ID: {channel['id']})")
    
    # Test posting
    print("\n📮 Testing message post...")
    result = client.chat_postMessage(
        channel="@jeremylongshore",  # Try DMing you
        text="🤖 Bob Ultimate test message - I'm alive and can send messages!"
    )
    print("✅ Test message sent!")
    
except SlackApiError as e:
    print(f"❌ Slack API Error: {e.response['error']}")
    print(f"Details: {e.response}")
except Exception as e:
    print(f"❌ Error: {e}")