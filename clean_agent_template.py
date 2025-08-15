#!/usr/bin/env python3
"""
BOB FERRARI EDITION - Complete Holistic AI Assistant
TEMPLATE VERSION - Add your own tokens to .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get tokens from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([GEMINI_API_KEY, SLACK_BOT_TOKEN, NEO4J_PASSWORD]):
    print("ERROR: Missing environment variables!")
    print("Create a .env file with:")
    print("  GEMINI_API_KEY=your-key")
    print("  SLACK_BOT_TOKEN=your-token")
    print("  NEO4J_PASSWORD=your-password")
    exit(1)

# Rest of the Bob Ferrari code continues here...
print("Bob Ferrari ready to run with environment variables!")