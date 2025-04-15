# Dockerfile.locust

FROM python:3.11-slim

# Set working directory
WORKDIR /locust

# Copy your locust tests into the container
COPY . .

# Install additional dependencies if needed
RUN pip install --no-cache-dir -r requirements-locust.txt

# Default command to run locust
CMD ["locust", "-f", "locustfile.py"]