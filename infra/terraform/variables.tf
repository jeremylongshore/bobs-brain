# Terraform Variables
# Environment-specific values in envs/*.tfvars

# Project Configuration
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

# Application Configuration
variable "app_name" {
  description = "Application name"
  type        = string
  default     = "bobs-brain"
}

variable "app_version" {
  description = "Application version"
  type        = string
  default     = "0.6.0"
}

# Agent Engine Configuration
variable "agent_docker_image" {
  description = "Docker image for Agent Engine (GCR path)"
  type        = string
  # Example: gcr.io/bobs-brain/agent:0.6.0
}

variable "agent_machine_type" {
  description = "Machine type for Agent Engine"
  type        = string
  default     = "n1-standard-4"
}

variable "agent_max_replicas" {
  description = "Maximum number of Agent Engine replicas"
  type        = number
  default     = 3
}

# Gateway Configuration
variable "a2a_gateway_image" {
  description = "Docker image for A2A Gateway (GCR path)"
  type        = string
  # Example: gcr.io/bobs-brain/a2a-gateway:0.6.0
}

variable "slack_webhook_image" {
  description = "Docker image for Slack Webhook (GCR path)"
  type        = string
  # Example: gcr.io/bobs-brain/slack-webhook:0.6.0
}

variable "gateway_max_instances" {
  description = "Maximum instances for Cloud Run gateways"
  type        = number
  default     = 10
}

# Slack Configuration
variable "slack_bot_token" {
  description = "Slack bot OAuth token (use Secret Manager in production)"
  type        = string
  sensitive   = true
}

variable "slack_signing_secret" {
  description = "Slack app signing secret (use Secret Manager in production)"
  type        = string
  sensitive   = true
}

# SPIFFE ID (R7)
variable "agent_spiffe_id" {
  description = "SPIFFE ID for agent identity"
  type        = string
  # Format: spiffe://intent.solutions/agent/bobs-brain/{env}/{region}/{version}
}

# Public URLs (set after deployment or use custom domains)
variable "a2a_gateway_url" {
  description = "Public URL for A2A Gateway (optional, defaults to Cloud Run URL)"
  type        = string
  default     = ""
}

variable "slack_webhook_url" {
  description = "Public URL for Slack Webhook (optional, defaults to Cloud Run URL)"
  type        = string
  default     = ""
}

# AI Model Configuration
variable "model_name" {
  description = "Gemini model to use"
  type        = string
  default     = "gemini-2.0-flash-exp"
}

# Vertex AI Search Configuration (Phase 3)
variable "vertex_search_datastore_id" {
  description = "Vertex AI Search datastore ID for ADK documentation"
  type        = string
  default     = "adk-documentation"
}

# Networking
variable "allow_public_access" {
  description = "Allow unauthenticated access to gateways"
  type        = bool
  default     = true
}

# Labels
variable "labels" {
  description = "Labels to apply to all resources"
  type        = map(string)
  default     = {}
}
