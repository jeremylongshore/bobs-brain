FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies - Bob Brain v5.0
RUN pip install --no-cache-dir \
    flask \
    gunicorn \
    slack-sdk \
    google-genai \
    google-auth \
    google-cloud-bigquery \
    google-cloud-firestore \
    neo4j \
    graphiti-core || echo "Graphiti install failed, continuing..."

# Copy Bob Brain v5.0 - Universal Assistant with Memory
COPY src/bob_brain_v5.py src/

# Set environment
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run Bob Brain v5.0
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 120 src.bob_brain_v5:app
# Cache bust: Sun Aug 10 21:27:44 CDT 2025
# Deploy timestamp: Sun Aug 10 21:44:39 CDT 2025
