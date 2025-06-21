#!/usr/bin/env python3
"""
MetaNode Network Configuration
==============================
Manages network configuration for testnet/mainnet connections
"""

import os
import json
from typing import Dict, Any, Optional, List

class NetworkConfig:
    """Configuration manager for MetaNode network connections"""
    
    def __init__(self, use_mainnet: bool = False):
        """
        Initialize network configuration
        
        Args:
            use_mainnet: Whether to use mainnet (True) or testnet (False)
        """
        self.use_mainnet = use_mainnet
        self.config_dir = os.path.expanduser("~/.metanode")
        os.makedirs(self.config_dir, exist_ok=True)
        
    def get_endpoints(self) -> Dict[str, str]:
        """
        Get network endpoints based on selected network
        
        Returns:
            Dictionary of endpoint URLs
        """
        if self.use_mainnet:
            return {
                "rpc_url": "https://mainnet.metanode.network:8545",
                "ws_url": "wss://mainnet.metanode.network:8546",
                "wallet_url": "https://wallet.metanode.network",
                "ipfs_gateway": "https://ipfs.metanode.network",
                "token_contract": "0x7a58c0Be72BE218B41C608b7Fe7C5bB630736C71"
            }
        else:
            return {
                "rpc_url": "http://159.203.17.36:8545",
                "ws_url": "ws://159.203.17.36:8546",
                "wallet_url": "http://159.203.17.36:8080",
                "ipfs_gateway": "http://159.203.17.36:8080/ipfs",
                "token_contract": "0xD8f24D419153E5D03d614C5155f900f4B5C8A65C"
            }
            
    def save_network_selection(self) -> None:
        """Save network selection to config file"""
        config_path = os.path.join(self.config_dir, "network.json")
        with open(config_path, "w") as f:
            json.dump({"use_mainnet": self.use_mainnet}, f, indent=2)
            
    def load_network_selection(self) -> bool:
        """
        Load network selection from config file
        
        Returns:
            Boolean indicating if mainnet is selected
        """
        config_path = os.path.join(self.config_dir, "network.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    self.use_mainnet = config.get("use_mainnet", False)
            except Exception:
                self.use_mainnet = False
                
        return self.use_mainnet
