#!/usr/bin/env python3
"""
MetaNode SDK - IPFS Tools Module
==============================

Utilities for interacting with IPFS distributed file storage in MetaNode.
"""

import os
import json
import time
import logging
import requests
import base64
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL

# Configure logging
logger = logging.getLogger(__name__)

class IPFSManager:
    """Manages IPFS operations for MetaNode distributed storage."""
    
    def __init__(self, api_url: Optional[str] = None, ipfs_node: Optional[str] = None):
        """
        Initialize IPFS manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            ipfs_node (str, optional): Direct IPFS node URL if available
        """
        self.api_url = api_url or API_URL
        self.ipfs_node = ipfs_node or f"{self.api_url}/ipfs"
        self.utils_dir = os.path.join(os.getcwd(), ".metanode", "utils")
        self.ipfs_dir = os.path.join(self.utils_dir, "ipfs")
        
        # Ensure directories exist
        os.makedirs(self.ipfs_dir, exist_ok=True)
    
    def add_file(self, file_path: str) -> Dict[str, Any]:
        """
        Add a file to IPFS storage.
        
        Args:
            file_path (str): Path to the file to upload
            
        Returns:
            dict: Upload result with IPFS hash
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "status": "error", 
                    "message": f"File not found: {file_path}"
                }
            
            # Read file contents
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Get file name
            file_name = os.path.basename(file_path)
            
            # Send file to IPFS via API
            files = {
                'file': (file_name, file_data)
            }
            
            response = requests.post(
                f"{self.ipfs_node}/add",
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                ipfs_hash = result.get("Hash")
                
                # Save metadata
                metadata = {
                    "file_name": file_name,
                    "file_path": file_path,
                    "ipfs_hash": ipfs_hash,
                    "size": os.path.getsize(file_path),
                    "timestamp": int(time.time())
                }
                
                metadata_file = os.path.join(self.ipfs_dir, f"file-{ipfs_hash}.json")
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                logger.info(f"Added file {file_name} to IPFS with hash {ipfs_hash}")
                return {
                    "status": "success",
                    "file_name": file_name,
                    "ipfs_hash": ipfs_hash,
                    "size": metadata["size"],
                    "metadata_file": metadata_file
                }
            else:
                logger.error(f"Failed to add file to IPFS: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPFS add error: {e}")
            return {"status": "error", "message": str(e)}
    
    def add_json(self, data: Dict[str, Any], name: Optional[str] = None) -> Dict[str, Any]:
        """
        Add JSON data to IPFS storage.
        
        Args:
            data (dict): JSON data to store
            name (str, optional): Name for the data
            
        Returns:
            dict: Upload result with IPFS hash
        """
        try:
            # Prepare JSON data
            json_data = json.dumps(data)
            
            # Generate name if not provided
            if not name:
                name = f"json-{int(time.time())}"
            
            # Send data to IPFS via API
            response = requests.post(
                f"{self.ipfs_node}/add",
                files={
                    'file': (f"{name}.json", json_data.encode())
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                ipfs_hash = result.get("Hash")
                
                # Save metadata and a copy of the data
                metadata = {
                    "name": name,
                    "ipfs_hash": ipfs_hash,
                    "size": len(json_data),
                    "timestamp": int(time.time()),
                    "data": data
                }
                
                metadata_file = os.path.join(self.ipfs_dir, f"json-{ipfs_hash}.json")
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                logger.info(f"Added JSON data with name {name} to IPFS with hash {ipfs_hash}")
                return {
                    "status": "success",
                    "name": name,
                    "ipfs_hash": ipfs_hash,
                    "size": metadata["size"],
                    "metadata_file": metadata_file
                }
            else:
                logger.error(f"Failed to add JSON to IPFS: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPFS add JSON error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_file(self, ipfs_hash: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a file from IPFS storage.
        
        Args:
            ipfs_hash (str): IPFS hash of the file
            output_path (str, optional): Path to save the file to
            
        Returns:
            dict: Download result with file path
        """
        try:
            # Query IPFS for the file
            response = requests.get(f"{self.ipfs_node}/cat?arg={ipfs_hash}")
            
            if response.status_code == 200:
                # Determine output path
                if not output_path:
                    # Look for metadata
                    metadata_file = os.path.join(self.ipfs_dir, f"file-{ipfs_hash}.json")
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        file_name = metadata.get("file_name", f"ipfs-{ipfs_hash}")
                    else:
                        file_name = f"ipfs-{ipfs_hash}"
                    
                    output_path = os.path.join(self.ipfs_dir, "downloads", file_name)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save file
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(output_path)
                logger.info(f"Retrieved file from IPFS hash {ipfs_hash} to {output_path} ({file_size} bytes)")
                return {
                    "status": "success",
                    "ipfs_hash": ipfs_hash,
                    "file_path": output_path,
                    "size": file_size
                }
            else:
                logger.error(f"Failed to get file from IPFS: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPFS get error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_json(self, ipfs_hash: str) -> Dict[str, Any]:
        """
        Get JSON data from IPFS storage.
        
        Args:
            ipfs_hash (str): IPFS hash of the JSON data
            
        Returns:
            dict: Download result with JSON data
        """
        try:
            # Query IPFS for the JSON data
            response = requests.get(f"{self.ipfs_node}/cat?arg={ipfs_hash}")
            
            if response.status_code == 200:
                # Parse JSON content
                try:
                    data = json.loads(response.text)
                    
                    # Save a copy locally
                    json_file = os.path.join(self.ipfs_dir, "downloads", f"{ipfs_hash}.json")
                    os.makedirs(os.path.dirname(json_file), exist_ok=True)
                    
                    with open(json_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    logger.info(f"Retrieved JSON from IPFS hash {ipfs_hash}")
                    return {
                        "status": "success",
                        "ipfs_hash": ipfs_hash,
                        "data": data,
                        "json_file": json_file
                    }
                except json.JSONDecodeError:
                    logger.error("Retrieved data is not valid JSON")
                    return {"status": "error", "message": "Retrieved data is not valid JSON"}
            else:
                logger.error(f"Failed to get JSON from IPFS: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPFS get JSON error: {e}")
            return {"status": "error", "message": str(e)}
    
    def pin_hash(self, ipfs_hash: str) -> Dict[str, Any]:
        """
        Pin a hash to keep it in IPFS storage.
        
        Args:
            ipfs_hash (str): IPFS hash to pin
            
        Returns:
            dict: Pin operation result
        """
        try:
            # Send pin request
            response = requests.post(
                f"{self.ipfs_node}/pin/add?arg={ipfs_hash}"
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Save pin information
                pin_info = {
                    "ipfs_hash": ipfs_hash,
                    "pinned_at": int(time.time()),
                    "pins": result.get("Pins", [])
                }
                
                pin_file = os.path.join(self.ipfs_dir, f"pin-{ipfs_hash}.json")
                with open(pin_file, 'w') as f:
                    json.dump(pin_info, f, indent=2)
                
                logger.info(f"Pinned IPFS hash {ipfs_hash}")
                return {
                    "status": "success",
                    "ipfs_hash": ipfs_hash,
                    "pins": result.get("Pins", []),
                    "pin_file": pin_file
                }
            else:
                logger.error(f"Failed to pin hash: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPFS pin error: {e}")
            return {"status": "error", "message": str(e)}
    
    def unpin_hash(self, ipfs_hash: str) -> Dict[str, Any]:
        """
        Unpin a hash from IPFS storage.
        
        Args:
            ipfs_hash (str): IPFS hash to unpin
            
        Returns:
            dict: Unpin operation result
        """
        try:
            # Send unpin request
            response = requests.post(
                f"{self.ipfs_node}/pin/rm?arg={ipfs_hash}"
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Update pin information if it exists
                pin_file = os.path.join(self.ipfs_dir, f"pin-{ipfs_hash}.json")
                if os.path.exists(pin_file):
                    with open(pin_file, 'r') as f:
                        pin_info = json.load(f)
                    
                    pin_info["unpinned_at"] = int(time.time())
                    pin_info["status"] = "unpinned"
                    
                    with open(pin_file, 'w') as f:
                        json.dump(pin_info, f, indent=2)
                
                logger.info(f"Unpinned IPFS hash {ipfs_hash}")
                return {
                    "status": "success",
                    "ipfs_hash": ipfs_hash,
                    "pins": result.get("Pins", [])
                }
            else:
                logger.error(f"Failed to unpin hash: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPFS unpin error: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_pins(self) -> Dict[str, Any]:
        """
        List all pinned hashes.
        
        Returns:
            dict: List of pinned hashes
        """
        try:
            # Send list pins request
            response = requests.get(
                f"{self.ipfs_node}/pin/ls"
            )
            
            if response.status_code == 200:
                result = response.json()
                pins = result.get("Keys", {})
                
                # Save pins list
                pins_info = {
                    "pins": pins,
                    "timestamp": int(time.time())
                }
                
                pins_file = os.path.join(self.ipfs_dir, f"pins-list-{int(time.time())}.json")
                with open(pins_file, 'w') as f:
                    json.dump(pins_info, f, indent=2)
                
                logger.info(f"Listed {len(pins)} pinned IPFS hashes")
                return {
                    "status": "success",
                    "pins": pins,
                    "count": len(pins),
                    "pins_file": pins_file
                }
            else:
                logger.error(f"Failed to list pins: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPFS list pins error: {e}")
            return {"status": "error", "message": str(e)}
    
    def publish_to_ipns(self, ipfs_hash: str, key_name: str = "self") -> Dict[str, Any]:
        """
        Publish an IPFS hash to IPNS.
        
        Args:
            ipfs_hash (str): IPFS hash to publish
            key_name (str): IPNS key name to use (default: "self")
            
        Returns:
            dict: Publish operation result
        """
        try:
            # Send publish request
            response = requests.post(
                f"{self.ipfs_node}/name/publish?arg={ipfs_hash}&key={key_name}"
            )
            
            if response.status_code == 200:
                result = response.json()
                ipns_name = result.get("Name")
                
                # Save publish information
                publish_info = {
                    "ipfs_hash": ipfs_hash,
                    "ipns_name": ipns_name,
                    "key_name": key_name,
                    "published_at": int(time.time()),
                    "result": result
                }
                
                publish_file = os.path.join(self.ipfs_dir, f"ipns-{ipns_name}.json")
                with open(publish_file, 'w') as f:
                    json.dump(publish_info, f, indent=2)
                
                logger.info(f"Published {ipfs_hash} to IPNS name {ipns_name}")
                return {
                    "status": "success",
                    "ipfs_hash": ipfs_hash,
                    "ipns_name": ipns_name,
                    "publish_file": publish_file
                }
            else:
                logger.error(f"Failed to publish to IPNS: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPNS publish error: {e}")
            return {"status": "error", "message": str(e)}
    
    def resolve_ipns(self, ipns_name: str) -> Dict[str, Any]:
        """
        Resolve an IPNS name to an IPFS hash.
        
        Args:
            ipns_name (str): IPNS name to resolve
            
        Returns:
            dict: Resolve operation result
        """
        try:
            # Send resolve request
            response = requests.post(
                f"{self.ipfs_node}/name/resolve?arg={ipns_name}"
            )
            
            if response.status_code == 200:
                result = response.json()
                path = result.get("Path")
                
                # Extract IPFS hash from path
                ipfs_hash = path.split("/")[-1] if path else None
                
                logger.info(f"Resolved IPNS name {ipns_name} to {path}")
                return {
                    "status": "success",
                    "ipns_name": ipns_name,
                    "path": path,
                    "ipfs_hash": ipfs_hash
                }
            else:
                logger.error(f"Failed to resolve IPNS name: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"IPNS resolve error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create IPFS manager
    ipfs_manager = IPFSManager()
    
    # Add a sample JSON object
    sample_data = {
        "name": "MetaNode Test",
        "description": "IPFS test data",
        "timestamp": int(time.time())
    }
    
    add_result = ipfs_manager.add_json(sample_data, "sample-data")
    print(f"Add JSON: {json.dumps(add_result, indent=2)}")
    
    # Pin the hash
    if add_result["status"] == "success":
        pin_result = ipfs_manager.pin_hash(add_result["ipfs_hash"])
        print(f"Pin hash: {json.dumps(pin_result, indent=2)}")
        
        # Get the JSON back
        get_result = ipfs_manager.get_json(add_result["ipfs_hash"])
        print(f"Get JSON: {json.dumps(get_result, indent=2)}")
