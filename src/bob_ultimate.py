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

# AI Models - Supporting both Vertex AI and Google GenAI
try:
    # Try Vertex AI first (current setup)
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig
    AI_BACKEND = "vertex"
    vertexai.init(project="bobs-house-ai", location="us-central1")
    ai_model = GenerativeModel("gemini-2.0-flash-exp")
except ImportError:
    try:
        # Fallback to Google GenAI SDK (future-proof)
        import google.generativeai as genai
        AI_BACKEND = "genai"
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        ai_model = genai.GenerativeModel('gemini-1.5-flash')
    except ImportError:
        AI_BACKEND = None
        ai_model = None

class BobUltimate:
    """
    The ULTIMATE Bob - Best features from ALL versions
    
    Combines:
    - Professional communication from bob_unified_v2
    - Production error handling from bob_production
    - Simple directness from bob_solid
    - AI capabilities from all versions
    """
    
    def __init__(self, slack_bot_token: str, slack_app_token: str = None):
        """Initialize Ultimate Bob with all best features"""
        self.setup_logging()
        
        # Slack configuration
        self.slack_client = WebClient(token=slack_bot_token)
        self.slack_app_token = slack_app_token
        
        # Socket mode if app token provided
        if slack_app_token:
            self.socket_client = SocketModeClient(app_token=slack_app_token)
            self.socket_client.socket_mode_request_listeners.append(self.handle_slack_message)
        else:
            self.socket_client = None
        
        # Prevent duplicate responses (from bob_unified_v2)
        self.processed_messages: Set[str] = set()
        self.last_cleanup = datetime.now()
        self._lock = threading.Lock()  # Thread safety from bob_production
        
        # ChromaDB setup
        chroma_path = os.environ.get("CHROMA_PERSIST_DIR", "/home/jeremylongshore/bobs-brain/chroma_data")
        os.makedirs(chroma_path, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        
        try:
            self.knowledge_collection = self.chroma_client.get_collection('bob_knowledge')
            self.logger.info(f"📚 Loaded existing collection with {self.knowledge_collection.count()} documents")
        except:
            self.knowledge_collection = self.chroma_client.create_collection('bob_knowledge')
            self.logger.info("📚 Created new knowledge collection")
        
        # Load critical knowledge if available
        try:
            from knowledge_loader import ensure_knowledge_loaded
            ensure_knowledge_loaded()
            self.logger.info("✅ Additional knowledge loaded")
        except:
            pass  # Knowledge loader is optional
        
        # Business context (from bob_unified_v2)
        self.business_context = {
            "company": "DiagnosticPro.io",
            "owner": "Jeremy Longshore",
            "owner_user_id": None,
            "experience": "15 years business experience (BBI, trucking)",
        }
        
        # Conversation memory with limits (best of both versions)
        self.conversation_memory = {
            "recent_interactions": {},  # user_id -> last_interaction_time
            "history": {},              # user_id -> last 10 messages
            "user_context": {}          # user_id -> known context
        }
        
        # Professional response patterns
        self.response_patterns = {
            "jeremy_greeting": "Hey Jeremy! What's on your mind?",
            "business_greeting": "Hello! Bob here - your DiagnosticPro AI partner. How can I help?",
            "error_response": "I encountered an issue. Let me know if you need assistance."
        }
        
        # Health check server (from bob_production)
        self.health_server = None
        
        self.logger.info(f"🤖 Bob Ultimate initialized (AI: {AI_BACKEND or 'Knowledge-only'})")
    
    def setup_logging(self):
        """Configure logging system"""
        log_dir = "/home/jeremylongshore/bobs-brain/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/bob_ultimate.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BobUltimate')
    
    def cleanup_processed_messages(self):
        """Clean up old processed messages to prevent memory buildup"""
        with self._lock:
            now = datetime.now()
            if now - self.last_cleanup > timedelta(minutes=30):
                if len(self.processed_messages) > 1000:
                    recent_messages = list(self.processed_messages)[-500:]
                    self.processed_messages = set(recent_messages)
                self.last_cleanup = now
                self.logger.info(f"🧹 Cleaned message cache: {len(self.processed_messages)} retained")
    
    def is_duplicate_message(self, event: Dict[str, Any]) -> bool:
        """Check if message already processed"""
        message_id = f"{event.get('channel')}:{event.get('ts')}:{event.get('user')}:{event.get('text', '')[:50]}"
        
        with self._lock:
            if message_id in self.processed_messages:
                self.logger.debug(f"🔄 Duplicate message: {message_id}")
                return True
            self.processed_messages.add(message_id)
            return False
    
    def is_bot_message(self, event: Dict[str, Any]) -> bool:
        """Enhanced bot detection"""
        if event.get("bot_id"):
            return True
        
        user_id = event.get("user", "")
        if user_id.startswith("B"):  # Bot user IDs
            return True
        
        text = event.get("text", "").lower()
        if any(indicator in text for indicator in ["i'm bob", "bob here", "bob ultimate"]):
            return True
        
        return False
    
    def is_jeremy(self, user_id: str) -> bool:
        """Check if user is Jeremy"""
        return (user_id == self.business_context.get("owner_user_id") or
                self.conversation_memory.get("user_context", {}).get(user_id, {}).get("is_owner", False))
    
    def update_conversation_memory(self, user_id: str, message: str, response: str = None):
        """Update conversation memory with limits"""
        with self._lock:
            # Update last interaction
            self.conversation_memory["recent_interactions"][user_id] = datetime.now()
            
            # Update conversation history (keep last 10)
            if user_id not in self.conversation_memory["history"]:
                self.conversation_memory["history"][user_id] = []
            
            self.conversation_memory["history"][user_id].append({
                "user": message,
                "bob": response,
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_memory["history"][user_id] = self.conversation_memory["history"][user_id][-10:]
            
            # Identify Jeremy
            if "jeremy" in message.lower():
                self.business_context["owner_user_id"] = user_id
                self.conversation_memory["user_context"][user_id] = {
                    "is_owner": True,
                    "name": "Jeremy"
                }
    
    def query_knowledge_base(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Query ChromaDB knowledge base"""
        try:
            results = self.knowledge_collection.query(
                query_texts=[query],
                n_results=max_results,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            knowledge_items = []
            for doc, metadata, distance in zip(
                results['documents'][0],
                results['metadatas'][0] or [{}] * len(results['documents'][0]),
                results['distances'][0]
            ):
                relevance = 1.0 - distance
                if relevance > 0.3:
                    knowledge_items.append({
                        'content': doc[:500],  # Limit length
                        'metadata': metadata,
                        'relevance': relevance
                    })
            
            return knowledge_items
            
        except Exception as e:
            self.logger.error(f"Knowledge query error: {e}")
            return []
    
    def generate_response(self, user_message: str, user_id: str) -> str:
        """
        Generate response using AI + knowledge base
        Best of all versions combined
        """
        message_lower = user_message.lower().strip()
        is_jeremy_user = self.is_jeremy(user_id)
        
        # Simple greeting handling (from bob_solid simplicity)
        if any(g in message_lower for g in ["hello", "hi", "hey"]):
            if is_jeremy_user:
                return self.response_patterns["jeremy_greeting"]
            else:
                return self.response_patterns["business_greeting"]
        
        # Query knowledge base
        knowledge = self.query_knowledge_base(user_message)
        
        # Build context from knowledge
        context = ""
        if knowledge:
            context = "Relevant knowledge:\n"
            for item in knowledge[:2]:  # Top 2 results
                context += f"- {item['content'][:200]}...\n"
        
        # Get conversation history
        history = self.conversation_memory.get("history", {}).get(user_id, [])
        history_text = ""
        if history:
            recent = history[-3:]  # Last 3 exchanges
            for h in recent:
                history_text += f"User: {h['user']}\nBob: {h.get('bob', 'thinking...')}\n"
        
        # Generate with AI if available
        if ai_model and AI_BACKEND:
            try:
                prompt = f"""You are Bob, a helpful AI assistant for DiagnosticPro.
                
{context}

Recent conversation:
{history_text}

User: {user_message}

Provide a helpful, concise response. If you don't know, say so honestly."""
                
                if AI_BACKEND == "vertex":
                    response = ai_model.generate_content(
                        prompt,
                        generation_config=GenerationConfig(
                            temperature=0.7,
                            max_output_tokens=300
                        )
                    )
                    return response.text
                    
                elif AI_BACKEND == "genai":
                    response = ai_model.generate_content(prompt)
                    return response.text
                    
            except Exception as e:
                self.logger.error(f"AI generation error: {e}")
                # Fall through to knowledge-based response
        
        # Fallback to knowledge-based response
        if knowledge and knowledge[0]['relevance'] > 0.5:
            content = knowledge[0]['content']
            if is_jeremy_user:
                return f"Based on what I know: {content}"
            else:
                return f"From DiagnosticPro knowledge: {content}"
        
        # Default responses
        if "diagnostic" in message_lower or "repair" in message_lower:
            return "DiagnosticPro helps protect from repair overcharges. What specific diagnostic question do you have?"
        
        return "How can I help with DiagnosticPro or vehicle diagnostics?"
    
    def handle_slack_message(self, client, request):
        """Handle Slack messages with all safety features"""
        try:
            self.cleanup_processed_messages()
            
            if request.type == "events_api":
                event = request.payload.get("event", {})
                
                # Validate message
                if not (event.get("type") == "message" and event.get("text")):
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                # Skip bot messages
                if self.is_bot_message(event):
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                # Skip duplicates
                if self.is_duplicate_message(event):
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                user_text = event.get("text", "").strip()
                channel = event.get("channel")
                user_id = event.get("user")
                
                if not all([user_text, channel, user_id]):
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                self.logger.info(f"📩 Message from {user_id}: '{user_text[:50]}...'")
                
                # Generate response
                response = self.generate_response(user_text, user_id)
                
                # Update memory
                self.update_conversation_memory(user_id, user_text, response)
                
                # Send to Slack
                self.slack_client.chat_postMessage(
                    channel=channel,
                    text=response,
                    username="Bob Ultimate"
                )
                
                self.logger.info(f"✅ Responded: '{response[:50]}...'")
        
        except Exception as e:
            self.logger.error(f"Message handling error: {e}")
            try:
                if 'channel' in locals():
                    self.slack_client.chat_postMessage(
                        channel=channel,
                        text=self.response_patterns["error_response"]
                    )
            except:
                pass
        
        finally:
            if hasattr(request, 'ack'):
                request.ack()
    
    def start_health_server(self):
        """Start health check server for Cloud Run"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    status = {
                        'status': 'healthy',
                        'ai_backend': AI_BACKEND or 'none',
                        'timestamp': datetime.now().isoformat()
                    }
                    self.wfile.write(json.dumps(status).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                pass  # Suppress logs
        
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        
        def run_server():
            self.logger.info(f"🏥 Health server on port {port}")
            server.serve_forever()
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        return server
    
    def start_service(self):
        """Start Bob Ultimate service"""
        try:
            self.logger.info("🚀 Starting Bob Ultimate...")
            
            # Start health check server
            self.health_server = self.start_health_server()
            
            # Log status
            knowledge_count = self.knowledge_collection.count()
            self.logger.info(f"📚 Knowledge base: {knowledge_count} items")
            self.logger.info(f"🤖 AI Backend: {AI_BACKEND or 'Knowledge-only mode'}")
            
            if self.socket_client:
                # Socket mode
                self.socket_client.connect()
                self.logger.info("✅ Bob Ultimate active on Slack (Socket Mode)")
                
                while True:
                    time.sleep(60)
                    if not self.socket_client.is_connected():
                        self.logger.warning("Reconnecting to Slack...")
                        self.socket_client.connect()
            else:
                # Webhook mode - just keep health server running
                self.logger.info("✅ Bob Ultimate ready (Webhook Mode)")
                while True:
                    time.sleep(60)
                    self.logger.debug(f"Status: {len(self.processed_messages)} messages processed")
        
        except KeyboardInterrupt:
            self.logger.info("👋 Shutting down gracefully...")
        except Exception as e:
            self.logger.error(f"Critical error: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive status"""
        return {
            'service': 'Bob Ultimate',
            'version': '1.0 FINAL',
            'ai_backend': AI_BACKEND or 'none',
            'knowledge_items': self.knowledge_collection.count(),
            'processed_messages': len(self.processed_messages),
            'active_users': len(self.conversation_memory["recent_interactions"]),
            'jeremy_identified': bool(self.business_context.get("owner_user_id")),
            'features': [
                'Duplicate prevention',
                'Smart memory management',
                'Professional communication',
                'AI + Knowledge hybrid',
                'Thread safety',
                'Health checks'
            ],
            'timestamp': datetime.now().isoformat()
        }


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print("\n👋 Bob Ultimate shutting down...")
    sys.exit(0)


def main():
    """Main entry point for Bob Ultimate"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Get tokens
    slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
    slack_app_token = os.getenv('SLACK_APP_TOKEN')  # Optional for socket mode
    
    if not slack_bot_token:
        print("❌ ERROR: SLACK_BOT_TOKEN not found")
        print("Get it from: https://api.slack.com/apps")
        return 1
    
    # Check for placeholder tokens
    if "PLACEHOLDER" in slack_bot_token:
        print("⚠️ WARNING: Using placeholder token")
        print("Update with real token from: https://api.slack.com/apps")
    
    try:
        # Initialize and start Bob Ultimate
        bob = BobUltimate(slack_bot_token, slack_app_token)
        
        # Print status
        status = bob.get_status()
        print(f"\n{'='*60}")
        print(f"🤖 BOB ULTIMATE - THE FINAL VERSION")
        print(f"{'='*60}")
        print(f"AI Backend: {status['ai_backend']}")
        print(f"Knowledge Base: {status['knowledge_items']} items")
        print(f"Features: {', '.join(status['features'][:3])}")
        print(f"{'='*60}\n")
        
        # Start service
        bob.start_service()
        
    except Exception as e:
        print(f"❌ Failed to start Bob Ultimate: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())