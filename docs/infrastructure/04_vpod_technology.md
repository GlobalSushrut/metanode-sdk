# vPod Technology

This document explains MetaNode's virtualized pod (vPod) technology, which provides optimized container environments for blockchain, validator, and agreement components.

## What Are vPods?

vPods (virtualized pods) are specialized container environments developed by MetaNode to efficiently run blockchain infrastructure components. They combine the benefits of containerization with optimized configurations for blockchain and distributed systems.

## Key Benefits

- **Performance Optimized**: Tuned specifically for blockchain workloads
- **Resource Efficient**: Minimized overhead compared to standard containers
- **Security Enhanced**: Hardened configurations with minimal attack surface
- **Pre-configured**: Ready-to-run with optimal settings for each component
- **Cross-compatible**: Works with both Docker and Kubernetes environments

## vPod Container Types

The MetaNode SDK includes several specialized vPod container types:

| vPod Type | Purpose | Base Image |
|-----------|---------|------------|
| Blockchain | Runs the core blockchain node | ethereum/client-go with MetaNode extensions |
| Validator | Manages transaction and agreement validation | MetaNode's custom validator image |
| Agreement | Handles agreement creation and management | Node.js-based agreement service |
| IPFS | Provides distributed file storage | IPFS daemon with MetaNode connectors |
| BFR | Blockchain Fast Relay - optimizes transaction routing | MetaNode's high-performance relay |

## Architecture

Each vPod consists of:

1. **Base Layer**: Minimal OS environment with essential dependencies
2. **Runtime Layer**: Component-specific runtimes (e.g., Geth for blockchain)
3. **MetaNode Layer**: MetaNode extensions and optimizations
4. **Configuration Layer**: Environment-specific configurations

```
┌───────────────────────────────────┐
│      Configuration Layer          │
│  (Environment & Component Config) │
├───────────────────────────────────┤
│        MetaNode Layer             │
│    (Extensions & Optimizations)   │
├───────────────────────────────────┤
│         Runtime Layer             │
│ (Geth, Validator, Agreement, etc) │
├───────────────────────────────────┤
│          Base Layer               │
│   (Minimal OS & Dependencies)     │
└───────────────────────────────────┘
```

## Using vPods with Docker

vPods can be deployed directly with Docker:

```bash
# Run a blockchain vPod
docker run -d \
  --name metanode-blockchain-vpod \
  --network metanode-net \
  -e METANODE_ROLE=blockchain \
  -e METANODE_NETWORK=testnet \
  -v ~/.metanode/data/blockchain:/data \
  -p 8545:8545 \
  metanode/blockchain:latest
```

## Using vPods with Kubernetes

vPods can also be deployed in Kubernetes:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metanode-blockchain-vpod
spec:
  replicas: 1
  selector:
    matchLabels:
      app: metanode
      component: blockchain
  template:
    metadata:
      labels:
        app: metanode
        component: blockchain
    spec:
      containers:
      - name: blockchain
        image: metanode/blockchain:latest
        env:
        - name: METANODE_ROLE
          value: "blockchain"
        - name: METANODE_NETWORK
          value: "testnet"
        volumeMounts:
        - name: blockchain-data
          mountPath: /data
```

## SDK Integration

The SDK automatically manages vPod containers:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Deploy vPod containers
vpod_deployment = sdk.deploy_vpod_containers(
    app_name="my-app", 
    vpod_types=["blockchain", "validator", "agreement"]
)
```

## vPod Configuration

Each vPod type has specific configuration parameters:

### Blockchain vPod

```bash
docker run -d --name metanode-blockchain \
  -e METANODE_BLOCKCHAIN_TYPE=geth \
  -e METANODE_CHAIN_ID=11155111 \
  -e METANODE_RPC_APIS="eth,net,web3,debug" \
  -e METANODE_MINING_ENABLED=true \
  -e METANODE_BLOCK_TIME=5 \
  metanode/blockchain:latest
```

### Validator vPod

```bash
docker run -d --name metanode-validator \
  -e METANODE_VALIDATOR_MODE=full \
  -e METANODE_BLOCKCHAIN_URL="http://metanode-blockchain:8545" \
  -e METANODE_VALIDATOR_PORT=7545 \
  -e METANODE_CONSENSUS_ENABLED=true \
  metanode/validator:latest
```

### Agreement vPod

```bash
docker run -d --name metanode-agreement \
  -e METANODE_BLOCKCHAIN_URL="http://metanode-blockchain:8545" \
  -e METANODE_VALIDATOR_URL="http://metanode-validator:7545" \
  -e METANODE_AGREEMENT_PORT=6545 \
  -e METANODE_AGREEMENT_STORAGE="/data" \
  metanode/agreement:latest
```

## Performance Tuning

vPods include performance optimizations for blockchain workloads:

1. **Memory Management**: Optimized garbage collection and memory allocation
2. **Disk I/O**: Efficient storage patterns for blockchain data
3. **Network Tuning**: Optimized parameters for P2P communication
4. **CPU Utilization**: Balanced workloads across available cores

Example of performance tuning with environment variables:

```bash
docker run -d --name metanode-blockchain \
  -e METANODE_CACHE_SIZE=2048 \
  -e METANODE_GC_MODE=incremental \
  -e METANODE_BLOCK_CACHE=1024 \
  -e METANODE_TXN_POOL_SIZE=5000 \
  -e METANODE_STATE_CACHE=500 \
  metanode/blockchain:latest
```

## Inter-vPod Communication

vPods communicate with each other through a secure internal network:

```
┌────────────────┐      ┌────────────────┐
│                │      │                │
│  Blockchain    │◄────►│   Validator    │
│     vPod       │      │     vPod       │
│                │      │                │
└────────┬───────┘      └────────┬───────┘
         │                       │
         │                       │
         ▼                       ▼
┌────────────────┐      ┌────────────────┐
│                │      │                │
│   Agreement    │◄────►│     IPFS       │
│     vPod       │      │     vPod       │
│                │      │                │
└────────────────┘      └────────────────┘
```

## Security Features

vPods include security enhancements:

1. **Minimal Base Images**: Reduced attack surface
2. **Read-Only Filesystems**: When possible for immutability
3. **Capability Restrictions**: Principle of least privilege
4. **Network Isolation**: Restricted communication paths
5. **Secret Management**: Secure credential handling

## Monitoring and Logging

vPods expose metrics and logs in standardized formats:

```bash
# Example: Setup monitoring for vPod
docker run -d \
  --name cadvisor \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  google/cadvisor:latest
```

## Building Custom vPods

You can customize vPods for specific requirements:

```Dockerfile
# Example: Custom blockchain vPod
FROM metanode/blockchain:latest

# Add custom scripts
COPY ./custom-scripts /opt/custom-scripts

# Add custom configuration
COPY ./custom-config.toml /config/custom-config.toml

# Set environment variables
ENV METANODE_CUSTOM_CONFIG=/config/custom-config.toml
ENV METANODE_STARTUP_SCRIPT=/opt/custom-scripts/startup.sh

# Expose additional ports
EXPOSE 9545

# Set custom entrypoint if needed
ENTRYPOINT ["/opt/custom-scripts/entrypoint.sh"]
```

## Troubleshooting vPod Issues

### Common Issues and Solutions

1. **vPod fails to start**:
   - Check logs: `docker logs metanode-blockchain-vpod`
   - Verify environment configuration
   - Ensure volume paths exist with correct permissions

2. **vPod performance issues**:
   - Check resource utilization: `docker stats metanode-blockchain-vpod`
   - Adjust memory and CPU allocations
   - Review performance tuning parameters

3. **Communication problems between vPods**:
   - Verify network configuration: `docker network inspect metanode-net`
   - Check service discovery is working
   - Validate URL configurations between components

## Next Steps

- Explore [Infrastructure Scaling](05_infrastructure_scaling.md) for handling increased load
- Implement [High Availability](06_high_availability.md) for production deployments
