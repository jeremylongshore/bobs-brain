variable "project_id" { type = string }
variable "api_services" {
  type    = list(string)
  default = [
    "aiplatform.googleapis.com",
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "cloudtrace.googleapis.com",
    "secretmanager.googleapis.com"
  ]
}
