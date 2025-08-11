#!/usr/bin/env python3
"""
Bob Base Model - Enhanced with Graphiti Memory
The foundation for all future agent specializations
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the existing Bob
from bob_firestore import BobFirestore

# Import enhanced memory
from bob_memory import BobMemory

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BobBase')


class BobBase(BobFirestore):
    """
    Enhanced Bob with Graphiti memory and modular architecture
    Inherits from BobFirestore to keep all existing functionality
    """
    
    def __init__(self, specialization: Optional[str] = None):
        """Initialize enhanced Bob with memory and specialization"""
        # Initialize parent (BobFirestore)
        super().__init__()
        
        # ENHANCEMENT: Advanced memory system
        self.enhanced_memory = BobMemory()
        logger.info("✅ Enhanced memory system initialized")
        
        # ENHANCEMENT: Specialization system
        self.specialization = specialization or "general"
        self.tools = {}
        self.load_specialization()
        
        # ENHANCEMENT: Track enhanced capabilities
        self.capabilities = {
            'memory': 'graphiti',
            'models': ['vertex-ai', 'gemini-2.0'],
            'specialization': self.specialization,
            'tools': list(self.tools.keys())
        }
        
        logger.info(f"✅ BobBase initialized with specialization: {self.specialization}")
    
    def load_specialization(self):
        """Load tools and configs for specialization"""
        if self.specialization == "research":
            logger.info("Loading research specialization...")
            # Will add research tools later
            self.tools['web_search'] = self._web_search_tool
            self.tools['deep_analysis'] = self._deep_analysis_tool
            
        elif self.specialization == "assistant":
            logger.info("Loading assistant specialization...")
            # Will add assistant tools later
            self.tools['schedule'] = self._schedule_tool
            self.tools['reminder'] = self._reminder_tool
            
        elif self.specialization == "diagnostic":
            logger.info("Loading diagnostic specialization...")
            # Specific to DiagnosticPro
            self.tools['analyze_repair'] = self._analyze_repair_tool
            self.tools['verify_quote'] = self._verify_quote_tool
    
    def process_message_enhanced(self, message: str, user_id: str, channel: Optional[str] = None) -> str:
        """
        Enhanced message processing with Graphiti memory
        This wraps the original process_message with memory enhancements
        """
        try:
            # 1. Remember the incoming message
            context = {
                'channel': channel,
                'timestamp': datetime.now().isoformat(),
                'specialization': self.specialization
            }
            self.enhanced_memory.remember(user_id, f"User said: {message}", context)
            
            # 2. Get user profile from knowledge graph
            user_profile = self.enhanced_memory.get_user_profile(user_id)
            
            # 3. Recall relevant past interactions
            relevant_history = self.enhanced_memory.recall(message, user_id, limit=3)
            
            # 4. Check for specialized processing
            specialized_response = self.specialized_processing(message, user_id)
            if specialized_response:
                # Remember the specialized response
                self.enhanced_memory.remember(user_id, f"Bob responded: {specialized_response}", context)
                return specialized_response
            
            # 5. Build enhanced context
            enhanced_context = self._build_enhanced_context(message, user_profile, relevant_history)
            
            # 6. Generate response using parent's method with enhanced context
            # We'll modify the query to include context
            enriched_message = self._enrich_message(message, enhanced_context)
            response = self.generate_response(enriched_message, user_id)
            
            # 7. Remember the response
            self.enhanced_memory.remember(user_id, f"Bob responded: {response}", context)
            
            # 8. Update conversation memory (parent's system)
            self.update_conversation_memory(user_id, message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in enhanced processing: {e}")
            # Fallback to parent's processing
            return self.generate_response(message, user_id)
    
    def specialized_processing(self, message: str, user_id: str) -> Optional[str]:
        """
        Hook for specialized behavior based on specialization
        Override this in specialized Bobs
        """
        message_lower = message.lower()
        
        # Check if any specialized tools should handle this
        for tool_name, tool_func in self.tools.items():
            if tool_name in message_lower:
                logger.info(f"Using specialized tool: {tool_name}")
                return tool_func(message, user_id)
        
        return None
    
    def _build_enhanced_context(self, message: str, user_profile: Dict, history: List[Dict]) -> Dict:
        """Build enhanced context from memory"""
        context = {
            'user_facts': user_profile.get('facts', [])[:5],  # Top 5 facts
            'user_preferences': user_profile.get('preferences', []),
            'user_interests': user_profile.get('interests', []),
            'relevant_history': []
        }
        
        # Add relevant history
        for item in history[:3]:
            context['relevant_history'].append({
                'content': item.get('content', '')[:200],
                'relevance': item.get('relevance', 0)
            })
        
        return context
    
    def _enrich_message(self, message: str, context: Dict) -> str:
        """Enrich the message with context for better AI response"""
        enriched = message
        
        # Add context if we have relevant history
        if context.get('relevant_history'):
            enriched += "\n\n[Context from previous conversations:"
            for hist in context['relevant_history']:
                if hist['relevance'] > 0.5:
                    enriched += f"\n- {hist['content'][:100]}..."
            enriched += "]"
        
        # Add user preferences if relevant
        if context.get('user_preferences'):
            enriched += "\n\n[User preferences:"
            for pref in context['user_preferences'][:3]:
                enriched += f"\n- {pref}"
            enriched += "]"
        
        return enriched
    
    def clone(self, new_specialization: str) -> 'BobBase':
        """Create a new Bob with different specialization"""
        logger.info(f"Cloning Bob with specialization: {new_specialization}")
        return BobBase(specialization=new_specialization)
    
    # Placeholder tool methods
    def _web_search_tool(self, message: str, user_id: str) -> str:
        """Placeholder for web search tool"""
        return f"Research Bob would search the web for: {message}"
    
    def _deep_analysis_tool(self, message: str, user_id: str) -> str:
        """Placeholder for deep analysis tool"""
        return f"Research Bob would deeply analyze: {message}"
    
    def _schedule_tool(self, message: str, user_id: str) -> str:
        """Placeholder for schedule tool"""
        return f"Assistant Bob would help with scheduling: {message}"
    
    def _reminder_tool(self, message: str, user_id: str) -> str:
        """Placeholder for reminder tool"""
        return f"Assistant Bob would set a reminder for: {message}"
    
    def _analyze_repair_tool(self, message: str, user_id: str) -> str:
        """Placeholder for repair analysis tool"""
        return f"Diagnostic Bob would analyze this repair: {message}"
    
    def _verify_quote_tool(self, message: str, user_id: str) -> str:
        """Placeholder for quote verification tool"""
        return f"Diagnostic Bob would verify this quote: {message}"
    
    def get_capabilities(self) -> Dict:
        """Return current Bob's capabilities"""
        return {
            **self.capabilities,
            'memory_stats': self.enhanced_memory.get_stats(),
            'health': self.health_check()
        }
    
    # Override the parent's handle_slack_event to use enhanced processing
    def handle_slack_event(self, client, request):
        """Override to use enhanced processing"""
        try:
            # Most of the logic is same as parent
            self.cleanup_old_messages()
            
            if request.type == "events_api":
                client.ack(request.envelope_id)
                
                event = request.payload.get("event", {})
                
                if event.get("type") != "message" or not event.get("text"):
                    return
                
                if self.is_bot_message(event):
                    return
                
                if self.is_duplicate(event):
                    return
                
                user_text = event.get("text", "").strip()
                channel = event.get("channel")
                user_id = event.get("user")
                
                if not all([user_text, channel, user_id]):
                    return
                
                logger.info(f"📩 Enhanced Bob processing message from {user_id}: {user_text[:50]}...")
                
                # USE ENHANCED PROCESSING HERE
                response = self.process_message_enhanced(user_text, user_id, channel)
                
                # Send response
                self.slack_client.chat_postMessage(
                    channel=channel,
                    text=response,
                    thread_ts=event.get('thread_ts')
                )
                
                logger.info(f"✅ Enhanced response sent: {response[:50]}...")
            else:
                client.ack(request.envelope_id)
            
        except Exception as e:
            logger.error(f"❌ Event handling error: {e}")
            try:
                client.ack(request.envelope_id)
            except:
                pass


# Create specialized Bob classes
class ResearchBob(BobBase):
    """Bob specialized for research and data gathering"""
    
    def __init__(self):
        super().__init__(specialization="research")
        logger.info("🔬 Research Bob initialized")
    
    def specialized_processing(self, message: str, user_id: str) -> Optional[str]:
        """Research-specific processing"""
        message_lower = message.lower()
        
        if "research" in message_lower or "find information" in message_lower:
            # Use memory to see what we already know
            existing = self.enhanced_memory.recall(message, user_id)
            
            if existing:
                summary = "Based on my knowledge:\n"
                for item in existing[:3]:
                    summary += f"- {item['content'][:100]}...\n"
                return summary
            else:
                return "I'll research that for you. (Research tools coming soon)"
        
        return super().specialized_processing(message, user_id)


class AssistantBob(BobBase):
    """Bob specialized for personal assistance"""
    
    def __init__(self):
        super().__init__(specialization="assistant")
        logger.info("📅 Assistant Bob initialized")
    
    def specialized_processing(self, message: str, user_id: str) -> Optional[str]:
        """Assistant-specific processing"""
        message_lower = message.lower()
        
        if "remind me" in message_lower or "schedule" in message_lower:
            # Store as a reminder in memory
            self.enhanced_memory.remember(user_id, f"Reminder: {message}", {"type": "reminder"})
            return f"I'll remember that for you: {message}"
        
        return super().specialized_processing(message, user_id)


class DiagnosticBob(BobBase):
    """Bob specialized for DiagnosticPro"""
    
    def __init__(self):
        super().__init__(specialization="diagnostic")
        logger.info("🔧 Diagnostic Bob initialized")
    
    def specialized_processing(self, message: str, user_id: str) -> Optional[str]:
        """Diagnostic-specific processing"""
        message_lower = message.lower()
        
        if "repair" in message_lower or "diagnostic" in message_lower or "quote" in message_lower:
            # Use specialized knowledge
            return "I can help analyze that repair quote. (Diagnostic tools coming soon)"
        
        return super().specialized_processing(message, user_id)


def main():
    """Test the enhanced Bob"""
    print("""
    ╔══════════════════════════════════════╗
    ║     BOB BASE MODEL v1.0               ║
    ║   Enhanced with Graphiti Memory       ║
    ║   Foundation for All Agents           ║
    ╚══════════════════════════════════════╝
    """)
    
    # Test different specializations
    print("\n🧪 Testing Bob specializations...")
    
    # Create base Bob
    base_bob = BobBase()
    print(f"✅ Base Bob created: {base_bob.get_capabilities()['specialization']}")
    
    # Create specialized Bobs
    research_bob = ResearchBob()
    print(f"✅ Research Bob created: {research_bob.get_capabilities()['specialization']}")
    
    assistant_bob = AssistantBob()
    print(f"✅ Assistant Bob created: {assistant_bob.get_capabilities()['specialization']}")
    
    diagnostic_bob = DiagnosticBob()
    print(f"✅ Diagnostic Bob created: {diagnostic_bob.get_capabilities()['specialization']}")
    
    # Test memory
    print("\n🧠 Testing enhanced memory...")
    base_bob.enhanced_memory.remember("test_user", "I love Python programming", {"type": "preference"})
    results = base_bob.enhanced_memory.recall("Python", "test_user")
    print(f"Memory recall: {len(results)} results found")
    
    print("\n✅ Bob Base Model ready for deployment!")


if __name__ == "__main__":
    main()