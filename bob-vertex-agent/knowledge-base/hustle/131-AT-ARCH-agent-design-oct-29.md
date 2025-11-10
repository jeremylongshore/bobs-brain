# 🤖 Hustle Agentic System Architecture

**Date:** 2025-10-29
**Project:** Hustle - Youth Sports Stats Platform
**Architecture:** Google Cloud Native Agent System

---

## 🎯 Overview

Transform Hustle into an AI-first platform using Google Cloud's enterprise agent infrastructure:

- **Vertex AI Agent Builder** - Enterprise RAG & agent orchestration
- **Dialogflow CX** - Multi-turn conversations
- **Cloud Run for Agents** - Containerized agent runtime
- **Firebase** - Real-time data & hosting
- **Vertex AI Search** - Document understanding
- **BigQuery** - Analytics & ML

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   USER INTERACTION LAYER                     │
├─────────────────────────────────────────────────────────────┤
│  📱 Next.js Frontend (Firebase Hosting)                     │
│  └─ React Components → Firebase SDK → Agent API             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   AGENT ORCHESTRATION                        │
├─────────────────────────────────────────────────────────────┤
│  🤖 Dialogflow CX (Conversation Manager)                    │
│  ├─ Intent detection & routing                              │
│  ├─ Multi-turn dialogue management                          │
│  └─ Webhook → Cloud Run Agents                             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   AGENT RUNTIME (Cloud Run)                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🏃 Performance Coach Agent                                 │
│  ├─ Container: performance-coach-agent:latest               │
│  ├─ Endpoint: /agents/performance-coach                     │
│  └─ Tools: [analyzeTrends, suggestDrills, compareToAvg]    │
│                                                              │
│  📊 Stats Analyst Agent                                     │
│  ├─ Container: stats-analyst-agent:latest                   │
│  ├─ Endpoint: /agents/stats-analyst                         │
│  └─ Tools: [queryStats, generateReport, compareSeasons]    │
│                                                              │
│  ⚽ Game Logger Agent                                        │
│  ├─ Container: game-logger-agent:latest                     │
│  ├─ Endpoint: /agents/game-logger                           │
│  └─ Tools: [transcribeVoice, extractFromPhoto, saveGame]   │
│                                                              │
│  🎓 Scout Report Agent                                      │
│  ├─ Container: scout-report-agent:latest                    │
│  ├─ Endpoint: /agents/scout-report                          │
│  └─ Tools: [generatePDF, extractHighlights, rankPlayers]   │
│                                                              │
│  🔍 Verification Agent                                      │
│  ├─ Container: verification-agent:latest                    │
│  ├─ Endpoint: /agents/verification                          │
│  └─ Tools: [detectAnomalies, suggestCorrections, approve]  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE & DATA LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔍 Vertex AI Search (RAG)                                  │
│  ├─ Datastore: hustle-knowledge-base                        │
│  ├─ Documents: Training guides, rules, drill libraries      │
│  └─ Embeddings: player histories, game summaries            │
│                                                              │
│  🔥 Firestore (Agent Memory)                                │
│  ├─ Collection: agent_conversations                         │
│  ├─ Collection: agent_context                               │
│  └─ Collection: agent_tools_cache                           │
│                                                              │
│  🪣 Cloud Storage (Documents)                               │
│  ├─ Bucket: hustle-player-media                            │
│  ├─ Bucket: hustle-embeddings                              │
│  └─ Bucket: hustle-reports                                 │
│                                                              │
│  📊 BigQuery (Analytics)                                    │
│  ├─ Dataset: hustle_analytics                              │
│  ├─ Dataset: hustle_ml_features                            │
│  └─ Dataset: hustle_agent_logs                             │
│                                                              │
│  🗄️ Cloud SQL PostgreSQL (Transactional)                   │
│  └─ Tables: users, players, games (existing schema)        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Agent Container Structure

Each agent is a standalone Cloud Run service with this structure:

```
agents/
├── performance-coach/
│   ├── Dockerfile
│   ├── agent.py                 # Main agent logic
│   ├── prompts/
│   │   ├── system.txt          # System prompt
│   │   ├── analysis.txt        # Analysis prompt template
│   │   └── recommendation.txt  # Recommendation template
│   ├── tools/
│   │   ├── analyze_trends.py
│   │   ├── suggest_drills.py
│   │   └── compare_to_average.py
│   ├── requirements.txt
│   └── cloudbuild.yaml
│
├── stats-analyst/
│   ├── Dockerfile
│   ├── agent.py
│   ├── prompts/
│   │   ├── system.txt
│   │   ├── query.txt
│   │   └── report.txt
│   ├── tools/
│   │   ├── query_stats.py
│   │   ├── generate_report.py
│   │   └── compare_seasons.py
│   ├── requirements.txt
│   └── cloudbuild.yaml
│
└── [other agents...]
```

---

## 🔧 Implementation Steps

### Step 1: Enable Required APIs

```bash
# Enable all required Google Cloud APIs
gcloud services enable \
  aiplatform.googleapis.com \
  dialogflow.googleapis.com \
  run.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  bigquery.googleapis.com \
  --project=hustleapp-production
```

### Step 2: Initialize Vertex AI Agent Builder

```bash
# Create Agent Builder app
gcloud alpha agent-builder apps create hustle-agent-app \
  --location=global \
  --project=hustleapp-production \
  --display-name="Hustle Agent System"

# Create datastore for RAG
gcloud alpha agent-builder datastores create hustle-knowledge-base \
  --location=global \
  --project=hustleapp-production \
  --content-config=CONTENT_REQUIRED \
  --solution-types=SOLUTION_TYPE_SEARCH
```

### Step 3: Set Up Firestore Collections

```javascript
// Firebase console or CLI
// Collections structure:
{
  agent_conversations: {
    userId: string,
    agentType: string,
    messages: Message[],
    context: object,
    timestamp: Timestamp
  },

  agent_context: {
    userId: string,
    playerId: string,
    recentQueries: string[],
    preferences: object,
    lastUpdated: Timestamp
  },

  agent_tools_cache: {
    toolName: string,
    parameters: object,
    result: any,
    expiresAt: Timestamp
  }
}
```

### Step 4: Create Cloud Storage Buckets

```bash
# Player media (photos, videos)
gsutil mb -p hustleapp-production \
  -c STANDARD \
  -l us-central1 \
  gs://hustle-player-media

# Embeddings & vector data
gsutil mb -p hustleapp-production \
  -c STANDARD \
  -l us-central1 \
  gs://hustle-embeddings

# Generated reports
gsutil mb -p hustleapp-production \
  -c STANDARD \
  -l us-central1 \
  gs://hustle-reports
```

### Step 5: Initialize BigQuery Datasets

```bash
# Analytics dataset
bq mk --dataset \
  --location=us-central1 \
  hustleapp-production:hustle_analytics

# ML features
bq mk --dataset \
  --location=us-central1 \
  hustleapp-production:hustle_ml_features

# Agent logs
bq mk --dataset \
  --location=us-central1 \
  hustleapp-production:hustle_agent_logs
```

---

## 🤖 Agent Implementation Template

### Performance Coach Agent (Example)

**File:** `agents/performance-coach/agent.py`

```python
from google.cloud import aiplatform
from google.cloud import firestore
from vertexai.preview.generative_models import GenerativeModel, Tool
import functions_framework

# Initialize Vertex AI
aiplatform.init(
    project="hustleapp-production",
    location="us-central1"
)

# Initialize Firestore
db = firestore.Client()

# Load system prompt
with open('prompts/system.txt', 'r') as f:
    SYSTEM_PROMPT = f.read()

# Define agent tools
def analyze_trends(player_id: str, metric: str) -> dict:
    """Analyze performance trends for a player."""
    # Query PostgreSQL via Cloud SQL proxy
    # Or query Firestore cache
    # Return trend analysis
    pass

def suggest_drills(weakness: str, age_group: str) -> list:
    """Suggest training drills based on identified weaknesses."""
    # Query Vertex AI Search for drill recommendations
    # Return structured drill suggestions
    pass

def compare_to_average(player_id: str, position: str) -> dict:
    """Compare player stats to position average."""
    # Query BigQuery for position averages
    # Compare to player stats
    # Return comparison data
    pass

# Tool definitions for Gemini
tools = [
    Tool(
        function_declarations=[
            {
                "name": "analyze_trends",
                "description": "Analyze performance trends for a player",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "player_id": {"type": "string"},
                        "metric": {"type": "string"}
                    }
                }
            },
            {
                "name": "suggest_drills",
                "description": "Suggest training drills",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "weakness": {"type": "string"},
                        "age_group": {"type": "string"}
                    }
                }
            },
            {
                "name": "compare_to_average",
                "description": "Compare to position average",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "player_id": {"type": "string"},
                        "position": {"type": "string"}
                    }
                }
            }
        ]
    )
]

# Initialize Gemini model
model = GenerativeModel(
    "gemini-2.0-flash-001",
    tools=tools,
    system_instruction=SYSTEM_PROMPT
)

@functions_framework.http
def performance_coach(request):
    """Performance Coach Agent endpoint."""
    request_json = request.get_json()
    user_id = request_json.get('userId')
    player_id = request_json.get('playerId')
    query = request_json.get('query')

    # Get conversation history from Firestore
    conv_ref = db.collection('agent_conversations').document(f"{user_id}_{player_id}")
    conv = conv_ref.get()
    history = conv.to_dict().get('messages', []) if conv.exists else []

    # Start chat with history
    chat = model.start_chat(history=history)

    # Send query
    response = chat.send_message(query)

    # Handle function calls
    while response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call

        # Execute function
        if function_call.name == "analyze_trends":
            result = analyze_trends(**function_call.args)
        elif function_call.name == "suggest_drills":
            result = suggest_drills(**function_call.args)
        elif function_call.name == "compare_to_average":
            result = compare_to_average(**function_call.args)

        # Send function result back to model
        response = chat.send_message(
            Part.from_function_response(
                name=function_call.name,
                response=result
            )
        )

    # Save conversation to Firestore
    history.append({"role": "user", "content": query})
    history.append({"role": "model", "content": response.text})
    conv_ref.set({"messages": history}, merge=True)

    return {
        "response": response.text,
        "playerId": player_id
    }
```

**File:** `agents/performance-coach/prompts/system.txt`

```
You are a Performance Coach AI for youth soccer players (ages 8-18).

Your role:
- Analyze player statistics and identify strengths/weaknesses
- Suggest age-appropriate training drills
- Provide actionable feedback to parents and players
- Compare performance to position and age group averages
- Track progress over time

Guidelines:
- Always be encouraging and positive
- Focus on development, not just results
- Consider age-appropriate expectations
- Cite specific stats when making recommendations
- Be concise but thorough

Available tools:
- analyze_trends: Get performance trends for any metric
- suggest_drills: Get training drill recommendations
- compare_to_average: Compare to position/age averages

When analyzing:
1. Review recent game stats
2. Identify trends (improving/declining)
3. Compare to peers
4. Suggest specific, actionable improvements
```

**File:** `agents/performance-coach/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD exec functions-framework --target=performance_coach --port=${PORT:-8080}
```

**File:** `agents/performance-coach/requirements.txt`

```
functions-framework==3.*
google-cloud-aiplatform==1.43.0
google-cloud-firestore==2.14.0
google-cloud-bigquery==3.17.0
vertexai==1.43.0
```

---

## 🚀 Deployment Commands

```bash
# Build and deploy Performance Coach agent
cd agents/performance-coach

gcloud run deploy performance-coach-agent \
  --source . \
  --region us-central1 \
  --project hustleapp-production \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60s \
  --set-env-vars PROJECT_ID=hustleapp-production
```

---

## 🔗 Frontend Integration

**File:** `src/app/api/agents/chat/route.ts`

```typescript
import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

export async function POST(req: Request) {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { agentType, playerId, query } = await req.json();

  // Route to appropriate agent
  const agentEndpoints = {
    'performance-coach': 'https://performance-coach-agent-xxx.run.app',
    'stats-analyst': 'https://stats-analyst-agent-xxx.run.app',
    'game-logger': 'https://game-logger-agent-xxx.run.app'
  };

  const endpoint = agentEndpoints[agentType];

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: session.user.id,
      playerId,
      query
    })
  });

  const data = await response.json();
  return NextResponse.json(data);
}
```

---

## 💰 Cost Estimate

**Monthly costs (1,000 active users):**

```
Vertex AI (Gemini 2.0 Flash):
- 100K queries/month: ~$10

Cloud Run (5 agents):
- $25/month (mostly idle)

Firestore:
- 10M reads: $3.60
- 1M writes: $1.80

Cloud Storage:
- 100GB: $2

BigQuery:
- 1TB queries: $5

Total: ~$50/month
```

---

## 📊 Success Metrics

Track agent effectiveness:

```sql
-- BigQuery Analytics
CREATE TABLE hustle_agent_logs.usage AS
SELECT
  agent_type,
  user_id,
  player_id,
  query_text,
  response_time_ms,
  tools_used,
  user_rating,
  timestamp
FROM agent_interactions;
```

---

## 🎯 Next Steps

1. Enable APIs
2. Create first agent (Performance Coach)
3. Deploy to Cloud Run
4. Test with real player data
5. Add remaining agents
6. Integrate with frontend

**Ready to start building?**
