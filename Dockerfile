# Use a Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY ./src ./src
COPY ./config ./config
COPY ./scripts ./scripts
COPY ./data ./data
COPY ./agent ./agent

# Create necessary directories
RUN mkdir -p /home/.bob_brain/chroma

# Create .env from environment if it doesn't exist
RUN touch .env

# Expose the port for the API
EXPOSE 5000

# Command to run Bob
CMD ["python", "src/bob_unified_v2.py"]
