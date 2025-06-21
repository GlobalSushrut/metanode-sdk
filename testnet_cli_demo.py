#!/usr/bin/env python3
"""
MetaNode CLI Integration with Testnet
====================================

This script demonstrates how to use the MetaNode SDK CLI to interact with the deployed testnet.
It provides a command-line interface for common operations like:
- Node registration
- Wallet management
- Escrow operations
- Ledger verification
"""

import os
import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import MetaNode SDK CLI module
from metanode.cli.app import app as cli_app
from metanode.config.endpoints import API_URL, BLOCKCHAIN_URL, VALIDATOR_URL
from metanode.wallet.core import WalletManager
from metanode.wallet.escrow import EscrowManager
from metanode.admin.k8s_manager import K8sManager
from metanode.ledger.verification import Verifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode-cli-demo")

class MetaNodeCLIDemo:
    """Demo class for interacting with the MetaNode testnet using CLI commands."""
    
    def __init__(self):
        """Initialize the CLI demo with configuration."""
        self.api_url = os.environ.get("METANODE_API_URL", API_URL)
        self.blockchain_url = os.environ.get("METANODE_BLOCKCHAIN_URL", BLOCKCHAIN_URL)
        self.validator_url = os.environ.get("METANODE_VALIDATOR_URL", VALIDATOR_URL)
        self.admin_key = os.environ.get("METANODE_ADMIN_KEY", "")
        
        # Initialize SDK components
        self.wallet_manager = WalletManager()
        self.escrow_manager = EscrowManager()
        self.k8s_manager = K8sManager()
        self.verifier = Verifier()
        
        # Set environment variables for CLI commands
        os.environ["METANODE_API_URL"] = self.api_url
        os.environ["METANODE_BLOCKCHAIN_URL"] = self.blockchain_url
        os.environ["METANODE_VALIDATOR_URL"] = self.validator_url
        
        logger.info(f"Initialized MetaNode CLI Demo with:")
        logger.info(f"  API URL: {self.api_url}")
        logger.info(f"  Blockchain URL: {self.blockchain_url}")
        logger.info(f"  Validator URL: {self.validator_url}")
    
    def run_cli_command(self, command: List[str]) -> str:
        """Run a MetaNode CLI command and return the output."""
        try:
            # Construct the full command with CLI prefix
            full_command = ["python", "-m", "metanode.cli"] + command
            logger.info(f"Running command: {' '.join(full_command)}")
            
            # Execute the command
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                logger.info("Command executed successfully")
                return result.stdout
            else:
                logger.error(f"Command failed with code {result.returncode}")
                logger.error(f"Error: {result.stderr}")
                return f"ERROR: {result.stderr}"
        
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return f"ERROR: {str(e)}"
    
    def list_available_commands(self) -> str:
        """List all available CLI commands."""
        return self.run_cli_command(["--help"])
    
    def wallet_commands_demo(self) -> Dict[str, Any]:
        """Demonstrate wallet management commands."""
        results = {
            "create_wallet": None,
            "list_wallets": None,
            "wallet_balance": None
        }
        
        # List existing wallets
        results["list_wallets"] = self.run_cli_command(["wallet", "list"])
        
        # Create a wallet if needed
        wallet_name = f"test-wallet-{os.urandom(4).hex()}"
        results["create_wallet"] = self.run_cli_command(["wallet", "create", wallet_name])
        
        # Get wallet balance
        results["wallet_balance"] = self.run_cli_command(["wallet", "balance", wallet_name])
        
        return results
    
    def escrow_commands_demo(self) -> Dict[str, Any]:
        """Demonstrate escrow management commands."""
        results = {
            "list_stakes": None,
            "create_stake": None
        }
        
        # List existing stakes
        results["list_stakes"] = self.run_cli_command(["escrow", "list"])
        
        # Create a test stake (will likely fail without proper setup)
        results["create_stake"] = self.run_cli_command([
            "escrow", "stake",
            "--amount", "0.1",
            "--wallet", "test-wallet",
            "--duration", "7"  # 7 days
        ])
        
        return results
    
    def k8s_commands_demo(self) -> Dict[str, Any]:
        """Demonstrate Kubernetes integration commands."""
        results = {
            "list_nodes": None,
            "node_status": None,
            "generate_manifests": None
        }
        
        # List nodes
        results["list_nodes"] = self.run_cli_command(["k8s", "list-nodes"])
        
        # Get node status
        results["node_status"] = self.run_cli_command(["k8s", "node-status"])
        
        # Generate deployment manifests
        output_dir = os.path.join(os.getcwd(), "generated-manifests")
        os.makedirs(output_dir, exist_ok=True)
        
        results["generate_manifests"] = self.run_cli_command([
            "k8s", "generate-manifests",
            "--output-dir", output_dir,
            "--node-name", "testnet-node-1"
        ])
        
        return results
    
    def ledger_commands_demo(self) -> Dict[str, Any]:
        """Demonstrate ledger verification commands."""
        results = {
            "verify_tx": None,
            "list_proofs": None
        }
        
        # Verify a test transaction (will likely fail without a real tx hash)
        test_tx_hash = "0x" + "0" * 64
        results["verify_tx"] = self.run_cli_command(["ledger", "verify", test_tx_hash])
        
        # List proof logs
        results["list_proofs"] = self.run_cli_command(["ledger", "list-proofs"])
        
        return results
    
    def run_full_demo(self) -> Dict[str, Any]:
        """Run the full CLI demo."""
        results = {}
        
        logger.info("==========================================")
        logger.info("MetaNode CLI Testnet Integration Demo")
        logger.info("==========================================")
        
        # Show available commands
        logger.info("\n== Available CLI Commands ==")
        results["available_commands"] = self.list_available_commands()
        
        try:
            # Wallet commands demo
            logger.info("\n== Wallet Commands Demo ==")
            results["wallet_commands"] = self.wallet_commands_demo()
            
            # Escrow commands demo
            logger.info("\n== Escrow Commands Demo ==")
            results["escrow_commands"] = self.escrow_commands_demo()
            
            # K8s commands demo
            logger.info("\n== Kubernetes Commands Demo ==")
            results["k8s_commands"] = self.k8s_commands_demo()
            
            # Ledger commands demo
            logger.info("\n== Ledger Commands Demo ==")
            results["ledger_commands"] = self.ledger_commands_demo()
        
        except Exception as e:
            logger.error(f"Demo encountered an error: {e}")
            results["error"] = str(e)
        
        # Save results
        output_file = "testnet_cli_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"\nResults saved to {output_file}")
        logger.info("==========================================")
        logger.info("Demo completed")
        logger.info("==========================================")
        
        return results


def main():
    """Run the MetaNode CLI testnet integration demo."""
    parser = argparse.ArgumentParser(description="MetaNode CLI Testnet Integration Demo")
    parser.add_argument("--api-url", help="Custom API URL")
    parser.add_argument("--blockchain-url", help="Custom blockchain URL")
    parser.add_argument("--validator-url", help="Custom validator URL")
    parser.add_argument("--admin-key", help="Admin API key")
    args = parser.parse_args()
    
    # Set environment variables if provided
    if args.api_url:
        os.environ["METANODE_API_URL"] = args.api_url
    if args.blockchain_url:
        os.environ["METANODE_BLOCKCHAIN_URL"] = args.blockchain_url
    if args.validator_url:
        os.environ["METANODE_VALIDATOR_URL"] = args.validator_url
    if args.admin_key:
        os.environ["METANODE_ADMIN_KEY"] = args.admin_key
    
    # Run the demo
    demo = MetaNodeCLIDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
