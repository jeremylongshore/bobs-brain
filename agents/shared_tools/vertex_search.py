"""
Vertex AI Search Tool Factory

This module provides Vertex AI Search tools configured for the org knowledge hub.
Bob and foreman use these tools to access the centralized RAG knowledge base.
"""

import os
import logging
import yaml
from typing import Any, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def load_vertex_search_config() -> Dict[str, Any]:
    """
    Load Vertex AI Search configuration from YAML file.

    Returns:
        Configuration dictionary for current environment
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "vertex_search.yaml"

    if not config_path.exists():
        logger.warning(f"Vertex Search config not found at {config_path}")
        return {}

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_current_environment() -> str:
    """
    Determine the current environment from env variables.

    Priority:
    1. APP_ENV
    2. ENVIRONMENT
    3. Default to "staging" (safe default)

    Returns:
        Environment string: "production", "staging", or "development"
    """
    env = os.getenv("APP_ENV")
    if not env:
        env = os.getenv("ENVIRONMENT")
    if not env:
        env = "staging"  # Safe default
        logger.info("No APP_ENV or ENVIRONMENT set, defaulting to staging")

    # Normalize environment names
    env = env.lower()
    if env in ["prod", "production"]:
        return "production"
    elif env in ["dev", "development"]:
        return "development"
    else:
        return "staging"


def get_bob_vertex_search_tool(env: Optional[str] = None) -> Any:
    """
    Get Vertex AI Search tool configured for Bob and foreman.

    This tool provides RAG capabilities using the org knowledge hub.

    Args:
        env: Environment override. If None, auto-detect from env vars.

    Returns:
        VertexAiSearchToolset configured for the current environment
    """
    # Determine environment
    if env is None:
        env = get_current_environment()

    logger.info(f"Configuring Vertex AI Search for environment: {env}")

    # Load configuration
    config = load_vertex_search_config()

    # Check for migration flag
    use_org_knowledge = os.getenv("USE_ORG_KNOWLEDGE", "false").lower() == "true"

    if not use_org_knowledge:
        # Use legacy configuration for backwards compatibility
        logger.info("Using legacy Vertex Search configuration (USE_ORG_KNOWLEDGE=false)")

        # Return legacy tool configuration
        # TODO: Import actual ADK VertexAiSearchToolset when available
        # from google.adk.toolsets import VertexAiSearchToolset
        # return VertexAiSearchToolset(
        #     project_id="bobs-brain",
        #     location="us",
        #     datastore_id="bob-vertex-agent-datastore"
        # )

        # Stub for now
        return {
            "type": "vertex_search",
            "config": {
                "project_id": "bobs-brain",
                "location": "us",
                "datastore_id": "bob-vertex-agent-datastore",
                "legacy": True
            }
        }

    # Use new org knowledge hub configuration
    if "environments" not in config or env not in config["environments"]:
        logger.error(f"No configuration found for environment: {env}")
        return None

    env_config = config["environments"][env]
    datastore_config = env_config["datastore"]

    logger.info(f"Using datastore: {datastore_config['id']} in project: {datastore_config['project_id']}")

    # TODO: Import and use actual ADK VertexAiSearchToolset
    # This is where the real ADK tool would be created:
    #
    # from google.adk.toolsets import VertexAiSearchToolset
    #
    # tool = VertexAiSearchToolset(
    #     project_id=datastore_config["project_id"],
    #     location=datastore_config["location"],
    #     datastore_id=datastore_config["id"]
    # )
    #
    # # Optional: Configure search parameters
    # if "search" in env_config:
    #     search_config = env_config["search"]
    #     tool.set_refresh_schedule(search_config.get("refresh_schedule", "daily"))
    #
    # return tool

    # For now, return a configuration stub
    return {
        "type": "vertex_search",
        "config": {
            "project_id": datastore_config["project_id"],
            "location": datastore_config["location"],
            "datastore_id": datastore_config["id"],
            "source_uri": env_config["source"]["uri_pattern"],
            "environment": env
        }
    }


def get_foreman_vertex_search_tool(env: Optional[str] = None) -> Any:
    """
    Get Vertex AI Search tool for iam-senior-adk-devops-lead (foreman).

    Currently uses the same configuration as Bob.
    Future: Could have foreman-specific search parameters.

    Args:
        env: Environment override. If None, auto-detect from env vars.

    Returns:
        VertexAiSearchToolset configured for the foreman
    """
    # For now, foreman uses the same tool as Bob
    return get_bob_vertex_search_tool(env)


def get_datastore_info(env: Optional[str] = None) -> Dict[str, str]:
    """
    Get datastore information for the current environment.

    Useful for debugging and configuration verification.

    Args:
        env: Environment override. If None, auto-detect from env vars.

    Returns:
        Dictionary with datastore configuration details
    """
    if env is None:
        env = get_current_environment()

    config = load_vertex_search_config()

    # Check migration flag
    use_org_knowledge = os.getenv("USE_ORG_KNOWLEDGE", "false").lower() == "true"

    if not use_org_knowledge and "legacy" in config:
        legacy = config["legacy"]
        return {
            "environment": "legacy",
            "datastore_id": legacy["datastore"]["id"],
            "project_id": legacy["datastore"]["project_id"],
            "location": legacy["datastore"]["location"],
            "bucket": legacy["source"]["bucket"],
            "document_count": str(legacy["source"]["documents"])
        }

    if "environments" not in config or env not in config["environments"]:
        return {"error": f"No configuration for environment: {env}"}

    env_config = config["environments"][env]

    return {
        "environment": env,
        "datastore_id": env_config["datastore"]["id"],
        "project_id": env_config["datastore"]["project_id"],
        "location": env_config["datastore"]["location"],
        "source_bucket": env_config["source"]["bucket"],
        "source_prefix": env_config["source"]["prefix"],
        "uri_pattern": env_config["source"]["uri_pattern"]
    }


# Export the main factory functions
__all__ = [
    "get_bob_vertex_search_tool",
    "get_foreman_vertex_search_tool",
    "get_current_environment",
    "get_datastore_info"
]