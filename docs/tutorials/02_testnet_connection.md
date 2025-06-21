# MetaNode Testnet Connection Guide

This tutorial provides detailed instructions on connecting to the MetaNode testnet and enhancing testnet decentralization through node clusters.

## Table of Contents

1. [Introduction to MetaNode Testnet](#1-introduction-to-metanode-testnet)
2. [Prerequisites](#2-prerequisites)
3. [Connecting to the Testnet](#3-connecting-to-the-testnet)
4. [Testing Connectivity](#4-testing-connectivity)
5. [Enhancing Testnet Decentralization](#5-enhancing-testnet-decentralization)
6. [Generating Verification Proofs](#6-generating-verification-proofs)
7. [Monitoring Node Status](#7-monitoring-node-status)
8. [Troubleshooting](#8-troubleshooting)
9. [Next Steps](#9-next-steps)

## 1. Introduction to MetaNode Testnet

The MetaNode testnet provides a sandbox environment for testing MetaNode applications, agreements, and infrastructure. The testnet includes:

- Blockchain RPC endpoint
- Validator network
- Agreement infrastructure
- IPFS integration
- BFR (Blockchain File Registry)

## 2. Prerequisites

Before connecting to the testnet, ensure you have the following:

- MetaNode SDK installed: `pip install metanode-sdk`
- MetaNode CLI installed: `pip install metanode-cli`
- A MetaNode wallet (create one if needed)
- Network access to the testnet endpoints

## 3. Connecting to the Testnet

### Using the SDK

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Configure testnet connection
testnet = sdk.connect_to_testnet(
    rpc_url="http://159.203.17.36:8545",  # Main testnet endpoint
    ws_url="ws://159.203.17.36:8546",     # WebSocket endpoint
    network_id="metanode-testnet",
    chain_id=1337
)

# Verify connection
if testnet.is_connected():
    print(f"Successfully connected to testnet at {testnet.rpc_url}")
    print(f"Current block: {testnet.get_block_number()}")
    print(f"Network ID: {testnet.network_id}")
else:
    print("Failed to connect to testnet")
```

### Using the CLI

```bash
# Connect to testnet
metanode-cli testnet connect --rpc-url http://159.203.17.36:8545 --ws-url ws://159.203.17.36:8546

# Verify connection
metanode-cli testnet status
```

## 4. Testing Connectivity

### Basic Connection Tests

```python
# Test RPC connection
connection_test = sdk.test_rpc_connection()

if connection_test["connected"]:
    print("RPC connection successful!")
    print(f"Block number: {connection_test['block_number']}")
    print(f"Network ID: {connection_test['network_id']}")
    print(f"Chain ID: {connection_test['chain_id']}")
    print(f"API version: {connection_test['api_version']}")
else:
    print(f"Connection failed: {connection_test['error']}")
```

### Advanced API Tests

```python
# Test agreement API functionality
api_test = sdk.test_agreement_api()
print(f"Agreement API status: {api_test['status']}")

# Test validator connectivity
validator_test = sdk.test_validator_connection()
print(f"Validator status: {validator_test['status']}")

# Test IPFS connectivity
ipfs_test = sdk.test_ipfs_connection()
print(f"IPFS status: {ipfs_test['status']}")
```

### Using the CLI for Testing

```bash
# Run comprehensive test suite
metanode-cli testnet test-all

# Test specific components
metanode-cli testnet test --component blockchain
metanode-cli testnet test --component validator
metanode-cli testnet test --component agreement
metanode-cli testnet test --component ipfs
```

## 5. Enhancing Testnet Decentralization

The MetaNode testnet can be enhanced by deploying additional node clusters that contribute to the network.

### Generating Node Identities

```python
# Generate node identities
node_identities = sdk.generate_node_identities(
    count=3,  # Create 3 nodes
    roles=["validator", "peer"],  # Roles for the nodes
    key_type="secp256k1"  # Cryptographic key type
)

# Save node identities for future use
sdk.save_node_identities(
    node_identities=node_identities,
    file_path="./node_identities.json",
    encrypt=True,
    password="secure_password"
)

print(f"Generated {len(node_identities)} node identities")
```

### Creating Node Configuration Files

```python
# Create node configuration files
node_configs = sdk.create_node_configs(
    node_identities=node_identities,
    network_id="metanode-testnet",
    config_options={
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
        f.write(config)
        
print(f"Created {len(node_configs)} configuration files")
```

### Deploying Node Cluster

```python
# Deploy a node cluster
cluster = sdk.deploy_node_cluster(
    cluster_name="my-validator-cluster",
    node_configs=node_configs,
    deployment_options={
        "deployment_method": "docker",  # Options: docker, kubernetes
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
```

### Using CLI for Node Cluster Creation

```bash
# Create and deploy node cluster using the CLI
metanode-cli node create-cluster \
  --name my-validator-cluster \
  --nodes 3 \
  --roles validator,peer \
  --deployment-method docker \
  --connect-to http://159.203.17.36:8545 \
  --monitoring true
```

## 6. Generating Verification Proofs

Verification proofs (chainlink.lock) ensure the integrity of your node cluster.

```python
# Generate a verification proof for the cluster
verification_proof = sdk.generate_verification_proof(
    verification_type="chainlink.lock",
    target_id=cluster["cluster_id"],
    proof_parameters={
        "include_node_identities": True,
        "include_network_config": True,
        "hash_algorithm": "keccak256"
    }
)

print(f"Verification proof generated: {verification_proof['proof_id']}")
print(f"Block number: {verification_proof['block_number']}")
print(f"Transaction hash: {verification_proof['transaction_hash']}")
print(f"Verification URL: {verification_proof['verification_url']}")
```

### Verifying a Proof

```python
# Verify a chainlink.lock proof
verification = sdk.verify_chainlink_proof(
    proof_id=verification_proof["proof_id"],
    verification_options={
        "check_blockchain_record": True,
        "check_ipfs_record": True
    }
)

if verification["valid"]:
    print("Proof verification successful!")
    print(f"Blockchain transaction: {verification['blockchain_tx']}")
    print(f"IPFS record: {verification['ipfs_cid']}")
else:
    print(f"Proof verification failed: {verification['reason']}")
```

## 7. Monitoring Node Status

### Checking Node Health

```python
# Check status of your node cluster
cluster_status = sdk.check_node_cluster_status(cluster["cluster_id"])

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

### Using CLI for Monitoring

```bash
# Check node cluster status
metanode-cli node status --cluster-id <cluster_id>

# Get detailed node metrics
metanode-cli node metrics --cluster-id <cluster_id> --format table

# Check node logs
metanode-cli node logs --cluster-id <cluster_id> --node-id <node_id> --lines 50
```

## 8. Troubleshooting

### Common Connection Issues

If you encounter connection issues, try the following:

```python
# Reset connection
sdk.reset_testnet_connection()

# Reconnect with different parameters
testnet = sdk.connect_to_testnet(
    rpc_url="http://159.203.17.36:8545",
    timeout_seconds=30,
    max_retries=5,
    retry_delay_seconds=2
)

# Check for specific error conditions
diagnostic = sdk.run_testnet_diagnostics()
for issue in diagnostic["issues"]:
    print(f"Issue: {issue['description']}")
    print(f"Recommended action: {issue['recommendation']}")
```

### Node Cluster Issues

```python
# Restart a node in the cluster
sdk.restart_node(
    cluster_id=cluster["cluster_id"],
    node_id="node-1"
)

# Repair a node cluster
repair_result = sdk.repair_node_cluster(
    cluster_id=cluster["cluster_id"],
    repair_options={
        "resync_nodes": True,
        "reset_peer_discovery": True,
        "update_bootnode_list": True
    }
)
print(f"Repair status: {repair_result['status']}")
```

### CLI Troubleshooting Commands

```bash
# Diagnose connection issues
metanode-cli testnet diagnose

# Repair node cluster
metanode-cli node repair --cluster-id <cluster_id>

# Reset and reconnect to testnet
metanode-cli testnet reconnect --hard-reset
```

## 9. Next Steps

After successfully connecting to the testnet and deploying a node cluster, you can:

1. Create and deploy agreements on the testnet
2. Test agreement validation and verification
3. Monitor your node cluster performance
4. Contribute to testnet decentralization

For more information on MetaNode agreements, see the [Agreement Overview](/docs/agreements/01_agreement_overview.md) documentation.

## Conclusion

This guide demonstrates how to connect to the MetaNode testnet and enhance its decentralization through node clusters. By following these steps, you can set up a robust testing environment for MetaNode applications and contribute to the network's infrastructure.

Remember that the testnet is a controlled environment designed for testing purposes. For production deployments, you'll need to follow the migration guidelines in the [Migration to Production](/docs/tutorials/03_production_migration.md) document.
