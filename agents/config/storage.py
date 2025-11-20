"""
Org Storage Configuration (LIVE1-GCS)

Provides configuration helpers for org-wide GCS knowledge hub bucket.
All writes are opt-in via feature flags (default: disabled).

Environment Variables:
    ORG_STORAGE_BUCKET: Bucket name (e.g., "intent-org-knowledge-hub-dev")
    ORG_STORAGE_WRITE_ENABLED: Enable writes (default: "false")

Layout:
    portfolio/runs/{run_id}/summary.json          - Portfolio summaries
    portfolio/runs/{run_id}/per-repo/{repo_id}.json - Per-repo results
    swe/agents/{agent_name}/runs/{run_id}.json    - Single-repo runs (future)
    docs/                                          - Org docs (future)
    vertex-search/                                 - RAG snapshots (LIVE2+)

BigQuery:
    - Deferred to future LIVE-BQ phase
    - This module does NOT include BigQuery helpers
"""

import os
from typing import Optional


def get_org_storage_bucket() -> Optional[str]:
    """
    Get org-wide storage bucket name from environment.

    Returns:
        Bucket name if set, None otherwise.

    Example:
        "intent-org-knowledge-hub-dev"
    """
    return os.getenv("ORG_STORAGE_BUCKET")


def is_org_storage_write_enabled() -> bool:
    """
    Check if org storage writes are enabled.

    Returns:
        True if ORG_STORAGE_WRITE_ENABLED is "true" (case-insensitive),
        False otherwise (default: disabled).

    Examples:
        ORG_STORAGE_WRITE_ENABLED="true"  → True
        ORG_STORAGE_WRITE_ENABLED="True"  → True
        ORG_STORAGE_WRITE_ENABLED="false" → False
        ORG_STORAGE_WRITE_ENABLED=""      → False
        (not set)                         → False
    """
    value = os.getenv("ORG_STORAGE_WRITE_ENABLED", "false")
    return value.lower() == "true"


def make_portfolio_run_summary_path(run_id: str) -> str:
    """
    Generate GCS object path for portfolio run summary.

    Args:
        run_id: Portfolio run ID (UUID)

    Returns:
        Object path relative to bucket root.

    Example:
        make_portfolio_run_summary_path("abc-123")
        → "portfolio/runs/abc-123/summary.json"
    """
    return f"portfolio/runs/{run_id}/summary.json"


def make_portfolio_run_repo_path(run_id: str, repo_id: str) -> str:
    """
    Generate GCS object path for per-repo portfolio results.

    Args:
        run_id: Portfolio run ID (UUID)
        repo_id: Repository identifier (e.g., "bobs-brain")

    Returns:
        Object path relative to bucket root.

    Example:
        make_portfolio_run_repo_path("abc-123", "bobs-brain")
        → "portfolio/runs/abc-123/per-repo/bobs-brain.json"
    """
    return f"portfolio/runs/{run_id}/per-repo/{repo_id}.json"


def make_swe_agent_run_path(agent_name: str, run_id: str) -> str:
    """
    Generate GCS object path for single-repo SWE agent runs (future use).

    Args:
        agent_name: Agent name (e.g., "iam-adk")
        run_id: Run ID (UUID)

    Returns:
        Object path relative to bucket root.

    Example:
        make_swe_agent_run_path("iam-adk", "xyz-789")
        → "swe/agents/iam-adk/runs/xyz-789.json"
    """
    return f"swe/agents/{agent_name}/runs/{run_id}.json"


# ==============================================================================
# Usage Examples
# ==============================================================================
#
# Check configuration:
#     bucket = get_org_storage_bucket()
#     enabled = is_org_storage_write_enabled()
#     if enabled and bucket:
#         print(f"Org storage enabled: gs://{bucket}/")
#
# Generate paths:
#     summary_path = make_portfolio_run_summary_path("run-123")
#     repo_path = make_portfolio_run_repo_path("run-123", "bobs-brain")
#
# ==============================================================================
