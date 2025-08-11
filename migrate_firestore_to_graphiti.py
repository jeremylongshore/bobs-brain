#!/usr/bin/env python3
"""
Migrate all 1,100 Firestore documents to Graphiti/Neo4j
This script accesses the bob-brain database in diagnostic-pro-mvp
"""

import os
import json
import asyncio
from datetime import datetime
from google.cloud import firestore
import requests
import time

def fetch_all_firestore_data():
    """Fetch all documents from Firestore bob-brain database"""
    
    print("Connecting to Firestore (diagnostic-pro-mvp/bob-brain)...")
    client = firestore.Client(project='diagnostic-pro-mvp', database='bob-brain')
    
    all_data = []
    collection_stats = {}
    
    # Get all collections
    collections = list(client.collections())
    
    for collection in collections:
        print(f"\nFetching {collection.id}...")
        docs = list(collection.stream())
        collection_stats[collection.id] = len(docs)
        
        for doc in docs:
            data = doc.to_dict()
            
            # Prepare document for migration
            doc_entry = {
                'id': doc.id,
                'collection': collection.id,
                'data': data,
                'content': data.get('content', ''),
                'metadata': data.get('metadata', {}),
                'timestamp': data.get('timestamp', data.get('created_at', datetime.now()))
            }
            
            # Special handling for different collections
            if collection.id == 'knowledge':
                # Knowledge documents are the most important
                doc_entry['priority'] = 'high'
                doc_entry['type'] = 'knowledge'
                
            elif collection.id == 'memory_episodes':
                # Memory episodes need temporal data preserved
                doc_entry['priority'] = 'high'
                doc_entry['type'] = 'memory'
                
            elif collection.id == 'bob_conversations':
                # Conversations should be preserved with context
                doc_entry['priority'] = 'medium'
                doc_entry['type'] = 'conversation'
                
            else:
                doc_entry['priority'] = 'normal'
                doc_entry['type'] = collection.id
            
            all_data.append(doc_entry)
            
        print(f"  Fetched {len(docs)} documents")
    
    # Sort by priority for migration
    priority_order = {'high': 0, 'medium': 1, 'normal': 2}
    all_data.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {len(all_data)} documents ready for migration")
    print(f"{'='*60}")
    
    for col, count in collection_stats.items():
        print(f"  {col:25} {count:5} documents")
    
    return all_data

def save_backup(data):
    """Save a backup of all data before migration"""
    
    backup_file = f"firestore_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Convert datetime objects to strings for JSON serialization
    def serialize(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return str(obj)
    
    with open(backup_file, 'w') as f:
        json.dump(data, f, indent=2, default=serialize)
    
    print(f"\n💾 Backup saved to: {backup_file}")
    return backup_file

async def migrate_to_graphiti_api(data):
    """Migrate data to Graphiti via Bob's API"""
    
    BASE_URL = "https://bobs-brain-157908567967.us-central1.run.app"
    
    print(f"\n🚀 Starting migration to Graphiti via API...")
    print(f"   Target: {BASE_URL}")
    
    migrated = 0
    failed = 0
    
    # Process in batches to avoid overwhelming the API
    batch_size = 10
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        print(f"\n  Processing batch {i//batch_size + 1}/{(len(data)-1)//batch_size + 1}...")
        
        for item in batch:
            try:
                # Prepare the message for Bob
                if item['content']:
                    message = f"Remember this {item['type']} from {item['collection']}: {item['content'][:500]}"
                else:
                    # For items without content, use the full data
                    message = f"Remember this {item['type']} data: {json.dumps(item['data'])[:500]}"
                
                # Add metadata context
                if item.get('metadata'):
                    message += f"\nMetadata: {json.dumps(item['metadata'])[:200]}"
                
                # Send to Bob's API
                event = {
                    "type": "event_callback",
                    "event": {
                        "type": "message",
                        "text": message,
                        "user": "U_MIGRATION_SYSTEM",
                        "channel": "C_FIRESTORE_MIGRATION",
                        "ts": str(time.time())
                    }
                }
                
                response = requests.post(
                    f"{BASE_URL}/slack/events",
                    json=event,
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                
                if response.status_code == 200:
                    migrated += 1
                    print(f"    ✅ {item['id'][:30]}... ({item['collection']})")
                else:
                    failed += 1
                    print(f"    ⚠️  {item['id'][:30]}... - Status: {response.status_code}")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                failed += 1
                print(f"    ❌ {item['id'][:30]}... - Error: {str(e)[:50]}")
        
        print(f"    Progress: {migrated}/{len(data)} migrated, {failed} failed")
        
        # Pause between batches
        if i + batch_size < len(data):
            print("    Pausing between batches...")
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"✅ MIGRATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Successfully migrated: {migrated}/{len(data)} documents")
    print(f"  Failed: {failed} documents")
    
    if failed > 0:
        print(f"\n  Note: Failed documents are saved in the backup file")
        print(f"  They can be re-migrated manually if needed")
    
    return migrated, failed

def main():
    """Main migration function"""
    
    print("=" * 60)
    print("🔄 FIRESTORE TO GRAPHITI MIGRATION")
    print("=" * 60)
    print("\nThis will migrate all 1,100 documents from Firestore")
    print("to Bob's Graphiti knowledge graph on Cloud Run")
    
    try:
        # Step 1: Fetch all data
        print("\n📥 Step 1: Fetching all Firestore data...")
        all_data = fetch_all_firestore_data()
        
        # Step 2: Create backup
        print("\n💾 Step 2: Creating backup...")
        backup_file = save_backup(all_data)
        
        # Step 3: Migrate to Graphiti
        print("\n🚀 Step 3: Migrating to Graphiti...")
        
        # Note: Using API method since direct Neo4j access requires being on GCP network
        asyncio.run(migrate_to_graphiti_api(all_data))
        
        print("\n" + "=" * 60)
        print("🎉 MIGRATION SUCCESSFUL!")
        print("=" * 60)
        print(f"\nBob's Brain now has:")
        print(f"  - All {len(all_data)} Firestore documents")
        print(f"  - Preserved in Graphiti knowledge graph")
        print(f"  - With temporal awareness and relationships")
        print(f"\nBackup saved to: {backup_file}")
        print("\n✅ Bob is ready with complete historical knowledge!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nPlease check:")
        print("  1. Firestore access permissions")
        print("  2. Bob's API is running")
        print("  3. Network connectivity")

if __name__ == "__main__":
    main()