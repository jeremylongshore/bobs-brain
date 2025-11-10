# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

provider "github" {
  owner = var.repository_owner
}

# Try to get existing repo
data "github_repository" "existing_repo" {
  count = var.create_repository ? 0 : 1
  full_name = "${var.repository_owner}/${var.repository_name}"
}

# Only create GitHub repo if create_repository is true
resource "github_repository" "repo" {
  count       = var.create_repository ? 1 : 0
  name        = var.repository_name
  description = "Repository created with goo.gle/agent-starter-pack"
  visibility  = "private"

  has_issues      = true
  has_wiki        = false
  has_projects    = false
  has_downloads   = false

  allow_merge_commit = true
  allow_squash_merge = true
  allow_rebase_merge = true
  
  auto_init = false
}


resource "github_actions_variable" "gcp_project_number" {
  repository    = var.repository_name
  variable_name = "GCP_PROJECT_NUMBER"
  value         = data.google_project.cicd_project.number
  depends_on    = [github_repository.repo]
}

resource "github_actions_secret" "wif_pool_id" {
  repository      = var.repository_name
  secret_name     = "WIF_POOL_ID"
  plaintext_value = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  depends_on      = [github_repository.repo, data.github_repository.existing_repo]
}

resource "github_actions_secret" "wif_provider_id" {
  repository      = var.repository_name
  secret_name     = "WIF_PROVIDER_ID"
  plaintext_value = google_iam_workload_identity_pool_provider.github_provider.workload_identity_pool_provider_id
  depends_on      = [github_repository.repo, data.github_repository.existing_repo]
}

resource "github_actions_secret" "gcp_service_account" {
  repository      = var.repository_name
  secret_name     = "GCP_SERVICE_ACCOUNT"
  plaintext_value = google_service_account.cicd_runner_sa.email
  depends_on      = [github_repository.repo, data.github_repository.existing_repo]
}

resource "github_actions_variable" "staging_project_id" {
  repository    = var.repository_name
  variable_name = "STAGING_PROJECT_ID"
  value         = var.staging_project_id
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "prod_project_id" {
  repository    = var.repository_name
  variable_name = "PROD_PROJECT_ID"
  value         = var.prod_project_id
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "region" {
  repository    = var.repository_name
  variable_name = "REGION"
  value         = var.region
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "cicd_project_id" {
  repository    = var.repository_name
  variable_name = "CICD_PROJECT_ID"
  value         = var.cicd_runner_project_id
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "app_sa_email_staging" {
  repository    = var.repository_name
  variable_name = "APP_SA_EMAIL_STAGING"
  value         = google_service_account.app_sa["staging"].email
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "app_sa_email_prod" {
  repository    = var.repository_name
  variable_name = "APP_SA_EMAIL_PROD"
  value         = google_service_account.app_sa["prod"].email
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "logs_bucket_name_staging" {
  repository    = var.repository_name
  variable_name = "LOGS_BUCKET_NAME_STAGING"
  value         = google_storage_bucket.logs_data_bucket[var.staging_project_id].name
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "logs_bucket_name_prod" {
  repository    = var.repository_name
  variable_name = "LOGS_BUCKET_NAME_PROD"
  value         = google_storage_bucket.logs_data_bucket[var.prod_project_id].name
  depends_on    = [github_repository.repo]
}




resource "github_actions_variable" "pipeline_gcs_root_staging" {
  repository    = var.repository_name
  variable_name = "PIPELINE_GCS_ROOT_STAGING"
  value         = "gs://${google_storage_bucket.data_ingestion_pipeline_gcs_root["staging"].name}"
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "pipeline_gcs_root_prod" {
  repository    = var.repository_name
  variable_name = "PIPELINE_GCS_ROOT_PROD"
  value         = "gs://${google_storage_bucket.data_ingestion_pipeline_gcs_root["prod"].name}"
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "pipeline_sa_email_staging" {
  repository    = var.repository_name
  variable_name = "PIPELINE_SA_EMAIL_STAGING"
  value         = google_service_account.vertexai_pipeline_app_sa["staging"].email
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "pipeline_sa_email_prod" {
  repository    = var.repository_name
  variable_name = "PIPELINE_SA_EMAIL_PROD"
  value         = google_service_account.vertexai_pipeline_app_sa["prod"].email
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "pipeline_name" {
  repository    = var.repository_name
  variable_name = "PIPELINE_NAME"
  value         = var.project_name
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "pipeline_cron_schedule" {
  repository    = var.repository_name
  variable_name = "PIPELINE_CRON_SCHEDULE"
  value         = var.pipeline_cron_schedule
  depends_on    = [github_repository.repo]
}


resource "github_actions_variable" "data_store_id_staging" {
  repository    = var.repository_name
  variable_name = "DATA_STORE_ID_STAGING"
  value         = google_discovery_engine_data_store.data_store_staging.data_store_id
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "data_store_id_prod" {
  repository    = var.repository_name
  variable_name = "DATA_STORE_ID_PROD"
  value         = google_discovery_engine_data_store.data_store_prod.data_store_id
  depends_on    = [github_repository.repo]
}

resource "github_actions_variable" "data_store_region" {
  repository    = var.repository_name
  variable_name = "DATA_STORE_REGION"
  value         = var.data_store_region
  depends_on    = [github_repository.repo]
}



resource "github_repository_environment" "production_environment" {
  repository  = var.repository_name
  environment = "production"
  depends_on  = [github_repository.repo, data.github_repository.existing_repo]

  deployment_branch_policy {
    protected_branches     = false
    custom_branch_policies = true
  }
}
