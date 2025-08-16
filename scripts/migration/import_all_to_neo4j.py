# \!/usr/bin/env python3
"""Import ALL data from this machine to Neo4j Aura"""

import glob
import hashlib
import json
import os
from datetime import datetime

from neo4j import GraphDatabase

# Neo4j Aura credentials
uri = "neo4j+s://d3653283.databases.neo4j.io"
user = "neo4j"
password = "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE"

print("Connecting to Neo4j Aura...")
driver = GraphDatabase.driver(uri, auth=(user, password))

all_data = []

# 1. Find and load all JSON files with data
print("\nSearching for all data files on machine...")
json_patterns = ["bob_data*.json", "*backup*.json", "archive/**/*.json", "data/*.json", "*.data.json"]

for pattern in json_patterns:
    files = glob.glob(pattern, recursive=True)
    for file in files:
        try:
            if os.path.getsize(file) > 100:  # Skip tiny files
                with open(file, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"  Found {len(data)} items in {file}")
                        all_data.extend(data)
                    elif isinstance(data, dict) and "text" in data:
                        print(f"  Found document in {file}")
                        all_data.append(data)
        except:
            pass

# 2. Load markdown documentation files
print("\nLoading documentation files...")
md_files = glob.glob("*.md") + glob.glob("docs/*.md")
for md_file in md_files:
    try:
        with open(md_file, "r") as f:
            content = f.read()
            if len(content) > 100:
                doc = {
                    "id": f"md_{os.path.basename(md_file).replace('.md', '')}",
                    "title": os.path.basename(md_file),
                    "text": content[:5000],  # Truncate long docs
                    "category": "documentation",
                    "source": md_file,
                }
                all_data.append(doc)
                print(f"  Added documentation: {md_file}")
    except:
        pass

# 3. Add CLAUDE.md content (critical project documentation)
if os.path.exists("CLAUDE.md"):
    with open("CLAUDE.md", "r") as f:
        claude_content = f.read()
        sections = claude_content.split("\n## ")
        for section in sections[:10]:  # First 10 sections
            if section.strip():
                title = section.split("\n")[0].replace("#", "").strip()
                doc = {
                    "id": f"claude_{hashlib.md5(title.encode()).hexdigest()[:8]}",
                    "title": f"CLAUDE.md - {title}",
                    "text": section[:2000],
                    "category": "project_critical",
                    "source": "CLAUDE.md",
                }
                all_data.append(doc)

# 4. Add Python source code documentation
print("\nExtracting Python source documentation...")
py_files = glob.glob("src/*.py")[:20]  # Limit to 20 files
for py_file in py_files:
    try:
        with open(py_file, "r") as f:
            content = f.read()
            # Extract docstrings and important functions
            if '"""' in content:
                docstring = content.split('"""')[1] if len(content.split('"""')) > 1 else ""
                doc = {
                    "id": f"py_{os.path.basename(py_file).replace('.py', '')}",
                    "title": os.path.basename(py_file),
                    "text": docstring[:1000],
                    "category": "source_code",
                    "source": py_file,
                }
                all_data.append(doc)
                print(f"  Added source: {py_file}")
    except:
        pass

# Remove duplicates
unique_data = []
seen_ids = set()
for doc in all_data:
    doc_id = doc.get("id", hashlib.md5(str(doc).encode()).hexdigest())
    if doc_id not in seen_ids:
        seen_ids.add(doc_id)
        unique_data.append(doc)

print(f"\nTotal unique documents found: {len(unique_data)}")

# Import to Neo4j
print(f"\nImporting {len(unique_data)} documents to Neo4j Aura...")

with driver.session() as session:
    imported = 0

    for doc in unique_data:
        try:
            # Create knowledge node
            result = session.run(
                """
                MERGE (k:Knowledge {id: $id})
                SET k.title = $title,
                    k.content = $content,
                    k.category = $category,
                    k.source = $source,
                    k.imported_at = datetime()
                RETURN k.id as doc_id
            """,
                id=doc.get("id", hashlib.md5(str(doc).encode()).hexdigest()[:12]),
                title=doc.get("title", "Untitled")[:200],
                content=doc.get("text", doc.get("content", ""))[:5000],
                category=doc.get("category", "general"),
                source=doc.get("source", "local_machine"),
            )

            imported += 1
            if imported % 10 == 0:
                print(f"  Imported {imported} documents...")

        except Exception as e:
            pass  # Skip errors silently

    print(f"\n✅ Successfully imported {imported} documents")

    # Get final statistics
    result = session.run(
        """
        MATCH (n)
        RETURN
            labels(n)[0] as label,
            COUNT(*) as count
        ORDER BY count DESC
    """
    )

    print("\nNeo4j Aura Statistics:")
    print("=" * 30)
    for record in result:
        print(f"{record['label']}: {record['count']}")

driver.close()
print("\n✅ ALL DATA IMPORTED TO NEO4J AURA\!")
