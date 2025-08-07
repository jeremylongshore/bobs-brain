#!/usr/bin/env python3
"""
Export ChromaDB data directly using chromadb client
"""

import json
import chromadb
import os

def export_chromadb_direct():
    """Export ChromaDB data using direct chromadb client"""

    print("🔍 Exporting ChromaDB data with direct client...")

    # Try both potential ChromaDB locations
    locations = [
        "/home/jeremylongshore/.bob_brain/chroma",
        "/home/jeremylongshore/.bob_brain/chromadb"
    ]

    for persist_path in locations:
        if not os.path.exists(persist_path):
            continue

        print(f"📂 Trying ChromaDB location: {persist_path}")

        try:
            # Connect to ChromaDB
            client = chromadb.PersistentClient(path=persist_path)

            # List collections
            collections = client.list_collections()
            print(f"📋 Found {len(collections)} collections")

            for collection_info in collections:
                print(f"   - Collection: {collection_info.name}")

                # Get the collection
                collection = client.get_collection(collection_info.name)

                # Get all data
                all_data = collection.get()

                print(f"📊 Collection '{collection_info.name}' contains {len(all_data['ids'])} items")

                if len(all_data['ids']) > 0:
                    # Prepare export data
                    export_data = {
                        "collection_name": collection_info.name,
                        "ids": all_data["ids"],
                        "documents": all_data["documents"],
                        "embeddings": all_data["embeddings"],
                        "metadatas": all_data["metadatas"],
                        "total_items": len(all_data["ids"]),
                        "source_path": persist_path
                    }

                    # Save to JSON
                    export_path = f"/home/jeremylongshore/bob_brain_backup/chroma_export_{collection_info.name}.json"
                    with open(export_path, "w") as f:
                        json.dump(export_data, f, indent=2)

                    print(f"✅ Exported collection '{collection_info.name}' to: {export_path}")
                    return True

        except Exception as e:
            print(f"⚠️  Error with location {persist_path}: {e}")
            continue

    print("❌ No ChromaDB data found in any location")
    return False

if __name__ == "__main__":
    export_chromadb_direct()
