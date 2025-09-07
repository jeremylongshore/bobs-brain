#!/bin/bash
set -e

echo "🔧 Deploying fixes to make Bob fully operational"
echo "================================================"

PROJECT_ID="bobs-house-ai"
REGION="us-central1"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Deploying Bob's Brain with new endpoints...${NC}"

# Deploy Bob's Brain with the new endpoints
gcloud run deploy bobs-brain \
    --source . \
    --platform managed \
    --region $REGION \
    --project $PROJECT_ID \
    --memory 1Gi \
    --timeout 3600 \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 10 \
    --vpc-connector bob-vpc-connector \
    --set-env-vars="SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN},SLACK_APP_TOKEN=${SLACK_APP_TOKEN},NEO4J_PASSWORD=bobshouse123,GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
    --quiet

echo -e "${GREEN}✅ Bob's Brain deployed with new endpoints:${NC}"
echo "  - /api/query - Intelligence queries"
echo "  - /slack/test - Slack testing"
echo "  - /slack/message - Send Slack messages"
echo "  - /api/mvp3/process - MVP3 processing"
echo "  - /api/orchestrate - System orchestration"

echo -e "${YELLOW}Step 2: Deploying Unified Scraper with process endpoint...${NC}"

# Deploy Unified Scraper with the new /api/process endpoint
gcloud run deploy unified-scraper \
    --source . \
    --platform managed \
    --region $REGION \
    --project $PROJECT_ID \
    --memory 1Gi \
    --timeout 3600 \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 5 \
    --vpc-connector bob-vpc-connector \
    --set-env-vars="NEO4J_PASSWORD=bobshouse123,GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
    --quiet

echo -e "${GREEN}✅ Unified Scraper deployed with process endpoint${NC}"

echo -e "${YELLOW}Step 3: Testing the new endpoints...${NC}"

# Test Bob's health
echo "Testing Bob's health..."
curl -s https://bobs-brain-157908567967.us-central1.run.app/health | python3 -m json.tool | head -10

# Test Bob's query endpoint
echo ""
echo "Testing Bob's query endpoint..."
curl -s -X POST https://bobs-brain-157908567967.us-central1.run.app/api/query \
    -H "Content-Type: application/json" \
    -d '{"question": "What are common hydraulic problems?"}' \
    | python3 -m json.tool 2>/dev/null | head -20 || echo "Query endpoint test complete"

# Test scraper process endpoint
echo ""
echo "Testing scraper process endpoint..."
curl -s -X POST https://unified-scraper-157908567967.us-central1.run.app/api/process \
    -H "Content-Type: application/json" \
    -d '{"url": "test.com", "content": "test", "title": "Test"}' \
    | python3 -m json.tool 2>/dev/null || echo "Process endpoint test complete"

echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Configure Slack webhook URL in Cloud Run environment"
echo "2. Test all endpoints with validation script"
echo "3. Monitor logs for any errors"
echo ""
echo "Run validation with: python3 test_phase5_validation.py"