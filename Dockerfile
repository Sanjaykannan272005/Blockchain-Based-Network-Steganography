# Use a stable Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# libpcap-dev is required for scapy packet sniffing
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir kyber-py

# Copy project files
COPY . .

# Default command (can be overridden in docker-compose)
CMD ["python", "app.py"]
