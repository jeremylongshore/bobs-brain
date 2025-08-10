# CLAUDE.md - Bob's Brain Documentation

## 🤖 BOB'S BRAIN STATUS
**Service:** bobs-brain
**Project:** bobs-house-ai  
**Directory:** /home/jeremylongshore/bobs-brain/
**GitHub:** https://github.com/jeremylongshore/bobs-brain
**Updated:** 2025-01-10T04:00:00Z

## CRITICAL STATUS ⚠️
- **Slack Tokens:** MISSING - Need from api.slack.com
- **Vertex AI:** Working but DEPRECATED (dies June 2026)
- **ChromaDB:** Working locally at /home/jeremylongshore/bobs-brain/chroma_data

## DIRECTORY STRUCTURE
```
/home/jeremylongshore/bobs-brain/
├── src/
│   ├── bob_solid.py           # MAIN - Simple 100-line version
│   ├── bob_unified_v2.py      # Original complex version
│   └── bob_production.py      # Production-ready with error handling
├── chroma_data/               # Vector database storage
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Cloud Run deployment
├── .env                      # Environment variables (needs tokens)
└── CLAUDE.md                 # This file
```

## QUICK START
```bash
cd /home/jeremylongshore/bobs-brain
export SLACK_BOT_TOKEN=xoxb-YOUR-TOKEN-HERE
export SLACK_SIGNING_SECRET=YOUR-SECRET-HERE
python3 src/bob_solid.py
```

## VERSIONS COMPARISON

### bob_solid.py (RECOMMENDED - 118 lines)
✅ **PROS:**
- Simple and working
- Just the essentials
- Easy to debug
- Minimal dependencies

❌ **CONS:**
- No error recovery
- No conversation memory
- Basic responses only

### bob_unified_v2.py (ORIGINAL - 383 lines)
✅ **PROS:**
- Full conversation history
- Knowledge loader system
- Slash commands (/bob-learn)
- Document ingestion

❌ **CONS:**
- Uses DEPRECATED Vertex AI SDK
- Complex error handling
- Hardcoded paths
- Will break June 2026

### bob_production.py (NEW - 400+ lines)
✅ **PROS:**
- Uses new Google Gen AI SDK
- Proper error handling
- Health checks for Cloud Run
- Thread-safe operations
- Memory leak prevention

❌ **CONS:**
- More complex
- Needs Google API key
- Not tested yet

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