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
  name                        = "${var.dev_project_id}-${var.project_name}-logs"
  location                    = var.region
  project                     = var.dev_project_id
  uniform_bucket_level_access = true

  depends_on = [resource.google_project_service.services]
}


resource "google_storage_bucket" "data_ingestion_PIPELINE_GCS_ROOT" {
  name                        = "${var.dev_project_id}-${var.project_name}-rag"
  location                    = var.region
  project                     = var.dev_project_id
  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [resource.google_project_service.services]
}


resource "google_discovery_engine_data_store" "data_store_dev" {
  location                    = var.data_store_region
  project                     = var.dev_project_id
  data_store_id               = "${var.project_name}-datastore"
  display_name                = "${var.project_name}-datastore"
  industry_vertical           = "GENERIC"
  content_config              = "NO_CONTENT"
  solution_types              = ["SOLUTION_TYPE_SEARCH"]
  create_advanced_site_search = false
  provider                    = google.dev_billing_override
  depends_on             = [resource.google_project_service.services]
}

resource "google_discovery_engine_search_engine" "search_engine_dev" {
  project        = var.dev_project_id
  engine_id      = "${var.project_name}-search"
  collection_id  = "default_collection"
  location       = google_discovery_engine_data_store.data_store_dev.location
  display_name   = "Search Engine App Staging"
  data_store_ids = [google_discovery_engine_data_store.data_store_dev.data_store_id]
  search_engine_config {
    search_tier = "SEARCH_TIER_ENTERPRISE"
  }
  provider      = google.dev_billing_override
}


