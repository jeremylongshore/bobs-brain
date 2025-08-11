# 🔄 FIRESTORE + GRAPHITI DUAL MEMORY INTEGRATION

**Status:** Ready for Deployment  
**Purpose:** Keep Firestore active for customer data collection while using Graphiti for intelligence

## 🎯 THE SOLUTION: DUAL MEMORY SYSTEM

Bob now uses BOTH systems in harmony:
- **Firestore**: Continues collecting customer data from website
- **Graphiti**: Provides intelligent knowledge graph capabilities
- **Auto-Sync**: New customer data automatically flows to Graphiti

## 📊 CURRENT FIRESTORE DATA (1,100 Documents)

| Collection | Count | Purpose | Integration |
|------------|-------|---------|-------------|
| **knowledge** | 980 | Historical knowledge base | Searchable by Bob |
| **diagnostic_submissions** | 5 | Customer repair quotes | Auto-synced to Graphiti |
| **memory_episodes** | 74 | Bob's memories | Preserved & searchable |
| **bob_conversations** | 13 | Chat logs | Dual storage |
| **shared_context** | 11 | Shared info | Available to Bob |
| **Others** | 17 | Various data | Accessible as needed |

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────┐
│      CUSTOMER WEBSITE           │
│   (Submits diagnostic data)     │
└────────────┬────────────────────┘
             │ Webhook
             ▼
┌─────────────────────────────────┐
│      FIRESTORE DATABASE         │
│   diagnostic-pro-mvp/bob-brain  │
│   (Stores customer submissions) │
└────────────┬────────────────────┘
             │ Auto-sync
             ▼
┌─────────────────────────────────┐
│    BOB'S DUAL MEMORY SYSTEM     │
│                                 │
│  ┌──────────┐   ┌──────────┐   │
│  │Firestore │◄─►│ Graphiti │   │
│  │  Reader  │   │   Graph  │   │
│  └──────────┘   └──────────┘   │
│                                 │
│      Vertex AI (Responses)      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│         SLACK WORKSPACE         │
│    (Bob responds with full      │
│     customer & knowledge data)  │
└─────────────────────────────────┘
```

## 🚀 DEPLOYMENT INSTRUCTIONS

### 1. Build the Dual Memory Container
```bash
cd ~/bobs-brain
docker build -f Dockerfile.dual -t gcr.io/bobs-house-ai/bob-dual-memory .
```

### 2. Push to Container Registry
```bash
docker push gcr.io/bobs-house-ai/bob-dual-memory
```

### 3. Deploy to Cloud Run
```bash
gcloud run deploy bobs-brain \
  --image gcr.io/bobs-house-ai/bob-dual-memory \
  --region us-central1 \
  --project bobs-house-ai \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --port 8080 \
  --min-instances 1 \
  --max-instances 10 \
  --set-env-vars "SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN,SLACK_APP_TOKEN=$SLACK_APP_TOKEN,GCP_PROJECT=bobs-house-ai,NEO4J_URI=bolt://10.128.0.2:7687,NEO4J_USER=neo4j,NEO4J_PASSWORD=BobBrain2025,OPENAI_API_KEY=$OPENAI_API_KEY" \
  --service-account bob-firestore-reader@bobs-house-ai.iam.gserviceaccount.com
```

### 4. Configure Website Webhook
Point your website's customer submission form to:
```
POST https://bobs-brain-157908567967.us-central1.run.app/customer-webhook

{
  "name": "Customer Name",
  "email": "customer@email.com",
  "phone": "555-1234",
  "vehicle": "2020 Toyota Camry",
  "issue": "Brake replacement quote",
  "quote": 850.00
}
```

## 🔄 HOW IT WORKS

### Customer Submission Flow:
1. Customer submits diagnostic request on website
2. Data saved to Firestore `diagnostic_submissions` collection
3. Bob's sync process detects new submission
4. Data automatically added to Graphiti knowledge graph
5. Bob can now reference this customer data in responses

### Bob's Response Flow:
1. User asks Bob a question in Slack
2. Bob searches BOTH:
   - Graphiti knowledge graph (relationships, temporal data)
   - Firestore collections (customer data, historical knowledge)
3. Vertex AI generates response using combined context
4. Response includes relevant customer information when applicable

## 📡 API ENDPOINTS

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check with memory status |
| `/slack/events` | POST | Slack event handling |
| `/customer-webhook` | POST | Direct customer data submission |
| `/sync` | POST | Manual Firestore→Graphiti sync |
| `/` | GET | Service information |

## 🔑 KEY FEATURES

1. **Preserves Firestore Integration**: Website continues working unchanged
2. **Adds Graphiti Intelligence**: Knowledge graph for better understanding
3. **Auto-Sync**: Customer data flows to knowledge graph automatically
4. **Dual Search**: Bob searches both systems for comprehensive answers
5. **Customer Context**: Bob knows about recent customer submissions
6. **Temporal Awareness**: Tracks when things happened vs when learned

## 📊 BENEFITS

- **No Migration Required**: Keep using existing Firestore setup
- **Enhanced Intelligence**: Graphiti adds relationship understanding
- **Customer Data Integration**: Bob knows about website submissions
- **Scalable**: Both systems can grow independently
- **Redundancy**: Data exists in both systems for reliability

## 🧪 TESTING

### Test Customer Webhook:
```bash
curl -X POST https://bobs-brain-157908567967.us-central1.run.app/customer-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Customer",
    "email": "test@example.com",
    "vehicle": "2022 Honda Civic",
    "issue": "Oil change quote",
    "quote": 75.00
  }'
```

### Test Sync:
```bash
curl -X POST https://bobs-brain-157908567967.us-central1.run.app/sync
```

### Ask Bob About Customers:
In Slack: "Bob, what recent customer submissions have we received?"

## ⚙️ CONFIGURATION

### Required Environment Variables:
```bash
# Firestore Access
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GCP_PROJECT=diagnostic-pro-mvp

# Graphiti/Neo4j
NEO4J_URI=bolt://10.128.0.2:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=BobBrain2025

# Slack
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# AI (temporary)
OPENAI_API_KEY=sk-...
```

### Service Account Permissions:
- `roles/datastore.user` on diagnostic-pro-mvp
- `roles/firestore.reader` on bob-brain database

## 🎯 RESULT

Bob now has:
- **Complete access** to 1,100 Firestore documents
- **Real-time updates** from customer submissions
- **Intelligent relationships** via Graphiti
- **Unified responses** combining all data sources

The website continues collecting customer data unchanged, while Bob becomes smarter with every interaction!