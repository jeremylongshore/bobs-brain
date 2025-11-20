#!/usr/bin/env python3
"""
Bob Slack Bot Runner - Clean entry point for production Slack bot
"""

import sys
from pathlib import Path

# Add bob package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from bob.core.config import BobConfig
from bob.agents.unified_v2 import BobUnifiedV2


def main():
    """Run Bob Unified v2 Slack Bot"""
    config = BobConfig()
    
    if not config.slack_bot_token or not config.slack_app_token:
        print("❌ Slack tokens not configured. Please check config/.env")
        return
    
    print("🤖 Starting Bob Unified v2 Slack Bot...")
    bob = BobUnifiedV2(config.slack_bot_token, config.slack_app_token)
    bob.start()


if __name__ == "__main__":
    main()