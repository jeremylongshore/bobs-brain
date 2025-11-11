# Cloud Run Gateway Module
#
# Deploys FastAPI gateway to Cloud Run that proxies to Reasoning Engine.
# CRITICAL: Gateway does NOT run the agent - it calls Vertex AI REST API.

terraform {
  required_version = "~> 1.9"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "bobs-brain-gateway"
}

variable "image" {
  description = "Container image for gateway"
  type        = string
}

variable "env" {
  description = "Environment variables for gateway"
  type        = map(string)
  default     = {}
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 10
}

variable "cpu" {
  description = "CPU allocation (e.g., '1' for 1 CPU)"
  type        = string
  default     = "1"
}

variable "memory" {
  description = "Memory allocation (e.g., '512Mi')"
  type        = string
  default     = "512Mi"
}

# Service Account for Cloud Run
resource "google_service_account" "sa" {
  account_id   = "${var.service_name}-sa"
  display_name = "Gateway Service Account"
  project      = var.project_id
}

# Grant aiplatform.user role (needed to call Reasoning Engine API)
resource "google_project_iam_member" "sa_aiplatform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

# Grant cloudtrace.agent role (needed for Cloud Trace export)
resource "google_project_iam_member" "sa_cloudtrace_agent" {
  project = var.project_id
  role    = "roles/cloudtrace.agent"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

# Cloud Run Service
resource "google_cloud_run_v2_service" "svc" {
  name     = var.service_name
  location = var.region
  project  = var.project_id

  template {
    service_account = google_service_account.sa.email

    # Scaling configuration
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = var.image

      # Resource limits
      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
        cpu_idle = true
      }

      # Standard environment variables
      env {
        name  = "ENGINE_MODE"
        value = lookup(var.env, "ENGINE_MODE", "agent_engine")
      }

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "LOCATION"
        value = lookup(var.env, "LOCATION", var.region)
      }

      env {
        name  = "AGENT_ENGINE_ID"
        value = lookup(var.env, "AGENT_ENGINE_ID", "")
      }

      env {
        name  = "AGENT_ENGINE_NAME"
        value = lookup(var.env, "AGENT_ENGINE_NAME", "")
      }

      # A2A card configuration
      env {
        name  = "A2A_NAME"
        value = lookup(var.env, "A2A_NAME", "Bob's Brain")
      }

      env {
        name  = "A2A_DESC"
        value = lookup(var.env, "A2A_DESC", "A2A gateway. Agent runs on Vertex AI Reasoning Engine.")
      }

      env {
        name  = "A2A_VERSION"
        value = lookup(var.env, "A2A_VERSION", "4.0.0")
      }

      ports {
        container_port = 8080
      }

      # Health check
      startup_probe {
        http_get {
          path = "/_health"
          port = 8080
        }
        initial_delay_seconds = 10
        timeout_seconds       = 3
        period_seconds        = 5
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/_health"
          port = 8080
        }
        initial_delay_seconds = 30
        timeout_seconds       = 3
        period_seconds        = 10
        failure_threshold     = 3
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  ingress = "INGRESS_TRAFFIC_ALL"

  depends_on = [
    google_project_iam_member.sa_aiplatform_user,
    google_project_iam_member.sa_cloudtrace_agent,
  ]
}

# Allow unauthenticated access (adjust for production)
resource "google_cloud_run_v2_service_iam_member" "noauth" {
  name     = google_cloud_run_v2_service.svc.name
  location = google_cloud_run_v2_service.svc.location
  project  = google_cloud_run_v2_service.svc.project
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Outputs
output "gateway_url" {
  description = "Cloud Run gateway URL"
  value       = google_cloud_run_v2_service.svc.uri
}

output "service_name" {
  description = "Cloud Run service name"
  value       = google_cloud_run_v2_service.svc.name
}

output "service_account_email" {
  description = "Service account email"
  value       = google_service_account.sa.email
}
