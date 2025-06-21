#!/usr/bin/env python3
"""
MetaNode SDK - vPod Administration Tools
======================================

Tools for managing virtual pods (vPods) in the MetaNode ecosystem.
"""

import os
import json
import time
import logging
import subprocess
import requests
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL, BLOCKCHAIN_URL

# Configure logging
logger = logging.getLogger(__name__)

class VPodManager:
    """Manages virtual pods (vPods) in the MetaNode ecosystem."""
    
    def __init__(self, api_url: Optional[str] = None, admin_key: Optional[str] = None):
        """
        Initialize vPod manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            admin_key (str, optional): Admin API key for authentication
        """
        self.api_url = api_url or API_URL
        self.admin_key = admin_key
        self.admin_dir = os.path.join(os.getcwd(), ".metanode", "admin")
        self.vpod_dir = os.path.join(self.admin_dir, "vpods")
        
        # Ensure directories exist
        os.makedirs(self.vpod_dir, exist_ok=True)
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for admin API calls."""
        headers = {"Content-Type": "application/json"}
        if self.admin_key:
            headers["X-Admin-Key"] = self.admin_key
        return headers
    
    def list_vpods(self) -> Dict[str, Any]:
        """
        List all vPods in the system.
        
        Returns:
            dict: List of vPods
        """
        try:
            # Query API for vPods
            response = requests.get(
                f"{self.api_url}/admin/vpods",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                vpods_data = response.json()
                
                # Save vPods information
                vpods_file = os.path.join(self.vpod_dir, f"vpods-list-{int(time.time())}.json")
                with open(vpods_file, 'w') as f:
                    json.dump(vpods_data, f, indent=2)
                
                vpods = vpods_data.get("vpods", [])
                logger.info(f"Retrieved {len(vpods)} vPods")
                return {
                    "status": "success",
                    "vpods": vpods,
                    "count": len(vpods),
                    "vpods_file": vpods_file
                }
            else:
                logger.error(f"Failed to list vPods: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod listing error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_vpod_status(self, vpod_id: str) -> Dict[str, Any]:
        """
        Get detailed status of a specific vPod.
        
        Args:
            vpod_id (str): ID of the vPod
            
        Returns:
            dict: vPod status
        """
        try:
            # Query API for vPod status
            response = requests.get(
                f"{self.api_url}/admin/vpods/{vpod_id}",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                vpod_data = response.json()
                
                # Save vPod status
                status_file = os.path.join(self.vpod_dir, f"vpod-{vpod_id}-{int(time.time())}.json")
                with open(status_file, 'w') as f:
                    json.dump(vpod_data, f, indent=2)
                
                logger.info(f"Retrieved status for vPod {vpod_id}")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "vpod_data": vpod_data,
                    "status_file": status_file
                }
            else:
                logger.error(f"Failed to get vPod status: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod status error: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_vpod(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new vPod with the specified configuration.
        
        Args:
            config (dict): vPod configuration
            
        Returns:
            dict: Creation operation result
        """
        try:
            # Send create command to API
            response = requests.post(
                f"{self.api_url}/admin/vpods",
                headers=self._get_auth_headers(),
                json=config
            )
            
            if response.status_code == 200:
                result = response.json()
                vpod_id = result.get("vpod_id")
                
                # Save creation information
                creation_file = os.path.join(self.vpod_dir, f"vpod-create-{vpod_id}-{int(time.time())}.json")
                with open(creation_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                logger.info(f"Created vPod with ID {vpod_id}")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "creation_result": result,
                    "creation_file": creation_file
                }
            else:
                logger.error(f"Failed to create vPod: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod creation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def update_vpod(self, vpod_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update vPod configuration.
        
        Args:
            vpod_id (str): ID of the vPod to update
            config (dict): New configuration parameters
            
        Returns:
            dict: Update operation result
        """
        try:
            # Send update command to API
            response = requests.put(
                f"{self.api_url}/admin/vpods/{vpod_id}",
                headers=self._get_auth_headers(),
                json=config
            )
            
            if response.status_code == 200:
                result = response.json()
                
                logger.info(f"Updated vPod {vpod_id} configuration")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "update_result": result
                }
            else:
                logger.error(f"Failed to update vPod: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod update error: {e}")
            return {"status": "error", "message": str(e)}
    
    def start_vpod(self, vpod_id: str) -> Dict[str, Any]:
        """
        Start a specific vPod.
        
        Args:
            vpod_id (str): ID of the vPod to start
            
        Returns:
            dict: Start operation result
        """
        try:
            # Send start command to API
            response = requests.post(
                f"{self.api_url}/admin/vpods/{vpod_id}/start",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                result = response.json()
                
                logger.info(f"Started vPod {vpod_id}")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "start_result": result
                }
            else:
                logger.error(f"Failed to start vPod: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod start error: {e}")
            return {"status": "error", "message": str(e)}
    
    def stop_vpod(self, vpod_id: str) -> Dict[str, Any]:
        """
        Stop a specific vPod.
        
        Args:
            vpod_id (str): ID of the vPod to stop
            
        Returns:
            dict: Stop operation result
        """
        try:
            # Send stop command to API
            response = requests.post(
                f"{self.api_url}/admin/vpods/{vpod_id}/stop",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                result = response.json()
                
                logger.info(f"Stopped vPod {vpod_id}")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "stop_result": result
                }
            else:
                logger.error(f"Failed to stop vPod: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod stop error: {e}")
            return {"status": "error", "message": str(e)}
    
    def delete_vpod(self, vpod_id: str) -> Dict[str, Any]:
        """
        Delete a specific vPod.
        
        Args:
            vpod_id (str): ID of the vPod to delete
            
        Returns:
            dict: Delete operation result
        """
        try:
            # Send delete command to API
            response = requests.delete(
                f"{self.api_url}/admin/vpods/{vpod_id}",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                result = response.json()
                
                logger.info(f"Deleted vPod {vpod_id}")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "delete_result": result
                }
            else:
                logger.error(f"Failed to delete vPod: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod deletion error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_vpod_logs(self, vpod_id: str, lines: int = 100) -> Dict[str, Any]:
        """
        Get logs from a specific vPod.
        
        Args:
            vpod_id (str): ID of the vPod
            lines (int): Number of log lines to retrieve
            
        Returns:
            dict: vPod logs
        """
        try:
            # Query API for vPod logs
            response = requests.get(
                f"{self.api_url}/admin/vpods/{vpod_id}/logs",
                headers=self._get_auth_headers(),
                params={"lines": lines}
            )
            
            if response.status_code == 200:
                logs_data = response.json()
                
                # Save logs information
                logs_file = os.path.join(self.vpod_dir, f"vpod-{vpod_id}-logs-{int(time.time())}.json")
                with open(logs_file, 'w') as f:
                    json.dump(logs_data, f, indent=2)
                
                logs = logs_data.get("logs", [])
                logger.info(f"Retrieved {len(logs)} log lines for vPod {vpod_id}")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "logs": logs,
                    "count": len(logs),
                    "logs_file": logs_file
                }
            else:
                logger.error(f"Failed to get vPod logs: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"vPod logs error: {e}")
            return {"status": "error", "message": str(e)}

    def use_existing_vpod(self, vpod_id: str, operation_id: str) -> Dict[str, Any]:
        """
        Configure an operation to use an existing vPod container.
        
        Args:
            vpod_id (str): ID of the existing vPod to use
            operation_id (str): ID of the operation to configure
            
        Returns:
            dict: Configuration result
        """
        try:
            # Send configuration command to API
            response = requests.post(
                f"{self.api_url}/admin/operations/{operation_id}/use_existing_vpod",
                headers=self._get_auth_headers(),
                json={"vpod_id": vpod_id}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Save configuration information
                config_file = os.path.join(
                    self.vpod_dir, 
                    f"operation-{operation_id}-vpod-{vpod_id}-{int(time.time())}.json"
                )
                with open(config_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                logger.info(f"Configured operation {operation_id} to use existing vPod {vpod_id}")
                return {
                    "status": "success",
                    "vpod_id": vpod_id,
                    "operation_id": operation_id,
                    "config_result": result,
                    "config_file": config_file
                }
            else:
                logger.error(f"Failed to configure operation: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Operation configuration error: {e}")
            return {"status": "error", "message": str(e)}
    
    def check_vpod_docker(self, vpod_id: str) -> Dict[str, Any]:
        """
        Check if a vPod's Docker container exists locally.
        
        Args:
            vpod_id (str): ID of the vPod
            
        Returns:
            dict: Container existence result
        """
        try:
            # Run docker command
            container_name = f"metanode-vpod-{vpod_id}"
            result = subprocess.run(
                ["docker", "ps", "-a", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
                capture_output=True,
                text=True
            )
            
            # Check if container exists
            output = result.stdout.strip()
            exists = container_name in output
            
            logger.info(f"vPod {vpod_id} Docker container {'exists' if exists else 'does not exist'}")
            return {
                "status": "success",
                "vpod_id": vpod_id,
                "container_name": container_name,
                "exists": exists,
                "output": output
            }
                
        except Exception as e:
            logger.error(f"Docker check error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create vPod manager
    vpod_manager = VPodManager(admin_key="sample-admin-key")
    
    # List vPods
    vpods_result = vpod_manager.list_vpods()
    print(f"vPods: {json.dumps(vpods_result, indent=2)}")
