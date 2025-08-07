#!/usr/bin/env python3
"""
Corrected Firestore migration with exactly 970 knowledge items
"""

import json
import time
from google.cloud import firestore
from sentence_transformers import SentenceTransformer

def migrate_corrected_data():
    """Migrate corrected data to Firestore"""

    print("🚀 CORRECTED FIRESTORE MIGRATION - 970 Knowledge Items")
    print("=" * 60)

    # Initialize Firestore client
    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Clear existing knowledge collection first
    print("🗑️  Clearing existing knowledge collection...")
    knowledge_collection = client.collection('knowledge')

    # Delete existing documents in batches
    deleted_count = 0
    docs = knowledge_collection.stream()
    batch = client.batch()
    batch_count = 0

    for doc in docs:
        batch.delete(doc.reference)
        batch_count += 1
        deleted_count += 1

        if batch_count >= 500:
            batch.commit()
            batch = client.batch()
            batch_count = 0
            print(f"   Deleted {deleted_count} existing documents...")

    # Commit any remaining deletes
    if batch_count > 0:
        batch.commit()

    print(f"✅ Cleared {deleted_count} existing knowledge documents")

    # Load corrected merged data
    with open("/home/jeremylongshore/bob_brain_backup/corrected_merged_data.json") as f:
        merged_data = json.load(f)

    print(f"📊 Corrected knowledge items to migrate: {len(merged_data)}")

    # Initialize sentence transformer for missing embeddings
    print("🤖 Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Migrate knowledge data in batches
    batch_size = 500  # Firestore batch limit
    batch_count = 0
    total_migrated = 0

    for i in range(0, len(merged_data), batch_size):
        batch = client.batch()
        batch_data = merged_data[i:i + batch_size]

        for item in batch_data:
            # Generate embedding if missing
            embedding = item.get('embedding')
            if embedding is None and item.get('content'):
                embedding = model.encode(item['content']).tolist()

            # Prepare document data
            doc_data = {
                'content': item.get('content', ''),
                'embedding': embedding,
                'metadata': item.get('metadata', {}),
                'timestamp': firestore.SERVER_TIMESTAMP,
                'migrated_at': time.time()
            }

            # Use item ID as document ID
            doc_ref = client.collection('knowledge').document(str(item['id']))
            batch.set(doc_ref, doc_data)

        # Commit batch
        try:
            batch.commit()
            total_migrated += len(batch_data)
            batch_count += 1
            print(f"✅ Batch {batch_count}: {total_migrated}/{len(merged_data)} knowledge items migrated")
        except Exception as e:
            print(f"❌ Batch {batch_count} failed: {e}")
            return False

    print(f"🎉 CORRECTED KNOWLEDGE MIGRATION COMPLETE: {total_migrated} items")

    # Migrate other collections (conversations, automation, insights) - these are unchanged
    print("\n📂 Migrating other collections...")

    # Conversations
    with open("/home/jeremylongshore/bob_brain_backup/bob_memory_export.json") as f:
        sqlite_data = json.load(f)

    conversations = sqlite_data['tables']['conversations']['data']
    batch = client.batch()
    for conv in conversations:
        doc_ref = client.collection('bob_conversations').document(str(conv['id']))
        conv_data = {
            'question': conv.get('question', ''),
            'answer': conv.get('answer', ''),
            'timestamp': conv.get('timestamp', ''),
            'migrated_at': time.time()
        }
        batch.set(doc_ref, conv_data)

    batch.commit()
    print(f"✅ Conversations migrated: {len(conversations)} items")

    # Automation rules
    with open("/home/jeremylongshore/bob_brain_backup/automation_export.json") as f:
        automation_data = json.load(f)

    rules = automation_data['tables']['automation_rules']['data']
    batch = client.batch()
    for rule in rules:
        doc_ref = client.collection('automation_rules').document(str(rule['id']))
        rule_data = {
            'trigger': rule.get('trigger', ''),
            'action': rule.get('action', ''),
            'enabled': rule.get('enabled', True),
            'created_at': rule.get('created_at', ''),
            'migrated_at': time.time()
        }
        batch.set(doc_ref, rule_data)

    batch.commit()
    print(f"✅ Automation rules migrated: {len(rules)} items")

    # Smart insights
    with open("/home/jeremylongshore/bob_brain_backup/smart_insights_export.json") as f:
        insights_data = json.load(f)

    insights = insights_data['tables']['insights']['data']
    batch = client.batch()
    for insight in insights:
        doc_ref = client.collection('insights').document(str(insight['id']))
        insight_data = {
            'category': insight.get('category', ''),
            'insight': insight.get('insight', ''),
            'confidence': insight.get('confidence', 0.0),
            'created_at': insight.get('created_at', ''),
            'migrated_at': time.time()
        }
        batch.set(doc_ref, insight_data)

    batch.commit()
    print(f"✅ Smart insights migrated: {len(insights)} items")

    # Final summary
    total_items = total_migrated + len(conversations) + len(rules) + len(insights)
    print(f"\n🎯 CORRECTED MIGRATION SUMMARY")
    print("=" * 35)
    print(f"Knowledge items: {total_migrated}")
    print(f"Conversations: {len(conversations)}")
    print(f"Automation rules: {len(rules)}")
    print(f"Smart insights: {len(insights)}")
    print(f"TOTAL ITEMS: {total_items}")

    return total_migrated == 970  # Validate exactly 970 knowledge items

if __name__ == "__main__":
    success = migrate_corrected_data()

    if success:
        print("\n🎉 CORRECTED MIGRATION SUCCESS!")
        print("✅ Exactly 970 knowledge items migrated to Firestore")
        print("✅ All other collections migrated successfully")
    else:
        print("\n❌ CORRECTED MIGRATION FAILED!")
        print("❌ Validation error - knowledge count incorrect")
