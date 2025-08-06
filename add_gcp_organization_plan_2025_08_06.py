#!/usr/bin/env python3
"""
Add GCP Organization Plan to Bob's Brain
Date: August 6, 2025
Context: Alice (GCP Agent) & Bob (Extended Brain) remain separate, communicate via MCP
"""

import chromadb
from datetime import datetime

def add_gcp_organization_to_bob():
    """Add comprehensive GCP organization plan to Bob's knowledge base"""

    print("🧠 Adding GCP Organization Plan to Bob's Brain...")

    # Connect to Bob's brain
    client = chromadb.PersistentClient(path='/home/jeremylongshore/.bob_brain/chroma')
    collection = client.get_collection('bob_knowledge')

    # GCP Organization knowledge items
    organization_knowledge = [
        {
            "content": "GCP PROFIT MACHINE ORGANIZATION PLAN: Structure - JEREMY LONGSHORE ENTERPRISES with 3 divisions: PROFIT-MACHINES (diagnostic-pro-mvp $210/month justified, restaurant-ops BBI, trucking-logistics), AI-OPERATIONS (bobs-house-ai $50-135/month for Alice & Bob agents), ARCHIVES (diagnostic-pro-legacy $5/month). Total monthly: $265-350. Cleanup opportunities: delete empty buckets save $15/month, fix mcp-coordinator, consolidate preview services.",
            "metadata": {
                "type": "organization_plan",
                "project": "GCP_Organization",
                "component": "Business_Structure",
                "date": "2025-08-06",
                "priority": "CRITICAL"
            }
        },
        {
            "content": "ALICE & BOB ARCHITECTURE: Alice = Full Google Cloud AI agent expert (deployed in bobs-house-ai), Bob = Jeremy's extended brain/context manager (separate system). Future communication via MCP (Model Context Protocol). Alice handles GCP operations, Bob manages business context and knowledge. Both are AI besties but maintain separation of concerns. Alice at alice-cloud-bestie service (1GB RAM), Bob needs Cloud Run deployment (512MB).",
            "metadata": {
                "type": "ai_architecture",
                "project": "AI_Agents",
                "component": "Alice_Bob_Separation",
                "date": "2025-08-06"
            }
        },
        {
            "content": "DIAGNOSTICPRO STATUS: MVP 2.0 nearly complete (90%), construction website live at diagnosticpro.io, workflow being finalized for rollout. Revenue model: $4.99 Equipment Diagnostic, $6.99 Quote Verification, $7.99 Emergency Triage. This is ONE of many upcoming projects. Production deployment on diagnostic-pro-mvp project with thebeast VM (16GB justified for workload).",
            "metadata": {
                "type": "project_status",
                "project": "DiagnosticPro",
                "component": "MVP_2.0_Status",
                "date": "2025-08-06"
            }
        },
        {
            "content": "GCP WASTE REDUCTION PLAN: Immediate deletions - alice-staging-bucket-jeremy (empty), diagnostic-pro-legacy_cloudbuild (empty), diagnosticpro-legacy-v2-uploads (empty), gcf-v2-sources/uploads (1KB each), diagnosticpro-vm-migration-temp (800MB after migration confirmed). Keep: cloudbuild artifacts (active), run-sources (active deployments). Estimated savings $15-20/month.",
            "metadata": {
                "type": "cost_optimization",
                "project": "GCP_Platform",
                "component": "Waste_Reduction",
                "date": "2025-08-06"
            }
        },
        {
            "content": "BOBS-HOUSE-AI SERVICE BREAKDOWN: 9 Cloud Run services - alice-cloud-bestie (1GB Alice agent), bob-preview-stable (512MB), bobs-brain-central (512MB), bobs-ai-house (512MB), mcp-coordinator (256MB FAILED needs fix), preview-link-1/2/3 (512MB each redundant), startaitools-prod (512MB). Monthly cost $50-135. Recommendation: consolidate preview links, fix mcp-coordinator for Alice-Bob communication.",
            "metadata": {
                "type": "service_inventory",
                "project": "Bobs_House_AI",
                "component": "Cloud_Run_Services",
                "date": "2025-08-06"
            }
        }
    ]

    # Add each knowledge item
    added_count = 0
    for item in organization_knowledge:
        try:
            # Check if this knowledge already exists
            existing = collection.query(
                query_texts=[item["content"][:100]],
                n_results=1
            )

            if not existing['documents'] or not existing['documents'][0]:
                # Add new knowledge
                collection.add(
                    documents=[item["content"]],
                    metadatas=[item["metadata"]],
                    ids=[f"gcp_org_{item['metadata']['component'].lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"]
                )
                print(f"✅ Added to Bob's brain: {item['metadata']['component']}")
                added_count += 1
            else:
                print(f"📝 Already in Bob's brain: {item['metadata']['component']}")

        except Exception as e:
            print(f"❌ Error adding {item['metadata']['component']}: {e}")

    # Get total count
    total_items = collection.count()
    print(f"\n🧠 Bob's brain now contains {total_items} knowledge items")
    print(f"📊 Added {added_count} new GCP organization items")

    return added_count > 0

if __name__ == "__main__":
    print("📋 Adding GCP Organization Plan to Bob's Brain...")
    success = add_gcp_organization_to_bob()
    if success:
        print("\n✅ GCP organization plan successfully integrated into Bob's Brain!")
    else:
        print("\n✅ Bob already has all GCP organization information!")
