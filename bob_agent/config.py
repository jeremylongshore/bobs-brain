# Bob Agent Configuration
# Slack tokens from environment variables (DO NOT hardcode tokens)
import os
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # Bot User OAuth Token
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # App-Level Token

# Database paths (existing setup)
CHROMA_PERSIST_DIR = "/home/jeremylongshore/.bob_brain/chroma"  # Chroma with 962 knowledge items
SQLITE_DB_PATH = "sqlite:////home/jeremylongshore/.bob_brain/bob_memory.db"  # Existing conversations
