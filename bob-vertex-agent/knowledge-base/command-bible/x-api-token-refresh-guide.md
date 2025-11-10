# X API Token Refresh Guide
**For Slash Commands Using X/Twitter API**

**Created:** October 4, 2025
**Issue:** OAuth token refresh failures in slash commands

---

## 🚨 Commands Affected by X API Token Issues

### Commands That Post to X (5 Total):

1. **`/content-nuke`** - Multi-platform blast
2. **`/blog-single-startai`** - Technical blog + X thread
3. **`/blog-both-x`** - Both blogs + X thread
4. **`/blog-jeremy-x`** - Portfolio blog + X thread
5. **`/post-x`** - Direct X posting

---

## 🔧 Token Refresh Configuration

### Current OAuth Setup:

**OAuth Type:** OAuth 2.0 with PKCE
**Token Storage:** Waygate MCP `.env` file
**Credentials Location:** `/home/jeremy/waygate-mcp/.env`

**Required Environment Variables:**
```bash
X_CLIENT_ID="your_client_id"
X_CLIENT_SECRET="your_client_secret"
X_OAUTH2_ACCESS_TOKEN="your_access_token"
X_OAUTH2_REFRESH_TOKEN="your_refresh_token"
```

---

## 🔄 Token Refresh Methods

### Method 1: Automatic Refresh (Recommended)

**Script:** `/home/jeremy/projects/content-nuke/scripts/refresh_tokens.py`

```bash
# Refresh X tokens automatically
python3 /home/jeremy/projects/content-nuke/scripts/refresh_tokens.py x

# Check token status
cat /home/jeremy/waygate-mcp/.env | grep X_OAUTH2_ACCESS_TOKEN
```

### Method 2: Manual Waygate MCP Refresh

```bash
# Navigate to Waygate MCP
cd /home/jeremy/waygate-mcp

# Check current token status
docker-compose logs -f waygate | grep -i oauth

# Restart Waygate to force token refresh
docker-compose restart waygate
```

### Method 3: Re-authenticate (Last Resort)

```bash
# Run OAuth setup script
cd /home/jeremy/projects/content-nuke/content-nuke-claude/scripts
python3 oauth2_pkce_setup.py

# Follow prompts to re-authenticate
# Copy new tokens to waygate-mcp/.env
```

---

## 🐛 Common Token Issues & Solutions

### Issue 1: "Invalid or expired token" Error

**Symptoms:**
- Command fails with 401 Unauthorized
- "Token has been revoked" message

**Solution:**
```bash
# Run automatic refresh
python3 /home/jeremy/projects/content-nuke/scripts/refresh_tokens.py x

# Verify new token is in waygate-mcp/.env
grep X_OAUTH2_ACCESS_TOKEN /home/jeremy/waygate-mcp/.env
```

---

### Issue 2: Rate Limiting (429 Error)

**Symptoms:**
- "Too many requests" error
- Commands work then fail after multiple uses

**Solution:**
```bash
# Wait 15 minutes before retrying
# Check rate limit status
curl -H "Authorization: Bearer $X_OAUTH2_ACCESS_TOKEN" \
  https://api.twitter.com/2/tweets/rate_limit_status

# Use /post-x less frequently (max 3-5 per hour)
```

---

### Issue 3: Token Not Synced Between Scripts

**Symptoms:**
- refresh_tokens.py updates token
- Slash commands still use old token

**Solution:**
```bash
# Ensure all scripts read from waygate-mcp/.env
# Update token in waygate-mcp/.env manually if needed

# Verify token location
ls -la /home/jeremy/waygate-mcp/.env

# Check if scripts are reading correct .env
grep "load_dotenv" /home/jeremy/projects/content-nuke/scripts/post_x_thread.py
```

---

### Issue 4: Refresh Token Expired

**Symptoms:**
- Can't refresh access token
- "Invalid refresh token" error

**Solution:**
```bash
# Re-authenticate completely
cd /home/jeremy/projects/content-nuke/content-nuke-claude/scripts
python3 oauth2_pkce_setup.py

# Save new tokens to waygate-mcp/.env
# Update both ACCESS_TOKEN and REFRESH_TOKEN
```

---

## 📋 Pre-Flight Checklist Before Running X Commands

Before running `/content-nuke`, `/blog-single-startai`, `/blog-both-x`, `/blog-jeremy-x`, or `/post-x`:

- [ ] Check token is valid: `grep X_OAUTH2_ACCESS_TOKEN /home/jeremy/waygate-mcp/.env`
- [ ] Verify waygate-mcp is running: `docker ps | grep waygate`
- [ ] Check for recent token refresh errors in logs
- [ ] Ensure rate limits not exceeded (max 3-5 posts per hour)
- [ ] Test with `/post-x` first before running multi-platform commands

---

## 🔍 Token Debugging Commands

```bash
# View current X API tokens (masked)
cat /home/jeremy/waygate-mcp/.env | grep X_OAUTH2 | sed 's/=.*/=***MASKED***/'

# Check waygate-mcp logs for OAuth errors
docker-compose -f /home/jeremy/waygate-mcp/docker-compose.yml logs -f waygate | grep -i oauth

# Test X API connectivity
curl -X GET "https://api.twitter.com/2/users/me" \
  -H "Authorization: Bearer $(grep X_OAUTH2_ACCESS_TOKEN /home/jeremy/waygate-mcp/.env | cut -d'=' -f2)"

# View token expiration (if available)
python3 -c "import jwt; print(jwt.decode(open('/home/jeremy/waygate-mcp/.env').read().split('X_OAUTH2_ACCESS_TOKEN=')[1].split()[0], options={'verify_signature': False}))"
```

---

## 📊 X API Command Usage Matrix

| Command | Uses X API? | Token Type | Auto-Refresh? | Fallback Method |
|---------|-------------|------------|---------------|-----------------|
| `/content-nuke` | ✅ Yes | OAuth 2.0 | Via refresh_tokens.py | Manual re-auth |
| `/blog-single-startai` | ✅ Yes | OAuth 2.0 | Via refresh_tokens.py | Manual re-auth |
| `/blog-both-x` | ✅ Yes | OAuth 2.0 | Via refresh_tokens.py | Manual re-auth |
| `/blog-jeremy-x` | ✅ Yes | OAuth 2.0 | Via refresh_tokens.py | Manual re-auth |
| `/post-x` | ✅ Yes | OAuth 2.0 | Via refresh_tokens.py | Manual re-auth |
| `/blog-startaitools` | ❌ No | N/A | N/A | N/A |
| `/blog-jeremylongshore` | ❌ No | N/A | N/A | N/A |

---

## 🔐 Security Best Practices

1. **Never commit tokens to git**
   - Always use `.env` files
   - Add `.env` to `.gitignore`

2. **Rotate tokens regularly**
   - Refresh tokens monthly
   - Re-authenticate if suspicious activity

3. **Monitor token usage**
   - Check waygate-mcp logs weekly
   - Track API rate limits

4. **Use Waygate MCP for centralized token storage**
   - Single source of truth for OAuth tokens
   - Automatic token refresh capabilities
   - Secure container-based isolation

---

## 📞 Emergency Token Recovery

If all else fails and you can't post to X:

1. **Stop all X API commands immediately**
2. **Re-authenticate from scratch:**
   ```bash
   cd /home/jeremy/projects/content-nuke/content-nuke-claude/scripts
   python3 oauth2_pkce_setup.py
   ```
3. **Update waygate-mcp/.env with new tokens**
4. **Restart waygate:**
   ```bash
   cd /home/jeremy/waygate-mcp
   docker-compose restart waygate
   ```
5. **Test with `/post-x` before using multi-platform commands**

---

## 📅 Maintenance Schedule

**Weekly:**
- Check token expiration status
- Review X API usage and rate limits
- Test `/post-x` to verify connectivity

**Monthly:**
- Refresh OAuth tokens proactively
- Review waygate-mcp logs for errors
- Update token refresh scripts if needed

**As Needed:**
- Re-authenticate if tokens expire
- Update OAuth credentials if X API changes
- Fix token sync issues between scripts

---

## 📂 Related Files

**Token Storage:**
- `/home/jeremy/waygate-mcp/.env` - OAuth tokens (DO NOT COMMIT)

**Refresh Scripts:**
- `/home/jeremy/projects/content-nuke/scripts/refresh_tokens.py` - Automatic refresh
- `/home/jeremy/projects/content-nuke/content-nuke-claude/scripts/oauth2_pkce_setup.py` - Re-authentication

**Posting Scripts:**
- `/home/jeremy/projects/content-nuke/scripts/post_x_thread.py` - Thread posting

**Documentation:**
- `/home/jeremy/projects/content-nuke/content-nuke-claude/docs/X_API_SETUP.md` - Setup guide
- `/home/jeremy/projects/content-nuke/content-nuke-claude/docs/X_OAUTH_API_REFERENCE.md` - API reference

---

**Last Updated:** October 4, 2025
**Next Review:** November 4, 2025
