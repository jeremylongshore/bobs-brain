# 🏠 Bob's House AI - FIXED AND WORKING

Bob is now fixed and ready to go! This is a simple, local AI agent that works with Slack.

## 🚀 Quick Start

1. **Copy environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Edit .env with your Slack tokens:**
   ```bash
   # Get these from https://api.slack.com/apps
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token

   # Optional: Add OpenAI API key for better responses
   OPENAI_API_KEY=sk-your-openai-key
   ```

3. **Run Bob:**
   ```bash
   ./run_bob.sh
   ```

## 🔧 Manual Docker Commands

```bash
# Build the image
docker build -t bob-agent .

# Run the container
docker run --env-file .env -p 3000:3000 bob-agent
```

## 📱 Slack Setup

1. Go to https://api.slack.com/apps
2. Create a new app
3. Enable Socket Mode
4. Add Bot Token Scopes: `app_mentions:read`, `chat:write`, `channels:history`
5. Install app to workspace
6. Copy tokens to .env file

## 🤖 What Bob Can Do

- **Chat**: Responds to messages in Slack
- **Smart or Simple**: Uses OpenAI if you have a key, otherwise gives simple responses
- **No Complex Dependencies**: Removed all the complex stuff that was breaking

## 🐛 Troubleshooting

- **Docker not running**: Start Docker first
- **Slack tokens wrong**: Check your Slack app settings
- **Still broken**: Check Docker logs: `docker logs bob-agent`

---

*Bob works now! 🎉*
