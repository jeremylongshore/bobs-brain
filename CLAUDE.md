# CLAUDE.md - Bob's Brain Documentation

## 🤖 BOB'S BRAIN STATUS
**Service:** bobs-brain
**Project:** bobs-house-ai  
**Cloud Run URL:** https://bobs-brain-157908567967.us-central1.run.app
**GitHub:** https://github.com/jeremylongshore/bobs-brain
**Updated:** 2025-08-10T20:17:00Z

## ✅ DEPLOYMENT STATUS - LIVE ON CLOUD RUN!
- **Cloud Run:** ✅ DEPLOYED & RUNNING
- **Slack Tokens:** ✅ CONFIGURED
- **Vertex AI:** ✅ Working (but DEPRECATED - dies June 2026)
- **Database:** ✅ MIGRATED TO FIRESTORE (bob-brain database)
  - ChromaDB: Legacy fallback at /home/jeremylongshore/bobs-brain/chroma_data
  - Firestore: Cloud-native at projects/diagnostic-pro-mvp/databases/bob-brain

## DIRECTORY STRUCTURE
```
/home/jeremylongshore/bobs-brain/
├── src/
│   ├── bob_cloud_run.py       # 🚀 CLOUD RUN VERSION - DEPLOYED!
│   ├── bob_firestore.py       # Socket Mode version with Firestore
│   ├── bob_ultimate.py        # Legacy ChromaDB version
│   ├── bob_legacy_v2.py       # Backup of best recovered version
│   ├── knowledge_loader.py    # Knowledge base loader
│   ├── migrate_to_firestore.py # Migration tool
│   ├── bob_test_harness.py    # Testing framework
│   └── thebrain_integration.py # Firestore integration
├── chroma_data/               # Vector database storage
├── logs/                      # Bob's activity logs
├── requirements.txt           # Full dependencies (heavy)
├── requirements-cloudrun.txt  # Minimal Cloud Run dependencies
├── Dockerfile                 # Optimized Cloud Run deployment
├── SLACK_SETUP.md            # Slack app configuration guide
├── .env                      # Environment variables
└── CLAUDE.md                 # This file
```

## QUICK START
```bash
cd /home/jeremylongshore/bobs-brain
export SLACK_BOT_TOKEN=xoxb-YOUR-TOKEN-HERE
export SLACK_APP_TOKEN=xapp-YOUR-APP-TOKEN-HERE
export SLACK_SIGNING_SECRET=YOUR-SECRET-HERE
python3 src/bob_firestore.py  # NEW: Uses Firestore cloud database
```

## BOB FIRESTORE - THE CLOUD VERSION (600 lines)

### ✅ **FEATURES COMBINED FROM ALL VERSIONS:**
- **Professional communication** (from recovered-latest branch)
- **Duplicate message prevention** (from recovered-latest)
- **Smart memory management** with cleanup (from recovered-latest)
- **Vertex AI integration** with Gemini 2.0 (from local versions)
- **Health checks & monitoring** (from bob_production)
- **Robust error handling** (from bob_production)
- **Knowledge loader integration** (from recovered-latest)
- **Jeremy recognition** - knows who the boss is (from recovered-latest)
- **Conversation history** - remembers last 10 exchanges per user
- **Graceful shutdown** - handles signals properly
- **Thread safety** - no race conditions
- **Firestore cloud database** - persistent cloud storage (NEW!)
- **ChromaDB fallback** - automatic fallback if Firestore unavailable
- **Business context awareness** - DiagnosticPro focused

### 📊 **WHAT MAKES IT CLOUD-NATIVE:**
1. **Firestore Integration**: Cloud-persistent knowledge that survives restarts
2. **MVP3 Protection**: Safely coexists with diagnostic-pro-mvp data
3. **Smart Fallback**: Automatically uses ChromaDB if Firestore unavailable
4. **Duplicate Prevention**: Content hashing prevents duplicate migrations
5. **Cloud-First Design**: Ready for production deployment
6. **Future ready**: Easy to migrate to Google Gen AI SDK when needed

## WHAT BOB DOES
1. **Listens to Slack** - @mentions and DMs
2. **Searches Knowledge** - Firestore cloud database (with ChromaDB fallback)
3. **Generates Responses** - Vertex AI Gemini
4. **Learns** - Stores documents in Firestore (cloud-persistent)

## DEPLOYMENT
```bash
# Local Testing
cd /home/jeremylongshore/bobs-brain
python3 src/bob_firestore.py

# Cloud Run Deployment
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --project bobs-house-ai \
  --port 3000
```

## REQUIRED ENVIRONMENT VARIABLES
```bash
SLACK_BOT_TOKEN=xoxb-...        # From api.slack.com
SLACK_SIGNING_SECRET=...        # From api.slack.com  
SLACK_APP_TOKEN=xapp-...        # For Socket Mode (optional)
GCP_PROJECT=bobs-house-ai       # Google Cloud project
PORT=3000                        # Server port
```

## CURRENT ISSUES
1. **No Slack Tokens** - Can't start without them
2. **Deprecated SDK** - vertexai.generative_models dies June 2026
3. ~~**No Cloud Persistence**~~ - ✅ FIXED! Now using Firestore
4. **No Authentication** - Anyone in Slack can use Bob

## NEXT STEPS
1. ✅ Get Slack tokens from api.slack.com
2. ✅ Test locally with bob_firestore.py  
3. ⬜ Migrate to Google Gen AI SDK
4. ✅ ~~Add Cloud Storage for ChromaDB~~ - DONE! Using Firestore
5. ⬜ Deploy to Cloud Run

## TESTING
```bash
# Check if Bob responds
curl http://localhost:3000/health

# Test in Slack
@Bob what do you know about diagnostics?

# Direct message Bob
"Hey Bob, how are you?"
```

**STATUS:** Waiting for Slack tokens to activate

## 🎉 MIGRATION COMPLETED (2025-01-10)
- **Migrated:** 5 knowledge documents from ChromaDB to Firestore
- **Database:** projects/diagnostic-pro-mvp/databases/bob-brain
- **Collection:** shared_knowledge (cloud-persistent)
- **MVP3 Data:** Protected and intact (diagnostic_submissions, users, sessions, payments)
- **Fallback:** ChromaDB still available if Firestore unavailable
- **Next:** Use `bob_firestore.py` for all new deployments