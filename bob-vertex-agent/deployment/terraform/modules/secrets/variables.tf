# Variables for Secret Manager module

variable "project_id" {
  description = "GCP project ID where secrets will be created"
  type        = string
}

variable "secrets" {
  description = "Map of secret names to their initial values (optional). Use empty string to create secret without version."
  type        = map(string)
  default     = {}
}

variable "labels" {
  description = "Additional labels to apply to secrets"
  type        = map(string)
  default     = {}
}
