#!/usr/bin/env python3
"""
MetaNode SDK - Core Testnet Connectivity Module
==============================================

Core functions for connecting to and interacting with the MetaNode testnet.
"""

import json
import requests
import hashlib
import logging
from typing import Dict, Any, Optional, Union, List
from ..config.endpoints import API_URL, BLOCKCHAIN_URL, BFR_URL, VALIDATOR_URL

# Configure logging
logger = logging.getLogger(__name__)

class TestnetConnection:
    """Manages connection to the MetaNode testnet."""
    
    def __init__(self, url: Optional[str] = None):
        """Initialize a testnet connection.
        
        Args:
            url (str, optional): Custom testnet URL. If None, uses default from config.
        """
        self.api_url = url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.bfr_url = BFR_URL
        self.validator_url = VALIDATOR_URL
        self.connected = False
        self.node_id = None
        self.merkle_root = None
        self.last_sync_time = None
    
    def connect_to_testnet(self, client_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Connect the client/server to the MetaNode testnet.
        
        Args:
            client_id (str, optional): Unique identifier for the connecting client.
                If not provided, a new ID will be generated.
                
        Returns:
            dict: Connection status and node ID
        """
        try:
            # Generate client ID if not provided
            if not client_id:
                import uuid
                client_id = f"metanode-client-{uuid.uuid4()}"
            
            # Call connection endpoint
            response = requests.post(
                f"{self.api_url}/connect",
                headers={"Content-Type": "application/json"},
                json={"client_id": client_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.connected = True
                self.node_id = data.get("node_id", client_id)
                logger.info(f"Connected to testnet as node {self.node_id}")
                return {"status": "connected", "node_id": self.node_id}
            else:
                logger.error(f"Failed to connect to testnet: {response.text}")
                return {"status": "error", "message": response.text}
        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return {"status": "error", "message": str(e)}
    
    def check_status(self) -> Dict[str, Any]:
        """
        Fetch current testnet health, Merkle root, and vPod information.
        
        Returns:
            dict: Status information including health, merkle root, and vPods
        """
        try:
            # Check API health
            api_response = requests.get(f"{self.api_url}/health")
            
            # Check blockchain status
            blockchain_response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={"jsonrpc": "2.0", "method": "web3_clientVersion", "params": [], "id": 1}
            )
            
            # Check BFR status
            bfr_response = requests.post(
                self.bfr_url,
                headers={"Content-Type": "application/json"},
                json={"jsonrpc": "2.0", "method": "bfr_status", "params": [], "id": 1}
            )
            
            # Check validator status
            validator_response = requests.get(self.validator_url)
            
            # Get vPod status if available
            vpod_status = {}
            try:
                vpod_response = requests.get(f"{self.api_url}/vpod/status")
                if vpod_response.status_code == 200:
                    vpod_status = vpod_response.json()
            except:
                pass
            
            # Compile status information
            status_info = {
                "api": api_response.json() if api_response.status_code == 200 else {"status": "error"},
                "blockchain": blockchain_response.json() if blockchain_response.status_code == 200 else {"status": "error"},
                "bfr": bfr_response.json() if bfr_response.status_code == 200 else {"status": "error"},
                "validator": validator_response.json() if validator_response.status_code == 200 else {"status": "error"},
                "vpods": vpod_status,
                "connected": self.connected,
                "node_id": self.node_id
            }
            
            return status_info
            
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_mainnet_hash(self) -> Dict[str, Any]:
        """
        Retrieve current mainnet ledger hash.
        
        Returns:
            dict: Mainnet hash information
        """
        try:
            # Request the latest block hash from blockchain
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0", 
                    "method": "eth_getBlockByNumber", 
                    "params": ["latest", False], 
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data and data["result"]:
                    block_hash = data["result"].get("hash", "")
                    return {"status": "success", "mainnet_hash": block_hash}
                else:
                    return {"status": "error", "message": "No block hash found"}
            else:
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Mainnet hash retrieval error: {e}")
            return {"status": "error", "message": str(e)}
    
    def sync_state(self) -> Dict[str, Any]:
        """
        Sync local node with latest state hash and Merkle root.
        
        Returns:
            dict: Sync status and information
        """
        try:
            # Get latest block
            block_response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0", 
                    "method": "eth_getBlockByNumber", 
                    "params": ["latest", True], 
                    "id": 1
                }
            )
            
            if block_response.status_code != 200:
                return {"status": "error", "message": "Failed to get latest block"}
            
            block_data = block_response.json()
            
            # Get BFR consensus status
            bfr_response = requests.post(
                self.bfr_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "bfr_consensusStatus",
                    "params": ["main-federation"],
                    "id": 1
                }
            )
            
            if bfr_response.status_code == 200:
                bfr_data = bfr_response.json()
            else:
                bfr_data = {"result": {}}
            
            # Calculate Merkle root from transactions if available
            merkle_root = None
            if "result" in block_data and block_data["result"] and "transactions" in block_data["result"]:
                txs = block_data["result"]["transactions"]
                tx_hashes = [tx["hash"] for tx in txs if isinstance(tx, dict) and "hash" in tx]
                if tx_hashes:
                    merkle_root = self._calculate_merkle_root(tx_hashes)
            
            # Update instance state
            self.merkle_root = merkle_root
            import time
            self.last_sync_time = time.time()
            
            return {
                "status": "synced",
                "block_number": block_data.get("result", {}).get("number"),
                "block_hash": block_data.get("result", {}).get("hash"),
                "merkle_root": merkle_root,
                "consensus_status": bfr_data.get("result"),
                "sync_time": self.last_sync_time
            }
            
        except Exception as e:
            logger.error(f"State sync error: {e}")
            return {"status": "error", "message": str(e)}
    
    def _calculate_merkle_root(self, items: List[str]) -> str:
        """
        Calculate Merkle root from a list of items.
        
        Args:
            items: List of strings to calculate Merkle root from
            
        Returns:
            str: Merkle root hash
        """
        if not items:
            return None
            
        # If only one item, that's the root
        if len(items) == 1:
            return items[0]
            
        # Create new level
        new_level = []
        
        # Process pairs
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                # Hash the pair together
                combined = items[i] + items[i+1]
                hashed = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(hashed)
            else:
                # Odd number of items, promote the last one
                new_level.append(items[i])
        
        # Recursive call with the new level
        return self._calculate_merkle_root(new_level)


# Simple usage example
if __name__ == "__main__":
    # Create connection to testnet
    testnet = TestnetConnection()
    
    # Connect to testnet
    connect_result = testnet.connect_to_testnet()
    print(f"Connection result: {json.dumps(connect_result, indent=2)}")
    
    # Check status
    status = testnet.check_status()
    print(f"Testnet status: {json.dumps(status, indent=2)}")
    
    # Get mainnet hash
    hash_info = testnet.get_mainnet_hash()
    print(f"Mainnet hash: {json.dumps(hash_info, indent=2)}")
    
    # Sync state
    sync_result = testnet.sync_state()
    print(f"State sync: {json.dumps(sync_result, indent=2)}")
