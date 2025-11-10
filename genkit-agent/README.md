# Bob's Brain - Vertex AI Agent (Genkit 2)

**Status:** 🚧 In Development (Feature Branch)
**Branch:** `feature/vertex-ai-genkit-migration`
**GCP Project:** `bobs-brain`

---

## Overview

This is the **new Vertex AI-native version** of Bob's Brain, built with:
- **Genkit 2** - Google's AI agent framework
- **Vertex AI** - Gemini 2.0 Flash (free tier, 8K tokens)
- **Firestore** - State management
- **Cloud Storage** - Knowledge base documents
- **Vertex AI Search** - Grounded responses from knowledge
- **Secret Manager** - Slack credentials & secrets
- **GitHub Actions** - Automated deployment

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Bob's Brain Vertex AI Agent              │
├─────────────────────────────────────────────────┤
│  Genkit 2 Flow (bobAgent)                       │
│    ├── Gemini 2.0 Flash (Vertex AI)             │
│    ├── Vertex AI Search (knowledge grounding)   │
│    └── Firestore (conversation state)           │
└────────────┬────────────────────────────────────┘
             │
    ┌────────▼─────────┐
    │  Cloud Functions  │ (HTTP trigger)
    │  (Gen 2)          │
    └────────┬─────────┘
             │
    ┌────────▼─────────┐
    │   Slack Events    │ (/slack/events webhook)
    │   API             │
    └──────────────────┘
```

---

## Setup

### 1. Install Dependencies
```bash
cd genkit-agent
npm install
```

### 2. Build TypeScript
```bash
npm run build
```

### 3. Local Development
```bash
npm run dev
# Starts Genkit dev UI at http://localhost:4000
```

### 4. Deploy to Google Cloud
```bash
npm run deploy
# OR use GitHub Actions (push to feature branch)
```

---

## Environment Variables

Stored in **Google Secret Manager**:
- `slack-bot-token` - Slack Bot OAuth Token
- `slack-signing-secret` - Slack Signing Secret
- `slack-app-id` - Slack App ID

Cloud Functions automatically loads these via `--set-secrets` flag.

---

## API Endpoints

### Main Agent Endpoint
```bash
POST https://us-central1-bobs-brain.cloudfunctions.net/bob-agent
Content-Type: application/json

{
  "query": "What is the meaning of life?",
  "userId": "U12345",
  "context": {}
}
```

### Slack Webhook
```bash
POST https://us-central1-bobs-brain.cloudfunctions.net/bob-agent/slack/events
```

---

## GitHub Actions Deployment

**Workflow:** `.github/workflows/deploy-vertex-ai.yml`

**Triggers:**
- Push to `main`
- Push to `feature/vertex-ai-genkit-migration`
- Manual workflow dispatch

**Steps:**
1. Checkout code
2. Install Node.js dependencies
3. Build TypeScript
4. Authenticate to GCP (Workload Identity)
5. Deploy to Cloud Functions (Gen 2)

---

## Project Structure

```
genkit-agent/
├── src/
│   └── index.ts          # Main Genkit agent flow
├── dist/                 # Compiled JavaScript (git ignored)
├── package.json          # Dependencies & scripts
├── tsconfig.json         # TypeScript config
└── README.md             # This file
```

---

## Key Features

### 1. Gemini 2.0 Flash
- Free tier usage
- 8,192 max output tokens
- Multimodal capabilities

### 2. Vertex AI Search
- Grounded responses from Cloud Storage documents
- Automatic indexing and search
- Real-time knowledge updates

### 3. Slack Integration
- Event subscriptions (mentions, DMs, channels)
- Signature verification
- Conversation memory via Firestore

### 4. GitHub Actions CI/CD
- Automated testing and deployment
- Secure GCP authentication (Workload Identity)
- Deploy on every push

---

## Development Commands

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Run local development server
npm run dev

# Deploy to Cloud Functions
npm run deploy

# Run in production mode
npm start
```

---

## Configuration

### GCP Project Settings
- **Project ID:** `bobs-brain`
- **Region:** `us-central1`
- **Service:** Cloud Functions (Gen 2)
- **Runtime:** Node.js 20

### Slack App
- **App ID:** `A099YKLCM1N`
- **Event Subscriptions:** message.channels, message.im, app_mention
- **Webhook URL:** Will be updated after deployment

---

## Next Steps

1. ✅ GCP project created
2. ✅ APIs enabled
3. ✅ Genkit agent initialized
4. ✅ GitHub Actions workflow created
5. ⏳ Set up Vertex AI Search datastore
6. ⏳ Create Slack webhook Cloud Function
7. ⏳ Migrate knowledge base to Cloud Storage
8. ⏳ Test end-to-end flow
9. ⏳ Deploy to production

---

## Resources

- **Genkit Docs:** https://firebase.google.com/docs/genkit
- **Vertex AI:** https://cloud.google.com/vertex-ai
- **Cloud Functions:** https://cloud.google.com/functions
- **Slack API:** https://api.slack.com/apps/A099YKLCM1N

---

**Last Updated:** 2025-11-09
**Status:** Ready for Vertex AI Search setup
