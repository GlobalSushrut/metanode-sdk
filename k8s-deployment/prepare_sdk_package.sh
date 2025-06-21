#!/bin/bash
# MetaNode SDK Package Preparation Script
# This script creates downloadable SDK packages for public distribution

set -e

echo "==============================================="
echo "MetaNode SDK Package Preparation"
echo "==============================================="
echo

# Create directory structure
echo "Creating directory structure..."
mkdir -p dist/download/docs
mkdir -p dist/download/examples

# Package the SDK
echo "Creating SDK package..."
cd /home/ubuntu/metanode-sdk
python setup.py sdist bdist_wheel
cp dist/*.tar.gz dist/download/metanode-sdk-1.0.0-beta.tar.gz
cp dist/*.whl dist/download/metanode-sdk-1.0.0-beta-py3-none-any.whl

# Copy documentation
echo "Copying documentation..."
cp -r docs/* dist/download/docs/
cp README.md dist/download/docs/

# Create examples
echo "Packaging example applications..."

# Federated learning example
mkdir -p dist/download/examples/federated-learning
cat > dist/download/examples/federated-learning/run_federated_app.py << 'EOF'
#!/usr/bin/env python3
"""
MetaNode Federated Learning Example Application
This example demonstrates a simple federated averaging algorithm.
"""
import numpy as np
import json
import os
import sys

# Import MetaNode SDK helpers when available
try:
    from metanode.sdk.federated import FederatedModel, Client
except ImportError:
    print("MetaNode SDK not installed. Running in standalone mode.")

def create_dummy_data():
    """Create dummy data for federated learning demo"""
    # Create synthetic data
    x_train = np.random.rand(100, 10)
    y_train = np.random.randint(0, 2, size=(100, 1))
    return x_train, y_train

def train_local_model(x_train, y_train):
    """Simple linear model training"""
    # Simple implementation of linear model
    weights = np.zeros((10, 1))
    learning_rate = 0.01
    epochs = 5
    
    for _ in range(epochs):
        # Forward pass
        y_pred = np.dot(x_train, weights)
        
        # Calculate error
        error = y_pred - y_train
        
        # Update weights
        weights -= learning_rate * np.dot(x_train.T, error) / len(x_train)
        
    return weights

def main():
    print("Starting Federated Learning Example")
    print("===================================")

    # Check if running in MetaNode environment
    metanode_env = os.environ.get("METANODE_ENV", "standalone")
    
    if metanode_env == "standalone":
        # Simulate federated learning with 3 clients
        print("Running in standalone mode (simulation)")
        client_weights = []
        
        for i in range(3):
            print(f"Training client {i+1}...")
            x_train, y_train = create_dummy_data()
            weights = train_local_model(x_train, y_train)
            client_weights.append(weights)
            
        # Federated averaging
        global_weights = sum(client_weights) / len(client_weights)
        print("\nFederated averaging complete")
        print(f"Global model shape: {global_weights.shape}")
        print(f"Sample weights: {global_weights[:3].flatten()}")
        
    else:
        # Use MetaNode SDK for real federated learning
        print(f"Running in MetaNode environment: {metanode_env}")
        client = Client()
        model = FederatedModel()
        
        # Generate local data
        x_train, y_train = create_dummy_data()
        
        # Train local model
        local_weights = train_local_model(x_train, y_train)
        
        # Submit weights to federated computation
        print("Submitting local model to federated computation...")
        model.submit_weights(local_weights)
        
        # Wait for global model (normally async)
        global_weights = model.get_global_weights()
        print("Received global model")
        
    print("\nFederated Learning Example completed successfully!")

if __name__ == "__main__":
    main()
EOF

cat > dist/download/examples/federated-learning/config.json << 'EOF'
{
  "name": "simple-federated-learning",
  "algorithm": "federated-average",
  "resources": {
    "cpus": 1,
    "memory": "512Mi"
  },
  "code": {
    "main": "run_federated_app.py",
    "dependencies": ["numpy"]
  }
}
EOF

# Secure aggregation example
mkdir -p dist/download/examples/secure-aggregation
cat > dist/download/examples/secure-aggregation/run_secure_app.py << 'EOF'
#!/usr/bin/env python3
"""
MetaNode Secure Aggregation Example Application
This example demonstrates secure aggregation with zero-knowledge proofs.
"""
import numpy as np
import json
import os
import sys
import hashlib
import random

# Import MetaNode SDK helpers when available
try:
    from metanode.sdk.secure import SecureModel, ZkClient, SecretSharing
except ImportError:
    print("MetaNode SDK not installed. Running in standalone mode.")

def create_dummy_data():
    """Create dummy data for secure aggregation"""
    # Create synthetic data
    sensitive_data = np.random.rand(10) * 100
    return sensitive_data

def hash_value(value):
    """Simple hash function for simulation"""
    return hashlib.sha256(str(value).encode()).hexdigest()[:8]

def main():
    print("Starting Secure Aggregation Example")
    print("==================================")

    # Check if running in MetaNode environment
    metanode_env = os.environ.get("METANODE_ENV", "standalone")
    use_existing_vpod = os.environ.get("USE_EXISTING_VPOD", "true").lower() == "true"
    
    if metanode_env == "standalone":
        # Simulate secure aggregation with 3 clients
        print("Running in standalone mode (simulation)")
        client_data = []
        client_proofs = []
        
        for i in range(3):
            print(f"Processing client {i+1}...")
            data = create_dummy_data()
            # Create commitment (hash) of data for verification
            proof = hash_value(data.sum())
            
            # Add random noise for privacy
            noise = np.random.normal(0, 10, size=10)
            noisy_data = data + noise
            
            client_data.append(noisy_data)
            client_proofs.append(proof)
            
        # Secure aggregation
        aggregated_data = sum(client_data) / len(client_data)
        print("\nSecure aggregation complete")
        print(f"Aggregated data shape: {aggregated_data.shape}")
        print(f"Sample values: {aggregated_data[:3]}")
        print(f"Proof hashes: {client_proofs}")
        
    else:
        # Use MetaNode SDK for real secure aggregation
        print(f"Running in MetaNode environment: {metanode_env}")
        print(f"Using existing vPod containers: {use_existing_vpod}")
        
        client = ZkClient()
        model = SecureModel()
        
        # Generate local data
        data = create_dummy_data()
        
        # Create zero-knowledge proof of data
        print("Creating zero-knowledge proof...")
        proof = client.create_proof(data)
        
        # Submit data with proof
        print("Submitting data to secure aggregation...")
        model.submit_data(data, proof)
        
        # Wait for aggregated result (normally async)
        result = model.get_aggregated_result()
        print("Received securely aggregated result")
        
    print("\nSecure Aggregation Example completed successfully!")

if __name__ == "__main__":
    main()
EOF

cat > dist/download/examples/secure-aggregation/config.json << 'EOF'
{
  "name": "secure-aggregation-demo",
  "algorithm": "secure-aggregation",
  "resources": {
    "cpus": 1,
    "memory": "512Mi"
  },
  "code": {
    "main": "run_secure_app.py",
    "dependencies": ["numpy"]
  }
}
EOF

# Create a README for examples
cat > dist/download/examples/README.md << 'EOF'
# MetaNode SDK Examples

This directory contains example applications for the MetaNode SDK.

## Federated Learning Example

A simple example of federated learning using federated averaging algorithm.

```bash
cd federated-learning
metanode-cli deploy config.json
```

## Secure Aggregation Example

Privacy-preserving data aggregation with zero-knowledge proofs.

```bash
cd secure-aggregation
metanode-cli deploy config.json 
```

## Console-Only Mode

Both examples work in console-only mode without any UI dependencies.
The secure aggregation example is configured to use existing Docker vPod containers.

## Running Locally

You can run these examples locally before deploying:

```bash
# Federated learning example
cd federated-learning
python run_federated_app.py

# Secure aggregation example
cd secure-aggregation
python run_secure_app.py
```
EOF

# Create zip archives for easy download
echo "Creating downloadable archives..."
cd dist/download/examples
zip -r ../federated-learning.zip federated-learning
zip -r ../secure-aggregation.zip secure-aggregation
cd ../../..

# Copy web files
echo "Copying web files..."
cp -r /home/ubuntu/metanode-k8s/public-html/* dist/download/

echo "==============================================="
echo "Package preparation complete!"
echo "SDK packages ready for download at: dist/download/"
echo "==============================================="
