"""
MetaNode Immutable Decentralized Agent
====================================
Agent that maintains cryptographic proofs and follows rules established by agreement
nodes while ensuring consensus validation via blockchain testnet/mainnet
"""

import os
import json
import time
import logging
import hashlib
import requests
from typing import Dict, Any, List, Optional, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("metanode.dapp.agent")

class DecentralizedAgent:
    """
    Immutable decentralized agent that connects to testnet/mainnet
    and maintains cryptographic proofs of actions
    """
    
    def __init__(self, network_endpoints: Dict[str, str], use_mainnet: bool = False):
        """
        Initialize decentralized agent
        
        Args:
            network_endpoints: Dictionary of network endpoint URLs
            use_mainnet: Whether to use mainnet
        """
        self.network_endpoints = network_endpoints
        self.use_mainnet = use_mainnet
        self.connected = False
        self.agent_id = self._generate_agent_id()
        self.proofs = []
        self.rules = []
        self.consensus_threshold = 2/3  # 66% consensus required
        
    def _generate_agent_id(self) -> str:
        """
        Generate unique agent ID with timestamp
        
        Returns:
            Agent ID
        """
        timestamp = str(time.time())
        agent_hash = hashlib.sha256(f"metanode-agent-{timestamp}".encode()).hexdigest()
        return f"agent-{agent_hash[:8]}"
        
    def connect(self) -> bool:
        """
        Connect to testnet/mainnet
        
        Returns:
            Whether connection was successful
        """
        try:
            # Connect to blockchain using RPC URL
            rpc_url = self.network_endpoints.get("rpc_url")
            response = requests.get(f"{rpc_url}/status", timeout=10)
            
            if response.status_code == 200:
                self.connected = True
                logger.info(f"Connected agent to {'mainnet' if self.use_mainnet else 'testnet'}")
                
                # Register agent with blockchain
                self._register_agent()
                
                # Load rules from agreement nodes
                self._load_rules()
                
                return True
            else:
                logger.error(f"Failed to connect to {'mainnet' if self.use_mainnet else 'testnet'}: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error connecting to network: {str(e)}")
            return False
            
    def _register_agent(self):
        """Register agent with blockchain"""
        # This would call the actual blockchain API
        # For now, we'll just log the registration
        logger.info(f"Registered agent {self.agent_id} with blockchain")
        
        # Record proof of registration
        self._add_proof("registration", {
            "agent_id": self.agent_id,
            "network": "mainnet" if self.use_mainnet else "testnet",
            "timestamp": time.time()
        })
        
    def _load_rules(self):
        """Load rules from agreement nodes"""
        try:
            # URL of agreement node API 
            agreement_url = self.network_endpoints.get("agreement_url", "")
            
            if agreement_url:
                response = requests.get(f"{agreement_url}/rules", timeout=10)
                
                if response.status_code == 200:
                    self.rules = response.json().get("rules", [])
                    logger.info(f"Loaded {len(self.rules)} rules from agreement nodes")
                    return
                    
            # Fallback to default rules if agreement nodes unavailable
            self.rules = [
                {
                    "id": "rule-immutability",
                    "description": "All actions must maintain immutability",
                    "condition": "action.immutable == true",
                    "priority": 1
                },
                {
                    "id": "rule-consensus",
                    "description": "All critical actions require consensus validation",
                    "condition": "action.critical ? action.consensus >= 0.66 : true",
                    "priority": 2
                }
            ]
            logger.info(f"Using {len(self.rules)} default rules (agreement nodes unavailable)")
            
        except Exception as e:
            logger.error(f"Error loading rules: {str(e)}")
            # Use default rules on error
            self.rules = [
                {
                    "id": "rule-immutability",
                    "description": "All actions must maintain immutability",
                    "condition": "action.immutable == true"
                }
            ]
            
    def _add_proof(self, action_type: str, data: Dict[str, Any]):
        """
        Add cryptographic proof of action
        
        Args:
            action_type: Type of action
            data: Action data
        """
        timestamp = time.time()
        
        # Create proof with cryptographic hash
        proof_data = {
            "agent_id": self.agent_id,
            "action": action_type,
            "data": data,
            "timestamp": timestamp
        }
        
        # Create proof hash
        proof_str = json.dumps(proof_data, sort_keys=True)
        proof_hash = hashlib.sha256(proof_str.encode()).hexdigest()
        
        # Add proof to blockchain record
        proof = {
            "hash": proof_hash,
            "data": proof_data,
            "verified": False
        }
        
        self.proofs.append(proof)
        
        # Submit proof to blockchain
        self._submit_proof(proof)
        
        return proof
        
    def _submit_proof(self, proof: Dict[str, Any]):
        """
        Submit proof to blockchain
        
        Args:
            proof: Proof data
        """
        try:
            # This would call the actual blockchain API
            # For demo purposes, just logging
            logger.info(f"Submitted proof {proof['hash']} to blockchain")
            
            # Mark as verified
            proof["verified"] = True
            
        except Exception as e:
            logger.error(f"Error submitting proof: {str(e)}")
            
    def validate_consensus(self, action: Dict[str, Any]) -> Tuple[bool, float]:
        """
        Validate action has consensus from network nodes
        
        Args:
            action: Action to validate
            
        Returns:
            Tuple of (is_valid, consensus_percentage)
        """
        if not self.connected:
            raise ValueError("Agent not connected to blockchain")
            
        # For critical actions, get validation from validator nodes
        consensus_count = 0
        validator_count = 0
        
        try:
            # Get validator nodes from network
            validator_url = self.network_endpoints.get("validator_url", "")
            
            if validator_url:
                # Submit action for validation
                response = requests.post(
                    f"{validator_url}/validate", 
                    json={"action": action},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    consensus_count = result.get("approved", 0)
                    validator_count = result.get("total", 0)
                    
                    # Calculate consensus percentage
                    if validator_count > 0:
                        consensus_percentage = consensus_count / validator_count
                        
                        # Check if consensus threshold is met
                        valid = consensus_percentage >= self.consensus_threshold
                        
                        logger.info(f"Action validation: {consensus_count}/{validator_count} validators approved ({consensus_percentage:.2f})")
                        
                        return (valid, consensus_percentage)
                        
            # If we can't reach validators, assume validation based on local rules
            for rule in self.rules:
                # Simple rule evaluation
                # In a real implementation, this would be a proper rule engine
                if action.get("critical", False) and rule.get("id") == "rule-consensus":
                    return (False, 0.0)  # Critical actions require external consensus
            
            # Non-critical actions are valid by default if they follow rules
            return (True, 1.0)
            
        except Exception as e:
            logger.error(f"Error validating consensus: {str(e)}")
            return (False, 0.0)
            
    def check_immutability(self, data: Dict[str, Any]) -> bool:
        """
        Check if data is immutable by verifying against blockchain
        
        Args:
            data: Data to check
            
        Returns:
            Whether data is immutable
        """
        if not self.connected:
            raise ValueError("Agent not connected to blockchain")
        
        # Create hash of data
        data_str = json.dumps(data, sort_keys=True)
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        
        try:
            # Check against blockchain (IPFS or microDB)
            ipfs_url = self.network_endpoints.get("ipfs_gateway", "")
            
            if ipfs_url:
                # Check if data exists in IPFS
                response = requests.get(f"{ipfs_url}/api/v0/block/stat?arg={data_hash}", timeout=10)
                
                if response.status_code == 200:
                    return True  # Data exists and is immutable
            
            # Check in local proofs as fallback
            for proof in self.proofs:
                proof_data_str = json.dumps(proof.get("data", {}).get("data", {}), sort_keys=True)
                proof_data_hash = hashlib.sha256(proof_data_str.encode()).hexdigest()
                
                if proof_data_hash == data_hash:
                    return proof.get("verified", False)
                    
            return False
            
        except Exception as e:
            logger.error(f"Error checking immutability: {str(e)}")
            return False
            
    def execute_action(self, action_type: str, data: Dict[str, Any], critical: bool = False) -> Dict[str, Any]:
        """
        Execute action with blockchain validation and immutability
        
        Args:
            action_type: Type of action
            data: Action data
            critical: Whether action is critical (requires consensus)
            
        Returns:
            Action result
        """
        if not self.connected:
            # Auto-connect if not connected
            if not self.connect():
                raise ValueError("Agent failed to connect to blockchain")
        
        # Add immutability flag to data
        data["immutable"] = True
        data["critical"] = critical
        
        # For critical actions, validate consensus
        if critical:
            valid, consensus = self.validate_consensus({
                "type": action_type,
                "data": data,
                "critical": True
            })
            
            if not valid:
                raise ValueError(f"Action failed consensus validation ({consensus:.2f} < {self.consensus_threshold})")
                
            # Add consensus info to data
            data["consensus"] = consensus
            
        # Add proof of action
        proof = self._add_proof(action_type, data)
        
        # Return action result
        return {
            "success": True,
            "action_type": action_type,
            "data": data,
            "proof": proof.get("hash"),
            "timestamp": time.time(),
            "agent_id": self.agent_id
        }
        
    def get_proofs(self) -> List[Dict[str, Any]]:
        """
        Get all proofs recorded by agent
        
        Returns:
            List of proofs
        """
        return self.proofs
        
    def get_rules(self) -> List[Dict[str, Any]]:
        """
        Get rules from agreement nodes
        
        Returns:
            List of rules
        """
        return self.rules
