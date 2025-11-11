# LinkedIn API Setup Guide

Complete guide to setting up LinkedIn API for automated posting with Content Nuke. This setup will work persistently without needing frequent re-authentication.

## Prerequisites

- Active LinkedIn account (personal or business)
- Terminal/command line access
- Understanding of OAuth2 flow

## LinkedIn API Authentication Options

### Option 1: Long-Term Access Token (Recommended)
LinkedIn provides 60-day access tokens that can be refreshed automatically.

### Option 2: Company Page Integration
For posting to Intent Solutions company page instead of personal profile.

## Step-by-Step Setup

### Step 1: Create LinkedIn Developer App

1. **Navigate to:** https://www.linkedin.com/developers/
2. **Sign in** with your LinkedIn account
3. **Click "Create App"**

### Step 2: App Configuration

**App Details:**
- **App Name:** `Content Nuke Automation`
- **LinkedIn Page:** Select your company page (Intent Solutions) or create one
- **Privacy Policy URL:** `https://startaitools.com/privacy` (or your site)
- **App Logo:** Upload a logo (optional)

**Products to Request:**
- ✅ **Share on LinkedIn** (required for posting)
- ✅ **Sign In with LinkedIn** (required for authentication)

### Step 3: App Settings

**Auth Tab Configuration:**
- **Authorized Redirect URLs:** Add these URLs:
  ```
  https://localhost:8080/callback
  http://localhost:8080/callback
  https://startaitools.com/auth/linkedin
  ```

**Settings Tab:**
- Verify company association
- Note your **Client ID** and **Client Secret**

### Step 4: Get Long-Term Access Token

#### Method A: Using LinkedIn's Token Tool (Easiest)

1. **Go to Auth tab** in your LinkedIn app
2. **Generate access token** (valid for 60 days)
3. **Copy the access token** - this is your `LINKEDIN_ACCESS_TOKEN`

#### Method B: OAuth2 Flow (More Robust)

Use this Python script to get renewable tokens:

```python
#!/usr/bin/env python3
import requests
import urllib.parse

# Your app credentials
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
REDIRECT_URI = "http://localhost:8080/callback"

# Step 1: Get authorization URL
auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope=r_liteprofile%20w_member_social"

print("Visit this URL and authorize the app:")
print(auth_url)
print()

# Step 2: Get authorization code from callback
auth_code = input("Enter the 'code' parameter from the callback URL: ")

# Step 3: Exchange code for access token
token_url = "https://www.linkedin.com/oauth/v2/accessToken"
token_data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.post(token_url, data=token_data)
tokens = response.json()

print("Your tokens:")
print(f"Access Token: {tokens['access_token']}")
print(f"Expires in: {tokens['expires_in']} seconds")
```

### Step 5: Add Credentials to Waygate

Add these variables to `/home/jeremy/waygate-mcp/.env`:

```bash
# LinkedIn API Configuration
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_ACCESS_TOKEN=your_access_token_here
LINKEDIN_PERSON_ID=your_linkedin_user_id
```

### Step 6: Get Your LinkedIn User ID

Run this command to get your user ID:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     https://api.linkedin.com/v2/userinfo
```

The response contains your `sub` field - this is your `LINKEDIN_PERSON_ID`.

## Token Refresh Strategy

LinkedIn access tokens expire after 60 days. To avoid manual renewal:

### Option 1: Automatic Refresh (Recommended)

Add this refresh function to the LinkedIn script:

```python
def refresh_linkedin_token(refresh_token, client_id, client_secret):
    """Refresh LinkedIn access token"""
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        # Update .env file with new tokens
        return tokens['access_token']
    return None
```

### Option 2: 45-Day Renewal Reminder

Set a calendar reminder to renew tokens every 45 days (before expiration).

## Company Page Posting

To post to Intent Solutions company page instead of personal profile:

1. **Add company page** as administrator in LinkedIn
2. **Request additional permissions** in LinkedIn app:
   - `w_organization_social` (post on behalf of organization)
3. **Use organization URN** instead of person URN:
   ```python
   "author": f"urn:li:organization:{organization_id}"
   ```

## Testing Your Setup

### Test Connection
```bash
python3 content-nuke-claude/scripts/post_linkedin.py test
```

### Test Posting
```bash
echo "Test post from Content Nuke automation 🚀" > /tmp/test-linkedin.txt
python3 content-nuke-claude/scripts/post_linkedin.py /tmp/test-linkedin.txt
```

## Content Nuke Integration

Once setup is complete, Content Nuke will automatically:

1. **Generate LinkedIn content** optimized for business/professional audience
2. **Post to LinkedIn** using stored credentials
3. **Track posting** in analytics database
4. **Handle token refresh** automatically when needed

## Rate Limits & Best Practices

### LinkedIn API Limits
- **100 posts per day** per user
- **500 posts per day** per app
- **No monthly limits** for organic posts

### Best Practices
- **Business-focused content** performs better on LinkedIn
- **Professional tone** and achievements
- **Company updates** and technical innovations
- **Industry insights** and thought leadership

## Troubleshooting

### Common Issues

**"Invalid token" error:**
- Token expired (60-day limit)
- Regenerate access token in LinkedIn app

**"Insufficient privileges" error:**
- App needs "Share on LinkedIn" product
- Request additional permissions if needed

**"Invalid organization" error:**
- User not admin of company page
- Use personal profile instead

### Debug Commands

**Check token validity:**
```bash
curl -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
     https://api.linkedin.com/v2/userinfo
```

**Test posting permissions:**
```bash
curl -X POST https://api.linkedin.com/v2/ugcPosts \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

## Security Notes

- **Never commit tokens** to git repositories
- **Use environment variables** only
- **Regenerate tokens** if accidentally exposed
- **Monitor usage** in LinkedIn Developer Portal
- **60-day expiration** prevents long-term exposure

## Support Resources

- [LinkedIn API Documentation](https://docs.microsoft.com/en-us/linkedin/)
- [OAuth2 Implementation Guide](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow)
- [LinkedIn Developer Portal](https://www.linkedin.com/developers/)

---

**Once configured, LinkedIn posting will be fully automated with Content Nuke! 🚀**