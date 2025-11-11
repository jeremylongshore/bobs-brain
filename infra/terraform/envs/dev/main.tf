terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.43" }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "project" {
  source     = "../../modules/project"
  project_id = var.project_id
}

module "iam" {
  source     = "../../modules/iam"
  project_id = var.project_id
}

module "artifact_registry" {
  source     = "../../modules/artifact_registry"
  project_id = var.project_id
  region     = var.region
  repo_name  = var.repo_name
}

module "cloud_run" {
  source       = "../../modules/cloud_run"
  project_id   = var.project_id
  region       = var.region
  service_name = var.service_name
  image        = var.image
  create       = false
}

module "agent_engine_bootstrap" {
  source     = "../../modules/agent_engine_bootstrap"
  project_id = var.project_id
  region     = var.region
}
