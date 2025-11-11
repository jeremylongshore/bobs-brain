resource "null_resource" "agent_engine" {
  provisioner "local-exec" {
    command     = "PROJECT_ID=${var.project_id} LOCATION=${var.region} bash ../../../scripts/deploy_agent_engine.sh"
    working_dir = "${path.module}/../../../.."
  }
}
