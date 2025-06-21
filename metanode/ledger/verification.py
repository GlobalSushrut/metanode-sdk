#!/usr/bin/env python3
"""
MetaNode SDK - Verification Module
=================================

Tools for validating cryptographic proofs and transactions.
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

class Verifier:
    """High-level interface for verification operations."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize the verifier.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.logs_dir = os.path.join(os.path.expanduser("~"), ".metanode", "verification")
        
        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Use the detailed verification engine
        self.verification_engine = Verification(api_url)
    
    def verify_tx(self, tx_hash: str) -> Dict[str, Any]:
        """
        Verify a blockchain transaction.
        
        Args:
            tx_hash (str): Transaction hash to verify
            
        Returns:
            dict: Transaction verification result
        """
        return self.verification_engine.verify_transaction(tx_hash)
    
    def verify_agreement(self, agreement_hash: str) -> Dict[str, Any]:
        """
        Verify an agreement's integrity and status.
        
        Args:
            agreement_hash (str): Hash of the agreement to verify
            
        Returns:
            dict: Agreement verification result
        """
        return self.verification_engine.verify_agreement(agreement_hash)
    
    def verify_proof_log(self, log_id: str) -> Dict[str, Any]:
        """
        Verify a proof log's integrity.
        
        Args:
            log_id (str): ID of the log to verify
            
        Returns:
            dict: Log verification result
        """
        try:
            # Find the log file (assuming it's in the standard logs directory)
            log_file = os.path.join(os.path.expanduser("~"), ".metanode", "logs", f"operation-{log_id}.json")
            
            if not os.path.exists(log_file):
                return {"status": "error", "message": f"Log {log_id} not found"}
            
            # Load the log
            with open(log_file, "r") as f:
                log_entry = json.load(f)
            
            # Extract the stored hash
            stored_hash = log_entry.get("hash")
            if not stored_hash:
                return {"status": "error", "message": "Log does not contain a hash"}
            
            # Compute the hash of the log entry
            entry_for_hash = log_entry.copy()
            entry_for_hash.pop("hash")
            computed_hash = hashlib.sha256(json.dumps(entry_for_hash, sort_keys=True).encode()).hexdigest()
            
            # Compare hashes
            if computed_hash == stored_hash:
                # Save verification record
                verification = {
                    "log_id": log_id,
                    "verified": True,
                    "stored_hash": stored_hash,
                    "computed_hash": computed_hash,
                    "timestamp": int(time.time())
                }
                
                verification_file = os.path.join(self.logs_dir, f"verify-log-{log_id}.json")
                with open(verification_file, "w") as f:
                    json.dump(verification, f, indent=2)
                
                return {
                    "status": "success", 
                    "verified": True,
                    "log_id": log_id,
                    "verification_file": verification_file
                }
            else:
                return {
                    "status": "success",
                    "verified": False,
                    "log_id": log_id,
                    "error": "Hash mismatch",
                    "stored_hash": stored_hash,
                    "computed_hash": computed_hash
                }
                
        except Exception as e:
            logger.error(f"Failed to verify proof log: {e}")
            return {"status": "error", "message": str(e)}

class Verification:
    """Validates cryptographic proofs and transactions for agreements."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize verification manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.logs_dir = os.path.join(os.getcwd(), ".metanode", "logs")
        
        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def verify_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """
        Verify a blockchain transaction.
        
        Args:
            tx_hash (str): Transaction hash to verify
            
        Returns:
            dict: Transaction verification result
        """
        try:
            # Query blockchain for transaction receipt
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_getTransactionReceipt",
                    "params": [tx_hash],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    receipt = data["result"]
                    
                    # Check if transaction was successful
                    if receipt and receipt.get("status") == "0x1":
                        # Get transaction details
                        tx_response = requests.post(
                            self.blockchain_url,
                            headers={"Content-Type": "application/json"},
                            json={
                                "jsonrpc": "2.0",
                                "method": "eth_getTransactionByHash",
                                "params": [tx_hash],
                                "id": 1
                            }
                        )
                        
                        tx_data = {}
                        if tx_response.status_code == 200:
                            tx_data = tx_response.json().get("result", {})
                        
                        # Save verification information
                        verification = {
                            "tx_hash": tx_hash,
                            "verified": True,
                            "block_number": int(receipt.get("blockNumber", "0x0"), 16),
                            "block_hash": receipt.get("blockHash"),
                            "gas_used": int(receipt.get("gasUsed", "0x0"), 16),
                            "timestamp": int(time.time()),
                            "transaction": tx_data
                        }
                        
                        # Save locally
                        verification_file = os.path.join(self.logs_dir, f"verify-tx-{tx_hash}.json")
                        with open(verification_file, 'w') as f:
                            json.dump(verification, f, indent=2)
                        
                        logger.info(f"Transaction {tx_hash} verified successfully")
                        return {
                            "status": "success",
                            "verified": True,
                            "tx_hash": tx_hash,
                            "block_number": verification["block_number"],
                            "gas_used": verification["gas_used"],
                            "verification_file": verification_file
                        }
                    else:
                        logger.warning(f"Transaction {tx_hash} failed or not found")
                        return {
                            "status": "error",
                            "verified": False,
                            "tx_hash": tx_hash,
                            "message": "Transaction failed or not found"
                        }
                elif "error" in data:
                    logger.error(f"Verification error: {data['error']}")
                    return {"status": "error", "message": str(data["error"])}
            else:
                logger.error(f"Verification request failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Verification error: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_agreement(self, agreement_hash: str) -> Dict[str, Any]:
        """
        Verify an agreement's integrity and status.
        
        Args:
            agreement_hash (str): Hash of the agreement to verify
            
        Returns:
            dict: Agreement verification result
        """
        try:
            # Query API for agreement status
            response = requests.get(
                f"{self.api_url}/agreement/{agreement_hash}/verify",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                agreement_data = response.json()
                
                # Also verify on-chain
                blockchain_response = requests.post(
                    self.blockchain_url,
                    headers={"Content-Type": "application/json"},
                    json={
                        "jsonrpc": "2.0",
                        "method": "metanode_verifyAgreement",
                        "params": [agreement_hash],
                        "id": 1
                    }
                )
                
                blockchain_verified = False
                chain_data = {}
                
                if blockchain_response.status_code == 200:
                    chain_result = blockchain_response.json()
                    if "result" in chain_result:
                        chain_data = chain_result["result"]
                        blockchain_verified = chain_data.get("verified", False)
                
                # Combine verification results
                verification = {
                    "agreement_hash": agreement_hash,
                    "api_verified": agreement_data.get("verified", False),
                    "blockchain_verified": blockchain_verified,
                    "status": agreement_data.get("status"),
                    "timestamp": int(time.time()),
                    "api_data": agreement_data,
                    "chain_data": chain_data
                }
                
                # Save locally
                verification_file = os.path.join(self.logs_dir, f"verify-agreement-{agreement_hash}.json")
                with open(verification_file, 'w') as f:
                    json.dump(verification, f, indent=2)
                
                logger.info(f"Agreement {agreement_hash} verification: API={verification['api_verified']}, Blockchain={verification['blockchain_verified']}")
                return {
                    "status": "success",
                    "agreement_hash": agreement_hash,
                    "api_verified": verification["api_verified"],
                    "blockchain_verified": verification["blockchain_verified"],
                    "agreement_status": verification["status"],
                    "verification_file": verification_file
                }
            else:
                logger.error(f"Agreement verification failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Agreement verification error: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_merkle_proof(self, proof: Dict[str, Any], root: str) -> Dict[str, Any]:
        """
        Verify a Merkle proof against a known root.
        
        Args:
            proof (dict): Merkle proof with path and value
            root (str): Expected Merkle root
            
        Returns:
            dict: Proof verification result
        """
        try:
            # Extract proof components
            leaf_hash = proof.get("leaf_hash")
            path = proof.get("path", [])
            
            if not leaf_hash or not path:
                return {
                    "status": "error",
                    "message": "Invalid proof format. Must include leaf_hash and path."
                }
            
            # Calculate Merkle root from proof
            current_hash = leaf_hash
            for node in path:
                if node.get("left"):
                    current_hash = hashlib.sha256(f"{node['left']}{current_hash}".encode()).hexdigest()
                else:
                    current_hash = hashlib.sha256(f"{current_hash}{node['right']}".encode()).hexdigest()
            
            # Compare calculated root with expected root
            verified = current_hash == root
            
            logger.info(f"Merkle proof verification: {verified} (calculated={current_hash}, expected={root})")
            return {
                "status": "success",
                "verified": verified,
                "calculated_root": current_hash,
                "expected_root": root
            }
                
        except Exception as e:
            logger.error(f"Merkle proof verification error: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_zk_proof(self, proof: Dict[str, Any], public_inputs: List[str]) -> Dict[str, Any]:
        """
        Verify a zero-knowledge proof.
        
        Args:
            proof (dict): Zero-knowledge proof data
            public_inputs (list): Public inputs for verification
            
        Returns:
            dict: ZK proof verification result
        """
        try:
            # Query API for ZK verification
            response = requests.post(
                f"{self.api_url}/zk/verify",
                headers={"Content-Type": "application/json"},
                json={
                    "proof": proof,
                    "public_inputs": public_inputs
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                verified = result.get("verified", False)
                
                logger.info(f"ZK proof verification: {verified}")
                return {
                    "status": "success",
                    "verified": verified,
                    "details": result
                }
            else:
                logger.error(f"ZK proof verification failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"ZK proof verification error: {e}")
            return {"status": "error", "message": str(e)}
    
    def validate_mining_report(self, report: Dict[str, Any], report_hash: str) -> Dict[str, Any]:
        """
        Validate a mining activity report.
        
        Args:
            report (dict): Mining report data
            report_hash (str): Hash of the report to validate
            
        Returns:
            dict: Report validation result
        """
        try:
            # Calculate hash of report to verify integrity
            report_json = json.dumps(report, sort_keys=True)
            calculated_hash = hashlib.sha256(report_json.encode()).hexdigest()
            
            # Check if calculated hash matches provided hash
            if calculated_hash != report_hash:
                logger.warning(f"Mining report hash mismatch: {calculated_hash} != {report_hash}")
                return {
                    "status": "error",
                    "verified": False,
                    "message": "Report hash mismatch"
                }
            
            # Query API for report validation
            response = requests.post(
                f"{self.api_url}/mining/validate_report",
                headers={"Content-Type": "application/json"},
                json={
                    "report": report,
                    "hash": report_hash
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                validated = result.get("validated", False)
                
                # Save validation result
                validation = {
                    "report_hash": report_hash,
                    "validated": validated,
                    "timestamp": int(time.time()),
                    "details": result,
                    "report": report
                }
                
                validation_file = os.path.join(self.logs_dir, f"validate-mining-{report_hash}.json")
                with open(validation_file, 'w') as f:
                    json.dump(validation, f, indent=2)
                
                logger.info(f"Mining report {report_hash} validation: {validated}")
                return {
                    "status": "success",
                    "validated": validated,
                    "report_hash": report_hash,
                    "validation_file": validation_file
                }
            else:
                logger.error(f"Mining report validation failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Mining report validation error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create verification manager
    verification = Verification()
    
    # Verify a transaction
    tx_result = verification.verify_transaction("0xSampleTransactionHash")
    print(f"Transaction verification: {json.dumps(tx_result, indent=2)}")
    
    # Verify an agreement
    agreement_result = verification.verify_agreement("0xSampleAgreementHash")
    print(f"Agreement verification: {json.dumps(agreement_result, indent=2)}")
    
    # Verify a Merkle proof
    proof = {
        "leaf_hash": "0xLeafHash",
        "path": [
            {"right": "0xRightNode1"},
            {"left": "0xLeftNode2"}
        ]
    }
    merkle_result = verification.verify_merkle_proof(proof, "0xExpectedRoot")
    print(f"Merkle proof verification: {json.dumps(merkle_result, indent=2)}")
