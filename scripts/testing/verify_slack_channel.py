#!/usr/bin/env python3
"""Verify Bob's Slack channel is active"""

from slack_sdk import WebClient
import time
import json
import os

token = os.environ.get("SLACK_BOT_TOKEN", "[REDACTED]")
client = WebClient(token=token)

print("=" * 60)
print("VERIFYING BOB'S SLACK CHANNEL STATUS")
print("=" * 60)

try:
    # 1. Check bot status
    auth = client.auth_test()
    print(f"\n✅ Bot Connected: {auth['user']} (ID: {auth['user_id']})")
    
    # 2. Get Bob's presence
    try:
        presence = client.users_getPresence(user=auth['user_id'])
        print(f"📊 Bot Presence: {presence['presence']} (Channel {'ACTIVE' if presence['presence'] == 'active' else 'NOT ACTIVE'})")
    except:
        print("❌ Could not get bot presence")
    
    # 3. Find Bob's Brain channel
    channels = client.conversations_list()
    bob_channel = None
    
    for channel in channels['channels']:
        if channel['name'] == 'bobs-brain':
            bob_channel = channel
            print(f"\n📍 Channel: #{channel['name']}")
            print(f"   ID: {channel['id']}")
            print(f"   Members: {channel['num_members']}")
            
            # Check if bot is member
            members = client.conversations_members(channel=channel['id'])
            if auth['user_id'] in members['members']:
                print("   ✅ Bot IS in channel")
            else:
                print("   ❌ Bot NOT in channel")
            
            # Get channel info
            info = client.conversations_info(channel=channel['id'])
            if info['channel'].get('is_member'):
                print("   ✅ Bot is active member")
            
            # Check recent messages
            history = client.conversations_history(channel=channel['id'], limit=5)
            print(f"\n📝 Recent messages: {len(history['messages'])}")
            
            for msg in history['messages'][:3]:
                user = msg.get('user', 'unknown')
                text = msg.get('text', '')[:50]
                print(f"   - {user}: {text}...")
            
            break
    
    # 4. Test sending a message
    print("\n🧪 SENDING TEST MESSAGE...")
    try:
        result = client.chat_postMessage(
            channel="C099A4N4PSN",  # bobs-brain channel ID
            text=f"🤖 Bob Brain Status Check - {time.strftime('%H:%M:%S')}\n" +
                 "If you see this, Bob CAN send messages.\n" +
                 "Now mention @bobs_brain to test receiving!"
        )
        print("✅ Message sent successfully!")
        print(f"   Timestamp: {result['ts']}")
    except Exception as e:
        print(f"❌ Failed to send: {e}")
    
    # 5. Check if Event Subscriptions are working
    print("\n🔌 EVENT SUBSCRIPTIONS:")
    print("   If Bob doesn't respond to mentions:")
    print("   1. Go to: https://api.slack.com/apps")
    print("   2. Select 'bobs_brain' app")
    print("   3. Click 'Event Subscriptions'")
    print("   4. Request URL should be:")
    print("      https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events")
    print("   5. Should show 'Verified' ✓")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)