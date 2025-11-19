# Development Environment Configuration
# terraform apply -var-file="envs/dev.tfvars"

# Project Configuration
project_id  = "bobs-brain-dev"
region      = "us-central1"
environment = "dev"

# Application Configuration
app_name    = "bobs-brain"
app_version = "0.6.0"

# Agent Engine Configuration
agent_docker_image = "gcr.io/bobs-brain-dev/agent:0.6.0"
agent_machine_type = "n1-standard-2"  # Smaller for dev
agent_max_replicas = 2

# Gateway Configuration
a2a_gateway_image   = "gcr.io/bobs-brain-dev/a2a-gateway:0.6.0"
slack_webhook_image = "gcr.io/bobs-brain-dev/slack-webhook:0.6.0"
gateway_max_instances = 5  # Fewer instances for dev

# Slack Configuration (dev credentials)
# IMPORTANT: Use Secret Manager or CI/CD secrets in production
slack_bot_token      = "xoxb-dev-placeholder"
slack_signing_secret = "dev-placeholder"

# SPIFFE ID (R7)
agent_spiffe_id = "spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0"

# AI Model Configuration
model_name = "gemini-2.0-flash-exp"

# Networking
allow_public_access = true

# Labels
labels = {
  cost_center = "development"
  team        = "platform"
}

# ADK Deployment Configuration
# Staging bucket created by storage.tf (output: staging_bucket_url)
# Used by: adk deploy agent_engine --staging_bucket
# Format: gs://<project-id>-adk-staging
