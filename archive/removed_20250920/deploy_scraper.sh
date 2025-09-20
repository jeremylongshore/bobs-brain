#!/bin/bash

# Deploy Circle of Life Scraper to Cloud Run
# Runs overnight to gather Bobcat S740 knowledge

set -e

PROJECT_ID="bobs-house-ai"
REGION="us-central1"
SERVICE_NAME="circle-of-life-scraper"

echo "🚀 Deploying Circle of Life Scraper..."

# Build and push container
echo "📦 Building container..."
gcloud builds submit \
    --project $PROJECT_ID \
    --config cloudbuild-scraper.yaml \
    --timeout=30m \
    .

# Deploy to Cloud Run as a service (for scheduled jobs)
echo "☁️ Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --project $PROJECT_ID \
    --region $REGION \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --max-instances 1 \
    --min-instances 0 \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --project $PROJECT_ID \
    --region $REGION \
    --format 'value(status.url)')

echo "✅ Scraper deployed at: $SERVICE_URL"

# Create service account for scheduler
echo "👤 Setting up service account..."
gcloud iam service-accounts create circle-of-life-scheduler \
    --project $PROJECT_ID \
    --display-name "Circle of Life Scheduler" \
    2>/dev/null || echo "Service account already exists"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:circle-of-life-scheduler@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

# Set up Cloud Scheduler job
echo "⏰ Setting up Cloud Scheduler..."
gcloud scheduler jobs create http overnight-scraper \
    --project $PROJECT_ID \
    --location $REGION \
    --schedule="0 2 * * *" \
    --time-zone="America/Chicago" \
    --uri="$SERVICE_URL/scrape" \
    --http-method=POST \
    --headers="Content-Type=application/json" \
    --message-body='{"scrape_type":"overnight"}' \
    --oidc-service-account-email="circle-of-life-scheduler@$PROJECT_ID.iam.gserviceaccount.com" \
    --oidc-token-audience="$SERVICE_URL" \
    2>/dev/null || echo "Scheduler job already exists"

echo "
✅ Circle of Life Scraper Deployment Complete!
============================================
Service URL: $SERVICE_URL
Schedule: Daily at 2:00 AM CST
Focus: Bobcat S740 and compact equipment

Test the scraper:
curl -X POST $SERVICE_URL/scrape \\
    -H 'Content-Type: application/json' \\
    -d '{\"scrape_type\":\"test\"}'

Check today's insights:
curl $SERVICE_URL/insights/today

Search S740 knowledge:
curl '$SERVICE_URL/search/s740?q=hydraulic'

The scraper will run automatically tonight at 2 AM!
"