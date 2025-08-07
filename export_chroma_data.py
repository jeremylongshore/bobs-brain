#!/usr/bin/env python3
"""
Export ChromaDB data for migration to Firestore
"""

import json
import os
from langchain_chroma import Chroma

def export_chromadb():
    """Export ChromaDB data to JSON format"""

    print("🔍 Exporting ChromaDB data...")

    # Initialize ChromaDB
    persist_directory = "/home/jeremylongshore/.bob_brain/chroma"

    if not os.path.exists(persist_directory):
        print(f"❌ ChromaDB directory not found: {persist_directory}")
        return False

    try:
        # Connect to ChromaDB
        vectorstore = Chroma(persist_directory=persist_directory)

        # Get all data
        chroma_data = vectorstore.get()

        print(f"📊 Found {len(chroma_data['ids'])} items in ChromaDB")

        # Convert embeddings to list format for JSON serialization
        embeddings_list = []
        if chroma_data.get('embeddings'):
            for embedding in chroma_data['embeddings']:
                if hasattr(embedding, 'tolist'):
                    embeddings_list.append(embedding.tolist())
                else:
                    embeddings_list.append(list(embedding))

        # Prepare export data
        export_data = {
            "ids": chroma_data["ids"],
            "documents": chroma_data["documents"],
            "embeddings": embeddings_list,
            "metadatas": chroma_data["metadatas"],
            "total_items": len(chroma_data["ids"])
        }

        # Save to JSON
        export_path = "/home/jeremylongshore/bob_brain_backup/chroma_export.json"
        with open(export_path, "w") as f:
            json.dump(export_data, f, indent=2)

        print(f"✅ ChromaDB data exported to: {export_path}")
        print(f"📈 Total items: {len(chroma_data['ids'])}")

        return True

    except Exception as e:
        print(f"❌ Error exporting ChromaDB: {e}")
        return False

if __name__ == "__main__":
    export_chromadb()
