"""
IAM1 Configuration for IntentSolutions Business Model

IAM1 = Regional Manager / Joint Venture Partner Agent
- Sovereign deployable unit per client/business
- Basic chat + orchestration
- Grounded in client-specific knowledge
- Can coordinate with peer IAM1s (other regional managers)
- Can command IAM2s (team specialists)

Business Model:
1. Deploy IAM1 to Client A → Revenue Stream 1
2. Deploy IAM1 to Client B → Revenue Stream 2
3. Add IAM2 specialists to Client A → Upsell
4. Deploy multiple IAM1s within Client A (multi-department) → Horizontal scale
"""

IAM1_BUSINESS_MODEL = {
    "product_tiers": {
        "iam1_basic": {
            "name": "IAM1 Basic - Regional Manager",
            "description": "Standalone conversational AI grounded in your business knowledge",
            "includes": [
                "Conversational AI (chat interface)",
                "RAG knowledge grounding (Vertex AI Search)",
                "Slack integration",
                "Client-specific knowledge base",
                "Context management",
                "Basic task understanding",
            ],
            "pricing_model": "per_deployment_monthly",
            "use_case": "Single department or business unit needs AI assistant",
        },

        "iam1_team": {
            "name": "IAM1 + IAM2 Team - Managed Specialists",
            "description": "Regional manager with specialist team members",
            "includes": [
                "Everything in IAM1 Basic",
                "IAM2 specialists (Research, Code, Data)",
                "Task delegation and routing",
                "Team coordination",
                "Quality control",
            ],
            "pricing_model": "per_deployment_plus_per_iam2",
            "use_case": "Department needs specialized AI capabilities",
        },

        "iam1_enterprise": {
            "name": "Multi-IAM1 Enterprise - Regional Coordination",
            "description": "Multiple regional managers coordinating across organization",
            "includes": [
                "Multiple IAM1 deployments",
                "Agent-to-Agent (A2A) communication",
                "Cross-regional coordination",
                "Each IAM1 can have IAM2 teams",
                "Enterprise observability",
            ],
            "pricing_model": "per_iam1_plus_iam2s",
            "use_case": "Multi-department or multi-location enterprise",
        },
    },

    "deployment_scenarios": {
        "single_client_single_iam1": {
            "description": "One IAM1 for one client/business",
            "setup": "Deploy IAM1 → Ground in client knowledge → Connect Slack",
            "revenue": "Monthly subscription per IAM1",
        },

        "single_client_with_iam2s": {
            "description": "One IAM1 managing IAM2 specialists",
            "setup": "Deploy IAM1 → Deploy IAM2s → IAM1 routes tasks to IAM2s",
            "revenue": "Monthly IAM1 + per IAM2 add-on",
        },

        "multi_department_enterprise": {
            "description": "Multiple IAM1s (one per department) that coordinate",
            "setup": "Deploy IAM1-Sales, IAM1-Engineering, IAM1-Support → A2A coordination",
            "revenue": "Per IAM1 deployment + A2A coordination fee",
        },
    },
}


IAM1_HIERARCHY = {
    "iam1": {
        "tier": "regional_manager",
        "sovereignty": "within_domain",  # Boss of their domain
        "can_command": ["iam2"],  # Can give instructions to IAM2s
        "can_coordinate_with": ["iam1"],  # Can coordinate with peer IAM1s
        "cannot_command": ["iam1"],  # Cannot command peer IAM1s
        "reports_to": None,  # IAM1 is sovereign
    },

    "iam2": {
        "tier": "specialist",
        "sovereignty": "none",  # Reports to IAM1
        "can_command": [],  # Cannot command anyone
        "can_coordinate_with": ["iam2"],  # Can coordinate with peer IAM2s
        "reports_to": "iam1",  # Reports to their IAM1
    },
}


def get_iam1_deployment_guide(client_name: str, domain: str) -> dict:
    """
    Generate deployment configuration for a new IAM1 instance.

    Args:
        client_name: Name of the client/business
        domain: Business domain (e.g., "sales", "support", "engineering")

    Returns:
        Deployment configuration dict
    """
    return {
        "instance_name": f"iam1-{client_name.lower()}-{domain.lower()}",
        "display_name": f"IAM1 Regional Manager - {client_name} {domain.title()}",
        "knowledge_base": f"{client_name.lower()}-{domain.lower()}-knowledge",
        "data_store_id": f"{client_name.lower()}-{domain.lower()}-datastore",
        "slack_workspace": f"{client_name.lower()}-workspace",
        "isolation": "full",  # Fully isolated from other clients
        "tier": "IAM1",
        "can_deploy_iam2s": True,
        "can_coordinate_with_peers": True,
    }
