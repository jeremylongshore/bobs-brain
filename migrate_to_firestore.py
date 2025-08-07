#!/usr/bin/env python3
"""
Migrate Bob's data to Firestore
"""

import json
import os
from google.cloud import firestore
from datetime import datetime

def initialize_firestore():
    """Initialize Firestore client"""
    try:
        # Initialize Firestore client
        client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")
        print("✅ Firestore client initialized")
        return client
    except Exception as e:
        print(f"❌ Error initializing Firestore: {e}")
        return None

def migrate_knowledge_data(firestore_client):
    """Migrate merged knowledge data to Firestore"""

    print("🚀 Migrating knowledge data to Firestore...")

    # Load merged data
    with open("/home/jeremylongshore/bob_brain_backup/merged_data.json") as f:
        merged_data = json.load(f)

    print(f"📊 Migrating {len(merged_data)} knowledge items...")

    # Migrate to Firestore /knowledge collection
    success_count = 0
    error_count = 0

    for i, item in enumerate(merged_data):
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
            doc_ref = firestore_client.collection("knowledge").document(str(item["id"]))
            doc_ref.set(doc_data)

            success_count += 1

            if (i + 1) % 100 == 0:
                print(f"   📈 Migrated {i + 1}/{len(merged_data)} items...")

        except Exception as e:
            print(f"❌ Error migrating item {item['id']}: {e}")
            error_count += 1

    print(f"✅ Knowledge migration complete: {success_count} success, {error_count} errors")
    return success_count, error_count

def migrate_conversations(firestore_client):
    """Migrate conversations to Firestore"""

    print("💬 Migrating conversations to Firestore...")

    # Load SQLite data
    with open("/home/jeremylongshore/bob_brain_backup/bob_memory_export.json") as f:
        sqlite_data = json.load(f)

    conversations = sqlite_data['tables']['conversations']['data']
    print(f"📊 Migrating {len(conversations)} conversations...")

    success_count = 0
    error_count = 0

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

            # Add document to bob_conversations collection
            doc_ref = firestore_client.collection("bob_conversations").add(doc_data)
            success_count += 1

        except Exception as e:
            print(f"❌ Error migrating conversation: {e}")
            error_count += 1

    print(f"✅ Conversations migration complete: {success_count} success, {error_count} errors")
    return success_count, error_count

def migrate_automation_rules(firestore_client):
    """Migrate automation rules to Firestore"""

    print("⚙️  Migrating automation rules to Firestore...")

    # Load automation data
    with open("/home/jeremylongshore/bob_brain_backup/automation_export.json") as f:
        automation_data = json.load(f)

    rules = automation_data['tables']['automation_rules']['data']
    print(f"📊 Migrating {len(rules)} automation rules...")

    success_count = 0
    error_count = 0

    for rule in rules:
        try:
            doc_data = {
                "rule_id": rule.get("id"),
                "name": rule.get("name"),
                "trigger_condition": rule.get("trigger"),
                "action_type": rule.get("action"),
                "configuration": rule.get("config"),
                "active": rule.get("active", True),
                "created_at": rule.get("created_at"),
                "last_executed_at": rule.get("last_run"),
                "execution_count": rule.get("execution_count", 0),
                "success_rate": rule.get("success_rate", 0.0),
                "migrated_at": firestore.SERVER_TIMESTAMP
            }

            doc_ref = firestore_client.collection("automation_rules").add(doc_data)
            success_count += 1

        except Exception as e:
            print(f"❌ Error migrating rule: {e}")
            error_count += 1

    print(f"✅ Automation rules migration complete: {success_count} success, {error_count} errors")
    return success_count, error_count

def migrate_insights(firestore_client):
    """Migrate smart insights to Firestore"""

    print("🧠 Migrating smart insights to Firestore...")

    # Load insights data
    with open("/home/jeremylongshore/bob_brain_backup/smart_insights_export.json") as f:
        insights_data = json.load(f)

    insights = insights_data['tables']['insights']['data']
    print(f"📊 Migrating {len(insights)} insights...")

    success_count = 0
    error_count = 0

    for insight in insights:
        try:
            doc_data = {
                "insight_id": insight.get("id"),
                "type": insight.get("type"),
                "title": insight.get("title"),
                "description": insight.get("description"),
                "confidence": insight.get("confidence", 0.0),
                "importance": insight.get("importance"),
                "data_sources": insight.get("data_sources"),
                "recommended_actions": insight.get("actions"),
                "generated_at": insight.get("generated_at"),
                "user_feedback": insight.get("user_feedback"),
                "migrated_at": firestore.SERVER_TIMESTAMP
            }

            doc_ref = firestore_client.collection("insights").add(doc_data)
            success_count += 1

        except Exception as e:
            print(f"❌ Error migrating insight: {e}")
            error_count += 1

    print(f"✅ Insights migration complete: {success_count} success, {error_count} errors")
    return success_count, error_count

def validate_migration(firestore_client):
    """Validate Firestore migration"""

    print("🔍 Validating Firestore migration...")

    # Expected counts based on our exports
    expected_counts = {
        "knowledge": 1925,  # Merged data
        "bob_conversations": 13,
        "automation_rules": 2,
        "insights": 3
    }

    validation_results = {}
    all_valid = True

    for collection_name, expected_count in expected_counts.items():
        try:
            # Count documents in collection
            docs = list(firestore_client.collection(collection_name).stream())
            actual_count = len(docs)

            validation_results[collection_name] = {
                "expected": expected_count,
                "actual": actual_count,
                "valid": actual_count >= expected_count * 0.95  # Allow 5% variance
            }

            if validation_results[collection_name]["valid"]:
                print(f"✅ {collection_name}: {actual_count}/{expected_count} - PASSED")
            else:
                print(f"❌ {collection_name}: {actual_count}/{expected_count} - FAILED")
                all_valid = False

        except Exception as e:
            print(f"❌ Error validating {collection_name}: {e}")
            all_valid = False

    return all_valid, validation_results

def main():
    """Main migration function"""

    print("🚀 STARTING BOB'S FIRESTORE MIGRATION")
    print("=" * 50)

    # Initialize Firestore
    firestore_client = initialize_firestore()
    if not firestore_client:
        return False

    # Run migrations
    migrations = [
        ("Knowledge Data", migrate_knowledge_data),
        ("Conversations", migrate_conversations),
        ("Automation Rules", migrate_automation_rules),
        ("Smart Insights", migrate_insights)
    ]

    migration_results = {}

    for name, migrate_func in migrations:
        print(f"\n🔄 {name} Migration...")
        try:
            success_count, error_count = migrate_func(firestore_client)
            migration_results[name] = {
                "success": success_count,
                "errors": error_count
            }
        except Exception as e:
            print(f"❌ {name} migration failed: {e}")
            migration_results[name] = {"success": 0, "errors": 1}

    # Validate migration
    print(f"\n🔍 Validating Migration...")
    is_valid, validation_results = validate_migration(firestore_client)

    # Summary
    print(f"\n📊 MIGRATION SUMMARY")
    print("=" * 30)

    for name, results in migration_results.items():
        print(f"{name}: {results['success']} success, {results['errors']} errors")

    print(f"\nValidation: {'✅ PASSED' if is_valid else '❌ FAILED'}")

    return is_valid

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Migration completed successfully!")
    else:
        print("\n⚠️  Migration completed with issues")
