#!/usr/bin/env python3
"""
MetaNode SDK - Admin Security Module
=================================

Security tools for MetaNode testnet administration.
"""

import os
import json
import time
import hashlib
import logging
import requests
from typing import Dict, Any, Optional, List, Union
from ..config.endpoints import API_URL, BLOCKCHAIN_URL

# Configure logging
logger = logging.getLogger(__name__)

class SecurityManager:
    """Manages security functions for MetaNode testnet administration."""
    
    def __init__(self, api_url: Optional[str] = None, admin_key: Optional[str] = None):
        """
        Initialize security manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            admin_key (str, optional): Admin API key for authentication
        """
        self.api_url = api_url or API_URL
        self.admin_key = admin_key
        self.admin_dir = os.path.join(os.getcwd(), ".metanode", "admin")
        self.security_dir = os.path.join(self.admin_dir, "security")
        
        # Ensure directories exist
        os.makedirs(self.security_dir, exist_ok=True)
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for admin API calls."""
        headers = {"Content-Type": "application/json"}
        if self.admin_key:
            headers["X-Admin-Key"] = self.admin_key
        return headers
    
    def list_api_keys(self) -> Dict[str, Any]:
        """
        List all API keys in the system.
        
        Returns:
            dict: List of API keys (with masked values)
        """
        try:
            # Query API for keys
            response = requests.get(
                f"{self.api_url}/admin/security/keys",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                keys_data = response.json()
                
                # Save keys information (safe to save as they're masked)
                keys_file = os.path.join(self.security_dir, f"api-keys-{int(time.time())}.json")
                with open(keys_file, 'w') as f:
                    json.dump(keys_data, f, indent=2)
                
                keys = keys_data.get("keys", [])
                logger.info(f"Retrieved {len(keys)} API keys")
                return {
                    "status": "success",
                    "keys": keys,
                    "count": len(keys),
                    "keys_file": keys_file
                }
            else:
                logger.error(f"Failed to list API keys: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"API key listing error: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_api_key(self, description: str, permissions: List[str]) -> Dict[str, Any]:
        """
        Create a new API key with the specified permissions.
        
        Args:
            description (str): Description for the API key
            permissions (list): List of permission strings
            
        Returns:
            dict: Creation operation result with key value
        """
        try:
            # Send create command to API
            response = requests.post(
                f"{self.api_url}/admin/security/keys",
                headers=self._get_auth_headers(),
                json={
                    "description": description,
                    "permissions": permissions
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                key_id = result.get("key_id")
                key_value = result.get("key_value")  # Full API key, only returned once
                
                # Save key information securely (without actual key value)
                key_info = {
                    "key_id": key_id,
                    "description": description,
                    "permissions": permissions,
                    "created_at": int(time.time())
                }
                
                key_file = os.path.join(self.security_dir, f"api-key-{key_id}-info.json")
                with open(key_file, 'w') as f:
                    json.dump(key_info, f, indent=2)
                
                logger.info(f"Created API key with ID {key_id}")
                return {
                    "status": "success",
                    "key_id": key_id,
                    "key_value": key_value,
                    "description": description,
                    "permissions": permissions,
                    "key_file": key_file,
                    "note": "Record the key_value securely. It won't be shown again."
                }
            else:
                logger.error(f"Failed to create API key: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"API key creation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def revoke_api_key(self, key_id: str) -> Dict[str, Any]:
        """
        Revoke an API key.
        
        Args:
            key_id (str): ID of the API key to revoke
            
        Returns:
            dict: Revocation result
        """
        try:
            # Send revoke command to API
            response = requests.delete(
                f"{self.api_url}/admin/security/keys/{key_id}",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Update key information file if it exists
                key_file = os.path.join(self.security_dir, f"api-key-{key_id}-info.json")
                if os.path.exists(key_file):
                    with open(key_file, 'r') as f:
                        key_info = json.load(f)
                    
                    key_info["revoked_at"] = int(time.time())
                    key_info["active"] = False
                    
                    with open(key_file, 'w') as f:
                        json.dump(key_info, f, indent=2)
                
                logger.info(f"Revoked API key {key_id}")
                return {
                    "status": "success",
                    "key_id": key_id,
                    "revocation_result": result
                }
            else:
                logger.error(f"Failed to revoke API key: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"API key revocation error: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_access_logs(self, limit: int = 100) -> Dict[str, Any]:
        """
        List access logs for the system.
        
        Args:
            limit (int): Maximum number of logs to retrieve
            
        Returns:
            dict: List of access logs
        """
        try:
            # Query API for access logs
            response = requests.get(
                f"{self.api_url}/admin/security/access_logs",
                headers=self._get_auth_headers(),
                params={"limit": limit}
            )
            
            if response.status_code == 200:
                logs_data = response.json()
                
                # Save logs information
                logs_file = os.path.join(self.security_dir, f"access-logs-{int(time.time())}.json")
                with open(logs_file, 'w') as f:
                    json.dump(logs_data, f, indent=2)
                
                logs = logs_data.get("logs", [])
                logger.info(f"Retrieved {len(logs)} access logs")
                return {
                    "status": "success",
                    "logs": logs,
                    "count": len(logs),
                    "logs_file": logs_file
                }
            else:
                logger.error(f"Failed to list access logs: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Access logs listing error: {e}")
            return {"status": "error", "message": str(e)}
    
    def check_security_status(self) -> Dict[str, Any]:
        """
        Check overall security status of the MetaNode testnet.
        
        Returns:
            dict: Security status information
        """
        try:
            # Query API for security status
            response = requests.get(
                f"{self.api_url}/admin/security/status",
                headers=self._get_auth_headers()
            )
            
            if response.status_code == 200:
                status_data = response.json()
                
                # Save status information
                status_file = os.path.join(self.security_dir, f"security-status-{int(time.time())}.json")
                with open(status_file, 'w') as f:
                    json.dump(status_data, f, indent=2)
                
                logger.info(f"Retrieved security status")
                return {
                    "status": "success",
                    "security_status": status_data,
                    "status_file": status_file
                }
            else:
                logger.error(f"Failed to check security status: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Security status check error: {e}")
            return {"status": "error", "message": str(e)}
    
    def update_firewall_rules(self, rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update firewall rules for the testnet.
        
        Args:
            rules (list): List of firewall rule dictionaries
            
        Returns:
            dict: Update operation result
        """
        try:
            # Send update command to API
            response = requests.put(
                f"{self.api_url}/admin/security/firewall",
                headers=self._get_auth_headers(),
                json={"rules": rules}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Save updated rules
                rules_file = os.path.join(self.security_dir, f"firewall-rules-{int(time.time())}.json")
                with open(rules_file, 'w') as f:
                    json.dump({"rules": rules, "updated_at": int(time.time())}, f, indent=2)
                
                logger.info(f"Updated firewall rules")
                return {
                    "status": "success",
                    "update_result": result,
                    "rules_count": len(rules),
                    "rules_file": rules_file
                }
            else:
                logger.error(f"Failed to update firewall rules: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Firewall rules update error: {e}")
            return {"status": "error", "message": str(e)}
    
    def generate_audit_report(self, start_time: int, end_time: int) -> Dict[str, Any]:
        """
        Generate a security audit report for a time period.
        
        Args:
            start_time (int): Start timestamp (Unix time)
            end_time (int): End timestamp (Unix time)
            
        Returns:
            dict: Audit report
        """
        try:
            # Query API for audit report
            response = requests.post(
                f"{self.api_url}/admin/security/audit",
                headers=self._get_auth_headers(),
                json={
                    "start_time": start_time,
                    "end_time": end_time
                }
            )
            
            if response.status_code == 200:
                report_data = response.json()
                
                # Save report information
                report_file = os.path.join(
                    self.security_dir, 
                    f"audit-report-{start_time}-to-{end_time}.json"
                )
                with open(report_file, 'w') as f:
                    json.dump(report_data, f, indent=2)
                
                events = report_data.get("events", [])
                logger.info(f"Generated audit report with {len(events)} events")
                return {
                    "status": "success",
                    "report": report_data,
                    "events_count": len(events),
                    "report_file": report_file
                }
            else:
                logger.error(f"Failed to generate audit report: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Audit report generation error: {e}")
            return {"status": "error", "message": str(e)}


# Simple usage example
if __name__ == "__main__":
    # Create security manager
    security = SecurityManager(admin_key="sample-admin-key")
    
    # Check security status
    status_result = security.check_security_status()
    print(f"Security status: {json.dumps(status_result, indent=2)}")
    
    # List API keys
    keys_result = security.list_api_keys()
    print(f"API keys: {json.dumps(keys_result, indent=2)}")
