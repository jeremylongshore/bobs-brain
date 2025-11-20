"""
Notification configuration module for Slack and other notification channels.

This module provides configuration for sending notifications about SWE/portfolio
completion via Slack and other channels. All features are OPT-IN by default.

Environment Variables:
- SLACK_NOTIFICATIONS_ENABLED: Enable Slack notifications (default: false)
- SLACK_SWE_CHANNEL_WEBHOOK_URL: Webhook URL for SWE notifications
- SLACK_SWE_CHANNEL_ID: Channel ID for SWE notifications (alternative to webhook)

Usage:
    from agents.config.notifications import (
        are_slack_notifications_enabled,
        get_swe_slack_destination
    )

    if are_slack_notifications_enabled():
        dest = get_swe_slack_destination()
        if dest:
            # Send notification to dest
"""

import os
import logging
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SlackDestination:
    """
    Represents a Slack notification destination.

    Either webhook_url OR channel_id should be set, not both.
    """
    webhook_url: Optional[str] = None
    channel_id: Optional[str] = None

    def is_valid(self) -> bool:
        """Check if destination has at least one valid target."""
        return bool(self.webhook_url or self.channel_id)

    def __repr__(self) -> str:
        if self.webhook_url:
            # Mask webhook URL for security
            masked = self.webhook_url[:30] + "..." if len(self.webhook_url) > 30 else self.webhook_url
            return f"SlackDestination(webhook={masked})"
        elif self.channel_id:
            return f"SlackDestination(channel={self.channel_id})"
        return "SlackDestination(unconfigured)"


def are_slack_notifications_enabled() -> bool:
    """
    Check if Slack notifications are enabled.

    Returns:
        bool: True if SLACK_NOTIFICATIONS_ENABLED is set to 'true', False otherwise.

    Default: False (opt-in)
    """
    enabled_str = os.getenv("SLACK_NOTIFICATIONS_ENABLED", "false").lower()
    is_enabled = enabled_str in ("true", "1", "yes")

    if is_enabled:
        logger.info("Slack notifications are ENABLED")
    else:
        logger.debug("Slack notifications are DISABLED (set SLACK_NOTIFICATIONS_ENABLED=true to enable)")

    return is_enabled


def get_swe_slack_destination() -> Optional[SlackDestination]:
    """
    Get the Slack destination for SWE/portfolio notifications.

    Checks environment variables in priority order:
    1. SLACK_SWE_CHANNEL_WEBHOOK_URL (preferred - direct webhook)
    2. SLACK_SWE_CHANNEL_ID (alternative - requires bot token)

    Returns:
        SlackDestination or None if not configured.
    """
    webhook_url = os.getenv("SLACK_SWE_CHANNEL_WEBHOOK_URL")
    channel_id = os.getenv("SLACK_SWE_CHANNEL_ID")

    if webhook_url:
        logger.info(f"Slack SWE destination: webhook (masked: {webhook_url[:30]}...)")
        return SlackDestination(webhook_url=webhook_url)
    elif channel_id:
        logger.info(f"Slack SWE destination: channel_id={channel_id}")
        return SlackDestination(channel_id=channel_id)
    else:
        logger.warning(
            "No Slack SWE destination configured. Set SLACK_SWE_CHANNEL_WEBHOOK_URL "
            "or SLACK_SWE_CHANNEL_ID to receive notifications."
        )
        return None


def should_send_slack_notifications() -> bool:
    """
    Combined check: are notifications enabled AND is destination configured?

    This is the main guard function to use before attempting to send Slack messages.

    Returns:
        bool: True if both enabled and configured, False otherwise.
    """
    if not are_slack_notifications_enabled():
        return False

    destination = get_swe_slack_destination()
    if not destination or not destination.is_valid():
        logger.warning("Slack notifications enabled but destination not configured - skipping")
        return False

    return True


def get_notification_summary() -> str:
    """
    Get a human-readable summary of notification configuration.

    Useful for logging, diagnostics, and readiness checks.

    Returns:
        str: Multi-line summary of notification status.
    """
    lines = []
    lines.append("Notification Configuration:")
    lines.append(f"  Slack Enabled: {are_slack_notifications_enabled()}")

    destination = get_swe_slack_destination()
    if destination:
        lines.append(f"  Slack Destination: {destination}")
    else:
        lines.append("  Slack Destination: Not configured")

    lines.append(f"  Ready to Send: {should_send_slack_notifications()}")

    return "\n".join(lines)


# Convenience function for logging config at startup
def log_notification_config() -> None:
    """Log the current notification configuration."""
    logger.info(get_notification_summary())


if __name__ == "__main__":
    # Quick test/diagnostic when run directly
    import sys
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print(get_notification_summary())
    print()

    if should_send_slack_notifications():
        print("✅ Ready to send Slack notifications")
        sys.exit(0)
    else:
        print("❌ Slack notifications not ready (disabled or misconfigured)")
        print()
        print("To enable:")
        print("  export SLACK_NOTIFICATIONS_ENABLED=true")
        print("  export SLACK_SWE_CHANNEL_WEBHOOK_URL=https://hooks.slack.com/services/...")
        sys.exit(1)
