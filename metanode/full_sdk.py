#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MetaNode Full Infrastructure SDK
================================

This module provides a comprehensive Python interface for the entire MetaNode infrastructure,
integrating blockchain, IPFS, validator nodes, and agreement management.

Features:
- App initialization and deployment
- Blockchain integration
- Agreement creation and management
- Testnet connectivity and contribution
- Node cluster deployment
- Infrastructure monitoring
- Cross-platform compatibility

Usage:
    from metanode.full_sdk import MetaNodeSDK
    
    # Initialize SDK
    sdk = MetaNodeSDK()
    
    # Create and deploy application with full infrastructure
    sdk.init_app("my-dapp")
    sdk.deploy_app("my-dapp", with_blockchain=True, with_ipfs=True)
    
    # Create and deploy an agreement
    agreement_id = sdk.create_agreement("my-dapp", agreement_type="standard")
    sdk.deploy_agreement("my-dapp", agreement_id)
    
    # Create node cluster for decentralization
    sdk.create_node_cluster("my-dapp")
"""

import os
import sys
import json
import uuid
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("metanode-sdk")

class MetaNodeSDK:
    """Main SDK class for MetaNode Full Infrastructure"""
    
    def __init__(self, 
                 rpc_endpoint: str = "http://159.203.17.36:8545",
                 ws_endpoint: str = "ws://159.203.17.36:8546",
                 network_type: str = "testnet",
                 ipfs_gateway: str = "http://localhost:8081",
                 config_dir: Optional[str] = None):
        """Initialize the SDK with connection parameters
        
        Args:
            rpc_endpoint: Blockchain RPC endpoint
            ws_endpoint: WebSocket endpoint for blockchain
            network_type: Network type (testnet or mainnet)
            ipfs_gateway: IPFS gateway URL
            config_dir: Custom configuration directory
        """
        self.rpc_endpoint = rpc_endpoint
        self.ws_endpoint = ws_endpoint
        self.network_type = network_type
        self.ipfs_gateway = ipfs_gateway
        
        # Set up configuration directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".metanode"
        
        self.config_dir.mkdir(exist_ok=True, parents=True)
        
        # Get CLI paths
        self.cli_path = self._get_cli_path()
        
        # Validate environment
        self._validate_environment()
        
        logger.info(f"MetaNode SDK initialized with {network_type} network")

    def _get_cli_path(self) -> str:
        """Find the MetaNode CLI path"""
        # Check if the CLI is in the PATH
        try:
            result = subprocess.run(["which", "metanode-cli"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            pass
            
        # Check if CLI exists in bin directory of package
        script_dir = Path(__file__).parent.parent / "bin" / "metanode-cli-enhanced"
        if script_dir.exists():
            return str(script_dir)
            
        # Check common install locations
        common_paths = [
            Path.home() / "bin" / "metanode-cli",
            Path("/usr/local/bin/metanode-cli"),
            Path("/usr/bin/metanode-cli"),
        ]
        
        for path in common_paths:
            if path.exists():
                return str(path)
                
        raise FileNotFoundError("MetaNode CLI not found. Please install it first.")
    
    def _validate_environment(self) -> None:
        """Validate that all required dependencies are available"""
        required_commands = ["docker", "python3", "curl"]
        
        for cmd in required_commands:
            try:
                subprocess.run(["which", cmd], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             check=True)
            except subprocess.CalledProcessError:
                logger.warning(f"{cmd} not found in PATH. Some features may not work correctly.")
    
    def _run_cli_command(self, *args) -> Tuple[int, str, str]:
        """Run a CLI command and return exit code, stdout and stderr"""
        cmd = [self.cli_path] + list(args)
        logger.debug(f"Running command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
        
    def init_app(self, app_name: str, app_dir: Optional[str] = None) -> bool:
        """Initialize a new MetaNode application
        
        Args:
            app_name: Name of the application
            app_dir: Directory where the application will be created (default: current dir)
            
        Returns:
            bool: True if successful, False otherwise
        """
        args = ["init", app_name]
        
        if app_dir:
            os.chdir(app_dir)
            
        args.extend(["--network", self.network_type, "--rpc", self.rpc_endpoint])
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"App {app_name} initialized successfully")
            logger.debug(stdout)
            return True
        else:
            logger.error(f"Failed to initialize app: {stderr}")
            return False
            
    def deploy_app(self, 
                  app_name: str, 
                  with_blockchain: bool = True, 
                  with_ipfs: bool = True, 
                  with_agreements: bool = True) -> bool:
        """Deploy a MetaNode application with selected components
        
        Args:
            app_name: Name of the application
            with_blockchain: Deploy with blockchain integration
            with_ipfs: Deploy with IPFS integration
            with_agreements: Deploy with agreement support
            
        Returns:
            bool: True if successful, False otherwise
        """
        args = ["deploy", app_name]
        
        if with_blockchain:
            args.append("--blockchain")
            
        if with_ipfs:
            args.append("--ipfs")
            
        if with_agreements:
            args.append("--agreements")
            
        args.extend(["--network", self.network_type, "--rpc", self.rpc_endpoint])
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"App {app_name} deployed successfully")
            logger.debug(stdout)
            return True
        else:
            logger.error(f"Failed to deploy app: {stderr}")
            return False
            
    def create_agreement(self, 
                        app_name: str, 
                        agreement_type: str = "standard") -> Optional[str]:
        """Create a new blockchain agreement for an application
        
        Args:
            app_name: Name of the application
            agreement_type: Type of agreement
            
        Returns:
            str: Agreement ID if successful, None otherwise
        """
        args = ["agreement", app_name, "--create", "--type", agreement_type]
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"Agreement created for app {app_name}")
            
            # Extract agreement ID from output
            for line in stdout.splitlines():
                if "Agreement created with ID:" in line:
                    agreement_id = line.split(":")[1].strip()
                    return agreement_id
                    
            logger.warning("Agreement created but couldn't extract ID from output")
            return None
        else:
            logger.error(f"Failed to create agreement: {stderr}")
            return None
            
    def deploy_agreement(self, app_name: str, agreement_id: str) -> bool:
        """Deploy an agreement to the blockchain
        
        Args:
            app_name: Name of the application
            agreement_id: ID of the agreement
            
        Returns:
            bool: True if successful, False otherwise
        """
        args = ["agreement", app_name, "--deploy", "--id", agreement_id]
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"Agreement {agreement_id} deployed successfully")
            logger.debug(stdout)
            return True
        else:
            logger.error(f"Failed to deploy agreement: {stderr}")
            return False
            
    def verify_agreement(self, app_name: str, agreement_id: str) -> bool:
        """Verify an agreement on the blockchain
        
        Args:
            app_name: Name of the application
            agreement_id: ID of the agreement
            
        Returns:
            bool: True if verified, False otherwise
        """
        args = ["agreement", app_name, "--verify", "--id", agreement_id]
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"Agreement {agreement_id} verified successfully")
            
            # Check if verification was successful
            if "Agreement verified successfully" in stdout:
                return True
            else:
                logger.warning("Verification output doesn't confirm success")
                return False
        else:
            logger.error(f"Failed to verify agreement: {stderr}")
            return False
            
    def create_node_cluster(self, 
                           app_name: str, 
                           node_count: int = 3, 
                           node_types: List[str] = None) -> bool:
        """Create a node cluster for improved decentralization
        
        Args:
            app_name: Name of the application
            node_count: Number of nodes in the cluster
            node_types: Types of nodes to create (validator, light, sync)
            
        Returns:
            bool: True if successful, False otherwise
        """
        args = ["cluster", app_name, "--create"]
        
        if node_count:
            args.extend(["--count", str(node_count)])
            
        if node_types:
            args.extend(["--types", ",".join(node_types)])
            
        args.extend(["--rpc", self.rpc_endpoint])
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"Node cluster created for app {app_name}")
            logger.debug(stdout)
            return True
        else:
            logger.error(f"Failed to create node cluster: {stderr}")
            return False
            
    def test_testnet_connection(self) -> Dict[str, Any]:
        """Test connection to the testnet
        
        Returns:
            dict: Test results
        """
        args = ["testnet", "--test", "--rpc", self.rpc_endpoint]
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info("Testnet connection test successful")
            
            # Try to parse JSON response
            try:
                for line in stdout.splitlines():
                    line = line.strip()
                    if line.startswith('{') and line.endswith('}'):
                        return json.loads(line)
            except json.JSONDecodeError:
                pass
                
            return {"status": "success", "details": stdout}
        else:
            logger.error(f"Failed to test testnet connection: {stderr}")
            return {"status": "error", "details": stderr}
            
    def setup_testnet_connection(self, app_name: str) -> bool:
        """Set up connection to the testnet for an application
        
        Args:
            app_name: Name of the application
            
        Returns:
            bool: True if successful, False otherwise
        """
        args = ["testnet", app_name, "--setup", "--rpc", self.rpc_endpoint]
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"Testnet connection set up for app {app_name}")
            logger.debug(stdout)
            return True
        else:
            logger.error(f"Failed to set up testnet connection: {stderr}")
            return False
            
    def check_status(self, app_name: str) -> Dict[str, Any]:
        """Check status of a MetaNode application
        
        Args:
            app_name: Name of the application
            
        Returns:
            dict: Status details
        """
        args = ["status", app_name]
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"Status check completed for app {app_name}")
            
            # Try to parse JSON response
            try:
                for line in stdout.splitlines():
                    line = line.strip()
                    if line.startswith('{') and line.endswith('}'):
                        return json.loads(line)
            except json.JSONDecodeError:
                pass
                
            return {"status": "success", "details": stdout}
        else:
            logger.error(f"Failed to check status: {stderr}")
            return {"status": "error", "details": stderr}
            
    def setup_verification_proofs(self, app_name: str) -> bool:
        """Set up verification proofs for an application
        
        Args:
            app_name: Name of the application
            
        Returns:
            bool: True if successful, False otherwise
        """
        args = ["testnet", app_name, "--verification", "--setup"]
        
        exit_code, stdout, stderr = self._run_cli_command(*args)
        
        if exit_code == 0:
            logger.info(f"Verification proofs set up for app {app_name}")
            logger.debug(stdout)
            return True
        else:
            logger.error(f"Failed to set up verification proofs: {stderr}")
            return False


# Alias for backward compatibility
MetaNode = MetaNodeSDK

if __name__ == "__main__":
    print("MetaNode Full Infrastructure SDK")
    print("Use this module by importing it in your Python code:")
    print("  from metanode.full_sdk import MetaNodeSDK")
