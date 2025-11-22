#!/usr/bin/env python3
"""
Agent Engine Deployment Smoke Test

Phase 18: Post-deployment health check for agents running in Vertex AI Agent Engine.

This script performs a minimal "is it alive?" check by invoking a deployed agent
with a trivial request and verifying it responds successfully.

Usage:
    # Test bob in dev
    python scripts/smoke_test_agent_engine.py \
      --project bobs-brain-dev \
      --location us-central1 \
      --agent bob \
      --env dev

    # Test foreman with environment variables
    export PROJECT_ID=bobs-brain-dev
    export LOCATION=us-central1
    export AGENT_NAME=iam-senior-adk-devops-lead
    export ENV=dev
    python scripts/smoke_test_agent_engine.py

Exit Codes:
    0 - Agent responded successfully
    1 - Agent failed to respond or returned error
    2 - Configuration error (missing params, etc.)

References:
    - 000-docs/145-NOTE-agent-engine-dev-deployment-prereqs.md
    - 000-docs/146-AA-REPT-phase-17-a2a-wiring-and-agent-engine-dev-prep.md
"""

import argparse
import os
import sys
import time
from typing import Dict, Any, Optional

# Try to import GCP libraries (may not be available locally)
try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform import gapic
    GCP_AVAILABLE = True
except ImportError:
    print("⚠️  Google Cloud AI Platform libraries not available", file=sys.stderr)
    print("   Install with: pip install google-cloud-aiplatform", file=sys.stderr)
    GCP_AVAILABLE = False


class Colors:
    """Terminal colors for output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str) -> None:
    """Print section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.RESET}\n")


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_failure(text: str) -> None:
    """Print failure message."""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {text}")


def get_smoke_test_prompt(agent_name: str) -> str:
    """
    Get minimal smoke test prompt for agent.

    Args:
        agent_name: Name of agent (bob, iam-senior-adk-devops-lead, etc.)

    Returns:
        Simple test prompt that should get a response
    """
    prompts = {
        "bob": "Hello Bob. Please respond with a simple greeting to confirm you're operational.",
        "iam-senior-adk-devops-lead": "Hello foreman. Please confirm you can receive requests.",
        "iam-adk": "Hello iam-adk specialist. Please confirm you're operational.",
    }

    return prompts.get(
        agent_name,
        f"Hello {agent_name}. Please respond to confirm you're operational."
    )


def invoke_agent_engine(
    project_id: str,
    location: str,
    agent_engine_id: str,
    prompt: str
) -> tuple[bool, Optional[Dict[str, Any]]]:
    """
    Invoke agent via Vertex AI Agent Engine API.

    Args:
        project_id: GCP project ID
        location: GCP region
        agent_engine_id: Agent Engine resource ID
        prompt: Input prompt

    Returns:
        (success, response_data)
    """
    if not GCP_AVAILABLE:
        print_failure("Google Cloud libraries not available - cannot invoke agent")
        return False, None

    try:
        print_info(f"Invoking agent at {location}/{agent_engine_id}...")

        # Initialize AI Platform
        aiplatform.init(project=project_id, location=location)

        # Create agent client
        client = aiplatform.gapic.ReasoningEngineServiceClient(
            client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
        )

        # Construct resource name
        resource_name = f"projects/{project_id}/locations/{location}/reasoningEngines/{agent_engine_id}"

        # Invoke agent (simplified - actual API may vary)
        request = gapic.QueryReasoningEngineRequest(
            name=resource_name,
            input={"query": prompt}
        )

        response = client.query_reasoning_engine(request=request)

        print_success("Agent responded successfully")

        # Parse response
        result_data = {
            "status": "success",
            "response": str(response),
            "latency_ms": None  # Would need timing logic
        }

        return True, result_data

    except Exception as e:
        print_failure(f"Failed to invoke agent: {e}")
        return False, {"error": str(e)}


def run_smoke_test(args: argparse.Namespace) -> int:
    """
    Run smoke test for deployed agent.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 = success, 1 = failure, 2 = config error)
    """
    print_header("AGENT ENGINE SMOKE TEST")
    print_info(f"Project: {args.project}")
    print_info(f"Location: {args.location}")
    print_info(f"Agent: {args.agent}")
    print_info(f"Environment: {args.env}")
    print()

    # Validate configuration
    if not args.project:
        print_failure("Missing required parameter: project")
        return 2

    if not args.agent_engine_id:
        print_warning("AGENT_ENGINE_ID not provided - using default naming convention")
        # Try to construct ID from agent name and environment
        args.agent_engine_id = f"{args.agent}-{args.env}"
        print_info(f"Assuming Agent Engine ID: {args.agent_engine_id}")

    # Get test prompt
    test_prompt = get_smoke_test_prompt(args.agent)
    print_info(f"Test prompt: \"{test_prompt[:60]}...\"")
    print()

    # Invoke agent
    start_time = time.time()
    success, response = invoke_agent_engine(
        project_id=args.project,
        location=args.location,
        agent_engine_id=args.agent_engine_id,
        prompt=test_prompt
    )
    duration_ms = int((time.time() - start_time) * 1000)

    # Report results
    print()
    print_header("SMOKE TEST RESULTS")

    if success:
        print_success("Agent responded successfully")
        print_info(f"Response time: {duration_ms}ms")
        if response:
            print_info(f"Response data: {str(response)[:100]}...")
        print()
        print_success("✅ SMOKE TEST PASSED")
        return 0
    else:
        print_failure("Agent did not respond successfully")
        print_info(f"Attempted in: {duration_ms}ms")
        if response and "error" in response:
            print_failure(f"Error: {response['error']}")
        print()
        print_failure("❌ SMOKE TEST FAILED")
        return 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Smoke test for Vertex AI Agent Engine deployments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--project",
        default=os.getenv("PROJECT_ID"),
        help="GCP project ID (or set PROJECT_ID env var)"
    )

    parser.add_argument(
        "--location",
        default=os.getenv("LOCATION", "us-central1"),
        help="GCP region (or set LOCATION env var)"
    )

    parser.add_argument(
        "--agent",
        default=os.getenv("AGENT_NAME", "bob"),
        help="Agent name (bob, iam-senior-adk-devops-lead, etc.)"
    )

    parser.add_argument(
        "--agent-engine-id",
        default=os.getenv("AGENT_ENGINE_ID"),
        help="Agent Engine resource ID (or set AGENT_ENGINE_ID env var)"
    )

    parser.add_argument(
        "--env",
        default=os.getenv("ENV", "dev"),
        choices=["dev", "staging", "prod"],
        help="Deployment environment"
    )

    args = parser.parse_args()

    try:
        return run_smoke_test(args)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
        return 130
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
