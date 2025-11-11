from datetime import datetime, timezone
from google.adk.tools import FunctionTool

def get_current_time(tz: str = "UTC") -> str:
    """Returns current time in ISO 8601 format (UTC)."""
    return datetime.now(timezone.utc).isoformat()

def get_current_time_tool() -> FunctionTool:
    return FunctionTool(get_current_time)
