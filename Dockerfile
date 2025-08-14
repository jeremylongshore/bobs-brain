FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies - Bob Brain Enterprise with Vertex AI
RUN pip install --no-cache-dir \
    flask \
    gunicorn \
    slack-sdk \
    google-cloud-aiplatform \
    vertexai \
    google-generativeai \
    google-auth \
    google-cloud-bigquery \
    google-cloud-datastore \
    neo4j \
    pytz \
    python-dotenv

# Copy Bob Brain Enterprise v7 - CEO Grade
COPY src/bob_brain_enterprise.py src/
COPY src/graphiti_integration.py src/
COPY src/circle_of_life.py src/

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV NEO4J_URI=neo4j+s://d3653283.databases.neo4j.io
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE
ENV GCP_PROJECT=bobs-house-ai
ENV GOOGLE_CLOUD_PROJECT=bobs-house-ai

# Run Bob Brain Enterprise v7.0 - 24/7 CEO Assistant
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 120 src.bob_brain_enterprise:app
# Cache bust: Wed Aug 14 2025 - Vertex AI Gemini Integration
# Deploy timestamp: Wed Aug 14 2025
