#!/usr/bin/env python3
"""
MetaNode SDK - Proof Logging Module
=================================

Tools for creating and managing cryptographic proof logs for agreements and operations.
"""

import os
import json
import time
import uuid
import hashlib
import logging
import requests
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL, BLOCKCHAIN_URL

# Configure logging
logger = logging.getLogger(__name__)

class ProofLogger:
    """Higher-level manager for cryptographic proof logs across multiple operations."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize proof logger.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.logs_dir = os.path.join(os.path.expanduser("~"), ".metanode", "logs")
        
        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def create_operation_log(self, operation_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new operation log with cryptographic proof.
        
        Args:
            operation_type: Type of operation (e.g., 'node_registration', 'deployment')
            data: Operation data to log
            
        Returns:
            Dict containing log ID and status
        """
        try:
            log_id = str(uuid.uuid4())
            timestamp = time.time()
            
            # Create log entry
            log_entry = {
                "log_id": log_id,
                "operation_type": operation_type,
                "timestamp": timestamp,
                "data": data,
                "hash": None  # Will be computed below
            }
            
            # Compute hash of the log entry (without the hash field)
            entry_for_hash = log_entry.copy()
            entry_for_hash.pop("hash")
            entry_hash = hashlib.sha256(json.dumps(entry_for_hash, sort_keys=True).encode()).hexdigest()
            log_entry["hash"] = entry_hash
            
            # Save to file
            log_file = os.path.join(self.logs_dir, f"operation-{log_id}.json")
            with open(log_file, "w") as f:
                json.dump(log_entry, f, indent=2)
            
            return {
                "status": "success",
                "log_id": log_id,
                "hash": entry_hash,
                "file": log_file
            }
        except Exception as e:
            logger.error(f"Failed to create operation log: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_operation_log(self, log_id: str) -> Dict[str, Any]:
        """
        Verify the integrity of an operation log.
        
        Args:
            log_id: ID of the log to verify
            
        Returns:
            Dict with verification status
        """
        try:
            # Find the log file
            log_file = os.path.join(self.logs_dir, f"operation-{log_id}.json")
            if not os.path.exists(log_file):
                return {"status": "error", "message": f"Log {log_id} not found"}
            
            # Load the log
            with open(log_file, "r") as f:
                log_entry = json.load(f)
            
            # Extract the stored hash
            stored_hash = log_entry.get("hash")
            if not stored_hash:
                return {"status": "error", "message": "Log does not contain a hash"}
            
            # Compute the hash of the log entry (without the hash field)
            entry_for_hash = log_entry.copy()
            entry_for_hash.pop("hash")
            computed_hash = hashlib.sha256(json.dumps(entry_for_hash, sort_keys=True).encode()).hexdigest()
            
            # Compare hashes
            if computed_hash == stored_hash:
                return {"status": "success", "verified": True, "log_id": log_id}
            else:
                return {"status": "success", "verified": False, "log_id": log_id, "error": "Hash mismatch"}
        except Exception as e:
            logger.error(f"Failed to verify operation log: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_operation_logs(self, operation_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List all operation logs, optionally filtered by operation type.
        
        Args:
            operation_type: Optional filter for operation type
            
        Returns:
            Dict with list of operation logs
        """
        try:
            logs = []
            for filename in os.listdir(self.logs_dir):
                if filename.startswith("operation-") and filename.endswith(".json"):
                    try:
                        with open(os.path.join(self.logs_dir, filename), "r") as f:
                            log_entry = json.load(f)
                            
                            # Filter by operation type if specified
                            if operation_type and log_entry.get("operation_type") != operation_type:
                                continue
                                
                            logs.append(log_entry)
                    except Exception as e:
                        logger.warning(f"Failed to load log file {filename}: {e}")
            
            return {"status": "success", "logs": logs}
        except Exception as e:
            logger.error(f"Failed to list operation logs: {e}")
            return {"status": "error", "message": str(e)}

class ProofLog:
    """Manages cryptographic proof logs for MetaNode operations."""
    
    def __init__(self, api_url: Optional[str] = None, agreement_id: Optional[str] = None):
        """
        Initialize proof log manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            agreement_id (str, optional): ID of the associated agreement
        """
        self.api_url = api_url or API_URL
        self.agreement_id = agreement_id
        self.logs_dir = os.path.join(os.getcwd(), ".metanode", "logs")
        
        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def store_proof_log(self, message: Dict[str, Any], sign_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Add signed message to mutable IPFS-based proof log.
        
        Args:
            message (dict): Message content to log
            sign_key (str, optional): Key to use for message signing, if any
            
        Returns:
            dict: Proof log storage result with hash
        """
        try:
            # Add metadata to the message
            timestamp = int(time.time())
            message_id = str(uuid.uuid4())
            
            proof_message = {
                "id": message_id,
                "timestamp": timestamp,
                "content": message
            }
            
            # Add agreement ID if available
            if self.agreement_id:
                proof_message["agreement_id"] = self.agreement_id
            
            # Sign the message if key is provided
            if sign_key:
                from ..utils.crypto import sign_message
                signature = sign_message(json.dumps(proof_message), sign_key)
                proof_message["signature"] = signature
            
            # Calculate message hash
            message_json = json.dumps(proof_message, sort_keys=True)
            message_hash = hashlib.sha256(message_json.encode()).hexdigest()
            
            # Save locally
            log_file = os.path.join(self.logs_dir, f"{message_id}.json")
            with open(log_file, 'w') as f:
                json.dump(proof_message, f, indent=2)
            
            # Submit to API
            response = requests.post(
                f"{self.api_url}/proof/log",
                headers={"Content-Type": "application/json"},
                json={
                    "proof": proof_message,
                    "hash": message_hash
                }
            )
            
            api_response = {}
            if response.status_code == 200:
                api_response = response.json()
                ipfs_hash = api_response.get("ipfs_hash")
                
                # Add IPFS hash to local file
                if ipfs_hash:
                    proof_message["ipfs_hash"] = ipfs_hash
                    with open(log_file, 'w') as f:
                        json.dump(proof_message, f, indent=2)
                
                logger.info(f"Stored proof log with ID {message_id} and hash {message_hash}")
            else:
                logger.warning(f"Failed to store proof in IPFS: {response.text}")
            
            return {
                "status": "success",
                "message_id": message_id,
                "message_hash": message_hash,
                "local_file": log_file,
                "ipfs_hash": api_response.get("ipfs_hash"),
                "proof_message": proof_message
            }
            
        except Exception as e:
            logger.error(f"Proof log storage error: {e}")
            return {"status": "error", "message": str(e)}
    
    def fetch_app_history(self, app_id: str) -> Dict[str, Any]:
        """
        Pull full timeline of agreement logs for auditing.
        
        Args:
            app_id (str): ID of the application
            
        Returns:
            dict: Application history with proof logs
        """
        try:
            # Query API for app history
            response = requests.get(
                f"{self.api_url}/proof/history/{app_id}",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                history = response.json()
                
                # Save history locally
                history_file = os.path.join(self.logs_dir, f"history-{app_id}.json")
                with open(history_file, 'w') as f:
                    json.dump(history, f, indent=2)
                
                logger.info(f"Retrieved history for app {app_id} with {len(history.get('logs', []))} logs")
                return {
                    "status": "success",
                    "app_id": app_id,
                    "history": history,
                    "history_file": history_file
                }
            else:
                logger.error(f"Failed to fetch app history: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"History retrieval error: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_proof_log(self, log_hash: str) -> Dict[str, Any]:
        """
        Verify the integrity of a proof log entry.
        
        Args:
            log_hash (str): Hash of the log entry to verify
            
        Returns:
            dict: Verification result
        """
        try:
            # Query API for verification
            response = requests.post(
                f"{self.api_url}/proof/verify",
                headers={"Content-Type": "application/json"},
                json={"hash": log_hash}
            )
            
            if response.status_code == 200:
                verification = response.json()
                verified = verification.get("verified", False)
                
                if verified:
                    logger.info(f"Proof log {log_hash} verified successfully")
                else:
                    logger.warning(f"Proof log {log_hash} verification failed")
                
                return {
                    "status": "success",
                    "verified": verified,
                    "details": verification
                }
            else:
                logger.error(f"Failed to verify proof log: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Verification error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_agreement_logs(self, agreement_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all logs for a specific agreement.
        
        Args:
            agreement_id (str, optional): ID of the agreement.
                If not provided, uses the instance agreement ID.
                
        Returns:
            dict: Agreement logs
        """
        try:
            # Determine target agreement
            target_agreement = agreement_id or self.agreement_id
            
            if not target_agreement:
                return {
                    "status": "error", 
                    "message": "No agreement ID specified."
                }
            
            # Query API for agreement logs
            response = requests.get(
                f"{self.api_url}/proof/agreement/{target_agreement}",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                logs = response.json()
                
                # Save logs locally
                logs_file = os.path.join(self.logs_dir, f"agreement-logs-{target_agreement}.json")
                with open(logs_file, 'w') as f:
                    json.dump(logs, f, indent=2)
                
                logger.info(f"Retrieved {len(logs.get('logs', []))} logs for agreement {target_agreement}")
                return {
                    "status": "success",
                    "agreement_id": target_agreement,
                    "logs": logs,
                    "logs_file": logs_file
                }
            else:
                logger.error(f"Failed to fetch agreement logs: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Logs retrieval error: {e}")
            return {"status": "error", "message": str(e)}
    
    def export_logs(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Export filtered logs to file.
        
        Args:
            filters (dict, optional): Filter criteria for logs
            
        Returns:
            dict: Export result
        """
        try:
            # Initialize filters
            if filters is None:
                filters = {}
            
            # Find local logs
            logs = []
            if os.path.exists(self.logs_dir):
                for filename in os.listdir(self.logs_dir):
                    if filename.endswith('.json') and not filename.startswith('history-') and not filename.startswith('agreement-logs-'):
                        try:
                            file_path = os.path.join(self.logs_dir, filename)
                            with open(file_path, 'r') as f:
                                log = json.load(f)
                                
                                # Apply filters
                                include = True
                                for key, value in filters.items():
                                    if key not in log or log[key] != value:
                                        include = False
                                        break
                                
                                if include:
                                    logs.append(log)
                                    
                        except Exception as e:
                            logger.error(f"Error processing log file {filename}: {e}")
            
            # Sort logs by timestamp
            logs.sort(key=lambda x: x.get('timestamp', 0))
            
            # Export to file
            export_file = os.path.join(self.logs_dir, f"export-{int(time.time())}.json")
            with open(export_file, 'w') as f:
                json.dump({"logs": logs, "exported_at": int(time.time())}, f, indent=2)
            
            logger.info(f"Exported {len(logs)} logs to {export_file}")
            return {
                "status": "success",
                "count": len(logs),
                "export_file": export_file
            }
                
        except Exception as e:
            logger.error(f"Export error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create proof log manager
    proof_log = ProofLog(agreement_id="sample-agreement-123")
    
    # Store a sample proof log
    message = {
        "type": "status_update",
        "status": "running",
        "metrics": {
            "cpu": 12.5,
            "memory": 256
        }
    }
    
    log_result = proof_log.store_proof_log(message)
    print(f"Proof log storage: {json.dumps(log_result, indent=2)}")
    
    # Retrieve logs for an agreement
    agreement_logs = proof_log.get_agreement_logs()
    print(f"Agreement logs: {json.dumps(agreement_logs, indent=2)}")
    
    # Export logs with filters
    export_result = proof_log.export_logs({"type": "status_update"})
    print(f"Export result: {json.dumps(export_result, indent=2)}")
