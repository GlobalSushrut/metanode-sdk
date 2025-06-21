#!/bin/bash
# MetaNode Testnet Deployment Script for DigitalOcean
# Target: ubuntu-s-4vcpu-8gb-tor1-01 (159.203.17.36)

# Exit on error
set -e

echo "==============================================="
echo "MetaNode Testnet Kubernetes Deployment"
echo "==============================================="
echo

# Install MicroK8s
echo "Installing MicroK8s..."
apt update && apt upgrade -y
snap install microk8s --classic --channel=1.27

# Add user to microk8s group
echo "Configuring MicroK8s..."
usermod -a -G microk8s ubuntu
mkdir -p /home/ubuntu/.kube
chown -f -R ubuntu:ubuntu /home/ubuntu/.kube

# Wait for MicroK8s to start
echo "Waiting for MicroK8s to start..."
microk8s status --wait-ready

# Enable required addons
echo "Enabling MicroK8s addons..."
microk8s enable dns ingress storage metrics-server dashboard

# Configure kubectl
echo "Configuring kubectl..."
microk8s config > /home/ubuntu/.kube/config
chmod 600 /home/ubuntu/.kube/config
snap install kubectl --classic

# Create namespace and deploy components
echo "Deploying MetaNode testnet components..."
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/namespace.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/configmap.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/storage.yaml

# Build and push Docker images if they don't exist
echo "Building MetaNode Docker images..."
# Clone repository if needed
if [ ! -d "/home/ubuntu/metanode-sdk" ]; then
  git clone https://github.com/metanode/metanode-sdk.git /home/ubuntu/metanode-sdk
fi

cd /home/ubuntu/metanode-sdk

# Build Docker images
docker build -t metanode/core:latest -f docker/core/Dockerfile .
docker build -t metanode/validator:latest -f docker/validator/Dockerfile .
docker build -t metanode/api:latest -f docker/api/Dockerfile .

# Deploy core components
echo "Deploying core components..."
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/ipfs.yaml
echo "Waiting for IPFS to start..."
microk8s kubectl -n metanode wait --for=condition=available --timeout=60s deployment/ipfs

microk8s kubectl apply -f /home/ubuntu/metanode-k8s/blockchain-core.yaml
echo "Waiting for blockchain core to start..."
microk8s kubectl -n metanode wait --for=condition=available --timeout=60s deployment/blockchain-core

microk8s kubectl apply -f /home/ubuntu/metanode-k8s/validator.yaml
echo "Waiting for validator to start..."
microk8s kubectl -n metanode wait --for=condition=available --timeout=60s deployment/validator

# Deploy API and SDK server
echo "Deploying API and SDK server..."
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/api.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/sdk-server.yaml

# Set up ingress
echo "Setting up ingress..."
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/ingress.yaml

# Set up SDK content
echo "Setting up SDK download content..."
SDK_POD=$(microk8s kubectl -n metanode get pod -l app=sdk-server -o jsonpath='{.items[0].metadata.name}')
microk8s kubectl -n metanode cp /home/ubuntu/metanode-sdk/dist ${SDK_POD}:/usr/share/nginx/html/download

echo "==============================================="
echo "MetaNode Testnet Deployment Complete!"
echo "==============================================="
echo "Access the testnet API at: http://159.203.17.36/api"
echo "Download the SDK at: http://159.203.17.36/download"
echo "Access the IPFS gateway at: http://159.203.17.36/ipfs"
echo
echo "Use 'microk8s kubectl -n metanode get all' to see all resources"
echo "Use 'microk8s dashboard-proxy' to access the Kubernetes dashboard"
echo "==============================================="
