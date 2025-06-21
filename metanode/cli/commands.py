#!/usr/bin/env python3
"""
MetaNode SDK - CLI Command Implementations
==========================================

This module contains the implementation logic for the MetaNode CLI commands.
"""

import os
import json
import time
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from ..admin.k8s_manager import K8sManager
from ..admin.security import SecurityManager
from ..utils.ipfs_tools import IPFSManager
from ..utils.zk_proofs import ZKProofManager

logger = logging.getLogger("metanode-cli-commands")

# K8s management commands
class K8sCommands:
    def __init__(self, admin_key: Optional[str] = None):
        """
        Initialize K8s commands with optional admin API key.
        
        Args:
            admin_key: Admin API key for authorized operations
        """
        self.admin_key = admin_key
        self.k8s_manager = K8sManager(admin_key=admin_key)
        self.data_dir = Path(os.path.expanduser("~/.metanode/admin/k8s"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cluster_info(self) -> Dict[str, Any]:
        """Get Kubernetes cluster information."""
        try:
            result = self.k8s_manager.get_cluster_info()
            # Save cluster info for future reference
            with open(self.data_dir / "cluster_info.json", "w") as f:
                json.dump(result, f, indent=2)
            return result
        except Exception as e:
            logger.error(f"Failed to get cluster info: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_nodes(self) -> Dict[str, Any]:
        """List Kubernetes nodes and their labels."""
        try:
            result = self.k8s_manager.list_nodes()
            # Format nodes with their testnet status
            formatted_nodes = []
            for node in result.get("nodes", []):
                testnet_node = "testnet-node" in node.get("labels", {}) and node["labels"]["testnet-node"] == "true"
                app_node = "app-node" in node.get("labels", {}) and node["labels"]["app-node"] == "true"
                
                node_type = "Unknown"
                if testnet_node:
                    node_type = "Testnet Node"
                elif app_node:
                    node_type = "Application Node"
                
                formatted_nodes.append({
                    "name": node["name"],
                    "type": node_type,
                    "ready": node["ready"],
                    "labels": node["labels"]
                })
            
            return {
                "status": "success",
                "nodes": formatted_nodes,
                "count": len(formatted_nodes)
            }
        except Exception as e:
            logger.error(f"Failed to list nodes: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_cryptographic_key(self) -> Dict[str, Any]:
        """Generate a new cryptographic key for node authentication."""
        try:
            result = self.k8s_manager.generate_node_crypt_key()
            return result
        except Exception as e:
            logger.error(f"Failed to generate cryptographic key: {e}")
            return {"status": "error", "message": str(e)}
    
    def register_node(self, node_name: str, key_id: str, is_testnet: bool = True) -> Dict[str, Any]:
        """
        Register a Kubernetes node with the MetaNode testnet.
        
        Args:
            node_name: Name of the Kubernetes node to register
            key_id: ID of the cryptographic key to use
            is_testnet: Whether this will be a testnet node (True) or app node (False)
        """
        try:
            result = self.k8s_manager.register_node_with_testnet(node_name, key_id, is_testnet)
            return result
        except Exception as e:
            logger.error(f"Failed to register node {node_name}: {e}")
            return {"status": "error", "message": str(e)}
    
    def deploy_testnet_node(self, node_id: str, node_name: str) -> Dict[str, Any]:
        """
        Deploy a testnet node to Kubernetes.
        
        Args:
            node_id: ID of the registered node
            node_name: Name of the Kubernetes node
        """
        try:
            result = self.k8s_manager.deploy_testnet_node(node_id, node_name)
            return result
        except Exception as e:
            logger.error(f"Failed to deploy testnet node {node_id}: {e}")
            return {"status": "error", "message": str(e)}
    
    def deploy_application(self, 
                          app_name: str, 
                          image: str,
                          node_name: Optional[str] = None, 
                          replicas: int = 1,
                          ports: Optional[List[int]] = None,
                          env_vars: Optional[Dict[str, str]] = None,
                          storage_size: str = "1Gi") -> Dict[str, Any]:
        """
        Deploy an application to a Kubernetes node.
        
        Args:
            app_name: Name of the application to deploy
            image: Docker image to use for the application
            node_name: Name of the Kubernetes node to deploy to (optional)
            replicas: Number of replicas to deploy
            ports: List of ports to expose
            env_vars: Environment variables to set
            storage_size: Size of the persistent volume claim
        """
        try:
            if ports is None:
                ports = [8080]
            
            if env_vars is None:
                env_vars = {}
            
            result = self.k8s_manager.deploy_application(
                app_name=app_name,
                image=image,
                node_name=node_name,
                replicas=replicas,
                ports=ports,
                env_vars=env_vars,
                storage_size=storage_size
            )
            return result
        except Exception as e:
            logger.error(f"Failed to deploy application {app_name}: {e}")
            return {"status": "error", "message": str(e)}
    
    def setup_testnet_sync(self) -> Dict[str, Any]:
        """Set up testnet node synchronization."""
        try:
            result = self.k8s_manager.setup_testnet_sync()
            return result
        except Exception as e:
            logger.error(f"Failed to set up testnet sync: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_deployment_status(self, deployment_name: str) -> Dict[str, Any]:
        """
        Get the status of a Kubernetes deployment.
        
        Args:
            deployment_name: Name of the deployment to check
        """
        try:
            result = self.k8s_manager.get_deployment_status(deployment_name)
            return result
        except Exception as e:
            logger.error(f"Failed to get status for deployment {deployment_name}: {e}")
            return {"status": "error", "message": str(e)}
    
    def apply_yaml_file(self, yaml_path: str) -> Dict[str, Any]:
        """
        Apply a YAML file to the Kubernetes cluster.
        
        Args:
            yaml_path: Path to the YAML file
        """
        try:
            result = self.k8s_manager.apply_yaml_file(yaml_path)
            return result
        except Exception as e:
            logger.error(f"Failed to apply YAML file {yaml_path}: {e}")
            return {"status": "error", "message": str(e)}

# Security management commands
class SecurityCommands:
    def __init__(self, admin_key: Optional[str] = None):
        """
        Initialize security commands with optional admin API key.
        
        Args:
            admin_key: Admin API key for authorized operations
        """
        self.admin_key = admin_key
        self.security_manager = SecurityManager(admin_key=admin_key)
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get the current security status of the testnet."""
        try:
            result = self.security_manager.get_security_status()
            return result
        except Exception as e:
            logger.error(f"Failed to get security status: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_api_key(self, username: str, scope: str = "standard") -> Dict[str, Any]:
        """
        Generate a new API key for a user.
        
        Args:
            username: Username to generate the key for
            scope: Scope of access ('standard', 'admin', 'readonly')
        """
        try:
            result = self.security_manager.generate_api_key(username, scope)
            return result
        except Exception as e:
            logger.error(f"Failed to generate API key for {username}: {e}")
            return {"status": "error", "message": str(e)}
    
    def revoke_api_key(self, key_id: str) -> Dict[str, Any]:
        """
        Revoke an API key.
        
        Args:
            key_id: ID of the API key to revoke
        """
        try:
            result = self.security_manager.revoke_api_key(key_id)
            return result
        except Exception as e:
            logger.error(f"Failed to revoke API key {key_id}: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_firewall_rule(self, 
                            rule_name: str,
                            source_ip: str,
                            destination: str,
                            action: str = "allow",
                            priority: int = 100) -> Dict[str, Any]:
        """
        Create a new firewall rule.
        
        Args:
            rule_name: Name of the rule
            source_ip: Source IP/CIDR
            destination: Destination (service or node)
            action: Action to take (allow/deny)
            priority: Rule priority (lower is higher priority)
        """
        try:
            result = self.security_manager.create_firewall_rule(
                rule_name, source_ip, destination, action, priority)
            return result
        except Exception as e:
            logger.error(f"Failed to create firewall rule {rule_name}: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_audit_report(self, 
                             start_date: Optional[str] = None,
                             end_date: Optional[str] = None,
                             report_type: str = "full") -> Dict[str, Any]:
        """
        Generate a security audit report.
        
        Args:
            start_date: Start date for the report (ISO format)
            end_date: End date for the report (ISO format)
            report_type: Type of report (full, access, network, critical)
        """
        try:
            result = self.security_manager.generate_audit_report(
                start_date, end_date, report_type)
            return result
        except Exception as e:
            logger.error(f"Failed to generate audit report: {e}")
            return {"status": "error", "message": str(e)}

# IPFS utility commands
class IPFSCommands:
    def __init__(self):
        """Initialize IPFS commands."""
        self.ipfs_manager = IPFSManager()
    
    def add_file(self, file_path: str) -> Dict[str, Any]:
        """
        Add a file to IPFS.
        
        Args:
            file_path: Path to the file to add
        """
        try:
            result = self.ipfs_manager.add_file(file_path)
            return result
        except Exception as e:
            logger.error(f"Failed to add file to IPFS: {e}")
            return {"status": "error", "message": str(e)}
    
    def add_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a JSON object to IPFS.
        
        Args:
            data: JSON object to add
        """
        try:
            result = self.ipfs_manager.add_json(data)
            return result
        except Exception as e:
            logger.error(f"Failed to add JSON to IPFS: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_file(self, ipfs_hash: str, output_path: str) -> Dict[str, Any]:
        """
        Get a file from IPFS.
        
        Args:
            ipfs_hash: IPFS hash of the file
            output_path: Path to save the file to
        """
        try:
            result = self.ipfs_manager.get_file(ipfs_hash, output_path)
            return result
        except Exception as e:
            logger.error(f"Failed to get file from IPFS: {e}")
            return {"status": "error", "message": str(e)}

# ZK Proof utility commands
class ZKProofCommands:
    def __init__(self):
        """Initialize ZK Proof commands."""
        self.zk_manager = ZKProofManager()
    
    def generate_proof(self, data: Dict[str, Any], circuit_id: str) -> Dict[str, Any]:
        """
        Generate a zero-knowledge proof.
        
        Args:
            data: Data to prove
            circuit_id: ID of the circuit to use
        """
        try:
            result = self.zk_manager.generate_proof(data, circuit_id)
            return result
        except Exception as e:
            logger.error(f"Failed to generate proof: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_proof(self, proof_data: Dict[str, Any], circuit_id: str) -> Dict[str, Any]:
        """
        Verify a zero-knowledge proof.
        
        Args:
            proof_data: Proof data
            circuit_id: ID of the circuit used
        """
        try:
            result = self.zk_manager.verify_proof(proof_data, circuit_id)
            return result
        except Exception as e:
            logger.error(f"Failed to verify proof: {e}")
            return {"status": "error", "message": str(e)}
