#!/bin/bash
#
# Create Bob's Brain Google Cloud Project
# Run this once to set up Bob's dedicated infrastructure
#

set -e

PROJECT_ID="bobs-house-ai"
PROJECT_NAME="Bob's House AI"
BILLING_ACCOUNT_ID=$(gcloud billing accounts list --format="value(ACCOUNT_ID)" --limit=1)

echo "════════════════════════════════════════════════════════════"
echo "Bob's Brain - Google Cloud Project Setup"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Project ID: $PROJECT_ID"
echo "Project Name: $PROJECT_NAME"
echo "Billing Account: $BILLING_ACCOUNT_ID"
echo ""

# Create project
echo "📝 Creating project..."
gcloud projects create $PROJECT_ID --name="$PROJECT_NAME" || echo "Project already exists"

# Link billing
echo "💳 Linking billing account..."
gcloud billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT_ID

# Set as active project
echo "✅ Setting as active project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  cloudresourcemanager.googleapis.com

echo ""
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "  1. Store secrets: ./05-Scripts/deploy/store-secrets.sh"
echo "  2. Deploy Bob: ./05-Scripts/deploy/deploy-to-cloudrun.sh"
echo ""
