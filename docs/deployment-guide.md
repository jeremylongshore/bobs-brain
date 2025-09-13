# 🚀 Bob's Brain Deployment Guide

## Complete Setup Instructions for Each Version

---

## Bob v1 - Simple Template Deployment

### Prerequisites
- Python 3.11+
- Slack workspace admin access
- 5 minutes

### Step-by-Step Setup

```bash
# 1. Clone and checkout
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain
git checkout main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create Slack App
```

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name: "Bob Brain v1"
4. Choose your workspace

### Configure Slack Permissions

**OAuth & Permissions → Bot Token Scopes:**
- `chat:write`
- `channels:history`
- `im:history`
- `groups:history`
- `app_mentions:read`

**Install to Workspace → Copy Bot Token**

### Environment Setup

```bash
# Create .env file
cat > .env << EOF
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token  # For Socket Mode
GOOGLE_API_KEY=your-gemini-key       # Optional
CHROMA_PERSIST_DIR=./chroma_data
EOF
```

### Run Bob v1

```bash
# Socket Mode (development)
python3 src/bob_ultimate.py

# Verify in Slack
# @Bob hello
# Bob should respond!
```

---

## Bob v2 - Graphiti Knowledge Graph Deployment

### Additional Prerequisites
- Neo4j Aura account (free tier works)
- OpenAI API key
- 30 minutes

### Neo4j Setup

1. Create account at [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura)
2. Create free instance
3. Save credentials:
   - Connection URI: `neo4j+s://xxxxx.databases.neo4j.io`
   - Username: `neo4j`
   - Password: `your-password`

### Setup Steps

```bash
# 1. Switch to Graphiti branch
git checkout enhance-bob-graphiti

# 2. Install additional dependencies
pip install graphiti-core==0.3.0
pip install neo4j==5.20.0

# 3. Update .env
cat >> .env << EOF
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
OPENAI_API_KEY=sk-your-openai-key
EOF
```

### Initialize Neo4j Indexes

```python
# Run once to setup indexes
python3 << EOF
from neo4j import GraphDatabase
driver = GraphDatabase.driver(
    "neo4j+s://xxxxx.databases.neo4j.io",
    auth=("neo4j", "your-password")
)
with driver.session() as session:
    # Create required indexes
    session.run("CREATE INDEX entity_name IF NOT EXISTS FOR (n:Entity) ON (n.name)")
    session.run("CREATE INDEX entity_id IF NOT EXISTS FOR (n:Entity) ON (n.id)")
print("✅ Neo4j indexes created")
EOF
```

### Run Bob v2

```bash
# Test Graphiti connection
python3 tests/test_memory_only.py

# Run Bob with knowledge graph
python3 src/bob_firestore.py
```

---

## Bob v3 - Production System Deployment

### Additional Prerequisites
- Google Cloud Platform account
- gcloud CLI installed
- Docker installed
- 2 hours

### GCP Project Setup

```bash
# 1. Create project
gcloud projects create bobs-brain-prod
gcloud config set project bobs-brain-prod

# 2. Enable APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  bigquery.googleapis.com \
  firestore.googleapis.com \
  secretmanager.googleapis.com

# 3. Set up billing
# Visit: https://console.cloud.google.com/billing
```

### Deploy Neo4j VM

```bash
# Create VM for Neo4j
gcloud compute instances create neo4j-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --boot-disk-size=30GB \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud

# SSH and install Neo4j
gcloud compute ssh neo4j-vm --zone=us-central1-a
# Run Neo4j setup script from repo
```

### Create VPC Connector

```bash
# For secure Neo4j access
gcloud compute networks vpc-access connectors create bob-vpc-connector \
  --region=us-central1 \
  --subnet=default \
  --subnet-project=bobs-brain-prod \
  --min-instances=2 \
  --max-instances=10
```

### Deploy Services

```bash
# 1. Switch to production branch
git checkout feature/graphiti-production

# 2. Deploy main Bob service
gcloud run deploy bobs-brain \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --timeout 3600 \
  --min-instances 0 \
  --max-instances 10 \
  --vpc-connector bob-vpc-connector \
  --vpc-egress private-ranges-only \
  --set-env-vars "PROJECT_ID=bobs-brain-prod"

# 3. Deploy unified scraper
docker build -f Dockerfile.unified-scraper -t gcr.io/bobs-brain-prod/unified-scraper:latest .
docker push gcr.io/bobs-brain-prod/unified-scraper:latest

gcloud run deploy unified-scraper \
  --image gcr.io/bobs-brain-prod/unified-scraper:latest \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --timeout 3600 \
  --min-instances 0

# 4. Deploy Circle of Life scraper
gcloud run deploy circle-of-life-scraper \
  --source . \
  --platform managed \
  --region us-central1
```

### Configure Slack for Production

```bash
# Update Slack app Event URL
# https://bobs-brain-xxxxx.run.app/slack/events

# Add to Secret Manager
echo -n "xoxb-your-token" | gcloud secrets create slack-bot-token --data-file=-
echo -n "your-signing-secret" | gcloud secrets create slack-signing-secret --data-file=-
```

### Setup BigQuery

```bash
# Create datasets
bq mk --dataset bobs-brain-prod:diagnosticpro_prod
bq mk --dataset bobs-brain-prod:diagnosticpro_analytics

# Tables will auto-create on first write
```

### Verify Production Deployment

```bash
# Check all services
for service in bobs-brain unified-scraper circle-of-life-scraper; do
  echo "Testing $service..."
  curl https://$service-xxxxx.run.app/health
done

# Should see:
# {"status": "healthy", "services": {...}}
```

---

## Bob v4 - Ferrari Edition Deployment

### Complete Setup (All Systems)

The Ferrari Edition combines everything. Start with v3 production setup, then add:

### Additional Components

```bash
# 1. Switch to Ferrari branch
git checkout feature/bob-ferrari-final

# 2. Install all dependencies
pip install -r requirements.txt

# 3. Setup ChromaDB locally
mkdir -p chroma_db

# 4. Complete .env file
cat > .env << EOF
# Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
SLACK_SIGNING_SECRET=your-secret

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GCP_PROJECT=bobs-brain-prod
GOOGLE_API_KEY=your-gemini-key

# Neo4j
NEO4J_URI=bolt://10.128.0.2:7687  # or cloud URI
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# OpenAI (for Graphiti)
OPENAI_API_KEY=sk-your-key

# BigQuery
BIGQUERY_DATASET=diagnosticpro_prod
BIGQUERY_PROJECT=bobs-brain-prod
EOF
```

### Run Ferrari Edition Locally

```bash
# Test all systems
python3 test_ferrari.py

# Output should show:
# ✅ Gemini: Connected
# ✅ Neo4j: 286 nodes found
# ✅ ChromaDB: Initialized
# ✅ BigQuery: Connected
# ✅ Datastore: Connected
# ✅ Graphiti: Ready (disabled)
# ✅ Slack: Polling active

# Run Ferrari
python3 bob_ferrari.py
```

### Deploy as System Service

```bash
# Install as systemd service (Linux)
sudo ./scripts/deployment/install-bob-service.sh

# Check status
sudo systemctl status bob-ferrari

# View logs
sudo journalctl -u bob-ferrari -f
```

---

## 📊 Deployment Comparison

| Aspect | v1 Simple | v2 Graph | v3 Production | v4 Ferrari |
|--------|-----------|----------|---------------|------------|
| **Setup Time** | 5 min | 30 min | 2 hours | 3 hours |
| **Cloud Services** | 0 | 1 (Neo4j) | 5+ | 6+ |
| **Monthly Cost** | $0 | $10 | $28 | $28 |
| **Dependencies** | 5 | 10 | 15 | 20 |
| **Complexity** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🆘 Troubleshooting

### Common Issues

**Slack not responding:**
- Check bot is in channel
- Verify tokens in .env
- Check Event Subscriptions URL

**Neo4j connection failed:**
- Verify credentials
- Check firewall rules
- Ensure indexes created

**Cloud Run timeout:**
- Increase timeout to 3600
- Check VPC connector
- Verify egress settings

**BigQuery permissions:**
- Grant BigQuery Admin role
- Check service account permissions
- Verify dataset exists

### Get Help

- GitHub Issues: [github.com/jeremylongshore/bobs-brain/issues](https://github.com/jeremylongshore/bobs-brain/issues)
- Documentation: This guide
- Logs: Check service logs for detailed errors

---

**Remember:** Start with v1 and upgrade as needed. Each version builds on the previous one!