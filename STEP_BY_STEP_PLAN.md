# Bob's Brain Graphiti Migration - Step by Step Plan with Testing

## Overview
Each step must be completed and tested before moving to the next. This ensures the migration goes together smoothly like a puzzle.

---

## 🧩 Step 1: Fix Graphiti Initialization ✅ READY TO START

### What's Wrong:
```python
# Current (BROKEN)
self.graphiti = Graphiti(neo4j_uri=uri, neo4j_user=user, neo4j_password=password)
```

### Fix Required:
```python
# Correct way
self.graphiti = Graphiti(host="localhost", port=7687, user="neo4j", password="password")
```

### Files to Fix:
- `/home/jeremylongshore/bobs-brain/src/bob_memory.py` (line ~50)

### Test Command:
```bash
cd ~/bobs-brain
python3 tests/test_memory_only.py
```

### Success Criteria:
- No more "unexpected keyword argument" error
- Memory system initializes without Graphiti errors

---

## 🧩 Step 2: Install Neo4j Locally

### Installation Options:

#### Option A: Docker (Easiest)
```bash
# Pull and run Neo4j
docker run \
  --name bob-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/BobBrain2025 \
  -v $HOME/neo4j/data:/data \
  neo4j:latest
```

#### Option B: Direct Install
```bash
# Add Neo4j repo
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt-get update

# Install Neo4j
sudo apt-get install neo4j
sudo neo4j-admin set-initial-password BobBrain2025
sudo systemctl start neo4j
```

### Test Command:
```bash
# Check if Neo4j is running
curl http://localhost:7474
# Should return Neo4j welcome page
```

### Success Criteria:
- Neo4j browser accessible at http://localhost:7474
- Can login with neo4j/BobBrain2025

---

## 🧩 Step 3: Test Graphiti Connection

### Create Test Script:
```python
# test_graphiti_connection.py
from graphiti_core import Graphiti
import os

# Set credentials
os.environ['NEO4J_PASSWORD'] = 'BobBrain2025'

try:
    graphiti = Graphiti(
        host="localhost",
        port=7687,
        user="neo4j",
        password="BobBrain2025"
    )
    print("✅ Graphiti connected successfully!")
    
    # Test adding data
    from graphiti_core.nodes import EpisodeType
    from datetime import datetime
    
    episode = EpisodeType(
        name="test_connection",
        content="Testing Graphiti connection",
        source="test_script",
        created_at=datetime.now()
    )
    
    graphiti.add_episode(episode)
    print("✅ Successfully added test episode!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

### Test Command:
```bash
python3 test_graphiti_connection.py
```

### Success Criteria:
- Connects to Neo4j without errors
- Can add and retrieve data

---

## 🧩 Step 4: Update Bob Memory with Working Graphiti

### Fix bob_memory.py:
```python
# src/bob_memory.py (updated initialization)
def __init__(self, project_id='diagnostic-pro-mvp', 
             neo4j_host=None, neo4j_port=None, 
             neo4j_user=None, neo4j_password=None):
    
    # Firestore setup (always available)
    self.firestore = firestore.Client(project=project_id, database='bob-brain')
    
    # Graphiti setup (if Neo4j available)
    if neo4j_host:
        try:
            self.graphiti = Graphiti(
                host=neo4j_host or "localhost",
                port=neo4j_port or 7687,
                user=neo4j_user or "neo4j",
                password=neo4j_password or os.environ.get('NEO4J_PASSWORD')
            )
            self.graphiti_available = True
        except Exception as e:
            self.graphiti = None
            self.graphiti_available = False
```

### Test Command:
```bash
# Run full memory test suite
python3 tests/test_memory_only.py

# Should show:
# ✅ Firestore: True
# ✅ Graphiti: True
```

### Success Criteria:
- Both Firestore and Graphiti show as available
- All memory tests pass

---

## 🧩 Step 5: Convert Socket Mode to HTTP

### Create New HTTP Version:
```python
# src/bob_http.py
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from bob_firestore import BobFirestore

app = Flask(__name__)
bob = BobFirestore()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "mode": "http"})

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    
    # Handle URL verification
    if data.get('type') == 'url_verification':
        return jsonify({"challenge": data['challenge']})
    
    # Handle events
    if data.get('type') == 'event_callback':
        event = data['event']
        if event['type'] == 'message':
            # Process message with Bob
            response = bob.process_message(event['text'], event['user'])
            # Send response back to Slack
            client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
            client.chat_postMessage(
                channel=event['channel'],
                text=response
            )
    
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```

### Test Command:
```bash
# Run locally
PORT=3000 python3 src/bob_http.py

# Test health endpoint
curl http://localhost:3000/health
```

### Success Criteria:
- Health endpoint returns {"status": "healthy"}
- Can receive Slack events

---

## 🧩 Step 6: Deploy Neo4j to GCP

### Create Compute Engine VM:
```bash
# Create VM for Neo4j
gcloud compute instances create bob-neo4j \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --boot-disk-size=50GB \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=neo4j-server \
  --metadata startup-script='#!/bin/bash
    apt-get update
    apt-get install -y docker.io
    docker run -d \
      --name neo4j \
      -p 7474:7474 -p 7687:7687 \
      -e NEO4J_AUTH=neo4j/BobBrainGCP2025 \
      --restart always \
      neo4j:latest'

# Create firewall rule
gcloud compute firewall-rules create neo4j-access \
  --allow tcp:7474,tcp:7687 \
  --source-ranges 0.0.0.0/0 \
  --target-tags neo4j-server
```

### Test Command:
```bash
# Get VM IP
NEO4J_IP=$(gcloud compute instances describe bob-neo4j \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# Test connection
curl http://$NEO4J_IP:7474
```

### Success Criteria:
- Neo4j accessible from local machine
- Can connect with credentials

---

## 🧩 Step 7: Deploy Bob to Cloud Run

### Build and Deploy:
```bash
cd ~/bobs-brain

# Build container
gcloud builds submit --tag gcr.io/bobs-house-ai/bob-http

# Deploy to Cloud Run
gcloud run deploy bob-brain \
  --image gcr.io/bobs-house-ai/bob-http \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN,NEO4J_HOST=$NEO4J_IP,NEO4J_PASSWORD=BobBrainGCP2025"
```

### Test Command:
```bash
# Get Cloud Run URL
BOB_URL=$(gcloud run services describe bob-brain \
  --region us-central1 \
  --format='get(status.url)')

# Test health
curl $BOB_URL/health
```

### Success Criteria:
- Bob accessible via Cloud Run URL
- Connected to Neo4j on GCP
- Responds to Slack events

---

## 🧩 Step 8: Migrate All Data

### Run Migration Script:
```bash
cd ~/bobs-brain

# Set Neo4j connection
export NEO4J_HOST=$NEO4J_IP
export NEO4J_PASSWORD=BobBrainGCP2025

# Run migration
python3 src/migrate_to_graphiti.py
```

### Test Command:
```bash
# Query Neo4j to verify data
python3 -c "
from graphiti_core import Graphiti
import os

graphiti = Graphiti(
    host=os.environ['NEO4J_HOST'],
    port=7687,
    user='neo4j',
    password=os.environ['NEO4J_PASSWORD']
)

stats = {
    'nodes': graphiti.get_node_count(),
    'edges': graphiti.get_edge_count()
}

print(f'✅ Migration complete: {stats}')
"
```

### Success Criteria:
- All Firestore docs migrated
- ChromaDB vectors imported
- Knowledge graph built

---

## 🧩 Step 9: Final Integration Test

### Complete System Test:
```bash
# Run all tests
python3 run_all_tests.py

# Test Slack integration
python3 test_slack_integration.py

# Test knowledge retrieval
python3 test_knowledge_graph.py
```

### Success Criteria:
- All tests pass
- Bob responds in Slack
- Knowledge graph queries work
- System stable under load

---

## 📊 Progress Tracker

| Step | Component | Status | Test Result |
|------|-----------|--------|-------------|
| 1 | Fix Graphiti params | 🔄 Ready | ⏳ Pending |
| 2 | Install Neo4j | ⏳ Waiting | ⏳ Pending |
| 3 | Test Graphiti | ⏳ Waiting | ⏳ Pending |
| 4 | Update Bob Memory | ⏳ Waiting | ⏳ Pending |
| 5 | HTTP Conversion | ⏳ Waiting | ⏳ Pending |
| 6 | Deploy Neo4j GCP | ⏳ Waiting | ⏳ Pending |
| 7 | Deploy Bob | ⏳ Waiting | ⏳ Pending |
| 8 | Migrate Data | ⏳ Waiting | ⏳ Pending |
| 9 | Final Test | ⏳ Waiting | ⏳ Pending |

---

## 💰 Cost Tracking

Using your $2,251.82 credits:

| Resource | Monthly Cost | Credits Used |
|----------|-------------|--------------|
| Neo4j VM | $50 | Running total: $50 |
| Cloud Run | $20 | Running total: $70 |
| Firestore | $10 | Running total: $80 |
| Vertex AI | $30 | Running total: $110 |

**Months remaining with credits: 20+ months**

---

## 🔑 Key Commands Reference

```bash
# Check current status
cd ~/bobs-brain && git status

# Run memory tests
python3 tests/test_memory_only.py

# Check Neo4j
docker ps | grep neo4j

# View logs
docker logs bob-neo4j

# Test Bob locally
python3 src/bob_http.py
```

---

**Next Action:** Start with Step 1 - Fix Graphiti initialization parameters