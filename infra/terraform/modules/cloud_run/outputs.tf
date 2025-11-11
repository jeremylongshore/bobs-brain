output "url" {
  value = try(google_cloud_run_v2_service.svc[0].uri, null)
}
