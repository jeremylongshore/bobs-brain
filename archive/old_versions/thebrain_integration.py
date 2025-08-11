#!/usr/bin/env python3
"""
Bob's Integration with "thebrain" Firestore Database
Enables Bob to store and retrieve knowledge from the unified cloud database
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Try to import Google Cloud Firestore
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False
    print("⚠️ Google Cloud Firestore not installed. Install with: pip install google-cloud-firestore")

class ThebrainIntegration:
    """
    Integration layer between Bob and "thebrain" Firestore database
    """
    
    def __init__(self, project_id: str = 'diagnostic-pro-mvp', database_id: str = 'thebrain'):
        """
        Initialize connection to "thebrain" database
        """
        self.project_id = project_id
        self.database_id = database_id
        self.db = None
        self.logger = logging.getLogger('ThebrainIntegration')
        
        if FIRESTORE_AVAILABLE:
            try:
                self.db = firestore.Client(
                    project=self.project_id,
                    database=self.database_id
                )
                self.logger.info(f"✅ Connected to 'thebrain' database in project {self.project_id}")
            except Exception as e:
                self.logger.error(f"❌ Failed to connect to thebrain: {e}")
                self.db = None
        else:
            self.logger.warning("Firestore not available - using local mode only")
    
    def migrate_chromadb_to_thebrain(self, chroma_collection):
        """
        Migrate Bob's ChromaDB knowledge to "thebrain" Firestore
        """
        if not self.db:
            self.logger.error("Cannot migrate - not connected to thebrain")
            return False
        
        try:
            # Get all documents from ChromaDB
            self.logger.info("📚 Starting migration from ChromaDB to thebrain...")
            
            # Get ChromaDB data
            all_data = chroma_collection.get()
            documents = all_data.get('documents', [])
            metadatas = all_data.get('metadatas', [])
            ids = all_data.get('ids', [])
            
            # Prepare batch write
            batch = self.db.batch()
            collection_ref = self.db.collection('shared_knowledge')
            
            migrated_count = 0
            for i, (doc_id, document, metadata) in enumerate(zip(ids, documents, metadatas)):
                # Create Firestore document
                knowledge_doc = {
                    'original_id': doc_id,
                    'content': document,
                    'metadata': metadata or {},
                    'source': 'chromadb_migration',
                    'migrated_at': datetime.now(),
                    'ai_agent': 'bob',
                    'knowledge_type': metadata.get('type', 'general') if metadata else 'general'
                }
                
                # Add to batch
                doc_ref = collection_ref.document(f"chroma_{doc_id}")
                batch.set(doc_ref, knowledge_doc)
                
                migrated_count += 1
                
                # Commit batch every 100 documents (Firestore limit is 500)
                if migrated_count % 100 == 0:
                    batch.commit()
                    batch = self.db.batch()
                    self.logger.info(f"  📦 Migrated {migrated_count} documents...")
            
            # Commit remaining documents
            if migrated_count % 100 != 0:
                batch.commit()
            
            self.logger.info(f"✅ Successfully migrated {migrated_count} knowledge items to thebrain")
            
            # Store migration metadata
            migration_doc = {
                'migration_id': f"migration_{datetime.now().isoformat()}",
                'source': 'chromadb',
                'destination': 'thebrain',
                'documents_migrated': migrated_count,
                'timestamp': datetime.now(),
                'status': 'completed'
            }
            self.db.collection('system_metrics').add(migration_doc)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Migration failed: {e}")
            return False
    
    def store_conversation(self, user_id: str, message: str, response: str, channel: str = None):
        """
        Store Bob's conversation in "thebrain"
        """
        if not self.db:
            self.logger.warning("Not connected to thebrain - conversation not stored")
            return None
        
        try:
            conversation_doc = {
                'user_id': user_id,
                'user_message': message,
                'bob_response': response,
                'channel': channel,
                'timestamp': datetime.now(),
                'ai_agent': 'bob',
                'conversation_id': hashlib.md5(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()
            }
            
            doc_ref = self.db.collection('bob_conversations').add(conversation_doc)
            self.logger.info(f"💬 Stored conversation in thebrain: {doc_ref[1].id}")
            return doc_ref[1].id
            
        except Exception as e:
            self.logger.error(f"Failed to store conversation: {e}")
            return None
    
    def query_shared_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Query shared knowledge from "thebrain"
        """
        if not self.db:
            self.logger.warning("Not connected to thebrain - returning empty results")
            return []
        
        try:
            # Search in shared knowledge collection
            knowledge_ref = self.db.collection('shared_knowledge')
            
            # For now, get recent documents (Firestore doesn't have built-in text search)
            # In production, you'd use Firestore extensions or external search
            results = knowledge_ref.limit(limit).get()
            
            knowledge_items = []
            for doc in results:
                data = doc.to_dict()
                data['id'] = doc.id
                knowledge_items.append(data)
            
            return knowledge_items
            
        except Exception as e:
            self.logger.error(f"Failed to query knowledge: {e}")
            return []
    
    def get_diagnostic_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent diagnostic submissions for Bob to learn from
        """
        if not self.db:
            return []
        
        try:
            # Get recent diagnostic submissions
            diag_ref = self.db.collection('diagnostic_submissions')
            results = diag_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit).get()
            
            insights = []
            for doc in results:
                data = doc.to_dict()
                # Anonymize personal data
                if 'full_name' in data:
                    data['full_name'] = 'REDACTED'
                if 'email' in data:
                    data['email'] = 'REDACTED@example.com'
                if 'phone' in data:
                    data['phone'] = 'XXX-XXX-XXXX'
                
                insights.append({
                    'problem': data.get('problem_description', ''),
                    'service': data.get('selected_service', ''),
                    'equipment': data.get('equipment_type', ''),
                    'timestamp': data.get('created_at', '')
                })
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Failed to get diagnostic insights: {e}")
            return []
    
    def sync_with_chromadb(self, chroma_collection):
        """
        Two-way sync between ChromaDB and "thebrain"
        """
        if not self.db:
            self.logger.warning("Cannot sync - not connected to thebrain")
            return False
        
        try:
            # Get latest from thebrain
            knowledge_ref = self.db.collection('shared_knowledge')
            cloud_docs = knowledge_ref.where('ai_agent', '!=', 'bob').limit(100).get()
            
            # Add new knowledge to ChromaDB
            new_items = 0
            for doc in cloud_docs:
                data = doc.to_dict()
                
                # Add to ChromaDB if not from Bob
                try:
                    chroma_collection.add(
                        ids=[doc.id],
                        documents=[data.get('content', '')],
                        metadatas=[data.get('metadata', {})]
                    )
                    new_items += 1
                except:
                    pass  # Document might already exist
            
            if new_items > 0:
                self.logger.info(f"📥 Synced {new_items} new knowledge items from thebrain")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Sync failed: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get connection status and statistics
        """
        status = {
            'connected': self.db is not None,
            'project': self.project_id,
            'database': self.database_id,
            'firestore_available': FIRESTORE_AVAILABLE
        }
        
        if self.db:
            try:
                # Get collection counts
                collections = ['shared_knowledge', 'bob_conversations', 'diagnostic_submissions']
                counts = {}
                
                for collection in collections:
                    # Note: This is expensive for large collections
                    # In production, maintain counters separately
                    docs = self.db.collection(collection).limit(1).get()
                    counts[collection] = 'available' if docs else 'empty'
                
                status['collections'] = counts
                status['status'] = 'operational'
            except:
                status['status'] = 'connection_error'
        else:
            status['status'] = 'not_connected'
        
        return status


# Integration function for Bob Unified
def enhance_bob_with_thebrain(bob_instance):
    """
    Enhance Bob Unified with "thebrain" capabilities
    """
    try:
        # Create thebrain integration
        thebrain = ThebrainIntegration()
        
        # Add to Bob instance
        bob_instance.thebrain = thebrain
        
        # Override or enhance Bob's methods
        original_generate_response = bob_instance.generate_professional_response
        
        def enhanced_generate_response(user_message: str, user_id: str) -> str:
            # Get original response
            response = original_generate_response(user_message, user_id)
            
            # Store conversation in thebrain
            if hasattr(bob_instance, 'thebrain'):
                bob_instance.thebrain.store_conversation(
                    user_id=user_id,
                    message=user_message,
                    response=response,
                    channel='slack'
                )
            
            return response
        
        bob_instance.generate_professional_response = enhanced_generate_response
        
        logging.info("✅ Bob enhanced with thebrain integration")
        return True
        
    except Exception as e:
        logging.error(f"Failed to enhance Bob with thebrain: {e}")
        return False


if __name__ == "__main__":
    # Test the integration
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("🧠 Testing thebrain Integration")
    print("=" * 50)
    
    integration = ThebrainIntegration()
    status = integration.get_status()
    
    print(f"Connection Status: {status['status']}")
    print(f"Firestore Available: {status['firestore_available']}")
    print(f"Project: {status['project']}")
    print(f"Database: {status['database']}")
    
    if status['connected']:
        print("\n✅ Successfully connected to thebrain!")
        print("Collections:", status.get('collections', {}))
    else:
        print("\n⚠️ Not connected to thebrain")
        print("To connect, ensure:")
        print("1. Google Cloud Firestore is installed: pip install google-cloud-firestore")
        print("2. Authentication is configured: gcloud auth application-default login")
        print("3. The 'thebrain' database exists in your project")