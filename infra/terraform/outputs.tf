# Terraform Outputs
# Values available after deployment

# Agent Engine Outputs
output "agent_engine_name" {
  description = "Agent Engine display name"
  value       = google_vertex_ai_reasoning_engine.bob.display_name
}

output "agent_engine_region" {
  description = "Agent Engine deployment region"
  value       = var.region
}

# A2A Gateway Outputs
output "a2a_gateway_url" {
  description = "A2A Gateway public URL"
  value       = google_cloud_run_service.a2a_gateway.status[0].url
}

output "a2a_gateway_service_name" {
  description = "A2A Gateway Cloud Run service name"
  value       = google_cloud_run_service.a2a_gateway.name
}

output "a2a_agentcard_url" {
  description = "AgentCard discovery URL (A2A protocol)"
  value       = "${google_cloud_run_service.a2a_gateway.status[0].url}/.well-known/agent.json"
}

# Slack Webhook Outputs
output "slack_webhook_url" {
  description = "Slack Webhook public URL"
  value       = google_cloud_run_service.slack_webhook.status[0].url
}

output "slack_webhook_service_name" {
  description = "Slack Webhook Cloud Run service name"
  value       = google_cloud_run_service.slack_webhook.name
}

output "slack_events_url" {
  description = "Slack Events API webhook URL (configure in Slack app)"
  value       = "${google_cloud_run_service.slack_webhook.status[0].url}/slack/events"
}

# Service Account Outputs
output "agent_engine_service_account" {
  description = "Agent Engine service account email"
  value       = google_service_account.agent_engine.email
}

output "a2a_gateway_service_account" {
  description = "A2A Gateway service account email"
  value       = google_service_account.a2a_gateway.email
}

output "slack_webhook_service_account" {
  description = "Slack Webhook service account email"
  value       = google_service_account.slack_webhook.email
}

output "github_actions_service_account" {
  description = "GitHub Actions service account email (for CI/CD)"
  value       = google_service_account.github_actions.email
}

# Configuration Outputs
output "environment" {
  description = "Deployment environment"
  value       = var.environment
}

output "project_id" {
  description = "GCP project ID"
  value       = var.project_id
}

output "app_version" {
  description = "Application version"
  value       = var.app_version
}

output "spiffe_id" {
  description = "Agent SPIFFE ID (R7)"
  value       = var.agent_spiffe_id
}

# Deployment Summary
output "deployment_summary" {
  description = "Deployment summary with all important URLs"
  value = {
    environment           = var.environment
    project_id            = var.project_id
    region                = var.region
    app_version           = var.app_version
    agent_engine_id       = google_vertex_ai_reasoning_engine.bob.id
    agent_engine_endpoint = "https://${var.region}-aiplatform.googleapis.com/v1/projects/${var.project_id}/locations/${var.region}/reasoningEngines/${google_vertex_ai_reasoning_engine.bob.id}:query"
    a2a_gateway_url       = google_cloud_run_service.a2a_gateway.status[0].url
    a2a_agentcard_url     = "${google_cloud_run_service.a2a_gateway.status[0].url}/.well-known/agent.json"
    slack_webhook_url     = google_cloud_run_service.slack_webhook.status[0].url
    slack_events_url      = "${google_cloud_run_service.slack_webhook.status[0].url}/slack/events"
    spiffe_id             = var.agent_spiffe_id
  }
}
