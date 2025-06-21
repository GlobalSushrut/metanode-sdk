#!/usr/bin/env python3
"""
MetaNode SDK - Server Mining Module
==================================

Tools for resource mining, tracking usage metrics, and reporting to the ledger.
"""

import os
import json
import time
import psutil
import hashlib
import logging
import requests
import threading
from typing import Dict, Any, Optional, List, Union, Callable
from ..config.endpoints import API_URL, BLOCKCHAIN_URL, BFR_URL

# Configure logging
logger = logging.getLogger(__name__)

class ResourceMining:
    """Manages resource mining operations for MetaNode servers."""
    
    def __init__(self, api_url: Optional[str] = None, server_id: Optional[str] = None):
        """
        Initialize resource mining manager.
        
        Args:
            api_url (str, optional): API URL for the MetaNode testnet
            server_id (str, optional): Server ID for the mining node
        """
        self.api_url = api_url or API_URL
        self.server_id = server_id
        self.mining_active = False
        self.mining_thread = None
        self.mining_interval = 60  # Default: report every 60 seconds
        self.start_time = None
        self.total_usage_metrics = {
            "cpu_seconds": 0,
            "memory_mb_seconds": 0,
            "network_bytes": 0,
            "storage_bytes": 0
        }
        self.callbacks = []
        
        # Try to load server ID from file if not provided
        if not self.server_id:
            try:
                server_file = os.path.join(os.getcwd(), ".metanode", "server.json")
                if os.path.exists(server_file):
                    with open(server_file, 'r') as f:
                        data = json.load(f)
                        self.server_id = data.get("server_id")
            except Exception as e:
                logger.warning(f"Failed to load server ID from file: {e}")
    
    def start_resource_mining(self, interval: int = 60) -> Dict[str, Any]:
        """
        Begin tracking usage metrics for reward eligibility.
        
        Args:
            interval (int): Interval in seconds between usage reports
            
        Returns:
            dict: Mining start status
        """
        try:
            # Check if we have a server ID
            if not self.server_id:
                return {
                    "status": "error", 
                    "message": "No server ID. Register server first."
                }
            
            # Check if mining is already active
            if self.mining_active:
                return {
                    "status": "error", 
                    "message": "Mining is already active."
                }
            
            # Set mining parameters
            self.mining_interval = interval
            self.mining_active = True
            self.start_time = time.time()
            
            # Reset usage metrics
            self.total_usage_metrics = {
                "cpu_seconds": 0,
                "memory_mb_seconds": 0,
                "network_bytes": 0,
                "storage_bytes": 0
            }
            
            # Notify API about mining start
            response = requests.post(
                f"{self.api_url}/mining/start",
                headers={"Content-Type": "application/json"},
                json={
                    "server_id": self.server_id,
                    "timestamp": int(self.start_time),
                    "interval": interval
                }
            )
            
            api_response = {}
            if response.status_code == 200:
                api_response = response.json()
                logger.info(f"Successfully registered mining start with API")
            else:
                logger.warning(f"Failed to register mining start with API: {response.text}")
            
            # Start mining thread
            self.mining_thread = threading.Thread(
                target=self._mining_loop,
                args=(interval,),
                daemon=True
            )
            self.mining_thread.start()
            
            logger.info(f"Started resource mining with {interval}s interval")
            return {
                "status": "success",
                "mining_active": True,
                "start_time": self.start_time,
                "interval": interval,
                "api_response": api_response
            }
            
        except Exception as e:
            logger.error(f"Failed to start mining: {e}")
            self.mining_active = False
            return {"status": "error", "message": str(e)}
    
    def stop_k8_instance(self) -> Dict[str, Any]:
        """
        Gracefully halt server and settle state.
        
        Returns:
            dict: Server stop status
        """
        try:
            # Check if mining is active
            if self.mining_active:
                # Stop mining loop
                self.mining_active = False
                if self.mining_thread and self.mining_thread.is_alive():
                    # Wait for thread to finish (with timeout)
                    self.mining_thread.join(timeout=5)
            
            # Get final metrics
            final_metrics = self._collect_usage_metrics()
            final_metrics.update(self.total_usage_metrics)
            
            # Calculate mining duration
            end_time = time.time()
            duration = end_time - (self.start_time or end_time)
            
            # Notify API about mining stop
            response = requests.post(
                f"{self.api_url}/mining/stop",
                headers={"Content-Type": "application/json"},
                json={
                    "server_id": self.server_id,
                    "start_time": self.start_time,
                    "end_time": end_time,
                    "duration": duration,
                    "final_metrics": final_metrics
                }
            )
            
            api_response = {}
            if response.status_code == 200:
                api_response = response.json()
                logger.info(f"Successfully registered mining stop with API")
            else:
                logger.warning(f"Failed to register mining stop with API: {response.text}")
            
            # Reset mining state
            self.start_time = None
            self.mining_thread = None
            
            # Save mining report
            report = {
                "server_id": self.server_id,
                "mining_duration": duration,
                "start_time": self.start_time,
                "end_time": end_time,
                "final_metrics": final_metrics,
                "api_response": api_response
            }
            
            mining_dir = os.path.join(os.getcwd(), ".metanode", "mining")
            os.makedirs(mining_dir, exist_ok=True)
            
            report_file = os.path.join(mining_dir, f"mining-report-{int(end_time)}.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Stopped resource mining after {duration:.2f} seconds")
            return {
                "status": "success",
                "mining_duration": duration,
                "final_metrics": final_metrics,
                "report_file": report_file,
                "api_response": api_response
            }
            
        except Exception as e:
            logger.error(f"Failed to stop mining: {e}")
            return {"status": "error", "message": str(e)}
    
    def report_resource_usage(self, metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Report memory/CPU/runtime to ledger for mining payouts.
        
        Args:
            metrics (dict, optional): Custom metrics to report. If None, 
                                     current metrics will be collected.
                                     
        Returns:
            dict: Report status
        """
        try:
            # Check if we have a server ID
            if not self.server_id:
                return {
                    "status": "error", 
                    "message": "No server ID. Register server first."
                }
            
            # Collect metrics if not provided
            if not metrics:
                metrics = self._collect_usage_metrics()
            
            # Add timestamp and server ID
            report = {
                "server_id": self.server_id,
                "timestamp": int(time.time()),
                "metrics": metrics
            }
            
            # Send report to API
            response = requests.post(
                f"{self.api_url}/mining/report",
                headers={"Content-Type": "application/json"},
                json=report
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully reported usage metrics")
                return {
                    "status": "success",
                    "report": report,
                    "response": data
                }
            else:
                logger.error(f"Failed to report metrics: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Failed to report metrics: {e}")
            return {"status": "error", "message": str(e)}
    
    def register_callback(self, callback: Callable[[Dict[str, Any]], None]) -> Dict[str, Any]:
        """
        Register a callback function to be called after each metrics report.
        
        Args:
            callback: Function to call with metrics as argument
            
        Returns:
            dict: Registration status
        """
        try:
            self.callbacks.append(callback)
            return {
                "status": "success", 
                "message": f"Registered callback: {callback.__name__}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _collect_usage_metrics(self) -> Dict[str, Any]:
        """
        Collect current system usage metrics.
        
        Returns:
            dict: Current usage metrics
        """
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_used_mb = memory.used / (1024 * 1024)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_used_gb = disk.used / (1024 * 1024 * 1024)
            
            # Network usage
            net_io = psutil.net_io_counters()
            net_bytes_sent = net_io.bytes_sent
            net_bytes_recv = net_io.bytes_recv
            
            return {
                "cpu": {
                    "percent": cpu_percent,
                    "cores": cpu_count
                },
                "memory": {
                    "used_mb": memory_used_mb,
                    "percent": memory.percent
                },
                "disk": {
                    "used_gb": disk_used_gb,
                    "percent": disk.percent
                },
                "network": {
                    "bytes_sent": net_bytes_sent,
                    "bytes_recv": net_bytes_recv
                }
            }
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {"error": str(e)}
    
    def _mining_loop(self, interval: int):
        """
        Background loop for periodic metric reporting.
        
        Args:
            interval (int): Seconds between reports
        """
        while self.mining_active:
            try:
                # Collect metrics
                metrics = self._collect_usage_metrics()
                
                # Update cumulative metrics
                time_delta = interval
                self.total_usage_metrics["cpu_seconds"] += metrics["cpu"]["percent"] * time_delta * metrics["cpu"]["cores"] / 100
                self.total_usage_metrics["memory_mb_seconds"] += metrics["memory"]["used_mb"] * time_delta
                self.total_usage_metrics["network_bytes"] += metrics["network"]["bytes_sent"] + metrics["network"]["bytes_recv"]
                
                # Report metrics
                report_result = self.report_resource_usage(metrics)
                
                # Call registered callbacks
                for callback in self.callbacks:
                    try:
                        callback({
                            "metrics": metrics,
                            "total": self.total_usage_metrics,
                            "report_result": report_result
                        })
                    except Exception as e:
                        logger.error(f"Error in callback: {e}")
                
                # Wait for next interval
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in mining loop: {e}")
                time.sleep(interval)  # Continue despite errors


# Simple usage example
if __name__ == "__main__":
    # Create resource mining manager with server ID
    mining = ResourceMining(server_id="demo-server-123")
    
    # Define a callback for metric reports
    def metric_callback(data):
        print(f"Mining metrics update: CPU {data['metrics']['cpu']['percent']}%, "
              f"Memory {data['metrics']['memory']['percent']}%")
    
    # Register callback
    mining.register_callback(metric_callback)
    
    # Start mining
    print("Starting resource mining...")
    result = mining.start_resource_mining(interval=10)
    print(f"Mining start: {json.dumps(result, indent=2)}")
    
    # Let it run for a minute
    print("Mining for 60 seconds...")
    time.sleep(60)
    
    # Stop mining
    print("Stopping resource mining...")
    stop_result = mining.stop_k8_instance()
    print(f"Mining stop: {json.dumps(stop_result, indent=2)}")
