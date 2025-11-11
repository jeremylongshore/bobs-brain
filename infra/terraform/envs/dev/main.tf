# Development Environment - Bob's Brain Gateway
#
# Deploys Cloud Run gateway that proxies to Vertex AI Reasoning Engine.
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
  source       = "../../modules/cloud_run_gateway"
  project_id   = var.project_id
  region       = var.region
  image        = var.image
  min_instances = 0
  max_instances = 10
  cpu          = "1"
  memory       = "512Mi"

  env = {
    ENGINE_MODE       = "agent_engine"
    LOCATION          = var.region
    AGENT_ENGINE_ID   = module.agent_engine.agent_engine_id
    AGENT_ENGINE_NAME = module.agent_engine.agent_engine_name
  }
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
