#!/usr/bin/env python3
"""
Bob's Brain - SOLID FOUNDATION
Just the essentials, done RIGHT
"""

import os
import logging
from typing import Dict, List

# Core dependencies only
from slack_bolt import App
from slack_sdk import WebClient
import chromadb
import vertexai
from vertexai.generative_models import GenerativeModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "") 
GCP_PROJECT = "bobs-house-ai"

# Check if we have real tokens
if not SLACK_BOT_TOKEN or "PLACEHOLDER" in SLACK_BOT_TOKEN:
    logger.error("❌ NO SLACK TOKEN - Bob needs real Slack credentials")
    logger.error("Go to: https://api.slack.com/apps")
    logger.error("Get your Bot User OAuth Token (xoxb-...)")
    # Exit gracefully
    exit(1)

# Initialize Slack - BASIC
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)
logger.info("✅ Slack connected")

# Initialize Vertex AI - BASIC  
vertexai.init(project=GCP_PROJECT, location="us-central1")
model = GenerativeModel("gemini-2.0-flash-exp")
logger.info("✅ Vertex AI connected")

# Initialize ChromaDB - BASIC
chroma_client = chromadb.PersistentClient(path="/home/jeremylongshore/bobs-brain/chroma_data")
try:
    collection = chroma_client.get_collection("bob_knowledge")
except:
    collection = chroma_client.create_collection("bob_knowledge")
logger.info(f"✅ ChromaDB ready with {collection.count()} docs")

# SIMPLE message handler
@app.event("app_mention")
def handle_mention(event, say):
    """When someone mentions Bob"""
    text = event['text']
    user = event['user']
    
    # Remove the @Bob part
    question = text.split('>', 1)[-1].strip() if '>' in text else text
    
    # Search knowledge base
    if collection.count() > 0:
        results = collection.query(query_texts=[question], n_results=3)
        context = "\n".join(results['documents'][0]) if results['documents'] else ""
    else:
        context = ""
    
    # Ask Vertex AI
    prompt = f"""You are Bob, a helpful assistant.
Context: {context[:500] if context else 'No context'}
Question: {question}
Answer:"""
    
    try:
        response = model.generate_content(prompt)
        answer = response.text
    except:
        answer = "I'm having trouble thinking right now. Try again?"
    
    # Reply in thread
    say(answer, thread_ts=event.get('ts'))

@app.event("message")
def handle_dm(event, say):
    """When someone DMs Bob"""
    # Only respond to DMs, not channel messages
    if event.get('channel_type') == 'im' and 'bot_id' not in event:
        text = event['text']
        
        # Ask Vertex AI directly (no context for DMs)
        prompt = f"You are Bob, a helpful assistant. User asks: {text}"
        
        try:
            response = model.generate_content(prompt)
            answer = response.text
        except:
            answer = "I'm having trouble right now. Try again?"
        
        say(answer)

# Start Bob
if __name__ == "__main__":
    logger.info("🤖 BOB IS STARTING...")
    
    # Use Socket Mode if token exists, otherwise web server
    if os.environ.get("SLACK_APP_TOKEN"):
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        logger.info("📡 Starting in Socket Mode (development)")
        handler.start()
    else:
        port = int(os.environ.get("PORT", 3000))
        logger.info(f"🌐 Starting web server on port {port}")
        app.start(port=port)