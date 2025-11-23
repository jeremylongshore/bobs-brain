#!/usr/bin/env python3
"""
Inline Source Deployment Script for Vertex AI Agent Engine

This script deploys ADK agents to Vertex AI Agent Engine using the inline
source deployment pattern (6767-INLINE standard). It packages agent source
code directly from the repository and deploys to Agent Engine without
requiring Docker containers or serialized artifacts.

Deployment Pattern (6767-INLINE):
1. Source code pushed to git repository
2. This script packages Python modules from agents/ directory
3. Vertex AI Agent Engine API receives inline source configuration
4. Agent Engine packages and executes agents/{agent}/agent.py::app

Usage:
    # Dry-run mode (validates config without deploying)
    python scripts/deploy_inline_source.py \\
        --agent bob \\
        --project-id bobs-brain-dev \\
        --region us-central1 \\
        --env dev \\
        --app-version 0.10.0 \\
        --dry-run

    # Real deployment (requires GCP credentials and WIF setup)
    python scripts/deploy_inline_source.py \\
        --agent bob \\
        --project-id bobs-brain-dev \\
        --region us-central1 \\
        --env dev \\
        --app-version 0.10.0

Exit Codes:
    0 - Success (dry-run or real deployment succeeded)
    1 - Deployment API error
    2 - Configuration error (missing/invalid args)
    3 - GCP client not available (expected in local/non-GCP environments)

References:
    - 000-docs/148-AA-REPT-phase-19-agent-engine-dev-deployment.md
    - 000-docs/6767-INLINE-DR-STND-inline-source-deployment-for-vertex-agent-engine.md
    - 000-docs/127-DR-STND-agent-engine-entrypoints.md
"""

import argparse
import os
import sys
from typing import Dict, Optional, Tuple


# ==============================================================================
# Agent Configuration Mapping
# ==============================================================================

def get_agent_config(agent_name: str) -> Optional[Dict[str, str]]:
    """
    Map logical agent names to Agent Engine entrypoint configuration.

    Args:
        agent_name: Logical agent name (e.g., 'bob', 'iam-senior-adk-devops-lead')

    Returns:
        Dict with keys:
            - entrypoint_module: Python module path (e.g., 'agents.bob.agent')
            - entrypoint_object: Object name within module (e.g., 'app')
            - display_name_pattern: Human-readable name pattern for Agent Engine
            - agent_id_pattern: Resource ID pattern for Agent Engine

        Returns None if agent_name is not recognized.
    """
    agent_configs = {
        "bob": {
            "entrypoint_module": "agents.bob.agent",
            "entrypoint_object": "app",
            "display_name_pattern": "{app_name}-{env}",
            "agent_id_pattern": "{app_name}-{env}",
            "description": "Bob - Main orchestrator agent for bobs-brain",
        },
        "iam-senior-adk-devops-lead": {
            # NOTE: Use underscored directory path for import, not hyphenated
            "entrypoint_module": "agents.iam_senior_adk_devops_lead.agent",
            "entrypoint_object": "app",
            "display_name_pattern": "{app_name}-foreman-{env}",
            "agent_id_pattern": "{app_name}-foreman-{env}",
            "description": "Foreman - IAM Senior ADK DevOps Lead (A2A orchestrator)",
        },
        # Future agents can be added here
        # "iam-adk": {...},
        # "iam-issue": {...},
    }

    return agent_configs.get(agent_name)


def build_agent_display_name(agent_config: Dict[str, str], app_name: str, env: str) -> str:
    """
    Build Agent Engine display name from pattern and variables.

    Args:
        agent_config: Agent configuration dict from get_agent_config()
        app_name: Application name (e.g., 'bobs-brain')
        env: Environment (e.g., 'dev', 'staging', 'prod')

    Returns:
        Formatted display name (e.g., 'bobs-brain-dev', 'bobs-brain-foreman-dev')
    """
    pattern = agent_config.get("display_name_pattern", "{app_name}-{env}")
    return pattern.format(app_name=app_name, env=env)


def build_agent_resource_id(agent_config: Dict[str, str], app_name: str, env: str) -> str:
    """
    Build Agent Engine resource ID from pattern and variables.

    Args:
        agent_config: Agent configuration dict from get_agent_config()
        app_name: Application name (e.g., 'bobs-brain')
        env: Environment (e.g., 'dev', 'staging', 'prod')

    Returns:
        Resource ID suitable for Agent Engine (e.g., 'bobs-brain-dev')
    """
    pattern = agent_config.get("agent_id_pattern", "{app_name}-{env}")
    return pattern.format(app_name=app_name, env=env)


# ==============================================================================
# Dry-Run Mode
# ==============================================================================

def dry_run_deploy(args: argparse.Namespace) -> int:
    """
    Dry-run mode: Validate configuration and print what would be deployed.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    print("=" * 80)
    print("DRY-RUN MODE: Inline Source Deployment Configuration")
    print("=" * 80)
    print()

    # Get agent configuration
    agent_config = get_agent_config(args.agent)
    if not agent_config:
        print(f"❌ ERROR: Unknown agent '{args.agent}'")
        print(f"   Supported agents: bob, iam-senior-adk-devops-lead")
        return 2

    # Build display name and resource ID
    app_name = "bobs-brain"  # Could be made configurable if needed
    display_name = build_agent_display_name(agent_config, app_name, args.env)
    resource_id = build_agent_resource_id(agent_config, app_name, args.env)

    # Print configuration
    print("GCP Configuration:")
    print(f"  Project ID:       {args.project_id}")
    print(f"  Region:           {args.region}")
    print(f"  Environment:      {args.env}")
    print()

    print("Agent Configuration:")
    print(f"  Agent Name:       {args.agent}")
    print(f"  Display Name:     {display_name}")
    print(f"  Resource ID:      {resource_id}")
    print(f"  Description:      {agent_config['description']}")
    print()

    print("Inline Source Configuration (6767-INLINE):")
    print(f"  Entrypoint Module:  {agent_config['entrypoint_module']}")
    print(f"  Entrypoint Object:  {agent_config['entrypoint_object']}")
    print(f"  Source Packages:    ['agents', 'deployment']")
    print(f"  Requirements File:  requirements.txt")
    print()

    print("Deployment Details:")
    print(f"  App Version:      {args.app_version}")
    print(f"  Deployment Method: Inline Source (6767-INLINE)")
    print(f"  Pattern:          App (lazy-loading, 6767-LAZY)")
    print()

    # Expected Agent Engine resource name
    expected_resource_name = (
        f"projects/{args.project_id}/locations/{args.region}"
        f"/reasoningEngines/{resource_id}"
    )
    print("Expected Agent Engine Resource:")
    print(f"  Resource Name:    {expected_resource_name}")
    print()

    # Print what would happen
    print("What Would Happen (if not dry-run):")
    print("  1. Initialize Vertex AI client")
    print("  2. Package source code from repository")
    print("  3. Call Vertex AI Agent Engine API:")
    print(f"     - Create or update ReasoningEngine: {display_name}")
    print(f"     - Deploy inline source from {agent_config['entrypoint_module']}::app")
    print("  4. Wait for deployment to complete")
    print("  5. Return agent ID and endpoint URL")
    print()

    print("=" * 80)
    print("✅ DRY-RUN COMPLETE: Configuration valid")
    print("=" * 80)
    print()
    print("To deploy for real:")
    print("  1. Ensure GCP credentials are configured (WIF or gcloud auth)")
    print("  2. Run without --dry-run flag")
    print()

    return 0


# ==============================================================================
# Real Deployment (Stubbed)
# ==============================================================================

def deploy_inline_source(args: argparse.Namespace) -> int:
    """
    Deploy agent to Vertex AI Agent Engine using inline source pattern.

    This function is structurally ready for Agent Engine deployment but
    currently stubbed. It will check for GCP client availability and either:
    - Deploy the agent if clients are available, OR
    - Print clear error message if GCP environment not configured

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code:
            0 - Deployment succeeded
            1 - Deployment API error
            3 - GCP client not available (expected in local environments)
    """
    print("=" * 80)
    print("INLINE SOURCE DEPLOYMENT: Vertex AI Agent Engine")
    print("=" * 80)
    print()

    # Get agent configuration
    agent_config = get_agent_config(args.agent)
    if not agent_config:
        print(f"❌ ERROR: Unknown agent '{args.agent}'", file=sys.stderr)
        print(f"   Supported agents: bob, iam-senior-adk-devops-lead", file=sys.stderr)
        return 2

    # Build display name and resource ID
    app_name = "bobs-brain"
    display_name = build_agent_display_name(agent_config, app_name, args.env)
    resource_id = build_agent_resource_id(agent_config, app_name, args.env)

    # Print deployment configuration
    print("Deployment Configuration:")
    print(f"  Project ID:       {args.project_id}")
    print(f"  Region:           {args.region}")
    print(f"  Environment:      {args.env}")
    print(f"  Agent:            {args.agent}")
    print(f"  Display Name:     {display_name}")
    print(f"  Resource ID:      {resource_id}")
    print(f"  App Version:      {args.app_version}")
    print()

    # Check for GCP client availability
    try:
        import google.cloud.aiplatform as aiplatform
        print("✅ Google Cloud AI Platform client available")
    except ImportError:
        print("⚠️  WARNING: google.cloud.aiplatform not available", file=sys.stderr)
        print("", file=sys.stderr)
        print("   This is expected in local/non-GCP environments.", file=sys.stderr)
        print("   Real deployment requires:", file=sys.stderr)
        print("     1. GCP credentials configured (WIF or gcloud auth)", file=sys.stderr)
        print("     2. google-cloud-aiplatform Python package installed", file=sys.stderr)
        print("     3. Vertex AI API enabled in project", file=sys.stderr)
        print("", file=sys.stderr)
        print("   Run with --dry-run to validate configuration without deploying.", file=sys.stderr)
        print("", file=sys.stderr)
        return 3

    # Build inline source deployment request structure
    print("Building Inline Source Deployment Request...")
    print()

    # Entrypoint configuration
    entrypoint_module = agent_config["entrypoint_module"]
    entrypoint_object = agent_config["entrypoint_object"]
    print(f"  Entrypoint: {entrypoint_module}::{entrypoint_object}")

    # Source packages (inline source pattern - no Docker)
    source_packages = ["agents", "deployment"]
    print(f"  Source Packages: {source_packages}")

    # Requirements file
    requirements_file = "requirements.txt"
    print(f"  Requirements: {requirements_file}")
    print()

    # Expected Agent Engine resource name
    expected_resource_name = (
        f"projects/{args.project_id}/locations/{args.region}"
        f"/reasoningEngines/{resource_id}"
    )

    # TODO: Implement actual Agent Engine API call
    # This is where the real deployment logic will go when GCP access is available
    print("=" * 80)
    print("⚠️  DEPLOYMENT STUBBED (Task 2)")
    print("=" * 80)
    print()
    print("The deployment request structure is ready, but actual API calls")
    print("are not yet implemented. When GCP access is available, this function")
    print("will call the Vertex AI Agent Engine API to deploy the agent.")
    print()
    print("TODO (for future implementation):")
    print("  1. Initialize Vertex AI client:")
    print(f"     aiplatform.init(project='{args.project_id}', location='{args.region}')")
    print()
    print("  2. Build ReasoningEngine configuration:")
    print("     - Package source code from repository")
    print("     - Configure inline source entrypoint")
    print("     - Set display name and metadata")
    print()
    print("  3. Create or update ReasoningEngine resource:")
    print("     - Check if agent already exists (get by resource_id)")
    print("     - If exists: update existing agent")
    print("     - If not: create new agent")
    print()
    print("  4. Wait for deployment operation to complete")
    print()
    print("  5. Return deployed agent resource name:")
    print(f"     {expected_resource_name}")
    print()
    print("API Call Structure (sketch):")
    print("  try:")
    print("      # Initialize Vertex AI")
    print(f"      aiplatform.init(project='{args.project_id}', location='{args.region}')")
    print()
    print("      # Build inline source configuration")
    print("      inline_source_config = {")
    print(f"          'entrypoint_module': '{entrypoint_module}',")
    print(f"          'entrypoint_object': '{entrypoint_object}',")
    print(f"          'source_packages': {source_packages},")
    print(f"          'requirements_file': '{requirements_file}',")
    print("      }")
    print()
    print("      # Create or update ReasoningEngine")
    print("      # reasoning_engine = aiplatform.ReasoningEngine.create(...)")
    print("      # OR")
    print("      # reasoning_engine = aiplatform.ReasoningEngine.get(resource_id)")
    print("      # reasoning_engine.update(...)")
    print()
    print("      # Wait for operation to complete")
    print("      # operation.result()")
    print()
    print("      return 0  # Success")
    print()
    print("  except Exception as e:")
    print("      print(f'❌ Deployment failed: {e}', file=sys.stderr)")
    print("      return 1  # API error")
    print()
    print("=" * 80)
    print()
    print("Current Status: Deployment request validated, API calls stubbed")
    print("Next Step: Complete GCP/WIF setup and implement actual API calls")
    print()

    # For now, return exit code 3 (GCP client available but deployment stubbed)
    return 3


# ==============================================================================
# Main Entry Point
# ==============================================================================

def main() -> int:
    """
    Main entry point for inline source deployment script.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(
        description="Deploy ADK agents to Vertex AI Agent Engine using inline source pattern",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Required arguments
    parser.add_argument(
        "--agent",
        required=True,
        choices=["bob", "iam-senior-adk-devops-lead"],
        help="Agent to deploy (bob or iam-senior-adk-devops-lead)"
    )

    parser.add_argument(
        "--project-id",
        required=True,
        help="GCP project ID (e.g., bobs-brain-dev)"
    )

    parser.add_argument(
        "--region",
        required=True,
        default="us-central1",
        help="GCP region (e.g., us-central1)"
    )

    parser.add_argument(
        "--env",
        required=True,
        choices=["dev", "staging", "prod"],
        help="Deployment environment (dev, staging, or prod)"
    )

    parser.add_argument(
        "--app-version",
        required=True,
        help="Application version (e.g., 0.10.0)"
    )

    # Optional flags
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without deploying (default: False)"
    )

    # Parse arguments
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse calls sys.exit() on error or --help
        return e.code if isinstance(e.code, int) else 2

    # Validate agent configuration exists
    agent_config = get_agent_config(args.agent)
    if not agent_config:
        print(f"❌ ERROR: Unknown agent '{args.agent}'", file=sys.stderr)
        print("   Supported agents: bob, iam-senior-adk-devops-lead", file=sys.stderr)
        return 2

    # Run in appropriate mode
    if args.dry_run:
        return dry_run_deploy(args)
    else:
        # Real deployment (stubbed but structurally ready)
        return deploy_inline_source(args)


if __name__ == "__main__":
    sys.exit(main())
