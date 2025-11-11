# Bob's Brain - Slack Credentials Security Guide

**Date:** 2025-10-05
**Status:** ⚠️ CREDENTIALS EXPOSED - ROTATION RECOMMENDED
**Credential Store:** `pass` password manager

---

## ⚠️ SECURITY ALERT

**IMPORTANT:** The Slack credentials below were shared in plaintext in a conversation. While they are now stored securely, it is **highly recommended** to rotate these secrets in the Slack app settings.

---

## 🔑 Current Slack App Credentials

### App Information
- **App ID:** A099YKLCM1N
- **Client ID:** 9318399480516.9338666429056
- **Client Secret:** 41acb3400fc4c3cf185cf44f6d79d73f ⚠️ ROTATE
- **Signing Secret:** d00942f9329d902a0af65f31f968f355 ⚠️ ROTATE
- **Verification Token:** 78d6H4he0T1kXcCpSl1y4iEM ⚠️ ROTATE

### Where These Are Stored

**1. Local .env file:** `~/projects/bobs-brain/.env` (gitignored)
**2. Password Manager:** `pass` (recommended for backup)

---

## 🔒 Storing in Pass Password Manager

### Manual Storage (Recommended Method)

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

pass insert bobs-brain/slack/bot-token
# Enter: xoxb-... (from Slack app OAuth page)
```

### Retrieve from Pass

```bash
# Get individual credentials
pass bobs-brain/slack/app-id
pass bobs-brain/slack/client-id
pass bobs-brain/slack/client-secret
pass bobs-brain/slack/signing-secret
pass bobs-brain/slack/bot-token

# Copy to clipboard (doesn't show in terminal)
pass -c bobs-brain/slack/client-secret

# Use in scripts
export SLACK_CLIENT_SECRET=$(pass bobs-brain/slack/client-secret)
```

### Update .env from Pass

```bash
# Create .env from pass (one-time setup)
cd ~/projects/bobs-brain

cat > .env <<EOF
SLACK_APP_ID=$(pass bobs-brain/slack/app-id)
SLACK_CLIENT_ID=$(pass bobs-brain/slack/client-id)
SLACK_CLIENT_SECRET=$(pass bobs-brain/slack/client-secret)
SLACK_SIGNING_SECRET=$(pass bobs-brain/slack/signing-secret)
SLACK_BOT_TOKEN=$(pass bobs-brain/slack/bot-token)
EOF
```

---

## 🔄 How to Rotate Credentials (RECOMMENDED!)

### Why Rotate?
These credentials were shared in plaintext and should be considered compromised.

### Steps to Rotate

#### 1. Go to Slack App Settings
```
https://api.slack.com/apps/A099YKLCM1N
```

#### 2. Rotate Client Secret
- Navigate to: **Basic Information → App Credentials**
- Click: **Rotate** next to Client Secret
- **Copy new secret immediately** (only shown once!)
- Update in pass: `pass insert -e bobs-brain/slack/client-secret`
- Update .env file

#### 3. Rotate Signing Secret
- Navigate to: **Basic Information → App Credentials**
- Click: **Rotate** next to Signing Secret
- **Copy new secret immediately**
- Update in pass: `pass insert -e bobs-brain/slack/signing-secret`
- Update .env file

#### 4. Regenerate Bot Token (Optional but Recommended)
- Navigate to: **OAuth & Permissions**
- Click: **Reinstall to Workspace**
- Copy new `xoxb-` token
- Update in pass: `pass insert -e bobs-brain/slack/bot-token`
- Update .env file

#### 5. Test New Credentials
```bash
cd ~/projects/bobs-brain
source .env
python -m flask --app src.app run --port 8080

# Test Slack endpoint
curl -X POST http://localhost:8080/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test"}'
```

---

## 📋 Slack App Configuration

### Required OAuth Scopes (Bot Token)
Ensure your Slack app has these scopes:

**Bot Token Scopes:**
- `chat:write` - Send messages
- `chat:write.public` - Send to public channels
- `channels:history` - Read channel history
- `channels:read` - View channels
- `groups:history` - Read private channel history
- `im:history` - Read DM history
- `users:read` - View users

### Event Subscriptions
**Request URL:** `https://your-cloud-run-url/slack/events`

**Subscribe to bot events:**
- `message.channels`
- `message.groups`
- `message.im`
- `app_mention`

---

## 🚀 Getting Missing Bot Token

If you don't have the bot token yet:

### 1. Install App to Workspace
```
https://api.slack.com/apps/A099YKLCM1N/oauth
Click: "Install to Workspace"
```

### 2. Copy Bot Token
- After installation, you'll see: **Bot User OAuth Token**
- Starts with: `xoxb-`
- **Copy immediately** - you may not see it again!

### 3. Store in Pass
```bash
pass insert bobs-brain/slack/bot-token
# Paste: xoxb-9318399480516-9338...
```

### 4. Add to .env
```bash
echo "SLACK_BOT_TOKEN=xoxb-..." >> ~/projects/bobs-brain/.env
```

---

## 🔐 Security Best Practices

### DO:
- ✅ Store all secrets in `pass`
- ✅ Use `.env` for local development (gitignored)
- ✅ Use Google Secret Manager for production
- ✅ Rotate secrets if exposed
- ✅ Use HTTPS for Slack webhooks
- ✅ Verify Slack request signatures

### DON'T:
- ❌ Commit .env to git
- ❌ Share secrets in chat/email
- ❌ Hardcode secrets in code
- ❌ Use same secrets for dev/prod
- ❌ Ignore security warnings

---

## 🛡️ Production Deployment

### Google Cloud Secret Manager

```bash
# Store secrets in Secret Manager
echo -n "41acb3400fc4c3cf185cf44f6d79d73f" | \
  gcloud secrets create slack-client-secret --data-file=-

echo -n "d00942f9329d902a0af65f31f968f355" | \
  gcloud secrets create slack-signing-secret --data-file=-

echo -n "xoxb-..." | \
  gcloud secrets create slack-bot-token --data-file=-
```

### Cloud Run Configuration

```bash
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --set-secrets \
    SLACK_CLIENT_SECRET=slack-client-secret:latest,\
    SLACK_SIGNING_SECRET=slack-signing-secret:latest,\
    SLACK_BOT_TOKEN=slack-bot-token:latest
```

---

## 📞 Quick Reference

### Pass Commands
```bash
# List all Bob's Brain secrets
pass bobs-brain/slack/

# Show specific secret
pass bobs-brain/slack/client-secret

# Copy to clipboard (safer)
pass -c bobs-brain/slack/client-secret

# Edit existing secret
pass edit bobs-brain/slack/client-secret

# Delete secret
pass rm bobs-brain/slack/client-secret
```

### Verify .env is Gitignored
```bash
cd ~/projects/bobs-brain
git check-ignore .env
# Should output: .env (means it's ignored)
```

### Load .env in Scripts
```bash
# In bash scripts
source ~/projects/bobs-brain/.env
echo $SLACK_CLIENT_SECRET

# In Python
from dotenv import load_dotenv
load_dotenv()
import os
os.getenv('SLACK_CLIENT_SECRET')
```

---

## ⚠️ IMMEDIATE ACTION ITEMS

- [ ] **CRITICAL:** Rotate Client Secret in Slack app settings
- [ ] **CRITICAL:** Rotate Signing Secret in Slack app settings
- [ ] **RECOMMENDED:** Get Bot Token from Slack app OAuth page
- [ ] **RECOMMENDED:** Store all credentials in pass
- [ ] **RECOMMENDED:** Test rotated credentials
- [ ] **OPTIONAL:** Set up Google Secret Manager for production

---

## 🔍 Verify Current Setup

```bash
# 1. Check .env exists and has credentials
cat ~/projects/bobs-brain/.env | grep SLACK

# 2. Check .env is gitignored
cd ~/projects/bobs-brain
git status .env  # Should say "ignored"

# 3. Test credentials work
source .env
python -m flask --app src.app run --port 8080
```

---

**Created:** 2025-10-05
**Last Updated:** 2025-10-05
**Status:** ⚠️ Credentials stored, rotation recommended
**Security Level:** Medium (exposed in conversation, needs rotation)
