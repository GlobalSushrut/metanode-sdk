#!/usr/bin/env python3
"""
Hospital IoT Manager dApp Device Management
"""

from hospital_mini_core import logger, print_dapp_response, simulate_blockchain_transaction
import time
import uuid

def add_device_methods(HospitalIoTManagerDapp):
    """Add device management methods to the dApp class"""
    
    def create_decentralized_agent(self):
        """Create a decentralized agent for hospital IoT data verification"""
        if not self.connected or not self.agreement_id:
            logger.error("Cannot create agent: Missing connection or agreement")
            print_dapp_response(
                "Agent Creation Failed", 
                {"error": "Missing blockchain connection or agreement"},
                "error"
            )
            return False
        
        logger.info("Creating decentralized agent for IoT data verification...")
        
        try:
            # In a real implementation, we would use:
            # from metanode.dapp import create_agent
            # agent_config = {...}
            # self.agent = create_agent(agent_config, self.blockchain_connection)
            
            # For demo purposes, simulate agent creation
            time.sleep(1.2)  # Simulate creation latency
            self.agent_id = f"agent-{uuid.uuid4()}"
            
            agent_details = {
                "agent_id": self.agent_id,
                "type": "medical-data-verifier",
                "agreement_id": self.agreement_id,
                "capabilities": [
                    "vital_sign_verification",
                    "data_integrity_check",
                    "anomaly_detection"
                ],
                "status": "active"
            }
            
            logger.info(f"Agent created with ID: {self.agent_id}")
            
            # Display the agent response
            print_dapp_response(
                "Decentralized Agent Created",
                agent_details
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            print_dapp_response(
                "Agent Creation Failed", 
                {"error": str(e)},
                "error"
            )
            return False

    def register_iot_device(self, device_id, device_type, department):
        """Register a new IoT medical device in the system"""
        if not self.connected or not self.agent_id:
            logger.error("Cannot register device: Missing connection or agent")
            print_dapp_response(
                "Device Registration Failed", 
                {"error": "Missing blockchain connection or agent"},
                "error"
            )
            return False
        
        logger.info(f"Registering IoT device: {device_id}")
        
        try:
            # In a real implementation, we would use blockchain storage
            # from metanode.blockchain.storage import store_data
            
            # For demo purposes, simulate device registration
            device_info = {
                "id": device_id,
                "type": device_type,
                "department": department,
                "registration_time": time.time(),
                "status": "active"
            }
            
            # Simulate blockchain transaction
            tx = simulate_blockchain_transaction()
            
            # Store in local registry
            self.registered_devices[device_id] = {
                "info": device_info,
                "tx_hash": tx["tx_hash"],
                "block_number": tx["block_number"]
            }
            
            logger.info(f"Device {device_id} registered successfully")
            
            # Display the registration response
            print_dapp_response(
                f"Medical Device Registered: {device_id}",
                {
                    "device": device_info,
                    "blockchain_tx": tx["tx_hash"],
                    "block_number": tx["block_number"]
                }
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to register device: {e}")
            print_dapp_response(
                "Device Registration Failed", 
                {"error": str(e)},
                "error"
            )
            return False

    def get_registered_devices(self):
        """List all registered IoT devices"""
        if not self.registered_devices:
            logger.info("No devices have been registered yet")
            print_dapp_response(
                "No Registered Devices Found",
                {"devices": []}
            )
            return []
        
        devices_list = []
        for device_id, data in self.registered_devices.items():
            devices_list.append({
                "id": device_id,
                "type": data["info"]["type"],
                "department": data["info"]["department"],
                "status": data["info"]["status"]
            })
        
        print_dapp_response(
            f"Found {len(devices_list)} Registered Devices",
            {"devices": devices_list}
        )
        
        return devices_list
    
    # Add the methods to the class
    HospitalIoTManagerDapp.create_decentralized_agent = create_decentralized_agent
    HospitalIoTManagerDapp.register_iot_device = register_iot_device
    HospitalIoTManagerDapp.get_registered_devices = get_registered_devices
    
    return HospitalIoTManagerDapp
