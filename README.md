# MetaNode SDK

## Blockchain & dApp Deployment Infrastructure

MetaNode SDK provides a complete blockchain-grade infrastructure for secure, lightweight, and highly scalable federated computing and dApp deployment. This next-generation SDK delivers Ethereum-grade security while surpassing traditional blockchain platforms with advanced features tailored for federated computing environments and automated decentralized application deployment.

## Features

- **Console-Based Workflows**: All operations are accessible through user-friendly CLI commands
- **Wallet Management**: Secure key generation, transaction signing, and token management
- **Mining Console**: Contribute compute resources and storage to earn tokens
- **Mainnet Deployment**: Deploy applications to the federated computing infrastructure
- **Cloud Management**: Deploy and scale MetaNode infrastructure in cloud environments
- **Zero-Knowledge Security**: Advanced privacy-preserving computation with proof verification
- **Federated Computing**: Distributed data processing with secure aggregation
- **dApp Integration**: Transform any application into a decentralized app with blockchain properties
- **Auto-Deployment**: Automatically deploy dApps to testnet or mainnet with blockchain properties
- **Docker.lock & K8s**: Seamless transformation to docker.lock format and Kubernetes blockchain clusters
- **vPod Container Integration**: Using the proven vPod approach that fixed the MetaNode demo CLI

## Installation

```bash
# Install from source
git clone https://github.com/metanode/metanode-sdk.git
cd metanode-sdk
pip install -e .
```

## Command Line Tools

The SDK provides several command-line tools:

- `metanode` - Main CLI interface for all MetaNode operations
- `metanode-cli` - Application deployment and management
- `metanode-wallet` - Wallet management and token operations
- `metanode-miner` - Resource contribution and mining operations
- `metanode-cloud` - Cloud infrastructure management
- `metanode-deploy` - Automatic dApp deployment to testnet/mainnet

## Quick Start

### Create a Wallet

```bash
metanode wallet create
```

### Start Mining

```bash
metanode mining
```

### Deploy an Application

```bash
# Create a deployment config file
metanode deploy config --name "MyApp" --version "1.0.0" > myapp.json

# Deploy the application
metanode deploy myapp.json
```

### Transform Any App into a dApp

```bash
# Transform and deploy to testnet (free)
metanode-deploy --app /path/to/app --testnet

# Transform and deploy to mainnet (requires rental tokens)
metanode-deploy --app /path/to/app --mainnet --wallet /path/to/wallet.json
```

### Use the Python SDK for dApp Integration

```python
# Simple dApp transformation
from metanode.dapp import make_dapp

# Transform any application into a dApp
result = make_dapp("/path/to/app", use_mainnet=False)
print(f"App transformed to dApp with blockchain properties: {result}")

# Create an immutable decentralized agent
from metanode.dapp import create_agent

agent = create_agent(use_mainnet=False)  # Connect to testnet
agent.execute_action("store_data", {"key": "value"}, critical=True)
```

### Check Mainnet Status

```bash
metanode mainnet-status
```

## Architecture

The MetaNode SDK consists of several core modules:

1. **Core**: Blockchain fundamentals, consensus algorithms, and chain validation
2. **Wallet**: Key management, transaction signing, and encrypted storage
3. **Mining**: Resource contribution, proof verification, and token rewards
4. **Cloud**: Infrastructure deployment, scaling, and mainnet management
5. **CLI**: Command-line tools for interacting with all components
6. **dApp**: Automatic transformation of any app to a decentralized application
7. **Docker/K8s**: Seamless integration with docker.lock format and Kubernetes blockchain clusters

## Example Applications

The SDK includes example applications that demonstrate how to use the various features:

- **Simple Application**: Basic federated computing with secure aggregation
- **Calculator App**: Demonstrates proof generation and verification
- **dApp Integration**: Example of transforming a standard app to a dApp with blockchain properties
- **Immutable Agent**: Example of deploying an agent with consensus validation and proofs

Run the example with:

```bash
cd examples/simple_application
python run_federated_app.py
```

## Documentation

Detailed documentation is available in the `docs` directory:

- [Getting Started](docs/getting-started.md)
- [SDK Reference](docs/sdk-reference.md)
- [Advanced Features](docs/advanced-features.md)

## Security

MetaNode provides Ethereum-grade security with advanced features:

- Zero-knowledge proofs for private computation
- Sharded computing for enhanced scalability
- Cross-zone validation for trust minimization
- Secure transaction signing and verification
- Encrypted key storage and management

## License

Proprietary License - All Rights Reserved. See [LICENSE](LICENSE) file for details.
