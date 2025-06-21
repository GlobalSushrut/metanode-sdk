#!/usr/bin/env python3
"""
MetaNode SDK - Kubernetes Manager Module
======================================

Manages Kubernetes deployments with cryptographic security for MetaNode testnet.
"""

import os
import json
import time
import base64
import logging
import hashlib
import requests
import subprocess
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL

# Configure logging
logger = logging.getLogger(__name__)

class K8sManager:
    """Manages Kubernetes deployments for MetaNode testnet."""
    
    def __init__(self, 
                api_url: Optional[str] = None,
                admin_key: Optional[str] = None,
                kubeconfig: Optional[str] = None):
        """
        Initialize K8s manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            admin_key (str, optional): Admin API key for authentication
            kubeconfig (str, optional): Path to kubeconfig file
        """
        self.api_url = api_url or API_URL
        self.admin_key = admin_key
        self.kubeconfig = kubeconfig or os.environ.get("KUBECONFIG", "~/.kube/config")
        self.admin_dir = os.path.join(os.getcwd(), ".metanode", "admin")
        self.k8s_dir = os.path.join(self.admin_dir, "k8s")
        
        # Ensure directories exist
        os.makedirs(self.k8s_dir, exist_ok=True)
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for admin API calls."""
        headers = {"Content-Type": "application/json"}
        if self.admin_key:
            headers["X-Admin-Key"] = self.admin_key
        return headers
    
    def _run_kubectl(self, command: List[str], check_output: bool = True) -> Dict[str, Any]:
        """
        Run kubectl command.
        
        Args:
            command (list): kubectl command as list of arguments
            check_output (bool): Whether to capture output
            
        Returns:
            dict: Command result
        """
        try:
            full_command = ["kubectl", "--kubeconfig", self.kubeconfig] + command
            
            if check_output:
                output = subprocess.check_output(full_command, stderr=subprocess.STDOUT)
                return {
                    "status": "success",
                    "output": output.decode("utf-8").strip(),
                    "command": " ".join(full_command)
                }
            else:
                subprocess.run(full_command, check=True)
                return {
                    "status": "success",
                    "command": " ".join(full_command)
                }
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Kubectl command failed: {e}")
            return {
                "status": "error", 
                "message": e.output.decode("utf-8").strip() if e.output else str(e),
                "command": " ".join(full_command),
                "exit_code": e.returncode
            }
        except Exception as e:
            logger.error(f"Kubectl execution error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_cluster_info(self) -> Dict[str, Any]:
        """
        Get information about the Kubernetes cluster.
        
        Returns:
            dict: Cluster information
        """
        try:
            # Get cluster info
            cluster_info = self._run_kubectl(["cluster-info"])
            if cluster_info["status"] == "error":
                return cluster_info
            
            # Get nodes
            nodes = self._run_kubectl(["get", "nodes", "-o", "json"])
            if nodes["status"] == "error":
                return nodes
            
            # Parse JSON output
            nodes_data = json.loads(nodes["output"])
            
            # Save cluster info
            info_data = {
                "cluster_info": cluster_info["output"],
                "nodes": nodes_data,
                "timestamp": int(time.time())
            }
            
            info_file = os.path.join(self.k8s_dir, f"cluster-info-{int(time.time())}.json")
            with open(info_file, 'w') as f:
                json.dump(info_data, f, indent=2)
            
            logger.info("Retrieved cluster information")
            return {
                "status": "success",
                "cluster_info": cluster_info["output"],
                "nodes": nodes_data,
                "nodes_count": len(nodes_data.get("items", [])),
                "info_file": info_file
            }
                
        except Exception as e:
            logger.error(f"Cluster info error: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_node_crypt_key(self) -> Dict[str, Any]:
        """
        Generate cryptographic key pair for testnet node authentication.
        
        Returns:
            dict: Generated key information
        """
        try:
            # Generate secure random key
            key_bytes = os.urandom(32)  # 256-bit key
            key_id = hashlib.sha256(key_bytes).hexdigest()[:16]
            
            # For demo/test purposes, using simple base64 encoding
            # In production, would use proper asymmetric cryptography
            encoded_key = base64.b64encode(key_bytes).decode('utf-8')
            
            # Hash for verification
            key_hash = hashlib.sha256(key_bytes).hexdigest()
            
            # Create key information
            key_info = {
                "key_id": key_id,
                "key_hash": key_hash,
                "created_at": int(time.time()),
                "encoded_key": encoded_key,
            }
            
            # Save key information securely
            key_file = os.path.join(self.k8s_dir, f"node-key-{key_id}.json")
            with open(key_file, 'w') as f:
                json.dump(key_info, f, indent=2)
            
            logger.info(f"Generated cryptographic key for node with ID {key_id}")
            return {
                "status": "success",
                "key_id": key_id,
                "key_hash": key_hash,
                "encoded_key": encoded_key,
                "key_file": key_file
            }
                
        except Exception as e:
            logger.error(f"Key generation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def register_node_with_testnet(self, 
                                  node_name: str, 
                                  key_id: str,
                                  is_testnet_node: bool = True) -> Dict[str, Any]:
        """
        Register a Kubernetes node with the MetaNode testnet.
        
        Args:
            node_name (str): Name of the Kubernetes node
            key_id (str): ID of the cryptographic key to use
            is_testnet_node (bool): Whether this node will serve as a testnet node
            
        Returns:
            dict: Registration result
        """
        try:
            # Check if node exists
            node_check = self._run_kubectl(["get", "node", node_name])
            if node_check["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Node {node_name} not found: {node_check['message']}"
                }
            
            # Load key information
            key_file = os.path.join(self.k8s_dir, f"node-key-{key_id}.json")
            if not os.path.exists(key_file):
                return {
                    "status": "error",
                    "message": f"Key with ID {key_id} not found"
                }
            
            with open(key_file, 'r') as f:
                key_info = json.load(f)
            
            encoded_key = key_info.get("encoded_key")
            key_hash = key_info.get("key_hash")
            
            # Prepare registration data
            registration_data = {
                "node_name": node_name,
                "key_id": key_id,
                "key_hash": key_hash,
                "is_testnet_node": is_testnet_node,
                "kubernetes_info": {
                    "node_name": node_name,
                    "register_time": int(time.time())
                }
            }
            
            # Send registration to API
            response = requests.post(
                f"{self.api_url}/admin/nodes/register",
                headers=self._get_auth_headers(),
                json=registration_data
            )
            
            if response.status_code == 200:
                result = response.json()
                node_id = result.get("node_id")
                
                # Label the node in Kubernetes
                role_label = "testnet-node=true" if is_testnet_node else "app-node=true"
                label_result = self._run_kubectl([
                    "label", "node", node_name,
                    role_label,
                    "metanode-id=" + node_id,
                    "--overwrite=true"
                ])
                
                # Save registration information
                reg_info = {
                    "node_id": node_id,
                    "node_name": node_name,
                    "key_id": key_id,
                    "is_testnet_node": is_testnet_node,
                    "registered_at": int(time.time()),
                    "registration_result": result,
                    "kubernetes_label_result": label_result
                }
                
                reg_file = os.path.join(self.k8s_dir, f"node-registration-{node_id}.json")
                with open(reg_file, 'w') as f:
                    json.dump(reg_info, f, indent=2)
                
                logger.info(f"Registered node {node_name} with testnet, node ID: {node_id}")
                return {
                    "status": "success",
                    "node_id": node_id,
                    "node_name": node_name,
                    "is_testnet_node": is_testnet_node,
                    "registration_file": reg_file
                }
            else:
                logger.error(f"Failed to register node: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Node registration error: {e}")
            return {"status": "error", "message": str(e)}
    
    def deploy_testnet_node(self, 
                           node_id: str, 
                           node_name: str,
                           config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Deploy testnet node components to a registered Kubernetes node.
        
        Args:
            node_id (str): ID of the registered node
            node_name (str): Name of the Kubernetes node
            config (dict, optional): Additional configuration parameters
            
        Returns:
            dict: Deployment result
        """
        try:
            # Check if node is registered
            reg_file = os.path.join(self.k8s_dir, f"node-registration-{node_id}.json")
            if not os.path.exists(reg_file):
                return {
                    "status": "error",
                    "message": f"Node with ID {node_id} not registered"
                }
            
            with open(reg_file, 'r') as f:
                reg_info = json.load(f)
            
            if not reg_info.get("is_testnet_node", False):
                return {
                    "status": "error",
                    "message": f"Node {node_name} is not registered as a testnet node"
                }
            
            # Verify node exists in cluster
            node_check = self._run_kubectl(["get", "node", node_name])
            if node_check["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Node {node_name} not found in cluster"
                }
            
            # Load key information
            key_id = reg_info.get("key_id")
            key_file = os.path.join(self.k8s_dir, f"node-key-{key_id}.json")
            
            with open(key_file, 'r') as f:
                key_info = json.load(f)
            
            encoded_key = key_info.get("encoded_key")
            
            # Create namespace if it doesn't exist
            self._run_kubectl(["create", "namespace", "metanode-testnet", "--dry-run=client", "-o=yaml", "|", "kubectl", "apply", "-f", "-"])
            
            # Create secret for node authentication
            secret_name = f"node-key-{node_id}"
            secret_yaml = f"""
            apiVersion: v1
            kind: Secret
            metadata:
              name: {secret_name}
              namespace: metanode-testnet
            type: Opaque
            data:
              node_key: {base64.b64encode(encoded_key.encode()).decode()}
              node_id: {base64.b64encode(node_id.encode()).decode()}
            """
            
            secret_file = os.path.join(self.k8s_dir, f"secret-{node_id}.yaml")
            with open(secret_file, 'w') as f:
                f.write(secret_yaml)
            
            # Apply secret
            secret_result = self._run_kubectl(["apply", "-f", secret_file])
            if secret_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create secret: {secret_result['message']}"
                }
            
            # Create testnet node deployment
            deployment_config = config or {}
            deployment_name = deployment_config.get("name", f"testnet-node-{node_id[:8]}")
            
            # Create deployment YAML
            deployment_yaml = f"""
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: {deployment_name}
              namespace: metanode-testnet
              labels:
                app: metanode-testnet
                node-id: {node_id}
            spec:
              replicas: 1
              selector:
                matchLabels:
                  app: metanode-testnet
                  node-id: {node_id}
              template:
                metadata:
                  labels:
                    app: metanode-testnet
                    node-id: {node_id}
                spec:
                  nodeSelector:
                    kubernetes.io/hostname: {node_name}
                    testnet-node: "true"
                  containers:
                  - name: metanode-testnet
                    image: {deployment_config.get('image', 'metanode/testnet:latest')}
                    env:
                    - name: NODE_ID
                      valueFrom:
                        secretKeyRef:
                          name: {secret_name}
                          key: node_id
                    - name: NODE_KEY
                      valueFrom:
                        secretKeyRef:
                          name: {secret_name}
                          key: node_key
                    - name: API_URL
                      value: {self.api_url}
                    ports:
                    - containerPort: 8545
                      name: rpc
                    - containerPort: 8546
                      name: ws
                    volumeMounts:
                    - name: testnet-data
                      mountPath: /data
                  volumes:
                  - name: testnet-data
                    persistentVolumeClaim:
                      claimName: testnet-data-{node_id[:8]}
            """
            
            # Create PVC for testnet data
            pvc_yaml = f"""
            apiVersion: v1
            kind: PersistentVolumeClaim
            metadata:
              name: testnet-data-{node_id[:8]}
              namespace: metanode-testnet
            spec:
              accessModes:
                - ReadWriteOnce
              resources:
                requests:
                  storage: {deployment_config.get('storage', '10Gi')}
            """
            
            # Save deployment files
            deployment_file = os.path.join(self.k8s_dir, f"deployment-{node_id}.yaml")
            with open(deployment_file, 'w') as f:
                f.write(deployment_yaml)
            
            pvc_file = os.path.join(self.k8s_dir, f"pvc-{node_id}.yaml")
            with open(pvc_file, 'w') as f:
                f.write(pvc_yaml)
            
            # Apply PVC
            pvc_result = self._run_kubectl(["apply", "-f", pvc_file])
            if pvc_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create PVC: {pvc_result['message']}"
                }
            
            # Apply deployment
            deploy_result = self._run_kubectl(["apply", "-f", deployment_file])
            if deploy_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create deployment: {deploy_result['message']}"
                }
            
            # Save deployment information
            deployment_info = {
                "node_id": node_id,
                "node_name": node_name,
                "deployment_name": deployment_name,
                "namespace": "metanode-testnet",
                "secret_name": secret_name,
                "deployed_at": int(time.time()),
                "config": deployment_config,
                "deployment_file": deployment_file,
                "pvc_file": pvc_file,
                "secret_file": secret_file
            }
            
            info_file = os.path.join(self.k8s_dir, f"testnet-deployment-{node_id}.json")
            with open(info_file, 'w') as f:
                json.dump(deployment_info, f, indent=2)
            
            logger.info(f"Deployed testnet node on {node_name} with ID {node_id}")
            return {
                "status": "success",
                "node_id": node_id,
                "node_name": node_name,
                "deployment_name": deployment_name,
                "info_file": info_file
            }
                
        except Exception as e:
            logger.error(f"Testnet node deployment error: {e}")
            return {"status": "error", "message": str(e)}
    
    def deploy_application_node(self, 
                               node_id: str, 
                               node_name: str,
                               app_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy application components to a Kubernetes node.
        
        Args:
            node_id (str): ID of the registered node
            node_name (str): Name of the Kubernetes node
            app_config (dict): Application configuration
            
        Returns:
            dict: Deployment result
        """
        try:
            # Check if node is registered
            reg_file = os.path.join(self.k8s_dir, f"node-registration-{node_id}.json")
            if not os.path.exists(reg_file):
                return {
                    "status": "error",
                    "message": f"Node with ID {node_id} not registered"
                }
            
            with open(reg_file, 'r') as f:
                reg_info = json.load(f)
            
            # Verify node exists in cluster
            node_check = self._run_kubectl(["get", "node", node_name])
            if node_check["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Node {node_name} not found in cluster"
                }
            
            # Get application details
            app_name = app_config.get("name", f"app-{int(time.time())}")
            app_image = app_config.get("image", "metanode/app:latest")
            app_replicas = app_config.get("replicas", 1)
            app_port = app_config.get("port", 8080)
            app_storage = app_config.get("storage", "1Gi")
            app_env = app_config.get("env", {})
            
            # Create namespace if it doesn't exist
            self._run_kubectl(["create", "namespace", "metanode-apps", "--dry-run=client", "-o=yaml", "|", "kubectl", "apply", "-f", "-"])
            
            # Generate environment variables for YAML
            env_yaml = ""
            for key, value in app_env.items():
                env_yaml += f"                    - name: {key}\n                      value: {value}\n"
            
            # Add testnet connection environment variable
            env_yaml += f"                    - name: METANODE_TESTNET_URL\n                      value: http://testnet-service.metanode-testnet:8545\n"
            
            # Create deployment YAML
            deployment_yaml = f"""
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: {app_name}
              namespace: metanode-apps
              labels:
                app: metanode-app
                app-name: {app_name}
            spec:
              replicas: {app_replicas}
              selector:
                matchLabels:
                  app: metanode-app
                  app-name: {app_name}
              template:
                metadata:
                  labels:
                    app: metanode-app
                    app-name: {app_name}
                spec:
                  nodeSelector:
                    app-node: "true"
                  containers:
                  - name: {app_name}
                    image: {app_image}
                    env:
{env_yaml}
                    ports:
                    - containerPort: {app_port}
                      name: http
                    volumeMounts:
                    - name: app-data
                      mountPath: /app/data
                  volumes:
                  - name: app-data
                    persistentVolumeClaim:
                      claimName: app-data-{app_name}
            """
            
            # Create service YAML
            service_yaml = f"""
            apiVersion: v1
            kind: Service
            metadata:
              name: {app_name}-service
              namespace: metanode-apps
            spec:
              selector:
                app: metanode-app
                app-name: {app_name}
              ports:
              - port: {app_port}
                targetPort: {app_port}
                protocol: TCP
                name: http
              type: ClusterIP
            """
            
            # Create PVC for app data
            pvc_yaml = f"""
            apiVersion: v1
            kind: PersistentVolumeClaim
            metadata:
              name: app-data-{app_name}
              namespace: metanode-apps
            spec:
              accessModes:
                - ReadWriteOnce
              resources:
                requests:
                  storage: {app_storage}
            """
            
            # Save deployment files
            deployment_file = os.path.join(self.k8s_dir, f"app-deployment-{app_name}.yaml")
            with open(deployment_file, 'w') as f:
                f.write(deployment_yaml)
            
            service_file = os.path.join(self.k8s_dir, f"app-service-{app_name}.yaml")
            with open(service_file, 'w') as f:
                f.write(service_yaml)
            
            pvc_file = os.path.join(self.k8s_dir, f"app-pvc-{app_name}.yaml")
            with open(pvc_file, 'w') as f:
                f.write(pvc_yaml)
            
            # Apply PVC
            pvc_result = self._run_kubectl(["apply", "-f", pvc_file])
            if pvc_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create PVC: {pvc_result['message']}"
                }
            
            # Apply deployment
            deploy_result = self._run_kubectl(["apply", "-f", deployment_file])
            if deploy_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create deployment: {deploy_result['message']}"
                }
            
            # Apply service
            service_result = self._run_kubectl(["apply", "-f", service_file])
            if service_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create service: {service_result['message']}"
                }
            
            # Save deployment information
            deployment_info = {
                "app_name": app_name,
                "node_id": node_id,
                "node_name": node_name,
                "namespace": "metanode-apps",
                "deployed_at": int(time.time()),
                "config": app_config,
                "deployment_file": deployment_file,
                "service_file": service_file,
                "pvc_file": pvc_file
            }
            
            info_file = os.path.join(self.k8s_dir, f"app-deployment-{app_name}.json")
            with open(info_file, 'w') as f:
                json.dump(deployment_info, f, indent=2)
            
            logger.info(f"Deployed application {app_name} on {node_name} with ID {node_id}")
            return {
                "status": "success",
                "app_name": app_name,
                "node_id": node_id,
                "node_name": node_name,
                "service_name": f"{app_name}-service",
                "info_file": info_file
            }
                
        except Exception as e:
            logger.error(f"Application deployment error: {e}")
            return {"status": "error", "message": str(e)}
    
    def setup_testnet_sync(self) -> Dict[str, Any]:
        """
        Set up synchronization between testnet nodes.
        
        Returns:
            dict: Sync setup result
        """
        try:
            # Create service for testnet nodes
            testnet_service_yaml = f"""
            apiVersion: v1
            kind: Service
            metadata:
              name: testnet-service
              namespace: metanode-testnet
            spec:
              selector:
                app: metanode-testnet
              ports:
              - port: 8545
                targetPort: 8545
                protocol: TCP
                name: rpc
              - port: 8546
                targetPort: 8546
                protocol: TCP
                name: ws
              type: ClusterIP
            """
            
            # Create ConfigMap for synchronization
            sync_config_yaml = f"""
            apiVersion: v1
            kind: ConfigMap
            metadata:
              name: testnet-sync-config
              namespace: metanode-testnet
            data:
              sync.json: |
                {{
                  "sync_interval": 60,
                  "api_url": "{self.api_url}",
                  "testnet_service": "testnet-service.metanode-testnet:8545",
                  "min_nodes": 3,
                  "blockchain_consensus": "proof-of-authority",
                  "node_discovery": true,
                  "timestamp": {int(time.time())}
                }}
            """
            
            # Save YAML files
            service_file = os.path.join(self.k8s_dir, "testnet-service.yaml")
            with open(service_file, 'w') as f:
                f.write(testnet_service_yaml)
            
            config_file = os.path.join(self.k8s_dir, "testnet-sync-config.yaml")
            with open(config_file, 'w') as f:
                f.write(sync_config_yaml)
            
            # Apply service
            service_result = self._run_kubectl(["apply", "-f", service_file])
            if service_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create testnet service: {service_result['message']}"
                }
            
            # Apply config
            config_result = self._run_kubectl(["apply", "-f", config_file])
            if config_result["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to create sync config: {config_result['message']}"
                }
            
            # Save sync setup information
            sync_info = {
                "service_file": service_file,
                "config_file": config_file,
                "setup_at": int(time.time()),
                "service_result": service_result,
                "config_result": config_result
            }
            
            info_file = os.path.join(self.k8s_dir, f"testnet-sync-setup-{int(time.time())}.json")
            with open(info_file, 'w') as f:
                json.dump(sync_info, f, indent=2)
            
            logger.info(f"Set up testnet synchronization")
            return {
                "status": "success",
                "service_name": "testnet-service",
                "config_name": "testnet-sync-config",
                "info_file": info_file
            }
                
        except Exception as e:
            logger.error(f"Testnet sync setup error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_deployment_status(self, deployment_type: str, name: str) -> Dict[str, Any]:
        """
        Get status of a deployment.
        
        Args:
            deployment_type (str): Type of deployment ("testnet" or "app")
            name (str): Name of the deployment
            
        Returns:
            dict: Deployment status
        """
        try:
            namespace = "metanode-testnet" if deployment_type == "testnet" else "metanode-apps"
            
            # Get deployment status
            deployment_status = self._run_kubectl(
                ["get", "deployment", name, "-n", namespace, "-o", "json"]
            )
            
            if deployment_status["status"] == "error":
                return {
                    "status": "error",
                    "message": f"Failed to get deployment status: {deployment_status['message']}"
                }
            
            # Parse JSON output
            status_data = json.loads(deployment_status["output"])
            
            # Check if pods are running
            pods_status = self._run_kubectl(
                ["get", "pods", "-l", f"app={'metanode-testnet' if deployment_type == 'testnet' else 'metanode-app'}", "-n", namespace, "-o", "json"]
            )
            
            if pods_status["status"] == "success":
                pods_data = json.loads(pods_status["output"])
            else:
                pods_data = {"items": []}
            
            # Save status information
            status_info = {
                "name": name,
                "type": deployment_type,
                "namespace": namespace,
                "deployment_status": status_data,
                "pods_status": pods_data,
                "timestamp": int(time.time())
            }
            
            status_file = os.path.join(self.k8s_dir, f"{deployment_type}-status-{name}-{int(time.time())}.json")
            with open(status_file, 'w') as f:
                json.dump(status_info, f, indent=2)
            
            # Extract key status information
            available_replicas = status_data.get("status", {}).get("availableReplicas", 0)
            desired_replicas = status_data.get("spec", {}).get("replicas", 0)
            pod_statuses = []
            
            for pod in pods_data.get("items", []):
                pod_name = pod.get("metadata", {}).get("name", "unknown")
                pod_status = pod.get("status", {}).get("phase", "Unknown")
                pod_statuses.append({"name": pod_name, "status": pod_status})
            
            logger.info(f"Retrieved status for {deployment_type} deployment {name}")
            return {
                "status": "success",
                "name": name,
                "type": deployment_type,
                "namespace": namespace,
                "available_replicas": available_replicas,
                "desired_replicas": desired_replicas,
                "pods": pod_statuses,
                "is_ready": available_replicas == desired_replicas and desired_replicas > 0,
                "status_file": status_file
            }
                
        except Exception as e:
            logger.error(f"Get deployment status error: {e}")
            return {"status": "error", "message": str(e)}    

# Simple usage example
if __name__ == "__main__":
    # Create K8s manager
    k8s_manager = K8sManager(admin_key="sample-admin-key")
    
    # Get cluster information
    cluster_info = k8s_manager.get_cluster_info()
    print(f"Cluster info: {json.dumps(cluster_info, indent=2)}")
    
    # Generate a node key
    node_key = k8s_manager.generate_node_crypt_key()
    print(f"Generated node key: {json.dumps(node_key, indent=2)}")
    
    # Set up testnet sync
    sync_result = k8s_manager.setup_testnet_sync()
    print(f"Sync setup: {json.dumps(sync_result, indent=2)}")

