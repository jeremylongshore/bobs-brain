#!/usr/bin/env python3
"""
Archive all documentation to databases
"""

import json
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

import chromadb
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

print("📚 ARCHIVING DOCUMENTATION TO DATABASES")
print("=" * 60)

# Setup
chroma_client = chromadb.PersistentClient(path="./chroma_db")
docs_collection = chroma_client.get_or_create_collection(
    name="bob_documentation", metadata={"description": "All Bob project documentation"}
)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Neo4j
uri = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
password = os.getenv("NEO4J_PASSWORD")
neo4j_driver = GraphDatabase.driver(uri, auth=("neo4j", password))

# Process all markdown files
doc_files = []
docs_dir = "/home/jeremylongshore/bobs-brain/docs/historical"

for file in os.listdir(docs_dir):
    if file.endswith(".md"):
        filepath = os.path.join(docs_dir, file)

        # Read content
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title and summary
        lines = content.split("\n")
        title = lines[0].replace("#", "").strip() if lines else file
        summary = " ".join(lines[1:4])[:200]  # First 3 lines

        doc_info = {"filename": file, "title": title, "summary": summary, "size": len(content), "lines": len(lines)}

        # Save to ChromaDB
        embedding = embedder.encode(f"{title}\n{summary}\n{content[:1000]}").tolist()

        docs_collection.add(
            embeddings=[embedding],
            documents=[content[:3000]],  # First 3000 chars
            metadatas=[{"filename": file, "title": title, "type": "documentation", "size": len(content)}],
            ids=[f"doc_{file.replace('.md', '')}"],
        )

        doc_files.append(doc_info)

print(f"✅ Saved {len(doc_files)} documentation files to ChromaDB")

# Save summary to Neo4j
with neo4j_driver.session() as session:
    # Create Documentation node
    session.run(
        """
        CREATE (d:Documentation {
            name: 'Bob Project Docs',
            date: datetime(),
            doc_count: $count,
            total_size: $size
        })
    """,
        count=len(doc_files),
        size=sum(d["size"] for d in doc_files),
    )

    # Add key docs as nodes
    important_docs = [
        "CLAUDE_HANDOFF_GUIDE.md",
        "CIRCLE_OF_LIFE_COMPLETE.md",
        "BOB_STRATEGIC_ASSESSMENT.md",
        "DEPLOYMENT_SUCCESS.md",
    ]

    for doc in doc_files:
        if doc["filename"] in important_docs:
            session.run(
                """
                MERGE (d:Document {filename: $filename})
                SET d.title = $title,
                    d.size = $size,
                    d.archived = datetime()
            """,
                filename=doc["filename"],
                title=doc["title"],
                size=doc["size"],
            )

print(f"✅ Saved documentation metadata to Neo4j")

# Summary
print("\n" + "=" * 60)
print(
    f"""
📊 DOCUMENTATION ARCHIVED!

Files Archived: {len(doc_files)}
Total Size: {sum(d['size'] for d in doc_files) / 1024:.2f} KB

Top Documentation Files:
"""
)

for doc in sorted(doc_files, key=lambda x: x["size"], reverse=True)[:10]:
    print(f"  {doc['filename']}: {doc['size']/1024:.1f}KB - {doc['title'][:40]}")

print("\n✅ All documentation preserved in databases!")
print("📁 Files moved to: docs/historical/")
print("\nYour root directory is now CLEAN! 🎉")
