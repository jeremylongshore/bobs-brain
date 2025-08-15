#!/bin/bash

# BOB STARTUP SCRIPT - Run this to start Bob locally

echo "============================================================"
echo "                    STARTING BOB LOCALLY                   "
echo "============================================================"
echo ""
echo "Bob will run on your machine and connect to:"
echo "  • Gemini AI for responses"
echo "  • Slack for messaging"
echo "  • Neo4j for knowledge"
echo ""
echo "Cost: ~$0 (uses free tier/minimal API calls)"
echo ""
echo "Press Ctrl+C to stop Bob"
echo "============================================================"
echo ""

# Set environment variables
export GOOGLE_API_KEY="AIzaSyDOEAIpqn7qN1LknylLPvTKWU5TnUHBzEo"
export SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN}"  # Set in environment

# Run Bob
while true; do
    echo "[$(date)] Starting Bob..."
    python3 bob_works_now.py

    # If Bob crashes, wait 5 seconds and restart
    echo "[$(date)] Bob stopped. Restarting in 5 seconds..."
    sleep 5
done
