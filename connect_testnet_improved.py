#!/usr/bin/env python3
"""
MetaNode Testnet Connection - Improved
====================================

This script connects to the deployed MetaNode testnet with a focus on working
with the actual operational components, particularly the blockchain node.
It also provides enhanced debugging and interaction capabilities.
"""

import os
import sys
import json
import time
import logging
import hashlib
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List

# Import MetaNode SDK components
from metanode.config.endpoints import API_URL, BLOCKCHAIN_URL, BFR_URL, VALIDATOR_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("metanode-testnet-client")

class TestnetClient:
    """Client for interacting with the MetaNode testnet."""
    
    def __init__(self, blockchain_url=BLOCKCHAIN_URL, api_url=API_URL):
        self.blockchain_url = blockchain_url
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
    def _rpc_call(self, method: str, params=None) -> Dict[str, Any]:
        """Make a JSON-RPC call to the blockchain node."""
        if params is None:
            params = []
            
        try:
            response = self.session.post(
                self.blockchain_url,
                json={
                    "jsonrpc": "2.0",
                    "method": method,
                    "params": params,
                    "id": int(time.time())
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"RPC call failed with status {response.status_code}: {response.text}")
                return {"error": f"HTTP {response.status_code}", "details": response.text}
                
        except requests.RequestException as e:
            logger.error(f"RPC request failed: {e}")
            return {"error": str(e)}
    
    def get_client_version(self) -> str:
        """Get the client version of the blockchain node."""
        result = self._rpc_call("web3_clientVersion")
        return result.get("result", "Unknown")
        
    def get_block_number(self) -> int:
        """Get the current block number."""
        result = self._rpc_call("eth_blockNumber")
        if "result" in result:
            return int(result["result"], 16)
        return -1
        
    def get_network_id(self) -> str:
        """Get the network ID."""
        result = self._rpc_call("net_version")
        return result.get("result", "Unknown")
        
    def get_syncing_status(self) -> Dict[str, Any]:
        """Check if the blockchain is syncing."""
        return self._rpc_call("eth_syncing")
        
    def get_peer_count(self) -> int:
        """Get the number of connected peers."""
        result = self._rpc_call("net_peerCount")
        if "result" in result:
            try:
                # Handle hex string format
                if isinstance(result["result"], str) and result["result"].startswith("0x"):
                    return int(result["result"], 16)
                # Handle direct integer
                elif isinstance(result["result"], int):
                    return result["result"]
                # Handle string integer
                elif isinstance(result["result"], str) and result["result"].isdigit():
                    return int(result["result"])
                else:
                    logger.warning(f"Unexpected peer count format: {result['result']}")
                    return 0
            except Exception as e:
                logger.error(f"Error parsing peer count: {e}")
                return 0
        return -1
    
    def get_accounts(self) -> List[str]:
        """Get the list of accounts on the node."""
        result = self._rpc_call("eth_accounts")
        return result.get("result", [])
        
    def get_balance(self, address: str) -> int:
        """Get the balance of an account."""
        result = self._rpc_call("eth_getBalance", [address, "latest"])
        if "result" in result:
            return int(result["result"], 16)
        return -1
        
    def get_block_by_number(self, block_number: int) -> Dict[str, Any]:
        """Get block details by number."""
        hex_block = hex(block_number) if isinstance(block_number, int) else block_number
        return self._rpc_call("eth_getBlockByNumber", [hex_block, True])
        
    def get_transaction_count(self, address: str) -> int:
        """Get the transaction count for an address."""
        result = self._rpc_call("eth_getTransactionCount", [address, "latest"])
        if "result" in result:
            return int(result["result"], 16)
        return -1
        
    def send_transaction(self, tx_object: Dict[str, Any]) -> Dict[str, Any]:
        """Send a transaction to the blockchain."""
        return self._rpc_call("eth_sendTransaction", [tx_object])
        
    def estimate_gas(self, tx_object: Dict[str, Any]) -> int:
        """Estimate gas for a transaction."""
        result = self._rpc_call("eth_estimateGas", [tx_object])
        if "result" in result:
            return int(result["result"], 16)
        return -1
        
    def get_mining_status(self) -> bool:
        """Check if the node is mining."""
        result = self._rpc_call("eth_mining")
        return result.get("result", False)
        
    def create_filter(self, filter_obj: Dict[str, Any]) -> str:
        """Create an event filter."""
        result = self._rpc_call("eth_newFilter", [filter_obj])
        return result.get("result", "")
        
    def get_filter_changes(self, filter_id: str) -> List[Any]:
        """Get changes for a filter since last poll."""
        result = self._rpc_call("eth_getFilterChanges", [filter_id])
        return result.get("result", [])


def check_validator_node():
    """Get status from validator node which seems to be online."""
    try:
        response = requests.get(f"{VALIDATOR_URL}/status", timeout=5)
        if response.status_code == 200:
            return {
                "status": "online",
                "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        else:
            return {"status": "error", "code": response.status_code, "response": response.text}
    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}


def create_local_wallet():
    """Create a local wallet for testing purposes."""
    import os
    import json
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    
    # Generate a new private key
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    
    # Get the public key
    public_key = private_key.public_key()
    
    # Serialize the keys
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Create a simple address from the public key
    public_key_hash = hashlib.sha256(public_key_bytes).hexdigest()
    address = f"0x{public_key_hash[:40]}"
    
    # Save wallet data
    wallet_dir = os.path.join(os.path.expanduser("~"), ".metanode", "wallets")
    os.makedirs(wallet_dir, exist_ok=True)
    
    wallet_file = os.path.join(wallet_dir, f"local-{address[-8:]}.json")
    wallet_data = {
        "address": address,
        "public_key": public_key_bytes.decode('utf-8'),
        "created_at": datetime.now().isoformat(),
        "type": "local_test_wallet"
    }
    
    with open(wallet_file, 'w') as f:
        json.dump(wallet_data, f, indent=2)
        
    logger.info(f"Created local test wallet: {address}")
    return wallet_data


def generate_testnet_report(client):
    """Generate a comprehensive report on testnet status."""
    report = {}
    
    # Get blockchain info with error handling
    try:
        report["client_version"] = client.get_client_version()
        logger.info(f"Client version: {report['client_version']}")
    except Exception as e:
        logger.error(f"Failed to get client version: {e}")
        report["client_version"] = "Error retrieving client version"
    
    try:
        report["block_number"] = client.get_block_number()
        logger.info(f"Current block number: {report['block_number']}")
    except Exception as e:
        logger.error(f"Failed to get block number: {e}")
        report["block_number"] = -1
    
    try:
        report["network_id"] = client.get_network_id()
        logger.info(f"Network ID: {report['network_id']}")
    except Exception as e:
        logger.error(f"Failed to get network ID: {e}")
        report["network_id"] = "Unknown"
    
    try:
        report["peer_count"] = client.get_peer_count()
        logger.info(f"Peer count: {report['peer_count']}")
    except Exception as e:
        logger.error(f"Failed to get peer count: {e}")
        report["peer_count"] = 0
    
    try:
        report["is_mining"] = client.get_mining_status()
        logger.info(f"Mining status: {report['is_mining']}")
    except Exception as e:
        logger.error(f"Failed to get mining status: {e}")
        report["is_mining"] = False
    
    # Get validator status
    try:
        report["validator_status"] = check_validator_node()
        logger.info(f"Validator status: {report['validator_status']['status']}")
    except Exception as e:
        logger.error(f"Failed to get validator status: {e}")
        report["validator_status"] = {"status": "error", "message": str(e)}
    
    # Get accounts and balances
    try:
        accounts = client.get_accounts()
        report["accounts"] = []
        
        for addr in accounts:
            try:
                balance = client.get_balance(addr)
                report["accounts"].append({
                    "address": addr,
                    "balance": balance,
                    "balance_eth": balance / 10**18 if balance >= 0 else "Unknown"
                })
            except Exception as e:
                logger.error(f"Failed to get balance for {addr}: {e}")
                report["accounts"].append({
                    "address": addr,
                    "balance": -1,
                    "balance_eth": "Error retrieving balance"
                })
    except Exception as e:
        logger.error(f"Failed to get accounts: {e}")
        report["accounts"] = []
    
    # Get block info with error handling
    current_block = report["block_number"]
    if current_block > 0:
        try:
            genesis_block = client.get_block_by_number(0)
            report["genesis_block"] = genesis_block.get("result", {})
            
            latest_block = client.get_block_by_number("latest")
            report["latest_block"] = latest_block.get("result", {})
            
            # Calculate blocks per second with safeguards
            if isinstance(report["genesis_block"], dict) and isinstance(report["latest_block"], dict) and \
               "timestamp" in report["genesis_block"] and "timestamp" in report["latest_block"]:
                try:
                    # Handle different timestamp formats
                    if isinstance(report["genesis_block"]["timestamp"], str):
                        if report["genesis_block"]["timestamp"].startswith("0x"):
                            genesis_time = int(report["genesis_block"]["timestamp"], 16)
                        else:
                            genesis_time = int(report["genesis_block"]["timestamp"])
                    else:
                        genesis_time = report["genesis_block"]["timestamp"]
                        
                    if isinstance(report["latest_block"]["timestamp"], str):
                        if report["latest_block"]["timestamp"].startswith("0x"):
                            latest_time = int(report["latest_block"]["timestamp"], 16)
                        else:
                            latest_time = int(report["latest_block"]["timestamp"])
                    else:
                        latest_time = report["latest_block"]["timestamp"]
                    
                    time_diff = latest_time - genesis_time
                    
                    if time_diff > 0:
                        blocks_per_sec = current_block / time_diff
                        report["blocks_per_second"] = blocks_per_sec
                        logger.info(f"Blocks per second: {blocks_per_sec}")
                except Exception as e:
                    logger.error(f"Failed to calculate blocks per second: {e}")
        except Exception as e:
            logger.error(f"Error retrieving block information: {e}")
                
    # Create a local wallet if interacting with the testnet directly
    report["local_wallet"] = create_local_wallet()
    
    return report


def main():
    """Run the improved testnet connection script."""
    logger.info("==========================================")
    logger.info("MetaNode Testnet Connection - Improved")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("==========================================")
    
    # Initialize testnet client
    logger.info(f"Connecting to blockchain node at {BLOCKCHAIN_URL}...")
    client = TestnetClient()
    
    # Generate comprehensive testnet report
    logger.info("Generating testnet status report...")
    report = generate_testnet_report(client)
    
    # Display key information
    logger.info(f"\nBlockchain Client: {report['client_version']}")
    logger.info(f"Current Block: {report['block_number']}")
    logger.info(f"Network ID: {report['network_id']}")
    logger.info(f"Connected Peers: {report['peer_count']}")
    logger.info(f"Mining Status: {report['is_mining']}")
    
    if report["accounts"]:
        logger.info(f"\nFound {len(report['accounts'])} accounts on the blockchain node")
        for account in report["accounts"]:
            logger.info(f"  Address: {account['address']}")
            logger.info(f"  Balance: {account['balance_eth']} ETH")
    else:
        logger.info("\nNo accounts found on the blockchain node")
        
    # Display local wallet info
    logger.info(f"\nCreated local wallet: {report['local_wallet']['address']}")
    
    # Save detailed report to file
    output_file = "testnet_detailed_report.json"
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"\nDetailed report written to {output_file}")
    
    # Suggest next steps
    logger.info("\n== Suggested Next Actions ==")
    logger.info("1. Use the local wallet to interact with the blockchain")
    logger.info("2. Check validator node status regularly")
    logger.info("3. Monitor block production rate")
    
    if report["block_number"] <= 1:
        logger.info("4. The blockchain has minimal blocks - you may want to trigger some transactions")
    
    logger.info("==========================================")
    logger.info("Connection test completed")
    logger.info("==========================================")


if __name__ == "__main__":
    main()
