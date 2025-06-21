# MetaNode Infrastructure Overview

This document provides an overview of the MetaNode SDK infrastructure components that enable decentralized application deployment with blockchain integration.

## Infrastructure Architecture

The MetaNode SDK deploys a multi-layered infrastructure stack to support decentralized applications with full blockchain capabilities:

```
┌─────────────────────────────────┐
│      Application Layer          │
├─────────────────────────────────┤
│     Agreement Layer             │
├─────────────────────────────────┤
│     Blockchain Layer            │
│  ┌─────────┐ ┌──────────────┐   │
│  │ Ledger  │ │  Validators  │   │
│  └─────────┘ └──────────────┘   │
├─────────────────────────────────┤
│     Storage & Consensus Layer   │
├─────────────────────────────────┤
│     Infrastructure Platform     │
│  (Kubernetes, Docker, vPods)    │
└─────────────────────────────────┘
```

## Key Components

### vPod Containers

The core of MetaNode infrastructure is the virtualized pod (vPod) technology, which allows running containerized blockchain nodes, validators, and agreement systems:

- **Blockchain vPods**: Run Ethereum-compatible blockchain nodes 
- **Validator vPods**: Handle agreement validation and consensus
- **Storage vPods**: Provide decentralized storage capabilities
- **IPFS vPods**: Enable distributed file storage and retrieval

### Kubernetes Integration

MetaNode infrastructure utilizes Kubernetes for orchestrating the vPod containers:

```python
# From infrastructure.py
def deploy_kubernetes_infrastructure(app_name, config):
    """Deploy full blockchain infrastructure with Kubernetes"""
    k8s_manager = K8sManager()
    
    # Deploy blockchain components
    blockchain_deployment = k8s_manager.deploy_component("blockchain", app_name)
    
    # Deploy validator nodes
    validator_deployment = k8s_manager.deploy_component("validator", app_name)
    
    # Deploy agreement system
    agreement_deployment = k8s_manager.deploy_component("agreement", app_name)
    
    # Return deployment status
    return {
        "blockchain": blockchain_deployment,
        "validator": validator_deployment,
        "agreement": agreement_deployment
    }
```

### Docker-based Deployment

For environments without Kubernetes, MetaNode deploys using Docker containers:

```bash
# Docker deployment for full blockchain stack
docker run -d \
  --name metanode-blockchain \
  --network metanode-net \
  -e METANODE_ROLE=blockchain \
  -v ~/.metanode/data:/data \
  -p 8545:8545 \
  metanode/blockchain:latest
```

## Connecting to Existing Infrastructure

### Testnet Connection

Applications can connect to the existing testnet infrastructure:

```python
from metanode.full_sdk import MetaNodeSDK

# Connect to testnet infrastructure
sdk = MetaNodeSDK()
connection = sdk.connect_to_testnet()

# Check infrastructure status
status = sdk.check_infrastructure_status()
print(f"Blockchain status: {status['blockchain']}")
print(f"Validator status: {status['validator']}")
```

### Setting Up Local Development Infrastructure

For local development, the SDK can deploy a lightweight infrastructure:

```bash
# Using the CLI
metanode-cli infra setup --local --components blockchain,validator,agreement

# Or using the setup script
./setup_local_infrastructure.sh
```

## Resource Requirements

| Component | CPU | Memory | Storage | Network |
|-----------|-----|--------|---------|---------|
| Blockchain Node | 2-4 cores | 4-8 GB | 50GB+ | 10Mbps+ |
| Validator | 1-2 cores | 2-4 GB | 10GB+ | 5Mbps+ |
| Agreement System | 1 core | 2 GB | 5GB | 5Mbps+ |
| IPFS Node | 1-2 cores | 2-4 GB | 20GB+ | 10Mbps+ |

## Infrastructure Management

### Deployment

```python
# Deploy full infrastructure
sdk.deploy_infrastructure(
    app_name="my-app",
    components=["blockchain", "validator", "agreement", "ipfs"],
    resources="medium"  # Options: low, medium, high, custom
)
```

### Scaling

```python
# Scale specific components
sdk.scale_infrastructure(
    app_name="my-app",
    component="blockchain",
    replicas=3,
    resources={
        "cpu": 4,
        "memory": "8Gi"
    }
)
```

### Monitoring

```python
# Get infrastructure status
status = sdk.get_infrastructure_status("my-app")

# Monitor resources
metrics = sdk.get_infrastructure_metrics(
    app_name="my-app",
    metrics=["cpu", "memory", "disk", "network"],
    duration="1h"
)
```

## Multi-Layer Security

The infrastructure implements security measures at multiple layers:

1. **Network Security**: Isolated container networks with controlled access
2. **Blockchain Security**: Consensus-based validation and verification
3. **Data Security**: Encrypted storage and secure key management
4. **Access Security**: Role-based access control (RBAC) for infrastructure management

## Infrastructure Configurations

Configuration templates for different deployment scenarios:

```yaml
# Development environment
environment: development
resources:
  blockchain:
    replicas: 1
    cpu: 1
    memory: 2Gi
  validator:
    replicas: 1
    cpu: 1
    memory: 1Gi

# Production environment
environment: production
resources:
  blockchain:
    replicas: 3
    cpu: 4
    memory: 8Gi
  validator:
    replicas: 5
    cpu: 2
    memory: 4Gi
```

## Next Steps

- Set up [Kubernetes Infrastructure](02_kubernetes_setup.md)
- Configure [Docker-based Deployment](03_docker_deployment.md)
- Learn about [vPod Technology](04_vpod_technology.md)
- Explore [Infrastructure Scaling](05_infrastructure_scaling.md)
- Implement [High Availability](06_high_availability.md)
