# 🚀 Bob's Brain - Quick Start Guide

**Date:** 2025-10-05
**Status:** ✅ READY TO LAUNCH
**All credentials:** Complete!

---

## ✅ Pre-Flight Checklist

- [x] Slack credentials stored in .env
- [x] Bot token obtained
- [x] .env is gitignored
- [x] Directory structure professional
- [x] All imports working (src symlink)

**You're ready to fire up Bob!**

---

## 🔥 Option 1: Quick Start (Simplest)

### 1. Add Your LLM API Key

Pick ONE provider and add your API key to `.env`:

```bash
cd ~/projects/bobs-brain

# Option A: Google Gemini (cheapest, $0.01/1M tokens)
echo 'GOOGLE_API_KEY=your-google-api-key-here' >> .env

# Option B: Anthropic Claude (best quality)
# echo 'ANTHROPIC_API_KEY=sk-ant-...' >> .env
# sed -i 's/PROVIDER=google/PROVIDER=anthropic/' .env
# sed -i 's/MODEL=gemini-2.0-flash/MODEL=claude-3-5-sonnet-20240620/' .env

# Option C: Local Ollama (free, slower)
# ollama pull qwen2.5:7b
# sed -i 's/PROVIDER=google/PROVIDER=ollama/' .env
# sed -i 's/MODEL=gemini-2.0-flash/MODEL=qwen2.5:7b/' .env
```

### 2. Install Dependencies

```bash
cd ~/projects/bobs-brain

# Activate virtual environment (or create if needed)
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Start Bob

```bash
# Load environment variables
source .env

# Start Flask app
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

### 4. Test Bob

Open another terminal:

```bash
# Health check
curl http://localhost:8080/health

# Test query (requires X-API-Key header)
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me-to-something-secure" \
  -d '{"query":"Hello Bob! Who are you?"}'
```

**Expected response:**
```json
{
  "ok": true,
  "answer": "Query received: Hello Bob! Who are you?"
}
```

---

## 🌐 Option 2: Connect to Slack (Full Setup)

### 1. Start Bob Locally (from Option 1)

```bash
cd ~/projects/bobs-brain
source .venv/bin/activate
source .env
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

### 2. Expose Local Server with ngrok

```bash
# Install ngrok if needed
# Download from: https://ngrok.com/download

# Start ngrok
ngrok http 8080

# Copy the HTTPS URL (e.g., https://abc123.ngrok-free.app)
```

### 3. Configure Slack Event Subscriptions

```
1. Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
2. Enable Events: Toggle ON
3. Request URL: https://your-ngrok-url.ngrok-free.app/slack/events
4. Wait for verification ✅
5. Subscribe to bot events:
   - message.channels
   - message.groups
   - message.im
   - app_mention
6. Save Changes
```

### 4. Test in Slack

```
1. Go to your Slack workspace
2. Invite @Bob to a channel: /invite @Bob
3. Mention Bob: @Bob hello!
4. Bob should respond!
```

---

## ☁️ Option 3: Deploy to Google Cloud Run (Production)

Bob gets his own dedicated Google Cloud project for:
- **Cost tracking**: See exactly what Bob costs
- **Security isolation**: Bob's credentials separate from other services
- **Clean organization**: Bob's infrastructure isolated

### Step 1: Create Bob's Project

```bash
cd ~/projects/bobs-brain
./05-Scripts/deploy/create-bob-project.sh
```

This creates the `bobs-house-ai` project and enables required APIs.

### Step 2: Store Secrets

**IMPORTANT**: First add your Google API key to .env:
```bash
echo 'GOOGLE_API_KEY=your-google-api-key-here' >> .env
```

Then store all secrets in Secret Manager:
```bash
./05-Scripts/deploy/store-secrets.sh
```

This stores:
- Slack Bot Token (from .env)
- Slack Signing Secret (from .env)
- Google API Key (from .env)
- BB_API_KEY (auto-generated, printed to terminal)

**Save the BB_API_KEY** printed by the script!

### Step 3: Deploy to Cloud Run

```bash
./05-Scripts/deploy/deploy-to-cloudrun.sh
```

This deploys Bob with:
- **Memory**: 1Gi
- **CPU**: 1 vCPU
- **Instances**: 0-10 (auto-scales, min=0 for cost savings)
- **Timeout**: 300s
- **Provider**: Google Gemini 2.0 Flash

### Step 4: Get Service URL

The deploy script prints the URL. You can also get it with:
```bash
gcloud run services describe bobs-brain \
  --project bobs-house-ai \
  --region us-central1 \
  --format="value(status.url)"

# Example output: https://bobs-brain-abc123.run.app
```

### Step 5: Configure Slack

```
1. Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions
2. Enable Events: Toggle ON
3. Request URL: https://bobs-brain-abc123.run.app/slack/events
4. Wait for verification ✅
5. Subscribe to bot events:
   - message.channels
   - message.groups
   - message.im
   - app_mention
6. Save Changes
```

### Step 6: Test Production Bob

```bash
# Health check
curl https://bobs-brain-abc123.run.app/health

# Test in Slack
@Bob hello from production!
```

### Monitoring & Logs

```bash
# View logs
gcloud run services logs read bobs-brain \
  --project bobs-house-ai \
  --region us-central1 \
  --limit 50

# View in Cloud Console
# https://console.cloud.google.com/run?project=bobs-house-ai
```

---

## 🛠️ Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Install dependencies
```bash
cd ~/projects/bobs-brain
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: "GOOGLE_API_KEY not set"

**Solution:** Add API key to .env
```bash
echo 'GOOGLE_API_KEY=your-key-here' >> .env
source .env
```

### Issue: Slack events not working

**Solution:** Check ngrok URL and Slack configuration
```bash
# 1. Make sure ngrok is running
ngrok http 8080

# 2. Update Slack Event Subscriptions URL
# 3. Check Bob's logs for errors
```

### Issue: "unauthorized" error

**Solution:** Update BB_API_KEY in .env
```bash
# Generate secure key
openssl rand -hex 32

# Add to .env
echo 'BB_API_KEY=your-secure-key-here' >> .env

# Use in requests
curl -H "X-API-Key: your-secure-key-here" ...
```

### Issue: Python can't find src module

**Solution:** Symlink is working, but try:
```bash
cd ~/projects/bobs-brain
ls -la src  # Should show: src -> 02-Src

# If missing, recreate:
ln -s 02-Src src
```

---

## 📊 API Endpoints Reference

### Public Endpoints (No Auth Required)

```bash
GET  /                    # Service info
GET  /health              # Health check
GET  /health/backends     # Backend status
GET  /config              # Current configuration
GET  /metrics             # Prometheus metrics
POST /slack/events        # Slack webhook
```

### Protected Endpoints (Require X-API-Key)

```bash
POST /api/query           # Ask Bob a question
POST /learn               # Submit correction
POST /api/skill           # Execute skill
POST /api/knowledge       # Query knowledge base
GET  /api/knowledge/status # Knowledge orchestrator status
```

### Example API Call

```bash
# Set your API key
export BB_API_KEY="change-me-to-something-secure"

# Ask Bob a question
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{
    "query": "What is the capital of France?"
  }'

# Submit correction (for learning)
curl -X POST http://localhost:8080/learn \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BB_API_KEY" \
  -d '{
    "correction": "Always be concise in responses",
    "context": "User prefers short answers"
  }'
```

---

## 🔐 Security Checklist

Before going to production:

- [ ] **Change BB_API_KEY** from default "change-me-to-something-secure"
- [ ] **Rotate Slack secrets** (client secret, signing secret)
- [ ] **Use Google Secret Manager** for production (not .env)
- [ ] **Enable request signature verification** for Slack
- [ ] **Set up monitoring** (Cloud Logging, Error Reporting)
- [ ] **Configure rate limiting** (already enabled via flask-limiter)
- [ ] **Review firewall rules** (if using VPC)

---

## 🎯 Recommended LLM Provider

For getting started quickly:

**Recommended:** Google Gemini Flash
- **Cost:** $0.01 per 1M tokens (very cheap!)
- **Speed:** ~500ms response time
- **Quality:** Very good for most tasks
- **Context:** 1M tokens
- **Setup:** Just add `GOOGLE_API_KEY` to .env

**Get API key:** https://aistudio.google.com/apikey

---

## 📚 Documentation

- **Main README:** `README.md` - Full project overview
- **AI Assistant Guide:** `CLAUDE.md` - Development guidance
- **Slack Setup:** `01-Docs/003-sec-slack-credentials.md` - Security guide
- **Directory Standards:** `.directory-standards.md` - File organization
- **Audit Report:** `claudes-docs/BOB-AUDIT-REPORT-2025-10-05.md` - Full analysis
- **LLM Options:** `claudes-docs/LOCAL-LLM-OPTIONS-2025-10-05.md` - Model comparison

---

## ⚡ One-Liner Quick Start

```bash
cd ~/projects/bobs-brain && \
echo 'GOOGLE_API_KEY=your-key-here' >> .env && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
source .env && \
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

**Then test:**
```bash
curl http://localhost:8080/health
```

---

**Created:** 2025-10-05
**Status:** Ready to launch! 🚀
**Next:** Add your LLM API key and start Bob!
