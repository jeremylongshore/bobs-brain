# Vertex AI Agent Engine Configuration
# R2: Agent Engine runtime (not self-hosted)
# Phase 19: Inline Source Deployment (6767-INLINE standard)
#
# IMPORTANT: This file defines placeholder resources for Agent Engine agents.
# The actual deployment uses INLINE SOURCE DEPLOYMENT via ADK, not Docker containers.
#
# Deployment Pattern (per 6767-INLINE):
# 1. Source code pushed to git
# 2. GitHub Actions workflow runs ARV checks
# 3. Python deployment script (scripts/deploy_inline_source.py) calls Vertex AI API
# 4. Agent Engine packages source code from repository
# 5. Runtime executes agents/bob/agent.py::app (lazy-loading App pattern)
#
# Terraform's Role:
# - Manages service accounts and IAM permissions (see iam.tf)
# - Documents expected Agent Engine resources
# - Does NOT configure inline source deployment details (handled by deployment script)
#
# See: 000-docs/6767-INLINE-DR-STND-inline-source-deployment-for-vertex-agent-engine.md

# Compute default image names for Docker-based deployment (future consideration)
locals {
  bob_image = coalesce(
    var.bob_docker_image,
    "gcr.io/${var.project_id}/agent:${var.app_version}"
  )

  foreman_image = coalesce(
    var.foreman_docker_image,
    "gcr.io/${var.project_id}/foreman:${var.app_version}"
  )
}

# ==============================================================================
# Bob Agent (Main Orchestrator)
# ==============================================================================
#
# TODO (Phase 19):
# The google_vertex_ai_reasoning_engine Terraform resource does not yet support
# full inline source deployment configuration in the current provider version.
#
# Current limitations:
# - Cannot specify source_packages, entrypoint_module, entrypoint_object via Terraform
# - Image-based deployment not yet stable/recommended for ADK agents
# - Environment variables, scaling config not directly configurable
#
# Deployment Approach (Manual/CI):
# 1. Ensure service account google_service_account.agent_engine exists (defined in iam.tf)
# 2. Run deployment script: python scripts/deploy_inline_source.py --agent bob --env dev
# 3. Script calls Vertex AI Agent Engine API with inline source config
# 4. Terraform can import existing agent: terraform import google_vertex_ai_reasoning_engine.bob RESOURCE_ID
#
# See:
# - scripts/deploy_inline_source.py (deployment automation)
# - .github/workflows/deploy-agent-engine-dev.yml (CI/CD integration)
# - 000-docs/6767-INLINE-DR-STND-inline-source-deployment-for-vertex-agent-engine.md
#
# ==============================================================================

resource "google_vertex_ai_reasoning_engine" "bob" {
  display_name = "${var.app_name}-${var.environment}"
  project      = var.project_id

  # TODO: Uncomment and configure when provider supports inline source deployment
  # Currently, deploy via scripts/deploy_inline_source.py instead
  #
  # spec {
  #   source_packages     = ["agents", "deployment"]
  #   entrypoint_module   = "agents.bob.agent"
  #   entrypoint_object   = "app"
  #   class_methods       = ["query", "orchestrate", "analyze_repo"]
  #   requirements_file   = "requirements.txt"
  # }

  depends_on = [
    google_service_account.agent_engine,
    google_project_iam_member.agent_engine_aiplatform,
    google_project_iam_member.agent_engine_vertex,
  ]
}

# Output Agent Engine ID for gateways
output "agent_engine_id" {
  description = "Bob Agent Engine instance ID (will be populated after deployment)"
  value       = try(google_vertex_ai_reasoning_engine.bob.id, "not-yet-deployed")
}

# Output Agent Engine REST endpoint
output "agent_engine_endpoint" {
  description = "Bob Agent Engine REST API endpoint (will be populated after deployment)"
  value       = try("https://${var.region}-aiplatform.googleapis.com/v1/projects/${var.project_id}/locations/${var.region}/reasoningEngines/${google_vertex_ai_reasoning_engine.bob.id}:query", "not-yet-deployed")
}

# ==============================================================================
# Foreman Agent (iam-senior-adk-devops-lead)
# ==============================================================================
#
# TODO (Phase 19):
# Same limitations as bob agent - deploy via scripts/deploy_inline_source.py
#
# Deployment Approach (Manual/CI):
# 1. Run deployment script: python scripts/deploy_inline_source.py --agent foreman --env dev
# 2. Script deploys from agents/iam_senior_adk_devops_lead/agent.py::app
# 3. Terraform can import: terraform import google_vertex_ai_reasoning_engine.foreman RESOURCE_ID
#
# ==============================================================================

resource "google_vertex_ai_reasoning_engine" "foreman" {
  display_name = "${var.app_name}-foreman-${var.environment}"
  project      = var.project_id

  # TODO: Uncomment and configure when provider supports inline source deployment
  # Currently, deploy via scripts/deploy_inline_source.py instead
  #
  # spec {
  #   source_packages     = ["agents", "deployment"]
  #   entrypoint_module   = "agents.iam_senior_adk_devops_lead.agent"
  #   entrypoint_object   = "app"
  #   class_methods       = ["delegate_task", "coordinate_agents", "query"]
  #   requirements_file   = "requirements.txt"
  # }

  depends_on = [
    google_service_account.agent_engine,
    google_project_iam_member.agent_engine_aiplatform,
    google_project_iam_member.agent_engine_vertex,
  ]
}

# Output Foreman Agent Engine ID
output "foreman_agent_engine_id" {
  description = "Foreman Agent Engine instance ID (will be populated after deployment)"
  value       = try(google_vertex_ai_reasoning_engine.foreman.id, "not-yet-deployed")
}

# Output Foreman Agent Engine REST endpoint
output "foreman_agent_engine_endpoint" {
  description = "Foreman Agent Engine REST API endpoint (will be populated after deployment)"
  value       = try("https://${var.region}-aiplatform.googleapis.com/v1/projects/${var.project_id}/locations/${var.region}/reasoningEngines/${google_vertex_ai_reasoning_engine.foreman.id}:query", "not-yet-deployed")
}
