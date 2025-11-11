#!/bin/bash
#
# Deploy Bob's Brain to Google Cloud Run
# Run this after storing secrets
#

set -e

PROJECT_ID="bobs-house-ai"
SERVICE_NAME="bobs-brain"
REGION="us-central1"

echo "════════════════════════════════════════════════════════════"
echo "Bob's Brain - Deploy to Cloud Run"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo ""

cd ~/projects/bobs-brain

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --allow-unauthenticated \
  --set-env-vars "PROVIDER=google,MODEL=gemini-2.0-flash,STATE_BACKEND=sqlite,VECTOR_BACKEND=chroma,GRAPH_BACKEND=none,CACHE_BACKEND=none,ARTIFACT_BACKEND=local" \
  --set-secrets \
    SLACK_BOT_TOKEN=slack-bot-token:latest,\
    SLACK_SIGNING_SECRET=slack-signing-secret:latest,\
    GOOGLE_API_KEY=google-api-key:latest,\
    BB_API_KEY=bb-api-key:latest

echo ""
echo "✅ Deployment complete!"
echo ""

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --project $PROJECT_ID \
  --region $REGION \
  --format="value(status.url)")

echo "Service URL: $SERVICE_URL"
echo ""
echo "Test health endpoint:"
echo "  curl $SERVICE_URL/health"
echo ""
echo "Configure Slack Event Subscriptions:"
echo "  1. Go to: https://api.slack.com/apps/A099YKLCM1N/event-subscriptions"
echo "  2. Request URL: $SERVICE_URL/slack/events"
echo "  3. Subscribe to bot events: message.channels, message.groups, message.im, app_mention"
echo "  4. Save Changes"
echo ""
