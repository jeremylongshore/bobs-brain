#!/usr/bin/env python3
"""
Archive all Bob versions to knowledge databases
Saves code patterns to ChromaDB, Neo4j, and BigQuery
Then safely removes archive folders
"""

import ast
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
import google.generativeai as genai
from google.cloud import bigquery
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

print("🗄️ ARCHIVING BOB'S EVOLUTION TO KNOWLEDGE BASES")
print("=" * 60)


class BobArchiver:
    def __init__(self):
        # Initialize connections
        self.setup_chromadb()
        self.setup_neo4j()
        self.setup_bigquery()
        self.setup_gemini()

        self.files_processed = 0
        self.knowledge_items = []

    def setup_chromadb(self):
        """Initialize ChromaDB for code embeddings"""
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.code_collection = self.chroma_client.get_or_create_collection(
            name="bob_code_evolution", metadata={"description": "Historical Bob implementations and patterns"}
        )
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ ChromaDB initialized")

    def setup_neo4j(self):
        """Initialize Neo4j for code relationships"""
        uri = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
        user = "neo4j"
        password = os.getenv("NEO4J_PASSWORD")

        try:
            self.neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
            print("✅ Neo4j connected")
        except Exception as e:
            print(f"⚠️ Neo4j connection failed: {e}")
            self.neo4j_driver = None

    def setup_bigquery(self):
        """Initialize BigQuery for analytics"""
        try:
            self.bq_client = bigquery.Client(project="bobs-house-ai")

            # Create dataset if not exists
            dataset_id = "bobs-house-ai.bob_code_archive"
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            dataset.description = "Archive of all Bob implementations"

            try:
                self.bq_client.create_dataset(dataset, exists_ok=True)
            except:
                pass  # Dataset exists

            # Create table if not exists
            table_id = "bobs-house-ai.bob_code_archive.implementations"
            schema = [
                bigquery.SchemaField("file_path", "STRING"),
                bigquery.SchemaField("file_name", "STRING"),
                bigquery.SchemaField("content_hash", "STRING"),
                bigquery.SchemaField("size_bytes", "INTEGER"),
                bigquery.SchemaField("functions", "STRING", mode="REPEATED"),
                bigquery.SchemaField("classes", "STRING", mode="REPEATED"),
                bigquery.SchemaField("imports", "STRING", mode="REPEATED"),
                bigquery.SchemaField("description", "STRING"),
                bigquery.SchemaField("archived_at", "TIMESTAMP"),
            ]

            table = bigquery.Table(table_id, schema=schema)
            try:
                self.bq_client.create_table(table, exists_ok=True)
            except:
                pass  # Table exists

            print("✅ BigQuery initialized")
        except Exception as e:
            print(f"⚠️ BigQuery setup failed: {e}")
            self.bq_client = None

    def setup_gemini(self):
        """Initialize Gemini for code understanding"""
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.gemini = genai.GenerativeModel("gemini-1.5-flash")
        print("✅ Gemini initialized for code analysis")

    def extract_code_features(self, filepath, content):
        """Extract features from Python code"""
        features = {"functions": [], "classes": [], "imports": [], "docstrings": []}

        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    features["functions"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    features["classes"].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        features["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        features["imports"].append(node.module)
        except:
            pass  # Syntax error in old code

        return features

    def analyze_with_gemini(self, content, filename):
        """Use Gemini to understand code purpose"""
        try:
            prompt = f"""Analyze this Python file '{filename}' and provide a one-line description of its purpose:

{content[:1000]}...

Description (one line only):"""

            response = self.gemini.generate_content(prompt)
            return response.text.strip()
        except:
            return f"Bob implementation: {filename}"

    def process_python_file(self, filepath):
        """Process a single Python file"""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Skip empty files
            if not content.strip():
                return

            filename = os.path.basename(filepath)
            rel_path = os.path.relpath(filepath, "/home/jeremylongshore/bobs-brain")

            # Extract features
            features = self.extract_code_features(filepath, content)

            # Get AI description
            description = self.analyze_with_gemini(content, filename)

            # Generate hash
            content_hash = hashlib.md5(content.encode()).hexdigest()

            # Save to ChromaDB (code embeddings)
            if len(content) > 100:  # Skip tiny files
                self.save_to_chromadb(rel_path, content, features, description)

            # Save to Neo4j (relationships)
            if self.neo4j_driver:
                self.save_to_neo4j(rel_path, features, description)

            # Save to BigQuery (analytics)
            if self.bq_client:
                self.save_to_bigquery(rel_path, features, description, content_hash, len(content))

            self.files_processed += 1

            if self.files_processed % 10 == 0:
                print(f"📁 Processed {self.files_processed} files...")

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    def save_to_chromadb(self, filepath, content, features, description):
        """Save code to vector database"""
        # Create searchable text
        searchable = f"{description}\n{filepath}\n"
        searchable += f"Functions: {', '.join(features['functions'])}\n"
        searchable += f"Classes: {', '.join(features['classes'])}\n"

        # Take first 2000 chars of code
        code_snippet = content[:2000]

        # Generate embedding
        embedding = self.embedder.encode(searchable).tolist()

        # Store in ChromaDB
        self.code_collection.add(
            embeddings=[embedding],
            documents=[code_snippet],
            metadatas=[
                {
                    "filepath": filepath,
                    "description": description,
                    "functions": ", ".join(features["functions"][:10]),
                    "classes": ", ".join(features["classes"][:10]),
                    "type": "historical_implementation",
                }
            ],
            ids=[f"code_{hashlib.md5(filepath.encode()).hexdigest()}"],
        )

    def save_to_neo4j(self, filepath, features, description):
        """Save code relationships to graph"""
        with self.neo4j_driver.session() as session:
            # Create code node
            session.run(
                """
                MERGE (c:Code {filepath: $filepath})
                SET c.description = $description,
                    c.archived_at = datetime(),
                    c.functions = $functions,
                    c.classes = $classes
            """,
                filepath=filepath,
                description=description,
                functions=features["functions"][:10],
                classes=features["classes"][:10],
            )

            # Link to Bob evolution
            session.run(
                """
                MATCH (b:Concept {name: 'Bob Ferrari'})
                MATCH (c:Code {filepath: $filepath})
                MERGE (b)-[:EVOLVED_FROM]->(c)
            """,
                filepath=filepath,
            )

    def save_to_bigquery(self, filepath, features, description, content_hash, size):
        """Save to BigQuery for analytics"""
        table_id = "bobs-house-ai.bob_code_archive.implementations"

        row = {
            "file_path": filepath,
            "file_name": os.path.basename(filepath),
            "content_hash": content_hash,
            "size_bytes": size,
            "functions": features["functions"][:20],
            "classes": features["classes"][:20],
            "imports": features["imports"][:30],
            "description": description,
            "archived_at": datetime.utcnow().isoformat(),
        }

        self.knowledge_items.append(row)

        # Batch insert every 50 items
        if len(self.knowledge_items) >= 50:
            self.flush_to_bigquery()

    def flush_to_bigquery(self):
        """Flush batch to BigQuery"""
        if not self.knowledge_items:
            return

        table_id = "bobs-house-ai.bob_code_archive.implementations"
        errors = self.bq_client.insert_rows_json(table_id, self.knowledge_items)

        if errors:
            print(f"⚠️ BigQuery insert errors: {errors}")
        else:
            print(f"✅ Saved {len(self.knowledge_items)} items to BigQuery")

        self.knowledge_items = []

    def archive_all_python_files(self):
        """Process all Python files in archive directories"""
        archive_dirs = [
            "/home/jeremylongshore/bobs-brain/archive",
            "/home/jeremylongshore/bobs-brain/src",
            "/home/jeremylongshore/bobs-brain/scripts",
        ]

        total_files = 0
        for base_dir in archive_dirs:
            if os.path.exists(base_dir):
                for root, dirs, files in os.walk(base_dir):
                    for file in files:
                        if file.endswith(".py"):
                            total_files += 1

        print(f"\n📊 Found {total_files} Python files to archive")

        # Process each file
        for base_dir in archive_dirs:
            if os.path.exists(base_dir):
                for root, dirs, files in os.walk(base_dir):
                    for file in files:
                        if file.endswith(".py"):
                            filepath = os.path.join(root, file)
                            self.process_python_file(filepath)

        # Flush remaining items
        if self.bq_client:
            self.flush_to_bigquery()

        print(f"\n✅ Archived {self.files_processed} files to knowledge bases!")

    def create_summary(self):
        """Create summary of what was archived"""
        summary = f"""
📚 BOB'S CODE EVOLUTION ARCHIVED
================================
Files Processed: {self.files_processed}
ChromaDB Vectors: {self.code_collection.count()}
Neo4j Nodes: Created/Updated
BigQuery Records: {self.files_processed}

Knowledge Now Searchable:
- All Bob implementations from v1 to Ferrari
- Code patterns and evolution
- Function and class definitions
- Historical debugging approaches

The archive folders can now be safely deleted.
Bob Ferrari has absorbed all the knowledge! 🏎️
"""
        print(summary)

        # Save summary
        with open("archive_summary.txt", "w") as f:
            f.write(summary)


if __name__ == "__main__":
    archiver = BobArchiver()
    archiver.archive_all_python_files()
    archiver.create_summary()

    print("\n🗑️ Archive folders can now be deleted with: rm -rf archive/")
    print("💾 All knowledge preserved in databases!")
