"""
Slack Integration Utilities
"""

import logging
from typing import Dict, Any, Set, Optional
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from datetime import datetime, timedelta
from .config import BobConfig


class SlackClient:
    """Slack client with enhanced communication features"""
    
    def __init__(self, config: BobConfig):
        """Initialize Slack client"""
        self.config = config
        self.web_client = WebClient(token=config.slack_bot_token)
        self.socket_client = SocketModeClient(app_token=config.slack_app_token)
        
        # Duplicate prevention
        self.processed_messages: Set[str] = set()
        self.last_cleanup = datetime.now()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def is_duplicate_message(self, message_id: str) -> bool:
        """Check if message has already been processed"""
        # Cleanup old messages every 30 minutes
        if datetime.now() - self.last_cleanup > timedelta(minutes=30):
            self.processed_messages.clear()
            self.last_cleanup = datetime.now()
        
        if message_id in self.processed_messages:
            return True
        
        self.processed_messages.add(message_id)
        return False
    
    def send_message(self, channel: str, text: str, thread_ts: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to Slack"""
        try:
            response = self.web_client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts
            )
            return response
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return {}
    
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get user information"""
        try:
            response = self.web_client.users_info(user=user_id)
            return response.get('user', {})
        except Exception as e:
            self.logger.error(f"Failed to get user info: {e}")
            return {}
    
    def is_jeremy(self, user_id: str) -> bool:
        """Check if user is Jeremy (owner)"""
        user_info = self.get_user_info(user_id)
        user_name = user_info.get('name', '').lower()
        real_name = user_info.get('real_name', '').lower()
        return 'jeremy' in user_name or 'jeremy' in real_name