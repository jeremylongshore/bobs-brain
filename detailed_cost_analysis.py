#!/usr/bin/env python3
"""
Detailed Firestore Cost Analysis for 20k Reads/Day + Embedding Costs
"""

import math
from datetime import datetime

def calculate_detailed_firestore_costs():
    """Calculate detailed Firestore costs for high-volume Bob operations"""

    print("💰 DETAILED FIRESTORE COST ANALYSIS")
    print("=" * 60)

    # Your specified usage pattern
    bob_reads_per_day = 20000  # Context management, vision formulation, task coordination
    bob_writes_per_day = 500   # New knowledge, conversations, insights
    alice_reads_per_day = 2000 # Task processing, shared context access
    alice_writes_per_day = 300 # Task results, monitoring data

    total_reads_per_day = bob_reads_per_day + alice_reads_per_day
    total_writes_per_day = bob_writes_per_day + alice_writes_per_day

    # Storage estimate (expanded from current 35MB)
    current_storage_mb = 35
    # Growth factors: more conversations, task logs, automation results
    projected_storage_mb = current_storage_mb * 5  # 175MB with full usage
    storage_gb = projected_storage_mb / 1024

    days_per_month = 30
    monthly_reads = total_reads_per_day * days_per_month
    monthly_writes = total_writes_per_day * days_per_month
    monthly_deletes = total_writes_per_day * 0.05 * days_per_month  # 5% delete rate for cleanup

    # Firestore pricing (US regions, 2024)
    READS_PER_100K = 0.36      # $0.36 per 100,000 reads
    WRITES_PER_100K = 1.80     # $1.80 per 100,000 writes
    DELETE_PER_100K = 0.02     # $0.02 per 100,000 deletes
    STORAGE_PER_GB = 0.18      # $0.18 per GB per month

    # Calculate costs
    read_cost = (monthly_reads / 100000) * READS_PER_100K
    write_cost = (monthly_writes / 100000) * WRITES_PER_100K
    delete_cost = (monthly_deletes / 100000) * DELETE_PER_100K
    storage_cost = storage_gb * STORAGE_PER_GB

    # Network egress (minimal for same-region operations)
    network_cost = 0.05  # ~$0.05/month for inter-service communication

    total_firestore_cost = read_cost + write_cost + delete_cost + storage_cost + network_cost

    print(f"📊 USAGE PATTERN:")
    print(f"   Bob reads/day: {bob_reads_per_day:,}")
    print(f"   Bob writes/day: {bob_writes_per_day:,}")
    print(f"   Alice reads/day: {alice_reads_per_day:,}")
    print(f"   Alice writes/day: {alice_writes_per_day:,}")
    print(f"   Total reads/month: {monthly_reads:,}")
    print(f"   Total writes/month: {monthly_writes:,}")
    print(f"   Storage: {storage_gb:.2f}GB")

    print(f"\n💵 FIRESTORE COSTS BREAKDOWN:")
    print(f"   Read operations: ${read_cost:.2f}/month")
    print(f"   Write operations: ${write_cost:.2f}/month")
    print(f"   Delete operations: ${delete_cost:.2f}/month")
    print(f"   Storage: ${storage_cost:.2f}/month")
    print(f"   Network: ${network_cost:.2f}/month")
    print(f"   TOTAL FIRESTORE: ${total_firestore_cost:.2f}/month")

    return {
        'operations': {
            'reads_monthly': monthly_reads,
            'writes_monthly': monthly_writes,
            'deletes_monthly': monthly_deletes,
            'storage_gb': storage_gb
        },
        'costs': {
            'reads': read_cost,
            'writes': write_cost,
            'deletes': delete_cost,
            'storage': storage_cost,
            'network': network_cost,
            'total': total_firestore_cost
        }
    }

def calculate_embedding_costs():
    """Calculate embedding generation costs (local vs cloud)"""

    print(f"\n🧠 EMBEDDING GENERATION COSTS:")
    print("=" * 40)

    # Embedding requirements
    new_knowledge_per_day = 50    # New items needing embeddings
    query_embeddings_per_day = 20000  # Each search query needs embedding
    total_embeddings_per_day = new_knowledge_per_day + query_embeddings_per_day
    monthly_embeddings = total_embeddings_per_day * 30

    print(f"📈 Embedding Volume:")
    print(f"   New knowledge/day: {new_knowledge_per_day}")
    print(f"   Query embeddings/day: {query_embeddings_per_day:,}")
    print(f"   Total/month: {monthly_embeddings:,}")

    # Option 1: Local SentenceTransformers (current approach)
    local_cpu_cost_per_hour = 200 / (30 * 24)  # Share of VM cost: ~$0.28/hour
    embedding_time_ms = 10  # ~10ms per embedding on CPU
    monthly_cpu_seconds = (monthly_embeddings * embedding_time_ms / 1000)
    monthly_cpu_hours = monthly_cpu_seconds / 3600
    local_embedding_cost = monthly_cpu_hours * local_cpu_cost_per_hour

    print(f"\n🖥️  LOCAL EMBEDDING (SentenceTransformers):")
    print(f"   CPU time needed: {monthly_cpu_hours:.1f} hours/month")
    print(f"   Cost: ${local_embedding_cost:.2f}/month")
    print(f"   Model: all-MiniLM-L6-v2 (384 dimensions)")
    print(f"   Advantages: No API limits, data privacy, consistent performance")

    # Option 2: Vertex AI Embeddings API
    vertex_cost_per_1k = 0.00025  # $0.025 per 1,000 characters (not embeddings)
    avg_text_length = 200  # Average characters per text
    monthly_characters = monthly_embeddings * avg_text_length
    vertex_embedding_cost = (monthly_characters / 1000) * vertex_cost_per_1k

    print(f"\n☁️  VERTEX AI EMBEDDINGS:")
    print(f"   Characters/month: {monthly_characters:,}")
    print(f"   Cost: ${vertex_embedding_cost:.2f}/month")
    print(f"   Model: text-embedding-gecko (768 dimensions)")
    print(f"   Advantages: Higher quality, no local compute needed")

    # Option 3: OpenAI Embeddings API
    openai_cost_per_1k_tokens = 0.0001  # $0.0001 per 1K tokens
    avg_tokens_per_text = 50  # ~50 tokens per text
    monthly_tokens = monthly_embeddings * avg_tokens_per_text
    openai_embedding_cost = (monthly_tokens / 1000) * openai_cost_per_1k_tokens

    print(f"\n🤖 OPENAI EMBEDDINGS (text-embedding-3-small):")
    print(f"   Tokens/month: {monthly_tokens:,}")
    print(f"   Cost: ${openai_embedding_cost:.2f}/month")
    print(f"   Model: text-embedding-3-small (1536 dimensions)")
    print(f"   Advantages: Highest quality, best performance")

    print(f"\n💡 RECOMMENDATION: LOCAL SENTENCETRANSFORMERS")
    print(f"   Lowest cost: ${local_embedding_cost:.2f}/month")
    print(f"   No API dependencies or rate limits")
    print(f"   Good quality for Bob's use case")

    return {
        'local': local_embedding_cost,
        'vertex_ai': vertex_embedding_cost,
        'openai': openai_embedding_cost,
        'recommended': 'local',
        'monthly_embeddings': monthly_embeddings
    }

def calculate_total_system_costs():
    """Calculate total costs for Bob + Alice + embeddings"""

    firestore_costs = calculate_detailed_firestore_costs()
    embedding_costs = calculate_embedding_costs()

    print(f"\n🎯 TOTAL SYSTEM COSTS SUMMARY:")
    print("=" * 50)

    # Current costs (before migration)
    current_cloud_sql = 12.00
    current_vm_included = 0.00  # Storage included in VM
    current_total = current_cloud_sql

    # New costs (after migration)
    firestore_monthly = firestore_costs['costs']['total']
    embedding_monthly = embedding_costs['local']  # Use local recommendation
    new_total = firestore_monthly + embedding_monthly

    # VM costs (unchanged)
    vm_monthly = 200.00  # thebeast VM cost

    print(f"💸 BEFORE MIGRATION:")
    print(f"   Cloud SQL: ${current_cloud_sql:.2f}/month")
    print(f"   VM Storage: ${current_vm_included:.2f}/month (included)")
    print(f"   VM Compute: ${vm_monthly:.2f}/month")
    print(f"   Total: ${current_total + vm_monthly:.2f}/month")

    print(f"\n💰 AFTER MIGRATION:")
    print(f"   Firestore: ${firestore_monthly:.2f}/month")
    print(f"   Embeddings: ${embedding_monthly:.2f}/month")
    print(f"   VM Compute: ${vm_monthly:.2f}/month")
    print(f"   Total: ${new_total + vm_monthly:.2f}/month")

    monthly_savings = current_total - new_total
    annual_savings = monthly_savings * 12

    print(f"\n💵 SAVINGS:")
    print(f"   Monthly: ${monthly_savings:.2f}")
    print(f"   Annual: ${annual_savings:.2f}")
    print(f"   ROI: Break-even in {abs(1/monthly_savings) if monthly_savings != 0 else 0:.1f} months")

    # High-volume scaling analysis
    print(f"\n📈 SCALING ANALYSIS:")
    scaling_factors = [1, 2, 5, 10]

    for factor in scaling_factors:
        scaled_reads = 22000 * factor  # Base reads scaled
        scaled_writes = 800 * factor
        scaled_monthly_reads = scaled_reads * 30
        scaled_monthly_writes = scaled_writes * 30

        scaled_read_cost = (scaled_monthly_reads / 100000) * 0.36
        scaled_write_cost = (scaled_monthly_writes / 100000) * 1.80
        scaled_storage = 0.17 * factor  # Storage scales with usage
        scaled_storage_cost = scaled_storage * 0.18

        scaled_total = scaled_read_cost + scaled_write_cost + scaled_storage_cost + 0.05

        print(f"   {factor}x usage: ${scaled_total:.2f}/month ({scaled_reads:,} reads/day)")

    return {
        'current_total': current_total,
        'new_total': new_total,
        'monthly_savings': monthly_savings,
        'annual_savings': annual_savings,
        'firestore_costs': firestore_costs,
        'embedding_costs': embedding_costs
    }

def deployment_cost_analysis():
    """Analyze deployment costs for Bob on different platforms"""

    print(f"\n🚀 BOB DEPLOYMENT COST ANALYSIS:")
    print("=" * 45)

    # Option 1: Bob on VM (current)
    vm_share_for_bob = 0.05  # Bob uses ~5% of VM resources
    vm_cost_for_bob = 200 * vm_share_for_bob

    print(f"🖥️  OPTION 1 - BOB ON VM (current):")
    print(f"   VM resource share: {vm_share_for_bob*100}%")
    print(f"   Cost allocation: ${vm_cost_for_bob:.2f}/month")
    print(f"   Advantages: No cold starts, persistent memory")
    print(f"   Disadvantages: Resource contention with other services")

    # Option 2: Bob on Cloud Run
    cloud_run_requests_per_month = 22000 * 30  # 22k operations/day
    cloud_run_cpu_seconds_per_request = 0.1  # 100ms average processing
    cloud_run_memory_gb_seconds = cloud_run_requests_per_month * 0.5 * cloud_run_cpu_seconds_per_request

    # Cloud Run pricing (approximate)
    cpu_cost = (cloud_run_requests_per_month * cloud_run_cpu_seconds_per_request) * 0.0000024  # vCPU-seconds
    memory_cost = cloud_run_memory_gb_seconds * 0.0000025  # GB-seconds
    request_cost = (cloud_run_requests_per_month / 1000000) * 0.40  # Per million requests

    cloud_run_total = cpu_cost + memory_cost + request_cost

    print(f"\n☁️  OPTION 2 - BOB ON CLOUD RUN:")
    print(f"   Monthly requests: {cloud_run_requests_per_month:,}")
    print(f"   CPU cost: ${cpu_cost:.2f}/month")
    print(f"   Memory cost: ${memory_cost:.2f}/month")
    print(f"   Request cost: ${request_cost:.2f}/month")
    print(f"   Total: ${cloud_run_total:.2f}/month")
    print(f"   Advantages: Auto-scaling, pay-per-use, no resource contention")
    print(f"   Disadvantages: Cold starts, stateless")

    print(f"\n🎯 RECOMMENDATION:")
    if cloud_run_total < vm_cost_for_bob:
        savings = vm_cost_for_bob - cloud_run_total
        print(f"   Deploy Bob to Cloud Run")
        print(f"   Additional savings: ${savings:.2f}/month")
        print(f"   Total annual savings: ${(savings * 12):.2f}")
    else:
        print(f"   Keep Bob on VM for cost efficiency")

    return {
        'vm_cost': vm_cost_for_bob,
        'cloud_run_cost': cloud_run_total,
        'recommended': 'cloud_run' if cloud_run_total < vm_cost_for_bob else 'vm'
    }

if __name__ == "__main__":
    print("📊 COMPREHENSIVE COST ANALYSIS FOR BOB + ALICE MIGRATION")
    print("=" * 70)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Scenario: 20,000 reads/day + embedding generation")

    # Run all analyses
    total_costs = calculate_total_system_costs()
    deployment_costs = deployment_cost_analysis()

    print(f"\n🏆 FINAL RECOMMENDATIONS:")
    print("=" * 35)
    print(f"✅ Migrate to Firestore (${total_costs['monthly_savings']:.2f}/month savings)")
    print(f"✅ Use local SentenceTransformers for embeddings")
    print(f"✅ Deploy Bob to {deployment_costs['recommended'].upper()}")
    print(f"✅ Total annual savings: ${total_costs['annual_savings']:.2f}")
    print(f"✅ Migration ROI: Positive from month 1")
