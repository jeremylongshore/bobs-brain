#!/usr/bin/env python3
"""
Bob's Brain - Production-Ready Slack Bot
Version 3.0 - Fixed Critical Issues
"""

import os
import sys
import json
import logging
import signal
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import contextmanager
import threading
import time

# Slack SDK
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

# Google Gen AI (NEW SDK - Not deprecated!)
import google.generativeai as genai

# ChromaDB for vector storage
import chromadb
from chromadb.config import Settings

# Environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging with production settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/bob.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Validate required environment variables
REQUIRED_ENV_VARS = {
    'SLACK_BOT_TOKEN': 'Bot User OAuth Token from api.slack.com',
    'SLACK_SIGNING_SECRET': 'Signing Secret from api.slack.com',
    'GOOGLE_API_KEY': 'Google AI API key from makersuite.google.com'
}

missing_vars = []
for var, description in REQUIRED_ENV_VARS.items():
    if not os.environ.get(var) or 'PLACEHOLDER' in os.environ.get(var, ''):
        missing_vars.append(f"  - {var}: {description}")

if missing_vars:
    logger.warning("=" * 60)
    logger.warning("⚠️  BOB IS RUNNING WITHOUT PROPER CONFIGURATION!")
    logger.warning("Missing or placeholder values for:")
    for var in missing_vars:
        logger.warning(var)
    logger.warning("Get these from:")
    logger.warning("  - Slack tokens: https://api.slack.com/apps")
    logger.warning("  - Google API: https://makersuite.google.com/app/apikey")
    logger.warning("=" * 60)

# Initialize Slack app with error handling
try:
    app = App(
        token=os.environ.get("SLACK_BOT_TOKEN", "xoxb-placeholder"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET", "placeholder")
    )
    logger.info("✅ Slack app initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Slack app: {e}")
    app = None

# Initialize Google Gen AI (NEW SDK!)
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "placeholder"))
    model = genai.GenerativeModel('gemini-1.5-flash')  # Using stable model
    logger.info("✅ Google Gen AI initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Google Gen AI: {e}")
    model = None

# Initialize ChromaDB with Cloud Run compatible path
if os.environ.get('K_SERVICE'):  # Running in Cloud Run
    CHROMA_PERSIST_DIR = "/tmp/chroma_persist"
    logger.info("Running in Cloud Run - using /tmp for ChromaDB")
else:
    CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_persist")
    logger.info(f"Running locally - using {CHROMA_PERSIST_DIR} for ChromaDB")

os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

try:
    chroma_client = chromadb.PersistentClient(
        path=CHROMA_PERSIST_DIR,
        settings=Settings(
            anonymized_telemetry=False,
            persist_directory=CHROMA_PERSIST_DIR
        )
    )
    logger.info("✅ ChromaDB initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize ChromaDB: {e}")
    chroma_client = None

# Get or create collection with error handling
collection = None
if chroma_client:
    try:
        collection = chroma_client.get_collection("bob_knowledge")
        logger.info(f"✅ Loaded existing collection with {collection.count()} documents")
    except Exception as e:
        try:
            collection = chroma_client.create_collection(
                name="bob_knowledge",
                metadata={"description": "Bob's knowledge base", "version": "3.0"}
            )
            logger.info("✅ Created new collection")
        except Exception as create_error:
            logger.error(f"❌ Failed to create collection: {create_error}")

class BobBrain:
    """Bob's cognitive functions with proper error handling"""
    
    def __init__(self, collection):
        self.collection = collection
        self.conversation_history = {}
        self.max_history_size = 100  # Prevent memory leak
        self._lock = threading.Lock()  # Thread safety
    
    def search_knowledge(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search knowledge base with error handling"""
        if not self.collection:
            logger.warning("No collection available for search")
            return []
            
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(n_results, 10)  # Limit results
            )
            
            if results and results['documents']:
                return [
                    {
                        'content': doc[:1000],  # Truncate long docs
                        'metadata': meta,
                        'distance': dist
                    }
                    for doc, meta, dist in zip(
                        results['documents'][0],
                        results['metadatas'][0],
                        results['distances'][0]
                    )
                ]
            return []
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def generate_response(self, user_message: str, channel: str, user: str) -> str:
        """Generate response with proper error handling"""
        
        if not model:
            return "I'm having trouble connecting to my AI service. Please try again later."
        
        # Clean up old conversations to prevent memory leak
        with self._lock:
            if len(self.conversation_history) > self.max_history_size:
                # Remove oldest conversations
                oldest = sorted(self.conversation_history.keys())[:20]
                for key in oldest:
                    del self.conversation_history[key]
        
        try:
            # Search for relevant knowledge
            knowledge = self.search_knowledge(user_message, n_results=3)
            
            # Build context
            context = ""
            if knowledge:
                context = "Relevant knowledge:\n"
                for item in knowledge:
                    source = item['metadata'].get('source', 'unknown')
                    content = item['content'][:200]
                    context += f"- {content}...\n"
            
            # Get conversation history (thread-safe)
            history_key = f"{channel}_{user}"
            with self._lock:
                history = self.conversation_history.get(history_key, [])
            
            # Build prompt
            prompt = f"""You are Bob, a helpful AI assistant.
            
{context if knowledge else "No specific context available."}

Recent conversation:
{chr(10).join([f"{msg['role']}: {msg['content']}" for msg in history[-3:]])}

User: {user_message}

Provide a helpful, concise response. If you don't know something, say so."""

            # Generate with Google Gen AI
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                )
            )
            
            reply = response.text
            
            # Update conversation history (thread-safe)
            with self._lock:
                history.append({"role": "user", "content": user_message})
                history.append({"role": "assistant", "content": reply})
                self.conversation_history[history_key] = history[-10:]
            
            return reply
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "I apologize, but I'm having trouble generating a response. Please try again."

# Initialize Bob's brain
bob = BobBrain(collection) if collection else None

# Slack event handlers with error handling
@app.event("app_mention")
def handle_mention(event, say):
    """Handle mentions with error handling"""
    if not bob:
        say("I'm still starting up. Please try again in a moment.")
        return
        
    try:
        user = event.get('user', 'unknown')
        channel = event.get('channel', 'unknown')
        text = event.get('text', '')
        
        # Remove bot mention
        text = text.split('>', 1)[-1].strip() if '>' in text else text
        
        logger.info(f"Mention from {user} in {channel}: {text[:50]}...")
        
        # Generate response
        response = bob.generate_response(text, channel, user)
        
        # Send response in thread
        say(
            text=response,
            thread_ts=event.get('thread_ts', event.get('ts'))
        )
        
    except Exception as e:
        logger.error(f"Error handling mention: {e}")
        say("Sorry, I encountered an error. Please try again.")

@app.event("message")
def handle_direct_message(event, say):
    """Handle DMs with error handling"""
    if event.get('channel_type') == 'im' and 'bot_id' not in event:
        if not bob:
            say("I'm still starting up. Please try again in a moment.")
            return
            
        try:
            user = event.get('user', 'unknown')
            channel = event.get('channel', 'unknown')
            text = event.get('text', '')
            
            logger.info(f"DM from {user}: {text[:50]}...")
            
            # Generate response
            response = bob.generate_response(text, channel, user)
            
            # Send response
            say(response)
            
        except Exception as e:
            logger.error(f"Error handling DM: {e}")
            say("Sorry, I encountered an error. Please try again.")

# Health check endpoint for Cloud Run
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Health check endpoint"""
        if self.path == '/health':
            status = {
                'status': 'healthy',
                'slack': app is not None,
                'ai': model is not None,
                'database': collection is not None,
                'timestamp': datetime.now().isoformat()
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress health check logs

def run_health_server():
    """Run health check server in background"""
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    logger.info(f"Health check server running on port {port}")
    server.serve_forever()

# Graceful shutdown handler
def signal_handler(sig, frame):
    logger.info("Received shutdown signal, cleaning up...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Main entry point with proper error handling"""
    logger.info("=" * 60)
    logger.info("🤖 Starting Bob's Brain v3.0 (Production)")
    logger.info("=" * 60)
    
    # Check if we have valid tokens
    if missing_vars:
        logger.warning("Running in placeholder mode - update environment variables!")
        
        # Start health check server only
        health_thread = threading.Thread(target=run_health_server, daemon=True)
        health_thread.start()
        
        # Keep alive
        while True:
            time.sleep(60)
            logger.info("Waiting for proper configuration...")
    
    # Start health check server in background
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # Start Slack app
    if app and os.environ.get("SLACK_APP_TOKEN"):
        # Socket mode for development
        try:
            handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
            logger.info("Starting in Socket Mode...")
            handler.start()
        except Exception as e:
            logger.error(f"Failed to start Socket Mode: {e}")
    elif app:
        # Web server mode for production
        logger.info("Starting in Web Server mode...")
        port = int(os.environ.get("PORT", 3000))
        app.start(port=port)
    else:
        logger.error("Cannot start - Slack app not initialized")
        # Keep health check running
        while True:
            time.sleep(60)

if __name__ == "__main__":
    main()