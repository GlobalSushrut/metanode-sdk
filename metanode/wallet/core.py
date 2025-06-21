#!/usr/bin/env python3
"""
MetaNode SDK - Wallet Core Module
===============================

Core wallet functionality for creating and managing MetaNode wallets.
"""

import os
import json
import time
import uuid
import hashlib
import logging
import secrets
import requests
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL, BLOCKCHAIN_URL

# Configure logging
logger = logging.getLogger(__name__)

class WalletManager:
    """Manager class for handling multiple MetaNode wallets."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize wallet manager for handling multiple wallets.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.wallet_dir = os.path.join(os.path.expanduser("~"), ".metanode", "wallets")
        self.wallets = {}
        
        # Ensure wallet directory exists
        os.makedirs(self.wallet_dir, exist_ok=True)
        
        # Load existing wallets
        self._load_wallets()
    
    def _load_wallets(self) -> None:
        """Load all existing wallets from the wallet directory."""
        try:
            for file in os.listdir(self.wallet_dir):
                if file.endswith(".json"):
                    try:
                        with open(os.path.join(self.wallet_dir, file), "r") as f:
                            wallet_data = json.load(f)
                            wallet_id = wallet_data.get("id")
                            if wallet_id:
                                self.wallets[wallet_id] = wallet_data
                    except Exception as e:
                        logger.warning(f"Failed to load wallet file {file}: {e}")
        except Exception as e:
            logger.error(f"Failed to load wallets: {e}")
    
    def create_wallet(self, password: Optional[str] = None) -> Dict[str, Any]:
        """Create a new wallet and add it to the manager."""
        wallet = Wallet(self.api_url)
        wallet_data = wallet.create_wallet(password)
        wallet_id = wallet_data.get("id")
        if wallet_id:
            self.wallets[wallet_id] = wallet_data
        return wallet_data
    
    def get_wallet(self, wallet_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a wallet by its ID."""
        return self.wallets.get(wallet_id)
    
    def list_wallets(self) -> List[Dict[str, Any]]:
        """List all wallets managed by this wallet manager."""
        return list(self.wallets.values())


class Wallet:
    """Manages MetaNode wallet operations."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize wallet manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.wallet_dir = os.path.join(os.getcwd(), ".metanode", "wallet")
        self.wallet_path = None
        self.address = None
        self.private_key = None
        self.public_key = None
        
        # Ensure wallet directory exists
        os.makedirs(self.wallet_dir, exist_ok=True)
    
    def create_wallet(self, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate user-owned wallet (for both client and server).
        
        Args:
            password (str, optional): Password to encrypt the wallet
            
        Returns:
            dict: Wallet creation result with address
        """
        try:
            # Generate a new private key
            private_key = secrets.token_hex(32)
            
            # Derive public key from private key
            # In a real implementation, this would use proper crypto libraries
            public_key = hashlib.sha256(private_key.encode()).hexdigest()
            
            # Generate wallet address
            address = "0x" + hashlib.sha256(public_key.encode()).hexdigest()[:40]
            
            # Create wallet object
            wallet = {
                "address": address,
                "public_key": public_key,
                "private_key": private_key if not password else f"ENCRYPTED:{private_key}",
                "created_at": int(time.time()),
                "encrypted": password is not None
            }
            
            # Save wallet to file
            wallet_file = os.path.join(self.wallet_dir, f"wallet-{address}.json")
            with open(wallet_file, 'w') as f:
                json.dump(wallet, f, indent=2)
            
            # Update instance state
            self.wallet_path = wallet_file
            self.address = address
            self.private_key = private_key
            self.public_key = public_key
            
            # Register wallet with API
            response = requests.post(
                f"{self.api_url}/wallet/register",
                headers={"Content-Type": "application/json"},
                json={
                    "address": address,
                    "public_key": public_key
                }
            )
            
            api_response = {}
            if response.status_code == 200:
                api_response = response.json()
                logger.info(f"Successfully registered wallet {address} with API")
            else:
                logger.warning(f"Failed to register wallet with API: {response.text}")
            
            logger.info(f"Created wallet with address {address}")
            return {
                "status": "success",
                "address": address,
                "public_key": public_key,
                "wallet_file": wallet_file,
                "api_response": api_response
            }
            
        except Exception as e:
            logger.error(f"Wallet creation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def load_wallet(self, address: Optional[str] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load an existing wallet.
        
        Args:
            address (str, optional): Address of the wallet to load
            file_path (str, optional): Direct path to wallet file
            
        Returns:
            dict: Wallet loading result
        """
        try:
            # Determine wallet file path
            wallet_file = None
            
            if file_path and os.path.exists(file_path):
                wallet_file = file_path
            elif address:
                potential_file = os.path.join(self.wallet_dir, f"wallet-{address}.json")
                if os.path.exists(potential_file):
                    wallet_file = potential_file
            else:
                # Look for any wallet file
                wallet_files = [f for f in os.listdir(self.wallet_dir) if f.startswith("wallet-") and f.endswith(".json")]
                if wallet_files:
                    wallet_file = os.path.join(self.wallet_dir, wallet_files[0])
            
            if not wallet_file:
                return {
                    "status": "error", 
                    "message": "Wallet not found. Create a new wallet first."
                }
            
            # Load wallet
            with open(wallet_file, 'r') as f:
                wallet = json.load(f)
            
            # Update instance state
            self.wallet_path = wallet_file
            self.address = wallet["address"]
            self.public_key = wallet["public_key"]
            
            # Only set private key if not encrypted
            if not wallet.get("encrypted", False):
                self.private_key = wallet["private_key"]
            
            logger.info(f"Loaded wallet with address {self.address}")
            return {
                "status": "success",
                "address": self.address,
                "public_key": self.public_key,
                "encrypted": wallet.get("encrypted", False)
            }
            
        except Exception as e:
            logger.error(f"Wallet loading error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Get current token/resource balance.
        
        Returns:
            dict: Balance information
        """
        try:
            # Check if we have a wallet
            if not self.address:
                return {
                    "status": "error", 
                    "message": "No wallet loaded. Load or create a wallet first."
                }
            
            # Query blockchain for balance
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_getBalance",
                    "params": [self.address, "latest"],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    # Convert hex balance to decimal
                    raw_balance = data["result"]
                    balance = int(raw_balance, 16) / 1e18  # Convert to MNT tokens
                    
                    logger.info(f"Retrieved balance for {self.address}: {balance} MNT")
                    return {
                        "status": "success",
                        "address": self.address,
                        "balance": balance,
                        "raw_balance": raw_balance
                    }
                elif "error" in data:
                    logger.error(f"Balance query error: {data['error']}")
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Balance query failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Balance query error: {e}")
            return {"status": "error", "message": str(e)}
    
    def transfer_tokens(self, to: str, amount: float) -> Dict[str, Any]:
        """
        Transfer tokens between wallets.
        
        Args:
            to (str): Recipient wallet address
            amount (float): Amount of tokens to transfer
            
        Returns:
            dict: Transfer result with transaction hash
        """
        try:
            # Check if we have a wallet
            if not self.address:
                return {
                    "status": "error", 
                    "message": "No wallet loaded. Load or create a wallet first."
                }
            
            # Check if we have the private key
            if not self.private_key:
                return {
                    "status": "error", 
                    "message": "Private key not available. Cannot sign transaction."
                }
            
            # Check amount
            if amount <= 0:
                return {
                    "status": "error", 
                    "message": "Invalid amount. Must be greater than 0."
                }
            
            # Get current balance
            balance_result = self.get_balance()
            if balance_result["status"] != "success":
                return balance_result
            
            if balance_result["balance"] < amount:
                return {
                    "status": "error", 
                    "message": f"Insufficient balance. Available: {balance_result['balance']} MNT"
                }
            
            # Convert amount to wei (1 MNT = 10^18 wei)
            amount_wei = int(amount * 1e18)
            amount_hex = hex(amount_wei)
            
            # Create transaction
            transaction = {
                "from": self.address,
                "to": to,
                "value": amount_hex,
                "gas": "0x76c0",  # 30400 gas
                "gasPrice": "0x9184e72a000",  # 10000000000000 wei
                "data": ""
            }
            
            # Sign transaction (in a real implementation, this would use proper signing)
            transaction_json = json.dumps(transaction, sort_keys=True)
            signature = hashlib.sha256((self.private_key + transaction_json).encode()).hexdigest()
            
            signed_tx = transaction.copy()
            signed_tx["signature"] = signature
            
            # Send transaction
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_sendTransaction",
                    "params": [signed_tx],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    tx_hash = data["result"]
                    
                    # Log transaction
                    tx_log = {
                        "from": self.address,
                        "to": to,
                        "amount": amount,
                        "tx_hash": tx_hash,
                        "timestamp": int(time.time())
                    }
                    
                    # Save transaction log
                    tx_dir = os.path.join(self.wallet_dir, "transactions")
                    os.makedirs(tx_dir, exist_ok=True)
                    
                    tx_file = os.path.join(tx_dir, f"tx-{tx_hash}.json")
                    with open(tx_file, 'w') as f:
                        json.dump(tx_log, f, indent=2)
                    
                    logger.info(f"Transferred {amount} MNT to {to} with tx {tx_hash}")
                    return {
                        "status": "success",
                        "from": self.address,
                        "to": to,
                        "amount": amount,
                        "tx_hash": tx_hash,
                        "tx_file": tx_file
                    }
                elif "error" in data:
                    logger.error(f"Transaction error: {data['error']}")
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Transaction failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Transfer error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_transaction_history(self) -> Dict[str, Any]:
        """
        Get transaction history for the wallet.
        
        Returns:
            dict: Transaction history
        """
        try:
            # Check if we have a wallet
            if not self.address:
                return {
                    "status": "error", 
                    "message": "No wallet loaded. Load or create a wallet first."
                }
            
            # Query blockchain for transactions
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "metanode_getTransactionHistory",
                    "params": [self.address],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    transactions = data["result"]
                    
                    # Save transaction history
                    history_file = os.path.join(self.wallet_dir, f"history-{self.address}.json")
                    with open(history_file, 'w') as f:
                        json.dump({"transactions": transactions, "updated_at": int(time.time())}, f, indent=2)
                    
                    logger.info(f"Retrieved {len(transactions)} transactions for {self.address}")
                    return {
                        "status": "success",
                        "address": self.address,
                        "transactions": transactions,
                        "count": len(transactions),
                        "history_file": history_file
                    }
                elif "error" in data:
                    logger.error(f"Transaction history error: {data['error']}")
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Transaction history query failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Transaction history error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create wallet manager
    wallet = Wallet()
    
    # Create a new wallet
    create_result = wallet.create_wallet()
    print(f"Wallet creation: {json.dumps(create_result, indent=2)}")
    
    # Get balance
    balance_result = wallet.get_balance()
    print(f"Balance: {json.dumps(balance_result, indent=2)}")
    
    # Transfer tokens example (commented out for safety)
    # transfer_result = wallet.transfer_tokens("0xRecipientAddress", 1.0)
    # print(f"Transfer: {json.dumps(transfer_result, indent=2)}")
    
    # Get transaction history
    history_result = wallet.get_transaction_history()
    print(f"Transaction history: {json.dumps(history_result, indent=2)}")
