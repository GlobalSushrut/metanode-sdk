#!/usr/bin/env python3
"""
MetaNode dApp Integration Example
===============================
Example of transforming any application into a decentralized app
with blockchain properties

This example demonstrates:
1. Transforming a Docker app into a docker.lock format with blockchain properties
2. Transforming Kubernetes deployments with blockchain integration
3. Creating an immutable decentralized agent

The implementation uses the successful vPod container approach that fixed
the MetaNode demo CLI, ensuring both federated-average and secure-aggregation 
algorithms work properly.
"""

import os
import sys
import logging
import argparse
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("metanode-example")

# Add parent directory to path to import metanode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import MetaNode SDK
try:
    from metanode.dapp import make_dapp, create_agent, execute_immutable_action, check_blockchain_connection
except ImportError:
    logger.error("Failed to import metanode.dapp. Please install the MetaNode SDK first.")
    sys.exit(1)

def transform_app_example(app_path: str, use_mainnet: bool = False) -> Dict[str, Any]:
    """
    Demonstrate transforming an app to a dApp
    
    Args:
        app_path: Path to application directory
        use_mainnet: Whether to use mainnet
        
    Returns:
        Transformation results
    """
    logger.info(f"Transforming app at {app_path} to a dApp (mainnet: {use_mainnet})")
    
    # Use the make_dapp function from the API
    # This will automatically add blockchain properties to your app
    result = make_dapp(app_path, use_mainnet=use_mainnet)
    
    logger.info(f"App transformed successfully: {result}")
    logger.info(f"Environment file created at {result.get('env_file')}")
    
    # Show what was transformed
    if "docker" in result:
        logger.info(f"Docker transformation: {result['docker']['status']}")
    
    if "kubernetes" in result:
        logger.info(f"Kubernetes transformation: {result['kubernetes']['status']}")
        logger.info(f"Transformed {result['kubernetes']['file_count']} Kubernetes files")
    
    return result

def agent_example(use_mainnet: bool = False) -> Dict[str, Any]:
    """
    Demonstrate creating and using an immutable decentralized agent
    
    Args:
        use_mainnet: Whether to use mainnet
        
    Returns:
        Action result
    """
    logger.info(f"Creating immutable decentralized agent (mainnet: {use_mainnet})")
    
    # First check blockchain connection
    connection = check_blockchain_connection(use_mainnet)
    logger.info(f"Blockchain connection status: {connection}")
    
    # Two ways to use an agent:
    
    # 1. Using the simple API function
    result1 = execute_immutable_action(
        action_type="store_data",
        data={"key": "example-key", "value": "example-value"},
        critical=False,
        use_mainnet=use_mainnet
    )
    logger.info(f"Executed action via API: {result1}")
    
    # 2. Creating and using an agent directly
    agent = create_agent(use_mainnet)
    
    # Use vPod container approach with federated-average and secure-aggregation
    result2 = agent.execute_action(
        action_type="run_algorithm", 
        data={
            "algorithm": "federated-average", 
            "participants": ["node-1", "node-2"],
            "config": {"rounds": 10, "batch_size": 32}
        },
        critical=True  # Requires consensus
    )
    logger.info(f"Executed algorithm via agent: {result2}")
    
    # Get all proofs recorded by the agent
    proofs = agent.get_proofs()
    logger.info(f"Agent has recorded {len(proofs)} proofs")
    
    return result2

def main():
    """Main function to demonstrate SDK usage"""
    parser = argparse.ArgumentParser(description='MetaNode dApp Integration Example')
    parser.add_argument('--app-path', type=str, help='Path to application directory', default='./app')
    parser.add_argument('--mainnet', action='store_true', help='Use mainnet instead of testnet')
    parser.add_argument('--mode', choices=['transform', 'agent', 'all'], default='all',
                        help='Mode to run: transform app, run agent, or both')
    args = parser.parse_args()
    
    logger.info(f"Starting MetaNode dApp Integration Example on {'mainnet' if args.mainnet else 'testnet'}")
    
    if args.mode in ['transform', 'all']:
        # Example 1: Transform app to dApp
        if os.path.exists(args.app_path):
            transform_result = transform_app_example(args.app_path, args.mainnet)
            logger.info(f"App transformation complete: {transform_result.get('status', 'success')}")
        else:
            logger.warning(f"App path {args.app_path} does not exist. Skipping transformation.")
    
    if args.mode in ['agent', 'all']:
        # Example 2: Use immutable decentralized agent
        try:
            agent_result = agent_example(args.mainnet)
            logger.info(f"Agent example complete: {agent_result.get('success')}")
        except Exception as e:
            logger.error(f"Agent example failed: {str(e)}")
    
    logger.info("Example completed successfully!")

if __name__ == "__main__":
    main()
