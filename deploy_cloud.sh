#!/bin/bash
# MetaNode Cloud Deployment Script

set -e

echo "==============================================="
echo "MetaNode Testnet Cloud Deployment"
echo "==============================================="

# Set variables
DROPLET_IP="159.203.17.36"
DROPLET_USER="root"
DROPLET_PASSWORD="Umesh3011@Adi"
LOCAL_DIR="/home/umesh/Videos/vKuber9/metanode-sdk"
REMOTE_DIR="/root/metanode-deployment"

# Check if sshpass is installed
if ! command -v sshpass &> /dev/null; then
    echo "Error: sshpass is required but not installed."
    echo "Install it with: sudo apt-get install sshpass"
    exit 1
fi

# Create temporary packaging directory
echo "Creating deployment package..."
PACKAGE_DIR="/tmp/metanode-deploy"
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

# Copy Kubernetes manifests
mkdir -p "$PACKAGE_DIR/metanode-k8s"
cp -r "$LOCAL_DIR/k8s-deployment"/*.yaml "$PACKAGE_DIR/metanode-k8s/"
cp -r "$LOCAL_DIR/k8s-deployment"/*.sh "$PACKAGE_DIR/metanode-k8s/"
cp "$LOCAL_DIR/k8s-deployment/README.md" "$PACKAGE_DIR/metanode-k8s/"

# Copy public HTML files
mkdir -p "$PACKAGE_DIR/metanode-k8s/public-html"
cp -r "$LOCAL_DIR/k8s-deployment/public-html"/* "$PACKAGE_DIR/metanode-k8s/public-html/"

# Copy Docker files
mkdir -p "$PACKAGE_DIR/metanode-sdk/docker/core"
mkdir -p "$PACKAGE_DIR/metanode-sdk/docker/validator"
mkdir -p "$PACKAGE_DIR/metanode-sdk/docker/api"
cp "$LOCAL_DIR/docker/core/Dockerfile" "$PACKAGE_DIR/metanode-sdk/docker/core/"
cp "$LOCAL_DIR/docker/validator/Dockerfile" "$PACKAGE_DIR/metanode-sdk/docker/validator/"
cp "$LOCAL_DIR/docker/api/Dockerfile" "$PACKAGE_DIR/metanode-sdk/docker/api/"

# Copy SDK source files (simulated as we don't have the actual files)
mkdir -p "$PACKAGE_DIR/metanode-sdk/src"
echo "# MetaNode SDK Source Files" > "$PACKAGE_DIR/metanode-sdk/setup.py"
echo "console_scripts = ['metanode-cli', 'metanode-wallet']" >> "$PACKAGE_DIR/metanode-sdk/setup.py"

# Create archive
cd /tmp
tar -czf metanode-deployment.tar.gz -C "$PACKAGE_DIR" .
echo "Deployment package created at: /tmp/metanode-deployment.tar.gz"

# Transfer files to DigitalOcean droplet
echo "==============================================="
echo "Transferring files to DigitalOcean droplet..."
echo "==============================================="

# Check if we can connect to the droplet
if ! sshpass -p "$DROPLET_PASSWORD" ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "$DROPLET_USER@$DROPLET_IP" exit; then
    echo "Error: Cannot connect to droplet. Please check your password and droplet status."
    exit 1
fi

# Transfer the deployment package
sshpass -p "$DROPLET_PASSWORD" scp -o StrictHostKeyChecking=accept-new /tmp/metanode-deployment.tar.gz "$DROPLET_USER@$DROPLET_IP:$REMOTE_DIR"

# SSH into the droplet and extract the package
echo "==============================================="
echo "Extracting package and starting deployment..."
echo "==============================================="
sshpass -p "$DROPLET_PASSWORD" ssh -o StrictHostKeyChecking=accept-new "$DROPLET_USER@$DROPLET_IP" << EOF
    cd "$REMOTE_DIR"
    echo "Extracting deployment package..."
    tar -xzf metanode-deployment.tar.gz
    
    echo "Setting execute permissions for scripts..."
    chmod +x "$REMOTE_DIR/metanode-k8s/"*.sh
    chmod +x "$REMOTE_DIR/metanode-sdk/docker/"*/*
    
    echo "Running deployment script..."
    "$REMOTE_DIR/metanode-k8s/deploy_public_testnet.sh"
EOF

echo "==============================================="
echo "MetaNode Testnet Deployment Complete!"
echo "==============================================="
echo "Access your testnet at: http://$DROPLET_IP/"
echo
echo "To test SDK installation:"
echo "  pip install metanode-sdk"
echo
echo "To verify deployment status, SSH to your droplet:"
echo "  sshpass -p <your-password> ssh $DROPLET_USER@$DROPLET_IP"
echo "  microk8s kubectl -n metanode get all"
echo "==============================================="
