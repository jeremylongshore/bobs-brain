#!/bin/bash
#
# Store Bob's Brain Slack Credentials in Pass Password Manager
# Run this script to backup all credentials to pass
#

set -e

echo "════════════════════════════════════════════════════════════"
echo "Bob's Brain - Store Credentials in Pass"
echo "════════════════════════════════════════════════════════════"
echo ""

# Check if pass is installed
if ! command -v pass &> /dev/null; then
    echo "❌ ERROR: 'pass' password manager not installed"
    echo "Install with: sudo apt install pass"
    exit 1
fi

echo "✅ pass is installed"
echo ""

# Source .env file to get credentials
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found"
    echo "Run this script from the bobs-brain directory"
    exit 1
fi

source .env

echo "Storing Slack credentials in pass..."
echo ""

# Store each credential
echo "📝 Storing App ID..."
pass insert -e bobs-brain/slack/app-id <<< "$SLACK_APP_ID"

echo "📝 Storing Client ID..."
pass insert -e bobs-brain/slack/client-id <<< "$SLACK_CLIENT_ID"

echo "📝 Storing Client Secret..."
pass insert -e bobs-brain/slack/client-secret <<< "$SLACK_CLIENT_SECRET"

echo "📝 Storing Signing Secret..."
pass insert -e bobs-brain/slack/signing-secret <<< "$SLACK_SIGNING_SECRET"

echo "📝 Storing Verification Token..."
pass insert -e bobs-brain/slack/verification-token <<< "$SLACK_VERIFICATION_TOKEN"

echo "📝 Storing Bot Token..."
pass insert -e bobs-brain/slack/bot-token <<< "$SLACK_BOT_TOKEN"

echo ""
echo "✅ All credentials stored in pass!"
echo ""
echo "View stored credentials:"
echo "  pass bobs-brain/slack/"
echo ""
echo "Retrieve individual credential:"
echo "  pass bobs-brain/slack/bot-token"
echo ""
echo "Copy to clipboard:"
echo "  pass -c bobs-brain/slack/bot-token"
echo ""
