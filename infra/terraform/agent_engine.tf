# Vertex AI Agent Engine Configuration
# R2: Agent Engine runtime (not self-hosted)

resource "google_vertex_ai_reasoning_engine" "bob" {
  display_name = "${var.app_name}-${var.environment}"
  location     = var.region
  project      = var.project_id

  spec {
    # Docker container with ADK agent
    # Built from my_agent/ directory
    image = var.agent_docker_image

    # Environment variables for agent runtime
    environment_variables = {
      # GCP Configuration
      PROJECT_ID       = var.project_id
      LOCATION         = var.region
      AGENT_ENGINE_ID  = google_vertex_ai_reasoning_engine.bob.id

      # Application Configuration
      APP_NAME         = var.app_name
      APP_VERSION      = var.app_version

      # SPIFFE ID (R7)
      AGENT_SPIFFE_ID  = var.agent_spiffe_id

      # Public URLs (for AgentCard)
      PUBLIC_URL       = coalesce(var.a2a_gateway_url, google_cloud_run_service.a2a_gateway.status[0].url)

      # AI Model Configuration
      MODEL_NAME       = var.model_name

      # Python Configuration
      PYTHONUNBUFFERED = "1"
      PYTHONDONTWRITEBYTECODE = "1"
    }

    # Compute resources
    # Adjust based on workload requirements
    machine_spec {
      machine_type = var.agent_machine_type
    }

    # Scaling configuration
    replica_count {
      min_replica_count = 1
      max_replica_count = var.agent_max_replicas
    }
  }

  # Service account for Agent Engine
  service_account = google_service_account.agent_engine.email

  # Labels for resource management
  labels = merge(
    var.labels,
    {
      environment = var.environment
      app         = var.app_name
      version     = replace(var.app_version, ".", "-")
      component   = "agent-engine"
    }
  )

  # Lifecycle
  lifecycle {
    # Prevent accidental destruction
    prevent_destroy = false  # Set to true in production

    # Ignore changes to certain fields
    ignore_changes = [
      # Ignore spec changes that trigger replacements
      # Update these manually or via CI/CD
    ]
  }

  depends_on = [
    google_service_account.agent_engine,
    google_project_iam_member.agent_engine_aiplatform,
    google_project_iam_member.agent_engine_vertex,
  ]
}

# Output Agent Engine ID for gateways
output "agent_engine_id" {
  description = "Agent Engine instance ID"
  value       = google_vertex_ai_reasoning_engine.bob.id
}

# Output Agent Engine REST endpoint
output "agent_engine_endpoint" {
  description = "Agent Engine REST API endpoint"
  value       = "https://${var.region}-aiplatform.googleapis.com/v1/projects/${var.project_id}/locations/${var.region}/reasoningEngines/${google_vertex_ai_reasoning_engine.bob.id}:query"
}
