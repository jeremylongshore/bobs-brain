FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies - NEW Google Gen AI SDK
RUN pip install --no-cache-dir \
    flask \
    gunicorn \
    slack-sdk \
    google-genai \
    google-auth \
    google-cloud-bigquery \
    google-cloud-firestore

# Copy the WORKING Bob with NEW SDK
COPY src/bob_production_final.py src/

# Set environment
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run Bob Production Final v4.0
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 120 src.bob_production_final:app
# Cache bust: Sun Aug 10 21:27:44 CDT 2025
# Deploy timestamp: Sun Aug 10 21:44:39 CDT 2025
