# BOB ON GOOGLE CLOUD - COMPLETE GRAPHITI MEMORY SYSTEM
**EVERYTHING ON GCP - DON'T MESS IT UP GUIDE**

## 🎯 SIMPLE TRUTH: BOB + GRAPHITI + GOOGLE CLOUD = WIN

---

## 🏗️ THE ONLY ARCHITECTURE YOU NEED

```
BOB'S BRAIN - ALL GOOGLE CLOUD
================================

1. BOB APPLICATION → Cloud Run
2. MEMORY SYSTEM → Graphiti + Neo4j 
3. ML/AI → Vertex AI
4. EVERYTHING ELSE → GONE

NO FIRESTORE
NO CHROMADB  
NO OPENAI
JUST GOOGLE CLOUD + GRAPHITI
```

---

## ✅ STEP-BY-STEP (DON'T SKIP ANY)

### STEP 1: Deploy Neo4j on Google Cloud
```bash
# Create the VM for Neo4j
gcloud compute instances create bob-neo4j \
  --machine-type=e2-standard-4 \
  --zone=us-central1-a \
  --boot-disk-size=100GB \
  --image-family=ubuntu-2204-lts \
  --project=bobs-house-ai

# SSH and install Neo4j
gcloud compute ssh bob-neo4j --zone=us-central1-a

# On the VM:
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j -y
sudo neo4j-admin dbms set-initial-password BobBrain2025
sudo systemctl enable neo4j
sudo systemctl start neo4j
```

### STEP 2: Configure Graphiti with Vertex AI
```python
# bob_graphiti_gcp.py
import os
from graphiti_core import Graphiti
from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel

# Initialize Vertex AI
aiplatform.init(project='bobs-house-ai', location='us-central1')

class BobGraphitiMemory:
    def __init__(self):
        # Get Neo4j internal IP
        neo4j_ip = os.environ.get('NEO4J_IP', '10.128.0.5')
        
        # Connect to Graphiti with Neo4j
        self.graphiti = Graphiti(
            uri=f"bolt://{neo4j_ip}:7687",
            user="neo4j",
            password="BobBrain2025"
        )
        
        # Vertex AI for responses
        self.llm = TextGenerationModel.from_pretrained("gemini-1.5-flash")
    
    async def remember(self, user_message, bob_response):
        """Store in Graphiti knowledge graph"""
        await self.graphiti.add_episode(
            name=f"conversation_{datetime.now().isoformat()}",
            episode_body=f"User: {user_message}\nBob: {bob_response}",
            source_description="Bob conversation",
            reference_time=datetime.now()
        )
    
    async def recall(self, query):
        """Search Graphiti memory"""
        results = await self.graphiti.search(query, num_results=5)
        return results
    
    async def think(self, user_message):
        """Generate response using memory + Vertex AI"""
        # Search memory
        context = await self.recall(user_message)
        
        # Build prompt with context
        prompt = f"""You are Bob, an AI assistant.
        
        Context from memory:
        {context}
        
        User: {user_message}
        Bob:"""
        
        # Generate with Vertex AI
        response = self.llm.predict(prompt, max_output_tokens=256)
        
        # Remember this interaction
        await self.remember(user_message, response.text)
        
        return response.text
```

### STEP 3: Deploy Bob to Cloud Run
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements-gcp.txt .
RUN pip install -r requirements-gcp.txt

# Copy Bob
COPY bob_graphiti_gcp.py .
COPY bob_server.py .

# Run server
CMD ["python", "bob_server.py"]
```

```python
# bob_server.py
from flask import Flask, request, jsonify
from bob_graphiti_gcp import BobGraphitiMemory
import asyncio

app = Flask(__name__)
bob = BobGraphitiMemory()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Bob is alive with Graphiti memory!"})

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    
    if data.get('type') == 'url_verification':
        return jsonify({"challenge": data['challenge']})
    
    if data.get('event', {}).get('type') == 'message':
        event = data['event']
        user_message = event['text']
        
        # Get Bob's response
        response = asyncio.run(bob.think(user_message))
        
        # Send to Slack
        from slack_sdk import WebClient
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        client.chat_postMessage(
            channel=event['channel'],
            text=response
        )
    
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

### STEP 4: Deploy Everything
```bash
# Build and deploy to Cloud Run
gcloud run deploy bob-brain \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "NEO4J_IP=10.128.0.5,SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN" \
  --memory 2Gi \
  --project bobs-house-ai
```

### STEP 5: Migrate ALL Old Data
```python
# migrate_to_graphiti.py
import asyncio
from bob_graphiti_gcp import BobGraphitiMemory
from google.cloud import firestore
import chromadb

async def migrate_everything():
    bob = BobGraphitiMemory()
    
    # Migrate Firestore
    print("Migrating Firestore to Graphiti...")
    fs = firestore.Client(project='diagnostic-pro-mvp')
    docs = fs.collection('shared_knowledge').get()
    
    for doc in docs:
        data = doc.to_dict()
        await bob.graphiti.add_episode(
            name=f"migrated_{doc.id}",
            episode_body=data.get('content', str(data)),
            source_description="Firestore migration",
            reference_time=datetime.now()
        )
    
    # Migrate ChromaDB
    print("Migrating ChromaDB to Graphiti...")
    chroma = chromadb.PersistentClient(path='./chroma_data')
    collection = chroma.get_collection('bob_knowledge')
    docs = collection.get()
    
    for doc in docs['documents']:
        await bob.graphiti.add_episode(
            name=f"chroma_migration",
            episode_body=doc,
            source_description="ChromaDB migration",
            reference_time=datetime.now()
        )
    
    print("✅ MIGRATION COMPLETE!")
    print("Firestore and ChromaDB are now OBSOLETE")
    print("Everything is in Graphiti on Google Cloud!")

# Run migration
asyncio.run(migrate_everything())
```

---

## 🎯 WHAT YOU GET

### BEFORE (MESS):
```
- Firestore (document store)
- ChromaDB (vector store)
- OpenAI (embeddings)
- Confusion everywhere
```

### AFTER (CLEAN):
```
- Neo4j + Graphiti (EVERYTHING)
- Vertex AI (ML/AI)
- Google Cloud (hosting)
- That's it. Done.
```

---

## 💰 COSTS (YOUR CREDITS COVER IT ALL)

| What | Cost/Month | Your Credits |
|------|------------|--------------|
| Neo4j VM | $50 | ✅ Covered |
| Cloud Run | $20 | ✅ Covered |
| Vertex AI | $30 | ✅ Covered |
| **TOTAL** | **$100** | **$2,251 available** |

**You have 22+ months FREE!**

---

## 🚨 DON'T MESS IT UP CHECKLIST

- [ ] Neo4j deployed on Google Cloud VM
- [ ] Graphiti connected to Neo4j
- [ ] Bob using Graphiti for ALL memory
- [ ] Vertex AI for ML (NOT OpenAI)
- [ ] Everything on Cloud Run
- [ ] Firestore DELETED (after migration)
- [ ] ChromaDB DELETED (after migration)
- [ ] OpenAI subscription CANCELLED

---

## 🔑 ENVIRONMENT VARIABLES

```bash
# The ONLY env vars you need:
NEO4J_IP=10.128.0.5  # Internal IP of Neo4j VM
NEO4J_PASSWORD=BobBrain2025
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
GCP_PROJECT=bobs-house-ai

# NEVER NEEDED AGAIN:
# OPENAI_API_KEY ❌
# FIRESTORE_DB ❌
# CHROMA_PATH ❌
```

---

## ✅ FINAL COMMANDS TO RUN

```bash
# 1. Create Neo4j VM
gcloud compute instances create bob-neo4j --machine-type=e2-standard-4

# 2. Deploy Bob to Cloud Run
gcloud run deploy bob-brain --source .

# 3. Migrate all data
python3 migrate_to_graphiti.py

# 4. Test it works
curl https://bob-brain-xxxxx.run.app/health

# 5. Delete old stuff (after confirming it works!)
# rm -rf chroma_data/
# Delete Firestore collections in console
```

---

## 🎉 DONE!

**Bob now has:**
- ONE memory system (Graphiti)
- ONE database (Neo4j)  
- ONE cloud (Google Cloud)
- ONE ML platform (Vertex AI)

**No more:**
- Multiple databases ❌
- Confusion ❌
- High costs ❌
- Complexity ❌

---

**THIS IS THE WAY. DON'T MESS IT UP!**