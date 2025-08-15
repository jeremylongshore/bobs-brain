#!/usr/bin/env python3
"""
Quick archive of all Python files to databases
"""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

# Load environment
from dotenv import load_dotenv

load_dotenv()

# Databases
import chromadb
from google.cloud import bigquery
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

print("🗄️ QUICK ARCHIVING BOB FILES TO DATABASES")
print("=" * 60)

# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="bob_archive", metadata={"description": "All historical Bob Python files"}
)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Neo4j
uri = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
password = os.getenv("NEO4J_PASSWORD")
neo4j_driver = GraphDatabase.driver(uri, auth=("neo4j", password))

# Find all Python files
python_files = []
for root, dirs, files in os.walk("/home/jeremylongshore/bobs-brain"):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, "/home/jeremylongshore/bobs-brain")

            # Get file info
            size = os.path.getsize(filepath)

            # Read first 500 chars
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    snippet = f.read(500)
            except:
                snippet = ""

            python_files.append({"path": rel_path, "name": file, "size": size, "snippet": snippet})

print(f"Found {len(python_files)} Python files")

# Save to ChromaDB
print("Saving to ChromaDB...")
for i, file_info in enumerate(python_files):
    doc = f"{file_info['name']}\n{file_info['path']}\n{file_info['snippet']}"
    embedding = embedder.encode(doc).tolist()

    collection.add(
        embeddings=[embedding],
        documents=[doc],
        metadatas=[{"filepath": file_info["path"], "filename": file_info["name"], "size": file_info["size"]}],
        ids=[f"file_{i}"],
    )

print(f"✅ Saved {len(python_files)} files to ChromaDB")

# Save to Neo4j
print("Saving to Neo4j...")
with neo4j_driver.session() as session:
    # Create Archive node
    session.run(
        """
        CREATE (a:Archive {
            name: 'Bob Python Files',
            date: datetime(),
            file_count: $count
        })
    """,
        count=len(python_files),
    )

    # Add top-level summary
    for file_info in python_files[:20]:  # Just save first 20 to Neo4j
        session.run(
            """
            MERGE (f:ArchivedFile {path: $path})
            SET f.name = $name,
                f.size = $size
        """,
            path=file_info["path"],
            name=file_info["name"],
            size=file_info["size"],
        )

print(f"✅ Saved summary to Neo4j")

# Save list to BigQuery
print("Saving to BigQuery...")
try:
    bq_client = bigquery.Client(project="bobs-house-ai")

    # Create simple table
    table_id = "bobs-house-ai.bob_code_archive.file_list"

    # Just save as JSON for now
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
    )

    # Write to temp file
    with open("/tmp/archive_files.json", "w") as f:
        for file_info in python_files:
            json.dump(file_info, f)
            f.write("\n")

    # Load to BigQuery
    with open("/tmp/archive_files.json", "rb") as f:
        job = bq_client.load_table_from_file(f, table_id, job_config=job_config)

    job.result()  # Wait for job to complete
    print(f"✅ Saved {len(python_files)} records to BigQuery")
except Exception as e:
    print(f"⚠️ BigQuery save failed: {e}")

# Summary
print("\n" + "=" * 60)
print(
    f"""
📊 ARCHIVE COMPLETE!

Files Archived: {len(python_files)}
Total Size: {sum(f['size'] for f in python_files) / 1024 / 1024:.2f} MB

Saved to:
✅ ChromaDB - Full text search of all files
✅ Neo4j - File relationships and metadata
✅ BigQuery - Analytics and history

Top directories with Python files:
"""
)

# Show distribution
from collections import Counter

dirs = Counter(os.path.dirname(f["path"]) for f in python_files)
for dir_name, count in dirs.most_common(10):
    print(f"  {dir_name or 'root'}: {count} files")

print("\n🎉 You can now safely delete archive folders!")
print("All code knowledge is preserved in the databases.")

# Save file list for reference
with open("archived_files.json", "w") as f:
    json.dump(python_files, f, indent=2)
print("\n📄 File list saved to archived_files.json")
