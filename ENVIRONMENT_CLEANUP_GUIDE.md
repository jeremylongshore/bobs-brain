# 🧹 ENVIRONMENT CLEANUP & ORGANIZATION GUIDE
**CRITICAL: Read this when you're confused about which file to use**

## 🔴 THE TRUTH: WHAT'S ACTUALLY RUNNING IN PRODUCTION

### LIVE IN PRODUCTION RIGHT NOW:
```bash
# This is what's ACTUALLY deployed:
File: src/bob_http_graphiti.py
URL: https://bobs-brain-sytrh5wz5q-uc.a.run.app
Status: WORKING but NOT using ML predictions
```

## 📁 FILE ORGANIZATION - WHAT TO USE

### ✅ PRODUCTION FILES (USE THESE)
```
python
/src/
  bob_http_graphiti.py     # ✅ PRODUCTION - Currently deployed
  bob_gcp_latest.py        # ✅ READY - Has ML integration, deploy this next
  data_ingestion_pipeline.py # ✅ READY - For web scraping
```

### ⚠️ EXPERIMENTAL FILES (DON'T USE YET)
```python
/src/
  bob_gcp_native.py        # Experimental - 100% GCP (no Graphiti)
  bob_graphiti_gemini.py   # Experimental - Testing Gemini integration
  bob_unified_graphiti.py  # Experimental - Trying to unify everything
  bob_vertex_native.py     # Experimental - Testing Vertex directly
  bob_dual_memory.py       # Experimental - Dual database approach
```

### ❌ DEPRECATED FILES (DELETE THESE)
```python
/src/
  bob_firestore.py         # OLD - Socket mode, not for Cloud Run
  bob_cloud_run.py         # OLD - Before Graphiti
  bob_ultimate.py          # OLD - Legacy version
  bob_base.py              # OLD - Over-engineered
  bob_legacy_v2.py         # OLD - Backup
```

## 🔧 SETUP FILES - WHAT EACH DOES

### ML Setup (USE IN THIS ORDER)
```bash
1. deploy_bigquery_ml.py      # Run FIRST - Creates BigQuery ML models ($5/mo)
2. official_automl_setup.py   # Run SECOND - Creates AutoML models ($20/model)
3. setup_gcp_monitoring.py    # Run THIRD - Sets up all logging/debugging
```

### Infrastructure Setup
```bash
setup_ml_models.sh           # Bash script version of ML setup
deploy_all_ml.sh            # Deploys everything at once
setup_bigquery_sync.sh      # Syncs Firestore → BigQuery
```

## 📝 DOCUMENTATION FILES - READ IN THIS ORDER

### 1. START HERE (Core Docs)
```
CLAUDE.md                    # 🔴 SINGLE SOURCE OF TRUTH - Read first!
BOB_STRATEGIC_ASSESSMENT.md  # Current state + what needs fixing
ENVIRONMENT_CLEANUP_GUIDE.md # THIS FILE - When confused
```

### 2. ARCHITECTURE (How It Works)
```
GRAPHITI_ARCHITECTURE.md     # How Graphiti connects everything
FIRESTORE_VS_BIGQUERY.md     # Why we need both databases
ML_INTEGRATION_GUIDE.md      # How ML models work
```

### 3. REFERENCE (When Needed)
```
DATA_MIGRATION_COMPLETE.md   # Migration history
FIRESTORE_GRAPHITI_INTEGRATION.md # Integration details
SLACK_SETUP.md              # Slack configuration
```

## 🚫 FILES TO DELETE (Clean up confusion)

```bash
# Run this to clean up deprecated files:
rm src/bob_firestore.py
rm src/bob_cloud_run.py
rm src/bob_ultimate.py
rm src/bob_base.py
rm src/bob_legacy_v2.py
rm src/bob_memory.py
rm knowledge_loader.py
rm migrate_to_firestore.py

# Remove old test files
rm test_*.py
rm check_production_data.py
rm migrate_*.py

# Remove duplicate configs
rm requirements.txt          # Keep requirements-gcp.txt
rm requirements-cloudrun.txt  # Keep requirements-gcp.txt
rm requirements-dual.txt      # Keep requirements-gcp.txt
rm Dockerfile                 # Keep Dockerfile.gcp
rm Dockerfile.dual           # Keep Dockerfile.gcp
rm Dockerfile.production     # Keep Dockerfile.gcp
```

## 🎯 WHAT TO DO NEXT (PRIORITY ORDER)

### 1. IMMEDIATE (Do Right Now)
```bash
# Deploy bob_gcp_latest.py which HAS ML integration
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --entry-point "python src/bob_gcp_latest.py"
```

### 2. TODAY
```bash
# Set up ML models
python3 deploy_bigquery_ml.py
python3 setup_gcp_monitoring.py
```

### 3. THIS WEEK
```bash
# Train AutoML (optional, costs $20)
python3 official_automl_setup.py

# Start data ingestion
python3 src/data_ingestion_pipeline.py
```

## 🎆 CURRENT ARCHITECTURE (SIMPLIFIED)

```
         USER
           ↓
        SLACK
           ↓
    BOB (Cloud Run)
    bob_gcp_latest.py
           ↓
    ┌─────┴─────┐
    ↓           ↓
GRAPHITI    BIGQUERY ML
(Knowledge)  (Predictions)
    ↓           ↓
  NEO4J     ML MODELS
```

## ⚠️ COMMON CONFUSIONS & FIXES

### Q: "Which file is actually running?"
**A:** `src/bob_http_graphiti.py` is LIVE but needs ML. Deploy `bob_gcp_latest.py` to fix.

### Q: "Do we need Graphiti?"
**A:** NO! We can use 100% Google Cloud. Use `bob_gcp_native.py` if you want pure GCP.

### Q: "Why so many bob_*.py files?"
**A:** Evolution. Each was an attempt. `bob_gcp_latest.py` is the best version.

### Q: "What about all these requirements.txt files?"
**A:** Only keep `requirements-gcp.txt`. Delete the rest.

### Q: "Should I use AutoML or BigQuery ML?"
**A:** Start with BigQuery ML ($5). Add AutoML later if needed ($20).

## 📝 QUICK REFERENCE COMMANDS

```bash
# Check what's deployed
gcloud run services describe bobs-brain --region us-central1

# View logs
gcloud run services logs read bobs-brain --limit 50

# Deploy new version
gcloud run deploy bobs-brain --source . --region us-central1

# Test locally
PORT=8080 python3 src/bob_gcp_latest.py

# Run ML setup
python3 deploy_bigquery_ml.py

# Check costs
gcloud billing accounts list
```

## 🔴 REMEMBER

1. **bob_http_graphiti.py** = What's running NOW (broken ML)
2. **bob_gcp_latest.py** = What SHOULD be running (fixed ML)
3. **CLAUDE.md** = Single source of truth
4. **$2,251 credits** = 30+ months of runtime

---
**When lost, return to this file!**