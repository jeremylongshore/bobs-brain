#!/bin/bash

echo "======================================"
echo "STARTING BOB LOCALLY"
echo "======================================"

# Set environment variables
export GOOGLE_API_KEY="AIzaSyDOEAIpqn7qN1LknylLPvTKWU5TnUHBzEo"
export SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN}"  # Set in environment
export SLACK_APP_TOKEN="${SLACK_APP_TOKEN}"  # Set in environment
export NEO4J_URI="neo4j+s://d3653283.databases.neo4j.io"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE"

echo "Environment configured"
echo ""
echo "INSTRUCTIONS:"
echo "1. Make sure Slack app is set to SOCKET MODE"
echo "   - Go to https://api.slack.com/apps"
echo "   - Select your bobs_brain app"
echo "   - Go to 'Socket Mode' in left menu"
echo "   - Enable Socket Mode"
echo "   - You should have an App-Level Token (starts with xapp-)"
echo ""
echo "2. Disable Event Subscriptions (not needed for Socket Mode)"
echo "   - Go to 'Event Subscriptions'"
echo "   - Toggle Enable Events to OFF"
echo ""
echo "Starting Bob..."
echo "======================================"

# Run Bob locally
python3 bob_local_forever.py
