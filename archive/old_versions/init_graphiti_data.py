#!/usr/bin/env python3
"""
Initialize Graphiti with foundational data via Bob's API
"""

import requests
import json
import time

BASE_URL = "https://bobs-brain-157908567967.us-central1.run.app"

def send_initialization_messages():
    """Send messages to Bob to populate the knowledge graph"""
    
    print("=" * 60)
    print("🚀 INITIALIZING BOB'S KNOWLEDGE GRAPH")
    print("=" * 60)
    
    # Initial knowledge to store
    messages = [
        "Bob, remember that Jeremy Longshore owns DiagnosticPro, a company that protects customers from repair shop overcharges.",
        "DiagnosticPro uses AI technology to verify automotive repair quotes and has saved customers thousands of dollars.",
        "Jeremy has 15 years of business experience and previously worked in trucking and BBI industries.",
        "Bob is powered by Graphiti knowledge graph, Neo4j database, and Vertex AI on Google Cloud Platform.",
        "The system includes temporal awareness, entity extraction, and semantic search capabilities.",
        "DiagnosticPro's mission is to bring transparency to the automotive repair industry.",
        "Bob can remember conversations, extract relationships, and provide contextual responses.",
        "The technical stack includes Cloud Run, Neo4j, Graphiti, Vertex AI, and Slack integration."
    ]
    
    print("\nSending initialization messages to Bob...")
    
    for i, message in enumerate(messages, 1):
        print(f"\n{i}. Sending: {message[:60]}...")
        
        # Create a Slack event
        event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "text": message,
                "user": "U_SYSTEM_INIT",
                "channel": "C_INITIALIZATION",
                "ts": str(time.time())
            }
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/slack/events",
                json=event,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"   ✅ Message processed")
            else:
                print(f"   ⚠️  Response: {response.status_code}")
                
            # Small delay between messages
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ INITIALIZATION COMPLETE!")
    print("   Bob's knowledge graph has been populated with foundational data")
    print("   Bob is now ready to learn and assist!")
    print("\n📱 NEXT STEPS:")
    print("1. Update Slack Event Subscriptions URL to:")
    print(f"   {BASE_URL}/slack/events")
    print("2. Start chatting with Bob in Slack!")
    print("3. Bob will continue learning from every conversation")
    print("=" * 60)

if __name__ == "__main__":
    send_initialization_messages()