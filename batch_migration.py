#!/usr/bin/env python3
"""
Efficient batch migration to Firestore
"""

import json
from google.cloud import firestore
from datetime import datetime

def batch_migrate_knowledge():
    """Migrate knowledge data in batches"""

    print("🚀 Starting batch migration...")

    # Initialize Firestore
    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Load merged data
    with open("/home/jeremylongshore/bob_brain_backup/merged_data.json") as f:
        merged_data = json.load(f)

    print(f"📊 Migrating {len(merged_data)} knowledge items in batches...")

    # Batch settings
    batch_size = 500  # Firestore batch limit
    success_count = 0
    error_count = 0

    # Process in batches
    for i in range(0, len(merged_data), batch_size):
        batch_items = merged_data[i:i + batch_size]

        try:
            # Create batch
            batch = client.batch()

            for item in batch_items:
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
                batch.set(doc_ref, doc_data)

            # Commit batch
            batch.commit()

            success_count += len(batch_items)
            print(f"✅ Batch {i//batch_size + 1}: Migrated {len(batch_items)} items (Total: {success_count})")

        except Exception as e:
            print(f"❌ Batch {i//batch_size + 1} failed: {e}")
            error_count += len(batch_items)

    print(f"🎉 Knowledge migration complete: {success_count} success, {error_count} errors")
    return success_count, error_count

def migrate_conversations():
    """Migrate conversations"""

    print("💬 Migrating conversations...")

    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Load SQLite data
    with open("/home/jeremylongshore/bob_brain_backup/bob_memory_export.json") as f:
        sqlite_data = json.load(f)

    conversations = sqlite_data['tables']['conversations']['data']
    print(f"📊 Migrating {len(conversations)} conversations...")

    success_count = 0
    for conv in conversations:
        try:
            doc_data = {
                "timestamp": conv.get("timestamp"),
                "message": conv.get("message"),
                "response": conv.get("response"),
                "context": conv.get("context"),
                "model": conv.get("model"),
                "migrated_at": firestore.SERVER_TIMESTAMP
            }

            client.collection("bob_conversations").add(doc_data)
            success_count += 1

        except Exception as e:
            print(f"❌ Error migrating conversation: {e}")

    print(f"✅ Conversations: {success_count} migrated")
    return success_count

def migrate_automation_and_insights():
    """Migrate automation rules and insights"""

    print("⚙️  Migrating automation and insights...")

    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Automation rules
    with open("/home/jeremylongshore/bob_brain_backup/automation_export.json") as f:
        automation_data = json.load(f)

    rules = automation_data['tables']['automation_rules']['data']
    automation_count = 0

    for rule in rules:
        try:
            doc_data = {
                "rule_id": rule.get("id"),
                "name": rule.get("name"),
                "trigger_condition": rule.get("trigger"),
                "action_type": rule.get("action"),
                "configuration": rule.get("config"),
                "active": rule.get("active", True),
                "migrated_at": firestore.SERVER_TIMESTAMP
            }

            client.collection("automation_rules").add(doc_data)
            automation_count += 1

        except Exception as e:
            print(f"❌ Error migrating rule: {e}")

    # Smart insights
    with open("/home/jeremylongshore/bob_brain_backup/smart_insights_export.json") as f:
        insights_data = json.load(f)

    insights = insights_data['tables']['insights']['data']
    insights_count = 0

    for insight in insights:
        try:
            doc_data = {
                "insight_id": insight.get("id"),
                "type": insight.get("type"),
                "title": insight.get("title"),
                "description": insight.get("description"),
                "confidence": insight.get("confidence", 0.0),
                "importance": insight.get("importance"),
                "migrated_at": firestore.SERVER_TIMESTAMP
            }

            client.collection("insights").add(doc_data)
            insights_count += 1

        except Exception as e:
            print(f"❌ Error migrating insight: {e}")

    print(f"✅ Automation rules: {automation_count}, Insights: {insights_count}")
    return automation_count, insights_count

def validate_migration():
    """Quick validation"""

    print("🔍 Validating migration...")

    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    collections = ["knowledge", "bob_conversations", "automation_rules", "insights"]
    results = {}

    for collection_name in collections:
        try:
            # Get approximate count (first 1000 docs)
            docs = list(client.collection(collection_name).limit(1000).stream())
            count = len(docs)
            results[collection_name] = count
            print(f"✅ {collection_name}: {count} documents")
        except Exception as e:
            print(f"❌ {collection_name}: Error - {e}")
            results[collection_name] = 0

    return results

def main():
    """Main migration"""

    print("🚀 BOB'S FIRESTORE MIGRATION - BATCH MODE")
    print("=" * 50)

    # Migrate knowledge (largest dataset)
    knowledge_success, knowledge_errors = batch_migrate_knowledge()

    # Migrate conversations
    conv_count = migrate_conversations()

    # Migrate automation and insights
    auto_count, insights_count = migrate_automation_and_insights()

    # Validate
    results = validate_migration()

    # Summary
    print(f"\n📊 MIGRATION SUMMARY")
    print("=" * 30)
    print(f"Knowledge: {knowledge_success} migrated, {knowledge_errors} errors")
    print(f"Conversations: {conv_count} migrated")
    print(f"Automation: {auto_count} migrated")
    print(f"Insights: {insights_count} migrated")

    print(f"\n🔍 VALIDATION RESULTS:")
    for collection, count in results.items():
        print(f"   {collection}: {count} documents")

    # Check if migration was successful
    total_expected = 1925 + 13 + 2 + 3  # knowledge + conversations + automation + insights
    total_actual = sum(results.values())

    if total_actual >= total_expected * 0.95:  # 95% threshold
        print(f"\n🎉 Migration SUCCESSFUL! {total_actual}/{total_expected}")
        return True
    else:
        print(f"\n⚠️  Migration needs review: {total_actual}/{total_expected}")
        return False

if __name__ == "__main__":
    success = main()
