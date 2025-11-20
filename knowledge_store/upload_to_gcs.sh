#!/bin/bash
# Upload ADK Documentation to GCS for Vertex AI Grounding

set -e

PROJECT_ID="bobs-brain"
BUCKET_NAME="bobs-brain-knowledge"  # Using EXISTING knowledge bucket - NO NEW BUCKETS!

echo "Uploading ADK documentation to EXISTING GCS bucket..."

# DO NOT create new bucket - use existing one
echo "Using existing bucket: gs://$BUCKET_NAME"

# Upload all documentation with proper metadata
gsutil -m cp -r knowledge_store/* gs://$BUCKET_NAME/adk-grounding/

# Set metadata for searchability
gsutil -m setmeta -h "Content-Type:text/html" gs://$BUCKET_NAME/adk-grounding/tools/*.html
gsutil -m setmeta -h "Content-Type:text/html" gs://$BUCKET_NAME/adk-grounding/custom-tools/*.html
gsutil -m setmeta -h "Content-Type:text/html" gs://$BUCKET_NAME/adk-grounding/gcp-tools/*.html
gsutil -m setmeta -h "Content-Type:application/pdf" gs://$BUCKET_NAME/adk-grounding/research/*.pdf

echo "Upload complete!"
echo "Documents available at: gs://$BUCKET_NAME/adk-grounding/"
