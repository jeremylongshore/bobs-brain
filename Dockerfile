FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements-cloudrun.txt .
RUN pip install --no-cache-dir -r requirements-cloudrun.txt

# Copy only the necessary files
COPY src/bob_cloud_run.py src/
COPY .env* ./

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 3000

# Start Bob Cloud Run with Flask HTTP server
CMD ["python", "src/bob_cloud_run.py"]