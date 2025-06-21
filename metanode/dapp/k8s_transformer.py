"""
MetaNode Kubernetes Transformer
=============================
Transform K8s deployments to blockchain clusters with testnet/mainnet connectivity
"""

import os
import yaml
import logging
from typing import Dict, Any, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("metanode.dapp.k8s")

class K8sTransformer:
    """Transform Kubernetes deployments to blockchain clusters"""
    
    def __init__(self, network_endpoints: Dict[str, str], use_mainnet: bool = False):
        """
        Initialize Kubernetes transformer
        
        Args:
            network_endpoints: Dictionary of network endpoint URLs
            use_mainnet: Whether to use mainnet
        """
        self.network_endpoints = network_endpoints
        self.use_mainnet = use_mainnet
        
    def add_blockchain_annotations(self, deployment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add blockchain annotations to a deployment
        
        Args:
            deployment: Kubernetes deployment object
            
        Returns:
            Updated deployment
        """
        # Add blockchain annotations
        deployment.setdefault("metadata", {}).setdefault("annotations", {}).update({
            "metanode.blockchain/verification": "required",
            "metanode.blockchain/immutable": "true",
            "metanode.blockchain/consensus": "true",
            "metanode.blockchain/network": "mainnet" if self.use_mainnet else "testnet"
        })
        
        # Add blockchain annotations to pod template
        if "spec" in deployment and "template" in deployment["spec"]:
            deployment["spec"]["template"].setdefault("metadata", {}).setdefault("annotations", {}).update({
                "metanode.blockchain/verification": "required",
                "metanode.blockchain/immutable": "true"
            })
            
        return deployment
        
    def add_vpod_container(self, deployment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add vPod sidecar container using the approach that fixed MetaNode demo CLI
        
        Args:
            deployment: Kubernetes deployment object
            
        Returns:
            Updated deployment
        """
        # Get containers list
        containers = deployment.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
        
        # Check if vPod container already exists
        vpod_exists = any(c.get("name") == "vpod-sidecar" for c in containers)
        
        if not vpod_exists:
            # Add vPod sidecar container
            vpod_container = {
                "name": "vpod-sidecar",
                "image": "python:3.9-slim",
                "command": [
                    "sh",
                    "-c",
                    "mkdir -p /data && echo '{\"status\":\"active\",\"service\":\"vpod\",\"vpod_id\":\"$(POD_NAME)\",\"algorithms\":[\"federated-average\",\"secure-aggregation\"]}' > /data/status.json && python3 -m http.server 8070 -d /data"
                ],
                "env": [
                    {
                        "name": "POD_NAME",
                        "valueFrom": {
                            "fieldRef": {
                                "fieldPath": "metadata.name"
                            }
                        }
                    }
                ],
                "ports": [
                    {
                        "containerPort": 8070
                    }
                ]
            }
            
            # Add container to deployment
            deployment.get("spec", {}).get("template", {}).get("spec", {}).setdefault("containers", []).append(vpod_container)
            
        return deployment
        
    def add_network_config(self, deployment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add network connection environment variables
        
        Args:
            deployment: Kubernetes deployment object
            
        Returns:
            Updated deployment
        """
        # Network environment variables
        network_env = [
            {
                "name": "METANODE_NETWORK",
                "value": "mainnet" if self.use_mainnet else "testnet"
            },
            {
                "name": "METANODE_RPC_URL",
                "value": self.network_endpoints["rpc_url"]
            },
            {
                "name": "METANODE_WS_URL",
                "value": self.network_endpoints["ws_url"]
            },
            {
                "name": "METANODE_WALLET_URL",
                "value": self.network_endpoints["wallet_url"]
            },
            {
                "name": "METANODE_IPFS_GATEWAY",
                "value": self.network_endpoints["ipfs_gateway"]
            },
            {
                "name": "METANODE_TOKEN_CONTRACT",
                "value": self.network_endpoints["token_contract"]
            },
            {
                "name": "METANODE_AUTO_CONNECT",
                "value": "true"
            }
        ]
        
        # Add env vars to each app container (skip vPod)
        containers = deployment.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
        for container in containers:
            if container.get("name") != "vpod-sidecar":
                container.setdefault("env", [])
                
                # Add env vars that don't already exist
                existing_env_names = {e.get("name") for e in container["env"]}
                for env_var in network_env:
                    if env_var["name"] not in existing_env_names:
                        container["env"].append(env_var)
                        
        return deployment
        
    def transform_yaml(self, yaml_path: str) -> Dict[str, Any]:
        """
        Transform Kubernetes YAML file with blockchain properties
        
        Args:
            yaml_path: Path to Kubernetes YAML file
            
        Returns:
            Transformation results
        """
        try:
            # Read YAML file
            with open(yaml_path, "r") as f:
                content = yaml.safe_load_all(f)
                documents = list(content)
                
            # Process each document
            updated_documents = []
            for doc in documents:
                # Skip empty documents
                if not doc:
                    continue
                    
                # Only process deployments and statefulsets
                if doc.get("kind") in ["Deployment", "StatefulSet"]:
                    # Add blockchain annotations
                    doc = self.add_blockchain_annotations(doc)
                    
                    # Add vPod container
                    doc = self.add_vpod_container(doc)
                    
                    # Add network config
                    doc = self.add_network_config(doc)
                    
                updated_documents.append(doc)
                
            # Write updated YAML back to file
            with open(yaml_path, "w") as f:
                yaml.dump_all(updated_documents, f)
                
            logger.info(f"Transformed Kubernetes file {yaml_path} with blockchain properties")
            return {"status": "transformed", "file": yaml_path}
        except Exception as e:
            logger.error(f"Error transforming {yaml_path}: {str(e)}")
            return {"status": "error", "file": yaml_path, "error": str(e)}
            
    def create_network_configmap(self, k8s_dir: str) -> str:
        """
        Create network connection ConfigMap
        
        Args:
            k8s_dir: Kubernetes directory path
            
        Returns:
            Path to created ConfigMap file
        """
        # Create network connection ConfigMap
        configmap_path = os.path.join(k8s_dir, "network-connection.yaml")
        
        configmap = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": "metanode-network-config"
            },
            "data": {
                "network": "mainnet" if self.use_mainnet else "testnet",
                "rpc_url": self.network_endpoints["rpc_url"],
                "ws_url": self.network_endpoints["ws_url"],
                "wallet_url": self.network_endpoints["wallet_url"],
                "ipfs_gateway": self.network_endpoints["ipfs_gateway"],
                "token_contract": self.network_endpoints["token_contract"],
                "auto_connect": "true",
                "auto_validation": "true"
            }
        }
        
        # Write ConfigMap to file
        with open(configmap_path, "w") as f:
            yaml.dump(configmap, f)
            
        logger.info(f"Created network connection ConfigMap at {configmap_path}")
        return configmap_path
        
    def transform(self, k8s_dir: str) -> Dict[str, Any]:
        """
        Transform all Kubernetes files in directory with blockchain properties
        
        Args:
            k8s_dir: Kubernetes directory path
            
        Returns:
            Transformation results
        """
        # Check if K8s directory exists
        if not os.path.exists(k8s_dir):
            os.makedirs(k8s_dir, exist_ok=True)
            logger.info(f"Created Kubernetes directory at {k8s_dir}")
            
        # Create network connection ConfigMap
        self.create_network_configmap(k8s_dir)
        
        # Transform all YAML files
        results = []
        for filename in os.listdir(k8s_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                yaml_path = os.path.join(k8s_dir, filename)
                result = self.transform_yaml(yaml_path)
                results.append(result)
                
        return {
            "status": "transformed",
            "file_count": len(results),
            "results": results,
            "network": "mainnet" if self.use_mainnet else "testnet"
        }
