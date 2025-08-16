# Claude Handoff Guide - Bob's Brain Project
**Last Updated:** 2025-08-13
**Prepared By:** Previous Claude Session
**Purpose:** Complete handoff documentation for next Claude session

---

## 🎯 IMMEDIATE CONTEXT

You are taking over Bob's Brain project. This is Jeremy's AI assistant that:
- Responds in Slack using Gemini 2.5 Flash
- Learns from every interaction
- Scrapes 40+ technical sources for equipment repair knowledge
- Integrates with customer website for diagnostic submissions

**CRITICAL:** Jeremy has $1000s in Vertex AI/Google Cloud credits. NEVER use OpenAI. Always use Gemini/Vertex AI.

---

## ✅ WHAT WAS ACCOMPLISHED TODAY (2025-08-13)

### 1. Neo4j Migration to Cloud (COMPLETE)
**Previous State:** Neo4j running on VM costing $50/month
**Current State:** Migrated to Neo4j Aura Free Tier

```
Neo4j Aura Credentials (ACTIVE):
- Instance ID: d3653283
- URI: neo4j+s://d3653283.databases.neo4j.io
- Username: neo4j
- Password: q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE
- Status: ✅ Connected and working
```

**Actions Taken:**
- Created Neo4j Aura client (`src/neo4j_aura_client.py`)
- Updated Bob Brain to use Aura instead of VM
- Deployed Bob with new credentials
- Verified connection working
- Old VM still running but can be deleted to save $50/month

### 2. Data Integration Architecture (COMPLETE)
**Created comprehensive data pipeline between all systems:**

```
Website Form → BigQuery → Neo4j Aura → AI Processing → Customer Response
```

**Files Created:**
- `src/datastore_to_bigquery_migration.py` - Migrates MVP3 data with enhanced schema
- `src/website_form_bigquery_integration.py` - Handles website form submissions
- `src/neo4j_bigquery_sync.py` - Bidirectional sync between Neo4j and BigQuery
- `src/gcp_neo4j_integration.py` - Google Cloud APIs for Neo4j

### 3. Enhanced BigQuery Schema (COMPLETE)
**Created future-proof schema with 70+ fields including:**
- Customer information (name, email, phone, company, fleet size)
- Equipment details (type, brand, model, serial, hours, condition)
- Problem data (description, category, error codes, symptoms)
- Website tracking (session, UTM parameters, user behavior)
- AI/ML fields (confidence, sentiment, priority, churn risk)
- Revenue tracking (lead score, conversion value, lifetime value)

### 4. Slack Integration (WORKING)
**Bob is responding in Slack with these tokens:**
```
SLACK_BOT_TOKEN: [REDACTED - Check Secret Manager]
SLACK_APP_TOKEN: [REDACTED - Check Secret Manager]
SLACK_SIGNING_SECRET: [REDACTED - Check Secret Manager]
```

### 5. Data Migration Investigation (COMPLETE)
**Finding:** The "900+ items" mentioned in docs don't exist
- ChromaDB has only 5 documents
- MVP3 Datastore is empty
- BigQuery tables exist but are empty
- Created scripts to generate 1000+ diagnostic scenarios when needed

---

## 🚨 WHAT NEEDS TO BE DONE NOW

### PRIORITY 1: Stop the old Neo4j VM (Save $50/month)
```bash
# First, verify Neo4j Aura is working
curl https://bobs-brain-sytrh5wz5q-uc.a.run.app/health
# Should show "neo4j": true

# Then stop the VM
gcloud compute instances stop bob-neo4j --zone=us-central1-a

# Or delete it permanently (after confirming Aura works for a few days)
gcloud compute instances delete bob-neo4j --zone=us-central1-a
```

### PRIORITY 2: Populate Data (Currently Empty)
The system is built but needs data. Run these:

```bash
# 1. Generate 1000+ diagnostic scenarios
python3 src/complete_data_migration.py

# 2. Run comprehensive scraping
curl -X POST https://unified-scraper-157908567967.us-central1.run.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"type": "full"}'

# 3. Run YouTube equipment scraping
curl -X POST https://unified-scraper-157908567967.us-central1.run.app/scrape/youtube \
  -H "Content-Type: application/json" \
  -d '{"query": "bobcat repair", "max_results": 50}'
```

### PRIORITY 3: Update Circle of Life to Use BigQuery
Currently, Circle of Life still reads from Datastore. Update `src/circle_of_life.py`:

```python
# Change line 56 FROM:
self.datastore_client = datastore.Client(project=self.mvp_project)

# TO: Read from BigQuery instead
# Query from bobs-house-ai.mvp3_migrated.diagnostics
```

### PRIORITY 4: Connect Website Forms
The backend is ready but website needs to point to new endpoints:

**New Endpoints Available:**
- `POST /submit-diagnostic` - Main form submission
- `POST /customer-webhook` - Backward compatible
- `GET /check-status/<submission_id>` - Check submission status

**To Deploy:**
```bash
gcloud run deploy website-form-integration \
  --source . \
  --region us-central1 \
  --set-env-vars "PROJECT_ID=bobs-house-ai,NEO4J_URI=neo4j+s://d3653283.databases.neo4j.io,NEO4J_PASSWORD=q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE"
```

### PRIORITY 5: Setup Automated Syncs
```bash
# Create scheduled job for Neo4j-BigQuery sync
gcloud scheduler jobs create http neo4j-bigquery-sync \
  --location us-central1 \
  --schedule "0 */4 * * *" \
  --uri "https://bobs-brain-sytrh5wz5q-uc.a.run.app/sync/neo4j-bigquery" \
  --http-method POST
```

---

## 📁 PROJECT STRUCTURE OVERVIEW

### Active Services (Cloud Run)
| Service | URL | Purpose | Status |
|---------|-----|---------|--------|
| bobs-brain | https://bobs-brain-sytrh5wz5q-uc.a.run.app | Main AI service | ✅ Running |
| unified-scraper | https://unified-scraper-157908567967.us-central1.run.app | Data collection | ✅ Running |
| circle-of-life-scraper | https://circle-of-life-scraper-157908567967.us-central1.run.app | Learning system | ✅ Running |

### Key Files You'll Work With
```
src/
├── bob_brain_v5.py              # Main Bob Brain (PRODUCTION)
├── circle_of_life.py            # Learning system (needs BigQuery update)
├── website_form_bigquery_integration.py  # New form handler (needs deployment)
├── neo4j_bigquery_sync.py      # Data sync (needs scheduling)
└── datastore_to_bigquery_migration.py   # Migration script (ready to run)
```

### Documentation Files
```
CLAUDE.md                        # Main project documentation
COMPLETE_DATA_INTEGRATION.md     # Data architecture overview
NEO4J_MIGRATION_COMPLETE.md      # Neo4j migration details
DATA_MIGRATION_STATUS.md         # Current data status
THIS FILE                        # Your handoff guide
```

---

## 🔧 COMMON COMMANDS YOU'LL NEED

### Check System Health
```bash
# Bob's health
curl https://bobs-brain-sytrh5wz5q-uc.a.run.app/health

# Test Neo4j connection
python3 test_neo4j_aura.py

# Check BigQuery data
bq query --use_legacy_sql=false "SELECT COUNT(*) FROM \`bobs-house-ai.knowledge_base.unified_knowledge\`"
```

### Deploy Changes
```bash
# Deploy Bob Brain
gcloud run deploy bobs-brain --source . --region us-central1

# Deploy with environment variables
gcloud run deploy bobs-brain \
  --set-env-vars "NEO4J_URI=neo4j+s://d3653283.databases.neo4j.io,NEO4J_PASSWORD=q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE"
```

### Monitoring
```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=bobs-brain" --limit 50

# Check costs
gcloud billing accounts list
```

---

## ⚠️ CRITICAL WARNINGS

1. **NEVER use OpenAI** - Jeremy has Vertex AI credits, not OpenAI
2. **Don't create duplicate Cloud Run services** - Check existing before deploying
3. **The website frontend was NOT modified** - Only backend APIs created
4. **Neo4j VM still running** - Delete it to save $50/month
5. **Data is currently empty** - Needs population through scripts

---

## 📊 CURRENT SYSTEM STATE

### What's Working
- ✅ Bob responding in Slack
- ✅ Neo4j Aura connected (free tier)
- ✅ BigQuery schemas created
- ✅ Scraper services running
- ✅ API endpoints ready

### What Needs Work
- ❌ No data in BigQuery (run migration/generation scripts)
- ❌ Circle of Life still using Datastore (needs update)
- ❌ Website forms not connected to new endpoints
- ❌ Old Neo4j VM still running ($50/month waste)
- ❌ Automated syncs not scheduled

---

## 🎯 SUCCESS CRITERIA

When you're done, the system should:
1. Have 1000+ items in BigQuery knowledge base
2. Neo4j VM deleted (saving $50/month)
3. Website forms storing data in enhanced schema
4. Circle of Life reading from BigQuery not Datastore
5. Automated Neo4j-BigQuery sync running every 4 hours

---

## 💡 QUICK WINS

1. **Stop Neo4j VM** - Immediate $50/month savings
2. **Run data generation** - Get 1000+ items in minutes
3. **Deploy form handler** - Start collecting customer data
4. **Schedule scrapers** - Continuous data collection

---

## 📞 CONTACT & RESOURCES

- **Project:** bobs-house-ai
- **GitHub:** https://github.com/jeremylongshore/bobs-brain
- **Neo4j Console:** https://console.neo4j.io (login with Google)
- **GCP Console:** https://console.cloud.google.com

---

**Good luck! The system is ready, it just needs data and final connections.**

---
*Generated by Claude on 2025-08-13 for seamless handoff to next Claude session*
