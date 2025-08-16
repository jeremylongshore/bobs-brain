# Reddit API Setup Instructions

## Step 1: Create Reddit App

1. Go to: https://www.reddit.com/prefs/apps
2. Log in with your Reddit account
3. Click "Create App" or "Create Another App"
4. Fill in:
   - **Name:** BobsBrainScraper
   - **App type:** Select **"script"**
   - **Description:** Equipment repair knowledge aggregator
   - **About URL:** (leave blank)
   - **Redirect URI:** http://localhost:8080
5. Click "Create app"

## Step 2: Save Your Credentials

After creating, you'll see:
- **Client ID:** (14-character string under "personal use script")
- **Client Secret:** (27-character string)

## Step 3: Set Environment Variables in Cloud Run

Run these commands with your actual credentials:

```bash
# Set Reddit API credentials for unified-scraper
gcloud run services update unified-scraper \
  --set-env-vars "REDDIT_CLIENT_ID=YOUR_CLIENT_ID_HERE" \
  --set-env-vars "REDDIT_CLIENT_SECRET=YOUR_SECRET_HERE" \
  --region us-central1

# Also update bob's brain if needed
gcloud run services update bobs-brain \
  --set-env-vars "REDDIT_CLIENT_ID=YOUR_CLIENT_ID_HERE" \
  --set-env-vars "REDDIT_CLIENT_SECRET=YOUR_SECRET_HERE" \
  --region us-central1
```

## Step 4: Public Sources We'll Focus On

### ✅ No Login Required:
- Reddit (with API key)
- RSS feeds (Diesel Progress, Equipment World, etc.)
- YouTube transcripts (public videos)
- Manufacturer blogs/news (public)

### ❌ Will Skip (Login Required):
- Heavy Equipment Forums (requires account)
- Bobcat Forum (requires dealer login)
- TractorByNet (requires membership)
- Private Facebook groups

## Test After Setup

```bash
# Test the scraper manually
curl -X POST https://unified-scraper-157908567967.us-central1.run.app/scrape/quick \
  -H "Content-Type: application/json" \
  -d '{}' --max-time 30
```
