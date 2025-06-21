"""
MetaNode SDK - Configuration Settings
=================================

Global settings for MetaNode SDK blockchain components and infrastructure.
Defines defaults for:
- Blockchain settings
- Docker configuration 
- Kubernetes deployment options
- Storage parameters
- Validation thresholds
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("metanode-config")

# Base directories
METANODE_HOME = os.path.expanduser("~/.metanode")
METANODE_CONFIG_DIR = os.path.join(METANODE_HOME, "config")
METANODE_DATA_DIR = os.path.join(METANODE_HOME, "data")
METANODE_KEYS_DIR = os.path.join(METANODE_HOME, "keys")

# Lock files
DOCKER_LOCK_PATH = "/tmp/docker.lock"
DB_LOCK_PATH = "/tmp/db.lock"

# Create directories if they don't exist
for directory in [METANODE_HOME, METANODE_CONFIG_DIR, METANODE_DATA_DIR, METANODE_KEYS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

# Blockchain settings
BLOCKCHAIN_SETTINGS = {
    "default_node_count": 3,
    "default_validator_count": 2,
    "default_storage_node_count": 3,
    "consensus_threshold": 0.67,  # 67% consensus required
    "max_transaction_retries": 3,
    "default_gas_limit": 3000000,
    "default_gas_price": "20000000000",  # 20 Gwei
    "confirmation_blocks": 1,
    "block_time": 15,  # seconds (Ethereum-like)
}

# Docker settings
DOCKER_SETTINGS = {
    "base_image": "metanode/vpod-base:latest",
    "blockchain_image": "metanode/blockchain-node:latest",
    "validator_image": "metanode/validator-node:latest",
    "storage_image": "metanode/storage-node:latest",
    "network_name": "metanode-network",
    "default_ports": {
        "rpc": 8545,
        "ws": 8546,
        "api": 8000,
        "validator": 8050,
        "storage": 8060,
    }
}

# Kubernetes settings
K8S_SETTINGS = {
    "namespace": "metanode",
    "service_account": "metanode-sa",
    "resource_limits": {
        "cpu": "500m",
        "memory": "512Mi"
    },
    "resource_requests": {
        "cpu": "250m",
        "memory": "256Mi"
    },
    "storage_class": "standard",
    "persistent_volume_size": "10Gi",
}

# API endpoints
DEFAULT_TESTNET_SERVER = "159.203.17.36"
DEFAULT_RPC_ENDPOINT = "http://localhost:8545"

def get_settings(section: str) -> Dict[str, Any]:
    """Get settings for a specific section"""
    if section.lower() == "blockchain":
        return BLOCKCHAIN_SETTINGS
    elif section.lower() == "docker":
        return DOCKER_SETTINGS
    elif section.lower() == "k8s":
        return K8S_SETTINGS
    else:
        return {}

def get_user_configuration() -> Dict[str, Any]:
    """Load user-specific configuration if available"""
    user_config_path = os.path.join(METANODE_CONFIG_DIR, "user_config.json")
    
    if not os.path.exists(user_config_path):
        return {}
        
    try:
        with open(user_config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load user configuration: {e}")
        return {}
