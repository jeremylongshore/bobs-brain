"""
GitHub Feature Flags and Safety Configuration

Controls which GitHub write operations are enabled and for which repositories.
All write operations are disabled by default for safety.
"""

import os
from typing import Set, Optional
from dataclasses import dataclass


@dataclass
class GitHubFeatureConfig:
    """Configuration for GitHub feature flags."""

    issue_creation_enabled: bool
    allowed_repos: Set[str]  # Set of repo_ids, or {"*"} for all repos

    def is_repo_allowed(self, repo_id: str) -> bool:
        """
        Check if a repo is in the allowed list.

        Args:
            repo_id: Repository ID to check

        Returns:
            True if repo is allowed, False otherwise
        """
        # "*" means all repos are allowed
        if "*" in self.allowed_repos:
            return True

        # Check if specific repo_id is in allowlist
        return repo_id in self.allowed_repos


def load_github_feature_config() -> GitHubFeatureConfig:
    """
    Load GitHub feature configuration from environment variables.

    Environment Variables:
        GITHUB_ISSUE_CREATION_ENABLED: "true" or "false" (default: "false")
        GITHUB_ISSUE_CREATION_ALLOWED_REPOS: Comma-separated repo IDs or "*" (default: "")

    Returns:
        GitHubFeatureConfig object

    Examples:
        # Disabled (default)
        export GITHUB_ISSUE_CREATION_ENABLED=false

        # Enabled for specific repos
        export GITHUB_ISSUE_CREATION_ENABLED=true
        export GITHUB_ISSUE_CREATION_ALLOWED_REPOS=bobs-brain,test-repo

        # Enabled for all repos (use with caution!)
        export GITHUB_ISSUE_CREATION_ENABLED=true
        export GITHUB_ISSUE_CREATION_ALLOWED_REPOS=*
    """
    # Load feature flag (default: disabled)
    enabled_str = os.getenv("GITHUB_ISSUE_CREATION_ENABLED", "false").lower()
    issue_creation_enabled = enabled_str in ("true", "1", "yes", "on")

    # Load allowed repos list (default: empty)
    allowed_str = os.getenv("GITHUB_ISSUE_CREATION_ALLOWED_REPOS", "")
    if not allowed_str:
        # Empty = no repos allowed
        allowed_repos = set()
    elif allowed_str.strip() == "*":
        # "*" = all repos allowed
        allowed_repos = {"*"}
    else:
        # Parse comma-separated list
        allowed_repos = {
            repo.strip()
            for repo in allowed_str.split(",")
            if repo.strip()
        }

    return GitHubFeatureConfig(
        issue_creation_enabled=issue_creation_enabled,
        allowed_repos=allowed_repos
    )


def can_create_issues_for_repo(repo_id: str, config: Optional[GitHubFeatureConfig] = None) -> bool:
    """
    Check if GitHub issue creation is allowed for a specific repository.

    This is the main safety gate for issue creation. Both conditions must be true:
    1. Issue creation feature must be globally enabled
    2. The specific repo must be in the allowlist

    Args:
        repo_id: Repository ID (from repo registry)
        config: Optional pre-loaded config (loads from env if not provided)

    Returns:
        True if issue creation is allowed, False otherwise

    Examples:
        >>> # Check if can create issues for bobs-brain
        >>> if can_create_issues_for_repo("bobs-brain"):
        ...     client.create_issue(...)
        ... else:
        ...     print("Issue creation disabled for this repo")
    """
    if config is None:
        config = load_github_feature_config()

    # Both must be true: feature enabled + repo allowed
    return config.issue_creation_enabled and config.is_repo_allowed(repo_id)


def get_feature_status_summary() -> dict:
    """
    Get human-readable summary of GitHub feature configuration.

    Returns:
        Dictionary with status information

    Example:
        >>> status = get_feature_status_summary()
        >>> print(status['message'])
        ✅ GitHub issue creation ENABLED for: bobs-brain, test-repo
    """
    config = load_github_feature_config()

    if not config.issue_creation_enabled:
        return {
            "enabled": False,
            "allowed_repos": [],
            "message": "🚫 GitHub issue creation is DISABLED (safe mode)",
            "recommendation": "Set GITHUB_ISSUE_CREATION_ENABLED=true to enable"
        }

    if "*" in config.allowed_repos:
        return {
            "enabled": True,
            "allowed_repos": ["*"],
            "message": "⚠️  GitHub issue creation ENABLED for ALL REPOS",
            "warning": "Use with caution - this allows creation in any repository"
        }

    repos_list = sorted(config.allowed_repos)
    return {
        "enabled": True,
        "allowed_repos": repos_list,
        "message": f"✅ GitHub issue creation ENABLED for: {', '.join(repos_list)}",
        "info": f"Allowed repos: {len(repos_list)}"
    }


# Example usage and testing
if __name__ == "__main__":
    print("🔐 GitHub Feature Configuration")
    print("=" * 60)

    # Load current config
    config = load_github_feature_config()

    print(f"\nFeature Flag: GITHUB_ISSUE_CREATION_ENABLED = {config.issue_creation_enabled}")
    print(f"Allowed Repos: {config.allowed_repos}")

    # Show status
    status = get_feature_status_summary()
    print(f"\n{status['message']}")

    if "warning" in status:
        print(f"⚠️  {status['warning']}")
    if "recommendation" in status:
        print(f"💡 {status['recommendation']}")

    # Test specific repos
    test_repos = ["bobs-brain", "test-repo", "unknown-repo"]
    print("\nRepository Access Checks:")
    for repo_id in test_repos:
        allowed = can_create_issues_for_repo(repo_id, config)
        icon = "✅" if allowed else "❌"
        print(f"  {icon} {repo_id}: {'ALLOWED' if allowed else 'BLOCKED'}")

    print("\n" + "=" * 60)
    print("Configuration loaded from environment variables:")
    print("  - GITHUB_ISSUE_CREATION_ENABLED")
    print("  - GITHUB_ISSUE_CREATION_ALLOWED_REPOS")
