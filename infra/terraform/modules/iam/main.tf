resource "google_service_account" "app" {
  account_id   = var.sa_app_id
  display_name = "bobs-brain app runtime"
}

resource "google_service_account" "cd" {
  account_id   = var.sa_cd_id
  display_name = "bobs-brain CI/CD"
}

resource "google_project_iam_member" "cd_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.cd.email}"
}

resource "google_project_iam_member" "cd_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.cd.email}"
}

resource "google_project_iam_member" "app_aiplatform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.app.email}"
}
