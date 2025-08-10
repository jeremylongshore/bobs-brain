#!/usr/bin/env python3
"""
Bob Unified Agent - Single Source of Truth Implementation
Consolidates all Bob functionality into one professional AI assistant
"""

import os
import time
import logging
import chromadb
from typing import Optional, List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from datetime import datetime

class BobUnified:
    """
    Unified Bob AI Agent for DiagnosticPro and Business Operations
    
    Professional repair industry expert with comprehensive knowledge base
    integration and robust Slack communication capabilities.
    """
    
    def __init__(self, slack_bot_token: str, slack_app_token: str):
        """Initialize Bob with Slack integration and knowledge base"""
        self.setup_logging()
        
        # Slack configuration
        self.slack_client = WebClient(token=slack_bot_token)
        self.socket_client = SocketModeClient(app_token=slack_app_token)
        self.socket_client.socket_mode_request_listeners.append(self.handle_slack_message)
        
        # ChromaDB knowledge base connection
        self.chroma_client = chromadb.PersistentClient(
            path='/home/jeremylongshore/.bob_brain/chroma'
        )
        self.knowledge_collection = self.chroma_client.get_collection('bob_knowledge')
        
        # Business context
        self.business_context = {
            "company": "DiagnosticPro.io",
            "industry": "Vehicle Repair & Diagnostics",
            "mission": "Protect customers from shop overcharges through accurate diagnostics",
            "owner": "Jeremy Longshore",
            "experience": "15 years business experience (BBI, trucking)",
            "target_market": "Multi-billion repair industry disruption"
        }
        
        # Track conversation state
        self.conversation_history = {}
        
        self.logger.info("🤖 Bob Unified Agent initialized successfully")
    
    def setup_logging(self):
        """Configure professional logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/jeremylongshore/bob-consolidation/logs/bob_unified.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BobUnified')
    
    def query_knowledge_base(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Query ChromaDB knowledge base with professional context awareness
        
        Args:
            query: User's question or topic
            max_results: Maximum number of relevant results to return
            
        Returns:
            List of relevant knowledge entries with metadata
        """
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
                knowledge_items.append({
                    'content': doc,
                    'metadata': metadata,
                    'relevance_score': 1.0 - distance,  # Higher score = more relevant
                    'rank': i + 1
                })
            
            self.logger.info(f"📚 Retrieved {len(knowledge_items)} knowledge items for query: '{query[:50]}...'")
            return knowledge_items
            
        except Exception as e:
            self.logger.error(f"❌ Knowledge base query failed: {e}")
            return []
    
    def generate_professional_response(self, user_message: str, channel_context: str = None) -> str:
        """
        Generate professional business response combining knowledge base and context
        
        Args:
            user_message: User's question or request
            channel_context: Slack channel context if available
            
        Returns:
            Professional, contextual response
        """
        # Query knowledge base for relevant information
        knowledge_items = self.query_knowledge_base(user_message, max_results=3)
        
        # Start building response with professional tone
        response_parts = []
        
        if knowledge_items and knowledge_items[0]['relevance_score'] > 0.7:
            # High relevance - use knowledge-based response
            best_match = knowledge_items[0]
            content = best_match['content']
            
            # Craft professional response based on knowledge
            if len(content) > 400:
                content = content[:400] + "..."
            
            response_parts.append(f"Based on my knowledge: {content}")
            
            # Add additional context if available
            if len(knowledge_items) > 1 and knowledge_items[1]['relevance_score'] > 0.6:
                additional = knowledge_items[1]['content'][:200]
                response_parts.append(f"\nAdditionally: {additional}...")
        
        elif "diagnostic" in user_message.lower() or "repair" in user_message.lower():
            # Industry-specific response
            response_parts.append(
                "As a diagnostic industry expert, I can help you with vehicle diagnostics, "
                "repair cost analysis, and protecting customers from overcharges. "
                f"At {self.business_context['company']}, we're revolutionizing the repair industry "
                "through accurate diagnostics and transparent pricing."
            )
        
        elif any(keyword in user_message.lower() for keyword in ["hello", "hi", "hey", "greeting"]):
            # Professional greeting
            response_parts.append(
                f"Hello! I'm Bob, your AI business partner for {self.business_context['company']}. "
                f"With {self.business_context['experience']}, I'm here to help with diagnostics, "
                "business strategy, and industry insights. How can I assist you today?"
            )
        
        else:
            # Generic professional response
            response_parts.append(
                "I'm Bob, your professional AI assistant specializing in vehicle diagnostics "
                "and repair industry operations. I have access to comprehensive knowledge "
                "about diagnostic procedures, business operations, and industry best practices. "
                "What specific area can I help you with?"
            )
        
        # Combine response parts
        final_response = "\n".join(response_parts)
        
        # Log response generation
        self.logger.info(f"💬 Generated response ({len(final_response)} chars) for: '{user_message[:30]}...'")
        
        return final_response
    
    def handle_slack_message(self, client, request):
        """
        Handle incoming Slack messages with professional processing
        
        Args:
            client: Slack socket mode client
            request: Slack request object
        """
        try:
            if request.type == "events_api":
                event = request.payload.get("event", {})
                
                if (event.get("type") == "message" and 
                    event.get("text") and 
                    not event.get("bot_id")):
                    
                    user_text = event.get("text", "").strip()
                    channel = event.get("channel")
                    user_id = event.get("user")
                    
                    if not user_text:
                        request.ack()
                        return
                    
                    self.logger.info(f"📩 Received message from {user_id}: '{user_text[:50]}...'")
                    
                    # Generate professional response
                    response = self.generate_professional_response(user_text, channel)
                    
                    # Send response to Slack
                    self.slack_client.chat_postMessage(
                        channel=channel,
                        text=response,
                        username="Bob - DiagnosticPro AI"
                    )
                    
                    # Update conversation history
                    if channel not in self.conversation_history:
                        self.conversation_history[channel] = []
                    
                    self.conversation_history[channel].append({
                        'timestamp': datetime.now().isoformat(),
                        'user_message': user_text,
                        'bot_response': response[:100] + "..." if len(response) > 100 else response
                    })
                    
                    self.logger.info(f"✅ Sent response to {channel}: '{response[:50]}...'")
        
        except Exception as e:
            self.logger.error(f"❌ Slack message handling error: {e}")
            try:
                # Send error response to user
                if 'channel' in locals():
                    self.slack_client.chat_postMessage(
                        channel=channel,
                        text="I apologize, but I encountered an error processing your request. "
                             "Please try again or contact support if the issue persists."
                    )
            except:
                pass  # Avoid cascading errors
        
        finally:
            request.ack()
    
    def start_service(self):
        """Start Bob's Slack service with professional monitoring"""
        try:
            self.logger.info("🚀 Starting Bob Unified Service...")
            
            # Verify knowledge base connection
            total_knowledge = self.knowledge_collection.count()
            self.logger.info(f"📚 Connected to knowledge base: {total_knowledge} items available")
            
            # Start Slack connection
            self.socket_client.connect()
            self.logger.info("✅ Bob Unified is now active and monitoring Slack!")
            
            # Keep service running with health monitoring
            while True:
                time.sleep(30)  # Health check every 30 seconds
                
                # Basic health check
                if not self.socket_client.is_connected():
                    self.logger.warning("⚠️ Slack connection lost - attempting reconnect...")
                    self.socket_client.connect()
                
        except KeyboardInterrupt:
            self.logger.info("👋 Bob Unified shutting down gracefully...")
        except Exception as e:
            self.logger.error(f"❌ Critical service error: {e}")
            raise
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report for monitoring"""
        try:
            knowledge_count = self.knowledge_collection.count()
            slack_connected = self.socket_client.is_connected() if hasattr(self.socket_client, 'is_connected') else True
            
            return {
                'service_status': 'active',
                'knowledge_base_items': knowledge_count,
                'slack_connection': 'connected' if slack_connected else 'disconnected',
                'conversation_channels': len(self.conversation_history),
                'business_context': self.business_context,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'service_status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """Main entry point for Bob Unified Agent"""
    # Get tokens from environment variables (secure approach)
    slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
    slack_app_token = os.getenv('SLACK_APP_TOKEN')
    
    if not slack_bot_token or not slack_app_token:
        print("❌ ERROR: Slack tokens not found in environment variables")
        print("Please ensure SLACK_BOT_TOKEN and SLACK_APP_TOKEN are set")
        return 1
    
    # Create logs directory if it doesn't exist
    os.makedirs('/home/jeremylongshore/bob-consolidation/logs', exist_ok=True)
    
    # Initialize and start Bob Unified
    try:
        bob = BobUnified(slack_bot_token, slack_app_token)
        bob.start_service()
    except Exception as e:
        print(f"❌ Failed to start Bob Unified: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())