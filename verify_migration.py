#!/usr/bin/env python3
"""
Verify complete migration counts
"""

from google.cloud import firestore

def verify_migration():
    """Verify actual migration counts"""

    print("🔍 Verifying migration counts...")

    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # For knowledge collection, we need to count all documents
    # Firestore doesn't have a direct count, so we'll paginate through all
    print("📊 Counting knowledge documents...")

    knowledge_count = 0
    last_doc = None

    while True:
        query = client.collection("knowledge").limit(1000)
        if last_doc:
            query = query.start_after(last_doc)

        docs = list(query.stream())
        if not docs:
            break

        knowledge_count += len(docs)
        last_doc = docs[-1]

        print(f"   Current count: {knowledge_count}")

        if len(docs) < 1000:  # Last batch
            break

    # Count other collections
    conv_count = len(list(client.collection("bob_conversations").stream()))
    auto_count = len(list(client.collection("automation_rules").stream()))
    insights_count = len(list(client.collection("insights").stream()))

    print(f"\n📊 FINAL COUNTS:")
    print(f"   Knowledge: {knowledge_count}")
    print(f"   Conversations: {conv_count}")
    print(f"   Automation Rules: {auto_count}")
    print(f"   Insights: {insights_count}")
    print(f"   Total: {knowledge_count + conv_count + auto_count + insights_count}")

    # Expected counts
    expected = {
        "knowledge": 1925,
        "conversations": 13,
        "automation": 2,
        "insights": 3
    }

    actual = {
        "knowledge": knowledge_count,
        "conversations": conv_count,
        "automation": auto_count,
        "insights": insights_count
    }

    print(f"\n✅ VALIDATION:")
    all_good = True
    for key, expected_count in expected.items():
        actual_count = actual[key]
        if actual_count >= expected_count:
            print(f"   {key}: ✅ {actual_count}/{expected_count}")
        else:
            print(f"   {key}: ❌ {actual_count}/{expected_count}")
            all_good = False

    return all_good

if __name__ == "__main__":
    success = verify_migration()
    if success:
        print("\n🎉 Migration verification PASSED!")
    else:
        print("\n⚠️  Migration verification FAILED!")
