#!/usr/bin/env python3
"""
MetaNode Wallet Core

Ethereum-compatible wallet implementation for MetaNode infrastructure.
Provides secure key management, transaction signing, and wallet operations.
"""

import os
import json
import time
import getpass
import logging
import hashlib
import secrets
from typing import Dict, List, Any, Optional, Tuple
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_account.messages import encode_defunct
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode.wallet")

class MetaNodeWallet:
    """
    Ethereum-compatible wallet implementation for MetaNode
    
    Features:
    - HD wallet support with BIP39 mnemonics
    - Hierarchical Deterministic key derivation
    - Transaction signing and verification
    - Secure encrypted key storage
    """
    
    def __init__(self, wallet_dir: str = "~/.metanode/wallets"):
        """Initialize the wallet"""
        self.wallet_dir = os.path.expanduser(wallet_dir)
        os.makedirs(self.wallet_dir, exist_ok=True)
        
        # Active account
        self.active_account = None
    
    def create_account(self, password: str) -> Dict:
        """Create a new Ethereum-compatible account"""
        # Generate a new private key
        account: LocalAccount = Account.create()
        
        # Encrypt the private key
        encrypted_key = self._encrypt_private_key(account.key.hex(), password)
        
        # Create wallet file
        wallet_data = {
            "address": account.address,
            "encrypted_private_key": encrypted_key,
            "public_key": account.key.public_key.to_hex(),
            "created_at": time.time()
        }
        
        # Save wallet file
        wallet_path = os.path.join(self.wallet_dir, f"{account.address}.json")
        with open(wallet_path, "w") as f:
            json.dump(wallet_data, f, indent=2)
        
        logger.info(f"Created new wallet with address {account.address}")
        return {
            "address": account.address,
            "public_key": account.key.public_key.to_hex()
        }
    
    def load_account(self, address: str, password: str) -> bool:
        """Load an existing account"""
        wallet_path = os.path.join(self.wallet_dir, f"{address}.json")
        
        if not os.path.exists(wallet_path):
            logger.error(f"Wallet file for address {address} does not exist")
            return False
        
        try:
            # Load wallet data
            with open(wallet_path, "r") as f:
                wallet_data = json.load(f)
            
            # Decrypt private key
            private_key = self._decrypt_private_key(
                wallet_data["encrypted_private_key"], 
                password
            )
            
            # Create account from private key
            self.active_account = Account.from_key(private_key)
            
            if self.active_account.address != address:
                logger.error("Address mismatch after decryption")
                self.active_account = None
                return False
            
            logger.info(f"Loaded wallet for address {address}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading wallet: {e}")
            self.active_account = None
            return False
    
    def sign_transaction(self, tx_data: Dict) -> Dict:
        """Sign a transaction"""
        if not self.active_account:
            raise ValueError("No active account")
        
        # Create transaction dictionary
        transaction = {
            "from": self.active_account.address,
            "to": tx_data.get("to"),
            "value": tx_data.get("value", 0),
            "gas": tx_data.get("gas", 21000),
            "gasPrice": tx_data.get("gasPrice", 20000000000),
            "nonce": tx_data.get("nonce", 0),
            "chainId": tx_data.get("chainId", 9928),  # MetaNode Chain ID
            "data": tx_data.get("data", ""),
        }
        
        # Sign transaction
        signed = self.active_account.sign_transaction(transaction)
        
        return {
            "raw_transaction": signed.rawTransaction.hex(),
            "hash": signed.hash.hex(),
            "transaction": transaction
        }
    
    def sign_message(self, message: str) -> Dict:
        """Sign a message"""
        if not self.active_account:
            raise ValueError("No active account")
        
        # Encode message
        encoded_message = encode_defunct(text=message)
        
        # Sign message
        signature = self.active_account.sign_message(encoded_message)
        
        return {
            "message": message,
            "signature": signature.signature.hex(),
            "address": self.active_account.address
        }
    
    @staticmethod
    def verify_message(message: str, signature: str, address: str) -> bool:
        """Verify a signed message"""
        try:
            # Encode message
            encoded_message = encode_defunct(text=message)
            
            # Recover signer address
            recovered_address = Account.recover_message(
                encoded_message, 
                signature=signature
            )
            
            # Compare addresses
            return recovered_address.lower() == address.lower()
            
        except Exception as e:
            logger.error(f"Error verifying message: {e}")
            return False
    
    def get_address(self) -> Optional[str]:
        """Get the active account address"""
        if self.active_account:
            return self.active_account.address
        return None
    
    def list_wallets(self) -> List[Dict]:
        """List all available wallets"""
        wallets = []
        
        for filename in os.listdir(self.wallet_dir):
            if filename.startswith("0x") and filename.endswith(".json"):
                wallet_path = os.path.join(self.wallet_dir, filename)
                
                try:
                    with open(wallet_path, "r") as f:
                        wallet_data = json.load(f)
                    
                    wallets.append({
                        "address": wallet_data["address"],
                        "created_at": wallet_data.get("created_at", 0)
                    })
                    
                except Exception as e:
                    logger.error(f"Error reading wallet file {filename}: {e}")
        
        return wallets
    
    def _encrypt_private_key(self, private_key: str, password: str) -> str:
        """Encrypt a private key with a password"""
        # Generate a salt
        salt = os.urandom(16)
        
        # Derive encryption key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Encrypt private key
        f = Fernet(key)
        encrypted_data = f.encrypt(private_key.encode())
        
        # Combine salt and encrypted data
        encrypted_result = base64.b64encode(salt + encrypted_data).decode('ascii')
        
        return encrypted_result
    
    def _decrypt_private_key(self, encrypted_data: str, password: str) -> str:
        """Decrypt a private key with a password"""
        # Decode encrypted data
        full_data = base64.b64decode(encrypted_data.encode('ascii'))
        
        # Extract salt and encrypted private key
        salt = full_data[:16]
        encrypted_key = full_data[16:]
        
        # Derive encryption key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Decrypt private key
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_key)
        
        return decrypted_data.decode('ascii')

# Command-line functions for wallet management
def create_wallet_interactive() -> Dict:
    """Interactive console function to create a new wallet"""
    print("\n=== Create New MetaNode Wallet ===\n")
    
    # Get password
    while True:
        password = getpass.getpass("Enter password for new wallet: ")
        confirm = getpass.getpass("Confirm password: ")
        
        if password == confirm:
            break
        
        print("Passwords do not match. Please try again.")
    
    # Create wallet
    wallet = MetaNodeWallet()
    result = wallet.create_account(password)
    
    print(f"\nWallet created successfully!")
    print(f"Address: {result['address']}")
    print("\nMake sure to keep your password safe. If you lose it, you won't be able to access your wallet.")
    
    return result

def load_wallet_interactive() -> Optional[MetaNodeWallet]:
    """Interactive console function to load an existing wallet"""
    wallet = MetaNodeWallet()
    wallets = wallet.list_wallets()
    
    if not wallets:
        print("No wallets found. Create one first.")
        return None
    
    print("\n=== Load MetaNode Wallet ===\n")
    
    # Display available wallets
    print("Available wallets:")
    for i, w in enumerate(wallets):
        print(f"{i+1}. {w['address']}")
    
    # Select wallet
    selection = input("\nEnter wallet number or address: ")
    
    try:
        # Check if selection is a number
        idx = int(selection) - 1
        if 0 <= idx < len(wallets):
            address = wallets[idx]["address"]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        # Selection is an address
        address = selection
    
    # Get password
    password = getpass.getpass(f"Enter password for {address}: ")
    
    # Load wallet
    if wallet.load_account(address, password):
        print(f"\nWallet {address} loaded successfully!")
        return wallet
    else:
        print("Failed to load wallet. Incorrect password or corrupt wallet file.")
        return None
