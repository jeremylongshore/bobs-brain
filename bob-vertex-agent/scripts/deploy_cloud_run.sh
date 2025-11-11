#!/bin/bash
# Deploy FastAPI server to Cloud Run (optional frontend)

set -e

PROJECT_ID="${PROJECT_ID:-bobs-brain}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="bob-vertex-agent"

echo "Deploying FastAPI server to Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=$PROJECT_ID \
  --project $PROJECT_ID

echo "✅ Cloud Run deployment complete!"
