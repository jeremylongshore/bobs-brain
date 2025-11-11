# Outputs for Secret Manager module

output "secret_ids" {
  description = "Map of secret names to their full resource IDs"
  value = {
    for k, v in google_secret_manager_secret.secrets : k => v.id
  }
}

output "secret_names" {
  description = "List of created secret names"
  value       = keys(google_secret_manager_secret.secrets)
}

output "secrets_map" {
  description = "Map of secret names to secret resource objects"
  value       = google_secret_manager_secret.secrets
  sensitive   = true
}
