#!/usr/bin/env python3
"""
MetaNode Wallet CLI

Console-based wallet management for MetaNode blockchain infrastructure.
Provides secure key management, transaction signing, and balance tracking.
"""

import os
import sys
import json
import time
import uuid
import typer
import getpass
import logging
from typing import Dict, Optional
from rich.console import Console
from rich.table import Table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode.wallet.cli")

# Create Typer app
app = typer.Typer(help="MetaNode Wallet - Blockchain Security")

# Rich console for pretty output
console = Console()

# Configuration paths
WALLET_DIR = os.path.expanduser("~/.metanode/wallets")
os.makedirs(WALLET_DIR, exist_ok=True)

class WalletManager:
    """Manages MetaNode wallets securely through the console"""
    
    def __init__(self, wallet_dir: str = WALLET_DIR):
        """Initialize wallet manager"""
        self.wallet_dir = wallet_dir
        self.active_wallet = None
        self.active_wallet_data = None
    
    def create_wallet(self, password: str) -> Dict:
        """Create a new wallet"""
        # Generate wallet ID
        wallet_id = f"wallet_{uuid.uuid4().hex[:8]}"
        
        # Generate simulated key pair (in a real implementation, use cryptographic keys)
        public_key = f"mpk_{uuid.uuid4().hex}"
        private_key = f"msk_{uuid.uuid4().hex}"
        
        # "Encrypt" private key (simplified for demo)
        # In production, use proper encryption
        encrypted_key = f"encrypted_{private_key}_{password}"
        
        # Create wallet data
        wallet_data = {
            "wallet_id": wallet_id,
            "public_key": public_key,
            "encrypted_private_key": encrypted_key,
            "created_at": time.time(),
            "balance": 100.0,  # Initial balance for demo
            "transaction_history": []
        }
        
        # Save wallet
        wallet_path = os.path.join(self.wallet_dir, f"{wallet_id}.json")
        with open(wallet_path, 'w') as f:
            json.dump(wallet_data, f, indent=2)
        
        logger.info(f"Created wallet {wallet_id}")
        return {
            "wallet_id": wallet_id,
            "public_key": public_key
        }
    
    def list_wallets(self) -> list:
        """List all available wallets"""
        wallets = []
        
        for filename in os.listdir(self.wallet_dir):
            if filename.startswith("wallet_") and filename.endswith(".json"):
                wallet_path = os.path.join(self.wallet_dir, filename)
                
                try:
                    with open(wallet_path, 'r') as f:
                        wallet_data = json.load(f)
                    
                    wallets.append({
                        "wallet_id": wallet_data["wallet_id"],
                        "public_key": wallet_data["public_key"],
                        "created_at": wallet_data["created_at"],
                        "balance": wallet_data.get("balance", 0.0)
                    })
                    
                except Exception as e:
                    logger.error(f"Error reading wallet {filename}: {e}")
        
        return wallets
    
    def load_wallet(self, wallet_id: str, password: str) -> bool:
        """Load a wallet by ID and password"""
        wallet_path = os.path.join(self.wallet_dir, f"{wallet_id}.json")
        
        if not os.path.exists(wallet_path):
            logger.error(f"Wallet not found: {wallet_id}")
            return False
        
        try:
            with open(wallet_path, 'r') as f:
                wallet_data = json.load(f)
            
            # Simplified authentication check
            # In production, use proper decryption and validation
            encrypted_key = wallet_data["encrypted_private_key"]
            if not encrypted_key.startswith(f"encrypted_msk_") or not encrypted_key.endswith(f"_{password}"):
                logger.error("Invalid password")
                return False
            
            self.active_wallet = wallet_id
            self.active_wallet_data = wallet_data
            logger.info(f"Loaded wallet {wallet_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading wallet: {e}")
            return False
    
    def get_balance(self) -> float:
        """Get balance of active wallet"""
        if not self.active_wallet_data:
            raise ValueError("No active wallet")
        
        return self.active_wallet_data.get("balance", 0.0)
    
    def transfer(self, recipient_id: str, amount: float) -> Dict:
        """Transfer tokens to another wallet"""
        if not self.active_wallet_data:
            raise ValueError("No active wallet")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if amount > self.active_wallet_data.get("balance", 0.0):
            raise ValueError("Insufficient balance")
        
        # Check if recipient exists
        recipient_path = os.path.join(self.wallet_dir, f"{recipient_id}.json")
        if not os.path.exists(recipient_path):
            raise ValueError(f"Recipient wallet not found: {recipient_id}")
        
        # Load recipient wallet
        with open(recipient_path, 'r') as f:
            recipient_data = json.load(f)
        
        # Create transaction
        tx_id = f"tx_{uuid.uuid4().hex[:12]}"
        tx_data = {
            "tx_id": tx_id,
            "sender": self.active_wallet,
            "recipient": recipient_id,
            "amount": amount,
            "timestamp": time.time()
        }
        
        # Update sender balance
        self.active_wallet_data["balance"] -= amount
        self.active_wallet_data["transaction_history"].append(tx_data)
        
        # Update recipient balance
        recipient_data["balance"] = recipient_data.get("balance", 0.0) + amount
        recipient_data["transaction_history"] = recipient_data.get("transaction_history", [])
        recipient_data["transaction_history"].append(tx_data)
        
        # Save wallets
        with open(os.path.join(self.wallet_dir, f"{self.active_wallet}.json"), 'w') as f:
            json.dump(self.active_wallet_data, f, indent=2)
        
        with open(recipient_path, 'w') as f:
            json.dump(recipient_data, f, indent=2)
        
        logger.info(f"Transferred {amount} tokens from {self.active_wallet} to {recipient_id}")
        return tx_data

# Global wallet manager instance
wallet_manager = WalletManager()

@app.command()
def create():
    """Create a new MetaNode wallet"""
    console.print("[bold blue]Creating New MetaNode Wallet[/]")
    
    # Get password
    password = typer.prompt("Enter wallet password", hide_input=True)
    confirm = typer.prompt("Confirm password", hide_input=True)
    
    if password != confirm:
        console.print("[red]Passwords do not match[/]")
        return
    
    # Create wallet
    try:
        wallet_info = wallet_manager.create_wallet(password)
        console.print("[green]✓[/] Wallet created successfully!")
        console.print(f"[bold]Wallet ID:[/] {wallet_info['wallet_id']}")
        console.print(f"[bold]Public Key:[/] {wallet_info['public_key']}")
        console.print("\n[yellow]Keep your password safe. If lost, you cannot recover your wallet.[/]")
    except Exception as e:
        console.print(f"[red]Error creating wallet: {e}[/]")

@app.command()
def list():
    """List all available wallets"""
    wallets = wallet_manager.list_wallets()
    
    if not wallets:
        console.print("[yellow]No wallets found[/]")
        return
    
    # Display wallets table
    table = Table(title="MetaNode Wallets")
    table.add_column("Wallet ID")
    table.add_column("Public Key")
    table.add_column("Balance")
    table.add_column("Created At")
    
    for wallet in wallets:
        table.add_row(
            wallet["wallet_id"],
            wallet["public_key"],
            f"{wallet['balance']:.2f} MNT",
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(wallet["created_at"]))
        )
    
    console.print(table)

@app.command()
def load(wallet_id: str):
    """Load a wallet and use it for operations"""
    password = typer.prompt("Enter wallet password", hide_input=True)
    
    try:
        if wallet_manager.load_wallet(wallet_id, password):
            balance = wallet_manager.get_balance()
            console.print("[green]✓[/] Wallet loaded successfully!")
            console.print(f"[bold]Wallet ID:[/] {wallet_id}")
            console.print(f"[bold]Balance:[/] {balance:.2f} MNT")
        else:
            console.print("[red]Failed to load wallet. Check ID and password.[/]")
    except Exception as e:
        console.print(f"[red]Error loading wallet: {e}[/]")

@app.command()
def balance():
    """Check balance of loaded wallet"""
    try:
        balance = wallet_manager.get_balance()
        console.print(f"[bold]Current Balance:[/] {balance:.2f} MNT")
    except ValueError:
        console.print("[red]No wallet loaded. Use 'metanode-wallet load' first.[/]")
    except Exception as e:
        console.print(f"[red]Error checking balance: {e}[/]")

@app.command()
def transfer(recipient: str, amount: float):
    """Transfer tokens to another wallet"""
    try:
        tx = wallet_manager.transfer(recipient, amount)
        console.print("[green]✓[/] Transfer successful!")
        console.print(f"[bold]Transaction ID:[/] {tx['tx_id']}")
        console.print(f"[bold]Amount:[/] {amount:.2f} MNT")
        console.print(f"[bold]Recipient:[/] {recipient}")
        console.print(f"[bold]New Balance:[/] {wallet_manager.get_balance():.2f} MNT")
    except ValueError as e:
        console.print(f"[red]Transfer failed: {e}[/]")
    except Exception as e:
        console.print(f"[red]Error during transfer: {e}[/]")

def main():
    """Main entry point for the wallet CLI"""
    try:
        app()
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
        sys.exit(1)

if __name__ == "__main__":
    main()
