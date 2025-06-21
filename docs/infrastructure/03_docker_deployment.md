# Docker-based Infrastructure Deployment

This document provides instructions for deploying MetaNode infrastructure using Docker containers, an alternative to Kubernetes for simpler environments or local development.

## Prerequisites

- Docker Engine (v19.03+)
- Docker Compose (v1.27+)
- MetaNode SDK installed (`pip install metanode-sdk`)
- Minimum 4GB RAM and 2 CPU cores available

## Overview

Docker provides a lightweight alternative to Kubernetes for MetaNode infrastructure deployment. This approach is ideal for:

- Development environments
- Single-host deployments
- Testing and proof-of-concept scenarios
- Environments without Kubernetes

## Docker Network Setup

First, create a dedicated network for MetaNode components:

```bash
# Create Docker network
docker network create metanode-net
```

## Deployment Options

### Option 1: Automated Deployment with SDK

The easiest approach is using the SDK's Docker deployment functionality:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Deploy with Docker
deployment = sdk.deploy_docker_infrastructure(
    app_name="my-app",
    components=["blockchain", "validator", "agreement", "ipfs"],
    data_dir="~/.metanode/data",
    ports={
        "blockchain_rpc": 8545,
        "blockchain_ws": 8546,
        "api": 8000
    }
)

# Check deployment status
status = sdk.check_docker_infrastructure_status("my-app")
print(f"Infrastructure status: {status}")
```

### Option 2: CLI-based Deployment

For command-line deployment:

```bash
# Deploy using the CLI
metanode-cli infra deploy-docker \
  --app my-app \
  --components blockchain,validator,agreement,ipfs \
  --data-dir ~/.metanode/data \
  --publish blockchain-rpc:8545,blockchain-ws:8546,api:8000
```

### Option 3: Docker Compose

For customizable deployments, the SDK can generate a `docker-compose.yml` file:

```bash
# Generate Docker Compose file
metanode-cli infra generate-compose \
  --output-file ./docker-compose.yml \
  --app my-app
  
# Deploy using Docker Compose
docker-compose -f ./docker-compose.yml up -d
```

Example `docker-compose.yml`:

```yaml
version: '3.8'

services:
  metanode-blockchain:
    image: metanode/blockchain:latest
    container_name: metanode-blockchain
    environment:
      - METANODE_ROLE=blockchain
      - METANODE_NETWORK=testnet
    volumes:
      - ~/.metanode/data/blockchain:/data
    ports:
      - "8545:8545"
      - "8546:8546"
    networks:
      - metanode-net
    restart: unless-stopped

  metanode-validator:
    image: metanode/validator:latest
    container_name: metanode-validator
    depends_on:
      - metanode-blockchain
    environment:
      - METANODE_ROLE=validator
      - METANODE_BLOCKCHAIN_URL=http://metanode-blockchain:8545
    volumes:
      - ~/.metanode/data/validator:/data
    networks:
      - metanode-net
    restart: unless-stopped

  metanode-agreement:
    image: metanode/agreement:latest
    container_name: metanode-agreement
    depends_on:
      - metanode-blockchain
      - metanode-validator
    environment:
      - METANODE_ROLE=agreement
      - METANODE_BLOCKCHAIN_URL=http://metanode-blockchain:8545
      - METANODE_VALIDATOR_URL=http://metanode-validator:7545
    volumes:
      - ~/.metanode/data/agreement:/data
    networks:
      - metanode-net
    restart: unless-stopped

  metanode-ipfs:
    image: metanode/ipfs:latest
    container_name: metanode-ipfs
    environment:
      - METANODE_ROLE=ipfs
    volumes:
      - ~/.metanode/data/ipfs:/data/ipfs
    ports:
      - "5001:5001"
      - "8080:8080"
    networks:
      - metanode-net
    restart: unless-stopped

  metanode-api:
    image: metanode/api:latest
    container_name: metanode-api
    depends_on:
      - metanode-blockchain
      - metanode-validator
      - metanode-ipfs
    environment:
      - METANODE_BLOCKCHAIN_URL=http://metanode-blockchain:8545
      - METANODE_VALIDATOR_URL=http://metanode-validator:7545
      - METANODE_IPFS_URL=http://metanode-ipfs:5001
    ports:
      - "8000:8000"
    networks:
      - metanode-net
    restart: unless-stopped

networks:
  metanode-net:
    external: true
```

## vPod Container Setup

The MetaNode infrastructure uses specialized vPod containers within Docker:

```bash
# Pull vPod images
docker pull metanode/blockchain:latest
docker pull metanode/validator:latest
docker pull metanode/agreement:latest
docker pull metanode/ipfs:latest

# Run a blockchain vPod
docker run -d \
  --name metanode-blockchain-vpod \
  --network metanode-net \
  -e METANODE_ROLE=blockchain \
  -e METANODE_NETWORK=testnet \
  -v ~/.metanode/data/blockchain:/data \
  -p 8545:8545 -p 8546:8546 \
  metanode/blockchain:latest
```

## Data Persistence

Configure volume mounts for persistent data:

```bash
# Create directories for persistent data
mkdir -p ~/.metanode/data/{blockchain,validator,agreement,ipfs}

# Example docker run with volume mounts
docker run -d \
  --name metanode-blockchain \
  -v ~/.metanode/data/blockchain:/data \
  metanode/blockchain:latest
```

## Resource Configuration

Configure container resources according to your needs:

```bash
# Example with resource limits
docker run -d \
  --name metanode-blockchain \
  --cpus 2 \
  --memory 4g \
  -v ~/.metanode/data/blockchain:/data \
  metanode/blockchain:latest
```

## Environment Variables

Configure components with environment variables:

### Blockchain Node

```bash
docker run -d \
  --name metanode-blockchain \
  -e METANODE_NETWORK=testnet \
  -e METANODE_LOG_LEVEL=info \
  -e METANODE_RPC_HOST=0.0.0.0 \
  -e METANODE_RPC_PORT=8545 \
  -e METANODE_WS_ENABLED=true \
  metanode/blockchain:latest
```

### Validator Node

```bash
docker run -d \
  --name metanode-validator \
  -e METANODE_BLOCKCHAIN_URL=http://metanode-blockchain:8545 \
  -e METANODE_VALIDATOR_PORT=7545 \
  -e METANODE_VALIDATION_MODE=full \
  metanode/validator:latest
```

## Connecting to External Testnet

Connect your Docker containers to the MetaNode testnet:

```bash
docker run -d \
  --name metanode-testnet-connector \
  --network metanode-net \
  -e METANODE_TESTNET_RPC=http://159.203.17.36:8545 \
  -e METANODE_TESTNET_WS=ws://159.203.17.36:8546 \
  -v ~/.metanode/testnet-config:/config \
  -p 6545:6545 \
  metanode/testnet-connector:latest
```

## Monitoring

Monitor your Docker-based infrastructure:

```bash
# Check container status
docker ps -a --filter name=metanode

# View logs
docker logs metanode-blockchain

# View container stats
docker stats metanode-blockchain metanode-validator metanode-agreement
```

## Security Best Practices

1. **Network Isolation**: Use the dedicated `metanode-net` network
2. **Volume Permissions**: Set appropriate permissions on data directories
3. **Resource Limits**: Set memory and CPU limits to prevent resource exhaustion
4. **Restart Policies**: Use `restart: unless-stopped` for automatic recovery
5. **Regular Updates**: Keep Docker images updated

```bash
# Example with security best practices
docker run -d \
  --name metanode-blockchain \
  --network metanode-net \
  --restart unless-stopped \
  --cpus 2 \
  --memory 4g \
  --read-only \
  --tmpfs /tmp \
  -v ~/.metanode/data/blockchain:/data:rw \
  metanode/blockchain:latest
```

## Running in Production

For production Docker deployments, consider:

1. **Docker Swarm**: For simple multi-host deployments
2. **External Database**: For high-volume data storage
3. **Reverse Proxy**: Using Nginx or Traefik for TLS and routing
4. **External Monitoring**: Prometheus and Grafana for metrics
5. **Log Aggregation**: Using Filebeat and ELK stack

## Troubleshooting

### Common Issues and Solutions

1. **Container exits immediately**:
   - Check logs: `docker logs metanode-blockchain`
   - Verify environment variables and volume mounts

2. **Network connectivity issues**:
   - Verify network: `docker network inspect metanode-net`
   - Check container networking: `docker exec metanode-blockchain ping metanode-validator`

3. **Storage issues**:
   - Check volume mounts: `docker inspect -f "{{ .Mounts }}" metanode-blockchain`
   - Verify permissions: `ls -la ~/.metanode/data`

## Next Steps

- Learn about [vPod Technology](04_vpod_technology.md) for container optimization
- Explore [Infrastructure Scaling](05_infrastructure_scaling.md) for handling increased load
- Implement [High Availability](06_high_availability.md) for production deployments
