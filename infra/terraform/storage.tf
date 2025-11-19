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
