"""
MetaNode SDK Docker Utilities Module
==================================

Provides Docker-related utilities for:
- Docker container management
- Docker image operations
- Docker networking
- Docker locks for blockchain components
"""

import os
import json
import time
import logging
import subprocess
from typing import Dict, List, Any, Optional, Union, Tuple

# Configure logging
logger = logging.getLogger("metanode-docker")

class DockerManager:
    """Docker operations manager for MetaNode SDK"""
    
    def __init__(self, docker_lock_path: str = "/tmp/docker.lock"):
        self.docker_lock_path = docker_lock_path
        self._check_docker_available()
        self._ensure_lock_file()
    
    def _check_docker_available(self) -> bool:
        """Check if Docker is installed and available"""
        try:
            result = subprocess.run(
                ["docker", "--version"], 
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"Docker found: {result.stdout.strip()}")
            return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.warning(f"Docker not available: {e}")
            return False
    
    def _ensure_lock_file(self) -> None:
        """Ensure docker.lock file exists"""
        if not os.path.exists(self.docker_lock_path):
            with open(self.docker_lock_path, "w") as f:
                lock_data = {
                    "timestamp": int(time.time()),
                    "locked_by": "metanode-sdk",
                    "status": "active"
                }
                json.dump(lock_data, f)
            logger.info(f"Created docker.lock at {self.docker_lock_path}")
    
    def run_container(self, 
                     image: str, 
                     name: str = None, 
                     ports: Dict[str, str] = None,
                     volumes: Dict[str, str] = None,
                     environment: Dict[str, str] = None,
                     detach: bool = True) -> Dict[str, Any]:
        """Run a Docker container"""
        
        cmd = ["docker", "run"]
        
        if detach:
            cmd.append("-d")
        
        if name:
            cmd.extend(["--name", name])
        
        if ports:
            for host_port, container_port in ports.items():
                cmd.extend(["-p", f"{host_port}:{container_port}"])
        
        if volumes:
            for host_path, container_path in volumes.items():
                cmd.extend(["-v", f"{host_path}:{container_path}"])
        
        if environment:
            for key, value in environment.items():
                cmd.extend(["-e", f"{key}={value}"])
        
        cmd.append(image)
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            container_id = result.stdout.strip()
            
            return {
                "status": "success",
                "container_id": container_id,
                "image": image,
                "name": name
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to run container: {e}")
            logger.error(f"Error output: {e.stderr}")
            
            return {
                "status": "error",
                "error": e.stderr,
                "command": " ".join(cmd)
            }
    
    def stop_container(self, container_id_or_name: str) -> Dict[str, Any]:
        """Stop a running Docker container"""
        try:
            subprocess.run(
                ["docker", "stop", container_id_or_name],
                check=True,
                capture_output=True,
                text=True
            )
            
            return {
                "status": "success",
                "container": container_id_or_name,
                "message": f"Container {container_id_or_name} stopped"
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop container {container_id_or_name}: {e}")
            
            return {
                "status": "error",
                "error": e.stderr,
                "container": container_id_or_name
            }
    
    def list_containers(self, all_containers: bool = False) -> List[Dict[str, Any]]:
        """List Docker containers"""
        cmd = ["docker", "ps", "--format", "{{json .}}"]
        
        if all_containers:
            cmd.append("-a")
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            containers = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        container = json.loads(line)
                        containers.append(container)
                    except json.JSONDecodeError:
                        logger.warning(f"Could not parse container info: {line}")
            
            return containers
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list containers: {e}")
            return []
    
    def create_network(self, name: str, driver: str = "bridge") -> Dict[str, Any]:
        """Create a Docker network"""
        try:
            result = subprocess.run(
                ["docker", "network", "create", "--driver", driver, name],
                check=True,
                capture_output=True,
                text=True
            )
            
            network_id = result.stdout.strip()
            
            return {
                "status": "success",
                "network_id": network_id,
                "name": name,
                "driver": driver
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create network {name}: {e}")
            
            return {
                "status": "error",
                "error": e.stderr,
                "name": name
            }

def is_docker_available() -> bool:
    """Check if Docker is installed and available"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            check=False,  # Don't raise exception on error
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def create_docker_lock() -> str:
    """Create docker.lock file used by blockchain components"""
    lock_path = "/tmp/docker.lock"
    
    if not os.path.exists(lock_path):
        with open(lock_path, "w") as f:
            f.write(f"locked:{int(time.time())}")
        logger.info(f"Created docker.lock at {lock_path}")
    
    return lock_path

def get_docker_lock_status() -> Dict[str, Any]:
    """Get status from docker.lock file"""
    lock_path = "/tmp/docker.lock"
    
    if not os.path.exists(lock_path):
        return {
            "status": "not_found",
            "exists": False
        }
    
    try:
        with open(lock_path, "r") as f:
            content = f.read().strip()
            
        if ":" in content:
            key, value = content.split(":", 1)
            try:
                lock_time = int(value)
                return {
                    "status": "valid",
                    "exists": True,
                    "locked_at": lock_time,
                    "locked_since": int(time.time()) - lock_time,
                    "key": key
                }
            except ValueError:
                return {
                    "status": "invalid",
                    "exists": True,
                    "content": content
                }
        else:
            return {
                "status": "invalid",
                "exists": True,
                "content": content
            }
    except Exception as e:
        return {
            "status": "error",
            "exists": True,
            "error": str(e)
        }

def ensure_docker_running() -> Dict[str, Any]:
    """Ensure Docker daemon is running and create lock file
    
    Returns:
        Dict with status of Docker daemon and lock file
    """
    # First check if Docker is available
    if not is_docker_available():
        logger.error("Docker is not available or not installed")
        return {
            "status": "error",
            "docker_running": False,
            "error": "Docker is not available or not installed"
        }
    
    # Create or check lock file
    lock_path = create_docker_lock()
    lock_status = get_docker_lock_status()
    
    # Check if any containers are running (simple check for Docker daemon)
    try:
        result = subprocess.run(
            ["docker", "ps", "-q"],
            check=False,
            capture_output=True,
            text=True
        )
        
        docker_running = result.returncode == 0
    except Exception:
        docker_running = False
    
    return {
        "status": "success" if docker_running else "error",
        "docker_running": docker_running,
        "lock_status": lock_status,
        "lock_path": lock_path
    }
