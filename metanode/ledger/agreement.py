#!/usr/bin/env python3
"""
MetaNode SDK - Agreement and Ledger Module
=======================================

Tools for managing agreements between clients and servers, and interacting with the mainnet ledger.
"""

import os
import json
import time
import hashlib
import logging
import requests
from enum import Enum
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL, BLOCKCHAIN_URL

# Configure logging
logger = logging.getLogger(__name__)

class AgreementStatus(Enum):
    """Status of an agreement between client and server."""
    CREATED = "created"
    ACTIVE = "active"
    EXPIRED = "expired"
    DISPUTED = "disputed"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Agreement:
    """Manages agreements between clients and servers in the MetaNode ecosystem."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize agreement manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.blockchain_url = BLOCKCHAIN_URL
        self.agreement_id = None
        self.agreement_hash = None
        self.agreement_file_path = None
    
    def generate_agreement(self, contract_meta: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate hash-locked deployment contract between client and server.
        
        Args:
            contract_meta (dict): Contract metadata with fields:
                - client_id: ID of the client
                - server_id: ID of the server
                - app_name: Name of the application
                - resources: Requested resources
                - duration: Duration of the agreement in seconds
                - payment_terms: Payment terms and rates
                
        Returns:
            dict: Agreement details and hash
        """
        try:
            # Validate required metadata
            required_fields = ["client_id", "server_id", "app_name", "resources"]
            missing = [field for field in required_fields if field not in contract_meta]
            if missing:
                return {"status": "error", "message": f"Missing required contract fields: {missing}"}
            
            # Set default values
            duration = contract_meta.get("duration", 86400)  # 24 hours default
            payment_terms = contract_meta.get("payment_terms", {
                "rate": "1.0",
                "currency": "MNT",
                "payment_schedule": "hourly"
            })
            
            # Generate timestamp and IDs
            timestamp = int(time.time())
            agreement_id_input = f"{contract_meta['client_id']}:{contract_meta['server_id']}:{contract_meta['app_name']}:{timestamp}"
            agreement_id = hashlib.sha256(agreement_id_input.encode()).hexdigest()[:16]
            
            # Create agreement content
            agreement = {
                "agreement_id": agreement_id,
                "client_id": contract_meta["client_id"],
                "server_id": contract_meta["server_id"],
                "app": {
                    "name": contract_meta["app_name"],
                    "version": contract_meta.get("version", "1.0.0")
                },
                "resources": contract_meta["resources"],
                "created_at": timestamp,
                "starts_at": contract_meta.get("starts_at", timestamp),
                "expires_at": contract_meta.get("starts_at", timestamp) + duration,
                "payment_terms": payment_terms,
                "status": AgreementStatus.CREATED.value,
                "extensions": contract_meta.get("extensions", {})
            }
            
            # Calculate agreement hash
            agreement_json = json.dumps(agreement, sort_keys=True)
            agreement_hash = hashlib.sha256(agreement_json.encode()).hexdigest()
            agreement["agreement_hash"] = agreement_hash
            
            # Save agreement to file
            agreements_dir = os.path.join(os.getcwd(), ".metanode", "agreements")
            os.makedirs(agreements_dir, exist_ok=True)
            
            agreement_file_path = os.path.join(agreements_dir, f"agreement-{agreement_id}.json")
            with open(agreement_file_path, 'w') as f:
                json.dump(agreement, f, indent=2)
            
            # Update instance state
            self.agreement_id = agreement_id
            self.agreement_hash = agreement_hash
            self.agreement_file_path = agreement_file_path
            
            logger.info(f"Generated agreement {agreement_id} with hash {agreement_hash}")
            return {
                "status": "success",
                "agreement_id": agreement_id,
                "agreement_hash": agreement_hash,
                "agreement_file": agreement_file_path,
                "agreement": agreement
            }
            
        except Exception as e:
            logger.error(f"Agreement generation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def submit_agreement_to_mainnet(self) -> Dict[str, Any]:
        """
        Add agreement to mainnet ledger for ZK-verification.
        
        Returns:
            dict: Submission result and transaction hash
        """
        try:
            # Check if we have an agreement
            if not self.agreement_hash or not self.agreement_file_path:
                return {
                    "status": "error", 
                    "message": "No agreement. Generate an agreement first."
                }
            
            # Load agreement from file
            with open(self.agreement_file_path, 'r') as f:
                agreement = json.load(f)
            
            # Submit agreement to blockchain via RPC
            response = requests.post(
                self.blockchain_url,
                headers={"Content-Type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "method": "metanode_submitAgreement",
                    "params": [agreement],
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    tx_hash = data["result"]
                    
                    # Update agreement status and transaction hash
                    agreement["status"] = AgreementStatus.ACTIVE.value
                    agreement["mainnet"] = {
                        "tx_hash": tx_hash,
                        "submitted_at": int(time.time())
                    }
                    
                    # Save updated agreement
                    with open(self.agreement_file_path, 'w') as f:
                        json.dump(agreement, f, indent=2)
                    
                    logger.info(f"Submitted agreement {self.agreement_id} to mainnet with tx {tx_hash}")
                    return {
                        "status": "success",
                        "agreement_id": self.agreement_id,
                        "tx_hash": tx_hash
                    }
                elif "error" in data:
                    error_message = data["error"]["message"]
                    logger.error(f"Mainnet submission error: {error_message}")
                    return {"status": "error", "message": error_message}
            else:
                logger.error(f"Mainnet RPC error: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Mainnet submission error: {e}")
            return {"status": "error", "message": str(e)}
    
    def validate_agreement_state(self, agreement_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Check current state (live, expired, dispute, complete).
        
        Args:
            agreement_id (str, optional): ID of the agreement to validate.
                                         If not provided, uses the instance agreement.
        
        Returns:
            dict: Agreement state and validity
        """
        try:
            # Determine the agreement to validate
            target_agreement_id = agreement_id or self.agreement_id
            
            if not target_agreement_id:
                return {
                    "status": "error", 
                    "message": "No agreement ID specified."
                }
            
            # Try to find agreement file
            agreement_file = None
            if self.agreement_file_path and os.path.exists(self.agreement_file_path):
                agreement_file = self.agreement_file_path
            else:
                # Search in agreements directory
                agreements_dir = os.path.join(os.getcwd(), ".metanode", "agreements")
                if os.path.exists(agreements_dir):
                    possible_files = [
                        os.path.join(agreements_dir, f"agreement-{target_agreement_id}.json"),
                        os.path.join(agreements_dir, f"agreement.deploy.{target_agreement_id}.lock")
                    ]
                    
                    for file_path in possible_files:
                        if os.path.exists(file_path):
                            agreement_file = file_path
                            break
            
            # Load agreement if found
            if agreement_file:
                with open(agreement_file, 'r') as f:
                    agreement = json.load(f)
            else:
                # Query the API for agreement
                response = requests.get(
                    f"{self.api_url}/agreement/{target_agreement_id}",
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    agreement = response.json()
                else:
                    return {
                        "status": "error", 
                        "message": f"Agreement {target_agreement_id} not found."
                    }
            
            # Check agreement state
            current_time = int(time.time())
            
            # Expired check
            if "expires_at" in agreement and current_time > agreement["expires_at"]:
                current_status = AgreementStatus.EXPIRED.value
            else:
                current_status = agreement.get("status", AgreementStatus.CREATED.value)
            
            # Get blockchain state
            mainnet_status = None
            if "mainnet" in agreement and "tx_hash" in agreement["mainnet"]:
                tx_hash = agreement["mainnet"]["tx_hash"]
                
                # Query blockchain for agreement state
                response = requests.post(
                    self.blockchain_url,
                    headers={"Content-Type": "application/json"},
                    json={
                        "jsonrpc": "2.0",
                        "method": "metanode_getAgreementStatus",
                        "params": [tx_hash],
                        "id": 1
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "result" in data:
                        mainnet_status = data["result"]["status"]
            
            # If blockchain status is different, use it (it's authoritative)
            if mainnet_status and mainnet_status != current_status:
                current_status = mainnet_status
                
                # Update local file if we have one
                if agreement_file:
                    agreement["status"] = current_status
                    with open(agreement_file, 'w') as f:
                        json.dump(agreement, f, indent=2)
            
            # Return validation result
            return {
                "status": "success",
                "agreement_id": target_agreement_id,
                "agreement_status": current_status,
                "valid": current_status in [AgreementStatus.CREATED.value, AgreementStatus.ACTIVE.value],
                "expired": current_status == AgreementStatus.EXPIRED.value,
                "disputed": current_status == AgreementStatus.DISPUTED.value,
                "completed": current_status == AgreementStatus.COMPLETED.value,
                "canceled": current_status == AgreementStatus.CANCELED.value,
                "details": agreement
            }
                
        except Exception as e:
            logger.error(f"Agreement validation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def load_agreement(self, agreement_id: str) -> Dict[str, Any]:
        """
        Load an existing agreement.
        
        Args:
            agreement_id (str): ID of the agreement to load
            
        Returns:
            dict: Loaded agreement data
        """
        try:
            # Search in agreements directory
            agreements_dir = os.path.join(os.getcwd(), ".metanode", "agreements")
            if os.path.exists(agreements_dir):
                possible_files = [
                    os.path.join(agreements_dir, f"agreement-{agreement_id}.json"),
                    os.path.join(agreements_dir, f"agreement.deploy.{agreement_id}.lock")
                ]
                
                for file_path in possible_files:
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            agreement = json.load(f)
                            
                            # Update instance state
                            self.agreement_id = agreement_id
                            self.agreement_hash = agreement.get("agreement_hash")
                            self.agreement_file_path = file_path
                            
                            return {
                                "status": "success",
                                "agreement_id": agreement_id,
                                "agreement_hash": self.agreement_hash,
                                "agreement": agreement
                            }
            
            # If not found locally, try the API
            response = requests.get(
                f"{self.api_url}/agreement/{agreement_id}",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                agreement = response.json()
                
                # Save to local file
                os.makedirs(agreements_dir, exist_ok=True)
                file_path = os.path.join(agreements_dir, f"agreement-{agreement_id}.json")
                
                with open(file_path, 'w') as f:
                    json.dump(agreement, f, indent=2)
                
                # Update instance state
                self.agreement_id = agreement_id
                self.agreement_hash = agreement.get("agreement_hash")
                self.agreement_file_path = file_path
                
                return {
                    "status": "success",
                    "agreement_id": agreement_id,
                    "agreement_hash": self.agreement_hash,
                    "agreement": agreement
                }
            else:
                return {
                    "status": "error", 
                    "message": f"Agreement {agreement_id} not found."
                }
                
        except Exception as e:
            logger.error(f"Agreement loading error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create agreement manager
    agreement_manager = Agreement()
    
    # Generate a sample agreement
    contract_meta = {
        "client_id": "client-123",
        "server_id": "server-456",
        "app_name": "web-app",
        "version": "1.0.0",
        "resources": {
            "cpu": "200m",
            "memory": "256Mi"
        },
        "duration": 3600,  # 1 hour
        "payment_terms": {
            "rate": "0.5",
            "currency": "MNT",
            "payment_schedule": "hourly"
        }
    }
    
    result = agreement_manager.generate_agreement(contract_meta)
    print(f"Agreement generation: {json.dumps(result, indent=2)}")
    
    # Submit to mainnet (commented out for example)
    # submit_result = agreement_manager.submit_agreement_to_mainnet()
    # print(f"Mainnet submission: {json.dumps(submit_result, indent=2)}")
    
    # Validate agreement state
    validation_result = agreement_manager.validate_agreement_state()
    print(f"Agreement validation: {json.dumps(validation_result, indent=2)}")
