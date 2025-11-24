# IAM Senior ADK DevOps Lead - Foreman Agent Container
#
# Phase 18: Agent Engine Dev Deployment
#
# This Dockerfile builds a containerized foreman agent for deployment to Vertex AI Agent Engine.
# The foreman orchestrates iam-* specialist agents via A2A protocol.
#
# Build command:
#   docker build -t gcr.io/bobs-brain-dev/foreman:0.10.0 -f agents/iam_senior_adk_devops_lead/Dockerfile .
#
# Push command:
#   docker push gcr.io/bobs-brain-dev/foreman:0.10.0

# Base image: Python 3.12 (match repo's Python version)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire agents/ directory
# This includes foreman, shared tools, and A2A components needed for delegation
COPY agents/ ./agents/

# Copy any other necessary source packages
COPY .well-known/ ./.well-known/ 2>/dev/null || true

# Set environment variables
# These will be overridden by Agent Engine runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PROJECT_ID="" \
    LOCATION="us-central1" \
    AGENT_ENGINE_ID="" \
    APP_NAME="iam-senior-adk-devops-lead" \
    AGENT_SPIFFE_ID=""

# Expose port (Agent Engine manages this, but good practice)
EXPOSE 8080

# Entrypoint: Agent Engine will import from agents.iam_senior_adk_devops_lead.agent:app
# The module-level `app` is the deployment entrypoint (6767-LAZY pattern)
CMD ["python", "-m", "agents.iam_senior_adk_devops_lead.agent"]
