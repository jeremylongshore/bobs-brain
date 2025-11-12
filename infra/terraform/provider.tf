# Provider Configuration
# R4 Compliance: Supports Workload Identity Federation for CI-only deployments

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.6.0"
    }
  }

  # Backend configuration for state management
  # Uncomment and configure for production use
  # backend "gcs" {
  #   bucket = "bobs-brain-terraform-state"
  #   prefix = "terraform/state"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region

  # Workload Identity Federation (for GitHub Actions CI)
  # This allows CI to authenticate without service account keys (R4)
  # Configure in GitHub Actions workflow with:
  #   - uses: google-github-actions/auth@v1
  #     with:
  #       workload_identity_provider: 'projects/.../locations/global/workloadIdentityPools/.../providers/...'
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}
