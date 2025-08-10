#!/usr/bin/env python3
"""
Bob Memory System with Graphiti Integration
Enhanced memory using knowledge graphs for better context understanding
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
import json

# Firestore for backup/compatibility
from google.cloud import firestore

# Neo4j and Graphiti for advanced memory
try:
    from graphiti_core import Graphiti
    from neo4j import GraphDatabase
    GRAPHITI_AVAILABLE = True
except ImportError:
    GRAPHITI_AVAILABLE = False
    print("⚠️ Graphiti not available. Install with: pip install graphiti-core neo4j")

class BobMemory:
    """
    Enhanced memory system for Bob using Graphiti + Firestore
    - Graphiti: Knowledge graph for relationships and facts
    - Firestore: Backup and compatibility layer
    """
    
    def __init__(self, project_id='diagnostic-pro-mvp', neo4j_uri=None, neo4j_user=None, neo4j_password=None):
        """Initialize dual memory system"""
        self.logger = logging.getLogger('BobMemory')
        
        # Firestore for backup/compatibility
        self.firestore = None
        try:
            self.firestore = firestore.Client(
                project=project_id,
                database='bob-brain'
            )
            self.logger.info("✅ Connected to Firestore for memory backup")
        except Exception as e:
            self.logger.warning(f"Firestore not available: {e}")
        
        # Graphiti for advanced memory (if available)
        self.graphiti = None
        if GRAPHITI_AVAILABLE:
            try:
                # Use environment variables or defaults
                uri = neo4j_uri or os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
                user = neo4j_user or os.environ.get('NEO4J_USER', 'neo4j')
                password = neo4j_password or os.environ.get('NEO4J_PASSWORD', 'bobpassword')
                
                # Initialize Graphiti
                self.graphiti = Graphiti(
                    neo4j_uri=uri,
                    neo4j_user=user,
                    neo4j_password=password
                )
                self.logger.info("✅ Connected to Graphiti knowledge graph")
            except Exception as e:
                self.logger.warning(f"Graphiti not available: {e}")
                self.graphiti = None
        
        # In-memory cache for quick access
        self.cache = {
            'user_profiles': {},
            'recent_facts': [],
            'relationships': {}
        }
        
        self.logger.info(f"BobMemory initialized - Firestore: {bool(self.firestore)}, Graphiti: {bool(self.graphiti)}")
    
    def remember(self, user_id: str, content: str, context: Optional[Dict] = None) -> bool:
        """
        Store knowledge in both systems
        Creates facts, entities, and relationships from content
        """
        try:
            episode = {
                "content": content,
                "user": user_id,
                "context": context or {},
                "timestamp": datetime.now().isoformat(),
                "episode_id": self._generate_id(content)
            }
            
            # Store in Graphiti (knowledge graph)
            if self.graphiti:
                try:
                    # Graphiti extracts entities and relationships automatically
                    self.graphiti.add_episode(
                        content=content,
                        source=user_id,
                        metadata=context
                    )
                    self.logger.info(f"📊 Stored in knowledge graph: {content[:50]}...")
                except Exception as e:
                    self.logger.error(f"Graphiti storage failed: {e}")
            
            # Store in Firestore (backup)
            if self.firestore:
                try:
                    doc_ref = self.firestore.collection('memory_episodes').add(episode)
                    self.logger.info(f"💾 Backed up to Firestore: {doc_ref[1].id}")
                except Exception as e:
                    self.logger.error(f"Firestore storage failed: {e}")
            
            # Update cache
            self._update_cache(user_id, content, context)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remember: {e}")
            return False
    
    def recall(self, query: str, user_id: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """
        Intelligent recall using knowledge graph
        Searches for relevant facts and relationships
        """
        results = []
        
        # Search Graphiti knowledge graph
        if self.graphiti:
            try:
                # Search with context
                graph_results = self.graphiti.search(
                    query=query,
                    user_context=user_id,
                    num_results=limit
                )
                
                # Format results
                for result in graph_results:
                    results.append({
                        'content': result.get('content', ''),
                        'relevance': result.get('score', 0),
                        'source': 'graphiti',
                        'metadata': result.get('metadata', {}),
                        'relationships': result.get('relationships', [])
                    })
                    
                self.logger.info(f"📊 Found {len(results)} results in knowledge graph")
                
            except Exception as e:
                self.logger.error(f"Graphiti search failed: {e}")
        
        # Fallback to Firestore if needed
        if not results and self.firestore:
            try:
                # Simple keyword search in Firestore
                episodes = self.firestore.collection('memory_episodes').where('user', '==', user_id).limit(limit).get()
                
                for doc in episodes:
                    data = doc.to_dict()
                    if query.lower() in data.get('content', '').lower():
                        results.append({
                            'content': data.get('content', ''),
                            'relevance': 0.5,  # Basic relevance
                            'source': 'firestore',
                            'metadata': data.get('context', {})
                        })
                        
            except Exception as e:
                self.logger.error(f"Firestore search failed: {e}")
        
        # Check cache as last resort
        if not results:
            results = self._search_cache(query, user_id)
        
        return results[:limit]
    
    def get_user_profile(self, user_id: str) -> Dict:
        """
        Build complete user understanding from knowledge graph
        Returns all facts, preferences, and relationships about a user
        """
        profile = {
            'user_id': user_id,
            'facts': [],
            'preferences': [],
            'relationships': [],
            'conversation_style': None,
            'interests': []
        }
        
        # Get from Graphiti
        if self.graphiti:
            try:
                # Get all facts about the user
                user_facts = self.graphiti.get_entity_facts(user_id)
                profile['facts'] = user_facts
                
                # Get relationships
                relationships = self.graphiti.get_entity_relationships(user_id)
                profile['relationships'] = relationships
                
                # Extract preferences and interests
                for fact in user_facts:
                    content = fact.get('content', '').lower()
                    if 'prefer' in content or 'like' in content:
                        profile['preferences'].append(fact)
                    if 'interest' in content or 'hobby' in content:
                        profile['interests'].append(content)
                        
            except Exception as e:
                self.logger.error(f"Failed to get user profile from Graphiti: {e}")
        
        # Merge with cache
        if user_id in self.cache['user_profiles']:
            cached = self.cache['user_profiles'][user_id]
            profile['facts'].extend(cached.get('facts', []))
            profile['preferences'].extend(cached.get('preferences', []))
        
        return profile
    
    def find_connections(self, entity1: str, entity2: str) -> List[Dict]:
        """
        Find connections between two entities in the knowledge graph
        Useful for understanding relationships and context
        """
        if not self.graphiti:
            return []
        
        try:
            # Find paths between entities
            connections = self.graphiti.find_paths(entity1, entity2, max_depth=3)
            
            return [{
                'path': conn.get('path', []),
                'relationship_types': conn.get('relationships', []),
                'strength': conn.get('strength', 0)
            } for conn in connections]
            
        except Exception as e:
            self.logger.error(f"Failed to find connections: {e}")
            return []
    
    def get_temporal_context(self, user_id: str, time_window_hours: int = 24) -> List[Dict]:
        """
        Get recent context for a user within a time window
        Helps maintain conversation continuity
        """
        cutoff_time = datetime.now().timestamp() - (time_window_hours * 3600)
        recent_context = []
        
        if self.firestore:
            try:
                # Query recent episodes
                episodes = (self.firestore.collection('memory_episodes')
                          .where('user', '==', user_id)
                          .order_by('timestamp', direction=firestore.Query.DESCENDING)
                          .limit(20)
                          .get())
                
                for doc in episodes:
                    data = doc.to_dict()
                    timestamp = datetime.fromisoformat(data.get('timestamp', ''))
                    if timestamp.timestamp() > cutoff_time:
                        recent_context.append({
                            'content': data.get('content', ''),
                            'timestamp': data.get('timestamp', ''),
                            'context': data.get('context', {})
                        })
                        
            except Exception as e:
                self.logger.error(f"Failed to get temporal context: {e}")
        
        return recent_context
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID for content"""
        return hashlib.md5(f"{content}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
    
    def _update_cache(self, user_id: str, content: str, context: Optional[Dict]):
        """Update in-memory cache"""
        # Update user profile cache
        if user_id not in self.cache['user_profiles']:
            self.cache['user_profiles'][user_id] = {
                'facts': [],
                'preferences': []
            }
        
        self.cache['user_profiles'][user_id]['facts'].append({
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'context': context
        })
        
        # Keep cache size manageable
        if len(self.cache['user_profiles'][user_id]['facts']) > 100:
            self.cache['user_profiles'][user_id]['facts'] = \
                self.cache['user_profiles'][user_id]['facts'][-50:]
        
        # Update recent facts
        self.cache['recent_facts'].append({
            'user': user_id,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 100 facts
        if len(self.cache['recent_facts']) > 100:
            self.cache['recent_facts'] = self.cache['recent_facts'][-100:]
    
    def _search_cache(self, query: str, user_id: Optional[str]) -> List[Dict]:
        """Search in-memory cache"""
        results = []
        query_lower = query.lower()
        
        # Search user-specific facts
        if user_id and user_id in self.cache['user_profiles']:
            for fact in self.cache['user_profiles'][user_id]['facts']:
                if query_lower in fact['content'].lower():
                    results.append({
                        'content': fact['content'],
                        'relevance': 0.3,
                        'source': 'cache',
                        'metadata': fact.get('context', {})
                    })
        
        # Search recent facts
        for fact in self.cache['recent_facts']:
            if query_lower in fact['content'].lower():
                if not user_id or fact['user'] == user_id:
                    results.append({
                        'content': fact['content'],
                        'relevance': 0.2,
                        'source': 'cache',
                        'metadata': {}
                    })
        
        return results
    
    def get_stats(self) -> Dict:
        """Get memory system statistics"""
        stats = {
            'firestore_available': bool(self.firestore),
            'graphiti_available': bool(self.graphiti),
            'cached_users': len(self.cache['user_profiles']),
            'recent_facts': len(self.cache['recent_facts']),
            'total_cache_size': sum(len(p['facts']) for p in self.cache['user_profiles'].values())
        }
        
        if self.graphiti:
            try:
                # Get graph statistics
                graph_stats = self.graphiti.get_statistics()
                stats['graph_nodes'] = graph_stats.get('nodes', 0)
                stats['graph_relationships'] = graph_stats.get('relationships', 0)
            except:
                pass
        
        return stats


# Test the memory system
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🧠 Testing Bob Memory System")
    print("=" * 50)
    
    # Initialize memory
    memory = BobMemory()
    
    # Test remembering
    print("\n📝 Testing remember function...")
    memory.remember("jeremy", "I prefer morning meetings", {"type": "preference"})
    memory.remember("jeremy", "My birthday is May 15", {"type": "personal"})
    memory.remember("jeremy", "I'm working on DiagnosticPro", {"type": "project"})
    
    # Test recall
    print("\n🔍 Testing recall function...")
    results = memory.recall("birthday", "jeremy")
    for result in results:
        print(f"  Found: {result['content'][:50]}... (relevance: {result['relevance']})")
    
    # Test user profile
    print("\n👤 Testing user profile...")
    profile = memory.get_user_profile("jeremy")
    print(f"  Facts: {len(profile['facts'])}")
    print(f"  Preferences: {len(profile['preferences'])}")
    
    # Show stats
    print("\n📊 Memory Statistics:")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Memory system test complete!")