# Use latest patched Python slim image
FROM python:3.13-slim

# Patch OS-level vulnerabilities in base image
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements first (layer caching — faster rebuilds)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 5000 to the host
EXPOSE 5000

# Bind inside the container; local runs default to loopback only.
ENV HOST=0.0.0.0

# Run the Flask app
CMD ["python", "app.py"]