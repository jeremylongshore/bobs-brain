# Bob's Slack Integration - ADK Architecture

**Status:** Production Implementation
**Version:** 1.0.0
**Date:** 2025-11-10

This is the **CORRECT** implementation of Bob's Slack integration using Vertex AI Agent Engine + ADK.

## Architecture

```
Slack Events → Cloud Run (FastAPI) → ADK Runner → Vertex AI Agent Engine
                    ↓
              Slack Bolt Handler
                    ↓
         VertexAiSessionService (Working Memory)
         VertexAiMemoryBankService (Long-Term Memory)
```

## Key Components

1. **FastAPI** - Web server for handling Slack webhooks
2. **Slack Bolt** - Slack event handling with signature verification
3. **ADK Runner** - Orchestrates agent execution with memory services
4. **VertexAiSessionService** - Manages working memory (session history within threads)
5. **VertexAiMemoryBankService** - Manages long-term memory (persistent facts across sessions)
6. **PreloadMemoryTool** - Automatically retrieves relevant memories at start of agent turn
7. **after_agent_callback** - Automatically saves sessions to Memory Bank for fact extraction

## Why This Architecture?

This implementation follows the correct Vertex AI Agent Engine architecture:

- ✅ Agent Engine handles ALL state management internally
- ✅ No external deduplication (session IDs provide natural deduplication)
- ✅ Dual-memory architecture (working + long-term)
- ✅ Automatic memory persistence via callbacks
- ✅ Proper ADK integration patterns

**Previous implementations incorrectly:**
- ❌ Added Firestore as external deduplication layer
- ❌ Bypassed Agent Engine's built-in memory management
- ❌ Used direct REST API calls instead of ADK abstraction

See `CRITICAL-ARCHITECTURE-ERROR.md` for analysis of previous errors.

## Prerequisites

1. **Vertex AI Agent Engine deployed**
   ```bash
   # Verify Agent Engine
   python3 ../verify_agent_engine.py
   ```

2. **Slack secrets in Google Secret Manager**
   ```bash
   # slack-bot-token (xoxb-...)
   # slack-signing-secret (from Slack App Basic Information)
   ```

3. **GitHub Actions configured** (for deployment)
   - Workload Identity Federation set up
   - Service account: `github-actions@bobs-brain.iam.gserviceaccount.com`

## Deployment

### Option 1: GitHub Actions (Recommended)

```bash
# Push changes to trigger deployment
git checkout -b feat/correct-adk-architecture
git add slack-adk-integration/ .github/workflows/deploy-slack-adk.yml
git commit -m "feat: implement correct ADK architecture"
git push origin feat/correct-adk-architecture
```

GitHub Actions will automatically:
1. Verify Agent Engine is accessible
2. Build Docker image
3. Push to Artifact Registry
4. Deploy to Cloud Run
5. Test health endpoint
6. Update deployment metadata

### Option 2: Manual Deployment

```bash
# Build and push Docker image
gcloud builds submit --tag us-central1-docker.pkg.dev/bobs-brain/bob-slack-adk/bob-slack-adk

# Deploy to Cloud Run
gcloud run deploy bob-slack-adk \
  --image us-central1-docker.pkg.dev/bobs-brain/bob-slack-adk/bob-slack-adk:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 60 \
  --max-instances 10 \
  --set-env-vars PROJECT_ID=bobs-brain \
  --set-env-vars LOCATION=us-central1 \
  --set-env-vars AGENT_ENGINE_ID=5828234061910376448 \
  --set-env-vars AGENT_ENGINE_NAME=projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448 \
  --set-env-vars APP_NAME=bob-battalion-commander \
  --set-secrets SLACK_BOT_TOKEN=slack-bot-token:latest \
  --set-secrets SLACK_SIGNING_SECRET=slack-signing-secret:latest \
  --project bobs-brain
```

## Configure Slack App

1. **Get Cloud Run URL**
   ```bash
   gcloud run services describe bob-slack-adk \
     --region us-central1 \
     --format='value(status.url)'
   ```

2. **Update Slack App Request URL**
   - Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
   - Enable Events: ON
   - Request URL: `https://YOUR-CLOUD-RUN-URL/slack/events`
   - Slack will send a verification challenge (handled automatically)

3. **Verify Bot Events Subscriptions**
   - `message.channels` - Messages in public channels
   - `message.im` - Direct messages
   - `app_mention` - When @bob is mentioned

4. **Save Changes** in Slack App configuration

## Testing

### Health Check
```bash
SERVICE_URL=$(gcloud run services describe bob-slack-adk --region=us-central1 --format='value(status.url)')
curl -s "$SERVICE_URL/_health" | jq
```

### Test in Slack

**Test 1: Basic Response**
```
@Bob What is 2+2?
```
Expected: Mathematical answer demonstrating working memory

**Test 2: Memory Persistence**
```
@Bob Remember that my favorite color is blue
```
Expected: Acknowledgment, fact will be saved to Memory Bank

**Test 3: Memory Retrieval (in NEW thread)**
```
@Bob What's my favorite color?
```
Expected: "Your favorite color is blue" (demonstrates Memory Bank retrieval)

### View Logs
```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=bob-slack-adk" \
  --project=bobs-brain \
  --limit=50 \
  --format=json
```

## Monitoring

### Key Metrics
- Request count: Number of Slack events processed
- Response time: Time from @mention to response
- Memory operations: Sessions saved to Memory Bank
- Error rate: Failed requests

### Endpoints
- `GET /_health` - Health check with component status
- `POST /slack/events` - Slack webhook endpoint

## Architecture Validation

Verify correct implementation:

- [ ] ✅ No Firestore dependencies in code
- [ ] ✅ ADK Runner initialized with both memory services
- [ ] ✅ PreloadMemoryTool included in agent tools
- [ ] ✅ after_agent_callback saves to Memory Bank
- [ ] ✅ No custom deduplication logic
- [ ] ✅ Session IDs from Slack thread_ts
- [ ] ✅ Agent Engine handles all state management

## Troubleshooting

### "Webhook verification failed"
- Check SLACK_SIGNING_SECRET matches Slack App
- Ensure Cloud Run allows unauthenticated requests

### "No response from Bob"
- Check Cloud Run logs for errors
- Verify Agent Engine is accessible: `python3 ../verify_agent_engine.py`
- Ensure Slack Bot Token has correct scopes

### "Memory not persisting"
- Check VertexAiMemoryBankService initialization
- Verify after_agent_callback is executing (check logs)
- Confirm Agent Engine ID is correct

### "Duplicate responses"
- Session IDs should use `thread_ts` (already implemented)
- ADK Runner handles deduplication internally

## Files

```
slack-adk-integration/
├── app/
│   ├── __init__.py           # Package init
│   ├── agent.py              # ADK agent with PreloadMemoryTool
│   ├── main.py               # FastAPI + Slack Bolt + ADK Runner
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
├── .env.example              # Configuration template
└── README.md                 # This file
```

## Dependencies

- `google-adk>=1.18.0` - Agent Development Kit
- `google-cloud-aiplatform>=1.112.0` - Vertex AI integration
- `fastapi==0.104.1` - Web server
- `uvicorn[standard]==0.24.0` - ASGI server
- `slack-bolt==1.18.0` - Slack SDK
- `python-dotenv==1.0.0` - Environment configuration

## Version History

### v1.0.0 (2025-11-10) - Initial Correct Implementation

**BREAKING CHANGE:** Complete rewrite following correct ADK pattern

- FastAPI + Slack Bolt + ADK Runner
- VertexAiSessionService for working memory
- VertexAiMemoryBankService for long-term memory
- PreloadMemoryTool + after_agent_callback
- GitHub Actions CI/CD workflow
- Deprecates slack-webhook Cloud Function

See `ARCHITECTURE-CORRECTION-PLAN.md` for full implementation details.
See `CRITICAL-ARCHITECTURE-ERROR.md` for error analysis.

## References

- **Architecture Plan**: `../ARCHITECTURE-CORRECTION-PLAN.md`
- **Error Analysis**: `../CRITICAL-ARCHITECTURE-ERROR.md`
- **Session Status**: `../SESSION-STATUS.md`
- **GitHub Actions**: `../.github/workflows/deploy-slack-adk.yml`
- **Agent Verification**: `../verify_agent_engine.py`

## Support

- **Project**: bobs-brain (GCP Project ID: 205354194989)
- **Agent Engine**: projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448
- **Slack App**: https://api.slack.com/apps/A099YKLCM1N

---

**Status:** Production Ready
**Deployment:** via GitHub Actions
**Last Updated:** 2025-11-10
