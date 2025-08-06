#!/usr/bin/env python3
"""
Add GCP Audit Report to Bob's Brain
Date: August 6, 2025
Time: 21:45 UTC
"""

import chromadb
from datetime import datetime

def add_gcp_audit_to_bob():
    """Add comprehensive GCP audit report to Bob's knowledge base"""

    print("🧠 Adding GCP Audit Report to Bob's Brain...")

    # Connect to Bob's brain
    client = chromadb.PersistentClient(path='/home/jeremylongshore/.bob_brain/chroma')
    collection = client.get_collection('bob_knowledge')

    # GCP Audit knowledge items
    audit_knowledge = [
        {
            "content": "GCP INFRASTRUCTURE AUDIT SUMMARY (Aug 6, 2025): jeremylongshore@gmail.com has 5 active GCP projects: bobs-house-ai (AI development hub, 9 Cloud Run services), diagnostic-pro-mvp (production system with thebeast n2-standard-4 VM running 24/7), diagnostic-pro-legacy (archived), gen-lang-client-0624266098 (Gemini API), fabled-seeker-fsz74 (inactive). Total estimated monthly cost $230-280 with thebeast VM being primary cost driver at ~$200/month.",
            "metadata": {
                "type": "infrastructure_audit",
                "project": "GCP_Platform",
                "component": "Multi_Project_Overview",
                "date": "2025-08-06",
                "priority": "CRITICAL"
            }
        },
        {
            "content": "THEBEAST VM ANALYSIS: diagnostic-pro-mvp project VM 'thebeast' specs: n2-standard-4 (4 vCPUs, 16GB RAM), 200GB disk, external IP 35.225.115.164, running 24/7 in us-central1-a. User upgraded from 8GB RAM due to memory constraints. n2-standard-4 provides 16GB RAM vs previous 8GB. Cost ~$200/month. Status: RUNNING and justified for memory-intensive workloads.",
            "metadata": {
                "type": "compute_analysis",
                "project": "Diagnostic_Pro_MVP",
                "component": "VM_Thebeast",
                "specs": "n2-standard-4_16GB_RAM",
                "date": "2025-08-06"
            }
        },
        {
            "content": "BOBS HOUSE AI PROJECT INVENTORY: 9 Cloud Run services deployed - alice-cloud-bestie, bob-preview-stable, bobs-ai-house, bobs-brain-central (all operational), mcp-coordinator (FAILED - needs attention), preview-link-1/2/3, startaitools-prod. 5 storage buckets active. Perfect for deploying Bob Slack agent via Cloud Run. Project #157908567967, us-central1 region, billing account 01AE21-39A539-C37223.",
            "metadata": {
                "type": "project_inventory",
                "project": "Bobs_House_AI",
                "component": "Cloud_Run_Services",
                "date": "2025-08-06"
            }
        },
        {
            "content": "GCP SECURITY ASSESSMENT: IAM properly configured with owner-level access, 8 specialized service accounts in diagnostic-pro-mvp (diagnosticpro-app, diagnosticpro-analytics, diagnosticpro-monitoring, etc.), multiple project isolation maintained. Concerns: overprivileged access patterns, failed mcp-coordinator service, legacy terminated VM still consuming resources. External IP on production VM. Recommendations: enable OS Login, review IAM roles, implement network security.",
            "metadata": {
                "type": "security_assessment",
                "project": "GCP_Platform",
                "component": "IAM_Security",
                "date": "2025-08-06"
            }
        },
        {
            "content": "GCP BILLING ANALYSIS (Aug 6, 2025): Primary billing account 01AE21-39A539-C37223 covers bobs-house-ai, diagnostic-pro-legacy, diagnostic-pro-mvp. Estimated monthly costs: thebeast VM ~$200 (justified for 16GB RAM upgrade from 8GB), Cloud Run services ~$20-50, Storage ~$10-30. Total ~$230-280/month. gen-lang-client billing DISABLED. Cost optimization: Bob deployment via Cloud Run would be $5-15/month vs VM approach.",
            "metadata": {
                "type": "billing_analysis",
                "project": "GCP_Platform",
                "component": "Cost_Management",
                "monthly_cost": "$230-280",
                "date": "2025-08-06"
            }
        },
        {
            "content": "BOB DEPLOYMENT STRATEGY GCP: Recommended deployment via Cloud Run in bobs-house-ai project. Command: 'gcloud run deploy bob-slack-agent --source . --project bobs-house-ai --region us-central1 --memory 512Mi --set-env-vars SLACK_BOT_TOKEN=xxx,SLACK_APP_TOKEN=xxx'. Advantages: pay-per-use ($0 when idle), auto-scaling, existing infrastructure. Cost: ~$5-15/month for Slack bot vs $200+ VM overhead. thebeast VM justified for memory-intensive tasks, not optimal for lightweight Slack bot.",
            "metadata": {
                "type": "deployment_strategy",
                "project": "Bob_Agent",
                "component": "Cloud_Run_Deployment",
                "estimated_cost": "$5-15_monthly",
                "date": "2025-08-06"
            }
        }
    ]

    # Add each knowledge item
    added_count = 0
    for item in audit_knowledge:
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
                    ids=[f"gcp_audit_{item['metadata']['component'].lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"]
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
    print(f"📊 Added {added_count} new GCP audit items")

    return added_count > 0

if __name__ == "__main__":
    print("🔍 Adding comprehensive GCP audit report to Bob's Brain...")
    success = add_gcp_audit_to_bob()
    if success:
        print("\n✅ GCP audit report successfully integrated into Bob's Brain!")
    else:
        print("\n✅ Bob already has all GCP audit information!")
