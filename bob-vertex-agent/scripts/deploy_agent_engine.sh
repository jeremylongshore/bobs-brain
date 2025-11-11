#!/bin/bash
# Deploy agent to Vertex AI Agent Engine

set -e

PROJECT_ID="${PROJECT_ID:-bobs-brain}"
REGION="${REGION:-us-central1}"

echo "Deploying to Vertex AI Agent Engine..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

# Use existing Makefile deployment
cd "$(dirname "$0")/.."
make deploy

echo "✅ Agent Engine deployment complete!"
