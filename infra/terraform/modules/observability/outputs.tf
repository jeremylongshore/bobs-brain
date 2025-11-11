output "dashboard_id" {
  description = "Cloud Monitoring dashboard ID"
  value       = google_monitoring_dashboard.gateway.id
}

output "latency_alert_id" {
  description = "Latency alert policy ID"
  value       = google_monitoring_alert_policy.latency_p95.id
}

output "error_rate_alert_id" {
  description = "Error rate alert policy ID"
  value       = google_monitoring_alert_policy.error_rate.id
}

output "budget_id" {
  description = "Budget ID"
  value       = google_billing_budget.monthly.id
}

output "dashboard_url" {
  description = "Dashboard URL in Cloud Console"
  value       = "https://console.cloud.google.com/monitoring/dashboards/custom/${google_monitoring_dashboard.gateway.id}?project=${var.project_id}"
}
