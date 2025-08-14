#!/bin/bash

echo "======================================"
echo "FIXING BOB'S SLACK INTEGRATION"
echo "======================================"

# Set all required environment variables
echo "Setting environment variables..."

gcloud run services update bobs-brain \
  --region us-central1 \
  --update-env-vars "\
SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN},\
SLACK_APP_TOKEN=${SLACK_APP_TOKEN},\
SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET},\
GOOGLE_API_KEY=AIzaSyDOEAIpqn7qN1LknylLPvTKWU5TnUHBzEo,\
NEO4J_URI=neo4j+s://d3653283.databases.neo4j.io,\
NEO4J_USER=neo4j,\
NEO4J_PASSWORD=q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE,\
PROJECT_ID=bobs-house-ai"

echo ""
echo "Waiting for deployment..."
sleep 10

echo ""
echo "Testing Bob's health..."
curl -s https://bobs-brain-sytrh5wz5q-uc.a.run.app/health | python3 -m json.tool | grep -E "(status|slack|gemini)"

echo ""
echo "======================================"
echo "SLACK APP CONFIGURATION NEEDED:"
echo "======================================"
echo "1. Go to: https://api.slack.com/apps"
echo "2. Select your Bob app"
echo "3. Go to 'Event Subscriptions'"
echo "4. Set Request URL to:"
echo "   https://bobs-brain-sytrh5wz5q-uc.a.run.app/slack/events"
echo "5. Subscribe to bot events:"
echo "   - message.channels"
echo "   - message.im"
echo "   - app_mention"
echo "6. Save changes"
echo ""
echo "7. Go to 'OAuth & Permissions'"
echo "8. Ensure these scopes are added:"
echo "   - app_mentions:read"
echo "   - channels:history"
echo "   - chat:write"
echo "   - im:history"
echo "   - im:read"
echo "   - im:write"
echo ""
echo "9. Reinstall the app to your workspace"
echo "10. Invite Bob to channels with: /invite @bob"
echo "======================================"