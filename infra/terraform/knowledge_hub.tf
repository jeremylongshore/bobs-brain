# knowledge_hub.tf - Org-wide Knowledge Hub Infrastructure (STUB)
#
# This defines the canonical knowledge hub pattern for Intent Solutions.
# All agent projects share this central knowledge repository via cross-project IAM.
#
# IMPORTANT: This is a TEMPLATE/STUB - wire actual values before applying
#
# Actual deployed project: datahub-intent (created manually)
# This Terraform represents the desired end state for IaC management

# ============================================================================
# VARIABLES - Override in envs/*.tfvars
# ============================================================================

variable "knowledge_hub_project_id" {
  description = "The GCP project ID for the org-wide knowledge hub"
  type        = string
  default     = "datahub-intent"  # Our actual project name
}

variable "knowledge_hub_location" {
  description = "The GCP region/multi-region for knowledge buckets"
  type        = string
  default     = "us-central1"
}

variable "knowledge_bucket_prefix" {
  description = "Prefix for knowledge bucket names"
  type        = string
  default     = "datahub-intent"  # Using project name as prefix
}

variable "enable_versioning" {
  description = "Enable versioning on knowledge buckets"
  type        = bool
  default     = true
}

variable "lifecycle_age_days" {
  description = "Days before transitioning to nearline storage"
  type        = number
  default     = 90
}

# Service Account Variables (populated from each project)
variable "bobs_brain_runtime_sa" {
  description = "Bob's Brain Agent Engine runtime service account"
  type        = string
  default     = ""  # TODO: Wire from bobs-brain project
}

variable "bobs_brain_search_sa" {
  description = "Bob's Brain Vertex AI Search service account"
  type        = string
  default     = ""  # TODO: Wire from bobs-brain project
}

variable "consumer_service_accounts" {
  description = "Additional service accounts that need read access"
  type = list(object({
    email  = string
    prefix = string  # Which prefix they can access
  }))
  default = []
}

# ============================================================================
# KNOWLEDGE HUB BUCKETS
# ============================================================================

# Development Knowledge Bucket
resource "google_storage_bucket" "knowledge_hub_dev" {
  # TODO: Uncomment when ready to manage via Terraform
  # count = 0  # Disabled - bucket exists, managed manually for now

  name     = "${var.knowledge_bucket_prefix}-dev"
  project  = var.knowledge_hub_project_id
  location = var.knowledge_hub_location

  # Uniform bucket-level access (no ACLs)
  uniform_bucket_level_access {
    enabled = true
  }

  # Soft delete for recovery
  soft_delete_policy {
    retention_duration_seconds = 2592000  # 30 days
  }

  versioning {
    enabled = var.enable_versioning
  }

  lifecycle_rule {
    condition {
      age = var.lifecycle_age_days
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365  # 1 year
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }

  labels = {
    environment = "dev"
    purpose     = "knowledge-hub"
    managed-by  = "terraform"
  }
}

# Production Knowledge Bucket
resource "google_storage_bucket" "knowledge_hub_prod" {
  # TODO: Uncomment when ready to manage via Terraform
  # count = 0  # Disabled - bucket exists, managed manually for now

  name     = "${var.knowledge_bucket_prefix}"  # Main bucket uses project name
  project  = var.knowledge_hub_project_id
  location = var.knowledge_hub_location

  uniform_bucket_level_access {
    enabled = true
  }

  soft_delete_policy {
    retention_duration_seconds = 2592000  # 30 days
  }

  versioning {
    enabled = true  # Always enabled in prod
  }

  lifecycle_rule {
    condition {
      age = var.lifecycle_age_days
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }

  # Compliance and retention
  retention_policy {
    retention_period = 2555  # 7 years in days
    is_locked        = false # Set to true after testing
  }

  labels = {
    environment  = "prod"
    purpose      = "knowledge-hub"
    managed-by   = "terraform"
    compliance   = "7-year-retention"
  }
}

# ============================================================================
# CROSS-PROJECT IAM BINDINGS
# ============================================================================

# Bob's Brain Runtime Access (Production)
resource "google_storage_bucket_iam_member" "bobs_brain_runtime_prod" {
  # TODO: Uncomment and wire actual SA when ready
  # count = var.bobs_brain_runtime_sa != "" ? 1 : 0

  bucket = var.knowledge_bucket_prefix  # Prod bucket
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.bobs_brain_runtime_sa}"

  # Optional: Restrict to bobs-brain prefix only
  # condition {
  #   title       = "bobs-brain-prefix-only"
  #   description = "Restrict access to bobs-brain/ prefix"
  #   expression  = "resource.name.startsWith('projects/_/buckets/${var.knowledge_bucket_prefix}/objects/bobs-brain/')"
  # }
}

# Bob's Brain Search Service Access (Production)
resource "google_storage_bucket_iam_member" "bobs_brain_search_prod" {
  # TODO: Uncomment and wire actual SA when ready
  # count = var.bobs_brain_search_sa != "" ? 1 : 0

  bucket = var.knowledge_bucket_prefix
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.bobs_brain_search_sa}"
}

# Dynamic IAM for additional consumers
resource "google_storage_bucket_iam_member" "consumer_access" {
  # TODO: Uncomment when ready to add more consumers
  # for_each = { for sa in var.consumer_service_accounts : sa.email => sa }

  # bucket = var.knowledge_bucket_prefix
  # role   = "roles/storage.objectViewer"
  # member = "serviceAccount:${each.value.email}"

  # TODO: Add prefix-based conditions when needed
}

# ============================================================================
# VERTEX AI SEARCH DATASTORE (Reference Only)
# ============================================================================

# NOTE: Vertex AI Search datastores are created via gcloud/console
# This is documentation of expected configuration

locals {
  vertex_search_config = {
    datastore_id = "universal-knowledge-store"
    project_id   = "bobs-brain"  # Datastore lives in consumer project
    location     = "us"
    data_source  = "gs://${var.knowledge_bucket_prefix}/bobs-brain/**"
    type         = "unstructured"
  }
}

# Output the configuration for documentation
output "vertex_search_setup_command" {
  description = "Command to create Vertex AI Search datastore"
  value = <<-EOT
    # Run this in bobs-brain project to create the datastore:

    gcloud ai search datastores create ${local.vertex_search_config.datastore_id} \
      --location=${local.vertex_search_config.location} \
      --project=${local.vertex_search_config.project_id} \
      --type=${local.vertex_search_config.type}

    # Then import data:
    gcloud ai search documents import \
      --datastore=${local.vertex_search_config.datastore_id} \
      --location=${local.vertex_search_config.location} \
      --project=${local.vertex_search_config.project_id} \
      --gcs-uri=${local.vertex_search_config.data_source}
  EOT
}

# ============================================================================
# OUTPUTS
# ============================================================================

output "knowledge_hub_project" {
  description = "The knowledge hub project ID"
  value       = var.knowledge_hub_project_id
}

output "knowledge_bucket_dev" {
  description = "Development knowledge bucket name"
  value       = "${var.knowledge_bucket_prefix}-dev"
}

output "knowledge_bucket_prod" {
  description = "Production knowledge bucket name"
  value       = var.knowledge_bucket_prefix
}

output "knowledge_bucket_structure" {
  description = "Expected bucket prefix structure"
  value = {
    bobs_brain     = "gs://${var.knowledge_bucket_prefix}/bobs-brain/"
    iam_agents     = "gs://${var.knowledge_bucket_prefix}/iam-agents/"
    diagnosticpro  = "gs://${var.knowledge_bucket_prefix}/diagnosticpro/"
    pipelinepilot  = "gs://${var.knowledge_bucket_prefix}/pipelinepilot/"
    shared         = "gs://${var.knowledge_bucket_prefix}/shared/"
  }
}

# ============================================================================
# NOTES FOR IMPLEMENTATION
# ============================================================================

# TODO LIST:
# 1. Get actual service account emails from each project:
#    - bobs-brain: Agent Engine runtime SA
#    - bobs-brain: Vertex AI Search service SA
#    - Future: Other project SAs
#
# 2. Decide on IAM conditions:
#    - Implement prefix-based restrictions if needed
#    - Consider time-based access for temporary permissions
#
# 3. Import existing resources:
#    - The datahub-intent project and bucket already exist
#    - Use: terraform import google_storage_bucket.knowledge_hub_prod datahub-intent
#
# 4. Add monitoring:
#    - Storage metrics and alerts
#    - Access pattern monitoring
#    - Cost allocation by prefix
#
# 5. Future enhancements:
#    - CMEK encryption
#    - Cross-region replication
#    - Backup buckets
#    - DLP scanning