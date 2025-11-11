# Terraform module for Google Secret Manager secrets
#
# Creates and manages Secret Manager secrets for the Bob's Brain application
# Supports automatic replication and version management

resource "google_secret_manager_secret" "secrets" {
  for_each = var.secrets

  project   = var.project_id
  secret_id = each.key

  replication {
    auto {}
  }

  labels = merge(
    var.labels,
    {
      managed_by = "terraform"
      component  = "bobs-brain"
    }
  )
}

resource "google_secret_manager_secret_version" "secret_versions" {
  for_each = {
    for k, v in var.secrets : k => v
    if v != null && v != ""
  }

  secret      = google_secret_manager_secret.secrets[each.key].id
  secret_data = each.value
}
