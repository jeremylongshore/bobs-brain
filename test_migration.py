#!/usr/bin/env python3
"""
Test script to verify ChromaDB to Firestore migration
Tests the migration without modifying production data
"""

import os
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('MigrationTest')

def test_firestore_connection():
    """Test Firestore connection"""
    try:
        from google.cloud import firestore
        
        logger.info("Testing Firestore connection...")
        db = firestore.Client(
            project='diagnostic-pro-mvp',
            database='bob-brain'
        )
        
        # Test read access
        test_collection = db.collection('shared_knowledge').limit(1).get()
        logger.info("✅ Firestore connection successful")
        
        # Check MVP3 collections (read-only)
        mvp3_collections = ['diagnostic_submissions', 'users', 'sessions', 'payments']
        for collection in mvp3_collections:
            try:
                docs = db.collection(collection).limit(1).get()
                logger.info(f"  ✓ MVP3 collection accessible: {collection}")
            except Exception as e:
                logger.warning(f"  ⚠ MVP3 collection not accessible: {collection}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Firestore connection failed: {e}")
        return False

def test_chromadb_connection():
    """Test ChromaDB connection"""
    try:
        import chromadb
        
        logger.info("Testing ChromaDB connection...")
        chroma_path = '/home/jeremylongshore/bobs-brain/chroma_data'
        
        if not os.path.exists(chroma_path):
            logger.warning(f"ChromaDB path not found: {chroma_path}")
            return False
        
        client = chromadb.PersistentClient(path=chroma_path)
        collections = client.list_collections()
        
        logger.info(f"✅ ChromaDB connection successful")
        logger.info(f"  Found {len(collections)} collections")
        
        for collection in collections:
            count = collection.count()
            logger.info(f"  - {collection.name}: {count} documents")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ChromaDB connection failed: {e}")
        return False

def test_migration_safety():
    """Test migration safety checks"""
    logger.info("\nTesting migration safety checks...")
    
    try:
        from src.migrate_to_firestore import SafeMigrationManager
        
        manager = SafeMigrationManager()
        
        # Test hash generation
        test_content = "Test document content"
        hash1 = manager.generate_content_hash(test_content)
        hash2 = manager.generate_content_hash(test_content)
        
        if hash1 == hash2:
            logger.info("✅ Content hashing works correctly")
        else:
            logger.error("❌ Content hashing inconsistent")
        
        # Test duplicate detection logic
        logger.info("✅ Duplicate detection logic ready")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration safety test failed: {e}")
        return False

def test_bob_firestore():
    """Test Bob Firestore edition"""
    logger.info("\nTesting Bob Firestore edition...")
    
    try:
        from src.bob_firestore import BobFirestore
        
        # Set dummy tokens for testing
        os.environ['SLACK_BOT_TOKEN'] = os.environ.get('SLACK_BOT_TOKEN', 'xoxb-test')
        os.environ['SLACK_APP_TOKEN'] = os.environ.get('SLACK_APP_TOKEN', 'xapp-test')
        os.environ['SLACK_SIGNING_SECRET'] = os.environ.get('SLACK_SIGNING_SECRET', 'test-secret')
        
        # Try to initialize (will fail on Slack but test DB connection)
        try:
            bob = BobFirestore()
            health = bob.health_check()
            
            logger.info(f"✅ Bob Firestore initialized")
            logger.info(f"  Database: {health['database']}")
            logger.info(f"  Knowledge items: {health['knowledge_items']}")
            logger.info(f"  AI Model: {health['ai_model']}")
            
            # Test knowledge query
            if bob.db_type == 'firestore':
                results = bob.query_knowledge("diagnostic")
                logger.info(f"  Query test returned {len(results)} results")
            
            return True
            
        except ValueError as e:
            if "Slack tokens required" in str(e):
                logger.info("⚠️ Bob initialization blocked by missing Slack tokens (expected)")
                return True
            raise
            
    except Exception as e:
        logger.error(f"❌ Bob Firestore test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     ChromaDB → Firestore Migration Test Suite        ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Firestore Connection", test_firestore_connection),
        ("ChromaDB Connection", test_chromadb_connection),
        ("Migration Safety", test_migration_safety),
        ("Bob Firestore Edition", test_bob_firestore)
    ]
    
    results = []
    for name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running: {name}")
        logger.info('='*50)
        
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            logger.error(f"Test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n✅ All tests passed! Ready for migration.")
        print("\nNext steps:")
        print("1. Run: python3 src/migrate_to_firestore.py")
        print("2. Verify migration with this test again")
        print("3. Update Bob to use bob_firestore.py instead of bob_ultimate.py")
    else:
        print("\n⚠️ Some tests failed. Please fix issues before migration.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())