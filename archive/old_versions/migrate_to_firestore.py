#!/usr/bin/env python3
"""
Safe Migration Script: ChromaDB to Firestore
Ensures no duplicates and preserves MVP3 data integrity
"""

import os
import sys
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Set, Optional
import chromadb
from google.cloud import firestore
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/jeremylongshore/bobs-brain/logs/migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ChromaToFirestoreMigration')

class SafeMigrationManager:
    """
    Safely migrates ChromaDB data to Firestore with duplicate prevention
    and MVP3 data protection
    """
    
    def __init__(self):
        """Initialize migration manager with safety checks"""
        self.project_id = 'diagnostic-pro-mvp'
        self.database_id = 'bob-brain'  # Use bob-brain database
        self.firestore_db = None
        self.chroma_client = None
        self.migrated_hashes: Set[str] = set()
        self.migration_stats = {
            'total_documents': 0,
            'migrated_new': 0,
            'skipped_duplicates': 0,
            'errors': 0,
            'mvp3_collections_checked': []
        }
        
    def connect_firestore(self) -> bool:
        """Connect to Firestore with safety checks"""
        try:
            self.firestore_db = firestore.Client(
                project=self.project_id,
                database=self.database_id
            )
            logger.info(f"✅ Connected to Firestore: {self.project_id}/{self.database_id}")
            
            # Verify MVP3 collections are intact
            mvp3_collections = ['diagnostic_submissions', 'users', 'sessions', 'payments']
            for collection_name in mvp3_collections:
                try:
                    # Just check if collection exists, don't modify
                    docs = self.firestore_db.collection(collection_name).limit(1).get()
                    self.migration_stats['mvp3_collections_checked'].append(collection_name)
                    logger.info(f"✓ MVP3 collection verified: {collection_name}")
                except Exception as e:
                    logger.warning(f"MVP3 collection not accessible: {collection_name}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to Firestore: {e}")
            return False
    
    def connect_chromadb(self) -> bool:
        """Connect to ChromaDB"""
        try:
            chroma_path = '/home/jeremylongshore/bobs-brain/chroma_data'
            if not os.path.exists(chroma_path):
                logger.error(f"ChromaDB path not found: {chroma_path}")
                return False
                
            self.chroma_client = chromadb.PersistentClient(path=chroma_path)
            logger.info(f"✅ Connected to ChromaDB at {chroma_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to ChromaDB: {e}")
            return False
    
    def generate_content_hash(self, content: str, metadata: Dict = None) -> str:
        """Generate unique hash for content to detect duplicates"""
        hash_input = content
        if metadata:
            # Include key metadata in hash to ensure uniqueness
            hash_input += str(metadata.get('source', ''))
            hash_input += str(metadata.get('type', ''))
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def check_duplicate_in_firestore(self, content_hash: str) -> bool:
        """Check if document already exists in Firestore"""
        try:
            # Check in shared_knowledge collection
            existing_docs = (self.firestore_db.collection('shared_knowledge')
                           .where('content_hash', '==', content_hash)
                           .limit(1)
                           .get())
            return len(list(existing_docs)) > 0
        except Exception:
            return False
    
    def migrate_collection(self, collection_name: str) -> Dict:
        """Migrate a single ChromaDB collection to Firestore"""
        stats = {
            'collection': collection_name,
            'total': 0,
            'migrated': 0,
            'duplicates': 0,
            'errors': 0
        }
        
        try:
            # Get ChromaDB collection
            try:
                collection = self.chroma_client.get_collection(collection_name)
            except:
                logger.warning(f"Collection not found: {collection_name}")
                return stats
            
            # Get all documents from ChromaDB
            all_data = collection.get()
            documents = all_data.get('documents', [])
            metadatas = all_data.get('metadatas', [])
            ids = all_data.get('ids', [])
            embeddings = all_data.get('embeddings', [])
            
            stats['total'] = len(documents)
            logger.info(f"📊 Found {stats['total']} documents in {collection_name}")
            
            # Prepare Firestore batch
            batch = self.firestore_db.batch()
            batch_count = 0
            
            for i, (doc_id, content, metadata) in enumerate(zip(ids, documents, metadatas)):
                try:
                    # Generate content hash for duplicate detection
                    content_hash = self.generate_content_hash(content, metadata)
                    
                    # Check if already migrated (in memory)
                    if content_hash in self.migrated_hashes:
                        stats['duplicates'] += 1
                        logger.debug(f"Skip: Already migrated (memory check) - {doc_id[:20]}...")
                        continue
                    
                    # Check if exists in Firestore
                    if self.check_duplicate_in_firestore(content_hash):
                        stats['duplicates'] += 1
                        self.migrated_hashes.add(content_hash)
                        logger.debug(f"Skip: Already in Firestore - {doc_id[:20]}...")
                        continue
                    
                    # Prepare document for Firestore
                    firestore_doc = {
                        'original_id': doc_id,
                        'content': content,
                        'content_hash': content_hash,
                        'metadata': metadata or {},
                        'source': 'chromadb_migration',
                        'original_collection': collection_name,
                        'migrated_at': datetime.now(),
                        'ai_agent': 'bob',
                        'knowledge_type': metadata.get('type', 'general') if metadata else 'general',
                        'embedding_available': embeddings is not None and i < len(embeddings)
                    }
                    
                    # Store embedding if available (as metadata, not vector)
                    if embeddings and i < len(embeddings):
                        # Store embedding dimension info only, not the full vector
                        firestore_doc['embedding_info'] = {
                            'dimensions': len(embeddings[i]) if embeddings[i] else 0,
                            'model': 'chromadb_default'
                        }
                    
                    # Use safe document ID (Firestore has restrictions)
                    safe_doc_id = f"chroma_{collection_name}_{content_hash[:16]}"
                    
                    # Add to batch
                    doc_ref = self.firestore_db.collection('shared_knowledge').document(safe_doc_id)
                    batch.set(doc_ref, firestore_doc, merge=False)  # merge=False to ensure new document
                    
                    batch_count += 1
                    stats['migrated'] += 1
                    self.migrated_hashes.add(content_hash)
                    
                    # Commit batch every 100 documents (Firestore limit is 500)
                    if batch_count >= 100:
                        batch.commit()
                        logger.info(f"  💾 Committed batch: {stats['migrated']} documents migrated")
                        batch = self.firestore_db.batch()
                        batch_count = 0
                        
                except Exception as e:
                    stats['errors'] += 1
                    logger.error(f"Error migrating document {doc_id}: {e}")
                    continue
            
            # Commit remaining documents
            if batch_count > 0:
                batch.commit()
                logger.info(f"  💾 Final batch committed: {batch_count} documents")
            
            logger.info(f"✅ Collection {collection_name} migration complete:")
            logger.info(f"   Total: {stats['total']}, Migrated: {stats['migrated']}, Duplicates: {stats['duplicates']}, Errors: {stats['errors']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to migrate collection {collection_name}: {e}")
            stats['errors'] = stats['total']
        
        return stats
    
    def create_migration_report(self) -> Dict:
        """Create detailed migration report"""
        report = {
            'migration_id': f"migration_{datetime.now().isoformat()}",
            'timestamp': datetime.now(),
            'source': 'chromadb',
            'destination': 'firestore_thebrain',
            'stats': self.migration_stats,
            'mvp3_protected': True,
            'duplicate_prevention': True,
            'status': 'completed' if self.migration_stats['errors'] == 0 else 'completed_with_errors'
        }
        
        # Store report in Firestore
        try:
            self.firestore_db.collection('system_metrics').add(report)
            logger.info("📊 Migration report saved to Firestore")
        except Exception as e:
            logger.error(f"Failed to save migration report: {e}")
        
        return report
    
    def perform_migration(self) -> bool:
        """Execute the complete migration process"""
        logger.info("🚀 Starting ChromaDB to Firestore Migration")
        logger.info("=" * 60)
        
        # Step 1: Connect to both databases
        if not self.connect_firestore():
            logger.error("Cannot proceed without Firestore connection")
            return False
        
        if not self.connect_chromadb():
            logger.error("Cannot proceed without ChromaDB connection")
            return False
        
        # Step 2: Get all ChromaDB collections
        try:
            collections = self.chroma_client.list_collections()
            logger.info(f"📚 Found {len(collections)} collections in ChromaDB")
        except Exception as e:
            logger.error(f"Failed to list ChromaDB collections: {e}")
            return False
        
        # Step 3: Migrate each collection
        for collection in collections:
            collection_name = collection.name
            logger.info(f"\n📦 Migrating collection: {collection_name}")
            
            stats = self.migrate_collection(collection_name)
            
            # Update global stats
            self.migration_stats['total_documents'] += stats['total']
            self.migration_stats['migrated_new'] += stats['migrated']
            self.migration_stats['skipped_duplicates'] += stats['duplicates']
            self.migration_stats['errors'] += stats['errors']
        
        # Step 4: Create and save migration report
        report = self.create_migration_report()
        
        # Step 5: Display final summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 MIGRATION COMPLETE - SUMMARY:")
        logger.info(f"  Total Documents Processed: {self.migration_stats['total_documents']}")
        logger.info(f"  New Documents Migrated: {self.migration_stats['migrated_new']}")
        logger.info(f"  Duplicates Skipped: {self.migration_stats['skipped_duplicates']}")
        logger.info(f"  Errors: {self.migration_stats['errors']}")
        logger.info(f"  MVP3 Collections Protected: {', '.join(self.migration_stats['mvp3_collections_checked'])}")
        logger.info("=" * 60)
        
        return self.migration_stats['errors'] == 0
    
    def verify_migration(self) -> bool:
        """Verify migration integrity"""
        logger.info("\n🔍 Verifying Migration Integrity...")
        
        try:
            # Count documents in Firestore shared_knowledge
            firestore_docs = self.firestore_db.collection('shared_knowledge').where('source', '==', 'chromadb_migration').get()
            firestore_count = len(list(firestore_docs))
            
            logger.info(f"✓ Firestore documents migrated: {firestore_count}")
            logger.info(f"✓ Expected documents: {self.migration_stats['migrated_new']}")
            
            if firestore_count == self.migration_stats['migrated_new']:
                logger.info("✅ Migration verification PASSED")
                return True
            else:
                logger.warning(f"⚠️ Count mismatch: Expected {self.migration_stats['migrated_new']}, Found {firestore_count}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return False


def main():
    """Main migration entry point"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║    ChromaDB → Firestore Migration Tool               ║
    ║    Safe migration with duplicate prevention          ║
    ║    MVP3 data protection enabled                      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Check for confirmation
    print("⚠️  This will migrate all ChromaDB data to Firestore.")
    print("   - Duplicates will be automatically skipped")
    print("   - MVP3 data will NOT be modified")
    print("   - All data will go to 'shared_knowledge' collection")
    print("")
    
    response = input("Do you want to proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        return
    
    # Create migration manager and run
    manager = SafeMigrationManager()
    success = manager.perform_migration()
    
    if success:
        # Verify the migration
        manager.verify_migration()
        print("\n✅ Migration completed successfully!")
        print("Next step: Update Bob to use Firestore instead of ChromaDB")
    else:
        print("\n⚠️ Migration completed with errors. Check logs for details.")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())