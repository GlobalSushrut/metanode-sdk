#!/usr/bin/env python3
"""
MetaNode SDK - Wallet Escrow Module
=================================

Tools for managing token staking, escrow, and service payments.
"""

import os
import json
import time
import hashlib
import logging
import requests
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL, BLOCKCHAIN_URL

# Configure logging
logger = logging.getLogger(__name__)

class EscrowManager:
    """High-level manager for escrow operations across multiple wallets."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize escrow manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.wallet_dir = os.path.join(os.path.expanduser("~"), ".metanode", "wallets")
        self.escrow_dir = os.path.join(os.path.expanduser("~"), ".metanode", "escrow")
        
        # Ensure escrow directory exists
        os.makedirs(self.escrow_dir, exist_ok=True)
    
    def stake_for_mining(self, amount: float, duration: int = 30) -> Dict[str, Any]:
        """
        Stake tokens for mining eligibility.
        
        Args:
            amount: Amount to stake in tokens
            duration: Stake duration in days
        
        Returns:
            Dict with status and stake information
        """
        try:
            # Convert days to seconds for the blockchain
            seconds = duration * 86400
            
            # Use the first available wallet for staking
            wallet_files = [f for f in os.listdir(self.wallet_dir) if f.endswith(".json")]
            if not wallet_files:
                return {"status": "error", "message": "No wallets found. Create a wallet first."}
            
            # Load the wallet
            wallet_file = os.path.join(self.wallet_dir, wallet_files[0])
            with open(wallet_file, 'r') as f:
                wallet = json.load(f)
                address = wallet["address"]
            
            # Create escrow instance for this address
            escrow = Escrow(self.api_url, address)
            result = escrow.stake_for_mining(amount, seconds)
            
            # Save the stake information
            if result["status"] == "success" and "stake_id" in result:
                stake_file = os.path.join(self.escrow_dir, f"stake-{result['stake_id']}.json")
                with open(stake_file, 'w') as f:
                    json.dump({
                        "stake_id": result["stake_id"],
                        "address": address,
                        "amount": amount,
                        "duration_days": duration,
                        "timestamp": time.time(),
                        "expiration": result.get("expiration_time", time.time() + seconds),
                    }, f, indent=2)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to stake tokens: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_stakes(self) -> Dict[str, Any]:
        """
        List all active stakes.
        
        Returns:
            Dict with status and list of stakes
        """
        try:
            stakes = []
            for file in os.listdir(self.escrow_dir):
                if file.startswith("stake-") and file.endswith(".json"):
                    try:
                        with open(os.path.join(self.escrow_dir, file), "r") as f:
                            stake = json.load(f)
                            stakes.append(stake)
                    except Exception as e:
                        logger.warning(f"Failed to load stake file {file}: {e}")
            
            return {"status": "success", "stakes": stakes}
            
        except Exception as e:
            logger.error(f"Failed to list stakes: {e}")
            return {"status": "error", "message": str(e)}
    
    def release_stake(self, stake_id: str) -> Dict[str, Any]:
        """
        Release tokens from a stake.
        
        Args:
            stake_id: ID of the stake to release
            
        Returns:
            Dict with status and release information
        """
        try:
            # Find the stake file
            stake_file = os.path.join(self.escrow_dir, f"stake-{stake_id}.json")
            if not os.path.exists(stake_file):
                return {"status": "error", "message": f"Stake {stake_id} not found"}
            
            # Load the stake info
            with open(stake_file, 'r') as f:
                stake = json.load(f)
                address = stake["address"]
            
            # Create escrow instance for this address
            escrow = Escrow(self.api_url, address)
            result = escrow.release_stake(stake_id)
            
            # Remove the stake file if release successful
            if result["status"] == "success":
                os.remove(stake_file)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to release stake: {e}")
            return {"status": "error", "message": str(e)}

class Escrow:
    """Manages token escrow operations for staking and payments."""
    
    def __init__(self, api_url: Optional[str] = None, address: Optional[str] = None):
        """
        Initialize escrow manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            address (str, optional): Wallet address
        """
        self.api_url = api_url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.address = address
        self.wallet_dir = os.path.join(os.getcwd(), ".metanode", "wallet")
        
        # Try to load wallet address from file if not provided
        if not self.address:
            try:
                wallet_files = [f for f in os.listdir(self.wallet_dir) if f.startswith("wallet-") and f.endswith(".json")]
                if wallet_files:
                    wallet_file = os.path.join(self.wallet_dir, wallet_files[0])
                    with open(wallet_file, 'r') as f:
                        wallet = json.load(f)
                        self.address = wallet["address"]
            except Exception as e:
                logger.warning(f"Failed to load wallet address from file: {e}")
    
    def stake_for_mining(self, amount: float, duration: int = 30*86400) -> Dict[str, Any]:
        """
        Lock tokens into escrow for mining eligibility.
        
        Args:
            amount (float): Amount to stake in MNT tokens
            duration (int): Duration of stake in seconds (default: 30 days)
            
        Returns:
            dict: Staking result with stake ID
        """
        try:
            # Check if we have a wallet address
            if not self.address:
                return {
                    "status": "error", 
                    "message": "No wallet address. Load or create a wallet first."
                }
            
            # Validate amount
            if amount <= 0:
                return {
                    "status": "error", 
                    "message": "Invalid stake amount. Must be greater than 0."
                }
            
            # Convert amount to wei (1 MNT = 10^18 wei)
            amount_wei = int(amount * 1e18)
            amount_hex = hex(amount_wei)
            
            # Create stake transaction
            timestamp = int(time.time())
            expires_at = timestamp + duration
            
            stake = {
                "address": self.address,
                "amount": amount_hex,
                "amount_value": amount,
                "timestamp": timestamp,
                "expires_at": expires_at,
                "duration": duration
            }
            
            # Generate stake ID
            stake_input = f"{self.address}:{amount}:{timestamp}:{duration}"
            stake_id = hashlib.sha256(stake_input.encode()).hexdigest()[:16]
            stake["stake_id"] = stake_id
            
            # Send stake request to blockchain
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "metanode_stakeForMining",
                    "params": [{
                        "from": self.address,
                        "value": amount_hex,
                        "stakeId": stake_id,
                        "duration": hex(duration)
                    }],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    tx_hash = data["result"]
                    stake["tx_hash"] = tx_hash
                    
                    # Save stake information
                    stakes_dir = os.path.join(self.wallet_dir, "stakes")
                    os.makedirs(stakes_dir, exist_ok=True)
                    
                    stake_file = os.path.join(stakes_dir, f"stake-{stake_id}.json")
                    with open(stake_file, 'w') as f:
                        json.dump(stake, f, indent=2)
                    
                    logger.info(f"Staked {amount} MNT for mining with ID {stake_id} and tx {tx_hash}")
                    return {
                        "status": "success",
                        "stake_id": stake_id,
                        "address": self.address,
                        "amount": amount,
                        "tx_hash": tx_hash,
                        "expires_at": expires_at,
                        "stake_file": stake_file
                    }
                elif "error" in data:
                    logger.error(f"Staking error: {data['error']}")
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Staking request failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Staking error: {e}")
            return {"status": "error", "message": str(e)}
    
    def release_stake(self, stake_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Unlock stake after session completion.
        
        Args:
            stake_id (str, optional): ID of the stake to release. 
                If not provided, tries to find the latest stake.
            
        Returns:
            dict: Stake release result
        """
        try:
            # Find stake to release
            target_stake = None
            
            if stake_id:
                # Try to find specific stake file
                stake_file = os.path.join(self.wallet_dir, "stakes", f"stake-{stake_id}.json")
                if os.path.exists(stake_file):
                    with open(stake_file, 'r') as f:
                        target_stake = json.load(f)
            else:
                # Find latest stake
                stakes_dir = os.path.join(self.wallet_dir, "stakes")
                if os.path.exists(stakes_dir):
                    stake_files = [f for f in os.listdir(stakes_dir) if f.startswith("stake-") and f.endswith(".json")]
                    if stake_files:
                        # Sort by modification time (most recent first)
                        stake_files.sort(key=lambda x: os.path.getmtime(os.path.join(stakes_dir, x)), reverse=True)
                        
                        latest_file = os.path.join(stakes_dir, stake_files[0])
                        with open(latest_file, 'r') as f:
                            target_stake = json.load(f)
                            stake_id = target_stake.get("stake_id")
            
            if not target_stake or not stake_id:
                return {
                    "status": "error", 
                    "message": "No stake found to release."
                }
            
            # Check if the stake has expired
            current_time = int(time.time())
            if current_time < target_stake.get("expires_at", 0):
                logger.warning(f"Stake {stake_id} has not expired yet. Early release may incur penalties.")
            
            # Send release request to blockchain
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "metanode_releaseStake",
                    "params": [{
                        "from": self.address,
                        "stakeId": stake_id
                    }],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    tx_hash = data["result"]
                    
                    # Update stake file
                    stake_file = os.path.join(self.wallet_dir, "stakes", f"stake-{stake_id}.json")
                    if os.path.exists(stake_file):
                        with open(stake_file, 'r') as f:
                            stake = json.load(f)
                        
                        stake["released_at"] = current_time
                        stake["release_tx_hash"] = tx_hash
                        stake["status"] = "released"
                        
                        with open(stake_file, 'w') as f:
                            json.dump(stake, f, indent=2)
                    
                    logger.info(f"Released stake {stake_id} with tx {tx_hash}")
                    return {
                        "status": "success",
                        "stake_id": stake_id,
                        "address": self.address,
                        "release_tx_hash": tx_hash
                    }
                elif "error" in data:
                    logger.error(f"Stake release error: {data['error']}")
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Stake release request failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Stake release error: {e}")
            return {"status": "error", "message": str(e)}
    
    def pay_for_resource(self, resource_hash: str, usage: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send micropayment for server use.
        
        Args:
            resource_hash (str): Hash of the resource/agreement
            usage (dict): Usage metrics to pay for
            
        Returns:
            dict: Payment result with transaction hash
        """
        try:
            # Check if we have a wallet address
            if not self.address:
                return {
                    "status": "error", 
                    "message": "No wallet address. Load or create a wallet first."
                }
            
            # Calculate payment amount based on usage
            # This is a simplified calculation - in reality, this would depend on resource rates
            cpu_amount = usage.get("cpu_seconds", 0) * 0.0001
            memory_amount = usage.get("memory_mb_seconds", 0) * 0.000001
            network_amount = usage.get("network_bytes", 0) * 0.0000000001
            
            total_amount = cpu_amount + memory_amount + network_amount
            if total_amount < 0.0001:  # Minimum payment amount
                total_amount = 0.0001
            
            # Convert amount to wei (1 MNT = 10^18 wei)
            amount_wei = int(total_amount * 1e18)
            amount_hex = hex(amount_wei)
            
            # Create payment data
            timestamp = int(time.time())
            payment_data = {
                "resource_hash": resource_hash,
                "usage": usage,
                "amount": total_amount,
                "timestamp": timestamp
            }
            
            payment_data_hex = "0x" + json.dumps(payment_data).encode().hex()
            
            # Send payment transaction
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "metanode_payForResource",
                    "params": [{
                        "from": self.address,
                        "resourceHash": resource_hash,
                        "value": amount_hex,
                        "data": payment_data_hex
                    }],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    tx_hash = data["result"]
                    
                    # Save payment information
                    payment = {
                        "from": self.address,
                        "resource_hash": resource_hash,
                        "usage": usage,
                        "amount": total_amount,
                        "timestamp": timestamp,
                        "tx_hash": tx_hash
                    }
                    
                    payments_dir = os.path.join(self.wallet_dir, "payments")
                    os.makedirs(payments_dir, exist_ok=True)
                    
                    payment_file = os.path.join(payments_dir, f"payment-{tx_hash}.json")
                    with open(payment_file, 'w') as f:
                        json.dump(payment, f, indent=2)
                    
                    logger.info(f"Paid {total_amount} MNT for resource {resource_hash} with tx {tx_hash}")
                    return {
                        "status": "success",
                        "resource_hash": resource_hash,
                        "amount": total_amount,
                        "tx_hash": tx_hash,
                        "payment_file": payment_file
                    }
                elif "error" in data:
                    logger.error(f"Payment error: {data['error']}")
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Payment request failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Payment error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_stakes(self) -> Dict[str, Any]:
        """
        Get list of active and past stakes.
        
        Returns:
            dict: Stake information
        """
        try:
            # Check if we have a wallet address
            if not self.address:
                return {
                    "status": "error", 
                    "message": "No wallet address. Load or create a wallet first."
                }
            
            # Query blockchain for stakes
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "metanode_getStakes",
                    "params": [self.address],
                    "id": 1
                }
            )
            
            # Also check local stake files
            local_stakes = []
            stakes_dir = os.path.join(self.wallet_dir, "stakes")
            if os.path.exists(stakes_dir):
                stake_files = [f for f in os.listdir(stakes_dir) if f.startswith("stake-") and f.endswith(".json")]
                for file_name in stake_files:
                    try:
                        with open(os.path.join(stakes_dir, file_name), 'r') as f:
                            stake = json.load(f)
                            local_stakes.append(stake)
                    except Exception as e:
                        logger.warning(f"Error loading stake file {file_name}: {e}")
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    chain_stakes = data["result"]
                    
                    # Merge chain and local stakes
                    all_stakes = {}
                    for stake in chain_stakes:
                        stake_id = stake.get("stakeId")
                        if stake_id:
                            all_stakes[stake_id] = stake
                    
                    for stake in local_stakes:
                        stake_id = stake.get("stake_id")
                        if stake_id and stake_id not in all_stakes:
                            all_stakes[stake_id] = stake
                    
                    # Convert to list
                    stakes_list = list(all_stakes.values())
                    
                    # Save combined stakes
                    stakes_file = os.path.join(self.wallet_dir, f"stakes-{self.address}.json")
                    with open(stakes_file, 'w') as f:
                        json.dump({"stakes": stakes_list, "updated_at": int(time.time())}, f, indent=2)
                    
                    logger.info(f"Retrieved {len(stakes_list)} stakes for {self.address}")
                    return {
                        "status": "success",
                        "address": self.address,
                        "stakes": stakes_list,
                        "count": len(stakes_list),
                        "stakes_file": stakes_file
                    }
                elif "error" in data:
                    logger.error(f"Stakes query error: {data['error']}")
                    # Return local stakes if available
                    if local_stakes:
                        logger.info(f"Using {len(local_stakes)} local stakes")
                        return {
                            "status": "partial",
                            "message": str(data["error"]),
                            "address": self.address,
                            "stakes": local_stakes,
                            "count": len(local_stakes)
                        }
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Stakes query failed: {response.text}")
                # Return local stakes if available
                if local_stakes:
                    logger.info(f"Using {len(local_stakes)} local stakes")
                    return {
                        "status": "partial",
                        "message": response.text,
                        "address": self.address,
                        "stakes": local_stakes,
                        "count": len(local_stakes)
                    }
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Stakes query error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create escrow manager with wallet address
    escrow = Escrow(address="0xSampleWalletAddress")
    
    # Stake for mining
    stake_result = escrow.stake_for_mining(10.0, 86400)  # 10 MNT for 1 day
    print(f"Stake result: {json.dumps(stake_result, indent=2)}")
    
    # Pay for resource usage
    usage = {
        "cpu_seconds": 1000,
        "memory_mb_seconds": 50000,
        "network_bytes": 1000000
    }
    
    payment_result = escrow.pay_for_resource("0xResourceHash123", usage)
    print(f"Payment result: {json.dumps(payment_result, indent=2)}")
    
    # Get stakes
    stakes_result = escrow.get_stakes()
    print(f"Stakes: {json.dumps(stakes_result, indent=2)}")
    
    # Release stake
    release_result = escrow.release_stake(stake_result["stake_id"])
    print(f"Release result: {json.dumps(release_result, indent=2)}")
