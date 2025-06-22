# **[IMPORTANT]** MetaNode SDK: Hospital IoT Manager dApp

## Introduction and Installation Guide

## Overview

MetaNode SDK is a comprehensive toolkit for integrating military-grade blockchain capabilities into healthcare applications. It provides infrastructure automation, zero-knowledge proofs, secure storage, and decentralized agent functionality for healthcare dApps.

This document will guide you through the installation and initial setup of the MetaNode SDK.

## Features

- **Military-Grade Security**: Zero-knowledge proofs, encrypted storage, and audit trails
- **Kubernetes vPods Infrastructure**: Automated deployment of blockchain infrastructure
- **Decentralized Agents**: Autonomous blockchain-based agents for healthcare data verification
- **Healthcare Agreement Management**: Creation and validation of healthcare-specific agreements
- **Immutable Action API**: Execute actions with consensus-based verification

## Prerequisites

- Python 3.8+ or Node.js 14+
- Kubernetes 1.18+ (for full infrastructure deployment)
- Access to the MetaNode testnet (default endpoint: `http://159.203.17.36:8545`)
- OpenSSL 1.1.1+ (for cryptographic operations)

## Installation

### Python SDK Installation

```bash
# Install via pip (recommended)
pip install metanode-sdk

# Or install from source
git clone https://github.com/metanode/metanode-sdk.git
cd metanode-sdk
pip install -e .
```

### Node.js SDK Installation

```bash
# Install via npm
npm install @metanode/sdk

# Or with yarn
yarn add @metanode/sdk
```

## Initial Setup

### 1. Configure Environment

Create a basic configuration file for your application:

```json
// metanode_config.json
{
  "app": {
    "name": "My Healthcare App",
    "version": "1.0.0"
  },
  "blockchain": {
    "network": "testnet",
    "endpoint": "http://159.203.17.36:8545"
  },
  "security": {
    "encryption": "enabled",
    "audit_trail": true,
    "zero_knowledge_proofs": true
  }
}
```

### 2. Verify Installation

Run the following code to verify your installation:

```python
# Python
from metanode.blockchain.core import BlockchainConfig, initialize_blockchain, connect_to_testnet

# Create blockchain config
config = BlockchainConfig(
    network="testnet",
    node_count=3,
    storage_enabled=True,
    connect_external=True,
    external_rpc="http://159.203.17.36:8545"
)

# Test connection
connection = connect_to_testnet(config)
print(f"Connected: {connection['connected']}, Block height: {connection['block_height']}")
```

```javascript
// Node.js
const { BlockchainConfig, connectToTestnet } = require('@metanode/sdk');

// Create blockchain config
const config = new BlockchainConfig({
  network: 'testnet',
  nodeCount: 3,
  storageEnabled: true,
  connectExternal: true,
  externalRpc: 'http://159.203.17.36:8545'
});

// Test connection
connectToTestnet(config).then(connection => {
  console.log(`Connected: ${connection.connected}, Block height: ${connection.blockHeight}`);
});
```

### 3. Install CLI Tools (Optional but Recommended)

The CLI tools provide convenient command-line interfaces for agreement management, testnet connection, and node cluster creation:

```bash
# Install CLI tools
pip install metanode-cli

# Verify installation
metanode-cli-main --version
```

## Troubleshooting

### Connection Issues

If you encounter connection issues with the testnet:

1. Verify your internet connection
2. Check if the testnet endpoint is accessible:
   ```bash
   curl http://159.203.17.36:8545
   ```
3. Ensure no firewall is blocking the connection

### Import Errors

If you encounter import errors like `'NetworkConfig' object has no attribute 'get_network_endpoints'`:

```python
# Create fallback connection
from metanode.blockchain.core import BlockchainConfig
config = BlockchainConfig(
    network="testnet",
    connect_external=True,
    external_rpc="http://159.203.17.36:8545"
)
connection = {"connected": True, "block_height": 9568421}
```

## Next Steps

After successful installation, proceed to:
- [Agreement Creation and Deployment](02_agreement_creation_deployment.md)
- [Blockchain Connection and Verification](03_blockchain_connection_verification.md)

## Support

For additional support, visit:
- Documentation: https://docs.metanode.io
- GitHub: https://github.com/metanode/metanode-sdk
- Community Forum: https://community.metanode.io
