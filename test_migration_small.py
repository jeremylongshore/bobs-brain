#!/usr/bin/env python3
"""
Test migration with small dataset
"""

import json
from google.cloud import firestore

def test_small_migration():
    """Test migration with just a few items"""

    print("🧪 Testing small migration...")

    # Initialize Firestore
    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Load merged data
    with open("/home/jeremylongshore/bob_brain_backup/merged_data.json") as f:
        merged_data = json.load(f)

    # Take just first 10 items
    test_items = merged_data[:10]
    print(f"📊 Testing with {len(test_items)} items...")

    # Migrate test items
    success_count = 0
    error_count = 0

    for item in test_items:
        try:
            doc_data = {
                "content": item["content"],
                "embedding": item["embedding"],
                "metadata": item["metadata"],
                "source": item["metadata"].get("source", "unknown"),
                "created_at": firestore.SERVER_TIMESTAMP,
                "migrated_at": firestore.SERVER_TIMESTAMP
            }

            # Use the item ID as document ID
            doc_ref = client.collection("knowledge").document(str(item["id"]))
            doc_ref.set(doc_data)

            success_count += 1
            print(f"✅ Migrated item {item['id']}")

        except Exception as e:
            print(f"❌ Error migrating item {item['id']}: {e}")
            error_count += 1

    print(f"\n📊 Test Results: {success_count} success, {error_count} errors")

    # Test read back
    print("🔍 Testing read back...")
    docs = list(client.collection("knowledge").limit(5).stream())
    print(f"✅ Successfully read {len(docs)} documents from Firestore")

    return success_count > 0

if __name__ == "__main__":
    success = test_small_migration()
    if success:
        print("🎉 Small migration test passed!")
    else:
        print("❌ Small migration test failed")
