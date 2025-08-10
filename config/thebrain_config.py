#!/usr/bin/env python3
"""
Configuration for "thebrain" - Unified Database for All AI Systems
This configuration enables Bob to connect to the shared Firestore database
"""

# Firestore Configuration for "thebrain"
THEBRAIN_CONFIG = {
    'project_id': 'diagnostic-pro-mvp',
    'database_id': 'thebrain',  # Unified database name
    'collections': {
        'diagnostic_submissions': 'Customer diagnostic data from DiagnosticPro',
        'bob_conversations': 'Bob's Slack conversations and responses',
        'alice_tasks': 'Alice's task management data',
        'shared_knowledge': 'Shared knowledge base for all AI agents',
        'system_metrics': 'Performance and usage metrics'
    }
}

# Connection settings
FIRESTORE_SETTINGS = {
    'use_emulator': False,  # Set to True for local development
    'emulator_host': 'localhost:8080',
    'credentials_path': None,  # Uses default credentials if None
}

# Data sharing rules
DATA_SHARING_RULES = {
    'customer_pii': {
        'share_with_ai': False,  # Don't share raw PII with AI training
        'anonymize_first': True,  # Anonymize before AI access
        'collections': ['diagnostic_submissions']
    },
    'business_intelligence': {
        'share_with_ai': True,  # Share business insights
        'collections': ['shared_knowledge', 'system_metrics']
    }
}

def get_firestore_client():
    """
    Get Firestore client connected to "thebrain" database
    """
    from google.cloud import firestore
    
    if FIRESTORE_SETTINGS['use_emulator']:
        # Use emulator for local development
        import os
        os.environ['FIRESTORE_EMULATOR_HOST'] = FIRESTORE_SETTINGS['emulator_host']
    
    client = firestore.Client(
        project=THEBRAIN_CONFIG['project_id'],
        database=THEBRAIN_CONFIG['database_id']
    )
    
    return client

def migrate_chromadb_to_thebrain():
    """
    Future migration function to sync Bob's ChromaDB with "thebrain"
    """
    # TODO: Implement migration from ChromaDB to Firestore
    # This will sync Bob's local knowledge with the cloud
    pass

if __name__ == "__main__":
    print("🧠 'thebrain' Configuration")
    print("=" * 50)
    print(f"Project: {THEBRAIN_CONFIG['project_id']}")
    print(f"Database: {THEBRAIN_CONFIG['database_id']}")
    print(f"Collections: {len(THEBRAIN_CONFIG['collections'])}")
    for collection, description in THEBRAIN_CONFIG['collections'].items():
        print(f"  - {collection}: {description}")