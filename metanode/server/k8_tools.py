#!/usr/bin/env python3
"""
MetaNode SDK - K8s Server Deployment Tools
=========================================

Tools for deploying and managing applications on Kubernetes for MetaNode servers.
"""

import os
import yaml
import json
import time
import hashlib
import logging
import subprocess
import requests
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL

# Configure logging
logger = logging.getLogger(__name__)

class K8sServerDeployment:
    """Manages Kubernetes deployments for MetaNode servers."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize K8s deployment manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        self.api_url = api_url or API_URL
        self.server_id = None
        self.agreement_file_path = None
        self.resources = None
    
    def register_k8_server(self, resource_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register K8s node to mainnet for mining eligibility.
        
        Args:
            resource_info (dict): Information about server resources with fields:
                - cpu_cores: Number of CPU cores available
                - memory_gb: Amount of RAM in GB
                - storage_gb: Amount of storage in GB
                - gpu_info: GPU information (optional)
                - location: Server geographical location (optional)
                
        Returns:
            dict: Registration result and server ID
        """
        try:
            # Validate required resource information
            required_fields = ["cpu_cores", "memory_gb", "storage_gb"]
            missing = [field for field in required_fields if field not in resource_info]
            if missing:
                return {"status": "error", "message": f"Missing required resource fields: {missing}"}
            
            # Generate a server ID based on hardware specs
            specs_str = f"{resource_info['cpu_cores']}:{resource_info['memory_gb']}:{resource_info['storage_gb']}"
            if "gpu_info" in resource_info:
                specs_str += f":{resource_info['gpu_info']}"
            
            import socket
            hostname = socket.gethostname()
            timestamp = int(time.time())
            
            server_id_input = f"{hostname}:{specs_str}:{timestamp}"
            server_id = hashlib.sha256(server_id_input.encode()).hexdigest()[:16]
            
            # Store resource info
            self.resources = resource_info
            self.server_id = server_id
            
            # Register with the API
            response = requests.post(
                f"{self.api_url}/register_server",
                headers={"Content-Type": "application/json"},
                json={
                    "server_id": server_id,
                    "resources": resource_info,
                    "hostname": hostname,
                    "timestamp": timestamp
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully registered server with ID {server_id}")
                
                # Save server info to local file
                server_info = {
                    "server_id": server_id,
                    "resources": resource_info,
                    "hostname": hostname,
                    "registration_time": timestamp,
                    "registration_response": data
                }
                
                os.makedirs(os.path.join(os.getcwd(), ".metanode"), exist_ok=True)
                server_file_path = os.path.join(os.getcwd(), ".metanode", "server.json")
                
                with open(server_file_path, 'w') as f:
                    json.dump(server_info, f, indent=2)
                
                return {
                    "status": "success",
                    "server_id": server_id,
                    "registration_details": data,
                    "server_file": server_file_path
                }
            else:
                logger.error(f"Server registration failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Server registration error: {e}")
            return {"status": "error", "message": str(e)}
    
    def deploy_app_to_server(self, k8_yaml_path: str) -> Dict[str, Any]:
        """
        Deploy Web2/Web3 app to K8s server and validate integrity.
        
        Args:
            k8_yaml_path (str): Path to Kubernetes YAML configuration
            
        Returns:
            dict: Deployment result and status
        """
        try:
            # Check if the YAML file exists
            if not os.path.exists(k8_yaml_path):
                return {"status": "error", "message": f"K8s YAML file not found: {k8_yaml_path}"}
            
            # Check if we have a registered server
            if not self.server_id:
                return {
                    "status": "error", 
                    "message": "No server ID. Run register_k8_server first."
                }
            
            # Parse the YAML file
            with open(k8_yaml_path, 'r') as f:
                k8_config = yaml.safe_load(f)
            
            # Generate a deployment hash
            file_content = open(k8_yaml_path, 'rb').read()
            deployment_hash = hashlib.sha256(file_content).hexdigest()
            
            # Apply the YAML configuration
            logger.info(f"Applying K8s configuration from {k8_yaml_path}")
            cmd = ["kubectl", "apply", "-f", k8_yaml_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Get deployed resources
                resources = []
                if isinstance(k8_config, dict):
                    kind = k8_config.get("kind")
                    name = k8_config.get("metadata", {}).get("name")
                    namespace = k8_config.get("metadata", {}).get("namespace", "default")
                    resources.append({"kind": kind, "name": name, "namespace": namespace})
                elif isinstance(k8_config, list):
                    for item in k8_config:
                        if isinstance(item, dict):
                            kind = item.get("kind")
                            name = item.get("metadata", {}).get("name")
                            namespace = item.get("metadata", {}).get("namespace", "default")
                            resources.append({"kind": kind, "name": name, "namespace": namespace})
                
                # Notify the API about the deployment
                response = requests.post(
                    f"{self.api_url}/deploy_app",
                    headers={"Content-Type": "application/json"},
                    json={
                        "server_id": self.server_id,
                        "deployment_hash": deployment_hash,
                        "resources": resources,
                        "timestamp": int(time.time())
                    }
                )
                
                deployment_response = {}
                if response.status_code == 200:
                    deployment_response = response.json()
                
                # Store deployment information
                deployment_info = {
                    "server_id": self.server_id,
                    "deployment_hash": deployment_hash,
                    "resources": resources,
                    "command_output": result.stdout,
                    "deployment_time": int(time.time()),
                    "api_response": deployment_response
                }
                
                deployments_dir = os.path.join(os.getcwd(), ".metanode", "deployments")
                os.makedirs(deployments_dir, exist_ok=True)
                
                deployment_file = os.path.join(deployments_dir, f"deployment-{int(time.time())}.json")
                with open(deployment_file, 'w') as f:
                    json.dump(deployment_info, f, indent=2)
                
                logger.info(f"Successfully deployed app: {result.stdout}")
                return {
                    "status": "success",
                    "deployment_hash": deployment_hash,
                    "resources": resources,
                    "output": result.stdout,
                    "deployment_file": deployment_file
                }
            else:
                error_message = result.stderr
                logger.error(f"Deployment failed: {error_message}")
                return {"status": "error", "message": error_message}
                
        except Exception as e:
            logger.error(f"Deployment error: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_agreement_file(self, app_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate agreement.deploy.lock for syncing with client/app.
        
        Args:
            app_info (dict): Application information with fields:
                - app_name: Name of the application
                - version: Application version
                - resources: Resource requirements
                - duration: Expected agreement duration in seconds
                
        Returns:
            dict: Agreement file information
        """
        try:
            # Validate required application information
            required_fields = ["app_name", "version", "resources"]
            missing = [field for field in required_fields if field not in app_info]
            if missing:
                return {"status": "error", "message": f"Missing required app fields: {missing}"}
            
            # Check if we have a registered server
            if not self.server_id:
                return {
                    "status": "error", 
                    "message": "No server ID. Run register_k8_server first."
                }
            
            # Generate a unique agreement ID
            timestamp = int(time.time())
            agreement_id_input = f"{self.server_id}:{app_info['app_name']}:{app_info['version']}:{timestamp}"
            agreement_id = hashlib.sha256(agreement_id_input.encode()).hexdigest()[:16]
            
            # Create agreement content
            agreement = {
                "agreement_id": agreement_id,
                "server_id": self.server_id,
                "app": {
                    "name": app_info["app_name"],
                    "version": app_info["version"]
                },
                "resources": app_info["resources"],
                "created_at": timestamp,
                "expires_at": timestamp + app_info.get("duration", 86400),  # Default 24h
                "status": "created"
            }
            
            # Save agreement to file
            agreements_dir = os.path.join(os.getcwd(), ".metanode", "agreements")
            os.makedirs(agreements_dir, exist_ok=True)
            
            agreement_file_path = os.path.join(agreements_dir, f"agreement.deploy.{agreement_id}.lock")
            with open(agreement_file_path, 'w') as f:
                json.dump(agreement, f, indent=2)
            
            # Store the path
            self.agreement_file_path = agreement_file_path
            
            # Register agreement with the API
            response = requests.post(
                f"{self.api_url}/register_agreement",
                headers={"Content-Type": "application/json"},
                json=agreement
            )
            
            api_response = {}
            if response.status_code == 200:
                api_response = response.json()
                logger.info(f"Successfully registered agreement {agreement_id} with API")
            else:
                logger.warning(f"Failed to register agreement with API: {response.text}")
            
            return {
                "status": "success",
                "agreement_id": agreement_id,
                "agreement_file": agreement_file_path,
                "api_response": api_response
            }
                
        except Exception as e:
            logger.error(f"Agreement generation error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create K8s deployment manager
    k8s_manager = K8sServerDeployment()
    
    # Register server with resource information
    resource_info = {
        "cpu_cores": 4,
        "memory_gb": 16,
        "storage_gb": 100,
        "gpu_info": "NVIDIA T4",
        "location": "us-west"
    }
    
    register_result = k8s_manager.register_k8_server(resource_info)
    print(f"Server registration: {json.dumps(register_result, indent=2)}")
    
    # Generate an agreement for a sample application
    app_info = {
        "app_name": "sample-web-app",
        "version": "1.0.0",
        "resources": {
            "cpu": "500m",
            "memory": "512Mi",
            "storage": "1Gi"
        },
        "duration": 3600  # 1 hour
    }
    
    agreement_result = k8s_manager.generate_agreement_file(app_info)
    print(f"Agreement generation: {json.dumps(agreement_result, indent=2)}")
    
    # Deploy a sample application
    # (assuming you have a sample k8s.yaml file)
    # deploy_result = k8s_manager.deploy_app_to_server("./sample-app-k8s.yaml")
    # print(f"Deployment result: {json.dumps(deploy_result, indent=2)}")
