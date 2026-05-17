# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create uploads directory inside container
RUN mkdir -p uploads

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
