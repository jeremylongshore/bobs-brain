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

# Output for deployment workflows
output "staging_bucket_url" {
  description = "GCS staging bucket URL for ADK CLI deployments"
  value       = "gs://${google_storage_bucket.adk_staging.name}"
}

output "staging_bucket_name" {
  description = "GCS staging bucket name"
  value       = google_storage_bucket.adk_staging.name
}
