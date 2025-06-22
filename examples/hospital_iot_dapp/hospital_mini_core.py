#!/usr/bin/env python3
"""
Hospital IoT Manager dApp Core Utilities
"""

import logging
import json
import uuid
import time
import sys
import os
import random
import hashlib
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("hospital-iot-demo")

def print_dapp_response(message, data=None, status="success"):
    """Format and print a simulated dApp response"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    response = {
        "timestamp": timestamp,
        "status": status,
        "message": message
    }
    
    if data:
        response["data"] = data
        
    print("\n" + "=" * 80)
    print(f"🏥 HOSPITAL IoT MANAGER RESPONSE")
    print("=" * 80)
    print(json.dumps(response, indent=2))
    print("=" * 80 + "\n")
    
    return response

def simulate_blockchain_transaction():
    """Simulate a blockchain transaction and return a transaction hash"""
    # Generate a random transaction hash
    random_data = str(random.random()).encode() + str(time.time()).encode()
    tx_hash = "0x" + hashlib.sha256(random_data).hexdigest()
    
    return {
        "tx_hash": tx_hash,
        "block_number": random.randint(9500000, 9600000),
        "gas_used": random.randint(21000, 100000),
        "status": "confirmed"
    }

def generate_vital_signs(patient_condition="normal"):
    """Generate realistic vital signs based on patient condition"""
    if patient_condition == "normal":
        return {
            "heart_rate": random.randint(60, 100),
            "blood_pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}",
            "temperature": round(random.uniform(97.8, 99.1), 1),
            "respiratory_rate": random.randint(12, 20),
            "oxygen_saturation": random.randint(95, 100)
        }
    elif patient_condition == "critical":
        return {
            "heart_rate": random.randint(110, 150),
            "blood_pressure": f"{random.randint(140, 180)}/{random.randint(90, 110)}",
            "temperature": round(random.uniform(99.5, 103.0), 1),
            "respiratory_rate": random.randint(25, 35),
            "oxygen_saturation": random.randint(85, 91)
        }
    else:  # random condition
        return {
            "heart_rate": random.randint(55, 150),
            "blood_pressure": f"{random.randint(100, 180)}/{random.randint(60, 110)}",
            "temperature": round(random.uniform(97.0, 103.0), 1),
            "respiratory_rate": random.randint(10, 35),
            "oxygen_saturation": random.randint(85, 100)
        }
