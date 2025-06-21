"""
MetaNode dApp API
===============
Simple API for transforming any app into a decentralized app
"""

import os
import logging
from typing import Dict, Any, Optional, Union

from metanode.dapp.fixed_connector import DAppConnector
from metanode.dapp.agent import DecentralizedAgent
from metanode.deployment.network_config import NetworkConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("metanode.dapp.api")

def make_dapp(
    app_path: str, 
    use_mainnet: bool = False, 
    wallet_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transform any application into a decentralized app
    
    Args:
        app_path: Path to application directory
        use_mainnet: Whether to use mainnet (requires tokens)
        wallet_path: Path to wallet file for mainnet token payment
        
    Returns:
        Transformation results
    """
    connector = DAppConnector(use_mainnet=use_mainnet, wallet_path=wallet_path)
    return connector.transform_app(app_path)
    
def deploy_dapp(
    app_path: str, 
    target_server: str,
    use_mainnet: bool = False, 
    wallet_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Deploy app to target server as a decentralized app
    
    Args:
        app_path: Path to application directory
        target_server: Target server address (user@host)
        use_mainnet: Whether to use mainnet (requires tokens)
        wallet_path: Path to wallet file for mainnet token payment
        
    Returns:
        Deployment results
    """
    connector = DAppConnector(use_mainnet=use_mainnet, wallet_path=wallet_path)
    return connector.deploy(app_path, target_server)
    
def create_agent(use_mainnet: bool = False) -> DecentralizedAgent:
    """
    Create immutable decentralized agent with blockchain connection
    
    Args:
        use_mainnet: Whether to use mainnet
        
    Returns:
        Decentralized agent instance
    """
    network_config = NetworkConfig()
    network_endpoints = network_config.get_network_endpoints(use_mainnet)
    
    agent = DecentralizedAgent(network_endpoints, use_mainnet)
    agent.connect()
    
    return agent
    
def execute_immutable_action(
    action_type: str,
    data: Dict[str, Any],
    critical: bool = False,
    use_mainnet: bool = False
) -> Dict[str, Any]:
    """
    Execute immutable action with blockchain validation
    
    Args:
        action_type: Type of action
        data: Action data
        critical: Whether action is critical (requires consensus)
        use_mainnet: Whether to use mainnet
        
    Returns:
        Action result with proof
    """
    agent = create_agent(use_mainnet)
    return agent.execute_action(action_type, data, critical)
    
def check_blockchain_connection(use_mainnet: bool = False) -> Dict[str, Any]:
    """
    Check blockchain connection status
    
    Args:
        use_mainnet: Whether to check mainnet
        
    Returns:
        Connection status information
    """
    network_config = NetworkConfig()
    network_endpoints = network_config.get_network_endpoints(use_mainnet)
    
    agent = DecentralizedAgent(network_endpoints, use_mainnet)
    connected = agent.connect()
    
    return {
        "connected": connected,
        "network": "mainnet" if use_mainnet else "testnet",
        "agent_id": agent.agent_id if connected else None,
        "endpoints": network_endpoints
    }
