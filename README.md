# 🤖 Bob's Brain - Slack AI Agent Template

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Slack Compatible](https://img.shields.io/badge/slack-socket_mode-4A154B)](https://api.slack.com/)
[![ChromaDB](https://img.shields.io/badge/vectordb-chromadb-orange)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A simple, clean template for building your own Slack AI assistant with knowledge base integration.

## 🎯 What This Is

Bob's Brain is a **template/starter kit** for developers who want to:
- Build a custom Slack bot with AI capabilities
- Connect it to their own knowledge base
- Have a working example to learn from
- Start with clean, organized Python code

**Note:** This is a template - you bring your own data and customize it for your needs.

## 📦 What's Included

### Two Bot Implementations
1. **Slack Bot** (`bob/agents/unified_v2.py`)
   - Uses Slack Socket Mode (WebSocket connection)
   - Handles messages and mentions
   - Prevents duplicate responses
   - Basic conversation memory

2. **CLI Bot** (`bob/agents/basic.py`)
   - Command-line interface for testing
   - SQLite for local storage
   - Good for development/debugging

### Core Features
- ✅ Slack integration via Socket Mode
- ✅ ChromaDB vector database hookup
- ✅ Message deduplication
- ✅ Conversation context tracking
- ✅ Clean Python package structure
- ✅ Configuration management
- ✅ Logging system

### What You Need to Add
- 🔧 Your own knowledge base data
- 🔧 Your business logic
- 🔧 Custom responses/personality
- 🔧 API integrations (OpenAI, etc.)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Slack workspace with app creation permissions
- ChromaDB (or modify to use your preferred vector DB)

### Installation

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp config/.env.template config/.env
```

### Configuration

1. **Create a Slack App**
   - Go to https://api.slack.com/apps
   - Create new app
   - Enable Socket Mode
   - Add Bot Token Scopes:
     - `app_mentions:read`
     - `chat:write`
     - `channels:history`
     - `im:history`

2. **Get Your Tokens**
   - Bot Token: `xoxb-...` (OAuth & Permissions page)
   - App Token: `xapp-...` (Basic Information page)

3. **Update `.env` file**
   ```env
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   ```

### Running the Bot

**For Slack:**
```bash
python run_slack_bot.py
```

**For CLI Testing:**
```bash
python run_bob.py
```

## 🏗️ Project Structure

```
bobs-brain/
├── bob/                  # Main package
│   ├── agents/          # Bot implementations
│   │   ├── unified_v2.py    # Slack bot
│   │   └── basic.py         # CLI bot
│   ├── core/            # Core functionality
│   │   ├── config.py        # Configuration
│   │   ├── knowledge.py     # ChromaDB integration
│   │   └── slack.py         # Slack utilities
│   └── utils/           # Helper functions
├── config/              # Configuration files
├── data/               # Sample data structure
├── tests/              # Test files
└── scripts/            # Utility scripts
```

## 🔧 Customization Guide

### Adding Your Knowledge Base

```python
from bob.core.knowledge import KnowledgeBase
from bob.core.config import BobConfig

# Initialize your knowledge base
config = BobConfig()
kb = KnowledgeBase(config)

# Add your documents
kb.add_knowledge(
    documents=["Your content here"],
    metadata=[{"source": "your_source"}]
)
```

### Customizing Responses

Edit `bob/agents/unified_v2.py` to modify:
- Response patterns
- Business context
- Greeting messages
- Conversation logic

### Integrating AI Models

The template is model-agnostic. You can add:
- OpenAI GPT
- Anthropic Claude
- Local models (Ollama)
- Any LLM API

Example in requirements.txt:
```python
openai>=1.0.0  # Uncomment and implement
```

## 📚 Learning Resources

### For Beginners
1. Start with the CLI bot (`run_bob.py`) to understand the flow
2. Read through `bob/agents/basic.py` - it's simpler
3. Test locally before deploying to Slack
4. Add features incrementally

### Key Files to Study
- `bob/core/config.py` - How configuration works
- `bob/agents/basic.py` - Simple bot logic
- `bob/agents/unified_v2.py` - Slack integration
- `run_slack_bot.py` - Entry point

## 🐛 Common Issues

### "No knowledge base found"
- You need to create and populate your ChromaDB collection
- Check the path in your config

### "Slack tokens not configured"
- Make sure `.env` file exists with your tokens
- Verify tokens are correct format

### "Bot not responding"
- Check Socket Mode is enabled in Slack app
- Verify bot is in the channel
- Check logs in `logs/` directory

## 🤝 Contributing

This is a template meant for learning and customization. Feel free to:
- Fork and modify for your needs
- Submit issues for bugs
- Share your improvements

## 📄 License

MIT License - Use this template however you want!

## 🙏 Acknowledgments

- Built as a learning template for the community
- Inspired by real production needs at DiagnosticPro.io
- Designed to be simple and hackable

---

**Remember:** This is a starting point. The magic happens when you add your own data and logic! 🚀

## Need Help?

- 📧 Email: jeremy@diagnosticpro.io
- 🐛 Issues: [GitHub Issues](https://github.com/jeremylongshore/bobs-brain/issues)
- 📖 Docs: Check the `docs/` directory for more details

---

*Bob's Brain - Your journey to building AI assistants starts here!*