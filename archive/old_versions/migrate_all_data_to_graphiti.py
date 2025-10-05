#!/usr/bin/env python3
"""
Comprehensive migration of ALL Bob's Brain data to Graphiti
Checks all possible data sources and migrates everything
"""

import os
import sys
import json
import asyncio
from datetime import datetime
import chromadb
from pathlib import Path

# This script will be run on Cloud Run where Neo4j is accessible
# For local testing, it will check what data exists

def check_chromadb_data():
    """Check all ChromaDB locations for data"""
    chroma_locations = [
        './chroma_data',
        os.path.expanduser('~/.bob_brain/chroma'),
        './chroma',
        '../chroma_data'
    ]
    
    all_data = []
    
    for location in chroma_locations:
        if os.path.exists(location):
            try:
                print(f"\nChecking ChromaDB at {location}...")
                client = chromadb.PersistentClient(path=location)
                collections = client.list_collections()
                
                for col in collections:
                    collection = client.get_collection(col.name)
                    count = collection.count()
                    
                    if count > 0:
                        print(f"  Found {count} documents in collection '{col.name}'")
                        
                        # Get all documents
                        data = collection.get()
                        documents = data.get('documents', [])
                        metadatas = data.get('metadatas', [])
                        ids = data.get('ids', [])
                        
                        for doc, meta, doc_id in zip(documents, metadatas, ids):
                            all_data.append({
                                'source': f'ChromaDB/{col.name}',
                                'id': doc_id,
                                'content': doc,
                                'metadata': meta,
                                'location': location
                            })
            except Exception as e:
                print(f"  Error reading ChromaDB at {location}: {e}")
    
    return all_data

def check_firestore_data():
    """Check Firestore for data"""
    firestore_data = []
    
    try:
        from google.cloud import firestore
        
        # Try different project IDs
        projects = ['diagnostic-pro-mvp', 'bobs-house-ai']
        
        for project_id in projects:
            try:
                print(f"\nChecking Firestore in project {project_id}...")
                fs = firestore.Client(project=project_id)
                
                # Try to list collections
                collections = fs.collections()
                for collection in collections:
                    docs = list(collection.stream())
                    if docs:
                        print(f"  Found {len(docs)} documents in collection '{collection.id}'")
                        
                        for doc in docs:
                            data = doc.to_dict()
                            firestore_data.append({
                                'source': f'Firestore/{project_id}/{collection.id}',
                                'id': doc.id,
                                'content': data.get('content', json.dumps(data)),
                                'metadata': {
                                    'project': project_id,
                                    'collection': collection.id,
                                    'timestamp': data.get('timestamp', '')
                                }
                            })
            except Exception as e:
                print(f"  Could not access Firestore in {project_id}: {e}")
                
    except ImportError:
        print("  Firestore library not available")
    
    return firestore_data

def check_local_files():
    """Check for any JSON or text files with Bob's data"""
    local_data = []
    
    # Look for knowledge files
    knowledge_files = [
        'knowledge_base.json',
        'bob_knowledge.json',
        'shared_knowledge.json',
        'data/knowledge.json'
    ]
    
    for file_path in knowledge_files:
        if os.path.exists(file_path):
            print(f"\nFound local file: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                if isinstance(data, list):
                    for item in data:
                        local_data.append({
                            'source': f'LocalFile/{file_path}',
                            'id': item.get('id', 'unknown'),
                            'content': item.get('content', str(item)),
                            'metadata': {'file': file_path}
                        })
                elif isinstance(data, dict):
                    local_data.append({
                        'source': f'LocalFile/{file_path}',
                        'id': 'file_content',
                        'content': json.dumps(data),
                        'metadata': {'file': file_path}
                    })
                    
                print(f"  Loaded {len(local_data)} items from {file_path}")
                
            except Exception as e:
                print(f"  Error reading {file_path}: {e}")
    
    return local_data

async def migrate_to_graphiti(all_data):
    """Migrate all collected data to Graphiti"""
    
    if not all_data:
        print("\n⚠️ No data found to migrate!")
        return
    
    print(f"\n📊 Ready to migrate {len(all_data)} total items to Graphiti")
    
    # This will only work when deployed to Cloud Run with proper access
    try:
        from graphiti_core import Graphiti
        
        print("\nConnecting to Graphiti...")
        graphiti = Graphiti(
            uri=os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687'),
            user=os.environ.get('NEO4J_USER', 'neo4j'),
            password=os.environ.get('NEO4J_PASSWORD', '<REDACTED_NEO4J_PASSWORD>')
        )
        
        print("✅ Connected to Graphiti")
        
        # Migrate data in batches
        batch_size = 10
        migrated = 0
        
        for i in range(0, len(all_data), batch_size):
            batch = all_data[i:i+batch_size]
            
            for item in batch:
                try:
                    # Create episode from the data
                    episode_name = f"{item['source']}_{item['id']}"
                    episode_body = item['content']
                    
                    # Add metadata as part of the body if present
                    if item.get('metadata'):
                        episode_body += f"\n\nMetadata: {json.dumps(item['metadata'])}"
                    
                    await graphiti.add_episode(
                        name=episode_name[:100],  # Limit name length
                        episode_body=episode_body,
                        source_description=item['source'],
                        reference_time=datetime.now()
                    )
                    
                    migrated += 1
                    if migrated % 10 == 0:
                        print(f"  Migrated {migrated}/{len(all_data)} items...")
                        
                except Exception as e:
                    print(f"  Failed to migrate {item['id']}: {e}")
        
        await graphiti.close()
        
        print(f"\n✅ Successfully migrated {migrated}/{len(all_data)} items to Graphiti!")
        
    except Exception as e:
        print(f"\n❌ Cannot connect to Graphiti: {e}")
        print("\nTo complete migration, this script needs to be run where Neo4j is accessible.")
        print("The data has been collected and is ready for migration.")

def main():
    """Main migration function"""
    print("=" * 60)
    print("🔍 SEARCHING FOR ALL BOB'S BRAIN DATA")
    print("=" * 60)
    
    # Collect all data
    all_data = []
    
    # Check ChromaDB
    chroma_data = check_chromadb_data()
    all_data.extend(chroma_data)
    
    # Check Firestore
    firestore_data = check_firestore_data()
    all_data.extend(firestore_data)
    
    # Check local files
    local_data = check_local_files()
    all_data.extend(local_data)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DATA SUMMARY")
    print("=" * 60)
    print(f"ChromaDB documents: {len(chroma_data)}")
    print(f"Firestore documents: {len(firestore_data)}")
    print(f"Local file items: {len(local_data)}")
    print(f"TOTAL items found: {len(all_data)}")
    
    if all_data:
        # Save data locally for backup
        backup_file = f"bob_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w') as f:
            json.dump(all_data, f, indent=2, default=str)
        print(f"\n💾 Data backed up to: {backup_file}")
        
        # Attempt migration
        print("\n🚀 Starting migration to Graphiti...")
        asyncio.run(migrate_to_graphiti(all_data))
    else:
        print("\n⚠️ No data found to migrate!")
        print("\nPossible reasons:")
        print("1. Data might already be migrated")
        print("2. Data might be in a different location")
        print("3. The 900+ items might be in production Firestore (not accessible locally)")
    
    print("\n" + "=" * 60)
    print("Migration process complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()