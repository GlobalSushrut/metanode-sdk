# MetaNode Public Testnet Deployment

This directory contains all necessary scripts and configuration files to deploy a public-facing MetaNode testnet on your DigitalOcean droplet (159.203.17.36). The deployment is designed to be accessible to anyone, allowing them to download the SDK and interact with your testnet.

## Deployment Contents

1. **Kubernetes Configuration Files**:
   - `namespace.yaml` - Creates the MetaNode namespace
   - `configmap.yaml` - Environment variables and configuration
   - `storage.yaml` - Persistent storage for blockchain and IPFS data
   - `ipfs.yaml` - IPFS node deployment
   - `blockchain-core.yaml` - Core blockchain nodes
   - `validator.yaml` - Validator nodes for consensus
   - `api.yaml` - API server with console-mode support
   - `sdk-server.yaml` - SDK download server
   - `ingress.yaml` - Kubernetes ingress configuration
   - `setup_public_access.yaml` - Public gateway configuration

2. **Docker Build Files**:
   - `/docker/core/Dockerfile` - Core node container
   - `/docker/validator/Dockerfile` - Validator node container
   - `/docker/api/Dockerfile` - API server with USE_EXISTING_VPOD support

3. **Deployment Scripts**:
   - `deploy_public_testnet.sh` - Complete deployment script
   - `prepare_sdk_package.sh` - SDK packaging script

4. **Public Interface Files**:
   - `public-html/index.html` - Website for SDK users
   - `install_instructions.md` - Detailed installation guide

## Key Features

- **Console-Only Operation**: All components run in console mode without UI dependencies
- **Existing Docker vPod Containers**: The API server uses existing Docker vPod containers
- **Public Access**: Anyone can download the SDK and interact with your testnet
- **Example Applications**: Includes federated averaging and secure aggregation examples
- **User-Friendly Installation**: Simple pip installation that automatically connects to your testnet
- **Kubernetes Management**: Easy scaling and maintenance of testnet infrastructure

## Important Implementation Note

This deployment implements the critical fix that was previously made to the MetaNode demo CLI:
- **USE_EXISTING_VPOD=true**: API server configured to use existing Docker vPod containers
- **CONSOLE_MODE=true**: All components configured to run in console-only mode
- **Both Algorithms Supported**: Works with both federated-average and secure-aggregation algorithms

## Deployment Instructions

1. **Transfer deployment files to your droplet**:
   ```bash
   scp -r /home/umesh/Videos/vKuber9/metanode-sdk/k8s-deployment root@159.203.17.36:/home/ubuntu/metanode-k8s
   scp -r /home/umesh/Videos/vKuber9/metanode-sdk root@159.203.17.36:/home/ubuntu/
   ```

2. **Connect to your droplet and run the deployment script**:
   ```bash
   ssh root@159.203.17.36
   chmod +x /home/ubuntu/metanode-k8s/deploy_public_testnet.sh
   /home/ubuntu/metanode-k8s/deploy_public_testnet.sh
   ```

3. **Verify the deployment**:
   ```bash
   microk8s kubectl -n metanode get all
   curl http://localhost:30080
   ```

## Public Access

After successful deployment, the following endpoints will be available:

- **Main Website**: http://159.203.17.36/
- **SDK Download**: http://159.203.17.36/download/
- **API Access**: http://159.203.17.36/api/
- **IPFS Gateway**: http://159.203.17.36/ipfs/
- **Token Faucet**: http://159.203.17.36/faucet/
- **Block Explorer**: http://159.203.17.36/explorer/

## User Installation

Anyone can install the SDK and connect to your testnet with:

```bash
pip install metanode-sdk
```

The SDK is pre-configured to connect to your testnet at 159.203.17.36.

## Secure Kubernetes Integration

The MetaNode SDK now includes a comprehensive Kubernetes integration module (`k8s_manager.py`) that manages secure deployment of testnet and application nodes with the following features:

### Cryptographic Security

- **Node Key Generation**: Creates unique 256-bit cryptographic keys for node authentication
- **Secure Node Registration**: Registers Kubernetes nodes with the testnet using cryptographic verification
- **Label-Based Node Selection**: Marks nodes as testnet or application nodes in Kubernetes

### Deployment Capabilities

- **Testnet Node Deployment**: Securely deploys testnet nodes with persistent storage and network isolation
- **Application Node Deployment**: Deploys application nodes that securely connect to the testnet
- **Synchronization Setup**: Configures testnet synchronization between nodes via Kubernetes Services

### CLI Integration

Use the CLI to manage your Kubernetes deployments:

```bash
# Generate a new cryptographic key for node authentication
metanode admin k8s create-key

# Register a Kubernetes node with the testnet
metanode admin k8s register-node --node-name worker1 --key-id key123 --is-testnet true

# Deploy a testnet node
metanode admin k8s deploy-testnet --node-id node123 --node-name worker1

# Setup testnet synchronization
metanode admin k8s setup-sync
```

## Deployment Template Details

### Testnet Node Template (`testnet.yaml`)

This template deploys a complete testnet node configuration with:
- Namespace isolation
- Role-based access control
- ConfigMap for configuration
- StatefulSet for testnet nodes
- Persistent volume claims
- Service configuration
- Network policies

### Application Node Template (`app.yaml`)

This template deploys an application node that connects to the testnet with:
- Namespace configuration
- Service account for the application
- ConfigMap for application settings
- Deployment with node selectors
- Persistent storage configuration
- Service exposure
- Network policies for secure communication
