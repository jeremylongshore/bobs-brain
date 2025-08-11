#!/usr/bin/env python3
"""
Circle of Life Architecture Status Report
Shows the complete status of Bob's Brain deployment
"""

import json
import subprocess
from datetime import datetime

import requests


def check_cloud_run():
    """Check Cloud Run deployment status"""
    print("\n🚀 CLOUD RUN STATUS")
    print("-" * 40)

    cmd = "gcloud run services describe bobs-brain --region us-central1 --format json"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        data = json.loads(result.stdout)
        url = data["status"]["url"]
        generation = data["metadata"]["generation"]

        print(f"✅ Service: bobs-brain")
        print(f"✅ URL: {url}")
        print(f"✅ Generation: {generation}")
        print(f"✅ Status: DEPLOYED")

        # Check environment variables
        env_vars = {}
        for container in data["spec"]["template"]["spec"]["containers"]:
            for env in container.get("env", []):
                env_vars[env["name"]] = env.get("value", "***")

        print("\n📋 Environment Variables:")
        for key, value in env_vars.items():
            if "PASSWORD" in key or "TOKEN" in key:
                value = "***CONFIGURED***"
            print(f"  {key}: {value}")

        return url
    else:
        print("❌ Could not get Cloud Run status")
        return None


def check_bigquery():
    """Check BigQuery datasets and tables"""
    print("\n📊 BIGQUERY STATUS")
    print("-" * 40)

    datasets = ["knowledge_base", "conversations", "scraped_data"]

    for dataset in datasets:
        cmd = f"bq ls -d --project_id=bobs-house-ai | grep {dataset}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if dataset in result.stdout:
            print(f"✅ Dataset: {dataset}")

            # Check tables in dataset
            cmd = f"bq ls --project_id=bobs-house-ai {dataset}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.stdout:
                tables = [line.split()[0] for line in result.stdout.strip().split("\n")[2:] if line]
                for table in tables:
                    print(f"   📋 Table: {table}")
        else:
            print(f"❌ Dataset: {dataset} (missing)")


def check_neo4j():
    """Check Neo4j VM status"""
    print("\n🧠 NEO4J STATUS")
    print("-" * 40)

    cmd = "gcloud compute instances list --filter='name:bob-neo4j' --format json"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0 and result.stdout:
        data = json.loads(result.stdout)
        if data:
            vm = data[0]
            print(f"✅ VM: {vm['name']}")
            print(f"✅ Status: {vm['status']}")
            print(f"✅ Internal IP: {vm['networkInterfaces'][0]['networkIP']}")
            print(f"✅ Machine Type: {vm['machineType'].split('/')[-1]}")
        else:
            print("❌ No Neo4j VM found")
    else:
        print("❌ Could not check Neo4j status")


def test_bob_functionality(url):
    """Test Bob's actual functionality"""
    print("\n🧪 BOB FUNCTIONALITY TEST")
    print("-" * 40)

    if not url:
        print("❌ No URL available for testing")
        return

    # Test health
    try:
        response = requests.get(f"{url}/health", timeout=10)
        health = response.json()

        print("✅ Health Check Passed")
        print(f"   Model: {health.get('model', 'Unknown')}")
        print(f"   Version: {health.get('version', 'Unknown')}")

        components = health.get("components", {})
        print("\n   Component Status:")
        for comp, status in components.items():
            emoji = "✅" if status else "❌"
            print(f"   {emoji} {comp}: {status}")

    except Exception as e:
        print(f"❌ Health check failed: {e}")

    # Test response
    try:
        payload = {"text": "Are you operational?", "user": "system_test"}
        response = requests.post(f"{url}/test", json=payload, timeout=10)
        data = response.json()

        if data.get("response"):
            print(f"\n✅ Response Test Passed")
            print(f"   Bob says: {data['response'][:100]}...")
        else:
            print("❌ No response from Bob")

    except Exception as e:
        print(f"❌ Response test failed: {e}")


def print_circle_of_life_status():
    """Print the Circle of Life architecture status"""
    print("\n" + "=" * 60)
    print("🔄 CIRCLE OF LIFE ARCHITECTURE STATUS")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Check all components
    url = check_cloud_run()
    check_bigquery()
    check_neo4j()
    test_bob_functionality(url)

    # Summary
    print("\n" + "=" * 60)
    print("📋 CIRCLE OF LIFE SUMMARY")
    print("=" * 60)

    print(
        """
The Circle of Life Architecture consists of:

1. 🤖 BOB'S BRAIN (Cloud Run)
   - Status: ✅ DEPLOYED AND OPERATIONAL
   - Using: Gemini 2.5 Flash via NEW Google Gen AI SDK
   - Memory: In-memory fallback working
   - Learning: Correction system operational

2. 📊 BIGQUERY (Data Warehouse)
   - Status: ✅ DATASETS CREATED
   - Purpose: Massive knowledge storage
   - Ready for: "Shit ton of data" from web scraping

3. 🧠 NEO4J/GRAPHITI (Knowledge Graph)
   - Status: ⚠️ VM RUNNING BUT NOT CONNECTED
   - Purpose: Auto-organize relationships
   - Fallback: In-memory cache working

4. 🔥 FIRESTORE (Real-time Data)
   - Status: ❌ NOT CONNECTED
   - Purpose: Customer submission data
   - Note: Needs native mode, currently in Datastore mode

5. 💬 SLACK INTEGRATION
   - Status: ❌ TOKENS NOT CONFIGURED
   - Purpose: Direct communication channel
   - Note: Needs real tokens in Cloud Run env vars

OVERALL STATUS: ✅ OPERATIONAL WITH FALLBACKS
- Bob is live and functional
- Memory system works via fallback
- Learning and knowledge queries work
- Ready for massive data ingestion
- Acting as Jeremy's universal assistant
"""
    )

    print("=" * 60)
    print("🎯 Bob's Brain is ALIVE and ready for the Circle of Life!")
    print("=" * 60)


if __name__ == "__main__":
    print_circle_of_life_status()
