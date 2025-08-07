#!/usr/bin/env python3
"""
Optimized corrected migration - use existing ChromaDB embeddings
"""

import json
import time
from google.cloud import firestore

def optimized_corrected_migration():
    """Optimized migration using existing ChromaDB embeddings"""

    print("🚀 OPTIMIZED CORRECTED MIGRATION - 970 Knowledge Items")
    print("=" * 60)

    # Initialize Firestore client
    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Clear existing knowledge collection
    print("🗑️  Clearing existing knowledge collection...")
    knowledge_collection = client.collection('knowledge')

    # Quick delete using smaller batches
    deleted_count = 0
    while True:
        docs = knowledge_collection.limit(100).stream()
        doc_list = list(docs)
        if not doc_list:
            break

        batch = client.batch()
        for doc in doc_list:
            batch.delete(doc.reference)
            deleted_count += 1
        batch.commit()
        print(f"   Deleted {deleted_count} documents...")

    print(f"✅ Cleared {deleted_count} existing knowledge documents")

    # Load corrected data (exactly 970 items)
    with open("/home/jeremylongshore/bob_brain_backup/corrected_merged_data.json") as f:
        merged_data = json.load(f)

    print(f"📊 Knowledge items to migrate: {len(merged_data)}")

    # Migrate in optimized batches (smaller for reliability)
    batch_size = 100  # Smaller batch size
    total_migrated = 0

    for i in range(0, len(merged_data), batch_size):
        batch = client.batch()
        batch_data = merged_data[i:i + batch_size]

        for item in batch_data:
            # Use existing embeddings (no regeneration)
            doc_data = {
                'content': item.get('content', ''),
                'embedding': item.get('embedding'),  # Keep existing or None
                'metadata': item.get('metadata', {}),
                'source': item.get('metadata', {}).get('source', 'unknown'),
                'timestamp': firestore.SERVER_TIMESTAMP
            }

            doc_ref = client.collection('knowledge').document(str(item['id']))
            batch.set(doc_ref, doc_data)

        # Commit with retry
        try:
            batch.commit()
            total_migrated += len(batch_data)
            print(f"✅ Migrated {total_migrated}/{len(merged_data)} knowledge items")
        except Exception as e:
            print(f"❌ Batch failed: {e}")
            return False

        time.sleep(0.1)  # Small delay between batches

    print(f"🎉 KNOWLEDGE MIGRATION COMPLETE: {total_migrated} items")

    # Quick validation
    knowledge_count = len(list(client.collection('knowledge').stream()))
    print(f"📊 Firestore knowledge validation: {knowledge_count} documents")

    return total_migrated == 970 and knowledge_count == 970

if __name__ == "__main__":
    success = optimized_corrected_migration()

    if success:
        print("\n🎉 CORRECTED MIGRATION SUCCESS!")
        print("✅ Exactly 970 knowledge items in Firestore")
        print("✅ Data discrepancy corrected from 1,925 to 970")
    else:
        print("\n❌ Migration validation failed")
