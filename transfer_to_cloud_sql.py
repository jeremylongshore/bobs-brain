#\!/usr/bin/env python3
"""
Transfer Bob's Brain data to Cloud SQL (bob-dry-storage)
Consolidate ChromaDB and SQLite into shared cloud database
"""

import chromadb
import sqlite3
import psycopg2
import os
from datetime import datetime

# Cloud SQL connection
CLOUD_SQL_HOST = "34.162.100.113"  # bob-dry-storage external IP
CLOUD_SQL_DB = "bob_pantry"
CLOUD_SQL_USER = "postgres"

def transfer_chromadb_to_cloud():
    """Transfer ChromaDB vectors to Cloud SQL"""
    print("🧠 Transferring ChromaDB (970 items) to Cloud SQL...")

    # Connect to local ChromaDB
    local_client = chromadb.PersistentClient(path='/home/jeremylongshore/.bob_brain/chroma')
    collection = local_client.get_collection('bob_knowledge')

    # Get all data
    all_data = collection.get()
    print(f"📊 Found {len(all_data['ids'])} items in ChromaDB")

    # TODO: Connect to Cloud SQL and create vector table
    # This would store embeddings in PostgreSQL with pgvector extension

    return len(all_data['ids'])

def transfer_sqlite_to_cloud():
    """Transfer SQLite databases to Cloud SQL"""
    databases = [
        ('/home/jeremylongshore/.bob_brain/bob_memory.db', 'conversations'),
        ('/home/jeremylongshore/.bob_brain/automation.db', 'workflows'),
        ('/home/jeremylongshore/.bob_brain/smart_insights.db', 'analytics')
    ]

    total_transferred = 0
    for db_path, table_type in databases:
        if os.path.exists(db_path):
            print(f"📁 Transferring {table_type} from {os.path.basename(db_path)}...")

            # Connect to SQLite
            sqlite_conn = sqlite3.connect(db_path)
            cursor = sqlite_conn.cursor()

            # Get tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"  - Table {table[0]}: {count} rows")
                total_transferred += count

            sqlite_conn.close()

    return total_transferred

def create_unified_schema():
    """Create unified schema in Cloud SQL for Bob & Alice"""
    schema = """
    -- Bob's Brain Unified Schema
    CREATE SCHEMA IF NOT EXISTS bob_brain;

    -- Knowledge vectors (from ChromaDB)
    CREATE TABLE IF NOT EXISTS bob_brain.knowledge_vectors (
        id TEXT PRIMARY KEY,
        content TEXT,
        embedding VECTOR(384),  -- or appropriate dimension
        metadata JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );

    -- Conversations (from bob_memory.db)
    CREATE TABLE IF NOT EXISTS bob_brain.conversations (
        id SERIAL PRIMARY KEY,
        user_input TEXT,
        bot_response TEXT,
        context JSONB,
        timestamp TIMESTAMP DEFAULT NOW()
    );

    -- Shared with Alice
    CREATE TABLE IF NOT EXISTS bob_brain.shared_context (
        id SERIAL PRIMARY KEY,
        agent TEXT,  -- 'bob' or 'alice'
        data JSONB,
        shared_at TIMESTAMP DEFAULT NOW()
    );
    """
    print("📋 Schema ready for Cloud SQL")
    return schema

if __name__ == "__main__":
    print("🚀 Starting Bob's Brain Cloud Transfer...")

    # Show what we'll transfer
    schema = create_unified_schema()
    print("\n📊 Data to transfer:")
    chromadb_count = transfer_chromadb_to_cloud()
    sqlite_count = transfer_sqlite_to_cloud()

    print(f"\n✅ Ready to transfer:")
    print(f"  - {chromadb_count} knowledge items from ChromaDB")
    print(f"  - {sqlite_count} records from SQLite databases")
    print(f"\n💡 Bob & Alice will share this data in Cloud SQL\!")
    print("\n⚠️  To complete transfer, need Cloud SQL password")
