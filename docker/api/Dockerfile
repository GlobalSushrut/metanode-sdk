FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy MetaNode SDK
COPY . /app/

# Install the SDK
RUN pip install --no-cache-dir -e .

# Use console mode by default and use existing Docker vPod containers
ENV CONSOLE_MODE=true
ENV USE_EXISTING_VPOD=true
ENV METANODE_ENV=testnet

# Default command - ensuring we use console mode and existing vPod containers
ENTRYPOINT ["python", "-m", "metanode.api.server"]
CMD ["--console-mode", "--use-existing-vpod"]
