# MetaNode SDK Reference

This document provides a comprehensive reference for the MetaNode SDK v1.0.0-beta components.

## Core Modules

### metanode.cli

The main command-line interface for MetaNode operations.

#### Commands

| Command | Description |
|---------|-------------|
| `deploy <config_path>` | Deploy an application to MetaNode network |
| `status [deployment_id]` | Check status of deployments |
| `mainnet-status` | View mainnet blockchain status |
| `version` | Display SDK version information |

#### Example

```python
# Use in Python code
from metanode.cli import deploy_application

result = deploy_application("/path/to/config.json")
print(f"Deployment ID: {result['id']}")
```

### metanode.wallet

Secure wallet management for the MetaNode blockchain.

#### CLI Commands

| Command | Description |
|---------|-------------|
| `create` | Create a new wallet |
| `list` | List all available wallets |
| `load <wallet_id>` | Load a wallet for operations |
| `balance` | Check balance of active wallet |
| `transfer <recipient> <amount>` | Transfer tokens to another wallet |

#### Python API

```python
from metanode.wallet.core import WalletManager

# Create wallet manager
wallet_manager = WalletManager()

# Create new wallet
wallet_info = wallet_manager.create_wallet("your_password")
print(f"Wallet ID: {wallet_info['wallet_id']}")

# Load wallet
success = wallet_manager.load_wallet("wallet_id", "your_password")
if success:
    # Check balance
    balance = wallet_manager.get_balance()
    print(f"Balance: {balance}")
    
    # Transfer tokens
    tx = wallet_manager.transfer("recipient_wallet_id", 10.0)
    print(f"Transaction ID: {tx['tx_id']}")
```

### metanode.mining

Contribute resources to the network and earn tokens.

#### CLI Commands

| Command | Description |
|---------|-------------|
| `start [--compute] [--storage]` | Start mining with specified resources |
| `stop` | Stop mining |
| `stats` | Get mining statistics |
| `mine` | Manually mine a block |
| `verify` | Manually verify a zero-knowledge proof |

#### Python API

```python
from metanode.mining.console import MiningConsole

# Create mining console
console = MiningConsole()

# Start mining
result = console.start_mining(compute_power=1.0, storage_gb=10.0)
print(f"Mining started: {result['status']}")

# Get stats
stats = console.get_mining_stats()
print(f"Blocks mined: {stats['blocks_mined']}")
print(f"Rewards earned: {stats['rewards_earned']}")

# Stop mining
console.stop_mining()
```

### metanode.cloud

Deploy and manage cloud infrastructure for MetaNode.

#### CLI Commands

| Command | Description |
|---------|-------------|
| `create` | Create a new cluster |
| `list` | List all clusters |
| `status <cluster_id>` | Check status of a cluster |
| `scale <cluster_id> --nodes <count>` | Scale cluster to specified node count |
| `delete <cluster_id>` | Delete a cluster |
| `deploy-mainnet <cluster_id>` | Deploy MetaNode mainnet to cluster |
| `mainnet-status <cluster_id>` | Check mainnet status on cluster |

#### Python API

```python
from metanode.cloud.manager import CloudManager

# Create cloud manager
manager = CloudManager()

# Create cluster
cluster = manager.create_cluster(
    name="my-cluster", 
    cloud_provider="aws", 
    region="us-east-1",
    node_count=3, 
    node_type="m5.large"
)
print(f"Cluster ID: {cluster['id']}")

# Deploy mainnet
mainnet = manager.deploy_mainnet(cluster['id'])
print(f"Mainnet ID: {mainnet['id']}")
```

## Core Blockchain Components

### Consensus Algorithm

MetaNode uses a hybrid consensus algorithm combining Proof of Contribution with Byzantine Fault Tolerance:

- **Proof of Contribution (PoC)**: Nodes earn reputation and rewards based on contributed resources and validated proofs
- **Byzantine Fault Tolerance (BFT)**: Ensures agreement among validators even with potential malicious actors
- **Zero-Knowledge Integration**: Validators verify computation correctness without seeing the actual data

```python
from metanode.core.blockchain import BlockchainNode

# Initialize a blockchain node
node = BlockchainNode(node_type="validator")

# Join the network
node.join_network(bootstrap_peers=["peer1.metanode.net", "peer2.metanode.net"])

# Start consensus participation
node.start_consensus()
```

### Zero-Knowledge Proofs

MetaNode implements advanced zero-knowledge proofs for privacy-preserving computation:

- **Circuit Generation**: Creates zk-SNARK circuits for verifiable computation
- **Proof Generation**: Generates proofs of computation correctness
- **Verification**: Validates computation integrity without revealing data

```python
from metanode.core.zk import ProofGenerator, Verifier

# Generate a proof
generator = ProofGenerator()
proof = generator.create_proof(
    function="add",
    inputs=[5, 10],
    output=15
)

# Verify the proof
verifier = Verifier()
is_valid = verifier.verify_proof(proof)
print(f"Proof valid: {is_valid}")
```

## Data Structures

### Block Structure

```json
{
  "header": {
    "block_number": 1234567,
    "timestamp": 1623451789,
    "previous_hash": "0x8f72d4e470142ab23...",
    "merkle_root": "0x7ab38c9e21f0d467...",
    "difficulty": 456789,
    "nonce": 98765
  },
  "transactions": [
    {
      "tx_id": "0xabcdef1234567890...",
      "from": "wallet_sender123",
      "to": "wallet_recipient456",
      "amount": 10.5,
      "timestamp": 1623451700,
      "signature": "0x9876543210abcdef..."
    }
  ],
  "proofs": [
    {
      "proof_id": "zk_proof_123456",
      "verifier": "wallet_validator789",
      "timestamp": 1623451750,
      "hash": "0x123456789abcdef..."
    }
  ]
}
```

### Wallet Structure

```json
{
  "wallet_id": "wallet_abc123",
  "public_key": "mpk_xyz987...",
  "encrypted_private_key": "encrypted_msk_...",
  "created_at": 1623450000,
  "balance": 100.0,
  "transaction_history": [
    {
      "tx_id": "tx_12345",
      "sender": "wallet_abc123",
      "recipient": "wallet_def456",
      "amount": 5.0,
      "timestamp": 1623450100
    }
  ]
}
```

## Configuration Files

### Application Deployment

```json
{
  "name": "MyApp",
  "version": "1.0.0",
  "description": "My MetaNode application",
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

### Cloud Cluster

```json
{
  "id": "cluster_abcdef12",
  "name": "production-cluster",
  "cloud_provider": "aws",
  "region": "us-east-1",
  "node_count": 5,
  "node_type": "m5.large",
  "status": "running",
  "created_at": "2023-06-12T10:30:00Z",
  "ipfs_gateway": "https://ipfs-cluster_abcdef12.metanode.network",
  "api_endpoint": "https://api-cluster_abcdef12.metanode.network"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `METANODE_CONFIG_DIR` | Path to config directory | `~/.metanode` |
| `METANODE_LOG_LEVEL` | Logging level | `info` |
| `METANODE_API_URL` | URL for MetaNode API | `https://api.metanode.network` |
| `METANODE_WALLET_PASSWORD` | Wallet password (not recommended) | None |

## Error Handling

The SDK provides standard error types for handling various failure cases:

```python
from metanode.core.exceptions import (
    MetaNodeError,
    WalletError,
    DeploymentError,
    MiningError,
    NetworkError
)

try:
    # Some operation
    pass
except WalletError as e:
    print(f"Wallet error: {e}")
except DeploymentError as e:
    print(f"Deployment error: {e}")
except MetaNodeError as e:
    print(f"General error: {e}")
```

## Directory Structure

```
~/.metanode/
├── wallets/             # Wallet files
├── apps/                # Application configs
├── deployments/         # Deployment records
├── mining/              # Mining data
│   ├── resources.json   # Resource tracking
│   └── proofs/          # Generated proofs
├── cloud/               # Cloud configurations
│   ├── clusters.json    # Cluster records
│   └── templates/       # Deployment templates
├── chain/               # Blockchain data
│   ├── blocks/          # Block data
│   └── state/           # Chain state
└── logs/                # Log files
```
