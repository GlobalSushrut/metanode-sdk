FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy MetaNode SDK
COPY . /app/

# Install the SDK
RUN pip install --no-cache-dir -e .

# Use console mode by default
ENV CONSOLE_MODE=true
ENV METANODE_ENV=testnet
ENV ZK_PROOF_LEVEL=testnet

# Default command
ENTRYPOINT ["python", "-m", "metanode.validator.service"]
CMD ["--console-mode"]
