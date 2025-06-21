#!/usr/bin/env python3
"""
MetaNode SDK - Admin Node Manager Module
======================================

Tools for administrators to manage MetaNode testnet nodes and infrastructure.
"""

import os
import json
import time
import logging
import requests
import subprocess
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL, BLOCKCHAIN_URL

# Configure logging
logger = logging.getLogger(__name__)

class NodeManager:
    """Manages MetaNode testnet nodes and infrastructure."""
    
    def __init__(self, api_url: Optional[str] = None, admin_key: Optional[str] = None):
        """
        Initialize node manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            admin_key (str, optional): Admin API key for authentication
        """
        self.api_url = api_url or API_URL
        self.admin_key = admin_key
        self.admin_dir = os.path.join(os.getcwd(), ".metanode", "admin")
        
        # Ensure admin directory exists
        os.makedirs(self.admin_dir, exist_ok=True)
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for admin API calls."""
        headers = {"Content-Type": "application/json"}
        if self.admin_key:
            headers["X-Admin-Key"] = self.admin_key
        return headers
    
    def list_nodes(self, node_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List all registered nodes in the testnet.
        
        Args:
            node_type (str, optional): Filter by node type (validator, api, blockchain, etc.)
            
        Returns:
            dict: List of nodes
        """
        try:
            # Build query parameters
            params = {}
            if node_type:
                params["type"] = node_type
            
            # Query API for nodes
            response = requests.get(
                f"{self.api_url}/admin/nodes",
                headers=self._get_auth_headers(),
                params=params
            )
            
            if response.status_code == 200:
                nodes_data = response.json()
                
                # Save nodes information
                nodes_file = os.path.join(self.admin_dir, f"nodes-{int(time.time())}.json")
                with open(nodes_file, 'w') as f:
                    json.dump(nodes_data, f, indent=2)
                
                nodes = nodes_data.get("nodes", [])
                logger.info(f"Retrieved {len(nodes)} nodes")
                return {
                    "status": "success",
                    "nodes": nodes,
                    "count": len(nodes),
                    "nodes_file": nodes_file
                }
            else:
                logger.error(f"Failed to list nodes: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Node listing error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_node_status(self, node_id: str) -> Dict[str, Any]:
        """
        Get detailed status of a specific node.
        
        Args:
            node_id (str): ID of the node
            
        Returns:
            dict: Node status
        """
        try:
            # Query API for node status
            response = requests.get(
                f"{self.api_url}/admin/nodes/{node_id}",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                node_data = response.json()
                
                # Save node status
                status_file = os.path.join(self.admin_dir, f"node-{node_id}-{int(time.time())}.json")
                with open(status_file, 'w') as f:
                    json.dump(node_data, f, indent=2)
                
                logger.info(f"Retrieved status for node {node_id}")
                return {
                    "status": "success",
                    "node_id": node_id,
                    "node_data": node_data,
                    "status_file": status_file
                }
            else:
                logger.error(f"Failed to get node status: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Node status error: {e}")
            return {"status": "error", "message": str(e)}
    
    def restart_node(self, node_id: str) -> Dict[str, Any]:
        """
        Restart a specific node.
        
        Args:
            node_id (str): ID of the node to restart
            
        Returns:
            dict: Restart operation result
        """
        try:
            # Send restart command to API
            response = requests.post(
                f"{self.api_url}/admin/nodes/{node_id}/restart",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                result = response.json()
                
                logger.info(f"Restarted node {node_id}")
                return {
                    "status": "success",
                    "node_id": node_id,
                    "restart_result": result
                }
            else:
                logger.error(f"Failed to restart node: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Node restart error: {e}")
            return {"status": "error", "message": str(e)}
    
    def update_node(self, node_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update node configuration.
        
        Args:
            node_id (str): ID of the node to update
            config (dict): New configuration parameters
            
        Returns:
            dict: Update operation result
        """
        try:
            # Send update command to API
            response = requests.put(
                f"{self.api_url}/admin/nodes/{node_id}/config",
                headers=self._get_auth_headers(),
                json=config
            )
            
            if response.status_code == 200:
                result = response.json()
                
                logger.info(f"Updated node {node_id} configuration")
                return {
                    "status": "success",
                    "node_id": node_id,
                    "update_result": result
                }
            else:
                logger.error(f"Failed to update node: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Node update error: {e}")
            return {"status": "error", "message": str(e)}
    
    def deploy_node(self, node_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy a new node to the testnet.
        
        Args:
            node_type (str): Type of node to deploy
            config (dict): Node configuration
            
        Returns:
            dict: Deployment result
        """
        try:
            # Send deployment request to API
            response = requests.post(
                f"{self.api_url}/admin/nodes/deploy",
                headers=self._get_auth_headers(),
                json={
                    "node_type": node_type,
                    "config": config
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                node_id = result.get("node_id")
                
                # Save deployment information
                deployment_file = os.path.join(self.admin_dir, f"deploy-{node_id}-{int(time.time())}.json")
                with open(deployment_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                logger.info(f"Deployed new {node_type} node with ID {node_id}")
                return {
                    "status": "success",
                    "node_id": node_id,
                    "node_type": node_type,
                    "deployment_result": result,
                    "deployment_file": deployment_file
                }
            else:
                logger.error(f"Failed to deploy node: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Node deployment error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_network_stats(self) -> Dict[str, Any]:
        """
        Get network-wide statistics.
        
        Returns:
            dict: Network statistics
        """
        try:
            # Query API for network stats
            response = requests.get(
                f"{self.api_url}/admin/network/stats",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                stats_data = response.json()
                
                # Save network stats
                stats_file = os.path.join(self.admin_dir, f"network-stats-{int(time.time())}.json")
                with open(stats_file, 'w') as f:
                    json.dump(stats_data, f, indent=2)
                
                logger.info(f"Retrieved network statistics")
                return {
                    "status": "success",
                    "stats": stats_data,
                    "stats_file": stats_file
                }
            else:
                logger.error(f"Failed to get network stats: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Network stats error: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_active_agreements(self) -> Dict[str, Any]:
        """
        List all active agreements in the testnet.
        
        Returns:
            dict: List of active agreements
        """
        try:
            # Query API for active agreements
            response = requests.get(
                f"{self.api_url}/admin/agreements/active",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                agreements_data = response.json()
                
                # Save agreements information
                agreements_file = os.path.join(self.admin_dir, f"agreements-{int(time.time())}.json")
                with open(agreements_file, 'w') as f:
                    json.dump(agreements_data, f, indent=2)
                
                agreements = agreements_data.get("agreements", [])
                logger.info(f"Retrieved {len(agreements)} active agreements")
                return {
                    "status": "success",
                    "agreements": agreements,
                    "count": len(agreements),
                    "agreements_file": agreements_file
                }
            else:
                logger.error(f"Failed to list agreements: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Agreement listing error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create node manager
    manager = NodeManager(admin_key="sample-admin-key")
    
    # List nodes
    nodes_result = manager.list_nodes()
    print(f"Nodes: {json.dumps(nodes_result, indent=2)}")
    
    # Get network stats
    stats_result = manager.get_network_stats()
    print(f"Network stats: {json.dumps(stats_result, indent=2)}")
