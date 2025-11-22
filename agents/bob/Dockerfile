# Bob's Brain - Bob (Global Orchestrator) Agent Container
#
# Phase 18: Agent Engine Dev Deployment
#
# This Dockerfile builds a containerized agent for deployment to Vertex AI Agent Engine.
# It follows ADK + Vertex AI Agent Engine patterns with module-level `app` export.
#
# Build command:
#   docker build -t gcr.io/bobs-brain-dev/agent:0.10.0 -f agents/bob/Dockerfile .
#
# Push command:
#   docker push gcr.io/bobs-brain-dev/agent:0.10.0

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
# This includes bob and all shared tools/modules
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
    APP_NAME="bobs-brain" \
    AGENT_SPIFFE_ID=""

# Expose port (Agent Engine manages this, but good practice)
EXPOSE 8080

# Entrypoint: Agent Engine will import from agents.bob.agent:app
# The module-level `app` is the deployment entrypoint (6767-LAZY pattern)
CMD ["python", "-m", "agents.bob.agent"]
