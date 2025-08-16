#!/usr/bin/env python3
"""
Debug Bob's Brain - Comprehensive diagnostics
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta

import requests
from google.cloud import logging, monitoring_v3
from google.cloud.monitoring_dashboard import v1


def check_health():
    """Check Bob's health endpoint"""
    print("\n=== CHECKING BOB'S HEALTH ===")
    try:
        response = requests.get("https://bobs-brain-sytrh5wz5q-uc.a.run.app/health", timeout=10)
        health = response.json()
        print(f"Status: {health.get('status')}")
        print(f"Model: {health.get('model')}")
        print(f"Components:")
        for component, status in health.get('components', {}).items():
            emoji = "✅" if status else "❌"
            print(f"  {emoji} {component}: {status}")
        return health
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return None


def test_slack_webhook():
    """Test Slack event endpoint"""
    print("\n=== TESTING SLACK WEBHOOK ===")
    
    # URL verification test
    test_data = {
        "type": "url_verification",
        "challenge": "test_challenge_123"
    }
    
    try:
        response = requests.post(
            "https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events",
            json=test_data,
            timeout=10
        )
        print(f"URL Verification: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Slack webhook test failed: {e}")
        return False


def test_chat():
    """Test Bob's chat endpoint"""
    print("\n=== TESTING CHAT ENDPOINT ===")
    
    test_message = {
        "message": "Hello Bob, what's the current date and time?",
        "user": "debug_test"
    }
    
    try:
        response = requests.post(
            "https://bobs-brain-sytrh5wz5q-uc.a.run.app/chat",
            json=test_message,
            timeout=30
        )
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Model: {result.get('model')}")
        print(f"Response: {result.get('response', 'No response')[:200]}...")
        return result
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return None


def check_recent_logs():
    """Check recent Cloud Run logs"""
    print("\n=== RECENT CLOUD RUN LOGS ===")
    
    client = logging.Client(project="bobs-house-ai")
    
    # Get logs from last hour
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    
    filter_str = f"""
    resource.type="cloud_run_revision"
    resource.labels.service_name="bobs-brain"
    timestamp >= "{one_hour_ago.isoformat()}Z"
    severity >= "WARNING"
    """
    
    entries = list(client.list_entries(filter_=filter_str, max_results=10))
    
    if entries:
        for entry in entries:
            timestamp = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            severity = entry.severity
            
            # Get the actual message
            if hasattr(entry, 'json_payload') and entry.json_payload:
                message = entry.json_payload.get('message', str(entry.json_payload))
            else:
                message = entry.payload or str(entry)
            
            print(f"{timestamp} [{severity}]: {message[:200]}")
    else:
        print("No recent warnings or errors found")


def check_slack_tokens():
    """Check if Slack tokens are configured"""
    print("\n=== CHECKING SLACK CONFIGURATION ===")
    
    # Check environment variables
    env_vars = [
        "SLACK_BOT_TOKEN",
        "SLACK_APP_TOKEN", 
        "SLACK_SIGNING_SECRET",
        "GOOGLE_API_KEY",
        "NEO4J_URI",
        "NEO4J_PASSWORD"
    ]
    
    print("Environment Variables (from Cloud Run):")
    # Note: We can't actually read the values from Cloud Run for security
    # But we can check if they're set
    try:
        import subprocess
        result = subprocess.run(
            ["gcloud", "run", "services", "describe", "bobs-brain", 
             "--region", "us-central1", "--format", "json"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            service = json.loads(result.stdout)
            env_vars_set = service.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [{}])[0].get('env', [])
            for var in env_vars_set:
                print(f"  ✅ {var['name']} is set")
        else:
            print("  ❌ Could not retrieve environment variables")
    except Exception as e:
        print(f"  ❌ Error checking env vars: {e}")


def test_gemini_connection():
    """Test if Gemini is actually working"""
    print("\n=== TESTING GEMINI CONNECTION ===")
    
    test_data = {
        "message": "Respond with exactly: 'Gemini is working'",
        "user": "test"
    }
    
    try:
        response = requests.post(
            "https://bobs-brain-sytrh5wz5q-uc.a.run.app/chat",
            json=test_data,
            timeout=30
        )
        result = response.json()
        if "Gemini" in result.get("response", "") or "working" in result.get("response", ""):
            print("✅ Gemini appears to be responding")
        else:
            print(f"⚠️ Unexpected response: {result.get('response', 'None')[:100]}")
        return True
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False


def create_monitoring_dashboard():
    """Create a monitoring dashboard for Bob"""
    print("\n=== SETTING UP MONITORING DASHBOARD ===")
    
    project_id = "bobs-house-ai"
    
    dashboard_json = {
        "displayName": "Bob's Brain Monitoring",
        "mosaicLayout": {
            "columns": 12,
            "tiles": [
                {
                    "width": 6,
                    "height": 4,
                    "widget": {
                        "title": "Request Rate",
                        "xyChart": {
                            "dataSets": [{
                                "timeSeriesQuery": {
                                    "timeSeriesFilter": {
                                        "filter": 'resource.type="cloud_run_revision" resource.labels.service_name="bobs-brain"',
                                        "aggregation": {
                                            "alignmentPeriod": "60s",
                                            "perSeriesAligner": "ALIGN_RATE"
                                        }
                                    }
                                }
                            }]
                        }
                    }
                },
                {
                    "xPos": 6,
                    "width": 6,
                    "height": 4,
                    "widget": {
                        "title": "Error Rate",
                        "xyChart": {
                            "dataSets": [{
                                "timeSeriesQuery": {
                                    "timeSeriesFilter": {
                                        "filter": 'resource.type="cloud_run_revision" severity="ERROR"',
                                        "aggregation": {
                                            "alignmentPeriod": "60s",
                                            "perSeriesAligner": "ALIGN_RATE"
                                        }
                                    }
                                }
                            }]
                        }
                    }
                }
            ]
        }
    }
    
    print("Dashboard configuration created (would need to be applied via Cloud Console)")
    return dashboard_json


def diagnose_slack_issue():
    """Deep dive into why Slack isn't working"""
    print("\n=== DIAGNOSING SLACK ISSUES ===")
    
    # Test if Bob can receive Slack events
    test_event = {
        "type": "event_callback",
        "event": {
            "type": "message",
            "text": "<@BOB_ID> test message from debug",
            "user": "debug_user",
            "channel": "C12345",
            "ts": str(time.time())
        }
    }
    
    try:
        response = requests.post(
            "https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events",
            json=test_event,
            timeout=10
        )
        print(f"Event submission: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        # Check if the event was processed
        time.sleep(2)
        
        # Check stats to see if event was processed
        health = requests.get("https://bobs-brain-sytrh5wz5q-uc.a.run.app/health").json()
        processed = health.get("stats", {}).get("processed_events", 0)
        print(f"Processed events: {processed}")
        
    except Exception as e:
        print(f"❌ Slack diagnosis failed: {e}")


def main():
    """Run all diagnostics"""
    print("=" * 60)
    print("BOB'S BRAIN DIAGNOSTIC TOOL")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Run all checks
    health = check_health()
    
    if health and health.get("status") == "healthy":
        test_slack_webhook()
        test_chat()
        test_gemini_connection()
        diagnose_slack_issue()
    
    check_slack_tokens()
    check_recent_logs()
    
    # Summary
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if health:
        if health.get("components", {}).get("slack") and health.get("components", {}).get("gemini"):
            print("✅ Bob appears to be configured correctly")
            print("⚠️ If Slack isn't working, check:")
            print("  1. Slack app is installed in workspace")
            print("  2. Bot is invited to channels")
            print("  3. Event subscriptions URL is set to:")
            print("     https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events")
            print("  4. OAuth scopes include: chat:write, channels:read, app_mentions:read")
        else:
            print("❌ Components are not fully operational")
    else:
        print("❌ Bob is not responding - check Cloud Run deployment")


if __name__ == "__main__":
    main()