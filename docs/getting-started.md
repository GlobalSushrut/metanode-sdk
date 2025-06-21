# Getting Started with MetaNode SDK

This guide will help you get started with the MetaNode SDK, an Ethereum-grade blockchain infrastructure for federated computing.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Docker (for running certain components)
- Linux or macOS environment (Windows support via WSL)

## Installation

Install the MetaNode SDK using pip:

```bash
pip install metanode-sdk
```

Or install from source for the latest development version:

```bash
git clone https://github.com/metanode/metanode-sdk.git
cd metanode-sdk
pip install -e .
```

## Initial Setup

After installation, set up your MetaNode environment:

```bash
metanode setup
```

This command initializes the necessary directories and configurations.

## Creating a Wallet

Your first step should be to create a wallet for managing your MetaNode tokens:

```bash
metanode wallet create
```

You'll be prompted to create a password. Make sure to remember it, as you'll need it to access your wallet in the future.

## Contributing Resources (Mining)

To contribute computing resources to the network and earn tokens:

```bash
metanode-miner start --compute 1.0 --storage 10
```

This command starts the mining process with 1.0 compute units and 10GB of storage. You can adjust these values based on what you want to contribute.

To check your mining status:

```bash
metanode-miner stats
```

To stop mining:

```bash
metanode-miner stop
```

## Deploying Your First Application

### 1. Create a Deployment Configuration

Create a JSON configuration file for your application:

```json
{
  "name": "MyFirstApp",
  "version": "1.0.0",
  "description": "My first MetaNode application",
  "resources": {
    "compute": 1.0,
    "memory": "256Mi",
    "storage": "50Mi"
  },
  "federated": {
    "algorithm": "secure-aggregation",
    "min_peers": 3,
    "timeout": 60
  },
  "security": {
    "use_zk_proofs": true,
    "encrypt_data": true,
    "verify_computation": true
  },
  "runtime": {
    "image": "metanode/federated-py:1.0",
    "entrypoint": "python main.py",
    "environment": {
      "METANODE_ENV": "production",
      "LOG_LEVEL": "info"
    }
  }
}
```

Save this file as `myapp.json`.

### 2. Deploy the Application

```bash
metanode deploy myapp.json
```

### 3. Check Deployment Status

```bash
metanode status
```

To view details of a specific deployment:

```bash
metanode status <deployment_id>
```

## Working with Tokens

To check your wallet balance:

```bash
metanode wallet balance
```

To transfer tokens to another wallet:

```bash
metanode wallet transfer <recipient_wallet_id> <amount>
```

## Cloud Infrastructure

If you need to manage cloud infrastructure for MetaNode:

```bash
# Create a new cluster
metanode cloud create --name "my-cluster" --provider aws --region us-east-1 --nodes 3

# Deploy mainnet to the cluster
metanode cloud deploy-mainnet <cluster_id>
```

## Next Steps

- Explore the [SDK Reference](sdk-reference.md) for detailed API documentation
- Check out the [Advanced Features](advanced-features.md) guide for more complex scenarios
- See the [examples directory](../examples) for working code samples

## Troubleshooting

If you encounter any issues:

1. Ensure all components are running in console mode with no UI dependencies
2. Check that Docker containers are properly configured and accessible
3. Verify network connectivity for blockchain synchronization
4. Check the logs at `~/.metanode/logs` for detailed error information

For more help, visit the [MetaNode GitHub repository](https://github.com/metanode/metanode-sdk) or join our [community forum](https://forum.metanode.network).
