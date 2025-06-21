"""
MetaNode SDK - Kubernetes Deployment Module
=======================================

Kubernetes deployment utilities for MetaNode blockchain infrastructure.
Provides deployment functions for blockchain nodes, validators, and storage nodes.
"""

import os
import time
import logging
import subprocess
from typing import Dict, List, Any, Optional, Union

import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException

from metanode.config.settings import K8S_SETTINGS, get_user_configuration

# Configure logging
logger = logging.getLogger("metanode-k8s-deployment")

class K8sDeployment:
    """Kubernetes deployment manager for MetaNode blockchain components"""
    
    def __init__(self, namespace: str = None, context: str = None):
        """Initialize the Kubernetes deployment manager
        
        Args:
            namespace (str, optional): Kubernetes namespace to use
            context (str, optional): Kubernetes context name to use
        """
        self.namespace = namespace or K8S_SETTINGS.get("namespace", "metanode")
        self.context = context
        self._load_config()
        self._ensure_namespace()
        
        # API clients
        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
        self.networking_api = client.NetworkingV1Api()
        
    def _load_config(self) -> None:
        """Load Kubernetes configuration"""
        try:
            if self.context:
                config.load_kube_config(context=self.context)
            else:
                config.load_kube_config()
            logger.info(f"Loaded Kubernetes config with context: {self.context or 'default'}")
        except Exception as e:
            logger.warning(f"Failed to load Kubernetes config: {e}")
            logger.info("Trying to load incluster config...")
            try:
                config.load_incluster_config()
                logger.info("Loaded incluster config")
            except Exception as e:
                logger.error(f"Failed to load incluster config: {e}")
                raise Exception("Could not load Kubernetes configuration")
    
    def _ensure_namespace(self) -> None:
        """Create namespace if it doesn't exist"""
        try:
            self.core_api.read_namespace(self.namespace)
            logger.info(f"Namespace {self.namespace} exists")
        except ApiException as e:
            if e.status == 404:
                namespace = client.V1Namespace(
                    metadata=client.V1ObjectMeta(name=self.namespace)
                )
                self.core_api.create_namespace(namespace)
                logger.info(f"Created namespace {self.namespace}")
            else:
                logger.error(f"Error checking namespace: {e}")
                
    def deploy_blockchain_node(self, 
                              name: str, 
                              image: str = None, 
                              replicas: int = 1) -> Dict[str, Any]:
        """Deploy a blockchain node to Kubernetes
        
        Args:
            name (str): Node name
            image (str, optional): Container image to use
            replicas (int, optional): Number of replicas
            
        Returns:
            Dict with deployment results
        """
        image = image or K8S_SETTINGS.get("blockchain_image", "metanode/blockchain-node:latest")
        
        try:
            # Create deployment
            deployment = self._create_deployment_object(
                name=name,
                image=image,
                replicas=replicas,
                port=8545,
                env_vars={
                    "NODE_TYPE": "blockchain",
                    "NODE_NAME": name
                }
            )
            
            # Create the deployment
            self.apps_api.create_namespaced_deployment(
                namespace=self.namespace,
                body=deployment
            )
            
            # Create service
            service = self._create_service_object(
                name=name,
                selector={"app": name},
                port=8545,
                target_port=8545
            )
            
            self.core_api.create_namespaced_service(
                namespace=self.namespace,
                body=service
            )
            
            logger.info(f"Deployed blockchain node {name}")
            return {
                "status": "success",
                "name": name,
                "image": image,
                "replicas": replicas
            }
        except ApiException as e:
            logger.error(f"Failed to deploy blockchain node {name}: {e}")
            return {
                "status": "error",
                "name": name,
                "error": str(e)
            }
            
    def deploy_validator_node(self, 
                             name: str, 
                             image: str = None, 
                             replicas: int = 1) -> Dict[str, Any]:
        """Deploy a validator node to Kubernetes
        
        Args:
            name (str): Node name
            image (str, optional): Container image to use
            replicas (int, optional): Number of replicas
            
        Returns:
            Dict with deployment results
        """
        image = image or K8S_SETTINGS.get("validator_image", "metanode/validator-node:latest")
        
        try:
            # Create deployment
            deployment = self._create_deployment_object(
                name=name,
                image=image,
                replicas=replicas,
                port=8050,
                env_vars={
                    "NODE_TYPE": "validator",
                    "NODE_NAME": name
                }
            )
            
            # Create the deployment
            self.apps_api.create_namespaced_deployment(
                namespace=self.namespace,
                body=deployment
            )
            
            # Create service
            service = self._create_service_object(
                name=name,
                selector={"app": name},
                port=8050,
                target_port=8050
            )
            
            self.core_api.create_namespaced_service(
                namespace=self.namespace,
                body=service
            )
            
            logger.info(f"Deployed validator node {name}")
            return {
                "status": "success",
                "name": name,
                "image": image,
                "replicas": replicas
            }
        except ApiException as e:
            logger.error(f"Failed to deploy validator node {name}: {e}")
            return {
                "status": "error",
                "name": name,
                "error": str(e)
            }
    
    def deploy_storage_node(self, 
                           name: str, 
                           image: str = None, 
                           replicas: int = 1,
                           storage_size: str = None) -> Dict[str, Any]:
        """Deploy a storage node to Kubernetes
        
        Args:
            name (str): Node name
            image (str, optional): Container image to use
            replicas (int, optional): Number of replicas
            storage_size (str, optional): Size of persistent storage
            
        Returns:
            Dict with deployment results
        """
        image = image or K8S_SETTINGS.get("storage_image", "metanode/storage-node:latest")
        storage_size = storage_size or K8S_SETTINGS.get("persistent_volume_size", "10Gi")
        
        try:
            # Create PVC
            pvc = self._create_pvc_object(
                name=f"{name}-data",
                storage_size=storage_size
            )
            
            self.core_api.create_namespaced_persistent_volume_claim(
                namespace=self.namespace,
                body=pvc
            )
            
            # Create deployment
            deployment = self._create_deployment_object(
                name=name,
                image=image,
                replicas=replicas,
                port=8060,
                env_vars={
                    "NODE_TYPE": "storage",
                    "NODE_NAME": name
                },
                volume_mounts=[
                    {
                        "name": "data",
                        "mountPath": "/data"
                    }
                ],
                volumes=[
                    {
                        "name": "data",
                        "persistentVolumeClaim": {
                            "claimName": f"{name}-data"
                        }
                    }
                ]
            )
            
            # Create the deployment
            self.apps_api.create_namespaced_deployment(
                namespace=self.namespace,
                body=deployment
            )
            
            # Create service
            service = self._create_service_object(
                name=name,
                selector={"app": name},
                port=8060,
                target_port=8060
            )
            
            self.core_api.create_namespaced_service(
                namespace=self.namespace,
                body=service
            )
            
            logger.info(f"Deployed storage node {name}")
            return {
                "status": "success",
                "name": name,
                "image": image,
                "replicas": replicas,
                "storage_size": storage_size
            }
        except ApiException as e:
            logger.error(f"Failed to deploy storage node {name}: {e}")
            return {
                "status": "error",
                "name": name,
                "error": str(e)
            }
            
    def _create_deployment_object(self, 
                                 name: str, 
                                 image: str, 
                                 replicas: int = 1, 
                                 port: int = None,
                                 env_vars: Dict[str, str] = None,
                                 volume_mounts: List[Dict[str, Any]] = None,
                                 volumes: List[Dict[str, Any]] = None) -> client.V1Deployment:
        """Create a Kubernetes Deployment object
        
        Args:
            name (str): Deployment name
            image (str): Container image
            replicas (int, optional): Number of replicas
            port (int, optional): Container port
            env_vars (Dict[str, str], optional): Environment variables
            volume_mounts (List[Dict], optional): Volume mounts
            volumes (List[Dict], optional): Volumes
            
        Returns:
            V1Deployment object
        """
        # Convert env_vars dict to K8s env list
        env = []
        if env_vars:
            for key, value in env_vars.items():
                env.append(
                    client.V1EnvVar(
                        name=key,
                        value=str(value)
                    )
                )
                
        # Container
        container = client.V1Container(
            name=name,
            image=image,
            env=env,
            resources=client.V1ResourceRequirements(
                limits={
                    "cpu": K8S_SETTINGS.get("resource_limits", {}).get("cpu", "500m"),
                    "memory": K8S_SETTINGS.get("resource_limits", {}).get("memory", "512Mi")
                },
                requests={
                    "cpu": K8S_SETTINGS.get("resource_requests", {}).get("cpu", "250m"),
                    "memory": K8S_SETTINGS.get("resource_requests", {}).get("memory", "256Mi")
                }
            )
        )
        
        # Add port if specified
        if port:
            container.ports = [client.V1ContainerPort(container_port=port)]
            
        # Add volume mounts if specified
        if volume_mounts:
            container.volume_mounts = []
            for mount in volume_mounts:
                container.volume_mounts.append(
                    client.V1VolumeMount(
                        name=mount["name"],
                        mount_path=mount["mountPath"]
                    )
                )
        
        # Pod template
        pod_template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": name}),
            spec=client.V1PodSpec(containers=[container])
        )
        
        # Add volumes if specified
        if volumes:
            pod_template.spec.volumes = []
            for volume in volumes:
                if "persistentVolumeClaim" in volume:
                    pod_template.spec.volumes.append(
                        client.V1Volume(
                            name=volume["name"],
                            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                                claim_name=volume["persistentVolumeClaim"]["claimName"]
                            )
                        )
                    )
                else:
                    # TODO: Handle other volume types as needed
                    pass
        
        # Deployment spec
        deployment_spec = client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels={"app": name}),
            template=pod_template
        )
        
        # Deployment
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=name),
            spec=deployment_spec
        )
        
        return deployment
    
    def _create_service_object(self, 
                              name: str, 
                              selector: Dict[str, str],
                              port: int, 
                              target_port: int) -> client.V1Service:
        """Create a Kubernetes Service object
        
        Args:
            name (str): Service name
            selector (Dict[str, str]): Pod selector labels
            port (int): Service port
            target_port (int): Container port
            
        Returns:
            V1Service object
        """
        service_spec = client.V1ServiceSpec(
            selector=selector,
            ports=[
                client.V1ServicePort(
                    port=port,
                    target_port=target_port
                )
            ]
        )
        
        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=name),
            spec=service_spec
        )
        
        return service
    
    def _create_pvc_object(self, 
                          name: str, 
                          storage_size: str,
                          access_modes: List[str] = None) -> client.V1PersistentVolumeClaim:
        """Create a Kubernetes PersistentVolumeClaim object
        
        Args:
            name (str): PVC name
            storage_size (str): Storage size (e.g., "10Gi")
            access_modes (List[str], optional): Access modes
            
        Returns:
            V1PersistentVolumeClaim object
        """
        if not access_modes:
            access_modes = ["ReadWriteOnce"]
            
        pvc_spec = client.V1PersistentVolumeClaimSpec(
            access_modes=access_modes,
            resources=client.V1ResourceRequirements(
                requests={"storage": storage_size}
            ),
            storage_class_name=K8S_SETTINGS.get("storage_class", "standard")
        )
        
        pvc = client.V1PersistentVolumeClaim(
            api_version="v1",
            kind="PersistentVolumeClaim",
            metadata=client.V1ObjectMeta(name=name),
            spec=pvc_spec
        )
        
        return pvc
        
# Module functions for easier access
def deploy_blockchain_node(name: str, 
                          image: str = None, 
                          replicas: int = 1,
                          namespace: str = None) -> Dict[str, Any]:
    """Deploy a blockchain node to Kubernetes"""
    k8s = K8sDeployment(namespace=namespace)
    return k8s.deploy_blockchain_node(name, image, replicas)

def deploy_validator_node(name: str, 
                         image: str = None, 
                         replicas: int = 1,
                         namespace: str = None) -> Dict[str, Any]:
    """Deploy a validator node to Kubernetes"""
    k8s = K8sDeployment(namespace=namespace)
    return k8s.deploy_validator_node(name, image, replicas)

def deploy_storage_node(name: str, 
                       image: str = None, 
                       replicas: int = 1,
                       storage_size: str = None,
                       namespace: str = None) -> Dict[str, Any]:
    """Deploy a storage node to Kubernetes"""
    k8s = K8sDeployment(namespace=namespace)
    return k8s.deploy_storage_node(name, image, replicas, storage_size)

def is_kubernetes_available() -> bool:
    """Check if Kubernetes is available"""
    try:
        config.load_kube_config()
        client.CoreV1Api().list_namespace()
        return True
    except Exception:
        try:
            config.load_incluster_config()
            client.CoreV1Api().list_namespace()
            return True
        except Exception:
            return False
            
def create_k8s_resources(manifest_path: str, namespace: str = None) -> Dict[str, Any]:
    """
    Create Kubernetes resources from a YAML manifest
    
    Args:
        manifest_path (str): Path to YAML manifest file
        namespace (str, optional): Kubernetes namespace
        
    Returns:
        Dict with creation results
    """
    if not os.path.exists(manifest_path):
        logger.error(f"Manifest file not found: {manifest_path}")
        return {
            "status": "error",
            "error": f"Manifest file not found: {manifest_path}",
            "created": False
        }
        
    namespace = namespace or K8S_SETTINGS.get("namespace", "metanode")
    
    try:
        # Load the manifest
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load_all(f)
            resources = list(manifest)
            
        # Apply each resource
        created = []
        for resource in resources:
            kind = resource.get('kind', '').lower()
            name = resource.get('metadata', {}).get('name', 'unknown')
            
            # Create command with kubectl (more reliable for complex resources)
            cmd = [
                "kubectl", "apply", 
                "-f", manifest_path,
                "-n", namespace
            ]
            
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            created.append({
                "kind": kind,
                "name": name,
                "output": result.stdout.strip()
            })
            
        return {
            "status": "success",
            "created": True,
            "resources": created
        }
        
    except Exception as e:
        logger.error(f"Failed to create resources from manifest: {e}")
        return {
            "status": "error",
            "error": str(e),
            "created": False
        }

def wait_for_deployment(name: str, namespace: str = None, timeout: int = 300) -> Dict[str, Any]:
    """
    Wait for a deployment to become ready
    
    Args:
        name (str): Deployment name
        namespace (str, optional): Kubernetes namespace
        timeout (int, optional): Timeout in seconds
        
    Returns:
        Dict with deployment status
    """
    namespace = namespace or K8S_SETTINGS.get("namespace", "metanode")
    
    try:
        # Use kubectl to check deployment status (more reliable)
        cmd = [
            "kubectl", "rollout", "status",
            f"deployment/{name}",
            "-n", namespace,
            f"--timeout={timeout}s"
        ]
        
        result = subprocess.run(
            cmd,
            check=True, 
            capture_output=True,
            text=True
        )
        
        return {
            "status": "ready",
            "deployment": name,
            "namespace": namespace,
            "output": result.stdout.strip()
        }
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Deployment {name} not ready: {e}")
        return {
            "status": "error",
            "deployment": name,
            "namespace": namespace,
            "error": e.stderr,
            "ready": False
        }
        
    except Exception as e:
        logger.error(f"Error waiting for deployment {name}: {e}")
        return {
            "status": "error",
            "deployment": name,
            "namespace": namespace,
            "error": str(e),
            "ready": False
        }
