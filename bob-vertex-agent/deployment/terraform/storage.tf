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

provider "google" {
  region = var.region
  user_project_override = true
}

resource "google_storage_bucket" "logs_data_bucket" {
  for_each                    = toset(local.all_project_ids)
  name                        = "${each.value}-${var.project_name}-logs"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}



resource "google_storage_bucket" "data_ingestion_pipeline_gcs_root" {
  for_each                    = local.deploy_project_ids
  name                        = "${each.value}-${var.project_name}-rag"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}



resource "google_discovery_engine_data_store" "data_store_staging" {
  location                    = var.data_store_region
  project                     = var.staging_project_id
  data_store_id               = "${var.project_name}-datastore"
  display_name                = "${var.project_name}-datastore"
  industry_vertical           = "GENERIC"
  content_config              = "NO_CONTENT"
  solution_types              = ["SOLUTION_TYPE_SEARCH"]
  create_advanced_site_search = false
  provider                    = google.staging_billing_override
  depends_on         = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}

resource "google_discovery_engine_search_engine" "search_engine_staging" {
  project        = var.staging_project_id
  engine_id      = "${var.project_name}-search"
  collection_id  = "default_collection"
  location       = google_discovery_engine_data_store.data_store_staging.location
  display_name   = "Search Engine App Staging"
  data_store_ids = [google_discovery_engine_data_store.data_store_staging.data_store_id]
  search_engine_config {
    search_tier = "SEARCH_TIER_ENTERPRISE"
  }
  provider = google.staging_billing_override
}

resource "google_discovery_engine_data_store" "data_store_prod" {
  location                    = var.data_store_region
  project                     = var.prod_project_id
  data_store_id               = "${var.project_name}-datastore"
  display_name                = "${var.project_name}-datastore"
  industry_vertical           = "GENERIC"
  content_config              = "NO_CONTENT"
  solution_types              = ["SOLUTION_TYPE_SEARCH"]
  create_advanced_site_search = false
  provider                    = google.prod_billing_override
  depends_on         = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}

resource "google_discovery_engine_search_engine" "search_engine_prod" {
  project        = var.prod_project_id
  engine_id      = "${var.project_name}-search"
  collection_id  = "default_collection"
  location       = google_discovery_engine_data_store.data_store_prod.location
  display_name   = "Search Engine App Prod"
  data_store_ids = [google_discovery_engine_data_store.data_store_prod.data_store_id]
  search_engine_config {
    search_tier = "SEARCH_TIER_ENTERPRISE"
  }
  provider = google.prod_billing_override
}


