# AI Model Monitor - Complete GitHub Setup

**Status**: Workflow Idea - To Be Implemented
**Date Saved**: 2025-10-03
**Category**: Monitoring & Alerts

---

## 📋 Prerequisites (Get These First)

Before starting, obtain these two items:

### 1. Anthropic API Key
1. Go to https://console.anthropic.com/settings/keys
2. Log in to your Anthropic account
3. Click "Create Key"
4. Copy the key (starts with `sk-ant-`)
5. **Save it somewhere safe** - you can only see it once!

### 2. Slack Webhook URL
1. Go to https://api.slack.com/messaging/webhooks
2. Click "Create your Slack app"
3. Choose "From scratch"
4. Name it "AI Release Monitor" and select your workspace
5. Click "Incoming Webhooks" → Toggle "Activate Incoming Webhooks" to ON
6. Click "Add New Webhook to Workspace"
7. Select the channel for notifications
8. Copy the webhook URL (starts with `https://hooks.slack.com/services/`)

---

## 🚀 Part 1: Create GitHub Repository

### Option A: Via GitHub Website

1. Go to https://github.com and sign in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in:
   - **Repository name:** `ai-model-monitor`
   - **Description:** "Automated AI model release tracker"
   - **Visibility:** Public or Private (your choice)
   - **✓ Check:** "Add a README file"
4. Click **"Create repository"**

### Option B: Via Command Line

```bash
# Create directory
mkdir ai-model-monitor
cd ai-model-monitor

# Initialize git
git init

# Create README
echo "# AI Model Release Monitor" > README.md

# First commit
git add README.md
git commit -m "Initial commit"

# Create repo on GitHub (requires GitHub CLI)
gh repo create ai-model-monitor --public --source=. --remote=origin --push
```

---

## 🔐 Part 2: Add GitHub Secrets

### Step-by-Step:

1. **Go to your repository** on GitHub
2. Click **"Settings"** tab (top right)
3. In left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"** (green button)

### Add Secret #1: Anthropic API Key
- **Name:** `ANTHROPIC_API_KEY`
- **Secret:** Paste your Anthropic key (the one starting with `sk-ant-`)
- Click **"Add secret"**

### Add Secret #2: Slack Webhook
- Click **"New repository secret"** again
- **Name:** `SLACK_WEBHOOK_URL`
- **Secret:** Paste your Slack webhook URL
- Click **"Add secret"**

**✅ You should now see 2 secrets listed**

---

## 📁 Part 3: Create Project Files

You'll create 4 files in your repository. Here's how:

### Method A: Via GitHub Web Interface

#### File 1: Create Workflow Directory and File

1. In your repo, click **"Add file"** → **"Create new file"**
2. In the filename box, type: `.github/workflows/monitor.yml`
   - (Typing the slashes will create the folders automatically)
3. Paste this content:

```yaml
name: AI Model Release Monitor

on:
  schedule:
    - cron: '0 0,12 * * *'  # 12 AM & 12 PM UTC
  workflow_dispatch:         # Manual trigger button

jobs:
  monitor:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install axios @anthropic-ai/sdk

      - name: Run AI model monitor
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: node scripts/analyze.js

      - name: Send completion notification
        if: always()
        run: |
          curl -X POST "${{ secrets.SLACK_WEBHOOK_URL }}" \
          -H 'Content-Type: application/json' \
          -d "{\"text\":\"✅ AI Model Monitor completed at $(date)\"}"
```

4. Click **"Commit changes"**
5. Add commit message: "Add workflow file"
6. Click **"Commit changes"** again

#### File 2: Create Analysis Script

1. Click **"Add file"** → **"Create new file"**
2. Filename: `scripts/analyze.js`
3. Paste this content:

```javascript
const Anthropic = require('@anthropic-ai/sdk');
const axios = require('axios');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const PROVIDERS = {
  'OpenAI': 'https://platform.openai.com/docs/changelog',
  'Anthropic': 'https://www.anthropic.com/news',
  'Google Gemini': 'https://ai.google.dev/gemini-api/docs/changelog',
  'Meta': 'https://ai.meta.com/blog/',
  'Alibaba Qwen': 'https://qwenlm.github.io/',
  'xAI Grok': 'https://x.ai/blog',
  'Mistral': 'https://mistral.ai/news/',
  'Cohere': 'https://cohere.com/blog'
};

async function fetchContent(url) {
  try {
    const response = await axios.get(url, {
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; AIModelMonitor/1.0)'
      }
    });
    return response.data.substring(0, 50000); // Limit content size
  } catch (error) {
    console.error(`Error fetching ${url}:`, error.message);
    return null;
  }
}

async function analyzeWithClaude(content, provider) {
  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 1024,
      messages: [{
        role: 'user',
        content: `You are monitoring ${provider} for new AI model releases, updates, and pricing changes.

Analyze this recent content and determine:
1. Are there any NEW model releases, updates, or pricing changes? (be specific)
2. Rate the importance from 1-10 (10 = major new model launch, 1 = minor update)
3. Provide a brief summary (2-3 sentences max)

If nothing new or relevant is found, respond with: "NO_NEW_RELEASES"

Content preview:
${content.substring(0, 10000)}`
      }]
    });

    return message.content[0].text;
  } catch (error) {
    console.error(`Error analyzing with Claude:`, error.message);
    return 'ERROR: Could not analyze content';
  }
}

async function sendToSlack(message) {
  try {
    await axios.post(process.env.SLACK_WEBHOOK_URL, {
      text: message,
      unfurl_links: false,
      unfurl_media: false
    });
    console.log('Slack notification sent');
  } catch (error) {
    console.error('Error sending to Slack:', error.message);
  }
}

async function createGitHubIssue(provider, analysis, importance) {
  try {
    const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');

    await axios.post(
      `https://api.github.com/repos/${owner}/${repo}/issues`,
      {
        title: `[${provider}] New AI Model Release Detected`,
        body: `## Analysis\n\n${analysis}\n\n---\n\n**Importance Rating:** ${importance}/10\n**Detected:** ${new Date().toISOString()}`,
        labels: ['ai-release', `importance-${importance}`, provider.toLowerCase().replace(/\s+/g, '-')]
      },
      {
        headers: {
          'Authorization': `token ${process.env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'User-Agent': 'AI-Model-Monitor'
        }
      }
    );
    console.log(`GitHub issue created for ${provider}`);
  } catch (error) {
    console.error(`Error creating GitHub issue:`, error.message);
  }
}

async function main() {
  console.log('🔍 Starting AI Model Release Monitor...');
  console.log(`📅 Time: ${new Date().toISOString()}`);

  let foundNewReleases = false;

  for (const [provider, url] of Object.entries(PROVIDERS)) {
    console.log(`\n📡 Checking ${provider}...`);

    const content = await fetchContent(url);
    if (!content) {
      console.log(`⚠️  Could not fetch content from ${provider}`);
      continue;
    }

    console.log(`✓ Content fetched, analyzing with Claude...`);
    const analysis = await analyzeWithClaude(content, provider);

    if (analysis.includes('NO_NEW_RELEASES')) {
      console.log(`✓ No new releases detected for ${provider}`);
      continue;
    }

    console.log(`🎉 NEW RELEASE DETECTED for ${provider}!`);
    foundNewReleases = true;

    // Extract importance rating
    const importanceMatch = analysis.match(/importance.*?(\d+)/i);
    const importance = importanceMatch ? parseInt(importanceMatch[1]) : 5;

    // Send Slack notification
    const slackMessage = `🚀 *${provider} - New Release Detected*\n\n${analysis}\n\n_Importance: ${importance}/10_`;
    await sendToSlack(slackMessage);

    // Create GitHub issue for important releases (7+)
    if (importance >= 7) {
      await createGitHubIssue(provider, analysis, importance);
    }

    // Rate limiting
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  if (!foundNewReleases) {
    console.log('\n✅ Monitor completed - no new releases detected');
  } else {
    console.log('\n✅ Monitor completed - notifications sent!');
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
```

4. Click **"Commit changes"** → Add message → **"Commit changes"**

#### File 3: Create package.json

1. Click **"Add file"** → **"Create new file"**
2. Filename: `package.json`
3. Paste this content:

```json
{
  "name": "ai-model-monitor",
  "version": "1.0.0",
  "description": "Automated AI model release tracker",
  "main": "scripts/analyze.js",
  "scripts": {
    "start": "node scripts/analyze.js"
  },
  "dependencies": {
    "@anthropic-ai/sdk": "^0.32.1",
    "axios": "^1.7.9"
  }
}
```

4. Click **"Commit changes"**

#### File 4: Create .gitignore

1. Click **"Add file"** → **"Create new file"**
2. Filename: `.gitignore`
3. Paste this content:

```
node_modules/
.env
.DS_Store
*.log
```

4. Click **"Commit changes"**

---

## ✅ Part 4: Enable and Test

### Enable GitHub Actions

1. Go to your repo's **"Actions"** tab
2. If you see "Get started with GitHub Actions", click **"I understand my workflows, go ahead and enable them"**
3. You should now see **"AI Model Release Monitor"** workflow

### Test the Workflow (Manual Run)

1. In the Actions tab, click **"AI Model Release Monitor"** (left sidebar)
2. Click **"Run workflow"** button (right side)
3. Click the green **"Run workflow"** button in the dropdown
4. Wait 30-60 seconds, then refresh the page
5. Click on the workflow run to see progress
6. Check your Slack channel for notifications!

### View Workflow Status

- ✅ Green checkmark = Success
- ❌ Red X = Failed (click to see error logs)
- 🟡 Yellow circle = Running

---

## 🔧 Troubleshooting

### Workflow fails with "Error: Cannot find module"
**Fix:** Make sure `package.json` was created correctly

### No Slack notifications
**Fix:**
1. Verify webhook URL is correct in secrets
2. Test webhook manually:
```bash
curl -X POST 'YOUR_WEBHOOK_URL' \
-H 'Content-Type: application/json' \
-d '{"text":"Test from command line"}'
```

### "Resource not accessible by integration" error
**Fix:** Go to Settings → Actions → General → Workflow permissions → Select "Read and write permissions"

### Rate limiting errors
**Fix:** The script includes 2-second delays between providers. Increase this if needed.

---

## 🎯 Next Steps

Once everything is working:

1. **Check the schedule:** The workflow runs automatically at 12 AM and 12 PM UTC
2. **Monitor issues:** GitHub will auto-create issues for important releases (rated 7+)
3. **Customize providers:** Edit `scripts/analyze.js` to add/remove providers
4. **Adjust timing:** Edit the cron schedule in `monitor.yml`

---

## 📊 Verification Checklist

- [ ] Repository created
- [ ] 2 secrets added (ANTHROPIC_API_KEY, SLACK_WEBHOOK_URL)
- [ ] 4 files created (monitor.yml, analyze.js, package.json, .gitignore)
- [ ] GitHub Actions enabled
- [ ] Manual test run successful
- [ ] Slack notification received
- [ ] No error messages in workflow logs

**You're done! 🎉** The monitor will now run automatically twice daily.

---

## 💡 Potential n8n Implementation

This could be converted to an n8n workflow with:

### Workflow Structure
```
Schedule Trigger (12 AM, 12 PM)
  ↓
HTTP Requests (fetch provider pages)
  ↓
Loop over providers
  ↓
Claude AI Node (analyze content)
  ↓
IF Node (check for new releases)
  ↓
Slack Node (send notification)
  ↓
GitHub Node (create issue if importance >= 7)
```

### Required n8n Nodes
- **Schedule Trigger** - Cron: `0 0,12 * * *`
- **HTTP Request** - Fetch provider pages
- **Loop Over Items** - Process each provider
- **Anthropic Claude** - AI analysis
- **IF** - Check for new releases
- **Slack** - Send webhook notifications
- **GitHub** - Create issues
- **Code** - Custom JavaScript for data processing

### Benefits of n8n Version
- Visual workflow editor
- No GitHub Actions required
- Can run on your own server
- Easier to modify and test
- Better error handling UI

---

**Date Saved**: 2025-10-03
**Status**: Ready to implement as GitHub Actions or n8n workflow
