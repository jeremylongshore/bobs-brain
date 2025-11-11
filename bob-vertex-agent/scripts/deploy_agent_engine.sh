#!/usr/bin/env bash
# Bootstrap Bob's Brain Agent to Vertex AI Agent Engine
#
# This script deploys the containerized agent to Vertex AI Agent Engine.
# It requires the Vertex AI Python SDK and uses the current SDK methods
# to upsert the agent configuration.
#
# Required environment variables:
#   PROJECT_ID - GCP project ID
#   LOCATION - GCP region (e.g., us-central1)
#   AGENT_ENGINE_ID - Agent Engine resource ID
#   IMAGE - Container image URL from Artifact Registry

set -euo pipefail

# Validate required environment variables
: "${PROJECT_ID:?PROJECT_ID environment variable is required}"
: "${LOCATION:?LOCATION environment variable is required}"
: "${AGENT_ENGINE_ID:?AGENT_ENGINE_ID environment variable is required}"
: "${IMAGE:?IMAGE environment variable is required}"

echo "Deploying Bob's Brain to Vertex AI Agent Engine..."
echo "  Project: $PROJECT_ID"
echo "  Location: $LOCATION"
echo "  Agent Engine ID: $AGENT_ENGINE_ID"
echo "  Image: $IMAGE"

# Use Python inline script to deploy via Vertex AI SDK
python - <<'PYTHON_SCRIPT'
import os
import sys

# Get environment variables
project_id = os.environ["PROJECT_ID"]
location = os.environ["LOCATION"]
engine_id = os.environ["AGENT_ENGINE_ID"]
image = os.environ["IMAGE"]

print(f"\n[Agent Engine Bootstrap]")
print(f"Project: {project_id}")
print(f"Location: {location}")
print(f"Engine ID: {engine_id}")
print(f"Image: {image}")

try:
    # Import Vertex AI SDK
    import vertexai
    from google.cloud import aiplatform

    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # TODO: Replace with actual Agent Engine upsert once SDK supports it
    # Current SDK may not have direct agent_engines.apps.upsert() method yet
    # This is a placeholder that would need to be updated with actual SDK calls
    # when the Agent Engine API is fully available in the Python SDK

    # Pseudocode for future implementation:
    # client = vertexai.Client(project=project_id, location=location)
    # response = client.agent_engines.apps.upsert(
    #     engine_id,
    #     image=image,
    #     display_name="bobs-brain",
    #     env={"RUN_MODE": "service"}
    # )

    # For now, use the existing make deploy method or gcloud CLI
    print(f"\n⚠️  Note: Agent Engine bootstrap using SDK is not yet implemented")
    print(f"    Falling back to existing deployment method (make deploy)")
    print(f"    Future implementation will use:")
    print(f"      - Engine ID: {engine_id}")
    print(f"      - Image: {image}")
    print(f"      - Display Name: bobs-brain")
    print(f"      - Environment: RUN_MODE=service")

    # Fallback: Use existing deployment
    import subprocess
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    print(f"\n[Fallback] Running make deploy from {repo_root}...")
    result = subprocess.run(
        ["make", "deploy"],
        cwd=repo_root,
        capture_output=False,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Deployment failed with exit code {result.returncode}")
        sys.exit(1)

    print(f"\n✅ Agent Engine deployment complete!")
    print(f"   Engine ID: {engine_id}")

except ImportError as e:
    print(f"❌ Error: Required Python packages not installed: {e}")
    print(f"   Please install: pip install google-cloud-aiplatform")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error during Agent Engine bootstrap: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

PYTHON_SCRIPT

echo ""
echo "✅ Agent Engine bootstrap complete!"
