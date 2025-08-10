# Graphiti Migration Plan - Google Cloud Platform
**Unified Knowledge Graph Architecture for Bob's Brain**
**Created:** 2025-01-10
**Status:** Ready for Implementation

## 🎯 MIGRATION OBJECTIVE

Consolidate all existing databases into a single, unified Graphiti knowledge graph on Google Cloud Platform:
- **Firestore** documents → Graph entities and relationships
- **ChromaDB** vectors → Graph embeddings with semantic search
- **Bob's memory** → Temporal knowledge graph
- **MVP3 data** → Integrated business entities

## 🏗️ TARGET ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                   Google Cloud Platform                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │            Graphiti Knowledge Graph              │   │
│  │                (Neo4j on GKE)                    │   │
│  ├──────────────────────────────────────────────────┤   │
│  │                                                  │   │
│  │  Entities:        Relationships:    Temporal:   │   │
│  │  • Users          • OWNS           • Created    │   │
│  │  • Companies      • ASKED          • Modified   │   │
│  │  • Documents      • RESPONDED      • Valid      │   │
│  │  • Conversations  • RELATES_TO     • Invalid    │   │
│  │  • Diagnostics    • LEARNED_FROM                │   │
│  │                                                  │   │
│  └──────────────────────────────────────────────────┘   │
│                           ↑                              │
│                           │                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Bob Base Model (Cloud Run)          │   │
│  │                                                  │   │
│  │  • ResearchBob    • AssistantBob                │   │
│  │  • DiagnosticBob  • Custom Specializations      │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 📊 CURRENT DATA INVENTORY

### 1. Firestore Collections
```
diagnostic-pro-mvp/bob-brain:
├── shared_knowledge (5 documents)
├── bob_conversations (ongoing)
├── memory_episodes (user interactions)
└── system_metrics (migration logs)

diagnostic-pro-mvp/(default):
├── diagnostic_submissions (MVP3)
├── users (MVP3)
├── sessions (MVP3)
└── payments (MVP3)
```

### 2. ChromaDB Collections
```
/home/jeremylongshore/bobs-brain/chroma_data:
└── bob_knowledge (5 documents with embeddings)
```

### 3. In-Memory Data
```
Bob's conversation_memory:
├── recent_interactions
├── greeting_count
├── user_context
└── conversation_history
```

## 🚀 IMPLEMENTATION PHASES

### Phase 1: Neo4j Setup on GCP (Day 1)

#### Option A: Google Kubernetes Engine (Recommended)
```bash
# 1. Create GKE cluster
gcloud container clusters create bob-graphiti \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n2-standard-4 \
  --disk-size 100

# 2. Deploy Neo4j using Helm
helm repo add neo4j https://neo4j.github.io/helm-charts
helm install bob-neo4j neo4j/neo4j \
  --set auth.password=BobBrainGraph2025 \
  --set core.persistentVolume.size=50Gi \
  --set neo4j.edition=enterprise \
  --set acceptLicenseAgreement=yes
```

#### Option B: Compute Engine VM
```bash
# Create VM with Neo4j
gcloud compute instances create bob-graphiti-neo4j \
  --zone=us-central1-a \
  --machine-type=n2-standard-8 \
  --boot-disk-size=200GB \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --metadata startup-script='#!/bin/bash
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add -
    echo "deb https://debian.neo4j.com stable latest" > /etc/apt/sources.list.d/neo4j.list
    apt-get update
    apt-get install -y neo4j
    systemctl enable neo4j
    systemctl start neo4j'
```

### Phase 2: Graphiti Installation & Configuration (Day 2)

```python
# requirements-graphiti.txt
graphiti-core==0.3.0
neo4j==5.26.0
google-cloud-firestore==2.11.1
chromadb==0.5.0
vertexai==1.38.0
```

### Phase 3: Migration Scripts (Days 3-5)

Create comprehensive migration tool:

```python
# src/migrate_to_graphiti.py
import os
from datetime import datetime
from typing import Dict, List, Any
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from google.cloud import firestore
import chromadb
import logging

class GraphitiMigrationManager:
    """
    Migrate all databases to Graphiti on GCP
    """
    
    def __init__(self):
        # Neo4j on GCP
        neo4j_host = os.environ.get('NEO4J_HOST', 'bob-neo4j.us-central1.gcp.com')
        neo4j_password = os.environ.get('NEO4J_PASSWORD', 'BobBrainGraph2025')
        
        # Initialize Graphiti
        self.graphiti = Graphiti(
            f"bolt://{neo4j_host}:7687",
            "neo4j",
            neo4j_password
        )
        
        # Connect to existing databases
        self.firestore = firestore.Client(
            project='diagnostic-pro-mvp',
            database='bob-brain'
        )
        
        self.chroma_client = chromadb.PersistentClient(
            path='/home/jeremylongshore/bobs-brain/chroma_data'
        )
        
        self.logger = logging.getLogger('GraphitiMigration')
    
    def migrate_firestore_to_graph(self):
        """
        Convert Firestore documents to graph entities
        """
        # Migrate shared_knowledge
        knowledge_docs = self.firestore.collection('shared_knowledge').get()
        
        for doc in knowledge_docs:
            data = doc.to_dict()
            
            # Create episode for Graphiti
            episode = EpisodeType(
                name=doc.id,
                content=data.get('content', ''),
                source=data.get('ai_agent', 'bob'),
                source_description="Migrated from Firestore",
                created_at=data.get('migrated_at', datetime.now()),
                valid_at=datetime.now(),
                metadata={
                    'original_source': 'firestore',
                    'knowledge_type': data.get('knowledge_type', 'general'),
                    'original_id': data.get('original_id', doc.id)
                }
            )
            
            # Add to Graphiti (creates entities and relationships)
            self.graphiti.add_episode(episode)
        
        # Migrate conversations
        conversations = self.firestore.collection('bob_conversations').get()
        
        for conv in conversations:
            data = conv.to_dict()
            
            # Create user entity
            user_episode = EpisodeType(
                name=f"user_{data.get('user_id')}",
                content=f"User message: {data.get('user_message')}",
                source=data.get('user_id'),
                created_at=data.get('timestamp'),
                valid_at=data.get('timestamp')
            )
            
            # Create Bob's response
            bob_episode = EpisodeType(
                name=f"bob_response_{conv.id}",
                content=f"Bob: {data.get('bob_response')}",
                source='bob',
                created_at=data.get('timestamp'),
                valid_at=data.get('timestamp'),
                reference_time=data.get('timestamp')
            )
            
            self.graphiti.add_episode(user_episode)
            self.graphiti.add_episode(bob_episode)
    
    def migrate_chromadb_to_graph(self):
        """
        Convert ChromaDB vectors to graph with embeddings
        """
        collection = self.chroma_client.get_collection('bob_knowledge')
        all_data = collection.get()
        
        for i, (doc_id, content, metadata) in enumerate(
            zip(all_data['ids'], all_data['documents'], all_data['metadatas'])
        ):
            # Create knowledge episode
            episode = EpisodeType(
                name=f"knowledge_{doc_id}",
                content=content,
                source='chromadb_migration',
                source_description="Business knowledge from ChromaDB",
                created_at=datetime.fromisoformat(
                    metadata.get('date', datetime.now().isoformat())
                ),
                metadata={
                    'original_source': 'chromadb',
                    'type': metadata.get('type', 'knowledge'),
                    'priority': metadata.get('priority', 'normal')
                }
            )
            
            self.graphiti.add_episode(episode)
    
    def migrate_mvp3_data(self):
        """
        Integrate MVP3 business data into knowledge graph
        """
        # Get default database for MVP3
        mvp3_db = firestore.Client(
            project='diagnostic-pro-mvp'
            # Uses default database
        )
        
        # Migrate users as entities
        users = mvp3_db.collection('users').get()
        for user in users:
            data = user.to_dict()
            
            # Create user entity
            user_episode = EpisodeType(
                name=f"mvp3_user_{user.id}",
                content=f"User: {data.get('name', 'Unknown')}",
                source='mvp3_migration',
                metadata={
                    'email': data.get('email', ''),
                    'created': data.get('created_at', ''),
                    'type': 'customer'
                }
            )
            
            self.graphiti.add_episode(user_episode)
        
        # Migrate diagnostic submissions
        diagnostics = mvp3_db.collection('diagnostic_submissions').get()
        for diag in diagnostics:
            data = diag.to_dict()
            
            # Create diagnostic entity
            diag_episode = EpisodeType(
                name=f"diagnostic_{diag.id}",
                content=f"Diagnostic: {data.get('problem_description', '')}",
                source='mvp3_diagnostic',
                metadata={
                    'service': data.get('selected_service', ''),
                    'equipment': data.get('equipment_type', ''),
                    'status': data.get('status', 'submitted')
                }
            )
            
            self.graphiti.add_episode(diag_episode)
    
    def create_core_entities(self):
        """
        Create core business entities in the graph
        """
        # Create Jeremy as owner
        jeremy_episode = EpisodeType(
            name="Jeremy_Longshore",
            content="Jeremy Longshore - Owner of DiagnosticPro with 15 years business experience",
            source='system',
            source_description="Core business entity",
            metadata={
                'role': 'owner',
                'experience': '15 years',
                'background': 'BBI, trucking'
            }
        )
        
        # Create DiagnosticPro company
        company_episode = EpisodeType(
            name="DiagnosticPro",
            content="DiagnosticPro.io - AI-powered diagnostic verification platform",
            source='system',
            source_description="Core business entity",
            metadata={
                'type': 'company',
                'industry': 'automotive_diagnostics',
                'mission': 'Protect customers from repair overcharges'
            }
        )
        
        # Create Bob as AI agent
        bob_episode = EpisodeType(
            name="Bob_AI_Agent",
            content="Bob - AI assistant for DiagnosticPro powered by Graphiti knowledge graph",
            source='system',
            source_description="Core AI entity",
            metadata={
                'type': 'ai_agent',
                'version': 'graphiti_enhanced',
                'capabilities': ['research', 'assistance', 'diagnostics']
            }
        )
        
        self.graphiti.add_episode(jeremy_episode)
        self.graphiti.add_episode(company_episode)
        self.graphiti.add_episode(bob_episode)
    
    def run_complete_migration(self):
        """
        Execute full migration to Graphiti
        """
        self.logger.info("Starting Graphiti migration on GCP...")
        
        # 1. Create core entities
        self.logger.info("Creating core entities...")
        self.create_core_entities()
        
        # 2. Migrate Firestore
        self.logger.info("Migrating Firestore data...")
        self.migrate_firestore_to_graph()
        
        # 3. Migrate ChromaDB
        self.logger.info("Migrating ChromaDB vectors...")
        self.migrate_chromadb_to_graph()
        
        # 4. Migrate MVP3
        self.logger.info("Integrating MVP3 business data...")
        self.migrate_mvp3_data()
        
        # 5. Build relationships
        self.logger.info("Building knowledge graph relationships...")
        self.graphiti.build_communities()
        
        self.logger.info("Migration complete!")
        
        # Get statistics
        stats = {
            'nodes': self.graphiti.get_node_count(),
            'edges': self.graphiti.get_edge_count(),
            'communities': self.graphiti.get_community_count()
        }
        
        return stats
```

### Phase 4: Update Bob to Use Graphiti (Days 6-7)

```python
# src/bob_graphiti.py
from graphiti_core import Graphiti
from graphiti_core.search import SearchConfig

class BobGraphiti(BobBase):
    """
    Bob powered by Graphiti knowledge graph on GCP
    """
    
    def __init__(self):
        super().__init__()
        
        # Connect to Graphiti on GCP
        self.graphiti = Graphiti(
            f"bolt://{os.environ['NEO4J_HOST']}:7687",
            "neo4j",
            os.environ['NEO4J_PASSWORD']
        )
        
    def process_message(self, message: str, user_id: str):
        """
        Process using Graphiti's knowledge graph
        """
        # Add message to graph
        episode = EpisodeType(
            name=f"message_{datetime.now().isoformat()}",
            content=message,
            source=user_id,
            created_at=datetime.now()
        )
        self.graphiti.add_episode(episode)
        
        # Search knowledge graph
        search_config = SearchConfig(
            query=message,
            num_results=5,
            include_community_info=True,
            temporal_context=datetime.now()
        )
        
        results = self.graphiti.search(search_config)
        
        # Generate response with graph context
        context = self._build_graph_context(results)
        response = self.generate_response(message, context)
        
        # Add response to graph
        response_episode = EpisodeType(
            name=f"response_{datetime.now().isoformat()}",
            content=response,
            source='bob',
            created_at=datetime.now()
        )
        self.graphiti.add_episode(response_episode)
        
        return response
    
    def _build_graph_context(self, results):
        """
        Build context from knowledge graph results
        """
        context = {
            'entities': [],
            'relationships': [],
            'facts': [],
            'temporal_context': []
        }
        
        for result in results:
            if result.node:
                context['entities'].append({
                    'name': result.node.name,
                    'content': result.node.content,
                    'created': result.node.created_at
                })
            
            if result.edges:
                for edge in result.edges:
                    context['relationships'].append({
                        'from': edge.source,
                        'to': edge.target,
                        'type': edge.relationship_type,
                        'valid_from': edge.valid_at
                    })
            
            if result.facts:
                context['facts'].extend(result.facts)
        
        return context
```

### Phase 5: Deploy to Production (Days 8-10)

```yaml
# k8s/graphiti-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bob-graphiti
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bob-graphiti
  template:
    metadata:
      labels:
        app: bob-graphiti
    spec:
      containers:
      - name: bob
        image: gcr.io/diagnostic-pro-mvp/bob-graphiti:latest
        env:
        - name: NEO4J_HOST
          value: "neo4j-service.default.svc.cluster.local"
        - name: NEO4J_PASSWORD
          valueFrom:
            secretKeyRef:
              name: neo4j-secrets
              key: password
        - name: SLACK_BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: slack-secrets
              key: bot-token
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
```

## 💰 COST OPTIMIZATION

### Current Monthly Costs
- Firestore: $10
- Cloud Run: $20
- Vertex AI: $50
**Total: $80/month**

### Graphiti on GCP Costs
- GKE cluster (3 nodes): $150
- Neo4j Enterprise: $100
- Cloud Run: $20
- Vertex AI (optimized): $30
**Total: $300/month**

### Cost Reduction Strategy
1. Use preemptible nodes: -70% compute cost = $45
2. Neo4j Community Edition: -$100 = $0
3. Autoscaling: Only scale when needed
**Optimized Total: $95/month**

## 🎯 BENEFITS OF GRAPHITI MIGRATION

### 1. Unified Knowledge
- All data in one graph
- No data silos
- Single source of truth

### 2. Relationship Intelligence
- Understands connections between entities
- Temporal awareness
- Context preservation

### 3. Advanced Queries
```cypher
// Find all diagnostic issues related to Jeremy's equipment
MATCH (jeremy:Person {name: "Jeremy"})-[:OWNS]->(equipment)
      -[:HAS_ISSUE]->(diagnostic)
WHERE diagnostic.created_at > datetime('2025-01-01')
RETURN diagnostic.problem, equipment.type
```

### 4. Real-time Updates
- Incremental graph updates
- No batch processing delays
- Instant knowledge availability

### 5. Scalability
- Handles millions of nodes/edges
- Distributed processing
- Cloud-native architecture

## 📋 MIGRATION CHECKLIST

- [ ] Set up Neo4j on GKE
- [ ] Configure Graphiti connection
- [ ] Run migration scripts
- [ ] Verify data integrity
- [ ] Update Bob to use Graphiti
- [ ] Test knowledge graph queries
- [ ] Deploy to production
- [ ] Monitor performance
- [ ] Decommission old databases

## 🚀 NEXT STEPS

1. **Immediate**: Review and approve migration plan
2. **Day 1**: Deploy Neo4j on GCP
3. **Days 2-5**: Run migration scripts
4. **Days 6-7**: Update Bob integration
5. **Days 8-10**: Production deployment
6. **Ongoing**: Monitor and optimize

---

**This migration will transform Bob from a multi-database system to a unified, intelligent knowledge graph powered by Graphiti on Google Cloud Platform.**