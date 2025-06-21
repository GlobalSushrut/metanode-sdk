#!/usr/bin/env python3
"""
MetaNode Testnet Connection Demo
===============================

This script demonstrates how to use the MetaNode SDK to connect to the deployed testnet
and perform various operations like checking node status, managing wallets, and retrieving
blockchain information.
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime

# Import MetaNode SDK components
from metanode.admin.k8s_manager import K8sManager
from metanode.wallet.core import WalletManager
from metanode.wallet.escrow import EscrowManager
from metanode.ledger.verification import Verifier
from metanode.utils.ipfs_tools import IPFSManager
from metanode.config.endpoints import API_URL, BLOCKCHAIN_URL, BFR_URL, VALIDATOR_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("metanode-testnet-client")

def check_testnet_status():
    """Check if the testnet nodes are accessible and responding."""
    endpoints = {
        "API": API_URL,
        "Blockchain": BLOCKCHAIN_URL,
        "BFR": BFR_URL,
        "Validator": VALIDATOR_URL
    }
    
    status = {}
    for name, url in endpoints.items():
        try:
            logger.info(f"Checking {name} endpoint at {url}...")
            response = requests.get(f"{url}/status", timeout=5)
            if response.status_code == 200:
                status[name] = {
                    "status": "online",
                    "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
                logger.info(f"{name} is online")
            else:
                status[name] = {"status": "error", "code": response.status_code}
                logger.warning(f"{name} returned status code {response.status_code}")
        except requests.RequestException as e:
            status[name] = {"status": "error", "message": str(e)}
            logger.error(f"Failed to connect to {name}: {e}")
            
            # Try a simple ping if the /status endpoint fails
            try:
                ping_response = requests.get(url, timeout=3)
                status[name]["ping"] = {
                    "code": ping_response.status_code,
                    "response": "Endpoint exists but no /status endpoint"
                }
                logger.info(f"{name} base URL is accessible with status {ping_response.status_code}")
            except requests.RequestException:
                logger.error(f"Failed to ping base URL for {name}")
    
    return status

def get_blockchain_info():
    """Get information about the blockchain from the RPC endpoint."""
    try:
        logger.info(f"Querying blockchain info from {BLOCKCHAIN_URL}...")
        
        # Get blockchain node info
        response = requests.post(
            BLOCKCHAIN_URL,
            headers={"Content-Type": "application/json"},
            json={
                "jsonrpc": "2.0",
                "method": "web3_clientVersion",
                "params": [],
                "id": 1
            },
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Blockchain node version: {result.get('result', 'Not available')}")
            
            # Get current block number
            block_response = requests.post(
                BLOCKCHAIN_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_blockNumber",
                    "params": [],
                    "id": 1
                },
                timeout=5
            )
            
            if block_response.status_code == 200:
                block_result = block_response.json()
                block_number = int(block_result.get('result', '0x0'), 16)
                logger.info(f"Current block number: {block_number}")
                
                # Get network ID
                net_response = requests.post(
                    BLOCKCHAIN_URL,
                    headers={"Content-Type": "application/json"},
                    json={
                        "jsonrpc": "2.0",
                        "method": "net_version",
                        "params": [],
                        "id": 1
                    },
                    timeout=5
                )
                
                net_id = "unknown"
                if net_response.status_code == 200:
                    net_result = net_response.json()
                    net_id = net_result.get('result', 'unknown')
                    logger.info(f"Network ID: {net_id}")
                
                return {
                    "status": "success",
                    "client_version": result.get('result'),
                    "block_number": block_number,
                    "network_id": net_id
                }
            else:
                logger.error(f"Failed to get block number, status: {block_response.status_code}")
                return {"status": "error", "message": f"Failed to get block number: {block_response.text}"}
        else:
            logger.error(f"Failed to get blockchain info, status: {response.status_code}")
            return {"status": "error", "message": f"Failed to get blockchain info: {response.text}"}
            
    except requests.RequestException as e:
        logger.error(f"Failed to connect to blockchain endpoint: {e}")
        return {"status": "error", "message": str(e)}

def check_wallet_status():
    """Check if we can access wallet functionality using the SDK."""
    try:
        logger.info("Creating wallet manager...")
        wallet_manager = WalletManager()
        
        # List available wallets
        wallets = wallet_manager.list_wallets()
        logger.info(f"Found {len(wallets)} existing wallets")
        
        # If no wallets exist, create a test wallet
        if not wallets:
            logger.info("Creating a new test wallet...")
            new_wallet = wallet_manager.create_wallet("test-wallet")
            logger.info(f"Created new wallet with address: {new_wallet.address}")
            return {
                "status": "success", 
                "message": "Created new test wallet", 
                "address": new_wallet.address
            }
        else:
            # Just return the first wallet
            logger.info(f"Found existing wallet: {wallets[0]}")
            return {
                "status": "success",
                "message": "Using existing wallet",
                "address": wallets[0]
            }
    except Exception as e:
        logger.error(f"Failed to check wallet status: {e}")
        return {"status": "error", "message": str(e)}

def check_testnet_nodes():
    """Check the status of testnet nodes using the K8s manager."""
    try:
        logger.info("Initializing Kubernetes manager...")
        k8s_manager = K8sManager()
        
        nodes = k8s_manager.list_testnet_nodes()
        logger.info(f"Found {len(nodes)} testnet nodes")
        
        return {
            "status": "success",
            "nodes": nodes
        }
    except Exception as e:
        logger.error(f"Failed to check testnet nodes: {e}")
        return {"status": "error", "message": str(e)}

def main():
    """Run the testnet connection demo."""
    logger.info("==========================================")
    logger.info("MetaNode Testnet Connection Demo")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("==========================================")
    
    # Store results for reporting
    results = {}
    
    # Check if testnet endpoints are accessible
    logger.info("\n== Checking Testnet Status ==")
    results["testnet_status"] = check_testnet_status()
    
    # Get blockchain information
    logger.info("\n== Retrieving Blockchain Information ==")
    results["blockchain_info"] = get_blockchain_info()
    
    # Check wallet functionality
    logger.info("\n== Checking Wallet Status ==")
    results["wallet_status"] = check_wallet_status()
    
    # Check testnet nodes
    logger.info("\n== Checking Testnet Nodes ==")
    results["testnet_nodes"] = check_testnet_nodes()
    
    # Write results to file
    output_file = "testnet_connection_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"\nResults written to {output_file}")
    logger.info("==========================================")
    logger.info("Demo completed")
    logger.info("==========================================")

if __name__ == "__main__":
    main()
