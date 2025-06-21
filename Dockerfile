FROM python:3.10-slim

LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="MetaNode SDK - Blockchain & dApp Deployment Infrastructure"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Docker client for container integrations
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy SDK files
COPY . .

# Install the SDK in development mode
RUN pip install -e .

# Verify installation
RUN metanode-cli --version || echo "CLI not installed correctly"

# Environment setup
ENV PYTHONUNBUFFERED=1
ENV METANODE_HOME=/app

# Default command
ENTRYPOINT ["metanode-cli"]
CMD ["--help"]
