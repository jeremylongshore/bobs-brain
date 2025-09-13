"""
Bob Configuration Management
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class BobConfig:
    """Centralized configuration management for Bob"""
    
    def __init__(self, config_dir: Path = None):
        """Initialize configuration"""
        self.config_dir = config_dir or Path(__file__).parent.parent.parent / "config"
        self._load_environment()
        
    def _load_environment(self):
        """Load environment variables from .env file"""
        env_file = self.config_dir / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    
    @property
    def slack_bot_token(self) -> str:
        """Get Slack bot token"""
        return os.getenv("SLACK_BOT_TOKEN", "")
    
    @property
    def slack_app_token(self) -> str:
        """Get Slack app token"""
        return os.getenv("SLACK_APP_TOKEN", "")
    
    @property
    def chroma_persist_dir(self) -> str:
        """Get ChromaDB persistence directory"""
        return os.getenv("CHROMA_PERSIST_DIR", str(Path.home() / ".bob_brain" / "chroma"))
    
    @property
    def log_level(self) -> str:
        """Get log level"""
        return os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def business_context(self) -> Dict[str, Any]:
        """Get business context"""
        return {
            "company": "DiagnosticPro.io",
            "owner": "Jeremy Longshore",
            "mission": "Vehicle diagnostics and repair industry expertise",
            "focus": "Customer protection from shop overcharges"
        }