"""A2A Protocol integration for IAM1 peer coordination.

This module enables IAM1 agents to coordinate with peer IAM1s across different domains
using the Agent2Agent (A2A) Protocol standard.

Copyright 2025 IntentSolutions
"""

import os
from typing import Any

# Registry of known peer IAM1 agents
# These are configured via environment variables per deployment
PEER_IAM1_REGISTRY: dict[str, str] = {
    "engineering": os.getenv("IAM1_ENGINEERING_URL", ""),
    "sales": os.getenv("IAM1_SALES_URL", ""),
    "operations": os.getenv("IAM1_OPERATIONS_URL", ""),
    "marketing": os.getenv("IAM1_MARKETING_URL", ""),
    "finance": os.getenv("IAM1_FINANCE_URL", ""),
    "hr": os.getenv("IAM1_HR_URL", ""),
}


def coordinate_with_peer_iam1(domain: str, request: str) -> str:
    """Coordinate with a peer IAM1 agent in another domain via A2A Protocol.

    Use this when you need information or assistance from another IAM1 regional manager.
    This is for PEER COORDINATION (not subordinate delegation).

    IAM1 peers are sovereign in their domains and you cannot command them.
    You can only request information or coordinate tasks.

    Args:
        domain: The domain of the peer IAM1. Options:
            - engineering: Technical implementation, product roadmap, architecture
            - sales: Sales metrics, customer data, revenue forecasts
            - operations: Infrastructure, support tickets, operational metrics
            - marketing: Campaign performance, brand metrics, market research
            - finance: Budget, financial forecasts, cost analysis
            - hr: Headcount, hiring, organizational structure
        request: The request/query to send to the peer IAM1. Be specific and clear.

    Examples:
        - domain="engineering", request="What is the Q2 product roadmap and required resources?"
        - domain="sales", request="Retrieve Q4 sales metrics and top customer accounts"
        - domain="operations", request="What are the top 10 customer support issues this month?"
        - domain="marketing", request="Summarize campaign performance for Q3"
        - domain="finance", request="What is the budget allocation for engineering in Q4?"
        - domain="hr", request="What is the current headcount and hiring pipeline?"

    Returns:
        Response from the peer IAM1 agent, or error message if coordination fails
    """
    try:
        # Validate domain
        if domain not in PEER_IAM1_REGISTRY:
            available = ", ".join(PEER_IAM1_REGISTRY.keys())
            return f"""❌ Unknown peer IAM1 domain: '{domain}'

Available peer domains: {available}

Please specify a valid domain from the available options."""

        peer_url = PEER_IAM1_REGISTRY[domain]

        # Check if peer is configured
        if not peer_url:
            return f"""❌ Peer IAM1 '{domain}' is not configured for this deployment.

This means the environment variable IAM1_{domain.upper()}_URL is not set.

To enable coordination with {domain} IAM1:
1. Deploy {domain} IAM1 instance
2. Configure IAM1_{domain.upper()}_URL environment variable with the deployment URL
3. Restart this IAM1 instance"""

        # Import A2A SDK (lazy import to avoid startup errors if not configured)
        try:
            from a2a_sdk import A2AClient, Message  # type: ignore
        except ImportError:
            return """❌ A2A SDK not installed.

The A2A Protocol integration requires the a2a-sdk package.
This should be installed automatically via requirements.

Please contact your system administrator."""

        # Initialize A2A client
        api_key = os.getenv("IAM1_A2A_API_KEY", "")
        auth_header = {"X-API-Key": api_key} if api_key else None

        print(f"[IAM1] 🤝 Coordinating with peer {domain.upper()} IAM1...")
        print(f"[IAM1] Request: {request[:100]}...")

        client = A2AClient(base_url=peer_url, auth_header=auth_header)

        # Create message for peer IAM1
        message = Message(
            role="user", content=[{"type": "text", "text": request}]
        )

        # Send request via A2A Protocol (JSON-RPC 2.0)
        task = client.tasks.create(messages=[message])

        # Wait for completion (with timeout)
        task = client.tasks.wait_until_complete(task.id, timeout=30)

        # Process response based on task status
        if task.status == "completed":
            # Extract response text from artifacts
            response_text = ""
            for artifact in task.artifacts:
                for part in artifact.parts:
                    if part.type == "text":
                        response_text += part.text + "\n"

            if not response_text.strip():
                return f"""❌ Peer IAM1 '{domain}' returned empty response.

The task completed successfully but no content was returned.
This may indicate an issue with the peer IAM1 configuration."""

            print(
                f"[IAM1] ✅ Received response from {domain.upper()} IAM1 ({len(response_text)} chars)"
            )

            return f"""┌─────────────────────────────────────────┐
│ PEER IAM1 {domain.upper()} RESPONSE
└─────────────────────────────────────────┘

{response_text.strip()}

────────────────────────────────────────────
End of peer IAM1 coordination with {domain}
"""

        elif task.status == "failed":
            error_msg = getattr(task, "error", "Unknown error")
            return f"""❌ Peer IAM1 '{domain}' task failed

Error: {error_msg}

The {domain} IAM1 was unable to complete your request.
You may need to rephrase the request or try again later."""

        else:
            return f"""⏱️ Peer IAM1 '{domain}' task timeout

Task status: {task.status}
Task ID: {task.id}

The {domain} IAM1 did not respond within the 30-second timeout.
This may indicate:
1. The task is complex and requires more time
2. The peer IAM1 is experiencing high load
3. There is a network connectivity issue

Please try again or break down the request into smaller parts."""

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        print(f"[IAM1] ❌ A2A coordination error: {error_type}: {error_msg}")

        return f"""❌ Error coordinating with peer IAM1 '{domain}'

Error type: {error_type}
Details: {error_msg}

This may be caused by:
1. Network connectivity issues
2. Authentication problems (check IAM1_A2A_API_KEY)
3. Peer IAM1 service unavailable
4. Invalid A2A Protocol response

Please check the configuration and try again."""


# Metadata for ADK tool registration
A2A_COORDINATE_TOOL_METADATA = {
    "name": "coordinate_with_peer_iam1",
    "description": """Coordinate with a peer IAM1 regional manager in another domain.

Use this for IAM1-to-IAM1 peer coordination (NOT for commanding subordinates).
Available domains: engineering, sales, operations, marketing, finance, hr.

This tool enables cross-domain collaboration between IAM1 agents.""",
    "function": coordinate_with_peer_iam1,
}
