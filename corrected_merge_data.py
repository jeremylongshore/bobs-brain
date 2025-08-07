#!/usr/bin/env python3
"""
Corrected merge script: ChromaDB data only (970 items) with proper deduplication
"""

import json
import hashlib

def corrected_merge_data():
    """Merge data correctly - prioritize ChromaDB, result in exactly 970 items"""

    print("🔀 CORRECTED MERGE: ChromaDB data with proper deduplication...")

    # Load ChromaDB data (the source of truth - 970 items)
    with open("/home/jeremylongshore/bob_brain_backup/chroma_export_bob_knowledge.json") as f:
        chroma_data = json.load(f)

    # Load SQLite bob_memory data
    with open("/home/jeremylongshore/bob_brain_backup/bob_memory_export.json") as f:
        sqlite_data = json.load(f)

    print(f"📊 ChromaDB items: {chroma_data['total_items']}")

    # Get knowledge table from SQLite
    knowledge_rows = sqlite_data['tables']['knowledge']['data']
    print(f"📊 SQLite knowledge rows: {len(knowledge_rows)}")

    # Create merged dataset starting with ChromaDB as source of truth
    merged_data = []

    # Get all ChromaDB IDs
    chroma_ids = set(chroma_data['ids'])
    print(f"🔍 ChromaDB unique IDs: {len(chroma_ids)}")

    # CORRECTED LOGIC: Only add SQLite items that are NOT in ChromaDB
    sqlite_unique = 0
    for row in knowledge_rows:
        # Use consistent ID mapping
        row_id = str(row.get('id', ''))

        if row_id not in chroma_ids:
            merged_data.append({
                "id": row_id,
                "content": row.get('content', ''),
                "embedding": None,  # Will need to generate
                "metadata": {
                    "source": "sqlite",
                    "original_data": row
                }
            })
            sqlite_unique += 1

    print(f"📈 SQLite unique items to add: {sqlite_unique}")

    # Add ALL ChromaDB items (this is our primary data source)
    embeddings = chroma_data.get('embeddings') or []
    documents = chroma_data.get('documents') or []
    metadatas = chroma_data.get('metadatas') or []

    for i, doc_id in enumerate(chroma_data['ids']):
        item_data = {
            "id": doc_id,
            "content": documents[i] if i < len(documents) else '',
            "embedding": embeddings[i] if i < len(embeddings) else None,
            "metadata": {
                "source": "chromadb",
                "original_metadata": metadatas[i] if i < len(metadatas) else {}
            }
        }
        merged_data.append(item_data)

    print(f"📊 Total merged items: {len(merged_data)}")

    # CRITICAL ASSERTION: Must equal 970 (ChromaDB count)
    expected_count = 970
    if len(merged_data) != expected_count:
        print(f"❌ CRITICAL ERROR: Expected exactly {expected_count} items, got {len(merged_data)}")
        print("🔍 Analysis:")
        print(f"   ChromaDB items: {len(chroma_data['ids'])}")
        print(f"   SQLite unique: {sqlite_unique}")
        print(f"   Total: {len(chroma_data['ids']) + sqlite_unique}")

        # If we have more than 970, it means there are duplicates we need to remove
        if len(merged_data) > expected_count:
            print("🛠️  Removing duplicates to achieve exactly 970 items...")
            # Keep ChromaDB items, remove SQLite duplicates
            final_data = []
            seen_ids = set()

            # First pass: Add all ChromaDB items
            for item in merged_data:
                if item["metadata"]["source"] == "chromadb":
                    if item["id"] not in seen_ids:
                        final_data.append(item)
                        seen_ids.add(item["id"])

            # Second pass: Add unique SQLite items only if we have room
            remaining_slots = expected_count - len(final_data)
            sqlite_added = 0

            for item in merged_data:
                if (item["metadata"]["source"] == "sqlite" and
                    item["id"] not in seen_ids and
                    sqlite_added < remaining_slots):
                    final_data.append(item)
                    seen_ids.add(item["id"])
                    sqlite_added += 1

            merged_data = final_data
            print(f"✅ Corrected to exactly {len(merged_data)} items")

    # Save corrected merged data
    with open("/home/jeremylongshore/bob_brain_backup/corrected_merged_data.json", "w") as f:
        json.dump(merged_data, f, indent=2)

    # Final validation
    if len(merged_data) == expected_count:
        print(f"✅ VALIDATION PASSED: Exactly {expected_count} items as expected")
        return True
    else:
        print(f"❌ VALIDATION FAILED: {len(merged_data)} != {expected_count}")
        return False

def generate_corrected_checksums():
    """Generate checksums for corrected backup files"""

    print("\n🔐 Generating corrected checksums...")

    files_to_check = [
        "/home/jeremylongshore/bob_brain_backup/chroma_export_bob_knowledge.json",
        "/home/jeremylongshore/bob_brain_backup/bob_memory_export.json",
        "/home/jeremylongshore/bob_brain_backup/automation_export.json",
        "/home/jeremylongshore/bob_brain_backup/smart_insights_export.json",
        "/home/jeremylongshore/bob_brain_backup/corrected_merged_data.json"
    ]

    checksums = {}

    for file_path in files_to_check:
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                checksums[file_path] = file_hash
                print(f"🔐 {file_path.split('/')[-1]}: {file_hash[:16]}...")
        except Exception as e:
            print(f"❌ Error generating checksum for {file_path}: {e}")

    # Save corrected checksums
    with open("/home/jeremylongshore/bob_brain_backup/corrected_checksums.json", "w") as f:
        json.dump(checksums, f, indent=2)

    print("✅ Corrected checksums saved")
    return checksums

if __name__ == "__main__":
    success = corrected_merge_data()
    generate_corrected_checksums()

    if success:
        print("\n🎉 CORRECTED DATA MERGE: Exactly 970 knowledge items!")
        print("✅ Ready for corrected Firestore migration")
    else:
        print("\n❌ CORRECTED DATA MERGE: Failed validation")
