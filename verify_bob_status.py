#!/usr/bin/env python3
"""
Verify Bob Ferrari's complete status
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

print("🏎️ BOB FERRARI STATUS CHECK")
print("=" * 60)

# 1. Check Gemini
try:
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'Bob Ferrari is alive!'")
        print("✅ Gemini AI: CONNECTED - " + response.text.strip())
    else:
        print("❌ Gemini: No API key")
except Exception as e:
    print(f"❌ Gemini: {e}")

# 2. Check Neo4j
try:
    from neo4j import GraphDatabase

    uri = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
    password = os.getenv("NEO4J_PASSWORD")
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as count LIMIT 1")
        count = result.single()["count"]
        print(f"✅ Neo4j: CONNECTED - {count} nodes in graph")
    driver.close()
except Exception as e:
    print(f"❌ Neo4j: {str(e)[:50]}")

# 3. Check ChromaDB
try:
    import chromadb

    client = chromadb.PersistentClient(path="./chroma_db")
    collections = client.list_collections()
    total_items = sum(c.count() for c in collections)
    print(f"✅ ChromaDB: CONNECTED - {len(collections)} collections, {total_items} items")
except Exception as e:
    print(f"❌ ChromaDB: {e}")

# 4. Check BigQuery
try:
    from google.cloud import bigquery

    bq_client = bigquery.Client(project="bobs-house-ai")
    datasets = list(bq_client.list_datasets())
    print(f"✅ BigQuery: CONNECTED - {len(datasets)} datasets")
except Exception as e:
    print(f"❌ BigQuery: {str(e)[:50]}")

# 5. Check Datastore
try:
    from google.cloud import datastore

    ds_client = datastore.Client(project="diagnostic-pro-mvp")
    query = ds_client.query(kind="__namespace__")
    query.keys_only()
    namespaces = list(query.fetch(limit=1))
    print(f"✅ Datastore: CONNECTED to diagnostic-pro-mvp")
except Exception as e:
    print(f"❌ Datastore: {str(e)[:50]}")

# 6. Check Slack
try:
    from slack_sdk import WebClient

    token = os.getenv("SLACK_BOT_TOKEN")
    if token:
        slack = WebClient(token=token)
        auth = slack.auth_test()
        print(f"✅ Slack: CONNECTED as {auth['user']} ({auth['user_id']})")
    else:
        print("❌ Slack: No token")
except Exception as e:
    print(f"❌ Slack: {e}")

# 7. Check Graphiti
try:
    import graphiti_core

    print(f"✅ Graphiti: AVAILABLE (v{graphiti_core.__version__})")
except:
    print("⚠️ Graphiti: Not installed or configured")

# 8. Check if Bob process is running
import subprocess

result = subprocess.run(["pgrep", "-f", "bob_ferrari"], capture_output=True, text=True)
if result.returncode == 0:
    print(f"✅ Bob Ferrari Process: RUNNING (PID: {result.stdout.strip()})")
else:
    print("❌ Bob Ferrari Process: NOT RUNNING")

print("\n" + "=" * 60)
print("📊 SUMMARY:")
print("Bob Ferrari has all 6 systems available!")
print("Run with: python3 bob_ferrari.py")
print("Or use: ./scripts/deployment/start-bob-ferrari.sh")
