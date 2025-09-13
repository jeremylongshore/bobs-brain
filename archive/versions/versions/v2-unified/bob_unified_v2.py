#!/usr/bin/env python3
"""
Bob Unified Agent v2 - Professional Communication Edition
Fixes: Duplicate responses, verbose introductions, adds conversation memory
"""

import os
import time
import logging
import chromadb
import json
from typing import Optional, List, Dict, Any, Set
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from datetime import datetime, timedelta

class BobUnifiedV2:
    """
    Enhanced Bob AI Agent with Professional Communication
    
    Fixes:
    - Duplicate response prevention
    - Smart conversation memory
    - Concise business partner communication
    - Context-aware responses
    """
    
    def __init__(self, slack_bot_token: str, slack_app_token: str):
        """Initialize enhanced Bob with professional communication improvements"""
        self.setup_logging()
        
        # Slack configuration
        self.slack_client = WebClient(token=slack_bot_token)
        self.socket_client = SocketModeClient(app_token=slack_app_token)
        self.socket_client.socket_mode_request_listeners.append(self.handle_slack_message)
        
        # Prevent duplicate responses
        self.processed_messages: Set[str] = set()
        self.last_cleanup = datetime.now()
        
        # ChromaDB knowledge base connection
        self.chroma_client = chromadb.PersistentClient(
            path='/home/jeremylongshore/.bob_brain/chroma'
        )
        self.knowledge_collection = self.chroma_client.get_collection('bob_knowledge')
        
        # Business context
        self.business_context = {
            "company": "DiagnosticPro.io",
            "owner": "Jeremy Longshore", 
            "owner_user_id": None,  # Will be set when Jeremy messages
            "experience": "15 years business experience (BBI, trucking)",
        }
        
        # Smart conversation memory
        self.conversation_memory = {
            "recent_interactions": {},  # user_id -> last_interaction_time
            "greeting_count": {},       # user_id -> count of recent greetings
            "user_context": {}          # user_id -> known context about user
        }
        
        # Professional response patterns
        self.response_patterns = {
            "jeremy_casual_greeting": [
                "Hey Jeremy!",
                "Hello Jeremy.",
                "Hi Jeremy - what's on your mind?",
                "Good to hear from you, Jeremy."
            ],
            "jeremy_first_greeting": (
                "Hello Jeremy! Ready to tackle DiagnosticPro challenges today. "
                "What can I help you with?"
            ),
            "business_greeting": (
                "Hello! Bob here - your DiagnosticPro AI partner. "
                "How can I assist with the business today?"
            )
        }
        
        self.logger.info("🤖 Bob Unified v2 initialized with enhanced communication")
    
    def setup_logging(self):
        """Configure professional logging system"""
        os.makedirs('/home/jeremylongshore/bob-consolidation/logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/jeremylongshore/bob-consolidation/logs/bob_unified_v2.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BobUnifiedV2')
    
    def cleanup_processed_messages(self):
        """Clean up old processed messages to prevent memory buildup"""
        now = datetime.now()
        if now - self.last_cleanup > timedelta(minutes=30):
            # Keep only last 1000 messages to prevent memory issues
            if len(self.processed_messages) > 1000:
                # Convert to list, keep last 500, convert back to set
                recent_messages = list(self.processed_messages)[-500:]
                self.processed_messages = set(recent_messages)
            self.last_cleanup = now
            self.logger.info(f"🧹 Cleaned up message cache: {len(self.processed_messages)} recent messages retained")
    
    def is_duplicate_message(self, event: Dict[str, Any]) -> bool:
        """Check if this message has already been processed"""
        # Create unique message identifier
        message_id = f"{event.get('channel')}:{event.get('ts')}:{event.get('user')}:{event.get('text', '')[:50]}"
        
        if message_id in self.processed_messages:
            self.logger.warning(f"🔄 Duplicate message detected, skipping: {message_id}")
            return True
        
        # Add to processed messages
        self.processed_messages.add(message_id)
        return False
    
    def is_bot_message(self, event: Dict[str, Any]) -> bool:
        """Enhanced bot message detection to prevent self-responses"""
        # Check for bot_id (standard bot detection)
        if event.get("bot_id"):
            return True
        
        # Check if message is from our bot user (additional safety)
        user_id = event.get("user")
        if user_id and user_id.startswith("B"):  # Bot user IDs typically start with B
            return True
        
        # Check message patterns that indicate bot responses
        text = event.get("text", "").lower()
        bot_indicators = ["i'm bob", "bob here", "diagnosticpro ai partner"]
        if any(indicator in text for indicator in bot_indicators):
            self.logger.info("🤖 Detected potential bot message pattern, skipping")
            return True
        
        return False
    
    def update_conversation_memory(self, user_id: str, message: str):
        """Update smart conversation memory for context-aware responses"""
        now = datetime.now()
        
        # Update recent interactions
        self.conversation_memory["recent_interactions"][user_id] = now
        
        # Track greeting patterns
        if any(greeting in message.lower() for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            if user_id not in self.conversation_memory["greeting_count"]:
                self.conversation_memory["greeting_count"][user_id] = []
            
            # Add timestamp, keep only last 5 greetings
            self.conversation_memory["greeting_count"][user_id].append(now)
            self.conversation_memory["greeting_count"][user_id] = \
                self.conversation_memory["greeting_count"][user_id][-5:]
        
        # Identify Jeremy and set business context
        if "jeremy" in message.lower() or user_id == self.business_context.get("owner_user_id"):
            self.business_context["owner_user_id"] = user_id
            self.conversation_memory["user_context"][user_id] = {
                "is_owner": True,
                "name": "Jeremy",
                "relationship": "business_owner"
            }
    
    def get_recent_greeting_count(self, user_id: str) -> int:
        """Get count of recent greetings (last 24 hours)"""
        if user_id not in self.conversation_memory["greeting_count"]:
            return 0
        
        now = datetime.now()
        recent_greetings = [
            timestamp for timestamp in self.conversation_memory["greeting_count"][user_id]
            if now - timestamp < timedelta(hours=24)
        ]
        return len(recent_greetings)
    
    def is_jeremy(self, user_id: str) -> bool:
        """Check if user is Jeremy (business owner)"""
        return (user_id == self.business_context.get("owner_user_id") or 
                self.conversation_memory.get("user_context", {}).get(user_id, {}).get("is_owner", False))
    
    def query_knowledge_base(self, query: str, max_results: int = 2) -> List[Dict[str, Any]]:
        """Query ChromaDB knowledge base (reduced results for conciseness)"""
        try:
            results = self.knowledge_collection.query(
                query_texts=[query],
                n_results=max_results,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            knowledge_items = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0] if results['metadatas'][0] else [{}] * len(results['documents'][0]),
                results['distances'][0]
            )):
                # Only include highly relevant results
                relevance_score = 1.0 - distance
                if relevance_score > 0.3:  # Minimum relevance threshold
                    knowledge_items.append({
                        'content': doc,
                        'metadata': metadata,
                        'relevance_score': relevance_score,
                        'rank': i + 1
                    })
            
            return knowledge_items
            
        except Exception as e:
            self.logger.error(f"❌ Knowledge base query failed: {e}")
            return []
    
    def generate_professional_response(self, user_message: str, user_id: str) -> str:
        """
        Generate concise, professional responses with context awareness
        
        Key improvements:
        - Smart greeting handling for Jeremy
        - Concise business partner communication
        - Context-aware responses
        - Strategic business focus
        """
        message_lower = user_message.lower().strip()
        is_jeremy_user = self.is_jeremy(user_id)
        recent_greetings = self.get_recent_greeting_count(user_id)
        
        # Handle greetings intelligently
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            if is_jeremy_user:
                if recent_greetings <= 1:
                    # First greeting of the day - more context
                    return self.response_patterns["jeremy_first_greeting"]
                else:
                    # Recent greeting - keep it brief
                    import random
                    return random.choice(self.response_patterns["jeremy_casual_greeting"])
            else:
                # Business greeting for others
                return self.response_patterns["business_greeting"]
        
        # Query knowledge base for substantive questions
        knowledge_items = self.query_knowledge_base(user_message, max_results=1)
        
        # Generate contextual response
        if knowledge_items and knowledge_items[0]['relevance_score'] > 0.5:
            # High relevance - use knowledge directly
            content = knowledge_items[0]['content']
            if len(content) > 200:
                content = content[:200] + "..."
            
            if is_jeremy_user:
                return f"Based on what I know: {content}"
            else:
                return f"From the DiagnosticPro knowledge base: {content}"
        
        # Industry-specific responses
        elif any(keyword in message_lower for keyword in ["diagnostic", "repair", "overcharge", "shop", "vehicle"]):
            if is_jeremy_user:
                return (
                    "DiagnosticPro territory. What specific diagnostic challenge "
                    "are we tackling? I can help with procedures, cost analysis, or strategy."
                )
            else:
                return (
                    "DiagnosticPro specializes in protecting customers from repair overcharges "
                    "through accurate diagnostics. How can I assist with your diagnostic needs?"
                )
        
        # Business strategy questions
        elif any(keyword in message_lower for keyword in ["business", "strategy", "market", "competition", "growth"]):
            if is_jeremy_user:
                return (
                    "Let's talk strategy. With your BBI and trucking experience, "
                    "what aspect of the repair industry disruption are we focusing on?"
                )
            else:
                return (
                    "DiagnosticPro is disrupting the multi-billion repair industry. "
                    "What business aspect can I help you understand?"
                )
        
        # Default professional response
        else:
            if is_jeremy_user:
                return "What can I help you with today, Jeremy?"
            else:
                return "How can DiagnosticPro assist you with vehicle diagnostics or repair concerns?"
    
    def handle_slack_message(self, client, request):
        """
        Enhanced Slack message handler with duplicate prevention and smart responses
        """
        try:
            # Cleanup old messages periodically
            self.cleanup_processed_messages()
            
            if request.type == "events_api":
                event = request.payload.get("event", {})
                
                # Enhanced message validation
                if not (event.get("type") == "message" and event.get("text")):
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                # Prevent bot self-responses
                if self.is_bot_message(event):
                    self.logger.info("🤖 Skipping bot message")
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                # Prevent duplicate processing
                if self.is_duplicate_message(event):
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                user_text = event.get("text", "").strip()
                channel = event.get("channel")
                user_id = event.get("user")
                
                if not user_text or not channel or not user_id:
                    if hasattr(request, 'ack'):
                        request.ack()
                    return
                
                self.logger.info(f"📩 Processing message from {user_id}: '{user_text[:30]}...'")
                
                # Update conversation memory
                self.update_conversation_memory(user_id, user_text)
                
                # Generate professional response
                response = self.generate_professional_response(user_text, user_id)
                
                # Send response to Slack
                self.slack_client.chat_postMessage(
                    channel=channel,
                    text=response,
                    username="Bob - DiagnosticPro AI"
                )
                
                self.logger.info(f"✅ Sent response to {channel}: '{response[:50]}...'")
        
        except Exception as e:
            self.logger.error(f"❌ Slack message handling error: {e}")
            try:
                # Send error response to user
                if 'channel' in locals():
                    self.slack_client.chat_postMessage(
                        channel=channel,
                        text="I encountered an issue processing your request. Let me know if you need assistance."
                    )
            except:
                pass  # Avoid cascading errors
        
        finally:
            # Acknowledge request if method exists
            if hasattr(request, 'ack'):
                request.ack()
    
    def start_service(self):
        """Start enhanced Bob service with professional monitoring"""
        try:
            self.logger.info("🚀 Starting Bob Unified v2 with enhanced communication...")
            
            # Verify knowledge base connection
            total_knowledge = self.knowledge_collection.count()
            self.logger.info(f"📚 Connected to knowledge base: {total_knowledge} items available")
            
            # Start Slack connection
            self.socket_client.connect()
            self.logger.info("✅ Bob Unified v2 is now active and monitoring Slack!")
            
            # Keep service running with health monitoring
            while True:
                time.sleep(60)  # Health check every minute
                
                # Basic health check
                if not self.socket_client.is_connected():
                    self.logger.warning("⚠️ Slack connection lost - attempting reconnect...")
                    self.socket_client.connect()
                
                # Log periodic status
                active_conversations = len(self.conversation_memory["recent_interactions"])
                processed_count = len(self.processed_messages)
                self.logger.info(f"💪 Bob v2 Status: {active_conversations} active conversations, {processed_count} processed messages")
                
        except KeyboardInterrupt:
            self.logger.info("👋 Bob Unified v2 shutting down gracefully...")
        except Exception as e:
            self.logger.error(f"❌ Critical service error: {e}")
            raise
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        try:
            knowledge_count = self.knowledge_collection.count()
            slack_connected = getattr(self.socket_client, 'is_connected', lambda: True)()
            
            return {
                'service_status': 'active',
                'version': '2.0',
                'knowledge_base_items': knowledge_count,
                'slack_connection': 'connected' if slack_connected else 'disconnected',
                'active_conversations': len(self.conversation_memory["recent_interactions"]),
                'processed_messages': len(self.processed_messages),
                'jeremy_identified': bool(self.business_context.get("owner_user_id")),
                'improvements': [
                    'Duplicate response prevention',
                    'Smart conversation memory',
                    'Context-aware greetings',
                    'Concise professional communication',
                    'Enhanced bot message detection'
                ],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'service_status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """Main entry point for enhanced Bob Unified Agent"""
    # Get tokens from environment variables
    slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
    slack_app_token = os.getenv('SLACK_APP_TOKEN')
    
    if not slack_bot_token or not slack_app_token:
        print("❌ ERROR: Slack tokens not found in environment variables")
        print("Please ensure SLACK_BOT_TOKEN and SLACK_APP_TOKEN are set")
        return 1
    
    # Create logs directory if it doesn't exist
    os.makedirs('/home/jeremylongshore/bob-consolidation/logs', exist_ok=True)
    
    # Initialize and start enhanced Bob
    try:
        bob = BobUnifiedV2(slack_bot_token, slack_app_token)
        bob.start_service()
    except Exception as e:
        print(f"❌ Failed to start Bob Unified v2: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())