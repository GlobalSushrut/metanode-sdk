#!/usr/bin/env python3
"""
Hospital IoT Manager dApp Demo Runner
====================================
This script demonstrates how the deployed Hospital IoT Manager dApp
behaves with blockchain interactions.
"""

from hospital_mini_core import logger, print_dapp_response, generate_vital_signs
from hospital_mini_dapp import HospitalIoTManagerDapp
from hospital_mini_device import add_device_methods
import time

def add_data_handling_methods(HospitalIoTManagerDapp):
    """Add data handling methods to the dApp class"""
    
    def receive_iot_data(self, device_id, patient_id, vital_data):
        """Receive and process data from an IoT medical device"""
        if device_id not in self.registered_devices:
            logger.error(f"Unknown device: {device_id}")
            print_dapp_response(
                "Data Submission Failed", 
                {"error": f"Unknown device: {device_id}"},
                "error"
            )
            return False
        
        logger.info(f"Receiving data from device {device_id} for patient {patient_id}")
        
        try:
            # Add timestamp and metadata
            timestamp = time.time()
            data_with_metadata = {
                "patient_id": patient_id,
                "device_id": device_id,
                "device_type": self.registered_devices[device_id]["info"]["type"],
                "timestamp": timestamp,
                "vital_signs": vital_data
            }
            
            # Check for anomalies in vital signs
            anomalies = []
            if "heart_rate" in vital_data and (vital_data["heart_rate"] < 50 or vital_data["heart_rate"] > 120):
                anomalies.append("Abnormal heart rate detected")
            
            if "blood_pressure" in vital_data:
                try:
                    sys, dia = map(int, vital_data["blood_pressure"].split('/'))
                    if sys > 140 or dia > 90:
                        anomalies.append("High blood pressure detected")
                except:
                    pass
            
            if "oxygen_saturation" in vital_data and vital_data["oxygen_saturation"] < 92:
                anomalies.append("Low oxygen levels detected")
            
            # Store data in local registry (in real app, this would be on blockchain)
            if patient_id not in self.patient_data:
                self.patient_data[patient_id] = []
                
            self.patient_data[patient_id].append({
                "data": data_with_metadata,
                "verification": {
                    "anomalies": anomalies,
                    "alert_level": "normal" if not anomalies else "warning"
                }
            })
            
            # Determine appropriate response based on anomalies
            if anomalies:
                response_message = f"Medical Alert: {len(anomalies)} anomalies detected"
                response_status = "warning"
            else:
                response_message = "Medical Data Processed Successfully"
                response_status = "success"
                
            # Display the data processing response
            print_dapp_response(
                response_message,
                {
                    "patient_id": patient_id,
                    "device_id": device_id,
                    "anomalies": anomalies,
                    "alert_level": "normal" if not anomalies else "warning",
                    "timestamp": timestamp
                },
                response_status
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process IoT data: {e}")
            print_dapp_response(
                "Data Processing Failed", 
                {"error": str(e)},
                "error"
            )
            return False
    
    def get_patient_history(self, patient_id):
        """Retrieve patient data history"""
        if patient_id not in self.patient_data:
            print_dapp_response(
                "No Data Found", 
                {"patient_id": patient_id, "records": 0}
            )
            return []
        
        # Prepare the history
        history = []
        for entry in self.patient_data[patient_id]:
            history.append({
                "timestamp": entry["data"]["timestamp"],
                "device_id": entry["data"]["device_id"],
                "vital_signs": entry["data"]["vital_signs"],
                "anomalies": entry["verification"]["anomalies"],
                "alert_level": entry["verification"]["alert_level"]
            })
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        print_dapp_response(
            f"Patient History Retrieved: {len(history)} Records",
            {
                "patient_id": patient_id,
                "records": len(history),
                "history": history
            }
        )
        
        return history
    
    # Add the methods to the class
    HospitalIoTManagerDapp.receive_iot_data = receive_iot_data
    HospitalIoTManagerDapp.get_patient_history = get_patient_history
    
    return HospitalIoTManagerDapp

def main():
    """Run the Hospital IoT Manager dApp demo"""
    print("\n" + "=" * 80)
    print("🏥 HOSPITAL IoT MANAGER DAPP DEMO")
    print("=" * 80)
    print("This demo shows how the deployed Hospital IoT Manager dApp")
    print("behaves with blockchain interactions.")
    print("=" * 80 + "\n")
    
    # Add all methods to the dApp class
    HospitalIoTManagerDappExtended = add_device_methods(HospitalIoTManagerDapp)
    HospitalIoTManagerDappFinal = add_data_handling_methods(HospitalIoTManagerDappExtended)
    
    # Initialize the dApp
    hospital_dapp = HospitalIoTManagerDappFinal(hospital_id="Memorial-General-Hospital")
    
    # Step 1: Connect to blockchain and load agreement
    print("\n[Step 1] Setting up blockchain connection and agreement...")
    hospital_dapp.connect_to_blockchain()
    hospital_dapp.load_agreement()
    
    # Step 2: Create decentralized agent
    print("\n[Step 2] Creating decentralized agent...")
    hospital_dapp.create_decentralized_agent()
    
    # Step 3: Register IoT devices
    print("\n[Step 3] Registering medical IoT devices...")
    devices = [
        {"id": "ECG-Monitor-A1", "type": "ecg_monitor", "dept": "Cardiology"},
        {"id": "Vitals-Monitor-B2", "type": "vitals_monitor", "dept": "ICU"}
    ]
    
    for device in devices:
        hospital_dapp.register_iot_device(device["id"], device["type"], device["dept"])
    
    # Step 4: List registered devices
    print("\n[Step 4] Checking registered devices...")
    hospital_dapp.get_registered_devices()
    
    # Step 5: Simulate real-time data from IoT devices
    print("\n[Step 5] Processing real-time IoT data...")
    patients = [
        {"id": "PT-10042", "condition": "normal"},
        {"id": "PT-20931", "condition": "critical"}
    ]
    
    # Send normal vitals for first patient
    hospital_dapp.receive_iot_data(
        devices[0]["id"],
        patients[0]["id"],
        generate_vital_signs("normal")
    )
    
    # Send critical vitals for second patient
    hospital_dapp.receive_iot_data(
        devices[1]["id"],
        patients[1]["id"],
        generate_vital_signs("critical")
    )
    
    # Step 6: View patient history
    print("\n[Step 6] Retrieving patient history...")
    for patient in patients:
        hospital_dapp.get_patient_history(patient["id"])
    
    print("\n" + "=" * 80)
    print("🏥 HOSPITAL IoT MANAGER DAPP DEMO COMPLETED")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
