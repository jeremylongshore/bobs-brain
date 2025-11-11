variable "project_id"   { type = string }
variable "region"       { type = string }
variable "service_name" { type = string }
variable "image"        { type = string }
variable "create" {
  type    = bool
  default = false
}
