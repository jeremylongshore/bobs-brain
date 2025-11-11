# Agent Engine Module
#
# This module creates a placeholder for the Reasoning Engine.
# In production, the engine would be created via gcloud or Console.

terraform {
  required_version = "~> 1.9"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "engine_id" {
  description = "Reasoning Engine ID"
  type        = string
}

# Construct full resource name
locals {
  engine_name = "projects/${var.project_id}/locations/${var.region}/reasoningEngines/${var.engine_id}"
}

# Outputs
output "agent_engine_id" {
  description = "Reasoning Engine ID (short form)"
  value       = var.engine_id
}

output "agent_engine_name" {
  description = "Reasoning Engine full resource name"
  value       = local.engine_name
}
