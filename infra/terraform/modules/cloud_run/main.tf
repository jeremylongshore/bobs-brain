resource "google_cloud_run_v2_service" "svc" {
  count    = var.create ? 1 : 0
  name     = var.service_name
  location = var.region
  template {
    containers { image = var.image }
  }
}
