# X (Twitter) API Setup Guide

Complete guide to setting up X (Twitter) API for automated thread posting. Works with any blog automation system or personal use.

## Prerequisites

- Active X (Twitter) account
- Terminal/command line access
- Basic understanding of environment variables

## Free Tier Overview

The X API Free tier is perfect for blog automation:
- **1,500 tweets per month** (plenty for daily posting)
- **50 tweets per day** rate limit
- **Read and write** permissions
- **$0 cost**

## Step-by-Step Setup

### Step 1: Apply for Developer Account

1. **Navigate to:** https://developer.twitter.com/en/portal/dashboard
2. **Sign in** with your X/Twitter account
3. **Click "Sign up for Free Account"**

### Step 2: Application Form

Complete the application with these responses:

**What's your primary reason for using the Twitter API?**
- Select: **"Building tools for personal use"**

**Please describe how you plan to use Twitter data and/or APIs:**
```
I plan to use the Twitter API to automate posting threads that promote my blog content. This will include:

1. Posting Twitter threads that summarize my blog posts
2. Sharing insights and updates from my content
3. Cross-promoting content between my blog and Twitter
4. All content will be original and created by me

The use case is personal automation for content marketing of my blog.
```

**Will you analyze Twitter data?**
- Select: **"No"**

**Will you use Twitter data for government purposes?**
- Select: **"No"**

**Do you plan to display Tweets outside of Twitter?**
- Select: **"No"**

### Step 3: Wait for Approval

- **Approval time:** Usually instant, sometimes 1-2 hours
- **Check email** for approval notification
- **Personal use cases** are typically approved quickly

### Step 4: Create Project

Once approved:

1. **Click "Create Project"**
2. **Project Name:** `Blog Automation`
3. **Use Case:** Select **"Making a bot"**
4. **Project Description:**
   ```
   Automated posting of Twitter threads to promote blog content and personal updates.
   ```

### Step 5: Create App

1. **App Name:** `blog-automation-poster`
2. **App Description:**
   ```
   Automated Twitter thread posting for blog content promotion
   ```

### Step 6: Save Your Credentials

**CRITICAL:** Save these 3 keys immediately when shown:

1. **API Key** (Consumer Key)
2. **API Secret** (Consumer Secret)
3. **Bearer Token**

### Step 7: Generate Access Tokens

1. **Navigate to "Keys and tokens" tab**
2. **Click "Generate" under "Access Token and Secret"**
3. **Save these additional credentials:**
   - **Access Token**
   - **Access Token Secret**

### Step 8: Configure Permissions ⚠️ CRITICAL

1. **Go to "Settings" tab**
2. **Under "App permissions"** click **"Edit"**
3. **Select "Read and write"**
4. **Save changes**
5. **IMPORTANT: Regenerate access tokens after changing permissions**

**⚠️ Common Issue:** If you get "oauth1-permissions" errors when posting tweets, your app needs **Elevated access**. Apply for Elevated access (still free) in your developer portal.

**Access Levels:**
- **Essential** (default): Read-only operations, bearer token only
- **Elevated** (free): Read/write operations, OAuth 1.0a posting, higher rate limits

## Environment Configuration

### Add Credentials to Shell

Edit your shell configuration file:

```bash
nano ~/.bashrc
```

Add these environment variables (replace with your actual keys):

```bash
# X (Twitter) API Credentials
export X_API_KEY="your_api_key_here"
export X_API_SECRET="your_api_secret_here"
export X_BEARER_TOKEN="your_bearer_token_here"
export X_ACCESS_TOKEN="your_access_token_here"
export X_ACCESS_SECRET="your_access_secret_here"
```

### Reload Configuration

```bash
source ~/.bashrc
```

## Test Your Setup

### Basic Connection Test

Create and run a test script:

```bash
cat > /tmp/test-x-api.sh << 'EOF'
#!/bin/bash
echo "Testing X API connection..."

if [ -z "$X_BEARER_TOKEN" ]; then
  echo "❌ X_BEARER_TOKEN not set"
  echo "Add your credentials to ~/.bashrc first"
  exit 1
fi

echo "✅ Bearer token found"
echo "Testing API connection..."

response=$(curl -s "https://api.twitter.com/2/users/me" \
  -H "Authorization: Bearer $X_BEARER_TOKEN")

if echo "$response" | grep -q '"id"'; then
  echo "🎉 API connection successful!"
  echo "Your X account info:"
  echo "$response" | jq .
else
  echo "❌ API connection failed"
  echo "Response: $response"
fi
EOF

chmod +x /tmp/test-x-api.sh
/tmp/test-x-api.sh
```

### Expected Success Output

```
Testing X API connection...
✅ Bearer token found
Testing API connection...
🎉 API connection successful!
Your X account info:
{
  "data": {
    "id": "123456789",
    "name": "Your Name",
    "username": "yourusername"
  }
}
```

## Using with Automation Tools

Once API is configured, you can integrate with various automation systems:

### Manual Testing
```bash
# Test posting a single tweet
curl -X POST "https://api.twitter.com/2/tweets" \
  -H "Authorization: Bearer $X_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from my automation setup!"}'
```

### Integration Options
- **Blog automation tools**
- **Social media schedulers**
- **Custom scripts and applications**
- **CI/CD pipeline integrations**

### Common Use Cases
- **Blog post promotion threads**
- **Automated content sharing**
- **Social media cross-posting**
- **Personal update broadcasting**

## Rate Limits & Best Practices

### Free Tier Limits
- **1,500 tweets/month** total
- **50 tweets/day** maximum
- **300 requests per 15 minutes**

### Recommended Usage
- **1-2 posts per day** = ~3-10 tweets
- **Weekly content** = ~7-15 tweets
- **Monthly usage:** ~100-300 tweets (well under limit)

### Best Practices
- **Test with single tweets first**
- **Monitor your usage** in X Developer Portal
- **Save content locally** before posting
- **Have manual fallback ready** (copy-paste option)

## Troubleshooting

### Common Issues

**"oauth1-permissions" error when posting:**
- Your app needs Elevated access (not just Essential)
- Apply for Elevated access in Developer Portal (still free)
- Regenerate access tokens after getting Elevated access
- Essential access only allows read operations

**"Unknown app" error:**
- Ensure app permissions are set to "Read and write"
- Regenerate access tokens if needed

**Rate limit exceeded:**
- Wait 15 minutes before retry
- Check monthly usage in Developer Portal

**Invalid credentials:**
- Verify all 5 environment variables are set
- Check for extra spaces or quotes in credentials

**Connection refused:**
- Test with basic curl command first
- Verify network connectivity to api.twitter.com

### Debug Commands

**Check environment variables:**
```bash
echo "API Key: ${X_API_KEY:0:10}..."
echo "Bearer Token: ${X_BEARER_TOKEN:0:15}..."
```

**Test basic API call:**
```bash
curl -s "https://api.twitter.com/2/users/me" \
  -H "Authorization: Bearer $X_BEARER_TOKEN" | jq .
```

**Verify write permissions:**
```bash
curl -X POST "https://api.twitter.com/2/tweets" \
  -H "Authorization: Bearer $X_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test tweet from Claude AutoBlog API"}' | jq .
```

## Manual Fallback

Even without API setup, you can still automate content creation:

1. **Generate content** using your preferred tools
2. **Save threads to files** for manual posting
3. **Copy-paste** each tweet to X manually
4. **Include posting instructions** in saved files

## Security Notes

- **Never commit API keys** to git repositories
- **Use environment variables** only
- **Regenerate keys** if accidentally exposed
- **Monitor usage** in X Developer Portal
- **Rate limits protect** against abuse

## Support

### X API Documentation
- [Twitter API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Rate Limits Guide](https://developer.twitter.com/en/docs/twitter-api/rate-limits)
- [Authentication Guide](https://developer.twitter.com/en/docs/authentication/overview)

### Additional Resources
- [Twitter API Community Forum](https://twittercommunity.com/)
- [API Status Page](https://api.twitterstat.us/)
- [Developer Best Practices](https://developer.twitter.com/en/docs/developer-utilities/rate-limit-chart)

---

**Ready to automate?** Use this guide to set up X API access for your blog automation needs!