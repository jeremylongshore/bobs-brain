#!/usr/bin/env bash
# Deploy Bob's Brain FastAPI service to Cloud Run
#
# Required environment variables:
#   PROJECT_ID - GCP project ID
#   LOCATION - GCP region (default: us-central1)
#   SERVICE_NAME - Cloud Run service name (default: bobs-brain)
#   IMAGE - Container image URL
#   AGENT_ENGINE_ID - Deployed Agent Engine ID
#   SLACK_ENABLED - Enable Slack integration (default: false)
#   SLACK_BOT_TOKEN_SECRET - Secret Manager secret name for Slack bot token
#   SLACK_SIGNING_SECRET_SECRET - Secret Manager secret name for Slack signing secret

set -euo pipefail

# Required variables
: "${PROJECT_ID:?PROJECT_ID environment variable is required}"
: "${LOCATION:?LOCATION environment variable is required}"
: "${SERVICE_NAME:?SERVICE_NAME environment variable is required}"
: "${IMAGE:?IMAGE environment variable is required}"
: "${AGENT_ENGINE_ID:?AGENT_ENGINE_ID environment variable is required}"

# Optional variables
SLACK_ENABLED="${SLACK_ENABLED:-false}"
SLACK_BOT_TOKEN_SECRET="${SLACK_BOT_TOKEN_SECRET:-slack-bot-token}"
SLACK_SIGNING_SECRET_SECRET="${SLACK_SIGNING_SECRET_SECRET:-slack-signing-secret}"

echo "Deploying FastAPI service to Cloud Run..."
echo "  Project: $PROJECT_ID"
echo "  Region: $LOCATION"
echo "  Service: $SERVICE_NAME"
echo "  Image: $IMAGE"
echo "  Agent Engine ID: $AGENT_ENGINE_ID"
echo "  Slack Enabled: $SLACK_ENABLED"

# Build gcloud command with required env vars
DEPLOY_CMD="gcloud run deploy ${SERVICE_NAME} \
  --project ${PROJECT_ID} \
  --region ${LOCATION} \
  --image ${IMAGE} \
  --allow-unauthenticated \
  --set-env-vars RUN_MODE=service \
  --set-env-vars PROJECT_ID=${PROJECT_ID} \
  --set-env-vars LOCATION=${LOCATION} \
  --set-env-vars AGENT_ENGINE_ID=${AGENT_ENGINE_ID} \
  --set-env-vars SLACK_ENABLED=${SLACK_ENABLED}"

# Add Slack secrets if enabled
if [ "$SLACK_ENABLED" = "true" ]; then
  DEPLOY_CMD="$DEPLOY_CMD \
    --set-secrets SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN_SECRET}:latest \
    --set-secrets SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET_SECRET}:latest"
fi

# Execute deployment
eval "$DEPLOY_CMD"

echo "✅ Cloud Run deployment complete!"
echo ""
echo "Service URL:"
gcloud run services describe "${SERVICE_NAME}" \
  --region "${LOCATION}" \
  --project "${PROJECT_ID}" \
  --format 'value(status.url)'
