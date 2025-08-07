#!/usr/bin/env python3
"""
Export ChromaDB data as specified in the requirements
"""

from langchain_chroma import Chroma
import json

def export_chromadb_data():
    """Export ChromaDB data exactly as specified"""

    print("🔍 Exporting ChromaDB data...")

    try:
        vectorstore = Chroma(persist_directory="/home/jeremylongshore/.bob_brain/chroma")
        chroma_data = vectorstore.get()

        print(f"📊 Found {len(chroma_data['ids'])} items in ChromaDB")

        with open("/home/jeremylongshore/bob_brain_backup/chroma_export.json", "w") as f:
            json.dump({"ids": chroma_data["ids"], "documents": chroma_data["documents"],
                       "embeddings": [e.tolist() for e in chroma_data["embeddings"]],
                       "metadatas": chroma_data["metadatas"]}, f)

        print("✅ ChromaDB export completed")
        return True

    except Exception as e:
        print(f"❌ Error exporting ChromaDB: {e}")
        return False

if __name__ == "__main__":
    export_chromadb_data()
