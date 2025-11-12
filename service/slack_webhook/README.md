# Slack Webhook - Slack Event Handler Proxy

**Version:** 0.6.0
**Status:** Phase 3 Implementation
**Compliance:** R3 (Cloud Run as gateway only)

---

## Purpose

The Slack Webhook is a **FastAPI service** that handles Slack events (mentions, DMs) and proxies them to the **Vertex AI Agent Engine** via REST API. It runs on **Cloud Run** and enables Bob's Brain to respond to Slack messages.

### R3 Compliance

This webhook enforces **Rule 3 (R3)**: Cloud Run as Gateway Only

- ✅ **DOES:** Receive Slack events via webhook
- ✅ **DOES:** Proxy queries to Agent Engine via HTTP/REST
- ✅ **DOES:** Post responses back to Slack
- ❌ **DOES NOT:** Import or run `google.adk.Runner` locally
- ❌ **DOES NOT:** Execute agent logic in Cloud Run
- ❌ **DOES NOT:** Embed agent runtime in webhook

**Why?** Agent Engine is the production runtime (R2). Cloud Run is only for protocol translation and routing.

---

## Architecture

```
┌─────────────────┐         ┌───────────────────┐         ┌──────────────────────┐
│  Slack          │  HTTPS  │  Slack Webhook    │  REST   │  Agent Engine        │
│  (User @Bob)    │────────>│  (Cloud Run)      │────────>│  (Vertex AI)         │
│                 │         │                   │         │                      │
│                 │<────────│  Event Handler    │<────────│  ADK Runner          │
└─────────────────┘         └───────────────────┘         └──────────────────────┘
```

**Flow:**
1. User mentions @Bob in Slack or sends DM
2. Slack sends event to webhook URL
3. Webhook verifies signature and extracts text
4. Webhook proxies query to Agent Engine REST API
5. Agent Engine processes with ADK Runner + dual memory
6. Webhook posts response back to Slack thread

---

## Slack Events Handled

### `app_mention`

Triggered when user mentions @Bob in a channel.

**Example:**
```
User: @Bob what's the weather today?
Bob: I don't have access to real-time weather data, but I can help with other questions!
```

### `message.im`

Triggered when user sends a direct message to Bob.

**Example:**
```
User (DM): Tell me about ADK
Bob (DM): ADK (Agent Development Kit) is Google's framework for building AI agents...
```

### `message.channels`

Triggered for messages in channels Bob is a member of (if configured).

---

## Endpoints

### `POST /slack/events`

**Slack event webhook endpoint**

Receives events from Slack Events API and processes them.

**Slack Configuration:**
- Event Subscriptions URL: `https://slack-webhook-xxx.run.app/slack/events`
- Subscribe to: `app_mention`, `message.im`, `message.channels`

**Security:**
- Verifies Slack signature (HMAC-SHA256)
- Prevents replay attacks (5-minute window)
- Ignores bot messages (prevent loops)
- Returns 200 immediately to prevent Slack retries

**Request Body (from Slack):**
```json
{
  "type": "event_callback",
  "event": {
    "type": "app_mention",
    "user": "U123456",
    "text": "<@U07NRCYJX8A> What is ADK?",
    "channel": "C123456",
    "ts": "1234567890.123456"
  }
}
```

**Response:**
```json
{
  "ok": true
}
```

### `GET /health`

**Health check**

**Response:**
```json
{
  "status": "healthy",
  "service": "slack-webhook",
  "version": "0.6.0",
  "agent_engine_url": "https://us-central1-aiplatform.googleapis.com/v1/projects/bobs-brain/locations/us-central1/reasoningEngines/xxx:query"
}
```

---

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | Yes | Slack bot OAuth token | `xoxb-123-456-abc` |
| `SLACK_SIGNING_SECRET` | Yes | Slack app signing secret | `abc123def456` |
| `PROJECT_ID` | Yes | GCP project ID | `bobs-brain` |
| `LOCATION` | Yes | GCP region | `us-central1` |
| `AGENT_ENGINE_ID` | Yes | Agent Engine instance ID | `12345678901234567890` |
| `AGENT_ENGINE_URL` | No | Override default URL | `https://...` |
| `PORT` | No | Service port (default 8080) | `8080` |

**Get Slack Credentials:**
1. Go to https://api.slack.com/apps/A099YKLCM1N
2. **OAuth & Permissions** → Copy "Bot User OAuth Token" (`xoxb-...`)
3. **Basic Information** → Copy "Signing Secret"

---

## Local Development

### Prerequisites

```bash
# Python 3.12+
python3 --version

# Install dependencies
cd service/slack_webhook
pip install -r requirements.txt

# ngrok or Cloudflare Tunnel for public URL
# (Slack requires HTTPS webhook)
```

### Run Locally

```bash
# Set environment variables
export SLACK_BOT_TOKEN=xoxb-your-token
export SLACK_SIGNING_SECRET=your-secret
export PROJECT_ID=bobs-brain
export LOCATION=us-central1
export AGENT_ENGINE_ID=your-engine-id

# Start server
python main.py
```

### Expose Public URL

**Option 1: Cloudflare Tunnel (Recommended)**
```bash
cloudflared tunnel --url http://localhost:8080
# Copy the https://xxx.trycloudflare.com URL
```

**Option 2: ngrok**
```bash
ngrok http 8080
# Copy the https://xxx.ngrok.io URL
```

### Configure Slack

1. Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
2. Enable Events: **ON**
3. Request URL: `https://YOUR-PUBLIC-URL/slack/events`
4. Slack will send verification challenge (webhook handles automatically)
5. Subscribe to bot events:
   - `app_mention`
   - `message.im`
   - `message.channels` (optional)
6. Save Changes

### Test in Slack

```
# In Slack channel or DM:
@Bob hello

# Bob should respond via Agent Engine
```

---

## Deployment

### Build Docker Image

```bash
cd service/slack_webhook
docker build -t gcr.io/bobs-brain/slack-webhook:0.6.0 .
```

### Push to GCR

```bash
docker push gcr.io/bobs-brain/slack-webhook:0.6.0
```

### Deploy to Cloud Run

```bash
gcloud run deploy slack-webhook \
  --image gcr.io/bobs-brain/slack-webhook:0.6.0 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SLACK_BOT_TOKEN=xoxb-...,SLACK_SIGNING_SECRET=...,PROJECT_ID=bobs-brain,LOCATION=us-central1,AGENT_ENGINE_ID=xxx
```

**Get Cloud Run URL:**
```bash
gcloud run services describe slack-webhook \
  --region us-central1 \
  --format 'value(status.url)'
```

### Update Slack Configuration

1. Copy Cloud Run URL: `https://slack-webhook-xxx.run.app`
2. Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
3. Update Request URL: `https://slack-webhook-xxx.run.app/slack/events`
4. Save Changes

**Or use Terraform (Phase 4):**
```hcl
resource "google_cloud_run_service" "slack_webhook" {
  name     = "slack-webhook"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/bobs-brain/slack-webhook:0.6.0"
        env {
          name  = "SLACK_BOT_TOKEN"
          value_from {
            secret_key_ref {
              name = "slack-bot-token"
              key  = "latest"
            }
          }
        }
        # ... more env vars
      }
    }
  }
}
```

---

## Security

### Signature Verification

All Slack requests are verified using HMAC-SHA256:

1. Extract timestamp and signature from headers
2. Compute expected signature: `v0=HMAC_SHA256(signing_secret, f"v0:{timestamp}:{body}")`
3. Compare using constant-time comparison
4. Reject if timestamp > 5 minutes old (replay attack prevention)

**Implementation:**
```python
def verify_slack_signature(body: bytes, timestamp: str, signature: str) -> bool:
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    expected = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
```

### Bot Loop Prevention

Ignores messages from bots (including itself):
```python
if event.get("bot_id"):
    return {"ok": True}  # Ignore bot messages
```

### Retry Prevention

Ignores Slack retry attempts (prevents duplicate responses):
```python
if request.headers.get("x-slack-retry-num"):
    return {"ok": True}  # Already processed
```

---

## Monitoring

### Cloud Run Logs

```bash
# View real-time logs
gcloud run services logs tail slack-webhook --region us-central1

# View recent logs
gcloud run services logs read slack-webhook --region us-central1 --limit 100

# Filter errors
gcloud run services logs read slack-webhook --region us-central1 --limit 50 | grep ERROR
```

### Key Metrics

- **Slack events received**: Total event count
- **Agent Engine queries**: Proxy request count
- **Slack messages posted**: Response count
- **Error rate**: Failed signature verifications, Agent Engine errors
- **Latency**: Time from event receipt to Slack response

### Slack App Logs

View Slack-side logs:
https://api.slack.com/apps/A099YKLCM1N/event-subscriptions

---

## Troubleshooting

### Slack Shows "Verification Failed"

**Cause:** Webhook not responding with challenge

**Fix:**
Ensure webhook handles URL verification:
```python
if data.get("type") == "url_verification":
    return {"challenge": data.get("challenge")}
```

### Bob Not Responding to Mentions

**Cause 1:** Signature verification failing

**Fix:**
- Verify `SLACK_SIGNING_SECRET` matches Slack app
- Check Cloud Run logs for signature errors

**Cause 2:** Agent Engine unavailable

**Fix:**
- Check Agent Engine deployment status
- Verify `AGENT_ENGINE_URL` is correct
- Check IAM permissions

**Cause 3:** Bot loop prevention triggered

**Fix:**
- Ensure bot's own messages have `bot_id` set
- Check logs for "Ignoring bot message"

### Duplicate Responses

**Cause:** Slack retrying due to slow response

**Fix:**
- Return `{"ok": True}` immediately (within 3 seconds)
- Process Agent Engine query asynchronously if needed
- Check for `x-slack-retry-num` header to ignore retries

### "Invalid Signature" Errors

**Cause:** Time skew or incorrect secret

**Fix:**
1. Verify server time is accurate (NTP sync)
2. Verify `SLACK_SIGNING_SECRET` matches Slack app
3. Check 5-minute timestamp window is sufficient

---

## Testing

### Unit Tests

```bash
# Test signature verification
python -c "
from main import verify_slack_signature
import time

body = b'{\"type\":\"url_verification\",\"challenge\":\"test\"}'
timestamp = str(int(time.time()))
# Generate test signature...
"
```

### Integration Tests

```bash
# Start webhook locally
python main.py &

# Test health
curl http://localhost:8080/health

# Test Slack challenge (requires ngrok/cloudflared)
curl -X POST http://localhost:8080/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'

# Should return: {"challenge":"test123"}
```

### End-to-End Test

1. Deploy to Cloud Run
2. Configure Slack webhook URL
3. Send test message in Slack: `@Bob hello`
4. Verify Bob responds
5. Check Cloud Run logs for event processing

---

## Related Documentation

- **Agent Engine Deployment:** See `my_agent/` directory
- **A2A Gateway:** See `service/a2a_gateway/`
- **Phase 3 Plan:** See `000-docs/057-AT-COMP-terraform-comparison.md`
- **Hard Mode Rules:** See `CLAUDE.md` (R3 section)
- **Slack App:** https://api.slack.com/apps/A099YKLCM1N

---

## Status

- **Phase 3:** In Progress ✅
- **Implementation:** Complete ✅
- **Testing:** Pending ⏳
- **Deployment:** Pending ⏳ (Phase 4 - Terraform)

**Next Steps:**
1. Test webhook locally
2. Deploy to Cloud Run
3. Configure Slack app with Cloud Run URL
4. Test end-to-end Slack → Agent Engine flow

---

**Last Updated:** 2025-11-11
**Version:** 0.6.0
**Category:** Phase 3 - Service Gateways
**Slack App ID:** A099YKLCM1N
**Bot User ID:** U07NRCYJX8A
