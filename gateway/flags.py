"""
Feature Flags

Simple environment variable-based feature flags for gateway functionality.
Flags are prefixed with FF_ and evaluated at runtime.

Example usage:
    from gateway.flags import enabled

    if enabled("slack"):
        # Mount Slack integration
        ...

    if enabled("streaming", default=True):
        # Enable streaming endpoint
        ...
"""
import os


def enabled(name: str, default: bool = False) -> bool:
    """
    Check if a feature flag is enabled.

    Args:
        name: Feature name (will be uppercased and prefixed with FF_)
        default: Default value if flag is not set

    Returns:
        True if flag is enabled, False otherwise

    Environment Variable Format:
        FF_{NAME} = "1" | "true" | "yes" | "on"  (enabled)
        FF_{NAME} = "0" | "false" | "no" | "off" (disabled)
        FF_{NAME} not set = use default

    Examples:
        FF_SLACK=true → enabled("slack") returns True
        FF_STREAMING=false → enabled("streaming") returns False
        FF_DEBUG not set → enabled("debug", default=True) returns True
    """
    env_var = f"FF_{name.upper()}"
    value = os.getenv(env_var)

    if value is None:
        return default

    # Normalize and check for truthy values
    return value.lower() in ("1", "true", "yes", "on")


def disabled(name: str, default: bool = False) -> bool:
    """
    Check if a feature flag is disabled (inverse of enabled).

    Args:
        name: Feature name
        default: Default value if flag is not set

    Returns:
        True if flag is disabled, False otherwise
    """
    return not enabled(name, default=not default)


def get_all_flags() -> dict:
    """
    Get all FF_ environment variables and their states.

    Returns:
        Dictionary mapping flag names to boolean values

    Example:
        {
            "slack": True,
            "streaming": False,
            "debug": True
        }
    """
    flags = {}
    for key, value in os.environ.items():
        if key.startswith("FF_"):
            name = key[3:].lower()
            flags[name] = value.lower() in ("1", "true", "yes", "on")
    return flags
