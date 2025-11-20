"""
Remote MCP Tools Module (STUB)

This module will contain MCP (Model Context Protocol) tools that connect
to externally running MCP servers. These servers may be deployed on Cloud Run,
other cloud services, or on-premises.

IMPORTANT: Tools here only configure connections to MCP servers.
They do NOT host the services themselves.

Status: STUB ONLY - No MCP servers deployed yet
"""

from typing import Any, Optional, List
import logging
import os

logger = logging.getLogger(__name__)


# ============================================================================
# MCP TOOLS - Connect to external MCP servers
# ============================================================================

def get_mcp_filesystem_tool() -> Optional[Any]:
    """
    Get MCP filesystem tool (FUTURE).

    This would connect to an MCP server providing filesystem access.
    The server could be deployed on Cloud Run or elsewhere.

    TODO: Deploy MCP filesystem server first, then wire here.
    """
    # TODO: When ready to implement:
    # 1. Deploy MCP server to Cloud Run (see scripts/mcp_servers/)
    # 2. Get the Cloud Run URL
    # 3. Wire it here:
    #
    # from google.adk.toolsets import MCPToolset
    # mcp_url = os.getenv("MCP_FILESYSTEM_URL")
    # if mcp_url:
    #     return MCPToolset(server_url=mcp_url)

    logger.info("MCP filesystem tool not configured (no server deployed)")
    return None


def get_mcp_database_tool() -> Optional[Any]:
    """
    Get MCP database tool (FUTURE).

    This would connect to an MCP server providing database access.
    Could be used for CloudSQL, Firestore, or other databases.

    TODO: Deploy MCP database server first, then wire here.
    """
    # TODO: When ready:
    # 1. Deploy MCP database server with proper credentials
    # 2. Configure connection here
    #
    # from google.adk.toolsets import MCPToolset
    # mcp_url = os.getenv("MCP_DATABASE_URL")
    # if mcp_url:
    #     return MCPToolset(
    #         server_url=mcp_url,
    #         auth_token=os.getenv("MCP_DATABASE_TOKEN")
    #     )

    logger.info("MCP database tool not configured (no server deployed)")
    return None


def get_mcp_github_tool() -> Optional[Any]:
    """
    Get MCP GitHub tool (FUTURE).

    This would connect to an MCP server providing GitHub API access.
    Useful for creating issues, PRs, and repository management.

    TODO: Deploy MCP GitHub server with proper auth.
    """
    # TODO: Implementation pattern:
    # 1. Create Cloud Run service with MCP GitHub server
    # 2. Configure GitHub token in Secret Manager
    # 3. Wire connection here

    logger.info("MCP GitHub tool not configured (no server deployed)")
    return None


def list_available_mcp_servers() -> List[str]:
    """
    List currently available MCP servers.

    Returns:
        List of configured MCP server names
    """
    # TODO: Once we have MCP servers, return their names
    return []  # No MCP servers deployed yet


# ============================================================================
# MCP SERVER DEPLOYMENT NOTES
# ============================================================================
"""
When we need MCP servers, the pattern will be:

1. Create server implementation in scripts/mcp_servers/{name}/
   - Dockerfile for the MCP server
   - server.py with MCP protocol implementation
   - requirements.txt

2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy mcp-{name} \
     --source scripts/mcp_servers/{name} \
     --project datahub-intent \
     --region us-central1
   ```

3. Wire in this file:
   - Add environment variable for the Cloud Run URL
   - Create MCPToolset with that URL
   - Return the toolset

4. Document in 6767-NNN-OD-DEPL-mcp-{name}-server.md:
   - Why we need this MCP server
   - What it provides access to
   - Security considerations
   - Deployment instructions
"""

# ============================================================================
# POLICY: MCP tools connect to external servers
# ============================================================================
# These tools:
# - Are ADK MCPToolset instances
# - Connect to MCP servers running elsewhere (Cloud Run, VMs, etc.)
# - Do NOT implement the server logic here
# - Require the external server to be deployed first
# - Should have clear documentation about the server they connect to