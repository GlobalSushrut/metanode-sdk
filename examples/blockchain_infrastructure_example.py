#!/usr/bin/env python3
"""
MetaNode SDK Blockchain Infrastructure Complete Example
=====================================================

This example demonstrates:
1. Setting up the complete infrastructure with Kubernetes and vPods
2. Configuring all layers: blockchain, validator, consensus, and storage
3. Deploying a full self-contained blockchain environment
4. Connecting to external networks (testnet)
5. Handling distributed storage and transactions

Usage:
    python blockchain_infrastructure_example.py
"""

import os
import sys
import time
import logging
import json
from pathlib import Path

# Add the parent directory to the path so we can import the metanode package
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import MetaNode SDK components
from metanode.blockchain import (
    initialize_blockchain, 
    connect_to_testnet,
    validate_agreement,
    store_data,
    retrieve_data,
    create_transaction,
    sign_transaction,
    submit_transaction
)
from metanode.blockchain.infrastructure import (
    InfrastructureConfig,
    setup_complete_infrastructure
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode-example")

def main():
    print("=" * 70)
    print("MetaNode SDK - Complete Blockchain Infrastructure Example")
    print("=" * 70)
    print("\nThis example demonstrates the full MetaNode blockchain stack with:")
    print("- Automatic Kubernetes cluster setup")
    print("- vPods blockchain and storage layers")
    print("- Multi-layer consensus with ZK proofs")
    print("- Agreement validation and runtime VM\n")
    
    # Step 1: Setup complete infrastructure
    print("\n[1/6] Setting up complete blockchain infrastructure...")
    infra_config = InfrastructureConfig(
        use_minikube=True,  # Use minikube for local development
        node_count=3,        # 3 blockchain nodes
        storage_nodes=3,     # 3 storage nodes
        validator_nodes=2    # 2 validator nodes
    )
    
    # This creates the complete infrastructure:
    # - Installs/configures Kubernetes
    # - Sets up vPods distribution
    # - Creates blockchain, consensus, validator, and storage layers
    result = setup_complete_infrastructure()
    print(f"Infrastructure setup result: {result['status']}")
    
    if result['status'] != "success":
        print(f"Failed to set up infrastructure: {result.get('error', 'Unknown error')}")
        return
    
    # Step 2: Initialize blockchain
    print("\n[2/6] Initializing blockchain...")
    blockchain = initialize_blockchain()
    print(f"Blockchain initialized on {blockchain['network']} with {blockchain['node_count']} nodes")
    print(f"RPC endpoint: {blockchain['rpc_endpoint']}")
    
    # Step 3: Connect to testnet
    print("\n[3/6] Connecting to testnet...")
    # Use optional custom testnet server if needed (159.203.17.36)
    testnet = connect_to_testnet(
        connector_nodes=2,
        testnet_server="159.203.17.36"  # Using the specified testnet server
    )
    print(f"Connected to testnet with {testnet['node_count']} connector nodes")
    print(f"Connection ID: {testnet['connection_id']}")
    
    # Step 4: Store data in distributed storage
    print("\n[4/6] Storing data in distributed storage...")
    data = {
        "sensor_id": "iot-sensor-1",
        "temperature": 24.5,
        "humidity": 65,
        "timestamp": time.time(),
        "location": "Building A, Floor 3"
    }
    
    storage_result = store_data(data, metadata={"source": "example", "priority": "high"})
    print(f"Data stored with hash: {storage_result['content_hash']}")
    print(f"Storage ID: {storage_result['storage_id']}")
    
    # Step 5: Validate contract agreement
    print("\n[5/6] Validating contract agreement...")
    agreement_id = "metanode-testnet-agreement-1"
    validation = validate_agreement(
        agreement_id=agreement_id,
        action="data_storage",
        metadata={"content_hash": storage_result['content_hash']}
    )
    print(f"Agreement validation result: {'Valid' if validation['validated'] else 'Invalid'}")
    print(f"Consensus level: {validation['consensus_level'] * 100:.0f}%")
    print(f"Runtime proof: {validation['runtime_proof']}")
    
    # Step 6: Create and submit blockchain transaction
    print("\n[6/6] Creating and submitting blockchain transaction...")
    transaction = create_transaction(
        operation="store_data_hash",
        data={
            "content_hash": storage_result['content_hash'],
            "storage_id": storage_result['storage_id'],
            "timestamp": time.time()
        },
        agreement_id=agreement_id
    )
    print(f"Transaction created: {transaction['tx_id']}")
    
    signed_tx = sign_transaction(transaction)
    print(f"Transaction signed at: {signed_tx['signed_at']}")
    
    receipt = submit_transaction(signed_tx, wait_for_receipt=True)
    print(f"Transaction submitted with hash: {receipt['tx_hash']}")
    print(f"Status: {receipt['status']}")
    
    if receipt['status'] == 'confirmed':
        print(f"Confirmed in block: {receipt['block_number']}")
    
    # Summary
    print("\n" + "=" * 70)
    print("MetaNode Blockchain Infrastructure Deployment Complete!")
    print("=" * 70)
    print("\nYou now have:")
    print("✓ Complete Kubernetes cluster with ZK blockchain")
    print("✓ Testnet connection established")
    print("✓ Distributed storage layer with light DB")
    print("✓ Multi-layer validation (consensus, ledger, validator)")
    print("✓ Runtime VM for smart contract execution")
    print("\nSummary of components:")
    print(f"- Blockchain nodes: {blockchain['node_count']}")
    print(f"- Storage nodes: {infra_config.storage_nodes}")
    print(f"- Validator nodes: {infra_config.validator_nodes}")
    print(f"- RPC endpoint: {blockchain['rpc_endpoint']}")
    print(f"- Runtime proof: {validation['runtime_proof']}")
    
    print("\nDemo data:")
    print(f"- Content hash: {storage_result['content_hash']}")
    print(f"- Transaction hash: {receipt['tx_hash']}")
    print(f"- Block number: {receipt.get('block_number', 'pending')}")

if __name__ == "__main__":
    main()
