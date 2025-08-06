#!/usr/bin/env python3
"""Simple Bob that works - no complex debugging"""

from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
import chromadb

# Initialize components
slack_client = WebClient(token=SLACK_BOT_TOKEN)
chroma_client = chromadb.PersistentClient(path='/home/jeremylongshore/.bob_brain/chroma')
collection = chroma_client.get_collection('bob_knowledge')

def simple_response(text):
    """Generate simple response using RAG system"""
    # For simple greetings, just respond simply
    if any(word in text.lower() for word in ["hello", "hi", "hey", "there"]):
        return "Yes, I'm here!"

    # Search knowledge base for relevant information
    results = collection.query(query_texts=[text], n_results=3)

    if results['documents'] and results['documents'][0]:
        # Use relevant knowledge to respond
        relevant_info = results['documents'][0][0]
        return relevant_info[:300]

    # Simple default response
    return "I'm here to help. What do you need?"

def handle_message(client, request):
    if request.type == "events_api":
        event = request.payload.get("event", {})
        if event.get("type") == "message" and event.get("text") and not event.get("bot_id"):
            user_text = event.get("text", "")
            channel = event.get("channel")

            print(f"📝 Got message: {user_text}")

            try:
                response = simple_response(user_text)
                slack_client.chat_postMessage(channel=channel, text=response)
                print(f"✅ Replied: {response[:50]}...")
            except Exception as e:
                slack_client.chat_postMessage(channel=channel, text=f"Error: {e}")

    request.ack()

print("🚀 Starting Simple Bob...")
socket_client = SocketModeClient(app_token=SLACK_APP_TOKEN)
socket_client.socket_mode_request_listeners.append(handle_message)
socket_client.connect()
print("✅ Simple Bob is ready!")

# Keep running
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("👋 Simple Bob stopping...")
