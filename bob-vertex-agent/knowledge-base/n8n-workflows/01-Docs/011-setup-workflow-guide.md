# X Automation Setup Guide

**Created**: October 4, 2025

This guide walks you through the complete setup of the "No Chase Tokens™" automation system.

## Prerequisites

✅ X (Twitter) Developer Account with OAuth 2.0 app created
✅ n8n instance running at `http://localhost:5678`
✅ Python 3.12+ installed
✅ `pass` (password manager) installed and configured with GPG
✅ Git configured for blog repositories

## Step-by-Step Setup

### Step 1: Generate n8n API Key

1. Open n8n web interface: `http://localhost:5678`
2. Login with credentials (user: jeremylongshore)
3. Go to **Settings** → **API**
4. Click **Create API Key**
5. Give it a name: "X Token Auto-Refresh"
6. Copy the generated API key
7. Update `/home/jeremy/x-token-automation/config/targets.json`:
   ```json
   {
     "name": "n8n-workflows",
     "type": "n8n_api",
     "base_url": "http://localhost:5678",
     "credential_name": "X OAuth2",
     "api_token": "YOUR_API_KEY_HERE",
     "description": "n8n X/Twitter OAuth2 credential auto-update"
   }
   ```

### Step 2: Create X OAuth2 Credential in n8n

1. In n8n, go to **Credentials** → **Add Credential**
2. Search for "Twitter OAuth2 API"
3. Name it exactly: **"X OAuth2"** (this must match the `credential_name` in targets.json)
4. Enter your X API credentials:
   - **Client ID**: Your X OAuth 2.0 Client ID
   - **Client Secret**: Your X OAuth 2.0 Client Secret
5. Click **Connect my account**
6. Complete the OAuth flow in the popup window
7. Verify the credential is saved

### Step 3: Initialize OAuth Tokens in pass

```bash
cd /home/jeremy/x-token-automation

# Run the OAuth initialization wizard
python3 bin/x-token-init.py

# Follow the prompts to complete OAuth flow
# Tokens will be encrypted and stored in pass under x/oauth2/
```

**What gets stored in pass:**
- `x/oauth2/client_id`
- `x/oauth2/client_secret`
- `x/oauth2/access_token`
- `x/oauth2/refresh_token`
- `x/oauth2/expires_at`

### Step 4: Test Manual Token Distribution

```bash
# Test token refresh
python3 /home/jeremy/x-token-automation/bin/x-token-refresh.py

# Expected output:
# ✅ Access token refreshed
# ✅ Tokens stored in pass

# Test token distribution
python3 /home/jeremy/x-token-automation/bin/x-token-distribute.py

# Expected output:
# ✅ Updated: /home/jeremy/waygate-mcp/.env
# ✅ n8n credential 'X OAuth2' updated successfully
```

### Step 5: Install Systemd Timer (Auto-Refresh Every 90min)

```bash
cd /home/jeremy/x-token-automation

# Copy service and timer files
sudo cp config/x-token-refresh.service /etc/systemd/system/
sudo cp config/x-token-refresh.timer /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start timer
sudo systemctl enable x-token-refresh.timer
sudo systemctl start x-token-refresh.timer

# Verify timer is active
sudo systemctl status x-token-refresh.timer

# Expected output:
# ● x-token-refresh.timer
#    Loaded: loaded (/etc/systemd/system/x-token-refresh.timer; enabled)
#    Active: active (waiting)
#   Trigger: [next execution time]
```

### Step 6: Import n8n Workflows

#### Workflow 1: X Token Auto-Refresh

1. In n8n, click **Workflows** → **Add Workflow**
2. Click **⋮** (menu) → **Import from File**
3. Select: `/home/jeremy/projects/n8n-workflows/x-automation-workflows/workflows/x-token-auto-refresh.json`
4. Click **Import**
5. **Activate** the workflow (toggle in top right)
6. Verify it runs every 90 minutes (check Schedule Trigger node)

#### Workflow 2: Content Nuke Publisher

1. Click **Add Workflow**
2. Import: `content-nuke-publisher.json`
3. Open the **Webhook** node
4. Copy the **Production URL**: `http://localhost:5678/webhook/content-nuke-publish`
5. **Activate** the workflow
6. Save the webhook URL for testing

### Step 7: Verify Token Auto-Refresh Works

```bash
# Check systemd timer logs
sudo journalctl -u x-token-refresh.service -f

# Manually trigger a refresh to test
sudo systemctl start x-token-refresh.service

# Expected output in logs:
# ✅ Access token refreshed
# ✅ Tokens stored in pass
# ✅ Updated: /home/jeremy/waygate-mcp/.env
# ✅ n8n credential 'X OAuth2' updated successfully
```

**Verify in n8n**:
1. Go to **Credentials** → **X OAuth2**
2. Check **Last Modified** timestamp - should be recent
3. Credentials are updated automatically!

### Step 8: Test Content Nuke Publisher Webhook

```bash
# Create test content files
echo "Test tweet 1/1

Testing the Content Nuke automation! 🚀" > /tmp/test-x-thread.txt

echo "Testing LinkedIn post automation from Content Nuke system." > /tmp/test-linkedin.txt

# Trigger n8n webhook
curl -X POST http://localhost:5678/webhook/content-nuke-publish \
  -H "Content-Type: application/json" \
  -d '{
    "x_thread_path": "/tmp/test-x-thread.txt",
    "linkedin_path": "/tmp/test-linkedin.txt",
    "startai_blog_path": "/home/jeremy/projects/blog/startaitools/content/posts/test-post.md",
    "jeremy_blog_path": "/home/jeremy/projects/blog/jeremylongshore/content/posts/test-post.md"
  }'

# Expected response:
# {
#   "timestamp": "2025-10-04T...",
#   "total": 4,
#   "successful": 4,
#   "failed": 0,
#   "platforms": {...}
# }
```

**Check n8n execution**:
1. Go to **Executions** in n8n
2. Find the "Content Nuke Publisher" execution
3. Verify all 4 nodes executed successfully
4. Check if X thread was posted (check your X account)

### Step 9: Test Full /content-nuke Command

```bash
# From a Claude Code session in any project directory
/content-nuke

# Claude will:
# 1. Analyze your working session
# 2. Ask for thread size (1-7)
# 3. Generate 4 content pieces
# 4. Show you the complete package for review
# 5. After approval, save all 4 files
# 6. Trigger n8n webhook
# 7. n8n publishes to all 4 platforms in parallel
```

## Troubleshooting

### Issue: n8n API returns "Unauthorized"

**Solution**:
1. Regenerate API key in n8n Settings → API
2. Update `targets.json` with new key
3. Test: `python3 bin/x-token-distribute.py`

### Issue: Token refresh fails

**Check**:
```bash
# Verify tokens exist in pass
pass ls x/oauth2

# Should show:
# x
# └── oauth2
#     ├── access_token
#     ├── client_id
#     ├── client_secret
#     ├── expires_at
#     └── refresh_token
```

**Fix**:
```bash
# Re-run initialization
python3 bin/x-token-init.py
```

### Issue: n8n credential not updated

**Check**:
1. Is the credential named exactly "X OAuth2"? (case-sensitive)
2. Is the n8n API key valid?
3. Check distribution logs: `tail -f ~/x-token-automation/logs/distribute.log`

### Issue: Webhook returns 404

**Fix**:
1. Verify "Content Nuke Publisher" workflow is **activated** in n8n
2. Check webhook URL matches the one in the workflow
3. n8n must be running: `docker ps | grep n8n`

### Issue: Blog deployment fails

**Check**:
1. Git credentials configured?
2. Hugo installed? `hugo version`
3. Blog repositories exist at correct paths?
4. Check n8n execution logs for error details

## Monitoring

### Check Token Refresh Status

```bash
# View timer status
sudo systemctl status x-token-refresh.timer

# View recent refresh logs
sudo journalctl -u x-token-refresh.service --since "1 hour ago"

# Check token expiration
pass x/oauth2/expires_at
```

### Check n8n Workflow Status

1. Open n8n web interface
2. Go to **Executions**
3. Filter by workflow: "X Token Auto-Refresh"
4. Check recent executions (should be every 90 minutes)

### View Distribution Logs

```bash
# Real-time log monitoring
tail -f /home/jeremy/x-token-automation/logs/distribute.log

# View last 50 lines
tail -50 /home/jeremy/x-token-automation/logs/distribute.log
```

## Architecture Summary

```
┌─────────────────────────────────────────────────┐
│         Token Auto-Refresh (90min)              │
│                                                  │
│  Systemd Timer → x-token-refresh.py             │
│                ↓                                 │
│  pass (encrypted storage)                       │
│                ↓                                 │
│  x-token-distribute.py                          │
│                ↓                                 │
│  ┌──────────────────┬─────────────────┐         │
│  ↓                  ↓                 ↓         │
│  waygate-mcp/.env   n8n credentials  (future)   │
│                     (via REST API)              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│         Content Publishing (manual)             │
│                                                  │
│  /content-nuke command → Generate 4 pieces      │
│                        ↓                         │
│  Trigger n8n webhook with file paths            │
│                        ↓                         │
│  ┌──────────┬──────────┬──────────┬──────────┐  │
│  ↓          ↓          ↓          ↓          ↓  │
│  X Thread  LinkedIn  StartAI    Jeremy          │
│  (API)     (API)     Blog (Git) Blog (Git)      │
└─────────────────────────────────────────────────┘
```

## Success Criteria

✅ Token refresh runs every 90 minutes automatically
✅ n8n credential updates without manual intervention
✅ `/content-nuke` triggers n8n webhook successfully
✅ All 4 platforms publish content in parallel
✅ Zero "token expired" errors
✅ Complete automation - no manual steps needed

## Next Steps

Once setup is complete:
1. Monitor first 24 hours of token auto-refresh
2. Test `/content-nuke` with real development session
3. Verify all 4 platforms receive content successfully
4. Add analytics tracking for published content
5. Consider adding Slack/Discord notifications for publishing events

---

**Setup Status**: ⏳ Pending manual configuration
**Documentation**: ✅ Complete
**Automation Scripts**: ✅ Ready
**n8n Workflows**: ✅ Ready for import
