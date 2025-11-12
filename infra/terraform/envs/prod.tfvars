# Production Environment Configuration
# terraform apply -var-file="envs/prod.tfvars"

# Project Configuration
project_id  = "bobs-brain"
region      = "us-central1"
environment = "prod"

# Application Configuration
app_name    = "bobs-brain"
app_version = "0.6.0"

# Agent Engine Configuration
agent_docker_image = "gcr.io/bobs-brain/agent:0.6.0"
agent_machine_type = "n1-standard-4"
agent_max_replicas = 5  # Higher for production

# Gateway Configuration
a2a_gateway_image   = "gcr.io/bobs-brain/a2a-gateway:0.6.0"
slack_webhook_image = "gcr.io/bobs-brain/slack-webhook:0.6.0"
gateway_max_instances = 20  # More instances for production

# Slack Configuration (production credentials)
# CRITICAL: Use Secret Manager or secure CI/CD secrets for production
# These are placeholders - replace with actual values or use Secret Manager
slack_bot_token      = "xoxb-prod-placeholder"  # REPLACE WITH ACTUAL TOKEN
slack_signing_secret = "prod-placeholder"       # REPLACE WITH ACTUAL SECRET

# SPIFFE ID (R7)
agent_spiffe_id = "spiffe://intent.solutions/agent/bobs-brain/prod/us-central1/0.6.0"

# AI Model Configuration
model_name = "gemini-2.0-flash-exp"

# Networking
allow_public_access = true

# Labels
labels = {
  cost_center = "production"
  team        = "platform"
  critical    = "true"
}
