#!/usr/bin/env python3
"""Simple test to verify Bob can send messages"""

import os
from slack_sdk import WebClient

# Set token
token = os.environ.get('SLACK_BOT_TOKEN', '')
client = WebClient(token=token)

try:
    # Post to general channel
    result = client.chat_postMessage(
        channel='#general',
        text='🤖 Bob Ultimate test - Testing 1, 2, 3... Can you see this?'
    )
    print("✅ Test message sent to #general!")
    
    # Post to bobs-brain channel
    result = client.chat_postMessage(
        channel='#bobs-brain',
        text='🤖 Bob is testing his brain! Reply if you see this.'
    )
    print("✅ Test message sent to #bobs-brain!")
    
except Exception as e:
    print(f"❌ Error: {e}")