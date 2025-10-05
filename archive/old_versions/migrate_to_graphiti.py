#!/usr/bin/env python3
"""
Migrate all existing Bob's Brain data to Graphiti
"""

import os
import asyncio
from datetime import datetime
from graphiti_core import Graphiti
from google.cloud import firestore
import json

# Set up environment - API key must be provided externally
# os.environ['OPENAI_API_KEY'] = 'your-api-key-here'

async def migrate_firestore_to_graphiti():
    """Migrate Firestore data to Graphiti"""
    
    print("=" * 60)
    print("🚀 MIGRATING BOB'S BRAIN DATA TO GRAPHITI")
    print("=" * 60)
    
    # Initialize Graphiti with GCP Neo4j
    print("\n1. Connecting to Graphiti...")
    graphiti = Graphiti(
        uri="bolt://10.128.0.2:7687",
        user="neo4j",
        password="<REDACTED_NEO4J_PASSWORD>"
    )
    print("   ✅ Connected to Graphiti")
    
    # Initialize Firestore
    print("\n2. Connecting to Firestore...")
    try:
        fs = firestore.Client(project='diagnostic-pro-mvp')
        print("   ✅ Connected to Firestore")
    except Exception as e:
        print(f"   ⚠️  Firestore connection failed: {e}")
        fs = None
    
    migrated_count = 0
    
    # Add some initial knowledge about the system
    print("\n3. Adding foundational knowledge...")
    
    foundational_episodes = [
        {
            "name": "system_overview",
            "body": "Bob's Brain is an AI assistant for DiagnosticPro, owned by Jeremy Longshore. It uses a Graphiti knowledge graph backed by Neo4j on Google Cloud Platform.",
            "description": "System overview"
        },
        {
            "name": "jeremy_info",
            "body": "Jeremy Longshore is the owner of DiagnosticPro. He has 15 years of business experience and previously worked in trucking and BBI industries.",
            "description": "Owner information"
        },
        {
            "name": "diagnosticpro_info",
            "body": "DiagnosticPro is a company that protects customers from automotive repair shop overcharges. It uses AI technology to verify repair quotes and has saved customers thousands of dollars.",
            "description": "Company information"
        },
        {
            "name": "technical_stack",
            "body": "The technical infrastructure includes: Google Cloud Run for hosting, Neo4j for graph database, Graphiti for knowledge management, Vertex AI for machine learning, and Slack for user interface.",
            "description": "Technical infrastructure"
        },
        {
            "name": "bob_capabilities",
            "body": "Bob can: remember conversations with temporal context, extract entities and relationships, search semantic knowledge, provide intelligent responses, and learn from interactions.",
            "description": "Bob's capabilities"
        }
    ]
    
    for episode in foundational_episodes:
        try:
            result = await graphiti.add_episode(
                name=episode["name"],
                episode_body=episode["body"],
                source_description=episode["description"],
                reference_time=datetime.now()
            )
            print(f"   ✅ Added: {episode['name']}")
            migrated_count += 1
        except Exception as e:
            print(f"   ❌ Failed to add {episode['name']}: {e}")
    
    # Migrate Firestore data if available
    if fs:
        print("\n4. Migrating Firestore documents...")
        try:
            # Try to get shared_knowledge collection
            collection = fs.collection('shared_knowledge')
            docs = collection.stream()
            
            for doc in docs:
                try:
                    data = doc.to_dict()
                    episode_body = data.get('content', '')
                    if not episode_body:
                        episode_body = json.dumps(data)
                    
                    result = await graphiti.add_episode(
                        name=f"firestore_{doc.id}",
                        episode_body=episode_body,
                        source_description=f"Migrated from Firestore: {doc.id}",
                        reference_time=data.get('timestamp', datetime.now())
                    )
                    print(f"   ✅ Migrated: {doc.id[:50]}...")
                    migrated_count += 1
                except Exception as e:
                    print(f"   ⚠️  Failed to migrate {doc.id}: {e}")
                    
        except Exception as e:
            print(f"   ⚠️  Could not access Firestore collection: {e}")
    
    # Test search functionality
    print("\n5. Testing Graphiti search...")
    test_queries = [
        "Who is Jeremy Longshore?",
        "What is DiagnosticPro?",
        "What technology does Bob use?"
    ]
    
    for query in test_queries:
        try:
            results = await graphiti.search(query, num_results=3)
            print(f"   Q: {query}")
            if results:
                print(f"   A: Found {len(results)} relevant results")
            else:
                print(f"   A: No results found")
        except Exception as e:
            print(f"   ❌ Search failed: {e}")
    
    # Get statistics
    print("\n6. Graph Statistics...")
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://10.128.0.2:7687", auth=("neo4j", "<REDACTED_NEO4J_PASSWORD>"))
        
        with driver.session() as session:
            # Count nodes
            node_count = session.run("MATCH (n) RETURN count(n) as count").single()['count']
            # Count relationships
            edge_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']
            
            print(f"   Total nodes: {node_count}")
            print(f"   Total relationships: {edge_count}")
            print(f"   Episodes migrated: {migrated_count}")
        
        driver.close()
    except Exception as e:
        print(f"   ⚠️  Could not get statistics: {e}")
    
    # Close Graphiti connection
    await graphiti.close()
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print(f"   Migrated {migrated_count} episodes to Graphiti")
    print("   Bob's Brain is now powered by a knowledge graph!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(migrate_firestore_to_graphiti())