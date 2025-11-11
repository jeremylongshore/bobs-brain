# Slack Webhook for Bob's Brain

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Platform](https://img.shields.io/badge/platform-GCP%20Cloud%20Functions-4285F4)
![Runtime](https://img.shields.io/badge/runtime-python3.12-3776AB)

Cloud Function that receives Slack events and forwards to Vertex AI Agent Engine.

## Overview

This Cloud Function serves as the integration point between Slack and Bob's Vertex AI Agent Engine. It:

- Receives Slack events (messages, mentions, DMs)
- Forwards queries to Vertex AI Agent Engine (IAM1)
- Returns AI-generated responses to Slack
- Maintains conversation context per user/channel
- Handles event deduplication to prevent duplicate responses

## Architecture

```
Slack Events → Cloud Function → Secret Manager (tokens)
                     ↓
            Vertex AI Agent Engine
                     ↓
            Gemini 2.5 Flash (IAM1)
                     ↓
            Response → Slack
```

## Deployment Status

**Environment:** Production
**Region:** us-central1
**Project:** bobs-brain
**Runtime:** Python 3.12
**URL:** https://slack-webhook-eow2wytafa-uc.a.run.app

## Features

### Event Handling
- **URL Verification:** Slack app setup handshake
- **Messages:** Channel messages and DMs
- **Mentions:** @bob mentions in channels
- **Deduplication:** Event cache prevents duplicate processing

### Performance
- **Immediate Response:** HTTP 200 within milliseconds
- **Background Processing:** AI processing in separate thread
- **Session Management:** Maintains context per user/channel

### Security
- **WIF Authentication:** No service account keys
- **Secret Manager:** Secure token storage
- **Bot Loop Prevention:** Filters bot messages
- **No Hardcoded Secrets:** All credentials externalized

### Observability
- **Cloud Logging:** Structured logs with execution IDs
- **Cloud Trace:** Distributed tracing enabled
- **Labels:** Deployment metadata and versioning

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PROJECT_ID` | GCP project ID | `bobs-brain` |
| `VERSION` | Deployment version | `0.1.0` |
| `LOG_EXECUTION_ID` | Enable execution ID logging | `true` |

### Secrets (Secret Manager)

| Secret Name | Description |
|-------------|-------------|
| `slack-bot-token` | Slack Bot User OAuth Token (xoxb-...) |

### Agent Engine Configuration

Hardcoded in `main.py`:
```python
AGENT_ENGINE_ID = "projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448"
```

## Deployment

### Prerequisites

1. **WIF Setup:** Workload Identity Federation configured
2. **GitHub Secrets:**
   - `WIF_POOL_ID`
   - `WIF_PROVIDER_ID`
   - `GCP_SERVICE_ACCOUNT`
   - `GCP_PROJECT_NUMBER`
   - `PROJECT_ID`

### Automatic Deployment (GitHub Actions)

**Triggers:**
- Push to `main` with changes to `slack-webhook/**`
- Manual workflow dispatch
- Version tags (`v*.*.*`)

**Workflow:** `.github/workflows/deploy-slack-webhook.yml`

### Manual Deployment

```bash
gcloud functions deploy slack-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --source=./slack-webhook \
  --entry-point=slack_events \
  --trigger-http \
  --allow-unauthenticated \
  --project=bobs-brain \
  --max-instances=10 \
  --min-instances=0 \
  --memory=512Mi \
  --timeout=60s \
  --set-env-vars="PROJECT_ID=bobs-brain,VERSION=0.1.0,LOG_EXECUTION_ID=true"
```

## Slack App Configuration

### Event Subscriptions

**Request URL:**
```
https://slack-webhook-eow2wytafa-uc.a.run.app
```

**Bot Events:**
- `message.channels` - Messages in public channels
- `message.im` - Direct messages
- `app_mention` - @bob mentions

### OAuth Scopes

**Bot Token Scopes:**
- `chat:write` - Send messages
- `chat:write.public` - Send to public channels
- `channels:history` - Read messages
- `channels:read` - View channels
- `app_mentions:read` - Know when mentioned
- `users:read` - View user info

## Testing

### URL Verification Test

```bash
curl -X POST https://slack-webhook-eow2wytafa-uc.a.run.app \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'

# Expected: {"challenge":"test123"}
```

### Slack Integration Test

1. Mention @Bob in any Slack channel
2. Send Bob a direct message
3. Verify response within 5-7 seconds

## Monitoring

### Cloud Logs

```bash
gcloud logging read \
  "resource.type=cloud_function AND resource.labels.function_name=slack-webhook" \
  --limit=50 \
  --project=bobs-brain
```

### Cloud Trace

View traces: https://console.cloud.google.com/traces/list?project=bobs-brain

### Metrics

View in Console:
- Invocations/minute
- Latency (P50, P95, P99)
- Error rate
- Memory usage

## Troubleshooting

### No Response in Slack

**Check:**
1. Cloud Function logs for errors
2. Secret Manager token is valid
3. Agent Engine is running
4. Slack app event subscriptions enabled

```bash
# View recent errors
gcloud functions logs read slack-webhook \
  --region=us-central1 \
  --project=bobs-brain \
  --limit=20
```

### Duplicate Responses

**Fixed:** HTTP 200 immediate acknowledgment implemented (Oct 2025)

If still occurring:
1. Check event cache is working
2. Verify Slack retry settings
3. Review duplicate event IDs in logs

### Slow Responses

**Normal:** 5-7 seconds end-to-end (Vertex AI processing)

If >10 seconds:
1. Check Agent Engine latency
2. Review Cloud Function cold start metrics
3. Increase memory allocation (currently 512Mi)

## Development

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID=bobs-brain

# Run with functions-framework
functions-framework --target=slack_events --debug
```

### Code Structure

```
slack-webhook/
├── main.py              # Cloud Function entry point
├── requirements.txt     # Python dependencies
├── VERSION             # Semantic version
├── CHANGELOG.md        # Release notes
└── README.md           # This file
```

### Version Management

**Semantic Versioning:** `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

**Auto-bump based on commit messages:**
- `BREAKING CHANGE:` or `major:` → MAJOR
- `feat:` or `feature:` → MINOR
- Everything else → PATCH

## Cost Estimation

**Per 1000 invocations:**
- Cloud Functions: $0.01 - $0.05
- Secret Manager: $0.00 (negligible)
- Vertex AI Agent: $0.10 - $0.30

**Total:** ~$0.11 - $0.35 per 1000 messages

## Security Best Practices

- No static secrets in code
- All credentials in Secret Manager
- WIF for GitHub Actions authentication
- Bot loop prevention
- Event deduplication
- Immediate HTTP acknowledgment

## Support

**Issues:** https://github.com/jeremylongshore/bobs-brain/issues
**Slack App:** https://api.slack.com/apps/A099YKLCM1N
**GCP Console:** https://console.cloud.google.com/functions/details/us-central1/slack-webhook?project=bobs-brain

---

**Last Updated:** 2025-11-10
**Maintained by:** @jeremylongshore
**License:** Proprietary
