# 🎯 PROJECT TRACKING - WHICH PROJECT TO USE

## 🔴 CRITICAL: TWO PROJECTS EXIST

### 1. `bobs-house-ai` (PRIMARY - USE THIS)
- **Purpose:** Bob's Brain deployment
- **What's here:**
  - Cloud Run (Bob's deployment)
  - Vertex AI / Gemini access
  - BigQuery for ML
  - Neo4j VM
  - $2,251 credits
- **When to use:** ALWAYS for Bob's code and deployment

### 2. `diagnostic-pro-mvp` (SECONDARY - DATA ONLY)
- **Purpose:** Customer data storage
- **What's here:**
  - Firestore database (1,100 documents)
  - Customer submissions
  - Historical data
- **When to use:** Only when accessing Firestore data

## 🎯 CURRENT STATUS

**WE ARE WORKING IN:** `bobs-house-ai`

**Bob is deployed in:** `bobs-house-ai`

**Bob reads data from:** `diagnostic-pro-mvp` (Firestore)

## 🔧 HOW TO STAY IN THE RIGHT PROJECT

### Always set project before working:
```bash
# Set the project
gcloud config set project bobs-house-ai

# Verify you're in the right project
gcloud config get-value project
# Should output: bobs-house-ai
```

### In Python code:
```python
# For Vertex AI
vertexai.init(project='bobs-house-ai', location='us-central1')

# For Firestore (different project!)
firestore_client = firestore.Client(project='diagnostic-pro-mvp')

# For BigQuery
bigquery_client = bigquery.Client(project='bobs-house-ai')
```

### Environment variables:
```bash
export GOOGLE_CLOUD_PROJECT=bobs-house-ai
export GCP_PROJECT=bobs-house-ai
```

## 🎯 DEPLOYMENT COMMANDS

### ALWAYS deploy to bobs-house-ai:
```bash
gcloud run deploy bobs-brain \
  --project bobs-house-ai \  # <-- ALWAYS SPECIFY PROJECT
  --region us-central1 \
  --source .
```

## ⚠️ COMMON MISTAKES

1. **Wrong project for Vertex AI**
   - ❌ Using `diagnostic-pro-mvp`
   - ✅ Use `bobs-house-ai`

2. **Wrong project for deployment**
   - ❌ Deploying to `diagnostic-pro-mvp`
   - ✅ Deploy to `bobs-house-ai`

3. **Forgetting to set project**
   - Always run: `gcloud config set project bobs-house-ai`

## 📍 REMEMBER

**Bob lives in:** `bobs-house-ai`

**Bob's data lives in:** `diagnostic-pro-mvp` (Firestore only)

**Everything else:** `bobs-house-ai`
