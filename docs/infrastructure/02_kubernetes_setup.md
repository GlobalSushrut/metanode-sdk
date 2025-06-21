# Kubernetes Infrastructure Setup

This document provides detailed instructions for setting up MetaNode infrastructure components using Kubernetes orchestration.

## Prerequisites

- Kubernetes cluster (v1.18+)
- kubectl CLI installed and configured
- Helm (v3.0+) for package management
- MetaNode SDK installed (`pip install metanode-sdk`)
- At least 8GB RAM and 4 CPU cores available

## Overview

The MetaNode SDK leverages Kubernetes to orchestrate the deployment and management of blockchain nodes, validators, agreement systems, and IPFS storage. This orchestration provides:

- High availability and fault tolerance
- Automatic scaling and load balancing
- Resource management and optimization
- Simplified deployment and updates

## Setup Options

### Option 1: Automated Setup with SDK

The simplest approach is using the SDK's automated Kubernetes setup:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Deploy full infrastructure on Kubernetes
deployment = sdk.deploy_kubernetes_infrastructure(
    app_name="my-app",
    components=["blockchain", "validator", "agreement", "ipfs"],
    namespace="metanode",
    replicas={
        "blockchain": 1,
        "validator": 3,
        "agreement": 1,
        "ipfs": 1
    }
)

# Check deployment status
status = sdk.check_infrastructure_status("my-app")
print(f"Infrastructure status: {status}")
```

### Option 2: CLI-based Setup

For those who prefer the command line:

```bash
# Create namespace for MetaNode components
kubectl create namespace metanode

# Deploy using the CLI
metanode-cli k8s deploy-infrastructure \
  --app my-app \
  --namespace metanode \
  --components blockchain,validator,agreement,ipfs \
  --replicas blockchain=1,validator=3,agreement=1,ipfs=1
```

### Option 3: Manual Setup with Manifests

For complete control, you can generate and apply Kubernetes manifests:

```bash
# Generate Kubernetes manifests
metanode-cli k8s generate-manifests \
  --output-dir ./k8s-manifests \
  --app my-app

# Apply the manifests
kubectl apply -f ./k8s-manifests/namespace.yaml
kubectl apply -f ./k8s-manifests/blockchain/
kubectl apply -f ./k8s-manifests/validator/
kubectl apply -f ./k8s-manifests/agreement/
kubectl apply -f ./k8s-manifests/ipfs/
```

## Kubernetes Resource Configuration

### Resource Requirements by Component

```yaml
# Example resource configurations
resources:
  blockchain:
    requests:
      memory: "4Gi"
      cpu: "2"
    limits:
      memory: "6Gi"
      cpu: "3"
  validator:
    requests:
      memory: "2Gi"
      cpu: "1"
    limits:
      memory: "3Gi"
      cpu: "2"
  agreement:
    requests:
      memory: "1Gi"
      cpu: "0.5"
    limits:
      memory: "2Gi"
      cpu: "1"
  ipfs:
    requests:
      memory: "2Gi"
      cpu: "1"
    limits:
      memory: "4Gi"
      cpu: "2"
```

### Persistence Configuration

```yaml
# Example persistent volume configuration
volumeClaimTemplates:
- metadata:
    name: blockchain-data
  spec:
    accessModes: [ "ReadWriteOnce" ]
    resources:
      requests:
        storage: 50Gi
```

## Networking Setup

MetaNode components need to communicate with each other and be accessible as required:

```yaml
# Example service configuration
apiVersion: v1
kind: Service
metadata:
  name: metanode-blockchain
  namespace: metanode
spec:
  selector:
    app: metanode
    component: blockchain
  ports:
  - name: rpc
    port: 8545
    targetPort: 8545
    protocol: TCP
  - name: ws
    port: 8546
    targetPort: 8546
    protocol: TCP
  type: ClusterIP  # Use LoadBalancer for external access
```

## Security Configuration

### RBAC Setup

```yaml
# Example RBAC configuration
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: metanode
  name: metanode-manager
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["pods", "deployments", "services", "configmaps", "secrets", "jobs"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

### Secret Management

```bash
# Create secrets for sensitive configuration
kubectl create secret generic metanode-keys \
  --from-file=node-key=./keys/node_key \
  --from-file=validator-key=./keys/validator_key \
  --namespace metanode
```

## High Availability Setup

For production deployments, configure high availability:

```python
# Deploy with high availability settings
sdk.deploy_kubernetes_infrastructure(
    app_name="my-app",
    high_availability=True,  # Enables HA configuration
    replicas={
        "blockchain": 3,  # Multiple blockchain nodes
        "validator": 5,   # Validator quorum
        "agreement": 2,   # Redundant agreement systems
        "ipfs": 3         # Distributed IPFS cluster
    },
    pod_anti_affinity=True,  # Ensures pods run on different nodes
    node_selector={
        "failure-domain.beta.kubernetes.io/zone": ["us-east-1a", "us-east-1b", "us-east-1c"]
    }
)
```

## Monitoring Integration

Configure Prometheus and Grafana for monitoring:

```bash
# Deploy monitoring stack
metanode-cli k8s deploy-monitoring \
  --namespace metanode-monitoring \
  --components prometheus,grafana,alertmanager

# Import pre-configured dashboards
metanode-cli k8s import-dashboards
```

## Configuration Management

### ConfigMaps for Configuration

```yaml
# Example ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: metanode-blockchain-config
  namespace: metanode
data:
  blockchain.json: |
    {
      "network": "testnet",
      "consensus": {
        "algorithm": "poa",
        "block_time": 5,
        "validators": 3
      },
      "rpc": {
        "apis": ["eth", "net", "web3", "debug"]
      }
    }
```

### Environment Variables

```yaml
# Example environment variables
env:
  - name: METANODE_NETWORK
    value: "testnet"
  - name: METANODE_LOG_LEVEL
    value: "info"
  - name: METANODE_RPC_HOST
    value: "0.0.0.0"
  - name: METANODE_RPC_PORT
    value: "8545"
  - name: METANODE_VALIDATOR_COUNT
    value: "3"
```

## Validation and Testing

After deployment, verify the infrastructure is working correctly:

```bash
# Check all resources
kubectl get all -n metanode

# Test blockchain connectivity
metanode-cli testnet test --kubernetes

# View logs from blockchain node
kubectl logs deployment/metanode-blockchain -n metanode

# Run a comprehensive validation test
metanode-cli infra validate-kubernetes --all-components
```

## Troubleshooting

### Common Issues and Solutions

1. **Pods not starting**:
   - Check resources: `kubectl describe pod <pod-name> -n metanode`
   - Verify persistent volumes: `kubectl get pvc -n metanode`

2. **Network connectivity issues**:
   - Check services: `kubectl get svc -n metanode`
   - Test connectivity: `kubectl exec -it <pod-name> -n metanode -- curl localhost:8545`

3. **Performance issues**:
   - Check resource utilization: `kubectl top pod -n metanode`
   - Consider scaling resources: `kubectl scale deployment/metanode-blockchain --replicas=3 -n metanode`

## Next Steps

- Configure [Docker-based Deployment](03_docker_deployment.md) as an alternative
- Learn about [vPod Technology](04_vpod_technology.md) for container optimization
- Explore [Infrastructure Scaling](05_infrastructure_scaling.md) for handling load
- Implement [High Availability](06_high_availability.md) for production deployments
