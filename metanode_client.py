#!/usr/bin/env python3
"""
MetaNode Client SDK
==================
A Python SDK for interacting with MetaNode services.
"""

import json
import requests
from typing import Dict, Any, Optional, Union, List


class MetaNodeSDK:
    """Client SDK for interacting with MetaNode services."""
    
    def __init__(self, base_url: str = "http://159.203.17.36"):
        """Initialize the MetaNode SDK with the server base URL.
        
        Args:
            base_url: Base URL for the MetaNode server (default: the current deployment)
        """
        self.base_url = base_url.rstrip('/')
        self.api_port = 8000
        self.blockchain_port = 8545
        self.bfr_port = 9000
        self.validator_port = 9001
        
        # Service URLs
        self.api_url = f"{self.base_url}:{self.api_port}"
        self.blockchain_url = f"{self.base_url}:{self.blockchain_port}"
        self.bfr_url = f"{self.base_url}:{self.bfr_port}"
        self.validator_url = f"{self.base_url}:{self.validator_port}"

    # API Service Methods
    def check_health(self) -> Dict[str, Any]:
        """Check the health of the API service.
        
        Returns:
            Dict with status information
        """
        response = requests.get(f"{self.api_url}/health")
        return response.json()
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get information about the API service.
        
        Returns:
            Dict with API information
        """
        response = requests.get(f"{self.api_url}/mode")
        return response.json()
    
    # Blockchain Service Methods
    def get_blockchain_version(self) -> Dict[str, Any]:
        """Get the blockchain client version.
        
        Returns:
            Dict with version information
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "web3_clientVersion",
            "params": [],
            "id": 1
        }
        response = requests.post(
            self.blockchain_url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        return response.json()
    
    def get_latest_block(self) -> Dict[str, Any]:
        """Get the latest block from the blockchain.
        
        Returns:
            Dict with block information
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": ["latest", True],
            "id": 1
        }
        response = requests.post(
            self.blockchain_url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        return response.json()
    
    def send_transaction(self, raw_transaction: str) -> Dict[str, Any]:
        """Send a raw transaction to the blockchain.
        
        Args:
            raw_transaction: Hexadecimal string of the raw transaction
            
        Returns:
            Dict with transaction result
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_sendRawTransaction",
            "params": [raw_transaction],
            "id": 1
        }
        response = requests.post(
            self.blockchain_url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        return response.json()
    
    # BFR Service Methods
    def check_bfr_status(self) -> Dict[str, Any]:
        """Check the status of the BFR service.
        
        Returns:
            Dict with BFR status
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "bfr_status",
            "params": [],
            "id": 1
        }
        response = requests.post(
            self.bfr_url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        return response.json()
    
    def check_consensus_status(self, federation_id: str = "test-federation") -> Dict[str, Any]:
        """Check the consensus status for a federation.
        
        Args:
            federation_id: ID of the federation
            
        Returns:
            Dict with consensus status
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "bfr_consensusStatus",
            "params": [federation_id],
            "id": 1
        }
        response = requests.post(
            self.bfr_url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        return response.json()
    
    # Validator Service Methods
    def check_validator_status(self) -> Dict[str, Any]:
        """Check the status of the validator service.
        
        Returns:
            Dict with validator status
        """
        response = requests.get(self.validator_url)
        return response.json()

    # Helper methods for future enhancements
    def custom_api_call(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a custom call to the API service.
        
        Args:
            endpoint: API endpoint (without leading slash)
            method: HTTP method
            data: Request data for POST calls
            
        Returns:
            Response data
        """
        url = f"{self.api_url}/{endpoint}"
        if method.upper() == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        return response.json()
    
    def custom_blockchain_call(self, method: str, params: List[Any]) -> Dict[str, Any]:
        """Make a custom call to the blockchain RPC.
        
        Args:
            method: RPC method name
            params: List of parameters
            
        Returns:
            Response data
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        response = requests.post(
            self.blockchain_url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        return response.json()


# Usage example
if __name__ == "__main__":
    print("MetaNode SDK Test")
    print("=================")
    
    # Create client
    client = MetaNodeSDK()
    
    # Test health checks
    print("\nHealth Checks:")
    print(f"API: {json.dumps(client.check_health(), indent=2)}")
    print(f"Blockchain: {json.dumps(client.get_blockchain_version(), indent=2)}")
    print(f"BFR: {json.dumps(client.check_bfr_status(), indent=2)}")
    print(f"Validator: {json.dumps(client.check_validator_status(), indent=2)}")
    
    # Test blockchain functionality
    print("\nBlockchain Latest Block:")
    print(json.dumps(client.get_latest_block(), indent=2))
    
    print("\nSDK test complete!")
