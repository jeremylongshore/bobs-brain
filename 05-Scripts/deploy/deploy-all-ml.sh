#!/bin/bash
# Deploy BOTH ML systems using your GCP credits

echo "🚀 Deploying Bob's Complete ML System"
echo "Using your $2,251 GCP credits"
echo ""

# 1. Deploy BigQuery ML (Fast & Cheap)
echo "📊 Setting up BigQuery ML models..."
python3 deploy_bigquery_ml.py
echo "✅ BigQuery ML ready (~$5/month from credits)"
echo ""

# 2. Deploy Vertex AI AutoML (Accurate & Powerful)
echo "🤖 Setting up Vertex AI AutoML..."
python3 official_automl_setup.py
echo "✅ AutoML ready (~$20/model from credits)"
echo ""

# 3. Update Bob to use both
echo "🧠 Updating Bob's Brain to use both ML systems..."
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --project bobs-house-ai \
  --image gcr.io/bobs-house-ai/bob-gcp-latest:latest \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "USE_BIGQUERY_ML=true,USE_AUTOML=true"

echo ""
echo "🎉 COMPLETE! Bob now has:"
echo "  1. BigQuery ML for fast predictions"
echo "  2. Vertex AI AutoML for accurate predictions"
echo "  3. Both covered by your credits"
echo ""
echo "Monthly cost: ~$50-75 (you have 30+ months of credits!)"
echo ""
echo "Test it:"
echo "curl https://bobs-brain-157908567967.us-central1.run.app/predict"
