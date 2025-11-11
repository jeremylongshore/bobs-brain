#!/bin/bash
#
# Store Bob's Brain Secrets in Google Secret Manager
# Run this after creating the project
#

set -e

PROJECT_ID="bobs-house-ai"

echo "════════════════════════════════════════════════════════════"
echo "Bob's Brain - Store Secrets in Secret Manager"
echo "════════════════════════════════════════════════════════════"
echo ""

# Load .env file
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found"
    echo "Run this script from the bobs-brain directory"
    exit 1
fi

source .env

echo "Storing Slack credentials..."
echo ""

# Store Slack credentials
echo "📝 Storing SLACK_BOT_TOKEN..."
echo -n "$SLACK_BOT_TOKEN" | gcloud secrets create slack-bot-token \
  --project=$PROJECT_ID \
  --data-file=- \
  --replication-policy=automatic || \
  echo -n "$SLACK_BOT_TOKEN" | gcloud secrets versions add slack-bot-token \
  --project=$PROJECT_ID \
  --data-file=-

echo "📝 Storing SLACK_SIGNING_SECRET..."
echo -n "$SLACK_SIGNING_SECRET" | gcloud secrets create slack-signing-secret \
  --project=$PROJECT_ID \
  --data-file=- \
  --replication-policy=automatic || \
  echo -n "$SLACK_SIGNING_SECRET" | gcloud secrets versions add slack-signing-secret \
  --project=$PROJECT_ID \
  --data-file=-

# Store LLM API key (user needs to add this to .env first)
if [ -n "$GOOGLE_API_KEY" ]; then
    echo "📝 Storing GOOGLE_API_KEY..."
    echo -n "$GOOGLE_API_KEY" | gcloud secrets create google-api-key \
      --project=$PROJECT_ID \
      --data-file=- \
      --replication-policy=automatic || \
      echo -n "$GOOGLE_API_KEY" | gcloud secrets versions add google-api-key \
      --project=$PROJECT_ID \
      --data-file=-
else
    echo "⚠️  GOOGLE_API_KEY not set in .env - skipping"
    echo "   Add your API key to .env and re-run this script"
fi

# Generate and store BB_API_KEY
echo "📝 Generating and storing BB_API_KEY..."
BB_API_KEY=$(openssl rand -hex 32)
echo -n "$BB_API_KEY" | gcloud secrets create bb-api-key \
  --project=$PROJECT_ID \
  --data-file=- \
  --replication-policy=automatic || \
  echo -n "$BB_API_KEY" | gcloud secrets versions add bb-api-key \
  --project=$PROJECT_ID \
  --data-file=-

echo ""
echo "✅ All secrets stored in Secret Manager!"
echo ""
echo "Generated BB_API_KEY: $BB_API_KEY"
echo "Save this key - you'll need it for API requests"
echo ""
echo "Next step: Deploy to Cloud Run"
echo "  ./05-Scripts/deploy/deploy-to-cloudrun.sh"
echo ""
