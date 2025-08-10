#!/usr/bin/env python3
"""
Bob Cloud Run Edition - HTTP endpoints for Google Cloud Run deployment
Uses Firestore for persistence and Vertex AI for intelligence
"""

import os
import sys
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Set
from pathlib import Path

# Flask for HTTP endpoints (Cloud Run requirement)
from flask import Flask, request, jsonify, make_response

# Slack SDK
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

# AI Integration - Vertex AI only
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Firestore
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv()
except ImportError:
    pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BobCloudRun')

# Flask app
app = Flask(__name__)

class BobCloudRun:
    """Bob optimized for Cloud Run with HTTP endpoints"""
    
    def __init__(self):
        """Initialize Bob for Cloud Run"""
        logger.info("🚀 Initializing Bob Cloud Run Edition")
        
        # Get tokens from environment
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "")
        self.slack_app_token = os.environ.get("SLACK_APP_TOKEN", "")  # Not used in HTTP mode
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
        
        if not self.slack_bot_token or not self.slack_signing_secret:
            logger.error("❌ Missing required Slack tokens")
            raise ValueError("SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET required")
        
        # Initialize Slack client and verifier
        self.slack_client = WebClient(token=self.slack_bot_token)
        self.signature_verifier = SignatureVerifier(self.slack_signing_secret)
        
        # Initialize Firestore
        self.setup_firestore()
        
        # Initialize Vertex AI
        self.setup_vertex_ai()
        
        # Memory management
        self.processed_messages: Set[str] = set()
        self.last_cleanup = datetime.now()
        self.conversation_memory = {}
        
        # Business context
        self.business_context = {
            "company": "DiagnosticPro.io",
            "owner": "Jeremy Longshore",
            "project": "diagnostic-pro-mvp"
        }
        
        self.start_time = datetime.now()
        logger.info("✅ Bob Cloud Run initialized successfully")
    
    def setup_firestore(self):
        """Initialize Firestore connection"""
        self.firestore_db = None
        
        if FIRESTORE_AVAILABLE:
            try:
                project_id = os.environ.get("GCP_PROJECT", "diagnostic-pro-mvp")
                database_id = os.environ.get("FIRESTORE_DATABASE", "bob-brain")
                
                self.firestore_db = firestore.Client(
                    project=project_id,
                    database=database_id
                )
                
                # Test connection
                test = self.firestore_db.collection('shared_knowledge').limit(1).get()
                logger.info(f"✅ Connected to Firestore: {project_id}/{database_id}")
            except Exception as e:
                logger.error(f"❌ Firestore connection failed: {e}")
                self.firestore_db = None
    
    def setup_vertex_ai(self):
        """Initialize Vertex AI"""
        try:
            project_id = os.environ.get("GCP_PROJECT", "diagnostic-pro-mvp")
            location = os.environ.get("GCP_LOCATION", "us-central1")
            
            vertexai.init(project=project_id, location=location)
            self.ai_model = GenerativeModel("gemini-2.0-flash-exp")
            logger.info("✅ Vertex AI initialized")
        except Exception as e:
            logger.error(f"❌ Vertex AI initialization failed: {e}")
            self.ai_model = None
    
    def verify_slack_request(self, request_body: bytes, timestamp: str, signature: str) -> bool:
        """Verify request is from Slack"""
        try:
            return self.signature_verifier.is_valid(request_body, timestamp, signature)
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    def is_duplicate(self, event: Dict) -> bool:
        """Check if message is duplicate"""
        msg_id = f"{event.get('channel')}:{event.get('ts')}:{event.get('text', '')[:50]}"
        if msg_id in self.processed_messages:
            return True
        self.processed_messages.add(msg_id)
        
        # Cleanup old messages periodically
        if datetime.now() - self.last_cleanup > timedelta(minutes=30):
            if len(self.processed_messages) > 1000:
                self.processed_messages = set(list(self.processed_messages)[-500:])
            self.last_cleanup = datetime.now()
        
        return False
    
    def query_knowledge(self, query: str, max_results: int = 3) -> List[Dict]:
        """Query Firestore for relevant knowledge"""
        if not self.firestore_db:
            return []
        
        try:
            # Simple keyword search (in production, use Vertex AI Search)
            knowledge_ref = self.firestore_db.collection('shared_knowledge')
            docs = knowledge_ref.where('ai_agent', '==', 'bob').limit(50).get()
            
            query_words = query.lower().split()
            results = []
            
            for doc in docs:
                data = doc.to_dict()
                content = data.get('content', '').lower()
                
                # Calculate relevance
                relevance = sum(1 for word in query_words if word in content)
                if relevance > 0:
                    results.append({
                        'content': data.get('content', ''),
                        'relevance': relevance / len(query_words)
                    })
            
            # Sort by relevance
            results.sort(key=lambda x: x['relevance'], reverse=True)
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Knowledge query failed: {e}")
            return []
    
    def generate_response(self, message: str, user_id: str) -> str:
        """Generate response using Vertex AI"""
        message_lower = message.lower().strip()
        
        # Simple greetings
        if any(g in message_lower for g in ["hello", "hi", "hey"]):
            return "Hello! I'm Bob, your DiagnosticPro AI assistant. How can I help you today?"
        
        # Query knowledge
        knowledge = self.query_knowledge(message)
        
        # Build context
        context = ""
        if knowledge:
            context = "Relevant knowledge:\n"
            for item in knowledge[:2]:
                context += f"- {item['content'][:200]}...\n"
        
        # Use Vertex AI
        if self.ai_model:
            try:
                prompt = f"""You are Bob, a helpful AI assistant for DiagnosticPro.
{context}

User: {message}

Provide a helpful, concise response. Be professional but friendly."""
                
                response = self.ai_model.generate_content(
                    prompt,
                    generation_config=GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=300
                    )
                )
                return response.text.strip()
            except Exception as e:
                logger.error(f"AI generation failed: {e}")
        
        # Fallback
        if knowledge and knowledge[0]['relevance'] > 0.5:
            return f"Based on my knowledge: {knowledge[0]['content'][:300]}..."
        
        return "I'm here to help with DiagnosticPro questions. What would you like to know?"
    
    def handle_event(self, event: Dict) -> Optional[str]:
        """Process Slack event and return response"""
        # Skip bot messages
        if event.get("bot_id") or event.get("user", "").startswith("B"):
            return None
        
        # Skip duplicates
        if self.is_duplicate(event):
            logger.debug(f"Skipping duplicate message")
            return None
        
        # Get message details
        text = event.get("text", "").strip()
        user_id = event.get("user", "")
        channel = event.get("channel", "")
        
        if not text or not user_id:
            return None
        
        logger.info(f"Processing message from {user_id}: {text[:50]}...")
        
        # Generate response
        response = self.generate_response(text, user_id)
        
        # Store conversation if Firestore available
        if self.firestore_db:
            try:
                conversation_doc = {
                    'user_id': user_id,
                    'user_message': text,
                    'bob_response': response,
                    'channel': channel,
                    'timestamp': datetime.now(),
                    'ai_agent': 'bob_cloud_run'
                }
                self.firestore_db.collection('bob_conversations').add(conversation_doc)
            except Exception as e:
                logger.error(f"Failed to store conversation: {e}")
        
        return response
    
    def send_response(self, channel: str, text: str, thread_ts: Optional[str] = None):
        """Send response to Slack"""
        try:
            self.slack_client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts
            )
            logger.info(f"Sent response: {text[:50]}...")
        except SlackApiError as e:
            logger.error(f"Failed to send message: {e}")

# Create global Bob instance
bob = BobCloudRun()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    uptime = str(datetime.now() - bob.start_time)
    status = {
        'status': 'healthy',
        'service': 'bob-cloud-run',
        'uptime': uptime,
        'firestore': 'connected' if bob.firestore_db else 'disconnected',
        'vertex_ai': 'connected' if bob.ai_model else 'disconnected',
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(status), 200

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    # Verify request is from Slack
    request_body = request.get_data()
    timestamp = request.headers.get('X-Slack-Request-Timestamp', '')
    signature = request.headers.get('X-Slack-Signature', '')
    
    if not bob.verify_slack_request(request_body, timestamp, signature):
        logger.warning("Invalid request signature")
        return make_response("Unauthorized", 401)
    
    # Parse request
    data = request.get_json()
    
    # Handle URL verification challenge
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data.get('challenge', '')})
    
    # Handle events
    if data.get('type') == 'event_callback':
        event = data.get('event', {})
        
        # Process message events
        if event.get('type') == 'message':
            response = bob.handle_event(event)
            
            if response:
                # Send response back to Slack
                channel = event.get('channel')
                thread_ts = event.get('thread_ts')
                bob.send_response(channel, response, thread_ts)
        
        # Return immediately (Slack requires quick response)
        return make_response("", 200)
    
    # Handle app mentions
    if data.get('type') == 'app_mention':
        event = data.get('event', {})
        response = bob.handle_event(event)
        
        if response:
            channel = event.get('channel')
            thread_ts = event.get('ts')  # Reply in thread
            bob.send_response(channel, response, thread_ts)
        
        return make_response("", 200)
    
    return make_response("", 200)

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'service': 'Bob Cloud Run',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            '/health': 'Health check',
            '/slack/events': 'Slack events webhook'
        }
    })

def main():
    """Main entry point"""
    port = int(os.environ.get('PORT', 3000))
    
    print("""
    ╔══════════════════════════════════════╗
    ║     BOB CLOUD RUN EDITION v1.0       ║
    ║   Optimized for Google Cloud Run     ║
    ║   HTTP endpoints + Firestore         ║
    ╚══════════════════════════════════════╝
    """)
    
    logger.info(f"Starting Bob Cloud Run on port {port}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main()