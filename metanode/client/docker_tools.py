#!/usr/bin/env python3
"""
MetaNode SDK - Client Docker Deployment Tools
===========================================

Tools for deploying and managing Docker containers in the MetaNode ecosystem.
"""

import os
import json
import time
import hashlib
import logging
import subprocess
import requests
from typing import Dict, Any, Optional, List, Union

# Configure logging
logger = logging.getLogger(__name__)

class DockerDeployment:
    """Manages Docker deployment for MetaNode client applications."""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize Docker deployment manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
        """
        from ..config.endpoints import API_URL
        self.api_url = api_url or API_URL
        self.docker_lock_path = None
        self.app_name = None
        self.agreement_hash = None
        self.server_id = None
    
    def init_docker_lock(self, app_name: str, image_name: str, 
                        version: str = "latest") -> Dict[str, Any]:
        """
        Generate docker.lock file with agreement hash and image metadata.
        
        Args:
            app_name (str): Name of the application
            image_name (str): Docker image name
            version (str): Docker image version/tag
            
        Returns:
            dict: Information about the generated docker.lock file
        """
        try:
            # Create unique identifier based on app and timestamp
            timestamp = int(time.time())
            app_id = f"{app_name}-{timestamp}"
            
            # Generate a hash for the application deployment
            hash_input = f"{app_name}:{image_name}:{version}:{timestamp}"
            agreement_hash = hashlib.sha256(hash_input.encode()).hexdigest()
            
            # Create docker.lock content
            docker_lock = {
                "app_id": app_id,
                "app_name": app_name,
                "image": {
                    "name": image_name,
                    "version": version
                },
                "created_at": timestamp,
                "agreement_hash": agreement_hash,
                "status": "initialized"
            }
            
            # Save to file in current directory
            lock_dir = os.path.join(os.getcwd(), ".metanode")
            os.makedirs(lock_dir, exist_ok=True)
            
            lock_file_path = os.path.join(lock_dir, "docker.lock")
            with open(lock_file_path, 'w') as f:
                json.dump(docker_lock, f, indent=2)
            
            # Update instance state
            self.docker_lock_path = lock_file_path
            self.app_name = app_name
            self.agreement_hash = agreement_hash
            
            logger.info(f"Created docker.lock for {app_name} at {lock_file_path}")
            return {
                "status": "success",
                "app_id": app_id,
                "lock_file": lock_file_path,
                "agreement_hash": agreement_hash
            }
            
        except Exception as e:
            logger.error(f"Failed to initialize docker lock: {e}")
            return {"status": "error", "message": str(e)}
    
    def deploy_client_docker(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy Docker container and bind to testnet.
        
        Args:
            config (dict): Deployment configuration with the following fields:
                - image_name: Docker image name
                - container_name: Desired container name
                - env_vars: Dictionary of environment variables
                - ports: Dictionary mapping host ports to container ports
                - volumes: List of volume mappings
                
        Returns:
            dict: Deployment result with container ID and status
        """
        try:
            # Validate config
            required_fields = ["image_name"]
            missing = [field for field in required_fields if field not in config]
            if missing:
                return {"status": "error", "message": f"Missing required fields: {missing}"}
            
            # Set default values
            image_name = config["image_name"]
            container_name = config.get("container_name", f"metanode-{int(time.time())}")
            env_vars = config.get("env_vars", {})
            ports = config.get("ports", {})
            volumes = config.get("volumes", [])
            
            # Build Docker run command
            cmd = ["docker", "run", "-d", "--name", container_name]
            
            # Add environment variables
            for key, value in env_vars.items():
                cmd.extend(["-e", f"{key}={value}"])
            
            # Add port mappings
            for host_port, container_port in ports.items():
                cmd.extend(["-p", f"{host_port}:{container_port}"])
            
            # Add volume mappings
            for volume in volumes:
                cmd.extend(["-v", volume])
            
            # Add the MetaNode specific environment to connect to testnet
            if self.agreement_hash:
                cmd.extend(["-e", f"METANODE_AGREEMENT_HASH={self.agreement_hash}"])
            
            # Add the image name
            cmd.append(image_name)
            
            # Execute the Docker command
            logger.info(f"Executing Docker command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                container_id = result.stdout.strip()
                
                # Update docker.lock file if it exists
                if self.docker_lock_path:
                    with open(self.docker_lock_path, 'r') as f:
                        lock_data = json.load(f)
                    
                    lock_data["status"] = "deployed"
                    lock_data["container_id"] = container_id
                    lock_data["deployed_at"] = int(time.time())
                    
                    with open(self.docker_lock_path, 'w') as f:
                        json.dump(lock_data, f, indent=2)
                
                return {
                    "status": "success",
                    "container_id": container_id,
                    "container_name": container_name
                }
            else:
                error_message = result.stderr.strip()
                logger.error(f"Docker deployment failed: {error_message}")
                return {"status": "error", "message": error_message}
                
        except Exception as e:
            logger.error(f"Docker deployment error: {e}")
            return {"status": "error", "message": str(e)}
    
    def bind_to_server(self, server_id: str) -> Dict[str, Any]:
        """
        Link client docker to running k8s server in the mesh.
        
        Args:
            server_id (str): ID of the server to bind to
            
        Returns:
            dict: Binding result and status
        """
        try:
            # Check if we have a valid agreement hash
            if not self.agreement_hash:
                return {
                    "status": "error", 
                    "message": "No agreement hash available. Run init_docker_lock first."
                }
            
            # Make a binding request to the API
            response = requests.post(
                f"{self.api_url}/bind",
                headers={"Content-Type": "application/json"},
                json={
                    "server_id": server_id,
                    "agreement_hash": self.agreement_hash,
                    "app_name": self.app_name
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.server_id = server_id
                
                # Update docker.lock file if it exists
                if self.docker_lock_path:
                    with open(self.docker_lock_path, 'r') as f:
                        lock_data = json.load(f)
                    
                    lock_data["bound_server_id"] = server_id
                    lock_data["binding_time"] = int(time.time())
                    
                    with open(self.docker_lock_path, 'w') as f:
                        json.dump(lock_data, f, indent=2)
                
                logger.info(f"Successfully bound to server {server_id}")
                return {
                    "status": "success",
                    "server_id": server_id,
                    "binding_details": data
                }
            else:
                logger.error(f"Binding failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Server binding error: {e}")
            return {"status": "error", "message": str(e)}
    
    def send_message_to_server(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send proof-logged message from client to server via /message.
        
        Args:
            payload (dict): Message payload to send
            
        Returns:
            dict: Message delivery result and server response
        """
        try:
            # Ensure we have a server ID
            if not self.server_id:
                return {
                    "status": "error", 
                    "message": "No server binding. Run bind_to_server first."
                }
            
            # Add metadata to payload
            message_payload = {
                **payload,
                "agreement_hash": self.agreement_hash,
                "timestamp": int(time.time()),
                "app_name": self.app_name
            }
            
            # Send the message
            response = requests.post(
                f"{self.api_url}/message",
                headers={"Content-Type": "application/json"},
                json={
                    "server_id": self.server_id,
                    "payload": message_payload
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Message sent to server {self.server_id}")
                return {
                    "status": "success",
                    "message_id": data.get("message_id"),
                    "response": data
                }
            else:
                logger.error(f"Message delivery failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Message delivery error: {e}")
            return {"status": "error", "message": str(e)}
    
    def verify_client_agreement(self) -> Dict[str, Any]:
        """
        Ensure client has valid agreement.lock hash synced.
        
        Returns:
            dict: Verification result and status
        """
        try:
            # Check if we have a docker.lock file
            if not self.docker_lock_path or not os.path.exists(self.docker_lock_path):
                return {
                    "status": "error", 
                    "message": "No docker.lock file found. Run init_docker_lock first."
                }
            
            # Read the docker.lock file
            with open(self.docker_lock_path, 'r') as f:
                lock_data = json.load(f)
            
            # Check if the agreement hash is present
            agreement_hash = lock_data.get("agreement_hash")
            if not agreement_hash:
                return {
                    "status": "error", 
                    "message": "No agreement hash found in docker.lock."
                }
            
            # Verify with the API
            response = requests.post(
                f"{self.api_url}/verify_agreement",
                headers={"Content-Type": "application/json"},
                json={"agreement_hash": agreement_hash}
            )
            
            if response.status_code == 200:
                data = response.json()
                verification_status = data.get("verified", False)
                
                if verification_status:
                    logger.info(f"Agreement {agreement_hash} verified successfully")
                    return {
                        "status": "success",
                        "verified": True,
                        "agreement_hash": agreement_hash,
                        "details": data
                    }
                else:
                    logger.warning(f"Agreement {agreement_hash} verification failed")
                    return {
                        "status": "error", 
                        "verified": False,
                        "message": "Agreement verification failed",
                        "details": data
                    }
            else:
                logger.error(f"Verification request failed: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Agreement verification error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create Docker deployment manager
    docker_manager = DockerDeployment()
    
    # Initialize docker.lock for a sample application
    result = docker_manager.init_docker_lock(
        app_name="sample-app",
        image_name="python:3.9-slim"
    )
    print(f"Docker lock initialization: {json.dumps(result, indent=2)}")
    
    # Example deployment configuration
    config = {
        "image_name": "python:3.9-slim",
        "container_name": "metanode-sample-app",
        "env_vars": {
            "APP_ENV": "development",
            "DEBUG": "true"
        },
        "ports": {
            "8080": "80"
        },
        "volumes": [
            "./app:/app"
        ]
    }
    
    # Deploy the container
    deploy_result = docker_manager.deploy_client_docker(config)
    print(f"Deployment result: {json.dumps(deploy_result, indent=2)}")
    
    # Bind to a server
    bind_result = docker_manager.bind_to_server("sample-server-123")
    print(f"Server binding result: {json.dumps(bind_result, indent=2)}")
    
    # Send a message to the server
    message_result = docker_manager.send_message_to_server({
        "type": "status_update",
        "content": "Container running successfully"
    })
    print(f"Message result: {json.dumps(message_result, indent=2)}")
    
    # Verify the agreement
    verify_result = docker_manager.verify_client_agreement()
    print(f"Verification result: {json.dumps(verify_result, indent=2)}")
