# Main Terraform Configuration
# Bob's Brain - Hard Mode Architecture
#
# IMPORTANT: This Terraform configuration assumes an EXISTING GCP project.
# It does NOT create projects. The project ID must be provided via var.project_id.
# For bobs-brain, the canonical project is:
#   Project ID: bobs-brain
#   Project Number: 205354194989
#
# This Terraform configuration deploys:
# 1. Vertex AI Agent Engine (R2) - ADK agent runtime
# 2. A2A Gateway (R3) - Agent-to-Agent protocol proxy
# 3. Slack Webhook (R3) - Slack integration proxy
# 4. IAM Configuration - Service accounts and permissions
#
# Hard Mode Rules Enforced:
# - R1: ADK only (agent code in my_agent/)
# - R2: Agent Engine runtime (not self-hosted)
# - R3: Cloud Run as gateway only (proxies to Agent Engine via REST)
# - R4: CI-only deployments (Workload Identity Federation)
# - R5: Dual memory (Session + Memory Bank in agent code)
# - R6: Single docs folder (000-docs/)
# - R7: SPIFFE ID propagation (in AgentCard and environment)
# - R8: Drift detection (check_nodrift.sh + CI scans)

# Enable required Google Cloud APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "aiplatform.googleapis.com",       # Vertex AI Agent Engine
    "run.googleapis.com",              # Cloud Run
    "compute.googleapis.com",          # Compute Engine
    "storage-api.googleapis.com",      # Cloud Storage
    "storage.googleapis.com",          # Cloud Storage (JSON API)
    "discoveryengine.googleapis.com",  # Vertex AI Search (Phase 3)
    "iam.googleapis.com",              # IAM
    "cloudresourcemanager.googleapis.com", # Resource Manager
    "serviceusage.googleapis.com",     # Service Usage
  ])

  project = var.project_id
  service = each.key

  disable_on_destroy = false
}

# Local values for common resource naming
locals {
  resource_prefix = "${var.app_name}-${var.environment}"

  common_labels = merge(
    var.labels,
    {
      app         = var.app_name
      environment = var.environment
      version     = replace(var.app_version, ".", "-")
      managed_by  = "terraform"
    }
  )
}

# Import service account, IAM, Agent Engine, and Cloud Run configurations
# These are defined in separate files for better organization:
# - iam.tf: Service accounts and IAM bindings
# - agent_engine.tf: Vertex AI Agent Engine resource
# - cloud_run.tf: A2A Gateway and Slack Webhook services
# - outputs.tf: Output values for deployed resources
