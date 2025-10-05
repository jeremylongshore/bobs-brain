#!/bin/bash
set -e

echo "🚀 Deploying Phase 5: Complete Ecosystem Integration"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ID="bobs-house-ai"
REGION="us-central1"

echo -e "${YELLOW}Step 1: Building Docker image for ecosystem integration...${NC}"
cat > Dockerfile.ecosystem << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir \
    google-cloud-aiplatform \
    neo4j \
    aiohttp

# Copy application code
COPY src/ecosystem_integration.py .
COPY src/ ./src/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run the ecosystem integration
CMD ["python", "ecosystem_integration.py"]
EOF

# Build the image
docker build -f Dockerfile.ecosystem -t ecosystem-integration .

echo -e "${YELLOW}Step 2: Pushing image to Container Registry...${NC}"
docker tag ecosystem-integration gcr.io/$PROJECT_ID/ecosystem-integration
docker push gcr.io/$PROJECT_ID/ecosystem-integration

echo -e "${YELLOW}Step 3: Running ecosystem integration as Cloud Run Job...${NC}"
gcloud run jobs create ecosystem-integration-phase5 \
    --image gcr.io/$PROJECT_ID/ecosystem-integration \
    --region $REGION \
    --memory 2Gi \
    --max-retries 1 \
    --parallelism 1 \
    --task-timeout 30m \
    --vpc-connector bob-vpc-connector \
    --set-env-vars="NEO4J_PASSWORD=$(gcloud secrets versions access latest --secret=neo4j-password)" \
    --service-account bobs-brain@$PROJECT_ID.iam.gserviceaccount.com

echo -e "${YELLOW}Step 4: Executing the integration job...${NC}"
gcloud run jobs execute ecosystem-integration-phase5 \
    --region $REGION \
    --wait

echo -e "${GREEN}✅ Phase 5 deployment initiated!${NC}"
echo "Check the logs with:"
echo "  gcloud run jobs executions logs --region $REGION"

# Also update Bob's Brain with orchestrator capabilities
echo -e "${YELLOW}Step 5: Updating Bob's Brain with orchestrator capabilities...${NC}"
cat > update_bob_orchestrator.py << 'EOF'
import requests
import json

# Update Bob with orchestrator configuration
config = {
    "mode": "orchestrator",
    "monitoring": {
        "neo4j": True,
        "bigquery": True,
        "scrapers": True,
        "mvp3": True
    },
    "automation": {
        "new_submission_alerts": True,
        "knowledge_updates": True,
        "system_health_checks": True
    }
}

response = requests.post(
    "https://bobs-brain-157908567967.us-central1.run.app/api/configure",
    json=config
)

print(f"Bob orchestrator update: {response.status_code}")
EOF

python3 update_bob_orchestrator.py

echo -e "${GREEN}✅ Phase 5: Complete Ecosystem Integration Deployed!${NC}"
echo ""
echo "🎉 Bob is now the operational heart of the system!"
echo ""
echo "Next steps:"
echo "1. Monitor the integration job logs"
echo "2. Check StartAITools.com dashboard"
echo "3. Verify Bob's Slack responses"
echo "4. Test customer submission flow"