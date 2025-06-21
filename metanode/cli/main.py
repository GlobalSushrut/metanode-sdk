#!/usr/bin/env python3
"""
MetaNode SDK - Command Line Interface
==================================

Main CLI entry point for MetaNode SDK.
"""

import os
import sys
import json
import time
import logging
import typer
from typing import Optional, List

from ..wallet.core import WalletManager
from ..wallet.escrow import EscrowManager
from ..ledger.proof_log import ProofLogger
from ..ledger.verification import Verifier
from ..admin.node_manager import NodeManager
from ..admin.vpod_tools import VPodManager
from ..admin.security import SecurityManager
from ..admin.k8s_manager import K8sManager
from ..utils.zk_proofs import ZKProofManager
from ..utils.ipfs_tools import IPFSManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("metanode-cli")

# Create Typer app
app = typer.Typer(help="MetaNode SDK - Command Line Tools")

# Create sub-commands for different modules
wallet_app = typer.Typer(help="Wallet management commands")
escrow_app = typer.Typer(help="Escrow and staking commands")
ledger_app = typer.Typer(help="Ledger and proof commands")
admin_app = typer.Typer(help="Admin commands")
k8s_app = typer.Typer(help="Kubernetes commands")
utils_app = typer.Typer(help="Utility commands")

# Add subcommands to main app
app.add_typer(wallet_app, name="wallet")
app.add_typer(escrow_app, name="escrow")
app.add_typer(ledger_app, name="ledger")
app.add_typer(admin_app, name="admin")
app.add_typer(utils_app, name="utils")

# Add Kubernetes subcommand to admin app
admin_app.add_typer(k8s_app, name="k8s")

# Global options
class GlobalOptions:
    api_url: Optional[str] = None
    admin_key: Optional[str] = None

global_options = GlobalOptions()

# Wallet commands
@wallet_app.command("create")
def wallet_create(
    name: str = typer.Option(..., help="Name for the wallet"),
    password: str = typer.Option(..., help="Wallet password", prompt=True, hide_input=True)
):
    """Create a new wallet"""
    wallet_manager = WalletManager()
    result = wallet_manager.create_wallet(name, password)
    if result["status"] == "success":
        typer.echo(f"Created wallet: {name}")
        typer.echo(f"Address: {result['address']}")
        typer.echo(f"Please keep your mnemonic phrase in a safe place: {result['mnemonic']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

@wallet_app.command("balance")
def wallet_balance(
    name: str = typer.Option(..., help="Name of the wallet"),
    password: str = typer.Option(..., help="Wallet password", prompt=True, hide_input=True)
):
    """Get wallet balance"""
    wallet_manager = WalletManager()
    loaded = wallet_manager.load_wallet(name, password)
    
    if loaded["status"] == "success":
        result = wallet_manager.get_balance()
        if result["status"] == "success":
            typer.echo(f"Wallet: {name}")
            typer.echo(f"Address: {loaded['address']}")
            typer.echo(f"Balance: {result['balance']} MTC")
        else:
            typer.echo(f"Error: {result['message']}", err=True)
    else:
        typer.echo(f"Error: {loaded['message']}", err=True)

@wallet_app.command("transfer")
def wallet_transfer(
    name: str = typer.Option(..., help="Name of the wallet"),
    to_address: str = typer.Option(..., help="Recipient address"),
    amount: float = typer.Option(..., help="Amount to transfer"),
    password: str = typer.Option(..., help="Wallet password", prompt=True, hide_input=True)
):
    """Transfer tokens to another address"""
    wallet_manager = WalletManager()
    loaded = wallet_manager.load_wallet(name, password)
    
    if loaded["status"] == "success":
        result = wallet_manager.transfer(to_address, amount)
        if result["status"] == "success":
            typer.echo(f"Transfer successful!")
            typer.echo(f"Transaction ID: {result['transaction_id']}")
            typer.echo(f"From: {loaded['address']}")
            typer.echo(f"To: {to_address}")
            typer.echo(f"Amount: {amount} MTC")
        else:
            typer.echo(f"Error: {result['message']}", err=True)
    else:
        typer.echo(f"Error: {loaded['message']}", err=True)

# Escrow commands
@escrow_app.command("stake")
def escrow_stake(
    name: str = typer.Option(..., help="Name of the wallet"),
    amount: float = typer.Option(..., help="Amount to stake"),
    duration: int = typer.Option(30, help="Stake duration in days"),
    password: str = typer.Option(..., help="Wallet password", prompt=True, hide_input=True)
):
    """Stake tokens for mining eligibility"""
    wallet_manager = WalletManager()
    loaded = wallet_manager.load_wallet(name, password)
    
    if loaded["status"] == "success":
        escrow_manager = EscrowManager()
        result = escrow_manager.stake_for_mining(amount, duration)
        if result["status"] == "success":
            typer.echo(f"Staking successful!")
            typer.echo(f"Stake ID: {result['stake_id']}")
            typer.echo(f"Amount: {amount} MTC")
            typer.echo(f"Duration: {duration} days")
            typer.echo(f"Expiration: {result['expiration_time']}")
        else:
            typer.echo(f"Error: {result['message']}", err=True)
    else:
        typer.echo(f"Error: {loaded['message']}", err=True)

@escrow_app.command("release")
def escrow_release(
    name: str = typer.Option(..., help="Name of the wallet"),
    stake_id: str = typer.Option(..., help="ID of the stake to release"),
    password: str = typer.Option(..., help="Wallet password", prompt=True, hide_input=True)
):
    """Release staked tokens"""
    wallet_manager = WalletManager()
    loaded = wallet_manager.load_wallet(name, password)
    
    if loaded["status"] == "success":
        escrow_manager = EscrowManager()
        result = escrow_manager.release_stake(stake_id)
        if result["status"] == "success":
            typer.echo(f"Stake release successful!")
            typer.echo(f"Stake ID: {stake_id}")
            typer.echo(f"Released Amount: {result['released_amount']} MTC")
            typer.echo(f"Transaction ID: {result['transaction_id']}")
        else:
            typer.echo(f"Error: {result['message']}", err=True)
    else:
        typer.echo(f"Error: {loaded['message']}", err=True)

# Ledger commands
@ledger_app.command("log")
def ledger_log(
    message: str = typer.Option(..., help="Message to log"),
    agreement_id: Optional[str] = typer.Option(None, help="Agreement ID to associate with this log"),
    ipfs: bool = typer.Option(False, help="Submit to IPFS")
):
    """Create a proof log entry"""
    proof_logger = ProofLogger()
    result = proof_logger.create_proof_log(message, agreement_id)
    
    if result["status"] == "success":
        typer.echo(f"Proof log created!")
        typer.echo(f"Log ID: {result['log_id']}")
        
        if ipfs:
            ipfs_result = proof_logger.submit_to_ipfs(result['log_id'])
            if ipfs_result["status"] == "success":
                typer.echo(f"Log submitted to IPFS!")
                typer.echo(f"IPFS Hash: {ipfs_result['ipfs_hash']}")
            else:
                typer.echo(f"IPFS submission error: {ipfs_result['message']}", err=True)
    else:
        typer.echo(f"Error: {result['message']}", err=True)

@ledger_app.command("verify")
def ledger_verify(
    tx_id: str = typer.Option(..., help="Transaction ID to verify")
):
    """Verify a blockchain transaction"""
    verifier = Verifier()
    result = verifier.verify_transaction(tx_id)
    
    if result["status"] == "success":
        typer.echo(f"Verification successful!")
        typer.echo(f"Transaction: {tx_id}")
        typer.echo(f"Verified: {result['verified']}")
        typer.echo(f"Block: {result['block_number']}")
        typer.echo(f"Timestamp: {result['timestamp']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

# Admin node commands
@admin_app.command("list-nodes")
def admin_list_nodes(
    admin_key: str = typer.Option(..., help="Admin API key", envvar="METANODE_ADMIN_KEY")
):
    """List MetaNode testnet nodes"""
    node_manager = NodeManager(admin_key=admin_key)
    result = node_manager.list_nodes()
    
    if result["status"] == "success":
        typer.echo(f"Total nodes: {result['count']}")
        for node in result["nodes"]:
            typer.echo(f"- {node['node_id']}: {node['status']} ({node['node_type']})")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

@admin_app.command("restart-node")
def admin_restart_node(
    node_id: str = typer.Option(..., help="Node ID to restart"),
    admin_key: str = typer.Option(..., help="Admin API key", envvar="METANODE_ADMIN_KEY")
):
    """Restart a MetaNode testnet node"""
    node_manager = NodeManager(admin_key=admin_key)
    result = node_manager.restart_node(node_id)
    
    if result["status"] == "success":
        typer.echo(f"Node {node_id} restart initiated successfully")
        typer.echo(f"Operation ID: {result['operation_id']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

# K8s commands
@k8s_app.command("create-key")
def k8s_create_key():
    """Create a cryptographic key for secure node deployment"""
    k8s_manager = K8sManager()
    result = k8s_manager.generate_node_crypt_key()
    
    if result["status"] == "success":
        typer.echo(f"Generated cryptographic key!")
        typer.echo(f"Key ID: {result['key_id']}")
        typer.echo(f"Key Hash: {result['key_hash']}")
        typer.echo(f"Key saved to: {result['key_file']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

@k8s_app.command("register-node")
def k8s_register_node(
    node_name: str = typer.Option(..., help="Name of the Kubernetes node"),
    key_id: str = typer.Option(..., help="ID of the cryptographic key to use"),
    is_testnet: bool = typer.Option(True, help="Whether this node will serve as a testnet node"),
    admin_key: str = typer.Option(..., help="Admin API key", envvar="METANODE_ADMIN_KEY")
):
    """Register a Kubernetes node with MetaNode testnet"""
    k8s_manager = K8sManager(admin_key=admin_key)
    result = k8s_manager.register_node_with_testnet(node_name, key_id, is_testnet)
    
    if result["status"] == "success":
        typer.echo(f"Node {node_name} registered successfully!")
        typer.echo(f"Node ID: {result['node_id']}")
        typer.echo(f"Is testnet node: {result['is_testnet_node']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

@k8s_app.command("deploy-testnet")
def k8s_deploy_testnet(
    node_id: str = typer.Option(..., help="ID of the registered node"),
    node_name: str = typer.Option(..., help="Name of the Kubernetes node"),
    admin_key: str = typer.Option(..., help="Admin API key", envvar="METANODE_ADMIN_KEY")
):
    """Deploy testnet node to Kubernetes"""
    k8s_manager = K8sManager(admin_key=admin_key)
    result = k8s_manager.deploy_testnet_node(node_id, node_name)
    
    if result["status"] == "success":
        typer.echo(f"Testnet node deployed successfully!")
        typer.echo(f"Node ID: {result['node_id']}")
        typer.echo(f"Deployment name: {result['deployment_name']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

@k8s_app.command("setup-sync")
def k8s_setup_sync(
    admin_key: str = typer.Option(..., help="Admin API key", envvar="METANODE_ADMIN_KEY")
):
    """Set up testnet node synchronization"""
    k8s_manager = K8sManager(admin_key=admin_key)
    result = k8s_manager.setup_testnet_sync()
    
    if result["status"] == "success":
        typer.echo(f"Testnet sync setup complete!")
        typer.echo(f"Service name: {result['service_name']}")
        typer.echo(f"Config name: {result['config_name']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

# Utils commands
@utils_app.command("zk-proof")
def utils_zk_proof(
    data: str = typer.Option(..., help="Data to create proof for"),
    aggregation_id: str = typer.Option(..., help="Aggregation session ID")
):
    """Generate a zero-knowledge proof for secure aggregation"""
    zk_manager = ZKProofManager()
    # Convert string data to dict
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        data_dict = {"rawData": data}
        
    result = zk_manager.generate_secure_aggregation_proof(data_dict, aggregation_id)
    
    if result["status"] == "success":
        typer.echo(f"Generated zero-knowledge proof!")
        typer.echo(f"Proof ID: {result['proof_id']}")
        typer.echo(f"Aggregation ID: {result['aggregation_id']}")
        typer.echo(f"Data hash: {result['data_hash']}")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

@utils_app.command("ipfs-add")
def utils_ipfs_add(
    file_path: str = typer.Option(..., help="Path to file to add to IPFS")
):
    """Add a file to IPFS"""
    ipfs_manager = IPFSManager()
    result = ipfs_manager.add_file(file_path)
    
    if result["status"] == "success":
        typer.echo(f"File added to IPFS!")
        typer.echo(f"File: {result['file_name']}")
        typer.echo(f"IPFS Hash: {result['ipfs_hash']}")
        typer.echo(f"Size: {result['size']} bytes")
    else:
        typer.echo(f"Error: {result['message']}", err=True)

# Main app command
@app.callback()
def main(
    api_url: Optional[str] = typer.Option(None, help="API URL", envvar="METANODE_API_URL"),
    admin_key: Optional[str] = typer.Option(None, help="Admin API key", envvar="METANODE_ADMIN_KEY"),
    debug: bool = typer.Option(False, help="Enable debug logging")
):
    """
    MetaNode SDK Command Line Interface
    
    A comprehensive toolkit for interacting with the MetaNode testnet ecosystem.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Set global options
    global_options.api_url = api_url
    global_options.admin_key = admin_key

    # Print welcome message
    typer.echo("MetaNode SDK CLI - v1.0.0")
    typer.echo("===============================")


if __name__ == "__main__":
    app()
