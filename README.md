# 🤖 Bob's Brain - Ultimate Edition

## THE FINAL BOB - One Version To Rule Them All

After analyzing 7+ different versions across multiple branches, we've created **Bob Ultimate** - the definitive version combining the best features from ALL implementations.

## Quick Start

```bash
cd /home/jeremylongshore/bobs-brain
export SLACK_BOT_TOKEN=xoxb-your-token-here
export SLACK_APP_TOKEN=xapp-your-token-here  # Optional
python3 src/bob_ultimate.py
```

## What's In This Repository

### Core Files (Keep These!)
- `src/bob_ultimate.py` - **THE MAIN BOB** - Use this one!
- `src/knowledge_loader.py` - Loads DiagnosticPro knowledge
- `src/bob_test_harness.py` - Testing framework
- `src/thebrain_integration.py` - Firestore integration

### Legacy Files (For Reference)
- `src/bob_unified_v2.py` - Previous best version (no AI)
- `src/bob_unified.py` - Original business-focused version

## Bob Ultimate Features

### 🎯 Best of ALL Versions
- **Duplicate prevention** (from bob_unified_v2)
- **Thread safety** (from bob_production)
- **Simple directness** (from bob_solid)
- **AI + Knowledge hybrid** (new combination)
- **Smart memory management** (enhanced)
- **Health checks** for Cloud Run (from bob_production)
- **Professional communication** (from bob_unified_v2)
- **Jeremy recognition** (knows the owner!)

### 🤖 AI Capabilities
- **Primary**: Vertex AI with Gemini 2.0
- **Fallback**: Google GenAI SDK (future-proof)
- **Offline**: Knowledge-base only mode

### 💾 Data Storage
- **ChromaDB**: Vector database for knowledge
- **Location**: `/home/jeremylongshore/bobs-brain/chroma_data`
- **Persistence**: Survives restarts locally

## Environment Variables

```bash
# Required
SLACK_BOT_TOKEN=xoxb-...        # From api.slack.com

# Optional
SLACK_APP_TOKEN=xapp-...        # For Socket Mode
SLACK_SIGNING_SECRET=...        # For webhooks
GOOGLE_API_KEY=...              # For GenAI fallback
CHROMA_PERSIST_DIR=./chroma_data  # Database location
PORT=8080                       # Health check port
```

## Deployment

### Local Testing
```bash
python3 src/bob_ultimate.py
```

### Cloud Run
```bash
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --project bobs-house-ai \
  --port 8080
```

## Architecture

```
Bob Ultimate
├── Slack Integration
│   ├── Socket Mode (development)
│   └── Webhook Mode (production)
├── AI Engine
│   ├── Vertex AI (primary)
│   └── Google GenAI (fallback)
├── Knowledge Base
│   ├── ChromaDB vectors
│   └── DiagnosticPro context
└── Safety Features
    ├── Duplicate prevention
    ├── Thread safety
    ├── Memory management
    └── Error recovery
```

## Version History

- **v1.0 ULTIMATE** - The final unified version (YOU ARE HERE)
- Previous: bob_unified_v2 (advanced but no AI)
- Previous: bob_production (good safety, complex)
- Previous: bob_solid (simple but limited)
- Previous: 4+ other experimental versions

## Status

✅ **READY TO USE** - Just needs Slack tokens!

Get tokens from: https://api.slack.com/apps

---

**CTO Decision**: This is THE Bob. All other versions are deprecated.
