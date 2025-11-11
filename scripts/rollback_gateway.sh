#!/usr/bin/env bash
#
# Rollback Cloud Run Gateway to Previous Revision
#
# This script rolls back the gateway to the previous stable revision.
# Use this when a deployment causes issues and you need to quickly revert.
#
# Usage:
#   PROJECT_ID=my-project REGION=us-central1 bash scripts/rollback_gateway.sh
#   make rollback  # Uses current gcloud project
#
# Environment Variables:
#   PROJECT_ID: GCP project ID (required)
#   REGION: GCP region (default: us-central1)
#   SERVICE: Cloud Run service name (default: bobs-brain-gateway)
#

set -euo pipefail

# Configuration
: "${PROJECT_ID:?ERROR: PROJECT_ID environment variable is required}"
: "${REGION:=us-central1}"
: "${SERVICE:=bobs-brain-gateway}"

echo "=================================================="
echo "Cloud Run Gateway Rollback"
echo "=================================================="
echo "Project:  $PROJECT_ID"
echo "Region:   $REGION"
echo "Service:  $SERVICE"
echo ""

# Get current traffic distribution
echo "Fetching current traffic distribution..."
CURRENT_TRAFFIC=$(gcloud run services describe "$SERVICE" \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --format="value(status.traffic.revisionName,status.traffic.percent)")

echo "Current traffic:"
echo "$CURRENT_TRAFFIC"
echo ""

# Get the current latest revision (the one serving 100% or most traffic)
CURRENT_REVISION=$(gcloud run services describe "$SERVICE" \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --format="value(status.latestReadyRevisionName)")

echo "Current latest revision: $CURRENT_REVISION"

# Get all revisions ordered by creation time (newest first)
echo ""
echo "Available revisions:"
gcloud run revisions list \
  --service="$SERVICE" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --format="table(metadata.name,status.conditions[0].lastTransitionTime,spec.containers[0].image)" \
  --limit=5

echo ""

# Get the previous revision (second in list, skipping latest)
PREVIOUS_REVISION=$(gcloud run revisions list \
  --service="$SERVICE" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --format="value(metadata.name)" \
  --limit=2 | tail -n 1)

if [ -z "$PREVIOUS_REVISION" ]; then
  echo "ERROR: No previous revision found. Cannot rollback."
  echo "This might be the first deployment, or all old revisions were pruned."
  exit 1
fi

if [ "$PREVIOUS_REVISION" == "$CURRENT_REVISION" ]; then
  echo "ERROR: Previous revision is the same as current revision."
  echo "No rollback available."
  exit 1
fi

echo "Target rollback revision: $PREVIOUS_REVISION"
echo ""
echo "⚠️  WARNING: This will shift 100% traffic to $PREVIOUS_REVISION"
read -p "Continue with rollback? (yes/no): " -r CONFIRM

if [ "$CONFIRM" != "yes" ]; then
  echo "Rollback cancelled."
  exit 0
fi

echo ""
echo "Rolling back to $PREVIOUS_REVISION..."

gcloud run services update-traffic "$SERVICE" \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --to-revisions "${PREVIOUS_REVISION}=100"

echo ""
echo "✅ Rollback complete!"
echo ""
echo "Verification:"
echo "- Dashboard: https://console.cloud.google.com/run/detail/$REGION/$SERVICE?project=$PROJECT_ID"
echo "- Health: curl https://\$(gcloud run services describe $SERVICE --region $REGION --format='value(status.url)')/_health"
echo ""
echo "Current traffic distribution:"
gcloud run services describe "$SERVICE" \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --format="table(status.traffic.revisionName,status.traffic.percent)"
