# Slack App Configuration for Bob Cloud Run

## IMPORTANT: Configure Your Slack App

Bob is deployed and running at: https://bobs-brain-157908567967.us-central1.run.app

To connect Slack to Bob, you need to update your Slack app settings:

### 1. Go to Slack API Dashboard
Visit: https://api.slack.com/apps

### 2. Select Your Bob App
Find and click on your Bob app (should be using the tokens provided)

### 3. Configure Event Subscriptions
- Go to "Event Subscriptions" in the left sidebar
- Enable Events: Toggle ON
- Request URL: Enter `https://bobs-brain-157908567967.us-central1.run.app/slack/events`
- Wait for "Verified" ✓ status

### 4. Subscribe to Bot Events
In the same Event Subscriptions page:
- Under "Subscribe to bot events"
- Add these events:
  - `app_mention` - When someone mentions @Bob
  - `message.channels` - Messages in channels Bob is in
  - `message.im` - Direct messages to Bob
  - `message.groups` - Messages in private channels
- Click "Save Changes"

### 5. OAuth & Permissions
- Go to "OAuth & Permissions" in the left sidebar
- Under "Bot Token Scopes", ensure you have:
  - `chat:write` - Send messages
  - `channels:history` - Read channel messages
  - `im:history` - Read DM history
  - `groups:history` - Read private channel history
  - `app_mentions:read` - Read mentions

### 6. Reinstall the App
- After making changes, reinstall the app to your workspace
- Go to "Install App" in the left sidebar
- Click "Reinstall to Workspace"

### 7. Test Bob
- Go to Slack
- Send a DM to Bob: "Hey Bob, are you there?"
- Or mention Bob in a channel: "@Bob what do you know?"

## Troubleshooting

If Bob doesn't respond:
1. Check Cloud Run logs: `gcloud run services logs read bobs-brain --region us-central1`
2. Verify the Request URL shows "Verified" in Slack Event Subscriptions
3. Make sure Bob is added to the channels you're testing in
4. Check that all OAuth scopes are properly configured

## Current Status
- Cloud Run: ✅ DEPLOYED
- Health Check: ✅ WORKING
- Slack Events URL: https://bobs-brain-157908567967.us-central1.run.app/slack/events
- Awaiting: Slack app configuration update