# Enhancing Testnet Decentralization

This document explains how to contribute to the MetaNode testnet's decentralization by setting up and deploying node clusters using the SDK.

## Overview

The MetaNode testnet operates at `http://159.203.17.36:8545` (RPC) and `ws://159.203.17.36:8546` (WebSocket). While the testnet is functional with just these endpoints, its decentralization, reliability, and performance can be enhanced by running additional nodes that participate in the network.

When you deploy node clusters, you are contributing to:
- Network resilience and fault tolerance
- Transaction validation capacity
- Block verification redundancy
- Overall decentralization of the network

## Node Cluster Types

The MetaNode SDK supports creating several types of node contributions:

| Type | Description | Resource Requirements |
|------|-------------|----------------------|
| **Validator** | Participates in transaction validation and block verification | Medium-High |
| **Peer** | Stores and syncs blockchain data | Medium |
| **Light** | Connects to the network with minimal resources | Low |

## Setting Up Node Clusters

### Using the SDK

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Create a node cluster with default settings
cluster_id = sdk.create_node_cluster(
    name="my-validator-cluster",
    node_type="validator",
    node_count=1
)

# Check cluster status
status = sdk.check_cluster_status(cluster_id)
print(f"Cluster status: {status}")
```

### Using the CLI

```bash
# Create a validator node
metanode-cli cluster create --name my-validator --type validator --resources medium

# Create a peer node with custom resources
metanode-cli cluster create --name my-peer --type peer --cpu 2 --memory 4G --disk 100G
```

### Using the Enhanced Decentralization Script

The SDK includes a shell script that automates the process of creating and configuring a node cluster:

```bash
# Run the script directly
./enhance_testnet_decentralization.sh

# Or with custom parameters
./enhance_testnet_decentralization.sh --name "custom-node" --type validator --resources high
```

## Node Configuration Options

When creating a node cluster, you can configure:

```json
{
  "node": {
    "identity": "metanode-contributor-[unique-id]",
    "role": "validator_contributor",
    "capabilities": ["sync", "store", "validate"],
    "peer_count_target": 25,
    "peer_count_max": 50
  },
  "network": {
    "testnet_rpc": "http://159.203.17.36:8545",
    "testnet_ws": "ws://159.203.17.36:8546",
    "bootnode": "enode://[node-key]@159.203.17.36:30303"
  },
  "consensus": {
    "contribute": true,
    "vote_enabled": true,
    "blocks_to_finality": 12,
    "min_peers_for_quorum": 3
  },
  "storage": {
    "max_block_history": 10000,
    "prune_threshold_gb": 20
  }
}
```

## Chainlink.lock Verification

When you deploy a node, the SDK generates a chainlink.lock file that contains verification information:

```json
{
  "provider": "chainlink",
  "network": "testnet",
  "timestamp": 1624552286,
  "rpc_endpoint": "http://159.203.17.36:8545",
  "ws_endpoint": "ws://159.203.17.36:8546",
  "chain_id": 11155111,
  "decentralization_contribution": {
    "node_id": "metanode-contributor-a8b7c6d5",
    "peer_enabled": true,
    "validator_enabled": true,
    "resource_contribution": {
      "max_storage_gb": 50,
      "max_bandwidth_mbps": 100,
      "cpu_cores": 2
    }
  },
  "verifier_nodes": ["0x8456782345dcBA12345"],
  "verified": true,
  "proof_of_execution": {
    "hash": "0xabcdef1234567890",
    "timestamp": 1624552286,
    "block_number": 12345678,
    "validator": "0x9876543210fedcba"
  }
}
```

This file serves as proof of your contribution to the network's decentralization.

## Monitoring Your Node Contribution

After deploying a node cluster, you can monitor its status:

```bash
# Using the CLI
metanode-cli cluster status my-validator-cluster

# Using Docker commands (if deployed via Docker)
docker logs metanode-testnet-connector

# Via the SDK
sdk.get_cluster_stats(cluster_id)
```

## Requirements for Running a Node

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| CPU         | 2 cores | 4+ cores    |
| Memory      | 4GB     | 8GB+        |
| Storage     | 20GB    | 100GB+      |
| Bandwidth   | 10 Mbps | 100+ Mbps   |
| Uptime      | >80%    | >95%        |

## Benefits of Running a Node

1. **Network Contribution**: Help build a more robust testnet for all MetaNode applications
2. **Development Testing**: Test your applications against a node you control
3. **Learning**: Gain deeper understanding of blockchain infrastructure
4. **Preparation**: Prepare for mainnet participation in the future

## Next Steps

- Set up [Verification Proofs](03_verification_proofs.md)
- Configure [Application-Specific Testnet Settings](04_testnet_config.md)
- Learn about [Testnet-to-Production Migration](05_testnet_to_prod.md)
