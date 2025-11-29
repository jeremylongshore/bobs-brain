# Slack Bob Gateway Module - Outputs

output "service_name" {
  description = "Name of the Cloud Run service"
  value       = var.enable ? google_cloud_run_v2_service.slack_gateway[0].name : null
}

output "service_url" {
  description = "URL of the Cloud Run service"
  value       = var.enable ? google_cloud_run_v2_service.slack_gateway[0].uri : null
}

output "service_id" {
  description = "ID of the Cloud Run service"
  value       = var.enable ? google_cloud_run_v2_service.slack_gateway[0].id : null
}

output "webhook_url" {
  description = "Slack webhook URL (for Slack app configuration)"
  value       = var.enable ? "${google_cloud_run_v2_service.slack_gateway[0].uri}/slack/events" : null
}

output "enabled" {
  description = "Whether the Slack gateway is enabled"
  value       = var.enable
}
