# ✅ Bob's Brain Slack Credentials - Setup Complete

**Date:** 2025-10-05
**Status:** Credentials stored, Bot Token needed
**Action Required:** Get Bot Token from Slack

---

## 🔑 Credentials Stored

All Slack credentials have been securely stored in:

### 1. Local .env file
**Location:** `~/projects/bobs-brain/.env` ✅ Gitignored

```bash
SLACK_APP_ID=A099YKLCM1N
SLACK_CLIENT_ID=9318399480516.9338666429056
SLACK_CLIENT_SECRET=41acb3400fc4c3cf185cf44f6d79d73f
SLACK_SIGNING_SECRET=d00942f9329d902a0af65f31f968f355
SLACK_VERIFICATION_TOKEN=78d6H4he0T1kXcCpSl1y4iEM
SLACK_BOT_TOKEN=(missing - see below)
```

### 2. Documentation
**Location:** `01-Docs/003-sec-slack-credentials.md`
- Full credential list
- How to use `pass` password manager
- Rotation instructions
- Security best practices

---

## ⚠️ CRITICAL: Missing Bot Token

You still need the **Bot User OAuth Token** to actually send messages!

### How to Get Bot Token

**1. Go to your Slack App:**
```
https://api.slack.com/apps/A099YKLCM1N/oauth
```

**2. Install to Workspace (if not already)**
- Click: "Install to Workspace"
- Authorize the permissions

**3. Copy Bot Token**
- After installation, look for: **Bot User OAuth Token**
- Starts with: `xoxb-`
- **Copy the entire token**

**4. Add to .env:**
```bash
echo 'SLACK_BOT_TOKEN=xoxb-your-token-here' >> ~/projects/bobs-brain/.env
```

---

## 🚀 Test Bob with Slack

Once you have the bot token:

### 1. Start Bob Locally
```bash
cd ~/projects/bobs-brain
source .env

# Start Flask app
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

### 2. Expose Local Server (ngrok or similar)
```bash
# Install ngrok if needed
ngrok http 8080

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

### 3. Configure Slack Webhook
```
Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions

Request URL: https://abc123.ngrok.io/slack/events
```

### 4. Test in Slack
- Go to your Slack workspace
- Mention @Bob in a channel
- Bob should respond!

---

## 🔒 Security Recommendations

### ⚠️ IMPORTANT: These secrets were exposed in plaintext

**Highly Recommended Actions:**

#### 1. Rotate Client Secret
```
https://api.slack.com/apps/A099YKLCM1N/general
→ App Credentials → Rotate Client Secret
```

#### 2. Rotate Signing Secret
```
https://api.slack.com/apps/A099YKLCM1N/general
→ App Credentials → Rotate Signing Secret
```

#### 3. Rotate Verification Token (Legacy - less critical)
Verification tokens are being phased out in favor of signing secrets, but you can regenerate if needed.

### Why Rotate?
These credentials were shared in a conversation log and should be considered potentially compromised.

---

## 📋 Required Slack App Scopes

Make sure your app has these OAuth scopes:

### Bot Token Scopes (Required)
✅ `chat:write` - Send messages
✅ `chat:write.public` - Send to public channels
✅ `channels:history` - Read messages
✅ `channels:read` - View channels
✅ `app_mentions:read` - Know when mentioned
✅ `users:read` - View user info

### Event Subscriptions (Required)
✅ `message.channels` - Public channel messages
✅ `message.groups` - Private channel messages
✅ `message.im` - Direct messages
✅ `app_mention` - When @bob is mentioned

---

## 🛡️ Password Manager Setup (Optional but Recommended)

Store credentials in `pass` for backup:

```bash
# Store each credential
pass insert bobs-brain/slack/app-id
# Enter: A099YKLCM1N

pass insert bobs-brain/slack/client-id
# Enter: 9318399480516.9338666429056

pass insert bobs-brain/slack/client-secret
# Enter: 41acb3400fc4c3cf185cf44f6d79d73f

pass insert bobs-brain/slack/signing-secret
# Enter: d00942f9329d902a0af65f31f968f355

pass insert bobs-brain/slack/verification-token
# Enter: 78d6H4he0T1kXcCpSl1y4iEM

pass insert bobs-brain/slack/bot-token
# Enter: xoxb-... (once you get it)
```

### Retrieve from Pass
```bash
# View credential
pass bobs-brain/slack/bot-token

# Copy to clipboard (safer)
pass -c bobs-brain/slack/bot-token

# Use in scripts
export SLACK_BOT_TOKEN=$(pass bobs-brain/slack/bot-token)
```

---

## 📊 Current Setup Status

| Component | Status | Notes |
|-----------|--------|-------|
| **App ID** | ✅ Stored | A099YKLCM1N |
| **Client ID** | ✅ Stored | 9318399480516.9338666429056 |
| **Client Secret** | ⚠️ Stored, needs rotation | Security concern |
| **Signing Secret** | ⚠️ Stored, needs rotation | Security concern |
| **Verification Token** | ⚠️ Stored, needs rotation | Legacy, less critical |
| **Bot Token** | ❌ Missing | **GET THIS NEXT!** |
| **.env file** | ✅ Created | Gitignored |
| **Documentation** | ✅ Created | 01-Docs/003-sec-slack-credentials.md |
| **Git Safety** | ✅ Verified | .env is gitignored |

---

## 🎯 Next Steps (In Order)

### 1. Get Bot Token (REQUIRED)
```
https://api.slack.com/apps/A099YKLCM1N/oauth
→ Install to Workspace
→ Copy "Bot User OAuth Token"
→ Add to .env file
```

### 2. Test Locally (REQUIRED)
```bash
cd ~/projects/bobs-brain
source .env
python -m flask --app src.app run --port 8080
```

### 3. Expose with ngrok (for testing)
```bash
ngrok http 8080
→ Update Slack Event Subscriptions URL
```

### 4. Rotate Secrets (RECOMMENDED)
```
https://api.slack.com/apps/A099YKLCM1N/general
→ Rotate Client Secret
→ Rotate Signing Secret
→ Update .env with new values
```

### 5. Deploy to Production (OPTIONAL)
```bash
# Use Google Secret Manager for production
gcloud secrets create slack-bot-token --data-file=- <<< "xoxb-..."

# Deploy to Cloud Run
gcloud run deploy bobs-brain \
  --source . \
  --set-secrets SLACK_BOT_TOKEN=slack-bot-token:latest
```

---

## 🔍 Verify Everything Works

### Check .env File
```bash
cat ~/projects/bobs-brain/.env | grep SLACK
# Should show all 6 SLACK_ variables
```

### Check Git Ignore
```bash
cd ~/projects/bobs-brain
git status .env
# Should say "ignored" or not appear
```

### Test Flask App
```bash
cd ~/projects/bobs-brain
source .env
python -m flask --app src.app run --port 8080

# In another terminal:
curl http://localhost:8080/health
# Should return: {"status":"ok",...}
```

### Test Slack Endpoint (after getting bot token)
```bash
curl -X POST http://localhost:8080/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'
# Should echo back: {"challenge":"test123"}
```

---

## 📚 Documentation Reference

**Full Security Guide:** `01-Docs/003-sec-slack-credentials.md`
- Complete credential list
- Rotation procedures
- Pass password manager usage
- Production deployment
- Security best practices

---

## ⚡ Quick Commands

```bash
# Load environment
source ~/projects/bobs-brain/.env

# Start Bob
python -m flask --app src.app run --port 8080

# Check Slack variables
env | grep SLACK

# Get from pass
pass bobs-brain/slack/bot-token

# Test health
curl http://localhost:8080/health
```

---

**Created:** 2025-10-05
**Status:** Setup complete, bot token needed
**Security:** ⚠️ Credential rotation recommended
**Next:** Get bot token from https://api.slack.com/apps/A099YKLCM1N/oauth
