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
