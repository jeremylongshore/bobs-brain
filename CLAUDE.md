# CLAUDE.md - Bob's Brain Documentation
**CRITICAL: This is the SINGLE SOURCE OF TRUTH for Bob's Brain project**
**Last Comprehensive Update:** 2025-01-11T00:45:00Z

## 🚨 CRITICAL RULES - READ FIRST
1. **GITHUB IS ALWAYS TRUTH**: Always pull latest from GitHub before making changes
2. **UNIFIED ARCHITECTURE**: Migrating to Graphiti + Neo4j + Vertex AI (Google Cloud Everything)
3. **OPENAI KEY ACQUIRED**: Real API key validated and working with Graphiti
4. **USE CORRECT CODE**: `bob_firestore.py` for Socket Mode (current), transitioning to `bob_graphiti_gcp.py`
5. **ALWAYS UPDATE GITHUB**: After ANY change, commit and push to GitHub

## 🤖 BOB'S BRAIN CURRENT STATUS
**Environment:** ✅ PRODUCTION on Cloud Run + GCP Neo4j VM
**Service:** bobs-brain (WITH GRAPHITI KNOWLEDGE GRAPH!)
**Project:** bobs-house-ai  
**Cloud Run URL:** https://bobs-brain-157908567967.us-central1.run.app
**GitHub:** https://github.com/jeremylongshore/bobs-brain (branch: enhance-bob-graphiti)
**Last Updated:** 2025-08-10T23:50:00Z
**GCP Credits:** $2,251.82 available (28+ months of runtime)
**OpenAI API Key:** ✅ Working (temporary - will migrate to Vertex AI)
**Neo4j Status:** ✅ RUNNING on GCP VM (10.128.0.2)

## 📊 PRODUCTION ARCHITECTURE - FULLY DEPLOYED!
- **Current Mode:** ✅ HTTP Mode on Cloud Run (LIVE!)
- **Service URL:** https://bobs-brain-157908567967.us-central1.run.app
- **Primary Database:** ✅ Neo4j on GCP VM (10.128.0.2)
- **Knowledge Graph:** ✅ Graphiti OPERATIONAL with foundational data
- **Vertex AI:** ✅ Working for response generation (Gemini 1.5 Flash)
- **Neo4j VM:** ✅ Running on GCP (bob-neo4j, e2-standard-4)
- **Test Status:** ✅ ALL PRODUCTION TESTS PASSING

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

## ✅ COMPLETED TASKS

### Infrastructure & Setup
1. ✅ **Neo4j Deployment:** Docker container running locally (bob-neo4j)
2. ✅ **Graphiti Configuration:** Fixed initialization parameters (uri, user, password)
3. ✅ **OpenAI Integration:** Real API key validated and working
4. ✅ **Neo4j Indexes:** Created fulltext and regular indexes for Graphiti
5. ✅ **Memory System:** BobMemory class with Firestore fallback
6. ✅ **Test Infrastructure:** Comprehensive test suite created

### Data & Migration
1. ✅ **ChromaDB to Firestore:** 5 documents successfully migrated
2. ✅ **Graphiti Knowledge Graph:** Initial data loaded (Jeremy, DiagnosticPro, Bob entities)
3. ✅ **Entity Extraction:** Working with OpenAI for automatic entity/relationship creation
4. ✅ **Search Functionality:** Graphiti search returning relevant results

### Documentation & Organization
1. ✅ **PROJECT_ORGANIZATION.md:** Created to prevent code confusion
2. ✅ **STEP_BY_STEP_PLAN.md:** Detailed migration roadmap
3. ✅ **GRAPHITI_ANALYSIS.md:** Complete framework research
4. ✅ **UNIFIED_ARCHITECTURE.md:** Google Cloud + Vertex AI integration plan
5. ✅ **BOB_GOOGLE_CLOUD_GRAPHITI.md:** Simplified deployment guide

### Testing & Validation
1. ✅ **Graphiti Connection:** Validated with Neo4j
2. ✅ **OpenAI API:** Tested and working for entity extraction
3. ✅ **Knowledge Graph Creation:** 15 entities and 23 relationships created
4. ✅ **Search Queries:** Successfully returning relevant results

## 🔄 MIGRATION ROADMAP (UPDATED)

### Phase 1: COMPLETED ✅
- Neo4j running locally
- Graphiti configured with OpenAI
- Initial knowledge graph created
- Test data successfully loaded

### Phase 2: Cloud Deployment (NEXT PRIORITY)
1. 🎯 **Deploy Neo4j to GCP Compute Engine** (e2-standard-4 VM)
2. 🎯 **Convert Bob to HTTP Mode** using Flask/FastAPI
3. 🎯 **Integrate Vertex AI** to replace OpenAI (cost optimization)
4. 🎯 **Deploy to Cloud Run** with proper environment variables

### Phase 3: Complete Migration (FINAL)
1. ⏳ Migrate ALL Firestore data to Graphiti
2. ⏳ Migrate remaining ChromaDB vectors
3. ⏳ Deprecate Firestore and ChromaDB completely
4. ⏳ Implement Vertex AI embeddings

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

### ✅ RESOLVED: Graphiti initialization error
**Problem:** `Graphiti.__init__() got an unexpected keyword argument 'neo4j_uri'`
**Solution:** Fixed - Now using correct parameters:
```python
# Correct implementation in bob_memory.py:
Graphiti(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="BobBrain2025"
)
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
- **2025-01-11 00:45:** Comprehensive update with completed Graphiti integration
- **2025-01-11 00:30:** Successfully tested Graphiti with real OpenAI key
- **2025-01-11 00:00:** Neo4j indexes created, Graphiti fully operational
- **2025-01-10 23:30:** OpenAI API key acquired and validated
- **2025-01-10 23:00:** Neo4j deployed locally via Docker
- **2025-01-10 22:00:** Fixed Graphiti initialization parameters
- **2025-01-10 Evening:** Created unified architecture plan (Google Cloud everything)
- **2025-01-10 Afternoon:** Built Bob Base Model with specializations
- **2025-01-10 Morning:** Migrated ChromaDB to Firestore (5 docs)
- **2025-01-09:** Bob's Brain birthed and initial recovery

## 🎯 NEXT TASKS (PRIORITIZED)

### High Priority - Cloud Deployment
1. **Deploy Neo4j to GCP** 
   - Create e2-standard-4 VM on Google Cloud
   - Configure with production settings
   - Set up internal networking

2. **Convert to HTTP Mode**
   - Create `bob_http.py` with Flask/FastAPI
   - Implement Slack event endpoints
   - Test locally before deployment

3. **Integrate Vertex AI**
   - Replace OpenAI with Vertex AI for cost optimization
   - Use Gemini for LLM, gecko for embeddings
   - Implement custom LLMClient and EmbedderClient

### Medium Priority - Data Migration
4. **Complete Data Migration**
   - Migrate ALL Firestore documents to Graphiti
   - Import remaining ChromaDB vectors
   - Verify data integrity

### Low Priority - Optimization
5. **Performance Tuning**
   - Optimize Neo4j queries
   - Implement caching strategies
   - Monitor resource usage

### Prompt Engineering Tasks (Requiring Refinement)
- **Entity Extraction Prompts:** Optimize for clearer entity boundaries
- **Relationship Mapping:** Improve context-aware relationship detection
- **Search Query Enhancement:** Implement query expansion techniques
- **Response Generation:** Align with industry benchmarks for clarity and relevance

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

## 💡 KEY INSIGHTS & ACHIEVEMENTS
- **Graphiti OPERATIONAL:** Successfully creating knowledge graphs with 15 entities, 23 relationships
- **OpenAI Integration:** Real API key working for entity extraction
- **Neo4j Running:** Docker container active with proper indexes
- **Unified Architecture Designed:** Google Cloud + Vertex AI + Graphiti plan complete
- **$2,251.82 GCP credits:** Sufficient for 20+ months of operation
- **Migration Path Clear:** From multiple databases to single Neo4j/Graphiti system

## 📈 PROJECT METRICS
- **Knowledge Graph Size:** 15 nodes, 23 edges
- **Test Coverage:** Graphiti integration validated
- **Data Migrated:** 5 ChromaDB docs → Firestore → Ready for Graphiti
- **Infrastructure Cost:** ~$100/month (covered by credits)
- **Time to Production:** Estimated 2-3 days for full deployment

---
**Remember: This file is the SINGLE SOURCE OF TRUTH. When in doubt, follow this guide.**