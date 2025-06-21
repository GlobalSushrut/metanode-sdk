#!/usr/bin/env python3
"""
MetaNode SDK - Zero-Knowledge Proofs Utility Module
================================================

Tools for generating and verifying zero-knowledge proofs for secure aggregation.
"""

import os
import json
import time
import hashlib
import logging
import requests
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL

# Configure logging
logger = logging.getLogger(__name__)

class ZKProofManager:
    """Manages zero-knowledge proofs for secure aggregation in MetaNode."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize ZK proof manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.utils_dir = os.path.join(os.getcwd(), ".metanode", "utils")
        self.zk_dir = os.path.join(self.utils_dir, "zk_proofs")
        
        # Ensure directories exist
        os.makedirs(self.zk_dir, exist_ok=True)
    
    def generate_proof(self, 
                      private_inputs: Dict[str, Any], 
                      public_inputs: Dict[str, Any], 
                      circuit_type: str = "secure_aggregation") -> Dict[str, Any]:
        """
        Generate a zero-knowledge proof for secure aggregation.
        
        Args:
            private_inputs (dict): Private inputs for the proof
            public_inputs (dict): Public inputs for the proof
            circuit_type (str): Type of ZK circuit to use
            
        Returns:
            dict: Generated proof
        """
        try:
            # Create request data
            timestamp = int(time.time())
            request_data = {
                "private_inputs": private_inputs,
                "public_inputs": public_inputs,
                "circuit_type": circuit_type,
                "timestamp": timestamp
            }
            
            # Send request to API
            response = requests.post(
                f"{self.api_url}/zk/generate",
                headers={"Content-Type": "application/json"},
                json=request_data
            )
            
            if response.status_code == 200:
                proof_data = response.json()
                proof = proof_data.get("proof", {})
                proof_id = proof_data.get("proof_id", hashlib.sha256(str(timestamp).encode()).hexdigest()[:16])
                
                # Save proof information (exclude private_inputs for security)
                proof_info = {
                    "proof_id": proof_id,
                    "proof": proof,
                    "public_inputs": public_inputs,
                    "circuit_type": circuit_type,
                    "timestamp": timestamp
                }
                
                proof_file = os.path.join(self.zk_dir, f"proof-{proof_id}.json")
                with open(proof_file, 'w') as f:
                    json.dump(proof_info, f, indent=2)
                
                logger.info(f"Generated ZK proof with ID {proof_id}")
                return {
                    "status": "success",
                    "proof_id": proof_id,
                    "proof": proof,
                    "proof_file": proof_file
                }
            else:
                logger.error(f"Failed to generate proof: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Proof generation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_proof(self, proof: Dict[str, Any], public_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a zero-knowledge proof.
        
        Args:
            proof (dict): The proof to verify
            public_inputs (dict): Public inputs for verification
            
        Returns:
            dict: Verification result
        """
        try:
            # Create request data
            request_data = {
                "proof": proof,
                "public_inputs": public_inputs,
                "timestamp": int(time.time())
            }
            
            # Send request to API
            response = requests.post(
                f"{self.api_url}/zk/verify",
                headers={"Content-Type": "application/json"},
                json=request_data
            )
            
            if response.status_code == 200:
                verification_data = response.json()
                verified = verification_data.get("verified", False)
                
                logger.info(f"ZK proof verification result: {verified}")
                return {
                    "status": "success",
                    "verified": verified,
                    "verification_details": verification_data
                }
            else:
                logger.error(f"Failed to verify proof: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Proof verification error: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_secure_aggregation_proof(self, 
                                        private_data: Dict[str, Any], 
                                        aggregation_id: str) -> Dict[str, Any]:
        """
        Generate a proof specifically for secure aggregation protocol.
        
        Args:
            private_data (dict): Private data to be aggregated
            aggregation_id (str): ID of the aggregation session
            
        Returns:
            dict: Generated proof for secure aggregation
        """
        try:
            # Prepare inputs for secure aggregation
            data_hash = hashlib.sha256(json.dumps(private_data, sort_keys=True).encode()).hexdigest()
            
            # Prepare inputs
            private_inputs = {
                "data": private_data,
                "random_seed": os.urandom(16).hex()
            }
            
            public_inputs = {
                "data_hash": data_hash,
                "aggregation_id": aggregation_id
            }
            
            # Generate the proof
            result = self.generate_proof(
                private_inputs=private_inputs,
                public_inputs=public_inputs,
                circuit_type="secure_aggregation"
            )
            
            if result["status"] == "success":
                # Add aggregation-specific metadata
                proof_id = result["proof_id"]
                proof_file = result["proof_file"]
                
                # Update the saved file with aggregation metadata
                with open(proof_file, 'r') as f:
                    proof_info = json.load(f)
                
                proof_info["aggregation_id"] = aggregation_id
                proof_info["data_hash"] = data_hash
                
                with open(proof_file, 'w') as f:
                    json.dump(proof_info, f, indent=2)
                
                logger.info(f"Generated secure aggregation proof for session {aggregation_id}")
                return {
                    "status": "success",
                    "proof_id": proof_id,
                    "proof": result["proof"],
                    "aggregation_id": aggregation_id,
                    "data_hash": data_hash,
                    "proof_file": proof_file
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Secure aggregation proof error: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_proofs(self) -> Dict[str, Any]:
        """
        List all saved proofs.
        
        Returns:
            dict: List of saved proofs
        """
        try:
            proofs = []
            
            if os.path.exists(self.zk_dir):
                for filename in os.listdir(self.zk_dir):
                    if filename.startswith("proof-") and filename.endswith(".json"):
                        try:
                            with open(os.path.join(self.zk_dir, filename), 'r') as f:
                                proof_info = json.load(f)
                                proofs.append({
                                    "proof_id": proof_info.get("proof_id"),
                                    "circuit_type": proof_info.get("circuit_type"),
                                    "timestamp": proof_info.get("timestamp"),
                                    "filename": filename
                                })
                        except Exception as e:
                            logger.warning(f"Error loading proof file {filename}: {e}")
            
            logger.info(f"Listed {len(proofs)} saved proofs")
            return {
                "status": "success",
                "proofs": proofs,
                "count": len(proofs)
            }
                
        except Exception as e:
            logger.error(f"Proof listing error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_circuit_templates(self) -> Dict[str, Any]:
        """
        Get available circuit templates for zero-knowledge proofs.
        
        Returns:
            dict: List of available circuit templates
        """
        try:
            # Query API for circuit templates
            response = requests.get(
                f"{self.api_url}/zk/circuits",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                templates_data = response.json()
                templates = templates_data.get("templates", [])
                
                logger.info(f"Retrieved {len(templates)} circuit templates")
                return {
                    "status": "success",
                    "templates": templates,
                    "count": len(templates)
                }
            else:
                logger.error(f"Failed to get circuit templates: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Circuit templates error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create ZK proof manager
    zk_manager = ZKProofManager()
    
    # Generate a simple proof for testing
    private_inputs = {
        "data": [1, 2, 3, 4, 5],
        "random_seed": "0123456789abcdef"
    }
    
    public_inputs = {
        "data_sum": 15,
        "data_count": 5
    }
    
    proof_result = zk_manager.generate_proof(private_inputs, public_inputs)
    print(f"Proof generation: {json.dumps(proof_result, indent=2)}")
    
    # Verify the generated proof
    if proof_result["status"] == "success":
        verify_result = zk_manager.verify_proof(proof_result["proof"], public_inputs)
        print(f"Proof verification: {json.dumps(verify_result, indent=2)}")
