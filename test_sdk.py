#!/usr/bin/env python3
"""
MetaNode SDK Test Script
=======================

This script tests the core functionality of the MetaNode SDK after installation,
including the blockchain infrastructure components.
"""

import os
import sys
import json
import time
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("metanode-sdk-tester")

def run_command(command, expected_success=True):
    """Run a shell command and return the output."""
    try:
        logger.info(f"Running command: {command}")
        result = subprocess.run(
            command, 
            shell=True, 
            check=expected_success,
            text=True,
            capture_output=True
        )
        if result.returncode == 0:
            logger.info("Command succeeded!")
            if result.stdout:
                logger.info(f"Output: {result.stdout.strip()}")
            return True, result.stdout
        else:
            logger.error(f"Command failed with code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr.strip()}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        logger.error(f"Command execution failed: {e}")
        return False, str(e)

def test_import():
    """Test importing the MetaNode SDK modules."""
    try:
        logger.info("Testing module imports...")
        
        # Try importing key modules
        import_statements = [
            "from metanode.admin.k8s_manager import K8sManager",
            "from metanode.admin.security import SecurityManager",
            "from metanode.utils.zk_proofs import ZKProofManager",
            "from metanode.utils.ipfs_tools import IPFSManager",
            "from metanode.cli import cli",
            "from metanode.blockchain import initialize_blockchain, connect_to_testnet",
            "from metanode.blockchain.validator import validate_agreement",
            "from metanode.blockchain.transaction import create_transaction",
            "from metanode.blockchain.storage import store_data",
            "from metanode.blockchain.infrastructure import InfrastructureConfig"
        ]
        
        for statement in import_statements:
            try:
                exec(statement)
                logger.info(f"Successfully imported: {statement}")
            except ImportError as e:
                logger.error(f"Failed to import: {statement}")
                logger.error(f"Error: {e}")
                return False
                
        logger.info("All imports successful!")
        return True
    except Exception as e:
        logger.error(f"Error testing imports: {e}")
        return False

def test_k8s_manager():
    """Test the K8s Manager functionality."""
    try:
        logger.info("Testing K8s Manager...")
        from metanode.admin.k8s_manager import K8sManager
        
        k8s_manager = K8sManager()
        
        # Test key generation (doesn't require actual K8s cluster)
        key_result = k8s_manager.generate_node_crypt_key()
        if key_result["status"] != "success":
            logger.error(f"Failed to generate cryptographic key: {key_result['message']}")
            return False
            
        logger.info(f"Successfully generated key with ID: {key_result['key_id']}")
        
        # Check if key file was created
        key_file = Path(key_result['key_file'])
        if not key_file.exists():
            logger.error(f"Key file not created at {key_file}")
            return False
            
        logger.info(f"Key file created at {key_file}")
        
        logger.info("K8s Manager tests passed!")
        return True
    except Exception as e:
        logger.error(f"Error testing K8s Manager: {e}")
        return False

def test_cli_commands():
    """Test CLI commands."""
    try:
        logger.info("Testing CLI commands...")
        
        # First check if we can import the CLI app
        try:
            from metanode.cli import cli
            logger.info("Successfully imported CLI app")
            cli_import_success = True
        except ImportError:
            logger.error("Failed to import CLI app")
            cli_import_success = False
            
        # Even if import fails, try basic CLI commands for installed packages
        try:
            # Use installed pip module venv to run metanode
            success, output = run_command("python -m metanode.cli.main --help", expected_success=False)
            if success and ("MetaNode SDK" in output or "Usage:" in output):
                logger.info("CLI module can be run via Python module")
                return True
        except Exception as e:
            logger.warning(f"Could not run CLI via Python module: {e}")
        
        # If we got here, both direct import and module running failed
        if not cli_import_success:
            return False
            
        logger.info("CLI command tests completed!")
        return True
    except Exception as e:
        logger.error(f"Error testing CLI commands: {e}")
        return False

def test_sdk_installation():
    """Test if the SDK is properly installed."""
    try:
        logger.info("Testing SDK installation...")
        
        # Check if metanode command exists in PATH
        success, output = run_command("which metanode", expected_success=False)
        if not success:
            logger.warning("metanode command not found in PATH")
        else:
            logger.info(f"metanode command found at {output.strip()}")
        
        # Test Python package installation
        success, output = run_command("pip show metanode-sdk")
        if not success:
            logger.error("MetaNode SDK not installed via pip")
            return False
            
        logger.info("SDK installation test passed!")
        return True
    except Exception as e:
        logger.error(f"Error testing SDK installation: {e}")
        return False

def test_blockchain():
    """Test blockchain functionality."""
    try:
        logger.info("Testing blockchain components...")
        
        # Import blockchain modules
        try:
            from metanode.blockchain import initialize_blockchain, connect_to_testnet
            from metanode.blockchain.validator import validate_agreement
            from metanode.blockchain.transaction import create_transaction, sign_transaction
            from metanode.blockchain.storage import store_data, retrieve_data
            from metanode.blockchain.infrastructure import setup_complete_infrastructure
            logger.info("Successfully imported blockchain modules")
        except ImportError as e:
            logger.error(f"Failed to import blockchain modules: {e}")
            return False
        
        # Create a simple test transaction
        try:
            # Create test data
            test_data = {"test": "data", "timestamp": time.time()}
            
            # Test transaction creation
            tx = create_transaction("test_operation", test_data)
            logger.info(f"Created test transaction with ID: {tx['tx_id']}")
            
            # Test agreement validation
            agreement_result = validate_agreement("test-agreement", "test_action")
            logger.info(f"Agreement validation result: {agreement_result['validated']}")
            
            # Test data storage
            storage_result = store_data(test_data)
            logger.info(f"Data stored with hash: {storage_result['content_hash']}")
            
            logger.info("All blockchain component tests succeeded!")
            return True
        except Exception as e:
            logger.error(f"Error in blockchain tests: {e}")
            return False
    except Exception as e:
        logger.error(f"Error testing blockchain: {e}")
        return False

def main():
    """Run all tests."""
    parser = argparse.ArgumentParser(description='Test MetaNode SDK functionality')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--blockchain', '-b', action='store_true', help='Test blockchain components')
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info("Starting MetaNode SDK tests...")
    
    test_results = {
        "Installation": test_sdk_installation(),
        "Imports": test_import(),
        "K8s Manager": test_k8s_manager(),
        "CLI Commands": test_cli_commands()
    }
    
    # Run blockchain tests if specified or if no specific tests are selected
    if args.blockchain or not any([args.verbose]):
        test_results["Blockchain"] = test_blockchain()
    
    # Print summary
    logger.info("\n----- TEST RESULTS SUMMARY -----")
    all_passed = True
    for test_name, result in test_results.items():
        status = "PASSED" if result else "FAILED"
        if not result:
            all_passed = False
        logger.info(f"{test_name}: {status}")
    
    if all_passed:
        logger.info("\n✅ ALL TESTS PASSED! The MetaNode SDK is working properly.")
        return 0
    else:
        logger.error("\n❌ SOME TESTS FAILED. Please check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
