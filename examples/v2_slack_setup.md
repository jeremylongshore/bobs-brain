# Bob v2 Unified - Slack Setup Guide

This guide walks you through setting up Bob v2 as a Slack bot for your workspace.

## 📋 Prerequisites

- Slack workspace (admin access required)
- Python 3.10+
- Bob v2 source code

## 🚀 Step-by-Step Setup

### 1. Create Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Name your app: `Bob AI Assistant`
5. Select your workspace

### 2. Configure Socket Mode

1. Go to **Socket Mode** in the left sidebar
2. Enable Socket Mode
3. Generate an **App-Level Token**:
   - Token Name: `bob-socket`
   - Scopes: `connections:write`
4. Copy the token (starts with `xapp-`)

### 3. Configure OAuth & Permissions

1. Go to **OAuth & Permissions**
2. Add **Bot Token Scopes**:
   - `app_mentions:read` - Read mentions
   - `chat:write` - Send messages
   - `channels:history` - Read channel messages
   - `groups:history` - Read private channel messages
   - `im:history` - Read direct messages
   - `mpim:history` - Read group DMs
   - `users:read` - Access user information

3. Click **"Install to Workspace"**
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 4. Configure Event Subscriptions

1. Go to **Event Subscriptions**
2. Enable Events
3. Subscribe to **Bot Events**:
   - `app_mention` - When Bob is @mentioned
   - `message.channels` - Channel messages
   - `message.groups` - Private channel messages
   - `message.im` - Direct messages

### 5. Set Up Environment Variables

Create `.env` file in Bob v2 directory:

```bash
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Bob Configuration
BOB_NAME="Bob"
BOB_MODE=production
LOG_LEVEL=INFO

# ChromaDB Configuration
CHROMA_PERSIST_DIR=/path/to/chroma/db
```

### 6. Install Dependencies

```bash
cd versions/v2-unified
pip install -r requirements.txt
```

### 7. Start Bob

```bash
# Using the startup script
./start_unified_bob_v2.sh

# Or directly with Python
python bob_unified_v2.py
```

### 8. Test Bob

1. Go to your Slack workspace
2. Invite Bob to a channel: `/invite @Bob`
3. Mention Bob: `@Bob hello!`
4. Bob should respond!

## 💬 Usage Examples

### In Channels
```
@Bob What can you help with?
@Bob Tell me about DiagnosticPro
@Bob Help me with customer service
```

### Direct Messages
```
Hello Bob!
What's the status?
Can you help me understand vehicle diagnostics?
```

## 🔧 Advanced Configuration

### Custom Responses

Edit response patterns in `bob_unified_v2.py`:

```python
self.response_patterns = {
    "custom_greeting": "Your custom greeting here",
    # Add more patterns
}
```

### Knowledge Base

Bob uses ChromaDB for knowledge storage:

```python
# Location: ~/.bob_brain/chroma
# Contains 970+ industry knowledge items
```

### Conversation Memory

Bob remembers recent interactions:
- User context
- Greeting frequency
- Conversation history

## 🐛 Troubleshooting

### Bob Not Responding

1. Check Socket Mode is enabled
2. Verify tokens in `.env`
3. Check logs: `tail -f logs/bob_unified_v2.log`
4. Ensure Bob is invited to channel

### Rate Limiting

Bob includes rate limit protection:
- Automatic retry with backoff
- Message deduplication
- Smart throttling

### Connection Issues

```bash
# Check Bob status
ps aux | grep bob_unified

# Restart Bob
pkill -f bob_unified
./start_unified_bob_v2.sh
```

## 📊 Monitoring

### Health Check
```python
# Bob includes health monitoring
http://localhost:8080/health  # If web server enabled
```

### Logs
```bash
# Real-time logs
tail -f logs/bob_unified_v2.log

# Error logs
grep ERROR logs/bob_unified_v2.log
```

### Metrics
- Response time tracking
- Message processing count
- Error rate monitoring

## 🚀 Production Deployment

### Docker Deployment

```bash
# Build image
docker build -f docker/v2-unified.Dockerfile -t bob-v2 .

# Run container
docker run -d \
  --name bob-v2 \
  -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN \
  -e SLACK_APP_TOKEN=$SLACK_APP_TOKEN \
  -v /path/to/chroma:/app/data/chroma \
  bob-v2
```

### Cloud Deployment (Google Cloud Run)

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT/bob-v2

# Deploy
gcloud run deploy bob-v2 \
  --image gcr.io/PROJECT/bob-v2 \
  --set-env-vars SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN \
  --set-env-vars SLACK_APP_TOKEN=$SLACK_APP_TOKEN
```

## 📝 Best Practices

1. **Security**
   - Never commit tokens to git
   - Use environment variables
   - Rotate tokens regularly

2. **Performance**
   - Monitor response times
   - Implement caching where appropriate
   - Use connection pooling

3. **Reliability**
   - Set up health checks
   - Implement automatic restarts
   - Monitor error rates

## 🆘 Getting Help

- Check logs first: `logs/bob_unified_v2.log`
- Review [Slack API docs](https://api.slack.com)
- Open issue on GitHub
- Contact: Jeremy Longshore - DiagnosticPro.io

---

*Bob v2 - Your Professional AI Business Partner in Slack*