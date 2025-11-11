resource "google_project_service" "services" {
  for_each           = toset(var.api_services)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}
