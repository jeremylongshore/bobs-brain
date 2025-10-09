# Bob's Brain Deployment Architecture

**Date:** 2025-10-05
**Status:** ✅ Ready for deployment
**Decision:** Dedicated Google Cloud project

---

## Architecture Decision

**Recommendation: Create dedicated `bobs-house-ai` Google Cloud project**

### Why Dedicated Project?

✅ **Cost Visibility**
- See exactly what Bob costs per month
- Separate billing reports
- Easy budget tracking and alerts

✅ **Security Isolation**
- Bob's credentials isolated from other services
- Separate IAM policies and service accounts
- Blast radius containment if compromised

✅ **Resource Management**
- Independent quotas and limits
- No interference with DiagnosticPro or other projects
- Easier to scale Bob independently

✅ **Clean Organization**
- Professional separation of concerns
- Each major service gets its own project
- Follows Google Cloud best practices

✅ **Operational Simplicity**
- Clear ownership and responsibility
- Easy to grant/revoke access
- Simpler monitoring and alerting

### Cost Analysis

**Estimated Monthly Cost: $5-15**

| Component | Cost | Notes |
|-----------|------|-------|
| **Cloud Run** | $2-5/mo | Min instances = 0, pay per request |
| **Secret Manager** | $0.06/mo | 4 secrets × $0.06/month |
| **Cloud Logging** | $0-5/mo | First 50GB free |
| **Cloud Build** | $0 | First 120 builds/day free |
| **Gemini API** | $0.01/1M tokens | Very cheap! |

**Total estimated: $5-15/month** depending on Slack usage

### Alternative Considered: Shared Project

❌ **Using existing `hustle-dev-202510` project**
- Cost tracking mixed with other services
- Harder to isolate Bob's resources
- IAM policies shared
- Not recommended for production

---

## Deployment Architecture

### Infrastructure Overview

```
┌─────────────────────────────────────────────────────────┐
│  Google Cloud Project: bobs-house-ai                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────────┐      ┌────────────────────┐    │
│  │   Cloud Run        │      │  Secret Manager    │    │
│  │   (bobs-brain)     │◄─────┤  - slack-bot-token │    │
│  │                    │      │  - signing-secret  │    │
│  │  - Flask app       │      │  - google-api-key  │    │
│  │  - Gemini API      │      │  - bb-api-key      │    │
│  │  - SQLite + Chroma │      └────────────────────┘    │
│  │  - Min: 0 instances│                                │
│  │  - Max: 10         │      ┌────────────────────┐    │
│  │  - 1Gi RAM         │      │  Cloud Logging     │    │
│  └────────┬───────────┘      │  Cloud Monitoring  │    │
│           │                  └────────────────────┘    │
│           │                                            │
│           ▼                                            │
│  ┌────────────────────┐                               │
│  │  Public Endpoint   │                               │
│  │  /slack/events     │◄──── Slack Event Webhook     │
│  │  /health           │                               │
│  │  /api/query        │                               │
│  └────────────────────┘                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Runtime**: Cloud Run (managed container platform)
- **Container**: Python 3.11 + Flask + Gunicorn
- **AI**: Google Gemini 2.5 Flash (via Vertex AI)
- **Storage**: SQLite (ephemeral) + Chroma (in-memory)
- **Secrets**: Secret Manager (encrypted at rest)
- **Monitoring**: Cloud Logging + Cloud Monitoring
- **Deployment**: Cloud Build (from source)

### Scaling Configuration

```yaml
Service: bobs-brain
Memory: 1Gi
CPU: 1 vCPU
Min instances: 0    # Zero cost when idle
Max instances: 10   # Auto-scale under load
Timeout: 300s       # 5 minutes for long requests
Concurrency: 80     # Requests per instance
```

**Cost optimization:**
- Min instances = 0 → No cost when not used
- Scales to zero after idle period
- Auto-scales up when Slack messages arrive
- Cold start: ~3-5 seconds (acceptable for Slack)

---

## Deployment Process

### Step 1: Create Project

```bash
cd ~/projects/bobs-brain
./05-Scripts/deploy/create-bob-project.sh
```

**What this does:**
1. Creates `bobs-house-ai` Google Cloud project
2. Links billing account
3. Enables required APIs:
   - Cloud Run
   - Cloud Build
   - Secret Manager
   - Cloud Logging
   - Cloud Monitoring

**Time**: ~2 minutes

### Step 2: Store Secrets

**Prerequisites:**
1. Add Google API key to .env:
   ```bash
   echo 'GOOGLE_API_KEY=your-key-here' >> .env
   ```

2. Run secrets script:
   ```bash
   ./05-Scripts/deploy/store-secrets.sh
   ```

**What this stores:**
- `slack-bot-token` → From .env
- `slack-signing-secret` → From .env
- `google-api-key` → From .env (for Gemini API)
- `bb-api-key` → Auto-generated (for API auth)

**IMPORTANT**: Save the `BB_API_KEY` printed by the script!

**Time**: ~1 minute

### Step 3: Deploy to Cloud Run

```bash
./05-Scripts/deploy/deploy-to-cloudrun.sh
```

**What this does:**
1. Builds container from source (using Cloud Build)
2. Pushes to Container Registry
3. Deploys to Cloud Run with:
   - Environment variables for LLM provider
   - Secret bindings from Secret Manager
   - Auto-scaling configuration
   - Public access for Slack webhook

**Time**: ~5-10 minutes (first deployment)

### Step 4: Configure Slack

1. Get service URL from deploy output
2. Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
3. Set Request URL: `https://bobs-brain-abc123.run.app/slack/events`
4. Subscribe to events:
   - `message.channels`
   - `message.groups`
   - `message.im`
   - `app_mention`
5. Save Changes

**Time**: ~2 minutes

---

## Testing & Verification

### Health Check

```bash
SERVICE_URL=$(gcloud run services describe bobs-brain \
  --project bobs-house-ai \
  --region us-central1 \
  --format="value(status.url)")

curl $SERVICE_URL/health
```

**Expected response:**
```json
{
  "ok": true,
  "service": "bobs-brain",
  "version": "v5.0.0",
  "timestamp": "2025-10-05T...",
  "backends": {
    "llm": "google:gemini-2.0-flash",
    "state": "sqlite",
    "vector": "chroma",
    "graph": "none"
  }
}
```

### Slack Integration Test

1. Go to Slack workspace
2. Invite Bob to channel: `/invite @Bob`
3. Mention Bob: `@Bob hello!`
4. Bob should respond within 3-5 seconds

### API Test

```bash
BB_API_KEY="your-bb-api-key-from-step-2"

curl -X POST $SERVICE_URL/api/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{
    "query": "Hello Bob! Can you hear me?"
  }'
```

**Expected response:**
```json
{
  "ok": true,
  "answer": "Yes! I can hear you. How can I help?"
}
```

---

## Monitoring & Operations

### View Logs

```bash
# Real-time logs
gcloud run services logs tail bobs-brain \
  --project bobs-house-ai \
  --region us-central1

# Last 50 log entries
gcloud run services logs read bobs-brain \
  --project bobs-house-ai \
  --region us-central1 \
  --limit 50
```

### Cloud Console

**Service Overview:**
https://console.cloud.google.com/run/detail/us-central1/bobs-brain/metrics?project=bobs-house-ai

**Logs Explorer:**
https://console.cloud.google.com/logs/query?project=bobs-house-ai

**Cost Dashboard:**
https://console.cloud.google.com/billing?project=bobs-house-ai

### Metrics to Monitor

| Metric | Target | Alert |
|--------|--------|-------|
| **Request latency** | < 3s | > 10s |
| **Error rate** | < 1% | > 5% |
| **Cold start time** | < 5s | > 10s |
| **Instance count** | 0-10 | > 10 |
| **Monthly cost** | < $15 | > $50 |

### Update Deployment

```bash
# Make code changes, then redeploy
cd ~/projects/bobs-brain
./05-Scripts/deploy/deploy-to-cloudrun.sh

# Or use gcloud directly
gcloud run deploy bobs-brain \
  --source . \
  --project bobs-house-ai \
  --region us-central1
```

Cloud Run supports:
- ✅ Zero-downtime deployments
- ✅ Gradual traffic migration
- ✅ Automatic rollback on errors
- ✅ Revision history

---

## Security Best Practices

### ✅ Implemented

- **Secrets in Secret Manager**: No secrets in code or environment
- **IAM least privilege**: Service accounts with minimal permissions
- **Request signature verification**: Slack requests validated
- **Rate limiting**: Flask-Limiter on all endpoints
- **API key auth**: Protected endpoints require X-API-Key header
- **HTTPS only**: All traffic encrypted in transit
- **Container security**: Non-root user, minimal base image

### 🔄 Recommended Next Steps

1. **Enable Cloud Armor**: DDoS protection and WAF rules
2. **Set up alerting**: Email/Slack alerts for errors
3. **Rotate secrets**: Monthly rotation of Slack credentials
4. **Enable VPC**: Network isolation for enhanced security
5. **Add monitoring**: Custom metrics and dashboards

---

## Cost Optimization

### Current Configuration

**Min instances: 0** → Scales to zero when idle
- No cost during inactive periods
- Cold start: 3-5 seconds (acceptable for Slack)

**Memory: 1Gi** → Right-sized for Bob's needs
- SQLite + Chroma fit in memory
- Gemini API calls don't need much RAM

**CPU: 1 vCPU** → Single core sufficient
- I/O bound (API calls), not CPU bound
- Can scale horizontally if needed

### Cost Breakdown

**Scenario: Light usage (100 requests/day)**
- Cloud Run: ~$2/month
- Secret Manager: $0.24/month
- Gemini API: ~$0.10/month
- **Total: ~$2.50/month**

**Scenario: Moderate usage (1000 requests/day)**
- Cloud Run: ~$8/month
- Secret Manager: $0.24/month
- Gemini API: ~$1/month
- **Total: ~$10/month**

**Scenario: Heavy usage (10,000 requests/day)**
- Cloud Run: ~$30/month
- Secret Manager: $0.24/month
- Gemini API: ~$10/month
- **Total: ~$40/month**

### Free Tier Benefits

- **Cloud Run**: 2M requests/month free
- **Cloud Build**: 120 builds/day free
- **Cloud Logging**: 50GB/month free
- **Cloud Monitoring**: Free for Cloud Run metrics
- **Gemini API**: Pay-as-you-go, very cheap ($0.01/1M tokens)

---

## Troubleshooting

### Issue: Slack verification fails

**Symptom**: "url_verification" event returns error

**Solution**: Check SLACK_SIGNING_SECRET is correct
```bash
gcloud secrets versions access latest \
  --secret slack-signing-secret \
  --project bobs-house-ai
```

### Issue: Gemini API errors

**Symptom**: "GOOGLE_API_KEY not found" or API quota errors

**Solution**: Verify API key in Secret Manager
```bash
gcloud secrets versions access latest \
  --secret google-api-key \
  --project bobs-house-ai
```

### Issue: Cold starts too slow

**Symptom**: First request takes > 10 seconds

**Solution**: Set min instances to 1 (costs ~$8/month)
```bash
gcloud run services update bobs-brain \
  --min-instances 1 \
  --project bobs-house-ai \
  --region us-central1
```

### Issue: Out of memory errors

**Symptom**: Container crashes with OOM

**Solution**: Increase memory to 2Gi
```bash
gcloud run services update bobs-brain \
  --memory 2Gi \
  --project bobs-house-ai \
  --region us-central1
```

---

## Rollback Procedure

Cloud Run keeps revision history. To rollback:

```bash
# List revisions
gcloud run revisions list \
  --service bobs-brain \
  --project bobs-house-ai \
  --region us-central1

# Rollback to previous revision
gcloud run services update-traffic bobs-brain \
  --to-revisions=bobs-brain-00002-xyz=100 \
  --project bobs-house-ai \
  --region us-central1
```

---

## Production Checklist

Before going live:

- [ ] ✅ .env has all credentials (Slack, Google API key)
- [ ] ✅ Secrets stored in Secret Manager
- [ ] ✅ Service deployed and healthy
- [ ] ✅ Slack Event Subscriptions configured
- [ ] ✅ Test message sent in Slack
- [ ] ✅ Health endpoint returns 200 OK
- [ ] ✅ Logs show successful requests
- [ ] ✅ Cost alerts configured
- [ ] ✅ BB_API_KEY saved securely
- [ ] 🔄 Rotate Slack Client Secret (recommended)
- [ ] 🔄 Rotate Slack Signing Secret (recommended)
- [ ] 🔄 Set up monitoring dashboards
- [ ] 🔄 Configure alerting rules

---

## Next Steps

1. **Get Google API key**: https://aistudio.google.com/apikey
2. **Run deployment scripts**:
   ```bash
   cd ~/projects/bobs-brain
   ./05-Scripts/deploy/create-bob-project.sh
   # Add API key to .env
   ./05-Scripts/deploy/store-secrets.sh
   ./05-Scripts/deploy/deploy-to-cloudrun.sh
   ```
3. **Configure Slack**: Update Event Subscriptions URL
4. **Test Bob**: Send test message in Slack
5. **Monitor costs**: Check billing dashboard weekly

---

**Created:** 2025-10-05
**Status:** ✅ Architecture finalized, scripts ready
**Next:** Add Google API key to .env and run deployment
**Estimated cost:** $5-15/month
