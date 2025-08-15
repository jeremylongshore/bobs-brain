#!/bin/bash
# Setup BigQuery ML and AutoML models using your GCP credits

echo "🤖 Setting up ML models with your FREE GCP credits..."

# 1. Enable required APIs (covered by credits)
echo "Enabling APIs..."
gcloud services enable bigquery.googleapis.com \
  automl.googleapis.com \
  aiplatform.googleapis.com \
  --project bobs-house-ai

# 2. Create BigQuery dataset for ML models
echo "Creating ML dataset..."
bq mk --dataset \
  --location=US \
  --description="ML models for Bob's Brain" \
  bobs-house-ai:ml_models

# 3. Create price prediction model (BigQuery ML - uses credits)
echo "Training price prediction model..."
bq query --use_legacy_sql=false '
CREATE OR REPLACE MODEL `bobs-house-ai.ml_models.repair_price_predictor`
OPTIONS(
  model_type="linear_reg",
  input_label_cols=["quoted_price"]
) AS
SELECT
  vehicle_make,
  vehicle_model,
  vehicle_year,
  repair_type,
  quoted_price
FROM `bobs-house-ai.scraped_data.repair_quotes`
WHERE quoted_price IS NOT NULL'

# 4. Create scam detection model (BigQuery ML - uses credits)
echo "Training scam detection model..."
bq query --use_legacy_sql=false '
CREATE OR REPLACE MODEL `bobs-house-ai.ml_models.scam_shop_detector`
OPTIONS(
  model_type="logistic_reg",
  input_label_cols=["is_overcharge"]
) AS
SELECT
  shop_name,
  repair_type,
  quoted_price,
  parts_cost,
  labor_cost,
  IF(quoted_price > (parts_cost + labor_cost) * 1.5, TRUE, FALSE) as is_overcharge
FROM `bobs-house-ai.scraped_data.repair_quotes`
WHERE parts_cost IS NOT NULL AND labor_cost IS NOT NULL'

# 5. Create clustering model to find shop patterns (BigQuery ML)
echo "Training shop clustering model..."
bq query --use_legacy_sql=false '
CREATE OR REPLACE MODEL `bobs-house-ai.ml_models.shop_clusters`
OPTIONS(
  model_type="kmeans",
  num_clusters=5
) AS
SELECT
  shop_name,
  AVG(quoted_price) as avg_price,
  COUNT(*) as num_quotes,
  AVG(quoted_price - parts_cost - labor_cost) as avg_profit_margin
FROM `bobs-house-ai.scraped_data.repair_quotes`
GROUP BY shop_name'

# 6. Create AutoML dataset (uses credits but more powerful)
echo "Setting up AutoML dataset..."
cat > create_automl_dataset.py << 'EOF'
from google.cloud import aiplatform

aiplatform.init(project='bobs-house-ai', location='us-central1')

# Create AutoML dataset
dataset = aiplatform.TabularDataset.create(
    display_name="repair_quotes_automl",
    bq_source="bq://bobs-house-ai.scraped_data.repair_quotes"
)

print(f"Created AutoML dataset: {dataset.resource_name}")
print("You can now train AutoML models in the console!")
EOF

python3 create_automl_dataset.py

echo ""
 echo "✅ ML MODELS SETUP COMPLETE!"
echo ""
echo "📊 BigQuery ML Models Created (using credits):"
echo "  - repair_price_predictor: Predicts fair repair prices"
echo "  - scam_shop_detector: Identifies overcharging shops"
echo "  - shop_clusters: Groups shops by behavior patterns"
echo ""
echo "🤖 AutoML Dataset Ready (using credits):"
echo "  - Go to: https://console.cloud.google.com/vertex-ai/datasets"
echo "  - Click 'repair_quotes_automl' to train models"
echo ""
echo "💰 COST COVERED BY YOUR $2,251 CREDITS:"
echo "  - BigQuery ML: ~$5/month"
echo "  - AutoML Training: ~$20 per model"
echo "  - Model Predictions: ~$0.001 per 1000 predictions"
echo "  - Total: <$50/month (you have 45+ months of credits!)"
