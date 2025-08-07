#!/usr/bin/env python3
"""
Add all project reports and documentation to Bob's Firestore knowledge database
So Bob can search and access all the information about his migration and current status
"""

import json
import time
from google.cloud import firestore
from sentence_transformers import SentenceTransformer
import os

def add_reports_to_bob_knowledge():
    """Add all project reports to Bob's searchable knowledge base"""

    print("📚 ADDING PROJECT REPORTS TO BOB'S KNOWLEDGE BASE")
    print("=" * 60)

    # Initialize Firestore client
    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Initialize sentence transformer for embeddings
    print("🤖 Loading sentence transformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Reports to add to Bob's knowledge
    reports_to_add = [
        {
            "file": "/home/jeremylongshore/bobs_brain/COMPREHENSIVE_PROJECT_HANDOFF_REPORT.md",
            "title": "Bob's Brain Migration Project - Complete Report",
            "category": "project_documentation",
            "priority": "critical"
        },
        {
            "file": "/home/jeremylongshore/bobs_brain/CORRECTED_MIGRATION_FINAL_REPORT.md",
            "title": "Bob's Data Correction - 1925 to 970 Knowledge Items",
            "category": "data_correction",
            "priority": "critical"
        },
        {
            "file": "/home/jeremylongshore/bobs_brain/BOB_UPDATED_STATUS_FINAL.md",
            "title": "Bob's Current Status and Remaining Tasks",
            "category": "current_status",
            "priority": "high"
        },
        {
            "file": "/home/jeremylongshore/bobs_brain/MIGRATION_COMPLETE_SUMMARY.md",
            "title": "Bob's Firestore Migration Summary",
            "category": "migration_summary",
            "priority": "high"
        },
        {
            "file": "/home/jeremylongshore/bobs_brain/agentsmithy_quirks_analysis.md",
            "title": "AgentSmithy Analysis for Alice Integration",
            "category": "alice_integration",
            "priority": "medium"
        },
        {
            "file": "/home/jeremylongshore/bobs_brain/cloud_sql_status.md",
            "title": "Cloud SQL Investigation and Cost Optimization",
            "category": "cost_optimization",
            "priority": "medium"
        }
    ]

    knowledge_collection = client.collection('knowledge')
    added_count = 0

    for report_info in reports_to_add:
        try:
            # Read report content
            if not os.path.exists(report_info["file"]):
                print(f"❌ File not found: {report_info['file']}")
                continue

            with open(report_info["file"], 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                print(f"❌ Empty file: {report_info['file']}")
                continue

            # Create document ID based on filename
            filename = os.path.basename(report_info["file"]).replace('.md', '')
            doc_id = f"project_report_{filename.lower()}"

            # Check if already exists
            existing_doc = knowledge_collection.document(doc_id).get()
            if existing_doc.exists:
                print(f"⚠️  Already exists, updating: {report_info['title']}")

            # Generate embedding
            print(f"🔍 Processing: {report_info['title']}")
            embedding = model.encode(content).tolist()

            # Prepare document
            doc_data = {
                'content': content,
                'embedding': embedding,
                'metadata': {
                    'source': 'project_report',
                    'title': report_info['title'],
                    'category': report_info['category'],
                    'priority': report_info['priority'],
                    'file_path': report_info['file'],
                    'added_at': time.time(),
                    'added_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'content_length': len(content),
                    'embedding_model': 'all-MiniLM-L6-v2'
                },
                'timestamp': firestore.SERVER_TIMESTAMP
            }

            # Add to Firestore
            knowledge_collection.document(doc_id).set(doc_data)
            added_count += 1
            print(f"✅ Added: {report_info['title']}")

        except Exception as e:
            print(f"❌ Error processing {report_info['title']}: {e}")

    # Update knowledge count
    total_knowledge = len(list(knowledge_collection.stream()))

    print(f"\n📊 RESULTS:")
    print(f"✅ Reports added to Bob's knowledge: {added_count}")
    print(f"📚 Total knowledge items now: {total_knowledge}")
    print(f"🔍 Bob can now search for:")
    print("   - Migration project details")
    print("   - Data correction information")
    print("   - Current status and tasks")
    print("   - Alice integration plans")
    print("   - Cost optimization results")

    return added_count, total_knowledge

def test_bob_report_search():
    """Test that Bob can now search for project information"""

    print("\n🧪 TESTING BOB'S REPORT SEARCH")
    print("=" * 40)

    from bob_firestore_tools import BobFirestoreTools
    tools = BobFirestoreTools()

    test_queries = [
        "migration project status",
        "data correction 970 knowledge items",
        "Alice integration deployment",
        "cost optimization results",
        "AgentSmithy quirks analysis"
    ]

    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        result = tools.search_knowledge(query)
        if "results:" in result.lower() or len(result) > 100:
            print(f"✅ Bob found information about: {query}")
        else:
            print(f"⚠️  Limited results for: {query}")

    return True

if __name__ == "__main__":
    # Add reports to Bob's knowledge
    added, total = add_reports_to_bob_knowledge()

    if added > 0:
        # Test Bob's ability to search project info
        test_bob_report_search()

        print(f"\n🎉 SUCCESS: Bob now knows about his migration project!")
        print(f"📚 {added} reports added to his searchable knowledge")
        print(f"🤖 Bob can now answer questions about:")
        print("   - His Firestore migration")
        print("   - Data correction from 1,925 to 970 items")
        print("   - Current operational status")
        print("   - Alice integration plans")
        print("   - Cost optimization achievements")
        print("   - AgentSmithy analysis")

    else:
        print("❌ No reports were added. Check file paths and permissions.")
