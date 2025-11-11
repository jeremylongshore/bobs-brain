variable "project_id" { type = string }
variable "region" {
  type    = string
  default = "us-central1"
}
variable "repo_name" {
  type    = string
  default = "bobs-brain"
}
variable "service_name" {
  type    = string
  default = "bobs-brain"
}
variable "image" {
  type    = string
  default = "us-docker.pkg.dev/PROJECT/REPO/IMAGE:tag"
}
