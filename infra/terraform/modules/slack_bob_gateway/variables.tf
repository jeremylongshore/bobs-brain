# Slack Bob Gateway Module - Input Variables
# R3: Cloud Run as gateway only (proxy to Agent Engine via REST)

variable "enable" {
  description = "Feature flag to enable/disable Slack gateway"
  type        = bool
  default     = false
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for Cloud Run deployment"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "app_name" {
  description = "Application name (for naming resources)"
  type        = string
  default     = "bobs-brain"
}

variable "image" {
  description = "Docker image for Slack gateway (set by CI)"
  type        = string
  # Example: gcr.io/bobs-brain/slack-webhook:0.11.0
}

variable "agent_engine_name" {
  description = "Full Agent Engine resource name"
  type        = string
  # Example: projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448
}

variable "agent_engine_id" {
  description = "Agent Engine ID (numeric)"
  type        = string
}

variable "slack_signing_secret_id" {
  description = "Secret Manager secret ID for Slack signing secret"
  type        = string
  default     = "slack-signing-secret"
}

variable "slack_bot_token_secret_id" {
  description = "Secret Manager secret ID for Slack bot token"
  type        = string
  default     = "slack-bot-token"
}

variable "service_account_email" {
  description = "Service account email for Cloud Run service"
  type        = string
}

variable "allow_unauthenticated" {
  description = "Allow unauthenticated access (required for Slack webhooks)"
  type        = bool
  default     = true
}

variable "max_instances" {
  description = "Maximum Cloud Run instances"
  type        = number
  default     = 10
}

variable "min_instances" {
  description = "Minimum Cloud Run instances (0 = scale to zero)"
  type        = number
  default     = 0
}

variable "cpu_limit" {
  description = "CPU limit per instance"
  type        = string
  default     = "1000m"
}

variable "memory_limit" {
  description = "Memory limit per instance"
  type        = string
  default     = "512Mi"
}

variable "timeout_seconds" {
  description = "Request timeout in seconds"
  type        = number
  default     = 300
}

variable "labels" {
  description = "Labels to apply to resources"
  type        = map(string)
  default     = {}
}
