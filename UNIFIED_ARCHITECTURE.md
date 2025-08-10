# UNIFIED ARCHITECTURE - GRAPHITI + VERTEX AI ON GCP
**Utilizing Your $2,251.82 Free Credits**

## 🎯 THE GOAL: ONE SYSTEM TO RULE THEM ALL

Replace Chroma + Firestore with:
- **Neo4j** - Graph database with vector embeddings
- **Graphiti** - Knowledge graph orchestration
- **Vertex AI** - ML models and embeddings
- **ALL ON GCP** - Using your free credits

---

## 🏗️ OFFICIAL MINIMALIST ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                 GOOGLE CLOUD PLATFORM                     │
│                 ($2,251 Credits Available)                │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              VERTEX AI PLATFORM                   │   │
│  │                                                   │   │
│  │  • Gemini 1.5 Flash (LLM)                       │   │
│  │  • Text Embeddings API (gecko@003)              │   │
│  │  • Model Garden (future models)                  │   │
│  │  • Vertex AI Pipelines (orchestration)          │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                       │
│  ┌────────────────▼─────────────────────────────────┐   │
│  │              GRAPHITI CORE                       │   │
│  │         (Running on Cloud Run)                   │   │
│  │                                                   │   │
│  │  • Entity Extraction (via Vertex AI)            │   │
│  │  • Relationship Building                        │   │
│  │  • Temporal Awareness                           │   │
│  │  • Hybrid Search (semantic + graph + keyword)   │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                       │
│  ┌────────────────▼─────────────────────────────────┐   │
│  │           NEO4J ENTERPRISE                       │   │
│  │      (Compute Engine VM or Neo4j Aura)          │   │
│  │                                                   │   │
│  │  • Graph Storage                                │   │
│  │  • Vector Indexes (embeddings from Vertex AI)   │   │
│  │  • Full-text Search                             │   │
│  │  • Cypher Queries                               │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 WHAT TO RETIRE (MAKE OBSOLETE)

### ❌ ChromaDB - REPLACED BY:
- Neo4j vector indexes
- Vertex AI embeddings
- Graphiti semantic search

### ❌ Firestore - REPLACED BY:
- Neo4j graph storage
- Graphiti temporal tracking
- Native graph relationships

---

## 🚀 IMPLEMENTATION PLAN

### Phase 1: Configure Vertex AI Integration
```python
# requirements-vertex.txt
graphiti-core==0.18.5
google-cloud-aiplatform==1.38.0
neo4j==5.26.0
```

```python
# vertex_graphiti_config.py
from graphiti_core import Graphiti
from graphiti_core.llm_client import LLMClient
from graphiti_core.embedder import EmbedderClient
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel, TextGenerationModel

class VertexAILLMClient(LLMClient):
    """Custom LLM client for Vertex AI"""
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = TextGenerationModel.from_pretrained(model_name)
    
    async def generate(self, prompt, **kwargs):
        response = await self.model.predict_async(prompt)
        return response.text

class VertexAIEmbedder(EmbedderClient):
    """Custom embedder using Vertex AI"""
    def __init__(self, model_name="textembedding-gecko@003"):
        self.model = TextEmbeddingModel.from_pretrained(model_name)
    
    async def embed(self, text):
        embeddings = await self.model.get_embeddings_async([text])
        return embeddings[0].values

# Initialize Graphiti with Vertex AI
graphiti = Graphiti(
    uri="bolt://neo4j-vm.us-central1.gcp:7687",
    user="neo4j",
    password="BobBrain2025",
    llm_client=VertexAILLMClient(),
    embedder=VertexAIEmbedder()
)
```

### Phase 2: Deploy Neo4j with Vector Support
```bash
# Deploy Neo4j on GCP Compute Engine
gcloud compute instances create neo4j-graphiti \
  --machine-type=n2-standard-4 \
  --boot-disk-size=100GB \
  --zone=us-central1-a \
  --image-family=ubuntu-2204-lts \
  --metadata startup-script='#!/bin/bash
    # Install Neo4j with APOC and Graph Data Science
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add -
    echo "deb https://debian.neo4j.com stable latest" > /etc/apt/sources.list.d/neo4j.list
    apt-get update
    apt-get install -y neo4j neo4j-graph-data-science
    
    # Configure for production
    echo "dbms.memory.heap.max_size=4G" >> /etc/neo4j/neo4j.conf
    echo "dbms.security.auth_enabled=true" >> /etc/neo4j/neo4j.conf
    
    # Enable vector indexes
    echo "dbms.index.fulltext.enabled=true" >> /etc/neo4j/neo4j.conf
    
    systemctl enable neo4j
    systemctl start neo4j'

# Estimated cost: $50/month (covered by credits)
```

### Phase 3: Migrate All Data
```python
# migrate_everything.py
import asyncio
from graphiti_core import Graphiti
from google.cloud import firestore
import chromadb

async def migrate_all_to_graphiti():
    """Migrate EVERYTHING to Graphiti"""
    
    # Initialize with Vertex AI
    graphiti = create_vertex_graphiti()
    
    # 1. Migrate Firestore documents
    print("Migrating Firestore...")
    fs = firestore.Client(project='diagnostic-pro-mvp')
    
    for collection in ['shared_knowledge', 'bob_conversations']:
        docs = fs.collection(collection).get()
        for doc in docs:
            data = doc.to_dict()
            await graphiti.add_episode(
                name=f"firestore_{doc.id}",
                episode_body=data.get('content', str(data)),
                source_description=f"Migrated from Firestore/{collection}",
                reference_time=datetime.now()
            )
    
    # 2. Migrate ChromaDB vectors
    print("Migrating ChromaDB...")
    chroma = chromadb.PersistentClient(path='./chroma_data')
    collection = chroma.get_collection('bob_knowledge')
    
    all_data = collection.get()
    for doc, metadata in zip(all_data['documents'], all_data['metadatas']):
        await graphiti.add_episode(
            name=f"chroma_{metadata.get('id', 'unknown')}",
            episode_body=doc,
            source_description="Migrated from ChromaDB",
            reference_time=datetime.now()
        )
    
    print("✅ Migration complete! Firestore and ChromaDB are now obsolete.")
    
    # 3. Delete old data (after verification)
    # fs.collection('shared_knowledge').delete()  # Uncomment when ready
    # chroma.delete_collection('bob_knowledge')   # Uncomment when ready

asyncio.run(migrate_all_to_graphiti())
```

### Phase 4: Cloud Run Deployment
```yaml
# cloud-run-config.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: bob-graphiti
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/execution-environment: gen2
    spec:
      containers:
      - image: gcr.io/bobs-house-ai/bob-graphiti
        env:
        - name: GCP_PROJECT
          value: bobs-house-ai
        - name: NEO4J_URI
          value: bolt://10.128.0.5:7687  # Internal IP
        - name: NEO4J_PASSWORD
          valueFrom:
            secretKeyRef:
              name: neo4j-password
              key: password
        - name: VERTEX_AI_LOCATION
          value: us-central1
        resources:
          limits:
            memory: 2Gi
            cpu: "2"
```

---

## 💰 COST BREAKDOWN (Using Credits)

| Service | Monthly Cost | Purpose |
|---------|-------------|---------|
| Neo4j VM (n2-standard-4) | $50 | Graph DB + Vectors |
| Cloud Run | $20 | Bob Application |
| Vertex AI Embeddings | $10 | Text embeddings |
| Vertex AI Gemini | $30 | LLM inference |
| **TOTAL** | **$110/month** | |
| **Credits Available** | **$2,251** | |
| **Months Free** | **20+** | |

---

## 🎯 BENEFITS OF THIS ARCHITECTURE

### 1. **TRUE UNIFICATION**
- ONE database (Neo4j)
- ONE framework (Graphiti)
- ONE cloud (GCP)
- ONE ML platform (Vertex AI)

### 2. **FULL CAPABILITIES**
- Graph relationships
- Vector embeddings
- Semantic search
- Temporal awareness
- ML model access

### 3. **SCALABILITY**
- Start small ($110/month)
- Scale to enterprise
- Add models from Model Garden
- Expand to Vertex AI Pipelines

### 4. **OFFICIAL & SUPPORTED**
- Graphiti official framework
- Neo4j official on GCP
- Vertex AI native integration
- All production-ready

---

## 🔧 ENVIRONMENT VARIABLES

```bash
# .env.production
GCP_PROJECT=bobs-house-ai
VERTEX_AI_LOCATION=us-central1
NEO4J_URI=bolt://neo4j-vm.internal:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=BobBrain2025
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# No more needed:
# OPENAI_API_KEY - replaced by Vertex AI
# FIRESTORE_DB - replaced by Neo4j
# CHROMA_PATH - replaced by Neo4j vectors
```

---

## 📝 MIGRATION COMMANDS

```bash
# Step 1: Deploy Neo4j
gcloud compute instances create neo4j-graphiti \
  --machine-type=n2-standard-4 \
  --zone=us-central1-a

# Step 2: Initialize Vertex AI
gcloud services enable aiplatform.googleapis.com
gcloud ai models list --region=us-central1

# Step 3: Run migration
python3 migrate_everything.py

# Step 4: Deploy to Cloud Run
gcloud run deploy bob-graphiti \
  --source . \
  --region us-central1

# Step 5: Verify and cleanup
# After confirming everything works:
# - Delete Firestore collections
# - Remove ChromaDB files
# - Cancel OpenAI subscription
```

---

## ✅ FINAL RESULT

**Before:**
- 3 databases (Firestore, ChromaDB, Neo4j)
- 2 embedding systems (OpenAI, Vertex)
- Complex synchronization
- $150+/month

**After:**
- 1 database (Neo4j with Graphiti)
- 1 ML platform (Vertex AI)
- Unified architecture
- $110/month (FREE with credits)

---

**This is the OFFICIAL, MINIMALIST, FULLY-CAPABLE architecture you want!**