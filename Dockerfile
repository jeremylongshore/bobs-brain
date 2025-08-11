FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask \
    gunicorn \
    slack-sdk \
    google-cloud-aiplatform \
    google-cloud-bigquery \
    google-cloud-firestore \
    vertexai \
    graphiti-core \
    neo4j \
    asyncio

# Copy the production Bob
COPY src/bob_final.py src/

# Set environment
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run Bob Final (production version)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 120 src.bob_final:app