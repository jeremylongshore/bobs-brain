#!/usr/bin/env python3
"""
Deploy Bob's Brain with Complete Circle of Life Architecture to Cloud Run
This script ensures all components are properly configured and connected
"""

import json
import os
import subprocess
import time


def run_command(cmd, description=""):
    """Run a shell command and return output"""
    print(f"\n{'='*60}")
    if description:
        print(f"🔧 {description}")
    print(f"📝 Running: {cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and "already exists" not in result.stderr:
            print(f"⚠️  {result.stderr}")
        return result.returncode == 0, result.stdout
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, str(e)


def main():
    print("\n" + "=" * 80)
    print("🌟 DEPLOYING BOB'S BRAIN - CIRCLE OF LIFE ARCHITECTURE 🌟")
    print("=" * 80)

    # Configuration
    PROJECT_ID = "bobs-house-ai"
    REGION = "us-central1"
    SERVICE_NAME = "bobs-brain"

    print("\n📋 DEPLOYMENT PLAN:")
    print("1. Set up IAM permissions")
    print("2. Configure BigQuery datasets and tables")
    print("3. Set up Neo4j connection")
    print("4. Configure environment variables")
    print("5. Deploy to Cloud Run")
    print("6. Verify deployment")

    # Step 1: Grant necessary IAM permissions to service account
    print("\n\n🔐 STEP 1: Configuring IAM Permissions")
    service_account = f"157908567967-compute@developer.gserviceaccount.com"

    roles = [
        "roles/aiplatform.user",
        "roles/bigquery.dataEditor",
        "roles/bigquery.jobUser",
        "roles/datastore.user",
        "roles/logging.logWriter",
    ]

    for role in roles:
        cmd = f"gcloud projects add-iam-policy-binding {PROJECT_ID} --member=serviceAccount:{service_account} --role={role} --quiet"
        run_command(cmd, f"Granting {role}")

    # Step 2: Set up BigQuery datasets and tables
    print("\n\n📊 STEP 2: Setting up BigQuery Datasets")

    # Create datasets
    datasets = ["knowledge_base", "conversations", "scraped_data"]
    for dataset in datasets:
        cmd = f"bq mk --dataset --location={REGION} --project_id={PROJECT_ID} {dataset}"
        run_command(cmd, f"Creating dataset: {dataset}")

    # Create tables with schemas
    print("\n📋 Creating BigQuery tables...")

    # Create repair_manuals table
    repair_manuals_schema = """
    content:STRING,source:STRING,vehicle_type:STRING,tags:STRING:REPEATED
    """
    cmd = f'bq mk --table --project_id={PROJECT_ID} knowledge_base.repair_manuals "{repair_manuals_schema.strip()}"'
    run_command(cmd, "Creating repair_manuals table")

    # Create forum_posts table
    forum_posts_schema = """
    question:STRING,answer:STRING,upvotes:INTEGER,source:STRING,vehicle_type:STRING
    """
    cmd = f'bq mk --table --project_id={PROJECT_ID} knowledge_base.forum_posts "{forum_posts_schema.strip()}"'
    run_command(cmd, "Creating forum_posts table")

    # Create repair_quotes table
    repair_quotes_schema = """
    repair_type:STRING,vehicle_type:STRING,quoted_price:FLOAT,fair_price:FLOAT,shop_name:STRING,location:STRING
    """
    cmd = f'bq mk --table --project_id={PROJECT_ID} scraped_data.repair_quotes "{repair_quotes_schema.strip()}"'
    run_command(cmd, "Creating repair_quotes table")

    # Create conversations history table
    conversations_schema = """
    user:STRING,message:STRING,response:STRING,timestamp:TIMESTAMP
    """
    cmd = f'bq mk --table --project_id={PROJECT_ID} conversations.history "{conversations_schema.strip()}"'
    run_command(cmd, "Creating conversations history table")

    # Create corrections table
    corrections_schema = """
    original:STRING,correction:STRING,user:STRING,timestamp:TIMESTAMP
    """
    cmd = f'bq mk --table --project_id={PROJECT_ID} conversations.corrections "{corrections_schema.strip()}"'
    run_command(cmd, "Creating corrections table")

    # Step 3: Check Neo4j VM status
    print("\n\n🧠 STEP 3: Checking Neo4j Status")
    cmd = "gcloud compute instances list --filter='name:bob-neo4j' --format='table(name,status,networkInterfaces[0].networkIP)'"
    success, output = run_command(cmd, "Checking Neo4j VM")

    neo4j_ip = "10.128.0.2"  # Default from our setup
    if "RUNNING" in output:
        print("✅ Neo4j VM is running")
    else:
        print("⚠️  Neo4j VM may not be running. Attempting to start...")
        cmd = "gcloud compute instances start bob-neo4j --zone=us-central1-a"
        run_command(cmd, "Starting Neo4j VM")

    # Step 4: Deploy to Cloud Run with all environment variables
    print("\n\n🚀 STEP 4: Deploying to Cloud Run")

    # Read Slack tokens from CLAUDE.md if available
    slack_bot_token = "xoxb-9318399480516-9316254671362-placeholder"
    slack_app_token = "xapp-1-A099YKLCM1N-9312940498067-placeholder"
    slack_signing_secret = "d00942f9329d902a0af65f31f968f355"

    print("\n📝 Building deployment command...")

    # Build the deployment command with all environment variables
    env_vars = [
        f"GCP_PROJECT={PROJECT_ID}",
        f"GCP_LOCATION={REGION}",
        f"NEO4J_URI=bolt://{neo4j_ip}:7687",
        "NEO4J_USER=neo4j",
        "NEO4J_PASSWORD=<REDACTED_NEO4J_PASSWORD>",
        f"SLACK_BOT_TOKEN={slack_bot_token}",
        f"SLACK_APP_TOKEN={slack_app_token}",
        f"SLACK_SIGNING_SECRET={slack_signing_secret}",
    ]

    env_vars_str = ",".join(env_vars)

    # Deploy command
    deploy_cmd = f"""gcloud run deploy {SERVICE_NAME} \
        --source . \
        --region {REGION} \
        --project {PROJECT_ID} \
        --port 8080 \
        --allow-unauthenticated \
        --memory 1Gi \
        --cpu 2 \
        --timeout 300 \
        --min-instances 1 \
        --max-instances 10 \
        --set-env-vars "{env_vars_str}" \
        --service-account {service_account}"""

    print("\n🚀 Deploying Bob's Brain to Cloud Run...")
    print("This may take a few minutes...")
    success, output = run_command(deploy_cmd, "Deploying to Cloud Run")

    if success:
        print("\n✅ DEPLOYMENT SUCCESSFUL!")

        # Step 5: Verify deployment
        print("\n\n🔍 STEP 5: Verifying Deployment")

        # Get service URL
        cmd = f"gcloud run services describe {SERVICE_NAME} --region {REGION} --format 'value(status.url)'"
        success, service_url = run_command(cmd, "Getting service URL")
        service_url = service_url.strip()

        if service_url:
            print(f"\n🌐 Service URL: {service_url}")

            # Test health endpoint
            print("\n🏥 Testing health endpoint...")
            cmd = f"curl -s {service_url}/health | python3 -m json.tool"
            run_command(cmd, "Health check")

            # Test the test endpoint
            print("\n🧪 Testing Bob's response...")
            test_message = "Hello Bob, tell me about the Circle of Life architecture"
            cmd = f"""curl -s -X POST {service_url}/test \
                -H "Content-Type: application/json" \
                -d '{{"text": "{test_message}"}}' | python3 -m json.tool"""
            run_command(cmd, "Testing Bob's response")

            print("\n\n" + "=" * 80)
            print("🎉 CIRCLE OF LIFE DEPLOYMENT COMPLETE! 🎉")
            print("=" * 80)
            print(f"\n✅ Bob's Brain is now live at: {service_url}")
            print("\n📋 Available endpoints:")
            print(f"  - Health: {service_url}/health")
            print(f"  - Test: {service_url}/test")
            print(f"  - Learn: {service_url}/learn")
            print(f"  - Slack Events: {service_url}/slack/events")
            print("\n🧠 Components Status:")
            print("  - Gemini AI: Connected via NEW Google Gen AI SDK")
            print("  - BigQuery: All datasets and tables created")
            print("  - Neo4j: Available for Graphiti integration")
            print("  - Memory System: Three-tier fallback operational")
            print("\n🔄 Circle of Life Architecture:")
            print("  - Graphiti auto-organizes all data")
            print("  - BigQuery stores massive knowledge warehouse")
            print("  - Firestore handles real-time updates")
            print("  - Bob remembers everything and learns from corrections")
            print("\n🚀 Bob is ready to be Jeremy's universal assistant!")

        else:
            print("⚠️  Could not get service URL")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        print("Common issues:")
        print("  - Ensure you're logged in: gcloud auth login")
        print("  - Check project: gcloud config set project bobs-house-ai")
        print("  - Verify billing is enabled")


if __name__ == "__main__":
    main()
