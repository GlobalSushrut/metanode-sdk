# MetaNode SDK Installation & Usage Guide

This guide shows how to install the MetaNode SDK and connect to the public testnet infrastructure.

## Understanding the MetaNode Architecture

The MetaNode testnet provides the underlying blockchain and federated computing **infrastructure** that:
- Manages server and client nodes in the network
- Handles consensus, data storage, and validation
- Provides the foundation for federated applications

As a developer, you'll use the SDK to:
1. Deploy your own server and client nodes that connect to this infrastructure
2. Build and deploy applications that run on this connected network

## Installation

### Method 1: Install via PyPI (Recommended)

```bash
pip install metanode-sdk
```

### Method 2: Install from Source

```bash
git clone https://github.com/metanode/metanode-sdk.git
cd metanode-sdk
pip install -e .
```

## Quick Start: Connecting to the Network

### 1. Create a Wallet

```bash
metanode-wallet create
```

This will prompt you for a password and create a new wallet. The output will display your wallet address.

### 2. Get Tokens from Testnet Faucet

Visit the faucet to get test tokens for network interaction:

```
http://159.203.17.36/faucet
```

### 3. Deploy Your Own Server Node

To participate in the network as a server node:

```bash
metanode-cli node deploy --type server
```

This deploys a server node that connects to the testnet infrastructure and participates in the network.

### 4. Deploy Your Own Client Node

To participate in the network as a client node:

```bash
metanode-cli node deploy --type client
```

This deploys a client node that connects to the testnet infrastructure.

### 5. Create and Deploy Your Application

Create an application configuration:

```bash
# app-config.json
{
  "name": "my-federated-app",
  "algorithm": "federated-average",  # or "secure-aggregation"
  "resources": {
    "cpus": 1,
    "memory": "512Mi"
  },
  "code": {
    "main": "run_federated_app.py",
    "dependencies": ["numpy", "pandas"]
  }
}
```

Deploy your application to run on your nodes:

```bash
metanode-cli app deploy app-config.json
```

### 6. Monitor Your Application

```bash
metanode-cli app status <app_id>
```

## Advanced Configuration

Configure your connection to the testnet infrastructure:

```bash
# Set custom testnet endpoint
metanode config set-network --custom http://159.203.17.36/api

# Reset to default testnet
metanode config set-network --default
```

## Managing Your Nodes

```bash
# List your deployed nodes
metanode-cli node list

# Get node status
metanode-cli node status <node_id>

# Scale your server nodes
metanode-cli node scale <node_id> --replicas 3
```

## Troubleshooting

If you encounter any issues:

1. Check your connection to the testnet infrastructure:
   ```bash
   metanode-cli network status
   ```

2. Verify your nodes are properly connected:
   ```bash
   metanode-cli node list --status
   ```

3. Make sure you're using console mode:
   ```bash
   export CONSOLE_MODE=true
   ```

## Need Help?

Visit our testnet website at http://159.203.17.36 for more documentation and support resources.
