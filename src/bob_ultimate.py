#!/usr/bin/env python3
"""
Bob Ultimate - The FINAL Unified Version
Combines the best of all Bob versions into ONE
"""

import os
import time
import logging
import chromadb
import json
import threading
import signal
import sys
from typing import Optional, List, Dict, Any, Set
from datetime import datetime, timedelta
from contextlib import contextmanager

# Slack SDK
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.errors import SlackApiError

# AI Integration - Vertex AI (will migrate to Google Gen AI later)
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

class BobUltimate:
    """
    The ULTIMATE Bob - Best features from all versions combined
    
    Features merged:
    - Professional communication (from recovered-latest)
    - Duplicate prevention (from recovered-latest)
    - Smart memory management (from recovered-latest)
    - Vertex AI integration (from local versions)
    - Health checks (from bob_production)
    - Error handling (from bob_production)
    - Knowledge loader (from recovered-latest)
    - Jeremy recognition (from recovered-latest)
    """
    
    def __init__(self):
        """Initialize the ULTIMATE Bob with all best features"""
        self.setup_logging()
        self.logger.info("🚀 Initializing Bob Ultimate - The FINAL Version")
        
        # Get environment variables
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "")
        self.slack_app_token = os.environ.get("SLACK_APP_TOKEN", "")
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
        
        # Validate tokens
        if not self.slack_bot_token or "PLACEHOLDER" in self.slack_bot_token:
            self.logger.error("❌ Missing Slack tokens! Get from api.slack.com")
            self.logger.error("Need: SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_SIGNING_SECRET")
            raise ValueError("Slack tokens required")
        
        # Initialize Slack
        self.slack_client = WebClient(token=self.slack_bot_token)
        self.socket_client = SocketModeClient(
            app_token=self.slack_app_token,
            web_client=self.slack_client
        )
        self.socket_client.socket_mode_request_listeners.append(self.handle_slack_event)
        
        # Initialize Vertex AI
        self.setup_ai()
        
        # Initialize ChromaDB
        self.setup_knowledge_base()
        
        # Duplicate prevention (from recovered-latest)
        self.processed_messages: Set[str] = set()
        self.last_cleanup = datetime.now()
        
        # Smart conversation memory (from recovered-latest)
        self.conversation_memory = {
            "recent_interactions": {},  # user_id -> last_interaction_time
            "greeting_count": {},       # user_id -> count of recent greetings
            "user_context": {},         # user_id -> known context about user
            "conversation_history": {}  # user_id -> last 10 messages
        }
        
        # Business context (from recovered-latest)
        self.business_context = {
            "company": "DiagnosticPro.io",
            "owner": "Jeremy Longshore",
            "owner_user_id": None,
            "experience": "15 years business experience (BBI, trucking)",
        }
        
        # Health check flag
        self.is_healthy = True
        self.start_time = datetime.now()
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        
        self.logger.info("✅ Bob Ultimate initialized successfully!")
    
    def setup_logging(self):
        """Configure professional logging"""
        log_dir = '/home/jeremylongshore/bobs-brain/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/bob_ultimate.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('BobUltimate')
    
    def setup_ai(self):
        """Initialize Vertex AI with fallback"""
        try:
            project_id = os.environ.get("GCP_PROJECT", "bobs-house-ai")
            location = os.environ.get("GCP_LOCATION", "us-central1")
            
            vertexai.init(project=project_id, location=location)
            self.ai_model = GenerativeModel("gemini-2.0-flash-exp")
            self.logger.info("✅ Vertex AI initialized with Gemini 2.0")
            
        except Exception as e:
            self.logger.error(f"⚠️ Vertex AI initialization failed: {e}")
            self.ai_model = None
    
    def setup_knowledge_base(self):
        """Initialize ChromaDB with proper path"""
        try:
            # Use proper bobs-brain directory
            chroma_path = '/home/jeremylongshore/bobs-brain/chroma_data'
            os.makedirs(chroma_path, exist_ok=True)
            
            self.chroma_client = chromadb.PersistentClient(path=chroma_path)
            
            # Get or create collection
            try:
                self.knowledge_collection = self.chroma_client.get_collection('bob_knowledge')
                count = self.knowledge_collection.count()
                self.logger.info(f"✅ Loaded existing knowledge base: {count} items")
            except:
                self.knowledge_collection = self.chroma_client.create_collection('bob_knowledge')
                self.logger.info("✅ Created new knowledge collection")
                self.load_initial_knowledge()
                
        except Exception as e:
            self.logger.error(f"❌ ChromaDB setup failed: {e}")
            self.knowledge_collection = None
    
    def load_initial_knowledge(self):
        """Load initial knowledge from knowledge_loader if available"""
        try:
            # Import knowledge loader from recovered-latest
            sys.path.insert(0, '/home/jeremylongshore/bobs-brain/src')
            from knowledge_loader import ensure_knowledge_loaded
            ensure_knowledge_loaded()
            self.logger.info("✅ Loaded initial knowledge base")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load initial knowledge: {e}")
    
    def cleanup_old_messages(self):
        """Clean up old processed messages to prevent memory leak"""
        now = datetime.now()
        if now - self.last_cleanup > timedelta(minutes=30):
            if len(self.processed_messages) > 1000:
                recent = list(self.processed_messages)[-500:]
                self.processed_messages = set(recent)
                self.logger.info(f"🧹 Cleaned message cache: {len(self.processed_messages)} retained")
            self.last_cleanup = now
    
    def is_duplicate(self, event: Dict) -> bool:
        """Check if message is duplicate"""
        msg_id = f"{event.get('channel')}:{event.get('ts')}:{event.get('text', '')[:50]}"
        if msg_id in self.processed_messages:
            return True
        self.processed_messages.add(msg_id)
        return False
    
    def is_bot_message(self, event: Dict) -> bool:
        """Enhanced bot detection"""
        if event.get("bot_id"):
            return True
        if event.get("user", "").startswith("B"):
            return True
        text = event.get("text", "").lower()
        if any(phrase in text for phrase in ["i'm bob", "bob here", "bob ultimate"]):
            return True
        return False
    
    def is_jeremy(self, user_id: str) -> bool:
        """Check if user is Jeremy"""
        return (user_id == self.business_context.get("owner_user_id") or
                self.conversation_memory.get("user_context", {}).get(user_id, {}).get("is_owner", False))
    
    def update_conversation_memory(self, user_id: str, message: str, response: str = None):
        """Update conversation memory with history"""
        now = datetime.now()
        
        # Update last interaction
        self.conversation_memory["recent_interactions"][user_id] = now
        
        # Track greetings
        if any(g in message.lower() for g in ["hello", "hi", "hey", "good morning"]):
            if user_id not in self.conversation_memory["greeting_count"]:
                self.conversation_memory["greeting_count"][user_id] = []
            self.conversation_memory["greeting_count"][user_id].append(now)
            # Keep only last 5 greetings
            self.conversation_memory["greeting_count"][user_id] = \
                self.conversation_memory["greeting_count"][user_id][-5:]
        
        # Identify Jeremy
        if "jeremy" in message.lower():
            self.business_context["owner_user_id"] = user_id
            self.conversation_memory["user_context"][user_id] = {
                "is_owner": True,
                "name": "Jeremy",
                "relationship": "business_owner"
            }
        
        # Store conversation history (last 10 exchanges)
        if user_id not in self.conversation_memory["conversation_history"]:
            self.conversation_memory["conversation_history"][user_id] = []
        
        self.conversation_memory["conversation_history"][user_id].append({
            "timestamp": now.isoformat(),
            "user": message,
            "bob": response
        })
        # Keep only last 10
        self.conversation_memory["conversation_history"][user_id] = \
            self.conversation_memory["conversation_history"][user_id][-10:]
    
    def query_knowledge(self, query: str, max_results: int = 3) -> List[Dict]:
        """Query ChromaDB for relevant knowledge"""
        if not self.knowledge_collection:
            return []
        
        try:
            results = self.knowledge_collection.query(
                query_texts=[query],
                n_results=max_results
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            knowledge = []
            for doc, meta, dist in zip(
                results['documents'][0],
                results.get('metadatas', [[]])[0],
                results['distances'][0]
            ):
                if 1.0 - dist > 0.3:  # Relevance threshold
                    knowledge.append({
                        'content': doc,
                        'metadata': meta,
                        'relevance': 1.0 - dist
                    })
            return knowledge
            
        except Exception as e:
            self.logger.error(f"Knowledge query failed: {e}")
            return []
    
    def generate_response(self, user_message: str, user_id: str) -> str:
        """
        Generate response using AI + Knowledge + Context
        Combines best of all versions
        """
        is_jeremy_user = self.is_jeremy(user_id)
        message_lower = user_message.lower().strip()
        
        # Simple greeting handling (from recovered-latest)
        if any(g in message_lower for g in ["hello", "hi", "hey"]):
            if is_jeremy_user:
                return "Hey Jeremy! What can I help you with today?"
            else:
                return "Hello! I'm Bob, your DiagnosticPro AI assistant. How can I help?"
        
        # Query knowledge base
        knowledge = self.query_knowledge(user_message)
        
        # Build context for AI
        context = ""
        if knowledge:
            context = "Relevant knowledge:\n"
            for item in knowledge[:2]:  # Use top 2
                context += f"- {item['content'][:200]}...\n"
        
        # Get conversation history
        history = self.conversation_memory.get("conversation_history", {}).get(user_id, [])
        if history:
            context += "\nRecent conversation:\n"
            for h in history[-3:]:  # Last 3 exchanges
                if h.get('user'):
                    context += f"User: {h['user']}\n"
                if h.get('bob'):
                    context += f"Bob: {h['bob']}\n"
        
        # Use Vertex AI if available
        if self.ai_model:
            try:
                prompt = f"""You are Bob, a helpful AI assistant for DiagnosticPro.
{context}

User: {user_message}

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
                self.logger.error(f"AI generation failed: {e}")
        
        # Fallback responses if AI fails
        if knowledge and knowledge[0]['relevance'] > 0.5:
            return f"Based on my knowledge: {knowledge[0]['content'][:300]}..."
        
        # Domain-specific fallbacks
        if any(word in message_lower for word in ["diagnostic", "repair", "vehicle"]):
            if is_jeremy_user:
                return "What specific diagnostic challenge are we tackling today?"
            return "DiagnosticPro helps protect against repair overcharges. How can I assist?"
        
        # Default
        if is_jeremy_user:
            return "What can I help you with, Jeremy?"
        return "How can I assist you today?"
    
    def handle_slack_event(self, client, request):
        """Handle Slack events with all safety checks"""
        try:
            # Cleanup periodically
            self.cleanup_old_messages()
            
            if request.type == "events_api":
                # Acknowledge request immediately for Socket Mode
                client.ack(request.envelope_id)
                
                event = request.payload.get("event", {})
                
                # Validate event
                if event.get("type") != "message" or not event.get("text"):
                    return
                
                # Skip bot messages
                if self.is_bot_message(event):
                    return
                
                # Skip duplicates
                if self.is_duplicate(event):
                    return
                
                user_text = event.get("text", "").strip()
                channel = event.get("channel")
                user_id = event.get("user")
                
                if not all([user_text, channel, user_id]):
                    return
                
                self.logger.info(f"📩 Message from {user_id}: {user_text[:50]}...")
                
                # Generate response
                response = self.generate_response(user_text, user_id)
                
                # Update memory
                self.update_conversation_memory(user_id, user_text, response)
                
                # Send response
                self.slack_client.chat_postMessage(
                    channel=channel,
                    text=response,
                    thread_ts=event.get('thread_ts')  # Only thread if already in thread
                )
                
                self.logger.info(f"✅ Responded: {response[:50]}...")
            else:
                # Acknowledge non-event requests
                client.ack(request.envelope_id)
            
        except Exception as e:
            self.logger.error(f"❌ Event handling error: {e}")
            try:
                client.ack(request.envelope_id)
            except:
                pass
    
    def health_check(self) -> Dict:
        """Generate health status"""
        return {
            'status': 'healthy' if self.is_healthy else 'unhealthy',
            'uptime': str(datetime.now() - self.start_time),
            'processed_messages': len(self.processed_messages),
            'active_conversations': len(self.conversation_memory.get("recent_interactions", {})),
            'knowledge_items': self.knowledge_collection.count() if self.knowledge_collection else 0,
            'ai_model': 'Vertex AI Gemini 2.0' if self.ai_model else 'None',
            'jeremy_identified': bool(self.business_context.get("owner_user_id")),
            'timestamp': datetime.now().isoformat()
        }
    
    def shutdown_handler(self, signum, frame):
        """Graceful shutdown"""
        self.logger.info("👋 Shutting down Bob Ultimate gracefully...")
        self.is_healthy = False
        sys.exit(0)
    
    def start(self):
        """Start Bob Ultimate service"""
        try:
            self.logger.info("🚀 Starting Bob Ultimate Service...")
            self.logger.info(f"📊 Health: {json.dumps(self.health_check(), indent=2)}")
            
            # Connect to Slack
            self.socket_client.connect()
            self.logger.info("✅ Connected to Slack!")
            
            # Keep running with periodic health checks
            while self.is_healthy:
                time.sleep(60)
                
                # Health check
                if not self.socket_client.is_connected():
                    self.logger.warning("⚠️ Reconnecting to Slack...")
                    self.socket_client.connect()
                
                # Log status
                health = self.health_check()
                self.logger.info(f"💓 Health: {health['active_conversations']} conversations, {health['processed_messages']} messages")
                
        except KeyboardInterrupt:
            self.shutdown_handler(None, None)
        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}")
            raise


def main():
    """Main entry point for Bob Ultimate"""
    print("""
    ╔══════════════════════════════════════╗
    ║        BOB ULTIMATE v1.0             ║
    ║   The FINAL Unified Bob Version      ║
    ║   Combining ALL Best Features        ║
    ╚══════════════════════════════════════╝
    """)
    
    # Check for tokens
    if not os.environ.get("SLACK_BOT_TOKEN"):
        print("❌ ERROR: Missing Slack tokens!")
        print("\nSet these environment variables:")
        print("  export SLACK_BOT_TOKEN=xoxb-...")
        print("  export SLACK_APP_TOKEN=xapp-...")
        print("  export SLACK_SIGNING_SECRET=...")
        print("\nGet them from: https://api.slack.com/apps")
        return 1
    
    try:
        bob = BobUltimate()
        bob.start()
    except Exception as e:
        print(f"❌ Failed to start Bob Ultimate: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())