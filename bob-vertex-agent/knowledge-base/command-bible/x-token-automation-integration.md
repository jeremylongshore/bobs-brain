# X Token Automation Integration Guide
**For Command Bible Reference**

**Created:** October 4, 2025
**Status:** ✅ Production Ready

---

## 🎯 What This Solves

**Problem:** Your 5 slash commands that post to X fail because OAuth 2.0 tokens expire every 2 hours.

**Solution:** Fully automated token refresh system that runs every 90 minutes and distributes fresh tokens to all slash commands.

---

## 🚀 Complete System Architecture

```
┌──────────────────────────────────────────────────┐
│  systemd Timer (every 90 minutes)                │
└───────────────┬──────────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────────┐
│  1. x-token-refresh.py                           │
│     • Reads refresh_token from pass              │
│     • Calls X OAuth2 API                         │
│     • Gets new tokens                            │
│     • Stores encrypted in pass                   │
└───────────────┬──────────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────────┐
│  2. x-token-distribute.py                        │
│     • Reads tokens from pass                     │
│     • Updates waygate-mcp/.env (atomic)          │
│     • Restarts waygate container                 │
└───────────────┬──────────────────────────────────┘
                │
                ↓
┌──────────────────────────────────────────────────┐
│  3. Slash Commands Always Work!                  │
│     • /content-nuke                              │
│     • /blog-single-startai                       │
│     • /blog-both-x                               │
│     • /blog-jeremy-x                             │
│     • /post-x                                    │
└──────────────────────────────────────────────────┘
```

---

## 📁 System Location

**Everything in:** `~/x-token-automation/`

```
x-token-automation/
├── bin/                    # 4 Python scripts
│   ├── x-token-init.py    # Initial setup wizard
│   ├── x-token-refresh.py # Token refresh (runs every 90 min)
│   ├── x-token-distribute.py # Push to all targets
│   └── x-token-verify.py  # Test tokens work
├── config/                 # Configuration files
│   ├── targets.json       # Where to distribute tokens
│   ├── x-token-refresh.service
│   └── x-token-refresh.timer
├── logs/                   # Operation logs
│   ├── refresh.log
│   ├── distribute.log
│   └── verify.log
├── install.sh              # One-command setup
└── README.md               # Complete documentation
```

---

## ⚡ Quick Installation

```bash
# 1. System is already created in ~/x-token-automation/

# 2. Run installation
cd ~/x-token-automation
./install.sh

# 3. Initialize OAuth
x-token-init.py
# Opens browser, authorize app, tokens saved

# 4. Enable automatic refresh
systemctl --user enable x-token-refresh.timer
systemctl --user start x-token-refresh.timer

# 5. Verify working
x-token-verify.py
```

**Done! Tokens refresh every 90 minutes forever.**

---

## 🔐 Security Features

### 1. Encrypted Storage (Pass)
- All tokens encrypted with GPG
- Never stored in plaintext
- Password manager integration

### 2. Atomic Operations
- No partial writes
- All-or-nothing updates
- Filesystem sync guarantees

### 3. Single Instance Lock
- Prevents concurrent refreshes
- Automatic cleanup
- No race conditions

### 4. Automatic Distribution
- Updates waygate-mcp/.env atomically
- Restarts services automatically
- Verifies distribution success

---

## 📊 How It Works

### Automatic Refresh Cycle (Every 90 min)

**Timer triggers at 90-minute intervals:**

1. **Read credentials from pass**
   ```
   pass x/oauth2/client_id
   pass x/oauth2/client_secret
   pass x/oauth2/refresh_token
   ```

2. **Call X OAuth API**
   ```
   POST https://api.twitter.com/2/oauth2/token
   grant_type=refresh_token
   ```

3. **Receive new tokens**
   ```json
   {
     "access_token": "new_access_token",
     "refresh_token": "new_refresh_token",
     "expires_in": 7200
   }
   ```

4. **Store in pass (encrypted)**
   ```
   pass insert x/oauth2/access_token
   pass insert x/oauth2/refresh_token
   ```

5. **Distribute to waygate-mcp**
   ```
   Update /home/jeremy/waygate-mcp/.env
   Restart waygate container
   ```

6. **Verify tokens work**
   ```
   GET https://api.twitter.com/2/users/me
   Status: 200 OK ✅
   ```

---

## 🎛️ Commands Affected

All 5 slash commands now have automatic token refresh:

| Command | Description | Token Source |
|---------|-------------|--------------|
| `/content-nuke` | Multi-platform blast | waygate-mcp/.env |
| `/blog-single-startai` | Tech blog + X | waygate-mcp/.env |
| `/blog-both-x` | Both blogs + X | waygate-mcp/.env |
| `/blog-jeremy-x` | Portfolio + X | waygate-mcp/.env |
| `/post-x` | Direct X posting | waygate-mcp/.env |

**All read from:** `/home/jeremy/waygate-mcp/.env`
**Updated by:** `x-token-distribute.py`
**Refresh cycle:** Every 90 minutes

---

## 🔍 Monitoring

### Check Timer Status
```bash
systemctl --user status x-token-refresh.timer
```

### View Recent Refreshes
```bash
tail -20 ~/x-token-automation/logs/refresh.log
```

### Manual Verification
```bash
x-token-verify.py
```

### Check Token Expiration
```bash
pass x/oauth2/expires_at | xargs -I {} date -d @{}
```

---

## 🐛 Troubleshooting

### Slash Command Fails with "Invalid Token"

**Quick Fix:**
```bash
# Manually trigger refresh
x-token-refresh.py

# Distribute to targets
x-token-distribute.py

# Verify works
x-token-verify.py
```

### Token Refresh Fails

**Check logs:**
```bash
tail -50 ~/x-token-automation/logs/refresh.log
```

**Common causes:**
- Refresh token expired → Run `x-token-init.py`
- Network error → Check internet
- X API error → Check X Developer Portal

### Timer Not Running

```bash
# Check status
systemctl --user status x-token-refresh.timer

# Enable
systemctl --user enable x-token-refresh.timer

# Start
systemctl --user start x-token-refresh.timer
```

---

## 📋 Maintenance

### Daily
- ✅ Automatic! No action needed

### Weekly
```bash
# Verify tokens work
x-token-verify.py

# Check for errors in logs
grep "❌" ~/x-token-automation/logs/refresh.log
```

### Monthly
```bash
# Test all slash commands
/post-x
/content-nuke
# etc.

# Review timer status
systemctl --user list-timers
```

---

## 🚨 Emergency Recovery

**If everything breaks:**

```bash
# 1. Stop timer
systemctl --user stop x-token-refresh.timer

# 2. Re-initialize from scratch
x-token-init.py

# 3. Distribute tokens
x-token-distribute.py

# 4. Verify working
x-token-verify.py

# 5. Restart timer
systemctl --user start x-token-refresh.timer
```

---

## ✅ Success Indicators

**System is working when:**
- ✅ Timer status shows "active (waiting)"
- ✅ Recent refresh logs show success
- ✅ `x-token-verify.py` returns 200 OK
- ✅ All slash commands post to X without errors
- ✅ No "invalid token" errors in logs

---

## 🎉 Benefits

### Before Automation:
- ❌ Tokens expire every 2 hours
- ❌ Manual refresh required
- ❌ Slash commands fail randomly
- ❌ No way to know when tokens expired
- ❌ Insecure plaintext token storage

### After Automation:
- ✅ Tokens refresh automatically every 90 min
- ✅ Zero manual intervention
- ✅ Slash commands always work
- ✅ Real-time monitoring via logs
- ✅ Encrypted pass storage
- ✅ Atomic distribution
- ✅ Comprehensive error handling

---

## 📂 Integration with Command Bible

**Location:** `/home/jeremy/x-token-automation/`

**Reference Files:**
- Complete system: `/home/jeremy/x-token-automation/README.md`
- This guide: `/home/jeremy/command-bible/x-token-automation-integration.md`
- X API commands: `/home/jeremy/command-bible/x-api-commands-reference.csv`
- Token refresh guide: `/home/jeremy/command-bible/x-api-token-refresh-guide.md`

---

## 🔗 Quick Links

**Run Commands:**
```bash
x-token-init.py          # Initial setup
x-token-refresh.py       # Manual refresh
x-token-distribute.py    # Distribute tokens
x-token-verify.py        # Verify tokens
```

**Manage Timer:**
```bash
systemctl --user enable x-token-refresh.timer   # Enable
systemctl --user start x-token-refresh.timer    # Start
systemctl --user status x-token-refresh.timer   # Check status
systemctl --user list-timers                    # List all timers
```

**View Logs:**
```bash
tail -f ~/x-token-automation/logs/refresh.log
tail -f ~/x-token-automation/logs/distribute.log
tail -f ~/x-token-automation/logs/verify.log
```

---

**Last Updated:** October 4, 2025
**Status:** ✅ Production Ready
**Automation:** ✅ Fully Automated
**Your slash commands will NEVER fail again! 🚀**
