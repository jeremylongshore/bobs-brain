#!/usr/bin/env python3
"""
Merge ChromaDB and SQLite knowledge data, prioritizing ChromaDB
"""

import json
import hashlib

def merge_data():
    """Merge ChromaDB and SQLite knowledge data"""

    print("🔀 Merging ChromaDB and SQLite knowledge data...")

    # Load ChromaDB data
    with open("/home/jeremylongshore/bob_brain_backup/chroma_export_bob_knowledge.json") as f:
        chroma_data = json.load(f)

    # Load SQLite bob_memory data
    with open("/home/jeremylongshore/bob_brain_backup/bob_memory_export.json") as f:
        sqlite_data = json.load(f)

    print(f"📊 ChromaDB items: {chroma_data['total_items']}")

    # Get knowledge table from SQLite
    knowledge_rows = sqlite_data['tables']['knowledge']['data']
    print(f"📊 SQLite knowledge rows: {len(knowledge_rows)}")

    # Create merged dataset - prioritize ChromaDB
    merged_data = []

    # Get all ChromaDB IDs to avoid duplicates
    chroma_ids = set(chroma_data['ids'])
    print(f"🔍 ChromaDB unique IDs: {len(chroma_ids)}")

    # Add items from SQLite that are NOT in ChromaDB
    sqlite_unique = 0
    for row in knowledge_rows:
        # Use various ID fields that might exist
        row_id = row.get('id') or row.get('doc_id') or str(hash(row.get('content', '')))

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

    # Add all ChromaDB items
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

    # Save merged data
    with open("/home/jeremylongshore/bob_brain_backup/merged_data.json", "w") as f:
        json.dump(merged_data, f, indent=2)

    print(f"✅ Merged data saved: {len(merged_data)} total items")

    # Validate expected count (should be close to 970 from ChromaDB)
    expected_count = 970
    if len(merged_data) >= expected_count:
        print(f"✅ Validation PASSED: {len(merged_data)} >= {expected_count}")
        return True
    else:
        print(f"⚠️  Validation WARNING: {len(merged_data)} < {expected_count}")
        return False

def generate_checksums():
    """Generate checksums for backup files"""

    print("\n🔐 Generating checksums...")

    files_to_check = [
        "/home/jeremylongshore/bob_brain_backup/chroma_export_bob_knowledge.json",
        "/home/jeremylongshore/bob_brain_backup/bob_memory_export.json",
        "/home/jeremylongshore/bob_brain_backup/automation_export.json",
        "/home/jeremylongshore/bob_brain_backup/smart_insights_export.json",
        "/home/jeremylongshore/bob_brain_backup/merged_data.json"
    ]

    checksums = {}

    for file_path in files_to_check:
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                checksums[file_path] = file_hash
                print(f"🔐 {file_path}: {file_hash[:16]}...")
        except Exception as e:
            print(f"❌ Error generating checksum for {file_path}: {e}")

    # Save checksums
    with open("/home/jeremylongshore/bob_brain_backup/checksums.json", "w") as f:
        json.dump(checksums, f, indent=2)

    print("✅ Checksums saved to checksums.json")
    return checksums

if __name__ == "__main__":
    success = merge_data()
    generate_checksums()

    if success:
        print("\n🎉 Data merge completed successfully!")
    else:
        print("\n⚠️  Data merge completed with warnings")
