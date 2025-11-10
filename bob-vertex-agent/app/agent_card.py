"""
Bob's Agent Card Definition

Defines Bob as the master orchestrator agent with metadata and capabilities.
"""

AGENT_CARD = {
    # Product Identity
    "name": "Battalion Commander Bob",
    "product_name": "Battalion Commander Bob - Lead Intel Commander",
    "version": "2.0.0",
    "tier": "IAM1",  # Battalion Commander tier
    "business_model": "deployable_battalion_commander",

    # Business Description
    "description": "Elite AI Battalion Commander for enterprise command and control. Commands specialized squads (IAM2 agents) and coordinates with peer commanders (other IAM1s) across the battlefield. Grounded in strategic intelligence with real-time situational awareness.",

    # Hierarchy & Permissions
    "hierarchy": {
        "tier": "IAM1",
        "role": "battalion_commander",
        "can_command": ["IAM2"],  # Commands specialized squads (IAM2 agents)
        "can_coordinate_with": ["IAM1"],  # Coordinates with peer commanders (other IAM1s)
        "reports_to": None,  # IAM1 Battalion Commander is sovereign within their domain
    },

    # Core Capabilities (standalone)
    "standalone_capabilities": [
        "conversational_ai",  # Basic chat functionality
        "knowledge_retrieval",  # RAG grounded in client knowledge
        "task_understanding",  # Understand user requests
        "context_management",  # Maintain conversation context
        "client_specific_grounding",  # Uses Vertex AI Search for client domain
    ],

    # Management Capabilities (when managing IAM2s)
    "management_capabilities": [
        "task_delegation",  # Delegate to IAM2 specialists
        "team_coordination",  # Coordinate IAM2 team members
        "decision_making",  # Decide routing and priorities
        "quality_control",  # Review IAM2 outputs
    ],

    # Peer Communication (with other IAM1s)
    "peer_capabilities": [
        "agent_to_agent_communication",  # A2A with peer IAM1s
        "information_sharing",  # Share info with peer managers
        "coordination",  # Coordinate cross-regional tasks
    ],

    # Deployment Model
    "deployment": {
        "method": "agent_engine_a2a",  # Agent-to-Agent framework
        "platform": "vertex_ai_agent_engine",
        "region": "us-central1",
        "isolation": "per_client",  # Each client gets isolated IAM1
        "grounding": "client_specific_vertex_search",  # Client's own knowledge base
    },

    # Revenue Model
    "business_value": {
        "standalone": "Basic conversational AI + RAG grounding",
        "with_iam2": "Full team orchestration with specialists",
        "multi_iam1": "Enterprise-wide multi-regional coordination",
    },

    # Technical Integration
    "integrations": [
        "vertex_ai_search",  # Client knowledge grounding
        "slack",  # Communication platform
        "bigquery",  # Client data access
        "a2a_framework",  # Inter-agent communication
    ],

    # Observability
    "observability": {
        "telemetry_enabled": True,
        "trace_all_calls": True,
        "log_agent_decisions": True,
        "client_isolation": True,  # Each client's data stays isolated
    }
}


def get_agent_card():
    """Return Bob's agent card"""
    return AGENT_CARD


def get_capabilities():
    """Return list of Bob's capabilities"""
    return AGENT_CARD["capabilities"]


def get_sub_agents():
    """Return sub-agent configurations"""
    return AGENT_CARD["sub_agents"]
