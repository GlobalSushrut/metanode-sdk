#!/usr/bin/env python3
"""
MetaNode Mining Console

Advanced blockchain mining console for MetaNode infrastructure.
Allows adding computing resources to the network and managing the blockchain.
"""

import os
import time
import json
import uuid
import logging
import argparse
import datetime
from typing import Dict, List, Optional
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode.mining")

class MiningConsole:
    """MetaNode Mining Console for managing blockchain resources"""
    
    def __init__(self, data_dir: str = "~/.metanode/mining"):
        """Initialize the mining console"""
        self.data_dir = os.path.expanduser(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Resource tracking
        self.resources_file = os.path.join(self.data_dir, "resources.json")
        self.resources = self._load_resources()
        
        # Node status
        self.is_mining = False
        self.node_id = str(uuid.uuid4())
        self.start_time = time.time()
    
    def _load_resources(self) -> Dict:
        """Load resource data"""
        if os.path.exists(self.resources_file):
            try:
                with open(self.resources_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading resources: {e}")
        
        # Initialize with defaults
        return {
            "nodes": [],
            "total_compute": 0,
            "total_storage": 0,
            "active_nodes": 0,
            "last_updated": time.time(),
            "mainnet_status": "operational"
        }
    
    def _save_resources(self) -> None:
        """Save resource data"""
        try:
            with open(self.resources_file, 'w') as f:
                json.dump(self.resources, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving resources: {e}")
    
    def start_mining(self, compute_power: float, storage_gb: float) -> Dict:
        """Start mining with specified resources"""
        if self.is_mining:
            logger.warning("Mining is already active")
            return {"status": "already_mining", "node_id": self.node_id}
        
        # Register node
        node_info = {
            "node_id": self.node_id,
            "compute_power": compute_power,
            "storage_gb": storage_gb,
            "started_at": time.time(),
            "last_block": None,
            "blocks_mined": 0,
            "rewards_earned": 0.0
        }
        
        # Update resources
        self.resources["nodes"].append(node_info)
        self.resources["total_compute"] += compute_power
        self.resources["total_storage"] += storage_gb
        self.resources["active_nodes"] += 1
        self.resources["last_updated"] = time.time()
        
        self._save_resources()
        self.is_mining = True
        
        logger.info(f"Started mining with node {self.node_id}")
        return {
            "status": "mining_started",
            "node_id": self.node_id,
            "mainnet_status": self.resources["mainnet_status"]
        }
    
    def stop_mining(self) -> Dict:
        """Stop mining"""
        if not self.is_mining:
            logger.warning("Mining is not active")
            return {"status": "not_mining"}
        
        # Find and update node
        for node in self.resources["nodes"]:
            if node["node_id"] == self.node_id:
                # Calculate mining time
                mining_time = time.time() - node["started_at"]
                
                # Update resources
                self.resources["total_compute"] -= node["compute_power"]
                self.resources["total_storage"] -= node["storage_gb"]
                self.resources["active_nodes"] -= 1
                self.resources["last_updated"] = time.time()
                
                # Remove node
                self.resources["nodes"] = [n for n in self.resources["nodes"] 
                                         if n["node_id"] != self.node_id]
                
                self._save_resources()
                self.is_mining = False
                
                logger.info(f"Stopped mining with node {self.node_id}")
                return {
                    "status": "mining_stopped",
                    "node_id": self.node_id,
                    "mining_time": mining_time,
                    "rewards_earned": node["rewards_earned"]
                }
        
        # Node not found
        logger.error(f"Node {self.node_id} not found")
        self.is_mining = False
        return {"status": "error", "message": "Node not found"}
    
    def get_mining_stats(self) -> Dict:
        """Get mining statistics"""
        # Find node info
        node_info = next((node for node in self.resources["nodes"] 
                         if node["node_id"] == self.node_id), None)
        
        if not node_info:
            return {
                "status": "not_mining",
                "mainnet_stats": {
                    "total_nodes": len(self.resources["nodes"]),
                    "total_compute": self.resources["total_compute"],
                    "total_storage": self.resources["total_storage"],
                    "mainnet_status": self.resources["mainnet_status"]
                }
            }
        
        # Calculate mining time
        mining_time = time.time() - node_info["started_at"]
        
        return {
            "status": "mining",
            "node_id": self.node_id,
            "compute_power": node_info["compute_power"],
            "storage_gb": node_info["storage_gb"],
            "mining_time": mining_time,
            "blocks_mined": node_info["blocks_mined"],
            "rewards_earned": node_info["rewards_earned"],
            "mainnet_stats": {
                "total_nodes": len(self.resources["nodes"]),
                "total_compute": self.resources["total_compute"],
                "total_storage": self.resources["total_storage"],
                "mainnet_status": self.resources["mainnet_status"]
            }
        }

    def mine_block(self) -> Dict:
        """Mine a new block"""
        if not self.is_mining:
            logger.warning("Mining is not active")
            return {"status": "not_mining"}
        
        # Find node info
        for node in self.resources["nodes"]:
            if node["node_id"] == self.node_id:
                # Simulate mining a block
                block_id = f"block_{uuid.uuid4().hex[:8]}"
                timestamp = time.time()
                
                # Calculate reward based on compute power
                reward = node["compute_power"] * 0.01 + 1.0
                
                # Update node info
                node["last_block"] = block_id
                node["blocks_mined"] += 1
                node["rewards_earned"] += reward
                
                self._save_resources()
                
                logger.info(f"Mined block {block_id}, earned {reward} tokens")
                return {
                    "status": "block_mined",
                    "block_id": block_id,
                    "timestamp": timestamp,
                    "reward": reward,
                    "total_mined": node["blocks_mined"],
                    "total_rewards": node["rewards_earned"]
                }
        
        # Node not found
        logger.error(f"Node {self.node_id} not found")
        return {"status": "error", "message": "Node not found"}

# Main function for CLI
def main():
    """Main function for the mining console CLI"""
    parser = argparse.ArgumentParser(description="MetaNode Mining Console")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Start mining
    start_parser = subparsers.add_parser("start", help="Start mining")
    start_parser.add_argument("--compute", type=float, default=1.0, 
                             help="Compute power to contribute (units)")
    start_parser.add_argument("--storage", type=float, default=10.0, 
                             help="Storage to contribute (GB)")
    
    # Stop mining
    subparsers.add_parser("stop", help="Stop mining")
    
    # Get mining stats
    subparsers.add_parser("stats", help="Get mining statistics")
    
    # Mine a block manually
    subparsers.add_parser("mine", help="Mine a block manually")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize mining console
    console = MiningConsole()
    
    # Handle commands
    if args.command == "start":
        result = console.start_mining(args.compute, args.storage)
        print(f"\n=== MetaNode Mining Started ===")
        print(f"Node ID: {result['node_id']}")
        print(f"Mainnet Status: {result['mainnet_status']}")
        print(f"\nContributing:")
        print(f"  - {args.compute} compute units")
        print(f"  - {args.storage} GB storage")
        print(f"\nMining is now active. Press Ctrl+C to stop.")
        
        # Keep mining until interrupted
        try:
            while True:
                time.sleep(10)
                result = console.mine_block()
                if result["status"] == "block_mined":
                    print(f"\n✅ Block mined: {result['block_id']}")
                    print(f"Reward: {result['reward']} MetaTokens")
                    print(f"Total mined: {result['total_mined']} blocks")
                    print(f"Total rewards: {result['total_rewards']} MetaTokens")
        except KeyboardInterrupt:
            result = console.stop_mining()
            print(f"\n=== Mining Stopped ===")
            print(f"Mining time: {result['mining_time']:.2f} seconds")
            print(f"Rewards earned: {result['rewards_earned']} MetaTokens")
    
    elif args.command == "stop":
        result = console.stop_mining()
        print(f"\n=== Mining Stopped ===")
        if result["status"] == "mining_stopped":
            print(f"Node ID: {result['node_id']}")
            print(f"Mining time: {result['mining_time']:.2f} seconds")
            print(f"Rewards earned: {result['rewards_earned']} MetaTokens")
        else:
            print(f"Status: {result['status']}")
    
    elif args.command == "stats":
        result = console.get_mining_stats()
        print(f"\n=== MetaNode Mining Statistics ===")
        
        print(f"\nMainnet Status:")
        print(f"  - Active nodes: {result['mainnet_stats']['total_nodes']}")
        print(f"  - Total compute: {result['mainnet_stats']['total_compute']} units")
        print(f"  - Total storage: {result['mainnet_stats']['total_storage']} GB")
        print(f"  - Status: {result['mainnet_stats']['mainnet_status']}")
        
        if result["status"] == "mining":
            print(f"\nYour Node ({result['node_id']}):")
            print(f"  - Mining time: {result['mining_time']:.2f} seconds")
            print(f"  - Compute: {result['compute_power']} units")
            print(f"  - Storage: {result['storage_gb']} GB")
            print(f"  - Blocks mined: {result['blocks_mined']}")
            print(f"  - Rewards earned: {result['rewards_earned']} MetaTokens")
        else:
            print(f"\nYour node is not currently mining.")
    
    elif args.command == "mine":
        result = console.mine_block()
        if result["status"] == "block_mined":
            print(f"\n=== Block Mined ===")
            print(f"Block ID: {result['block_id']}")
            print(f"Reward: {result['reward']} MetaTokens")
            print(f"Total mined: {result['total_mined']} blocks")
            print(f"Total rewards: {result['total_rewards']} MetaTokens")
        else:
            print(f"\nError: {result['status']}")
            if result["status"] == "not_mining":
                print("You need to start mining first with 'metanode-miner start'")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
