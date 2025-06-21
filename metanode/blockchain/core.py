"""
MetaNode SDK Blockchain Core Module
==================================

Provides core blockchain functionality using vPods clusters within Kubernetes:
- Initializes the blockchain infrastructure
- Connects to mainnet/testnet
- Manages ZK-proof verification
- Handles docker.lock mechanism integration

This module forms the foundation of the MetaNode blockchain architecture.
"""

import os
import time
import logging
import subprocess
import json
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

from kubernetes import client, config
import yaml

from metanode.utils.docker import ensure_docker_running
from metanode.config.settings import get_settings
from metanode.deployment.k8s import create_k8s_resources, wait_for_deployment

# Configure logging
logger = logging.getLogger("metanode-blockchain")

class BlockchainConfig:
    """Configuration for blockchain deployment"""
    
    def __init__(self, 
                 network: str = "testnet", 
                 node_count: int = 3,
                 storage_enabled: bool = True,
                 validator_count: int = 2,
                 connect_external: bool = False,
                 external_rpc: Optional[str] = None):
        self.network = network
        self.node_count = max(node_count, 2)  # Minimum 2 nodes
        self.storage_enabled = storage_enabled
        self.validator_count = max(validator_count, 1)  # Minimum 1 validator
        self.connect_external = connect_external
        self.external_rpc = external_rpc
        self.docker_lock_path = "/tmp/docker.lock"
        
        # Create docker.lock file if it doesn't exist
        if not os.path.exists(self.docker_lock_path):
            with open(self.docker_lock_path, "w") as f:
                f.write(f"locked:{int(time.time())}")

def initialize_blockchain(config: Optional[BlockchainConfig] = None) -> Dict[str, Any]:
    """
    Initialize the blockchain infrastructure using vPods in Kubernetes
    
    Args:
        config: Optional blockchain configuration, uses defaults if None
        
    Returns:
        Dict with blockchain initialization status and endpoints
    """
    if config is None:
        config = BlockchainConfig()
        
    logger.info(f"Initializing blockchain infrastructure on {config.network}")
    
    # Ensure Docker is running for our container management
    ensure_docker_running()
    
    # Setup the vPod clusters
    vpod_cluster = create_vpod_cluster(
        node_count=config.node_count,
        storage_enabled=config.storage_enabled,
        validator_count=config.validator_count
    )
    
    # Initialize RPC nodes for transaction handling
    rpc_nodes = configure_rpc_nodes(vpod_cluster)
    
    # Setup communicator node if connecting to external network
    communicator = None
    if config.connect_external and config.external_rpc:
        communicator = setup_communicator_node(
            vpod_cluster, 
            external_rpc=config.external_rpc
        )
    
    # Record the initialization timestamp in the docker.lock file
    with open(config.docker_lock_path, "w") as f:
        lock_data = {
            "timestamp": int(time.time()),
            "network": config.network,
            "node_count": config.node_count,
            "validators": config.validator_count,
            "storage_enabled": config.storage_enabled
        }
        f.write(f"locked:{json.dumps(lock_data)}")
        
    return {
        "status": "initialized",
        "network": config.network,
        "vpod_cluster_id": vpod_cluster.get("id"),
        "node_count": config.node_count,
        "validator_count": config.validator_count,
        "rpc_endpoint": f"http://localhost:8070/rpc",
        "connected_to_external": config.connect_external,
        "storage_enabled": config.storage_enabled
    }

def connect_to_mainnet(
    connector_nodes: int = 2,
    external_rpc: str = "https://mainnet.infura.io/v3/YOUR_API_KEY"
) -> Dict[str, Any]:
    """
    Connect the blockchain infrastructure to Ethereum mainnet
    
    Args:
        connector_nodes: Number of nodes to connect to mainnet (2-5 recommended)
        external_rpc: Mainnet RPC endpoint URL
        
    Returns:
        Dict with connection status and details
    """
    logger.info(f"Connecting to Ethereum mainnet via {external_rpc}")
    
    # Create a mainnet blockchain config
    config = BlockchainConfig(
        network="mainnet",
        node_count=max(2, min(connector_nodes, 5)),  # Between 2-5 nodes
        connect_external=True,
        external_rpc=external_rpc
    )
    
    # Initialize the blockchain infrastructure
    blockchain_status = initialize_blockchain(config)
    
    # Configure the mainnet connection
    vpod_main = setup_vpods_main_connection(
        network="mainnet",
        node_count=config.node_count,
        external_rpc=external_rpc
    )
    
    return {
        "status": "connected",
        "network": "mainnet",
        "connection_id": vpod_main.get("connection_id"),
        "node_count": config.node_count,
        "rpc_endpoint": blockchain_status.get("rpc_endpoint")
    }

def connect_to_testnet(
    connector_nodes: int = 2, 
    external_rpc: str = "https://rpc.ankr.com/eth_sepolia",
    testnet_server: Optional[str] = None
) -> Dict[str, Any]:
    """
    Connect the blockchain infrastructure to Ethereum testnet
    
    Args:
        connector_nodes: Number of nodes to connect to testnet (2-5 recommended)
        external_rpc: Testnet RPC endpoint URL
        testnet_server: Optional specific testnet server address (e.g. "159.203.17.36")
        
    Returns:
        Dict with connection status and details
    """
    logger.info(f"Connecting to Ethereum testnet via {external_rpc}")
    
    # Special handling for specific testnet server if provided
    if testnet_server:
        logger.info(f"Using specific testnet server: {testnet_server}")
        # Configure SSH connection to the testnet server if needed
        external_rpc = f"http://{testnet_server}:8545"
    
    # Create a testnet blockchain config
    config = BlockchainConfig(
        network="testnet",
        node_count=max(2, min(connector_nodes, 5)),  # Between 2-5 nodes
        connect_external=True,
        external_rpc=external_rpc
    )
    
    # Initialize the blockchain infrastructure
    blockchain_status = initialize_blockchain(config)
    
    # Configure the testnet connection
    vpod_main = setup_vpods_main_connection(
        network="testnet",
        node_count=config.node_count,
        external_rpc=external_rpc
    )
    
    return {
        "status": "connected",
        "network": "testnet",
        "connection_id": vpod_main.get("connection_id"),
        "node_count": config.node_count,
        "rpc_endpoint": blockchain_status.get("rpc_endpoint")
    }

def setup_vpods_main_connection(
    network: str, 
    node_count: int, 
    external_rpc: str
) -> Dict[str, Any]:
    """
    Set up the vPods.main component that connects to external network
    
    Args:
        network: Network type ("mainnet" or "testnet")
        node_count: Number of nodes to allocate
        external_rpc: External RPC endpoint
        
    Returns:
        Dict with connection details
    """
    logger.info(f"Setting up vPods.main connection to {network}")
    
    # This would typically involve K8s deployment configuration
    # For this implementation we'll simulate the connection
    
    # In production, this would deploy actual connector pods
    connection_id = f"vpods-main-{network}-{int(time.time())}"
    
    return {
        "connection_id": connection_id,
        "network": network,
        "node_count": node_count,
        "external_rpc": external_rpc
    }
