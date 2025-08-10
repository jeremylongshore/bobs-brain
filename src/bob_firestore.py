#!/usr/bin/env python3
"""
Bob Firestore Edition - Cloud-native version using Firestore as primary database
Maintains compatibility with existing systems while adding cloud persistence
"""

import os
import time
import logging
import json
import threading
import signal
import sys
import hashlib
from typing import Optional, List, Dict, Any, Set
from datetime import datetime, timedelta
from contextlib import contextmanager

# Slack SDK
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.errors import SlackApiError

# AI Integration
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Firestore Integration
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False
    print("⚠️ Firestore not available. Install with: pip install google-cloud-firestore")

# ChromaDB for fallback
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


class BobFirestore:
    """
    Bob with Firestore as primary database
    Falls back to ChromaDB if Firestore is unavailable
    """
    
    def __init__(self):
        """Initialize Bob with Firestore integration"""
        self.setup_logging()
        self.logger.info("🚀 Initializing Bob Firestore Edition")
        
        # Environment variables
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "")
        self.slack_app_token = os.environ.get("SLACK_APP_TOKEN", "")
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
        
        # Validate tokens
        if not self.slack_bot_token or "PLACEHOLDER" in self.slack_bot_token:
            self.logger.error("❌ Missing Slack tokens! Get from api.slack.com")
            raise ValueError("Slack tokens required")
        
        # Initialize Slack
        self.slack_client = WebClient(token=self.slack_bot_token)
        self.socket_client = SocketModeClient(
            app_token=self.slack_app_token,
            web_client=self.slack_client
        )
        self.socket_client.socket_mode_request_listeners.append(self.handle_slack_event)
        
        # Initialize databases
        self.setup_databases()
        
        # Initialize Vertex AI
        self.setup_ai()
        
        # Duplicate prevention
        self.processed_messages: Set[str] = set()
        self.last_cleanup = datetime.now()
        
        # Conversation memory
        self.conversation_memory = {
            "recent_interactions": {},
            "greeting_count": {},
            "user_context": {},
            "conversation_history": {}
        }
        
        # Business context
        self.business_context = {
            "company": "DiagnosticPro.io",
            "owner": "Jeremy Longshore",
            "owner_user_id": None,
            "experience": "15 years business experience (BBI, trucking)",
        }
        
        # Health monitoring
        self.is_healthy = True
        self.start_time = datetime.now()
        self.db_type = "firestore" if self.firestore_db else "chromadb"
        
        # Graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        
        self.logger.info(f"✅ Bob Firestore initialized with {self.db_type}")
    
    def setup_logging(self):
        """Configure logging"""
        log_dir = 'logs' if os.path.exists('/app') else '/home/jeremylongshore/bobs-brain/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/bob_firestore.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('BobFirestore')
    
    def setup_databases(self):
        """Initialize Firestore as primary, ChromaDB as fallback"""
        self.firestore_db = None
        self.chroma_collection = None
        
        # Try Firestore first
        if FIRESTORE_AVAILABLE:
            try:
                project_id = os.environ.get("GCP_PROJECT", "diagnostic-pro-mvp")
                database_id = "bob-brain"  # Use bob-brain database
                
                self.firestore_db = firestore.Client(
                    project=project_id,
                    database=database_id
                )
                
                # Test connection
                test_doc = self.firestore_db.collection('shared_knowledge').limit(1).get()
                self.logger.info(f"✅ Connected to Firestore: {project_id}/{database_id}")
                
                # Count documents for stats
                try:
                    docs = self.firestore_db.collection('shared_knowledge').where('ai_agent', '==', 'bob').limit(1000).get()
                    count = len(list(docs))
                    self.logger.info(f"📚 Firestore has {count}+ Bob knowledge items")
                except:
                    pass
                    
            except Exception as e:
                self.logger.error(f"❌ Firestore connection failed: {e}")
                self.firestore_db = None
        
        # Fallback to ChromaDB if Firestore not available
        if not self.firestore_db and CHROMADB_AVAILABLE:
            try:
                chroma_path = 'chroma_data' if os.path.exists('/app') else '/home/jeremylongshore/bobs-brain/chroma_data'
                os.makedirs(chroma_path, exist_ok=True)
                
                chroma_client = chromadb.PersistentClient(path=chroma_path)
                
                try:
                    self.chroma_collection = chroma_client.get_collection('bob_knowledge')
                    count = self.chroma_collection.count()
                    self.logger.info(f"✅ Using ChromaDB fallback: {count} items")
                except:
                    self.chroma_collection = chroma_client.create_collection('bob_knowledge')
                    self.logger.info("✅ Created new ChromaDB collection")
                    
            except Exception as e:
                self.logger.error(f"❌ ChromaDB setup failed: {e}")
        
        if not self.firestore_db and not self.chroma_collection:
            self.logger.warning("⚠️ No database available - running in memory-only mode")
    
    def setup_ai(self):
        """Initialize Vertex AI"""
        try:
            project_id = os.environ.get("GCP_PROJECT", "bobs-house-ai")
            location = os.environ.get("GCP_LOCATION", "us-central1")
            
            vertexai.init(project=project_id, location=location)
            self.ai_model = GenerativeModel("gemini-2.0-flash-exp")
            self.logger.info("✅ Vertex AI initialized with Gemini 2.0")
            
        except Exception as e:
            self.logger.error(f"⚠️ Vertex AI initialization failed: {e}")
            self.ai_model = None
    
    def cleanup_old_messages(self):
        """Clean up old processed messages"""
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
        """Check if message is from a bot"""
        if event.get("bot_id"):
            return True
        if event.get("user", "").startswith("B"):
            return True
        text = event.get("text", "").lower()
        if any(phrase in text for phrase in ["i'm bob", "bob here", "bob firestore"]):
            return True
        return False
    
    def is_jeremy(self, user_id: str) -> bool:
        """Check if user is Jeremy"""
        return (user_id == self.business_context.get("owner_user_id") or
                self.conversation_memory.get("user_context", {}).get(user_id, {}).get("is_owner", False))
    
    def query_knowledge_firestore(self, query: str, max_results: int = 5) -> List[Dict]:
        """Query Firestore for relevant knowledge"""
        if not self.firestore_db:
            return []
        
        try:
            # Get knowledge from shared_knowledge collection
            knowledge_ref = self.firestore_db.collection('shared_knowledge')
            
            # Search by keywords (simple approach - in production use Vertex AI Search)
            query_words = query.lower().split()
            results = []
            
            # Get recent Bob knowledge
            docs = knowledge_ref.where('ai_agent', '==', 'bob').limit(100).get()
            
            for doc in docs:
                data = doc.to_dict()
                content = data.get('content', '').lower()
                
                # Simple relevance scoring
                relevance = sum(1 for word in query_words if word in content)
                if relevance > 0:
                    results.append({
                        'content': data.get('content', ''),
                        'metadata': data.get('metadata', {}),
                        'relevance': relevance / len(query_words),
                        'source': 'firestore'
                    })
            
            # Sort by relevance and return top results
            results.sort(key=lambda x: x['relevance'], reverse=True)
            return results[:max_results]
            
        except Exception as e:
            self.logger.error(f"Firestore query failed: {e}")
            return []
    
    def query_knowledge_chromadb(self, query: str, max_results: int = 5) -> List[Dict]:
        """Query ChromaDB for relevant knowledge (fallback)"""
        if not self.chroma_collection:
            return []
        
        try:
            results = self.chroma_collection.query(
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
                if 1.0 - dist > 0.3:
                    knowledge.append({
                        'content': doc,
                        'metadata': meta,
                        'relevance': 1.0 - dist,
                        'source': 'chromadb'
                    })
            return knowledge
            
        except Exception as e:
            self.logger.error(f"ChromaDB query failed: {e}")
            return []
    
    def query_knowledge(self, query: str, max_results: int = 5) -> List[Dict]:
        """Query knowledge from primary database"""
        if self.firestore_db:
            return self.query_knowledge_firestore(query, max_results)
        elif self.chroma_collection:
            return self.query_knowledge_chromadb(query, max_results)
        else:
            return []
    
    def store_conversation(self, user_id: str, message: str, response: str, channel: str = None):
        """Store conversation in Firestore"""
        if not self.firestore_db:
            return
        
        try:
            conversation_doc = {
                'user_id': user_id,
                'user_message': message,
                'bob_response': response,
                'channel': channel,
                'timestamp': datetime.now(),
                'ai_agent': 'bob_firestore',
                'conversation_id': hashlib.md5(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()
            }
            
            self.firestore_db.collection('bob_conversations').add(conversation_doc)
            self.logger.debug(f"💬 Stored conversation in Firestore")
            
        except Exception as e:
            self.logger.error(f"Failed to store conversation: {e}")
    
    def add_to_knowledge_base(self, content: str, metadata: Dict = None):
        """Add new knowledge to the database"""
        try:
            doc_id = hashlib.md5(content.encode()).hexdigest()[:16]
            
            if self.firestore_db:
                # Add to Firestore
                knowledge_doc = {
                    'content': content,
                    'content_hash': hashlib.sha256(content.encode()).hexdigest(),
                    'metadata': metadata or {},
                    'source': 'bob_learning',
                    'created_at': datetime.now(),
                    'ai_agent': 'bob_firestore',
                    'knowledge_type': metadata.get('type', 'general') if metadata else 'general'
                }
                
                self.firestore_db.collection('shared_knowledge').document(f"bob_{doc_id}").set(knowledge_doc)
                self.logger.info(f"📚 Added to Firestore knowledge base")
                
            elif self.chroma_collection:
                # Add to ChromaDB
                self.chroma_collection.add(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[metadata] if metadata else None
                )
                self.logger.info(f"📚 Added to ChromaDB knowledge base")
                
        except Exception as e:
            self.logger.error(f"Failed to add to knowledge base: {e}")
    
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
        
        # Store conversation history
        if user_id not in self.conversation_memory["conversation_history"]:
            self.conversation_memory["conversation_history"][user_id] = []
        
        self.conversation_memory["conversation_history"][user_id].append({
            "timestamp": now.isoformat(),
            "user": message,
            "bob": response
        })
        self.conversation_memory["conversation_history"][user_id] = \
            self.conversation_memory["conversation_history"][user_id][-10:]
        
        # Store in Firestore if available
        if response:
            self.store_conversation(user_id, message, response)
    
    def generate_response(self, user_message: str, user_id: str) -> str:
        """Generate response using AI + Knowledge + Context"""
        is_jeremy_user = self.is_jeremy(user_id)
        message_lower = user_message.lower().strip()
        
        # Simple greeting handling
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
            for item in knowledge[:3]:
                context += f"- {item['content'][:300]}...\n"
            context += f"\n(Source: {knowledge[0]['source']})\n"
        
        # Get conversation history
        history = self.conversation_memory.get("conversation_history", {}).get(user_id, [])
        if history:
            context += "\nRecent conversation:\n"
            for h in history[-3:]:
                if h.get('user'):
                    context += f"User: {h['user']}\n"
                if h.get('bob'):
                    context += f"Bob: {h['bob']}\n"
        
        # Use Vertex AI if available
        if self.ai_model:
            try:
                prompt = f"""You are Bob, a helpful AI assistant for DiagnosticPro.
Database: Using {self.db_type} for knowledge storage.
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
        """Handle Slack events"""
        try:
            # Cleanup periodically
            self.cleanup_old_messages()
            
            if request.type == "events_api":
                # Acknowledge request
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
                    thread_ts=event.get('thread_ts')
                )
                
                self.logger.info(f"✅ Responded: {response[:50]}...")
            else:
                client.ack(request.envelope_id)
            
        except Exception as e:
            self.logger.error(f"❌ Event handling error: {e}")
            try:
                client.ack(request.envelope_id)
            except:
                pass
    
    def health_check(self) -> Dict:
        """Generate health status"""
        knowledge_count = 0
        if self.firestore_db:
            try:
                docs = self.firestore_db.collection('shared_knowledge').where('ai_agent', '==', 'bob').limit(1).get()
                knowledge_count = "available"
            except:
                knowledge_count = "error"
        elif self.chroma_collection:
            knowledge_count = self.chroma_collection.count()
        
        return {
            'status': 'healthy' if self.is_healthy else 'unhealthy',
            'database': self.db_type,
            'uptime': str(datetime.now() - self.start_time),
            'processed_messages': len(self.processed_messages),
            'active_conversations': len(self.conversation_memory.get("recent_interactions", {})),
            'knowledge_items': knowledge_count,
            'ai_model': 'Vertex AI Gemini 2.0' if self.ai_model else 'None',
            'jeremy_identified': bool(self.business_context.get("owner_user_id")),
            'timestamp': datetime.now().isoformat()
        }
    
    def shutdown_handler(self, signum, frame):
        """Graceful shutdown"""
        self.logger.info("👋 Shutting down Bob Firestore gracefully...")
        self.is_healthy = False
        sys.exit(0)
    
    def start(self):
        """Start Bob Firestore service"""
        try:
            self.logger.info("🚀 Starting Bob Firestore Service...")
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
                self.logger.info(f"💓 Health: DB={health['database']}, Conversations={health['active_conversations']}, Messages={health['processed_messages']}")
                
        except KeyboardInterrupt:
            self.shutdown_handler(None, None)
        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}")
            raise


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════╗
    ║     BOB FIRESTORE EDITION v1.0       ║
    ║   Cloud-native with Firestore DB     ║
    ║   ChromaDB fallback supported        ║
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
        bob = BobFirestore()
        bob.start()
    except Exception as e:
        print(f"❌ Failed to start Bob Firestore: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())