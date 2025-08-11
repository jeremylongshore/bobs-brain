#!/bin/bash
# Setup BigQuery for analytics while keeping Firestore for real-time

echo "Setting up BigQuery for DiagnosticPro analytics..."

# 1. Create BigQuery dataset
bq mk --dataset \
  --location=US \
  --description="DiagnosticPro customer analytics and ML" \
  bobs-house-ai:diagnosticpro_analytics

# 2. Create tables matching Firestore collections
bq mk --table \
  bobs-house-ai:diagnosticpro_analytics.diagnostic_submissions \
  vehicle_make:STRING,vehicle_model:STRING,vehicle_year:INTEGER,repair_type:STRING,quoted_price:FLOAT,fair_price:FLOAT,customer_email:STRING,timestamp:TIMESTAMP

bq mk --table \
  bobs-house-ai:diagnosticpro_analytics.repair_insights \
  shop_name:STRING,repair_type:STRING,average_overcharge:FLOAT,scam_probability:FLOAT

# 3. Set up automatic sync from Firestore to BigQuery
echo "Creating sync function..."

cat > sync_to_bigquery.py << 'EOF'
from google.cloud import firestore
from google.cloud import bigquery
import functions_framework

@functions_framework.cloud_event
def sync_to_bigquery(cloud_event):
    """Triggered by Firestore, syncs to BigQuery"""
    
    # Get the Firestore data
    firestore_data = cloud_event.data
    
    # Insert into BigQuery
    client = bigquery.Client()
    table = client.table('bobs-house-ai.diagnosticpro_analytics.diagnostic_submissions')
    
    row = {
        'vehicle_make': firestore_data.get('vehicle_make'),
        'vehicle_model': firestore_data.get('vehicle_model'),
        'quoted_price': firestore_data.get('quoted_price'),
        'timestamp': firestore_data.get('timestamp')
    }
    
    errors = client.insert_rows_json(table, [row])
    
    if errors:
        print(f"BigQuery insert error: {errors}")
    else:
        print(f"Synced to BigQuery: {row}")
EOF

# 4. Deploy the sync function
gcloud functions deploy sync-firestore-to-bigquery \
  --runtime python310 \
  --trigger-event providers/cloud.firestore/eventTypes/document.create \
  --trigger-resource "projects/diagnostic-pro-mvp/databases/bob-brain/documents/diagnostic_submissions/{docId}" \
  --entry-point sync_to_bigquery \
  --source . \
  --project bobs-house-ai

echo "✅ BigQuery setup complete!"
echo ""
echo "Now you have:"
echo "1. Firestore: Real-time customer submissions"
echo "2. BigQuery: Analytics and ML on all data"
echo "3. Automatic sync: Every new submission goes to both"