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

# Copy the agent code and data into the container
COPY ./agent ./agent
COPY ./data ./data

# Create .env from environment if it doesn't exist
RUN touch .env

# Expose the port for the Slack integration
EXPOSE 3000

# Command to run the main agent
CMD ["python", "agent/main_agent.py"]
