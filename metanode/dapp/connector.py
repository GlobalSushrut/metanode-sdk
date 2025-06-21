"""
MetaNode DApp Connector
======================
Transform any application into a decentralized application by connecting
to MetaNode's testnet/mainnet.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("metanode.dapp")

class DAppConnector:
    """
    DAppConnector - Transform any application into a decentralized app
    with blockchain properties and automatic testnet/mainnet connection
    """
    
    def __init__(self, use_mainnet: bool = False, wallet_path: Optional[str] = None):
        """
        Initialize DApp connector
        
        Args:
            use_mainnet: Whether to use mainnet (requires tokens)
            wallet_path: Path to wallet file for mainnet token payment
        """
        # Import network config and token payment modules
        from metanode.deployment.network_config import NetworkConfig
        from metanode.deployment.token_payment import TokenPayment
        
        # Import transformers
        from metanode.dapp.docker_transformer import DockerTransformer
        from metanode.dapp.k8s_transformer import K8sTransformer
        
        # Load network configuration
        self.network_config = NetworkConfig()
        self.use_mainnet = use_mainnet
        self.wallet_path = wallet_path
        self.network_endpoints = self.network_config.get_network_endpoints(use_mainnet)
        
        # Create transformers
        self.docker_transformer = DockerTransformer(self.network_endpoints, use_mainnet)
        self.k8s_transformer = K8sTransformer(self.network_endpoints, use_mainnet)
        
        # Create token payment handler if using mainnet
        if use_mainnet and wallet_path:
            self.token_payment = TokenPayment(self.network_endpoints, wallet_path)
        else:
            self.token_payment = None
            
        self.logger = logging.getLogger("metanode.dapp.connector")
        
    def transform_docker(self, docker_dir: str) -> Dict[str, Any]:
        """
        Transform Docker app into docker.lock format with blockchain properties
        
        Args:
            docker_dir: Docker application directory
            
        Returns:
            Transformation results
        """
        return self.docker_transformer.transform(docker_dir)
        
    def transform_kubernetes(self, k8s_dir: str) -> Dict[str, Any]:
        """
        Transform Kubernetes deployment into blockchain cluster
        with automatic testnet/mainnet connection
        
        Args:
            k8s_dir: Kubernetes directory path
            
        Returns:
            Transformation results
        """
        return self.k8s_transformer.transform(k8s_dir)
        
    def process_payment(self) -> bool:
        """
        Process rental token payment for mainnet if applicable
        
        Returns:
            Whether payment was processed successfully
        """
        if self.use_mainnet and self.token_payment:
            return self.token_payment.charge_rental_tokens()
        return True  # No payment needed for testnet
        
    def transform_app(self, app_path: str) -> Dict[str, Any]:
        """
        Transform any application into a decentralized app
        
        Args:
            app_path: Path to application directory
            
        Returns:
            Transformation results
        """
        # Check if app path exists
        if not os.path.exists(app_path):
            raise ValueError(f"Application path does not exist: {app_path}")
            
        # Process mainnet payment if applicable
        if self.use_mainnet:
            payment_result = self.process_payment()
            if not payment_result:
                raise ValueError("Mainnet rental token payment failed")
                
        # Detect application structure
        docker_dir = os.path.join(app_path, "docker")
        k8s_dir = os.path.join(app_path, "k8s")
        
        results = {}
        
        # Transform Docker if it exists
        if os.path.exists(docker_dir) or os.path.exists(os.path.join(app_path, "docker-compose.yml")):
            docker_dir = docker_dir if os.path.exists(docker_dir) else app_path
            results["docker"] = self.transform_docker(docker_dir)
        
        # Transform Kubernetes if it exists
        if os.path.exists(k8s_dir):
            results["kubernetes"] = self.transform_kubernetes(k8s_dir)
        elif not results:  # No Docker or K8s found, assume single service app
            # Create minimal K8s structure
            os.makedirs(k8s_dir, exist_ok=True)
            self.create_minimal_k8s(app_path, k8s_dir)
            results["kubernetes"] = self.transform_kubernetes(k8s_dir)
            
        # Create environment file with connection info
        env_file = os.path.join(app_path, ".env.metanode")
        self.create_env_file(env_file)
        results["env_file"] = env_file
        
        self.logger.info(f"Transformed application {app_path} into dApp")
        return results
        
    def create_minimal_k8s(self, app_path: str, k8s_dir: str):
        """
        Create minimal Kubernetes structure for app
        
        Args:
            app_path: Application path
            k8s_dir: Kubernetes directory path
        """
        # Create base deployment
        deployment_file = os.path.join(k8s_dir, "deployment.yaml")
        
        # Basic deployment
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "app"
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "app": "app"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "app"
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": "app",
                            "image": "app:latest",
                            "ports": [
                                {"containerPort": 8000}
                            ]
                        }]
                    }
                }
            }
        }
        
        with open(deployment_file, "w") as f:
            yaml.dump(deployment, f)
            
        self.logger.info(f"Created minimal Kubernetes deployment at {deployment_file}")
        
    def create_env_file(self, env_file: str):
        """
        Create environment file with blockchain connection info
        
        Args:
            env_file: Path to output environment file
        """
        with open(env_file, "w") as f:
            f.write(f"# MetaNode Blockchain Connection\n")
            f.write(f"METANODE_NETWORK={'mainnet' if self.use_mainnet else 'testnet'}\n")
            
            # Write network endpoints
            for key, value in self.network_endpoints.items():
                env_key = f"METANODE_{key.upper()}"
                f.write(f"{env_key}={value}\n")
                
            # Add auto connection flag
            f.write("METANODE_AUTO_CONNECT=true\n")
            
        self.logger.info(f"Created blockchain environment file at {env_file}")
        
    def deploy(self, app_path: str, target_server: Optional[str] = None) -> Dict[str, Any]:
        """
        Deploy application to target server with blockchain integration
        
        Args:
            app_path: Path to application directory
            target_server: Target server address (user@host)
            
        Returns:
            Deployment results
        """
        # Transform the app first
        transform_results = self.transform_app(app_path)
        
        # If no target server, just return the transformation results
        if not target_server:
            return transform_results
            
        # Deploy to remote server
        from metanode.deployment.auto_deploy_agent import AutoDeployAgent
        
        deploy_agent = AutoDeployAgent(
            use_mainnet=self.use_mainnet,
            wallet_path=self.wallet_path
        )
        
        # Deploy transformed app
        results = deploy_agent.deploy_to_server(app_path, target_server)
        results["transform_results"] = transform_results
        
        return results
    """
    Core connector to transform any application into a decentralized app
    by connecting to MetaNode blockchain infrastructure.
    """
    
    def __init__(self, app_path: str, use_mainnet: bool = False):
        """
        Initialize DApp connector
        
        Args:
            app_path: Path to the application directory
            use_mainnet: Whether to connect to mainnet (requires tokens)
        """
        self.app_path = os.path.abspath(app_path)
        self.use_mainnet = use_mainnet
        self.endpoints = self._get_network_endpoints()
        
    def _get_network_endpoints(self) -> Dict[str, str]:
        """
        Get network endpoints based on selected network
        
        Returns:
            Dictionary of endpoint URLs
        """
        if self.use_mainnet:
            return {
                "rpc_url": "https://mainnet.metanode.network:8545",
                "ws_url": "wss://mainnet.metanode.network:8546",
                "wallet_url": "https://wallet.metanode.network",
                "ipfs_gateway": "https://ipfs.metanode.network",
                "token_contract": "0x7a58c0Be72BE218B41C608b7Fe7C5bB630736C71"
            }
        else:
            return {
                "rpc_url": "http://159.203.17.36:8545",
                "ws_url": "ws://159.203.17.36:8546",
                "wallet_url": "http://159.203.17.36:8080",
                "ipfs_gateway": "http://159.203.17.36:8080/ipfs",
                "token_contract": "0xD8f24D419153E5D03d614C5155f900f4B5C8A65C"
            }
            
    def create_env_file(self) -> str:
        """
        Create .env file with blockchain connection settings
        
        Returns:
            Path to created .env file
        """
        env_path = os.path.join(self.app_path, ".env")
        with open(env_path, "w") as f:
            f.write(f"# MetaNode Blockchain Connection Settings\n")
            f.write(f"METANODE_NETWORK={'mainnet' if self.use_mainnet else 'testnet'}\n")
            f.write(f"METANODE_RPC_URL={self.endpoints['rpc_url']}\n")
            f.write(f"METANODE_WS_URL={self.endpoints['ws_url']}\n")
            f.write(f"METANODE_WALLET_URL={self.endpoints['wallet_url']}\n")
            f.write(f"METANODE_IPFS_GATEWAY={self.endpoints['ipfs_gateway']}\n")
            f.write(f"METANODE_TOKEN_CONTRACT={self.endpoints['token_contract']}\n")
            
        logger.info(f"Created .env file at {env_path}")
        return env_path
