#!/bin/bash
# Setup script for Bob with Slack tokens

echo "🤖 BOB SETUP SCRIPT"
echo "=================="
echo ""
echo "Please provide your Slack tokens..."
echo ""

# Check if .env file exists
if [ -f .env ]; then
    echo "📝 Found existing .env file - will update it"
else
    echo "📝 Creating new .env file"
fi

# Function to update or add environment variable
update_env() {
    key=$1
    value=$2
    if grep -q "^$key=" .env 2>/dev/null; then
        # Update existing
        sed -i "s|^$key=.*|$key=$value|" .env
    else
        # Add new
        echo "$key=$value" >> .env
    fi
}

echo "Please paste your Slack tokens below:"
echo ""

read -p "SLACK_BOT_TOKEN (xoxb-...): " bot_token
read -p "SLACK_APP_TOKEN (xapp-...): " app_token  
read -p "SLACK_SIGNING_SECRET: " signing_secret

# Update .env file
update_env "SLACK_BOT_TOKEN" "$bot_token"
update_env "SLACK_APP_TOKEN" "$app_token"
update_env "SLACK_SIGNING_SECRET" "$signing_secret"

# Add other required variables
update_env "GCP_PROJECT" "diagnostic-pro-mvp"
update_env "GCP_LOCATION" "us-central1"
update_env "PORT" "3000"

echo ""
echo "✅ Tokens saved to .env file"
echo ""
echo "Testing Bob startup..."
echo ""

# Export for current session
export SLACK_BOT_TOKEN="$bot_token"
export SLACK_APP_TOKEN="$app_token"
export SLACK_SIGNING_SECRET="$signing_secret"

# Try to start Bob
python3 src/bob_firestore.py