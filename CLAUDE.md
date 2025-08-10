# CLAUDE.md - Bob's Brain Documentation
**CRITICAL: This is the SINGLE SOURCE OF TRUTH for Bob's Brain project**

## 🚨 CRITICAL RULES - READ FIRST
1. **GITHUB IS ALWAYS TRUTH**: Always pull latest from GitHub before making changes
2. **CURRENT MODE**: Bob uses Socket Mode (WebSocket) - NOT HTTP mode yet
3. **GRAPHITI MIGRATION**: In progress - enhancing Bob with knowledge graph memory
4. **USE CORRECT CODE**: `bob_firestore.py` for Socket Mode (current), `bob_cloud_run.py` needs conversion
5. **ALWAYS UPDATE GITHUB**: After ANY change, commit and push to GitHub

## 🤖 BOB'S BRAIN CURRENT STATUS
**Environment:** Development VM (thebeast - 4 CPU, 15GB RAM)
**Project:** bobs-house-ai (diagnostic-pro-mvp)  
**GitHub:** https://github.com/jeremylongshore/bobs-brain (branch: enhance-bob-graphiti)
**Last Updated:** 2025-08-10T23:15:00Z
**GCP Credits:** $2,251.82 available (expires 2025-2026)

## 📊 ARCHITECTURE TRANSITION IN PROGRESS
- **Current Mode:** ⚠️ Socket Mode (requires persistent connection)
- **Target Mode:** HTTP Mode for Cloud Run (conversion needed)
- **Primary Database:** ✅ Firestore (5 docs migrated from ChromaDB)
- **Knowledge Graph:** 🚧 Graphiti planned (requires Neo4j)
- **Vertex AI:** ✅ Working (Gemini 1.5 Flash)
- **Test Status:** 66.7% passing (Memory ✅, Firestore ✅, Graphiti ❌)

## 📁 PROJECT STRUCTURE
```
/home/jeremylongshore/bobs-brain/
├── src/
│   ├── bob_firestore.py       # ✅ ACTIVE - Socket Mode version (current)
│   ├── bob_cloud_run.py       # ⚠️ NEEDS CONVERSION - HTTP server version
│   ├── bob_memory.py          # ✅ NEW - Graphiti/Firestore memory system
│   ├── bob_base.py            # ✅ NEW - Base model with specializations
│   ├── bob_ultimate.py        # ❌ DEPRECATED - Legacy version
│   ├── bob_legacy_v2.py       # ❌ DEPRECATED - Old backup
│   ├── knowledge_loader.py    # Shared knowledge base loader
│   └── migrate_to_firestore.py # One-time migration tool
├── tests/
│   ├── test_memory_only.py    # ✅ Memory system tests
│   ├── test_bob_base.py       # ⚠️ Full test suite
│   └── run_all_tests.py       # Master test runner
├── GRAPHITI_MIGRATION_PLAN.md # ✅ Migration strategy document
├── requirements-cloudrun.txt  # Minimal deps for Cloud Run
├── requirements.txt           # Full deps including test tools
├── Dockerfile                 # For Cloud Run deployment
├── SLACK_SETUP.md            # Slack configuration
├── CLAUDE.md                 # THIS FILE - SINGLE SOURCE OF TRUTH
└── .gitignore                # Protects secrets
```

## 🔄 MIGRATION ROADMAP (STEP BY STEP)

### Phase 1: Local Testing (Current)
1. ✅ Bob running with Socket Mode locally
2. ✅ Firestore database connected
3. ✅ Memory system tests passing
4. 🚧 Fix Graphiti initialization parameters
5. ⏳ Install Neo4j locally for testing

### Phase 2: Cloud Infrastructure
1. ⏳ Deploy Neo4j to GCP Compute Engine
2. ⏳ Convert Bob from Socket Mode to HTTP
3. ⏳ Test HTTP mode locally with Flask
4. ⏳ Deploy Bob to Cloud Run

### Phase 3: Data Migration
1. ⏳ Migrate Firestore docs to Graphiti
2. ⏳ Import ChromaDB vectors
3. ⏳ Build knowledge graph relationships
4. ⏳ Test complete system

## 🚀 HOW TO DEPLOY (FUTURE - AFTER CONVERSION)

### Prerequisites Check
```bash
# 1. ALWAYS check current status first
gcloud run services list --region us-central1 | grep bob

# 2. If you see multiple bob services, DELETE extras:
# gcloud run services delete [duplicate-service-name] --region us-central1

# 3. Pull latest from GitHub
cd ~/bobs-brain
git pull origin bobs-brain-birthed
```

### Deploy to Cloud Run
```bash
cd ~/bobs-brain

# Deploy using optimized Dockerfile and requirements-cloudrun.txt
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --project bobs-house-ai \
  --port 3000 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars "SLACK_BOT_TOKEN=xoxb-[token],SLACK_APP_TOKEN=xapp-[token],SLACK_SIGNING_SECRET=[secret],GCP_PROJECT=bobs-house-ai"
```

## 🔧 SLACK CONFIGURATION

### Current Tokens (Store in Cloud Run env vars ONLY)
- **Bot Token:** xoxb-9318399480516-9316254671362-[rest]
- **App Token:** xapp-1-A099YKLCM1N-9312940498067-[rest]
- **Signing Secret:** d00942f9329d902a0af65f31f968f355

### Slack App Settings
1. Go to https://api.slack.com/apps
2. Event Subscriptions URL: `https://bobs-brain-157908567967.us-central1.run.app/slack/events`
3. Required OAuth Scopes:
   - chat:write
   - channels:history
   - im:history
   - groups:history
   - app_mentions:read

## 🧪 TESTING

### Test Health Check
```bash
curl https://bobs-brain-157908567967.us-central1.run.app/health
```

### Test Slack Integration
```bash
python3 test_slack_verification.py
```

### Check Logs
```bash
gcloud run services logs read bobs-brain --region us-central1 --limit 50
```

## ⚠️ KNOWN ISSUES & FIXES

### Issue: Graphiti initialization error
**Problem:** `Graphiti.__init__() got an unexpected keyword argument 'neo4j_uri'`
**Fix:** Use host/port parameters instead:
```python
# Wrong
Graphiti(neo4j_uri="bolt://localhost:7687")
# Correct
Graphiti(host="localhost", port=7687)
```

### Issue: Socket Mode vs HTTP confusion
**Problem:** Cloud Run requires HTTP endpoints, Bob uses Socket Mode
**Fix:** Need to convert bob_firestore.py to HTTP mode with Flask

### Issue: Neo4j not available
**Problem:** Graphiti requires Neo4j database
**Fix:** Install Neo4j locally or deploy to GCP

### Issue: Firestore query needs index
**Problem:** Temporal queries require composite index
**Fix:** Create index in Firestore console

## 📝 DEVELOPMENT WORKFLOW

1. **ALWAYS START WITH:**
   ```bash
   cd ~/bobs-brain
   git pull origin bobs-brain-birthed
   ```

2. **Make changes locally**

3. **Test locally if needed:**
   ```bash
   PORT=5000 python3 src/bob_cloud_run.py
   ```

4. **Commit and push to GitHub:**
   ```bash
   git add [files]
   git commit -m "Clear description"
   git push origin bobs-brain-birthed
   ```

5. **Deploy to Cloud Run** (see deployment section above)

## 🔴 WHAT NOT TO DO
- ❌ DO NOT create multiple Cloud Run services
- ❌ DO NOT use requirements.txt for Cloud Run (too heavy)
- ❌ DO NOT use bob_firestore.py for Cloud Run (wrong mode)
- ❌ DO NOT commit secrets to GitHub (.env files)
- ❌ DO NOT deploy without pulling latest from GitHub first
- ❌ DO NOT use bob_ultimate.py or bob_legacy_v2.py (outdated)

## 📊 PROJECT HISTORY
- **2025-08-10 23:15:** Updated documentation to reflect actual architecture
- **2025-08-10 Evening:** Created Graphiti migration plan
- **2025-08-10 Afternoon:** Built Bob Base Model with specializations
- **2025-08-10 Morning:** Migrated ChromaDB to Firestore (5 docs)
- **2025-08-09:** Bob's Brain birthed and initial recovery
- **Current Focus:** Graphiti knowledge graph integration

## 🎯 NEXT STEPS CHECKLIST

### Immediate Actions:
1. ✅ Read this CLAUDE.md file first
2. Fix Graphiti parameters in bob_memory.py (host/port not neo4j_uri)
3. Install Neo4j locally for testing
4. Test Graphiti connection
5. Convert Socket Mode to HTTP for Cloud Run

### Testing Commands:
```bash
# Run memory tests
python3 tests/test_memory_only.py

# Run all tests
python3 run_all_tests.py

# Check current Bob
python3 src/bob_firestore.py  # Requires Slack tokens
```

## 🆘 EMERGENCY RECOVERY
If Bob is completely broken:
1. Working code in GitHub: https://github.com/jeremylongshore/bobs-brain
2. Current branch: `enhance-bob-graphiti`
3. Stable branch: `bobs-brain-birthed`
4. For Socket Mode: Use `bob_firestore.py` with Slack tokens
5. For testing: Use `tests/test_memory_only.py` (no tokens needed)

## 💡 KEY INSIGHTS
- Graphiti requires Neo4j (graph database)
- Socket Mode needs conversion for Cloud Run
- $2,251.82 GCP credits available (19+ months free)
- Memory system works with Firestore fallback
- Test coverage at 66.7% (Graphiti failing due to Neo4j)

---
**Remember: This file is the SINGLE SOURCE OF TRUTH. When in doubt, follow this guide.**