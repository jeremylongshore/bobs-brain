# Production Environment - Bob's Brain Gateway
#
# Deploys Cloud Run gateway with observability (dashboards, alerts, budgets).
# CRITICAL: Gateway does NOT run the agent - it calls the remote engine.

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Agent Engine (placeholder - assumes engine already exists)
module "agent_engine" {
  source     = "../../modules/agent_engine"
  project_id = var.project_id
  region     = var.region
  engine_id  = var.engine_id
}

# Deploy Cloud Run gateway
module "gateway" {
  source        = "../../modules/cloud_run_gateway"
  project_id    = var.project_id
  region        = var.region
  image         = var.image
  min_instances = 1  # Prod: Always have 1 instance warm
  max_instances = 100
  cpu           = "2"
  memory        = "1Gi"

  env = merge({
    ENGINE_MODE       = "agent_engine"
    LOCATION          = var.region
    AGENT_ENGINE_ID   = module.agent_engine.agent_engine_id
    AGENT_ENGINE_NAME = module.agent_engine.agent_engine_name
  }, var.env)
}

# Observability: Dashboard, Alerts, Budget
module "observability" {
  source            = "../../modules/observability"
  project_id        = var.project_id
  region            = var.region
  service_name      = "bobs-brain-gateway"
  billing_account   = var.billing_account
  budget_amount_usd = var.budget_amount_usd
}

# Outputs
output "gateway_url" {
  description = "Cloud Run gateway URL"
  value       = module.gateway.gateway_url
}

output "agent_engine_id" {
  description = "Reasoning Engine ID"
  value       = module.agent_engine.agent_engine_id
}

output "agent_engine_name" {
  description = "Reasoning Engine full resource name"
  value       = module.agent_engine.agent_engine_name
}

output "dashboard_url" {
  description = "Cloud Monitoring dashboard URL"
  value       = module.observability.dashboard_url
}

output "dashboard_id" {
  description = "Dashboard ID"
  value       = module.observability.dashboard_id
}

output "latency_alert_id" {
  description = "Latency alert policy ID"
  value       = module.observability.latency_alert_id
}

output "error_rate_alert_id" {
  description = "Error rate alert policy ID"
  value       = module.observability.error_rate_alert_id
}

output "budget_id" {
  description = "Budget ID"
  value       = module.observability.budget_id
}
