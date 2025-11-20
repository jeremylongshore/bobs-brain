"""
Agent Engine Configuration Module (Phase AE1)

This module defines the Vertex AI Agent Engine deployment topology
for Bob's Brain across all environments (dev, staging, prod).

NO DEPLOYMENT OPERATIONS - This is config-only.

Environment Strategy:
- dev: Rapid iteration, may use local stubs for iam-* agents
- staging: Pre-production validation with full Agent Engine deployment
- prod: Production workloads with current/next-gen Bob versions

Related Docs:
- 000-docs/6767-101-AT-ARCH-agent-engine-topology-and-envs.md
"""

from dataclasses import dataclass
from typing import Dict, Optional, Literal

# Type alias for environment names
Environment = Literal["dev", "staging", "prod"]


@dataclass
class AgentEngineConfig:
    """Configuration for a single agent in Vertex AI Agent Engine."""

    reasoning_engine_id: str
    """Full reasoning engine resource name: projects/PROJECT_ID/locations/REGION/reasoningEngines/ID"""

    region: str
    """GCP region where the agent is deployed (e.g., us-central1)"""

    spiffe_id: str
    """SPIFFE ID for agent identity: spiffe://trust-domain/agent/name/env/region/version"""

    notes: Optional[str] = None
    """Optional notes about this agent deployment"""


# ==============================================================================
# DEVELOPMENT ENVIRONMENT
# ==============================================================================

DEV_CONFIG: Dict[str, AgentEngineConfig] = {
    "bob": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/BOB_DEV_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.9.0",
        notes="Dev instance for rapid iteration and testing"
    ),
    "foreman": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/FOREMAN_DEV_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain-foreman/dev/us-central1/0.9.0",
        notes="Dev foreman for SWE pipeline testing"
    ),
    # iam-adk and iam-issue use local stubs in dev (not deployed to Agent Engine)
}


# ==============================================================================
# STAGING ENVIRONMENT
# ==============================================================================

STAGING_CONFIG: Dict[str, AgentEngineConfig] = {
    "bob": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/BOB_STAGING_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain/staging/us-central1/0.9.0",
        notes="Pre-production validation instance"
    ),
    "foreman": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/FOREMAN_STAGING_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain-foreman/staging/us-central1/0.9.0",
        notes="Pre-production foreman with full A2A protocol"
    ),
    "iam-adk": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/IAM_ADK_STAGING_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain-iam-adk/staging/us-central1/0.9.0",
        notes="ADK design specialist (staging)"
    ),
    "iam-issue": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/IAM_ISSUE_STAGING_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain-iam-issue/staging/us-central1/0.9.0",
        notes="Issue management specialist (staging)"
    ),
}


# ==============================================================================
# PRODUCTION ENVIRONMENT
# ==============================================================================

PROD_CONFIG: Dict[str, AgentEngineConfig] = {
    "bob_current": AgentEngineConfig(
        reasoning_engine_id="projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/0.8.0",
        notes="⭐ CURRENT CANONICAL BOB (pre-ADK architecture) - Active production"
    ),
    "bob_next_gen": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/BOB_PROD_NEXT_GEN_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/0.9.0",
        notes="Next-gen ADK Bob (for migration phases: Shadow → Canary → Active)"
    ),
    "foreman": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/FOREMAN_PROD_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain-foreman/prod/us-central1/0.9.0",
        notes="Production foreman for SWE department"
    ),
    "iam-adk": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/IAM_ADK_PROD_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain-iam-adk/prod/us-central1/0.9.0",
        notes="ADK design specialist (production)"
    ),
    "iam-issue": AgentEngineConfig(
        reasoning_engine_id="projects/PROJECT_ID/locations/us-central1/reasoningEngines/IAM_ISSUE_PROD_PLACEHOLDER",
        region="us-central1",
        spiffe_id="spiffe://intent.solutions/agent/bobs-brain-iam-issue/prod/us-central1/0.9.0",
        notes="Issue management specialist (production)"
    ),
}


# ==============================================================================
# ENVIRONMENT REGISTRY
# ==============================================================================

ALL_ENVIRONMENTS: Dict[Environment, Dict[str, AgentEngineConfig]] = {
    "dev": DEV_CONFIG,
    "staging": STAGING_CONFIG,
    "prod": PROD_CONFIG,
}


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_agent_engine_config(
    env: Environment,
    agent_role: str
) -> Optional[AgentEngineConfig]:
    """
    Get Agent Engine configuration for a specific environment and agent role.

    Args:
        env: Environment name (dev, staging, prod)
        agent_role: Agent role name (bob, foreman, iam-adk, iam-issue, etc.)
                   For prod Bob, use "bob_current" or "bob_next_gen"

    Returns:
        AgentEngineConfig if found, None if agent not deployed to Agent Engine
        in that environment (e.g., iam-adk in dev uses local stub)

    Example:
        >>> config = get_agent_engine_config("prod", "bob_current")
        >>> print(config.reasoning_engine_id)
        projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448
    """
    if env not in ALL_ENVIRONMENTS:
        return None

    env_config = ALL_ENVIRONMENTS[env]
    return env_config.get(agent_role)


def get_reasoning_engine_id(
    env: Environment,
    agent_role: str
) -> Optional[str]:
    """
    Get just the reasoning engine ID for an agent.

    Args:
        env: Environment name
        agent_role: Agent role name

    Returns:
        Full reasoning engine resource name, or None if not deployed
    """
    config = get_agent_engine_config(env, agent_role)
    return config.reasoning_engine_id if config else None


def list_agents_in_environment(env: Environment) -> Dict[str, AgentEngineConfig]:
    """
    List all agents deployed to Agent Engine in a specific environment.

    Args:
        env: Environment name

    Returns:
        Dictionary mapping agent role to config

    Example:
        >>> agents = list_agents_in_environment("staging")
        >>> print([role for role in agents.keys()])
        ['bob', 'foreman', 'iam-adk', 'iam-issue']
    """
    return ALL_ENVIRONMENTS.get(env, {})


def is_agent_deployed_to_engine(
    env: Environment,
    agent_role: str
) -> bool:
    """
    Check if an agent is deployed to Agent Engine (vs local stub).

    Args:
        env: Environment name
        agent_role: Agent role name

    Returns:
        True if agent has Agent Engine deployment, False otherwise

    Example:
        >>> is_agent_deployed_to_engine("dev", "iam-adk")
        False  # Uses local stub in dev
        >>> is_agent_deployed_to_engine("staging", "iam-adk")
        True  # Real Agent Engine deployment
    """
    return get_agent_engine_config(env, agent_role) is not None


def get_spiffe_id(
    env: Environment,
    agent_role: str
) -> Optional[str]:
    """
    Get the SPIFFE ID for an agent.

    Args:
        env: Environment name
        agent_role: Agent role name

    Returns:
        SPIFFE ID string, or None if agent not deployed
    """
    config = get_agent_engine_config(env, agent_role)
    return config.spiffe_id if config else None


# ==============================================================================
# CONFIGURATION VALIDATION
# ==============================================================================

def validate_config() -> None:
    """
    Validate that all required configuration is present.

    Checks:
    - All environments defined
    - All agents have valid reasoning engine IDs
    - All SPIFFE IDs follow correct format
    - Current canonical Bob (…6448) is marked in prod

    Raises:
        ValueError: If configuration is invalid
    """
    # Check all environments exist
    required_envs: list[Environment] = ["dev", "staging", "prod"]
    for env in required_envs:
        if env not in ALL_ENVIRONMENTS:
            raise ValueError(f"Missing environment config: {env}")

    # Check current canonical Bob is in prod
    prod_bob_current = PROD_CONFIG.get("bob_current")
    if not prod_bob_current:
        raise ValueError("Missing bob_current in PROD_CONFIG")

    if "5828234061910376448" not in prod_bob_current.reasoning_engine_id:
        raise ValueError(
            f"bob_current should reference canonical Bob ...6448, "
            f"got: {prod_bob_current.reasoning_engine_id}"
        )

    # Check all SPIFFE IDs have correct format
    for env_name, env_config in ALL_ENVIRONMENTS.items():
        for agent_role, agent_config in env_config.items():
            if not agent_config.spiffe_id.startswith("spiffe://intent.solutions/agent/"):
                raise ValueError(
                    f"Invalid SPIFFE ID format for {env_name}/{agent_role}: "
                    f"{agent_config.spiffe_id}"
                )

    print("✅ Agent Engine configuration valid")


# Run validation on import (in non-production contexts)
if __name__ == "__main__":
    validate_config()
