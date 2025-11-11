variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "image" {
  description = "Container image for gateway"
  type        = string
}

variable "engine_id" {
  description = "Reasoning Engine ID (short form, e.g., 'bobs-brain-engine')"
  type        = string
}

variable "billing_account" {
  description = "GCP billing account ID (format: XXXXXX-XXXXXX-XXXXXX)"
  type        = string
}

variable "budget_amount_usd" {
  description = "Monthly budget amount in USD"
  type        = number
  default     = 300
}

variable "env" {
  description = "Additional environment variables for gateway (e.g., feature flags)"
  type        = map(string)
  default     = {}
}
