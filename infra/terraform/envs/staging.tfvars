# Staging Environment Configuration
# terraform apply -var-file="envs/staging.tfvars"

# Project Configuration
project_id  = "bobs-brain-staging"
region      = "us-central1"
environment = "staging"

# Application Configuration
app_name    = "bobs-brain"
app_version = "0.6.0"

# Agent Engine Configuration
agent_docker_image = "gcr.io/bobs-brain-staging/agent:0.6.0"
agent_machine_type = "n1-standard-4"
agent_max_replicas = 3

# Gateway Configuration
a2a_gateway_image   = "gcr.io/bobs-brain-staging/a2a-gateway:0.6.0"
slack_webhook_image = "gcr.io/bobs-brain-staging/slack-webhook:0.6.0"
gateway_max_instances = 10

# Slack Configuration (staging credentials)
# IMPORTANT: Use Secret Manager or CI/CD secrets in production
slack_bot_token      = "xoxb-staging-placeholder"
slack_signing_secret = "staging-placeholder"

# SPIFFE ID (R7)
agent_spiffe_id = "spiffe://intent.solutions/agent/bobs-brain/staging/us-central1/0.6.0"

# AI Model Configuration
model_name = "gemini-2.0-flash-exp"

# Vertex AI Search Configuration (Phase 3)
vertex_search_datastore_id = "adk-documentation"

# Networking
allow_public_access = true

# Labels
labels = {
  cost_center = "staging"
  team        = "platform"
}
