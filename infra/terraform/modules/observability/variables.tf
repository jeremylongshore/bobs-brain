variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "service_name" {
  description = "Cloud Run service name for monitoring"
  type        = string
  default     = "bobs-brain-gateway"
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

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}
