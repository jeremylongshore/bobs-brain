# Staging Bucket for ADK Deployments
# Required by: adk deploy agent_engine --staging_bucket
#
# ADK CLI uses this bucket to:
# 1. Upload packaged agent code
# 2. Store Docker build artifacts
# 3. Stage deployment files before Agent Engine deployment

resource "google_storage_bucket" "adk_staging" {
  name          = "${var.project_id}-adk-staging"
  location      = var.region
  project       = var.project_id
  force_destroy = false  # Protect against accidental deletion

  # Security: Block public access
  uniform_bucket_level_access = true

  # Lifecycle: Clean up old deployment artifacts after 30 days
  lifecycle_rule {
    condition {
      age = 30  # Days
    }
    action {
      type = "Delete"
    }
  }

  # Versioning: Keep deployment history
  versioning {
    enabled = true
  }

  # Labels for resource management
  labels = merge(
    var.labels,
    {
      component = "adk-staging"
      purpose   = "deployment-artifacts"
    }
  )
}

# Grant ADK deployment permissions to Agent Engine service account
resource "google_storage_bucket_iam_member" "adk_staging_admin" {
  bucket = google_storage_bucket.adk_staging.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.agent_engine.email}"
}

# ADK Documentation Bucket for Vertex AI Search (Phase 3)
# Used by: Vertex AI Search to index ADK documentation
#
# This bucket stores ADK documentation markdown files that are
# indexed by Vertex AI Search for semantic search capabilities.
resource "google_storage_bucket" "adk_docs" {
  name          = "${var.project_id}-adk-docs"
  location      = var.region
  project       = var.project_id
  force_destroy = false  # Protect documentation

  # Security: Block public access
  uniform_bucket_level_access = true

  # Lifecycle: Documents are permanent, no auto-deletion
  # Manual cleanup only if needed

  # Versioning: Track document changes
  versioning {
    enabled = true
  }

  # Labels for resource management
  labels = merge(
    var.labels,
    {
      component = "adk-docs"
      purpose   = "vertex-search-documentation"
      phase     = "phase-3"
    }
  )
}

# Grant read access to Vertex AI Search service
# Note: Vertex AI Search uses the default Vertex AI service agent
# Format: service-{PROJECT_NUMBER}@gcp-sa-discoveryengine.iam.gserviceaccount.com
resource "google_storage_bucket_iam_member" "adk_docs_vertex_search" {
  bucket = google_storage_bucket.adk_docs.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-discoveryengine.iam.gserviceaccount.com"
}

# Grant admin access to Agent Engine service account for document management
resource "google_storage_bucket_iam_member" "adk_docs_admin" {
  bucket = google_storage_bucket.adk_docs.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.agent_engine.email}"
}

# Note: data "google_project" "project" is defined in cloud_run.tf

# Output for deployment workflows
output "staging_bucket_url" {
  description = "GCS staging bucket URL for ADK CLI deployments"
  value       = "gs://${google_storage_bucket.adk_staging.name}"
}

output "staging_bucket_name" {
  description = "GCS staging bucket name"
  value       = google_storage_bucket.adk_staging.name
}

output "adk_docs_bucket_url" {
  description = "GCS bucket URL for ADK documentation (Vertex AI Search)"
  value       = "gs://${google_storage_bucket.adk_docs.name}"
}

output "adk_docs_bucket_name" {
  description = "GCS bucket name for ADK documentation"
  value       = google_storage_bucket.adk_docs.name
}

# ==============================================================================
# ORG-WIDE KNOWLEDGE HUB (LIVE1-GCS)
# ==============================================================================
# Central storage bucket for org-wide agent/SWE audit data, portfolio results,
# and knowledge artifacts. Shared across all repos/products in the organization.
#
# Naming: intent-org-knowledge-hub-{env}
# Examples:
#   - intent-org-knowledge-hub-dev
#   - intent-org-knowledge-hub-staging
#   - intent-org-knowledge-hub-prod
#
# Directory Layout:
#   portfolio/runs/{run_id}/summary.json          - Portfolio audit summaries
#   portfolio/runs/{run_id}/per-repo/{repo_id}.json - Per-repo results
#   swe/agents/{agent_name}/runs/{run_id}.json    - Single-repo SWE runs (future)
#   docs/                                          - Org-wide documentation (future)
#   vertex-search/                                 - RAG snapshots (LIVE2+)
#
# Feature flags:
#   - ORG_STORAGE_WRITE_ENABLED (default: false)
#   - Writes are opt-in per environment
#
# BigQuery integration:
#   - Deferred to future LIVE-BQ phase
#   - This phase focuses only on GCS JSON writes
# ==============================================================================

resource "google_storage_bucket" "org_knowledge_hub" {
  # Only create if org_storage_enabled is true (default: false)
  count = var.org_storage_enabled ? 1 : 0

  name          = var.org_storage_bucket_name
  location      = var.org_storage_location
  project       = var.project_id
  force_destroy = false  # Protect org-wide knowledge

  # Security: Block public access
  uniform_bucket_level_access = true

  # Lifecycle: Retain portfolio runs for 90 days, keep summaries indefinitely
  lifecycle_rule {
    # Delete per-repo detailed results after 90 days
    condition {
      age                        = 90
      matches_prefix             = ["portfolio/runs/*/per-repo/"]
    }
    action {
      type = "Delete"
    }
  }

  # Versioning: Track changes to audit data
  versioning {
    enabled = true
  }

  # Labels for resource management
  labels = merge(
    var.labels,
    {
      component = "org-knowledge-hub"
      purpose   = "org-wide-audit-data"
      phase     = "live1-gcs"
    }
  )
}

# Grant read/write access to Bob's Brain runtime service account
resource "google_storage_bucket_iam_member" "org_knowledge_hub_bobs_brain" {
  count  = var.org_storage_enabled ? 1 : 0
  bucket = google_storage_bucket.org_knowledge_hub[0].name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.agent_engine.email}"
}

# Grant read/write access to additional service accounts (future repos)
resource "google_storage_bucket_iam_member" "org_knowledge_hub_writers" {
  for_each = var.org_storage_enabled ? toset(var.org_storage_writer_service_accounts) : toset([])
  bucket   = google_storage_bucket.org_knowledge_hub[0].name
  role     = "roles/storage.objectAdmin"
  member   = "serviceAccount:${each.value}"
}

# Output for deployment workflows and app configuration
output "org_storage_bucket_url" {
  description = "GCS org storage bucket URL (if enabled)"
  value       = var.org_storage_enabled ? "gs://${google_storage_bucket.org_knowledge_hub[0].name}" : "NOT_ENABLED"
}

output "org_storage_bucket_name" {
  description = "GCS org storage bucket name (if enabled)"
  value       = var.org_storage_enabled ? google_storage_bucket.org_knowledge_hub[0].name : "NOT_ENABLED"
}

# ==============================================================================
# IMPORTANT NOTES FOR TERRAFORM APPLY:
# ==============================================================================
# 1. Do NOT run `terraform apply` from local; deployment is CI-controlled
# 2. BigQuery is NOT enabled in LIVE1-GCS; future LIVE-BQ phase will add it
# 3. Default org_storage_enabled = false; must explicitly enable per environment
# 4. Bucket naming uses environment variable to avoid hard-coded project IDs
# ==============================================================================
