# CLAUDE.md - Bob's Brain Documentation

## 🤖 BOB'S BRAIN STATUS
**Service:** bobs-brain
**Project:** bobs-house-ai  
**Directory:** /home/jeremylongshore/bobs-brain/
**GitHub:** https://github.com/jeremylongshore/bobs-brain
**Updated:** 2025-01-10T05:42:00Z

## CRITICAL STATUS ⚠️
- **Slack Tokens:** MISSING - Need from api.slack.com
- **Vertex AI:** Working but DEPRECATED (dies June 2026)
- **ChromaDB:** Working locally at /home/jeremylongshore/bobs-brain/chroma_data

## DIRECTORY STRUCTURE
```
/home/jeremylongshore/bobs-brain/
├── src/
│   ├── bob_ultimate.py        # 🚀 THE FINAL VERSION - USE THIS!
│   ├── bob_legacy_v2.py       # Backup of best recovered version
│   ├── knowledge_loader.py    # Knowledge base loader
│   ├── bob_test_harness.py    # Testing framework
│   └── thebrain_integration.py # Firestore integration
├── chroma_data/               # Vector database storage
├── logs/                      # Bob's activity logs
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Cloud Run deployment
├── .env                      # Environment variables (needs tokens)
└── CLAUDE.md                 # This file
```

## QUICK START
```bash
cd /home/jeremylongshore/bobs-brain
export SLACK_BOT_TOKEN=xoxb-YOUR-TOKEN-HERE
export SLACK_APP_TOKEN=xapp-YOUR-APP-TOKEN-HERE
export SLACK_SIGNING_SECRET=YOUR-SECRET-HERE
python3 src/bob_ultimate.py
```

## BOB ULTIMATE - THE FINAL VERSION (478 lines)

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
- **ChromaDB vector search** - semantic knowledge retrieval
- **Business context awareness** - DiagnosticPro focused

### 📊 **WHAT MAKES IT ULTIMATE:**
1. **Best of recovered-latest**: All the smart features (duplicate prevention, memory, Jeremy detection)
2. **Best of local versions**: Working AI integration with Vertex AI
3. **Best of production**: Health checks, error handling, logging
4. **Unified architecture**: One clean class that does everything
5. **Proper paths**: Uses /home/jeremylongshore/bobs-brain/ correctly
6. **Future ready**: Easy to migrate to Google Gen AI SDK when needed

## WHAT BOB DOES
1. **Listens to Slack** - @mentions and DMs
2. **Searches Knowledge** - ChromaDB vector search
3. **Generates Responses** - Vertex AI Gemini
4. **Learns** - Stores documents in ChromaDB

## DEPLOYMENT
```bash
# Local Testing
cd /home/jeremylongshore/bobs-brain
python3 src/bob_solid.py

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
3. **No Cloud Persistence** - ChromaDB resets on container restart
4. **No Authentication** - Anyone in Slack can use Bob

## NEXT STEPS
1. ✅ Get Slack tokens from api.slack.com
2. ✅ Test locally with bob_solid.py
3. ⬜ Migrate to Google Gen AI SDK
4. ⬜ Add Cloud Storage for ChromaDB
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