# MetaNode SDK: Testnet Module Reference

This document provides a comprehensive API reference for the Testnet connectivity module within the MetaNode SDK.

## Table of Contents

- [Overview](#overview)
- [Core Classes](#core-classes)
- [Testnet Connection](#testnet-connection)
- [Node Cluster Management](#node-cluster-management)
- [Verification Proofs](#verification-proofs)
- [Transaction Management](#transaction-management)
- [Validator Operations](#validator-operations)
- [CLI Integration](#cli-integration)
- [Error Handling](#error-handling)

## Overview

The Testnet module provides tools for connecting to the MetaNode testnet, deploying node clusters, enhancing testnet decentralization, and interacting with the blockchain infrastructure. The testnet runs at endpoint 159.203.17.36:8545 (RPC) and 159.203.17.36:8546 (WebSocket).

## Core Classes

### TestnetConnection

The primary class for testnet connectivity.

```python
from metanode.blockchain import TestnetConnection

# Create a connection to the testnet
testnet = TestnetConnection()

# Access connection properties
print(f"RPC URL: {testnet.rpc_url}")  # http://159.203.17.36:8545
print(f"WS URL: {testnet.ws_url}")    # ws://159.203.17.36:8546

# Or access through the SDK
from metanode.full_sdk import MetaNodeSDK
sdk = MetaNodeSDK()
testnet = sdk.connect_to_testnet()
```

### NodeManager

Class for managing node clusters that contribute to the testnet.

```python
from metanode.blockchain import NodeManager

# Create a node manager
node_manager = NodeManager()

# Or access through the SDK
from metanode.full_sdk import MetaNodeSDK
sdk = MetaNodeSDK()
node_manager = sdk.node_manager
```

## Testnet Connection

### connect_to_testnet

Establishes a connection to the MetaNode testnet.

```python
from metanode.full_sdk import MetaNodeSDK

sdk = MetaNodeSDK()

# Connect with default settings
testnet = sdk.connect_to_testnet()

# Connect with custom settings
testnet = sdk.connect_to_testnet(
    rpc_url="http://159.203.17.36:8545",  # Default testnet endpoint
    ws_url="ws://159.203.17.36:8546",     # Default WebSocket endpoint
    network_id="metanode-testnet",
    chain_id=1337,
    timeout_seconds=30,
    max_retries=3,
    retry_delay_seconds=2
)

print(f"Connected to testnet at {testnet.rpc_url}")
```

### test_rpc_connection

Tests the connection to the testnet RPC endpoint.

```python
# Test connection
connection_test = sdk.test_rpc_connection()

if connection_test["connected"]:
    print("Successfully connected to testnet!")
    print(f"Current block number: {connection_test['block_number']}")
    print(f"Network ID: {connection_test['network_id']}")
    print(f"Chain ID: {connection_test['chain_id']}")
else:
    print(f"Connection failed: {connection_test['error']}")
```

### get_testnet_info

Retrieves information about the testnet.

```python
# Get testnet information
info = sdk.get_testnet_info()

print(f"Network name: {info['network_name']}")
print(f"Network ID: {info['network_id']}")
print(f"Chain ID: {info['chain_id']}")
print(f"Current block: {info['block_number']}")
print(f"Consensus algorithm: {info['consensus_algorithm']}")
print(f"Active validators: {info['active_validator_count']}")
print(f"API version: {info['api_version']}")
```

### reconnect_testnet

Reestablishes a connection to the testnet.

```python
# Reconnect to testnet
reconnect_result = sdk.reconnect_testnet()

if reconnect_result["reconnected"]:
    print("Successfully reconnected to testnet")
else:
    print(f"Reconnection failed: {reconnect_result['error']}")
```

## Node Cluster Management

### generate_node_identities

Generates identities for nodes that will participate in the testnet.

```python
# Generate node identities
node_identities = sdk.generate_node_identities(
    count=3,                      # Required: Number of nodes to generate
    roles=["validator", "peer"],  # Required: Roles for the nodes
    key_type="secp256k1",         # Optional: Type of cryptographic keys
    naming_prefix="node"          # Optional: Prefix for node names
)

# Display generated identities
for i, node in enumerate(node_identities):
    print(f"Node {i+1}:")
    print(f"  Address: {node['address']}")
    print(f"  Role: {node['role']}")
    print(f"  Public key: {node['public_key']}")
```

### create_node_configs

Creates configuration files for the nodes.

```python
# Create node configuration files
node_configs = sdk.create_node_configs(
    node_identities=node_identities,       # Required: Node identities
    network_id="metanode-testnet",         # Required: Network ID
    config_options={                       # Optional: Configuration options
        "peer_discovery": True,
        "sync_mode": "full",
        "bootnodes": ["enode://abc123@159.203.17.36:30303"],
        "rpc_enabled": True,
        "ws_enabled": True
    }
)

# Save configuration files
for i, config in enumerate(node_configs):
    with open(f"./node_{i}_config.json", "w") as f:
        import json
        json.dump(config, f, indent=2)
```

### deploy_node_cluster

Deploys a cluster of nodes to enhance testnet decentralization.

```python
# Deploy a node cluster
cluster = sdk.deploy_node_cluster(
    cluster_name="my-validator-cluster",  # Required: Name for the cluster
    node_configs=node_configs,            # Required: Node configurations
    deployment_options={                  # Optional: Deployment options
        "deployment_method": "docker",    # Options: docker, kubernetes
        "resource_limits": {
            "cpu_per_node": 2,
            "memory_per_node": "4Gi"
        },
        "connection_endpoints": ["http://159.203.17.36:8545"],
        "data_persistence": True,
        "monitoring_enabled": True
    }
)

print(f"Node cluster deployed: {cluster['cluster_id']}")
print(f"Access URL: {cluster['access_url']}")
print(f"Nodes deployed: {len(cluster['nodes'])}")
```

### check_node_cluster_status

Checks the status of a deployed node cluster.

```python
# Check node cluster status
cluster_status = sdk.check_node_cluster_status(
    cluster_id=cluster["cluster_id"]     # Required: Cluster ID
)

print(f"Cluster status: {cluster_status['status']}")
print(f"Active nodes: {cluster_status['active_node_count']}/{cluster_status['total_node_count']}")
print(f"Block height: {cluster_status['block_height']}")
print(f"Syncing: {cluster_status['syncing']}")
print(f"Peers: {cluster_status['peer_count']}")

# Get detailed node information
for node in cluster_status["nodes"]:
    print(f"\nNode {node['id']}:")
    print(f"  Status: {node['status']}")
    print(f"  Role: {node['role']}")
    print(f"  Block height: {node['block_height']}")
    print(f"  Peer count: {node['peer_count']}")
    print(f"  CPU usage: {node['resources']['cpu_usage']}%")
    print(f"  Memory usage: {node['resources']['memory_usage']}%")
```

## Verification Proofs

### generate_verification_proof

Generates a chainlink.lock verification proof for a node cluster or agreement.

```python
# Generate verification proof for a node cluster
cluster_proof = sdk.generate_verification_proof(
    verification_type="chainlink.lock",    # Required: Type of verification
    target_id=cluster["cluster_id"],       # Required: Target ID (cluster or agreement)
    target_type="node_cluster",            # Required: Target type
    proof_parameters={                     # Optional: Proof parameters
        "include_node_identities": True,
        "include_network_config": True,
        "hash_algorithm": "keccak256"
    }
)

print(f"Verification proof generated: {cluster_proof['proof_id']}")
print(f"Block number: {cluster_proof['block_number']}")
print(f"Transaction hash: {cluster_proof['transaction_hash']}")
print(f"IPFS CID: {cluster_proof['ipfs_cid']}")
```

### verify_chainlink_proof

Verifies a chainlink.lock proof.

```python
# Verify a chainlink.lock proof
verification = sdk.verify_chainlink_proof(
    proof_id=cluster_proof["proof_id"],    # Required: Proof ID
    verification_options={                 # Optional: Verification options
        "check_blockchain_record": True,
        "check_ipfs_record": True
    }
)

if verification["valid"]:
    print("Proof verification successful!")
    print(f"Blockchain transaction: {verification['blockchain_tx']}")
    print(f"IPFS record: {verification['ipfs_cid']}")
    print(f"Recorded at block: {verification['block_number']}")
    print(f"Timestamp: {verification['timestamp']}")
else:
    print(f"Proof verification failed: {verification['reason']}")
```

## Transaction Management

### create_transaction

Creates a blockchain transaction.

```python
from metanode.blockchain import Transaction

# Create transaction through the SDK
transaction = sdk.create_transaction(
    to_address="0x456def...",             # Required: Recipient address
    value=0,                              # Optional: Value in wei
    data=b"0x...",                        # Optional: Transaction data
    gas_limit=100000,                     # Optional: Gas limit
    gas_price=None,                       # Optional: Gas price (auto if None)
    nonce=None                            # Optional: Nonce (auto if None)
)

print(f"Transaction created: {transaction['tx_hash']}")
```

### sign_transaction

Signs a blockchain transaction.

```python
# Sign transaction
signed_tx = sdk.sign_transaction(
    transaction_id=transaction["tx_id"],  # Required: Transaction ID
    wallet_name="my-metanode-wallet"      # Optional: Wallet to use (default if None)
)

print(f"Transaction signed: {signed_tx['signed']}")
print(f"Signed transaction data: {signed_tx['raw_tx']}")
```

### send_transaction

Sends a signed transaction to the blockchain.

```python
# Send transaction
tx_receipt = sdk.send_transaction(
    transaction_id=transaction["tx_id"]   # Required: Transaction ID
)

print(f"Transaction sent: {tx_receipt['tx_hash']}")
print(f"Block number: {tx_receipt['block_number']}")
print(f"Status: {tx_receipt['status']}")
```

### get_transaction_status

Checks the status of a transaction.

```python
# Check transaction status
tx_status = sdk.get_transaction_status(
    transaction_hash=tx_receipt["tx_hash"]  # Required: Transaction hash
)

print(f"Transaction status: {tx_status['status']}")
if tx_status["confirmed"]:
    print(f"Confirmations: {tx_status['confirmations']}")
    print(f"Block number: {tx_status['block_number']}")
```

## Validator Operations

### get_validator_list

Retrieves the list of active validators on the testnet.

```python
# Get validators
validators = sdk.get_validator_list()

print(f"Total validators: {len(validators)}")
for validator in validators:
    print(f"Validator: {validator['address']}")
    print(f"  Status: {validator['status']}")
    print(f"  Blocks produced: {validator['blocks_produced']}")
    print(f"  Last active: {validator['last_active']}")
```

### check_validator_status

Checks the status of a specific validator.

```python
# Check validator status
validator_status = sdk.check_validator_status(
    validator_address="0x789ghi..."       # Required: Validator address
)

print(f"Validator status: {validator_status['status']}")
print(f"Currently active: {validator_status['active']}")
print(f"Last block produced: {validator_status['last_block']}")
print(f"Performance score: {validator_status['performance_score']}/100")
```

### register_validator

Registers a new validator on the testnet.

```python
# Register a validator
registration = sdk.register_validator(
    node_identity=node_identities[0],     # Required: Node identity
    stake_amount=1000000000000000000,     # Optional: Stake amount in wei
    metadata={                            # Optional: Validator metadata
        "organization": "Example Org",
        "region": "us-east",
        "contact": "validator@example.com"
    }
)

print(f"Validator registration: {registration['status']}")
print(f"Transaction hash: {registration['tx_hash']}")
```

## CLI Integration

The SDK integrates with the MetaNode CLI for testnet operations.

### Command Line Usage

```bash
# Connect to testnet
metanode-cli testnet connect

# Check testnet status
metanode-cli testnet status

# Get testnet information
metanode-cli testnet info

# Create node cluster
metanode-cli node create-cluster \
  --name my-validator-cluster \
  --nodes 3 \
  --roles validator,peer \
  --deployment-method docker \
  --connect-to http://159.203.17.36:8545

# Generate verification proof
metanode-cli node generate-proof \
  --cluster-id <cluster_id> \
  --type chainlink.lock
  
# Check node status
metanode-cli node status --cluster-id <cluster_id>
```

### CLI Wrapper Functions

```python
# Execute CLI commands from the SDK
cli_result = sdk.execute_cli_command(
    command="testnet",
    subcommand="connect",
    arguments={"rpc-url": "http://159.203.17.36:8545"}
)

print(f"CLI command executed: {cli_result['success']}")
print(f"Output: {cli_result['output']}")
```

## Error Handling

The SDK uses a consistent error handling pattern for testnet operations:

```python
from metanode.exceptions import (
    TestnetConnectionError,
    NodeDeploymentError,
    BlockchainTransactionError,
    ValidatorError
)

try:
    # SDK operations
    testnet = sdk.connect_to_testnet()
except TestnetConnectionError as e:
    print(f"Connection error: {e.message}")
    print(f"RPC URL: {e.rpc_url}")
except NodeDeploymentError as e:
    print(f"Node deployment error: {e.message}")
    print(f"Failed nodes: {e.failed_nodes}")
except BlockchainTransactionError as e:
    print(f"Transaction error: {e.message}")
    print(f"Transaction hash: {e.tx_hash}")
except ValidatorError as e:
    print(f"Validator error: {e.message}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Conclusion

This reference covers the core functionality of the MetaNode SDK Testnet module. For practical examples of testnet connectivity and node cluster deployment, refer to these tutorials:

- [Complete Workflow](/docs/tutorials/01_complete_workflow.md)
- [Testnet Connection](/docs/tutorials/02_testnet_connection.md)
- [Production Migration](/docs/tutorials/03_production_migration.md)

The Testnet module provides all the necessary tools for connecting to the MetaNode testnet at 159.203.17.36:8545, deploying node clusters to enhance testnet decentralization, and generating cryptographic verification proofs.
