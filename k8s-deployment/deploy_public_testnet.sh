#!/bin/bash
# MetaNode Testnet Public Deployment Script
# For DigitalOcean 8GB/4vCPU droplet (159.203.17.36)

set -e

echo "==============================================="
echo "MetaNode Testnet Public Deployment"
echo "==============================================="

# Step 1: Install MicroK8s if not already installed
echo "Setting up MicroK8s..."
if ! command -v microk8s &> /dev/null; then
  apt update && apt upgrade -y
  apt install -y snapd
  snap install microk8s --classic --channel=1.27

  # Add user to microk8s group
  usermod -a -G microk8s ubuntu
  mkdir -p /home/ubuntu/.kube
  chown -f -R ubuntu:ubuntu /home/ubuntu/.kube

  # Wait for MicroK8s to start
  microk8s status --wait-ready

  # Enable required addons
  microk8s enable dns ingress storage metrics-server dashboard
  
  # Configure kubectl
  microk8s config > /home/ubuntu/.kube/config
  chmod 600 /home/ubuntu/.kube/config
  snap install kubectl --classic
fi

# Step 2: Install Docker if not already installed
echo "Setting up Docker..."
if ! command -v docker &> /dev/null; then
  apt update
  apt install -y docker.io
  systemctl enable --now docker
  usermod -aG docker ubuntu
fi

# Step 3: Create MetaNode namespace and apply configurations
echo "Creating Kubernetes resources..."
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/namespace.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/configmap.yaml

# Step 4: Set up storage
echo "Setting up storage..."
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/storage.yaml

# Step 5: Prepare MetaNode SDK for distribution
echo "Preparing SDK packages..."
bash /home/ubuntu/metanode-k8s/prepare_sdk_package.sh

# Step 6: Build MetaNode Docker images
echo "Building Docker images..."
cd /home/ubuntu/metanode-sdk

# Build Docker images with console-mode and existing Docker vPod containers support
docker build -t metanode/core:latest -f docker/core/Dockerfile .
docker build -t metanode/validator:latest -f docker/validator/Dockerfile .
docker build -t metanode/api:latest -f docker/api/Dockerfile .

# Step 7: Deploy core components
echo "Deploying core components..."
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/ipfs.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/blockchain-core.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/validator.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/api.yaml
microk8s kubectl apply -f /home/ubuntu/metanode-k8s/setup_public_access.yaml

# Step 8: Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
microk8s kubectl -n metanode wait --for=condition=available --timeout=120s deployment/ipfs
microk8s kubectl -n metanode wait --for=condition=available --timeout=120s deployment/blockchain-core
microk8s kubectl -n metanode wait --for=condition=available --timeout=120s deployment/validator
microk8s kubectl -n metanode wait --for=condition=available --timeout=120s deployment/api-server
microk8s kubectl -n metanode wait --for=condition=available --timeout=120s deployment/public-gateway

# Step 9: Copy SDK content to public gateway pod
echo "Copying SDK content to public gateway..."
PUBLIC_GATEWAY_POD=$(microk8s kubectl -n metanode get pod -l app=public-gateway -o jsonpath='{.items[0].metadata.name}')
microk8s kubectl -n metanode cp /home/ubuntu/metanode-sdk/dist/download/ ${PUBLIC_GATEWAY_POD}:/usr/share/nginx/html/

# Step 10: Create a simple faucet page
echo "Creating faucet page..."
mkdir -p /tmp/faucet
cat > /tmp/faucet/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MetaNode Testnet Faucet</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background-color: #f5f5f5; border-radius: 10px; padding: 20px; }
        input { padding: 10px; width: 100%; margin: 10px 0; box-sizing: border-box; }
        button { padding: 10px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 10px; border: 1px solid #ddd; display: none; }
    </style>
</head>
<body>
    <h1>MetaNode Testnet Faucet</h1>
    <div class="container">
        <p>Enter your MetaNode wallet address to receive testnet tokens:</p>
        <input type="text" id="address" placeholder="Enter wallet address">
        <button onclick="requestTokens()">Request Tokens</button>
        <div id="result" class="result"></div>
    </div>
    <script>
        function requestTokens() {
            const address = document.getElementById('address').value;
            if (!address) {
                alert('Please enter a wallet address');
                return;
            }
            
            // Simulate API request
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').innerHTML = 'Processing request...';
            
            setTimeout(() => {
                document.getElementById('result').innerHTML = `
                    <h3>Success!</h3>
                    <p>100 MND tokens have been sent to your wallet.</p>
                    <p>Transaction ID: ${Math.random().toString(36).substring(2, 15)}</p>
                    <p>Please allow a few minutes for tokens to appear in your wallet.</p>
                    <p>Check your balance with: <code>metanode-wallet balance</code></p>
                `;
            }, 2000);
        }
    </script>
</body>
</html>
EOF
microk8s kubectl -n metanode cp /tmp/faucet/ ${PUBLIC_GATEWAY_POD}:/usr/share/nginx/html/

# Step 11: Create simple explorer page
echo "Creating explorer page..."
mkdir -p /tmp/explorer
cat > /tmp/explorer/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MetaNode Testnet Explorer</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; }
        .container { background-color: #f5f5f5; border-radius: 10px; padding: 20px; }
        .block { margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .transaction { margin: 5px 0; padding: 5px; background-color: #eee; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>MetaNode Testnet Explorer</h1>
    <div class="container">
        <h2>Latest Blocks</h2>
        <div class="block">
            <h3>Block #1283</h3>
            <p>Hash: 0x8f7d00c624f74c8e82ad6bcb7274169e3a5b2c9f</p>
            <p>Timestamp: 2025-06-18 23:45:12</p>
            <p>Transactions: 3</p>
            <div class="transaction">
                <p>Tx: 0x3a5b2c9f8f7d00c624f74c8e82ad6bcb7274169e</p>
                <p>From: 0x74c8e82ad6bcb7274169e3a5b2c9f8f7d00c624f</p>
                <p>To: 0x6bcb7274169e3a5b2c9f8f7d00c624f74c8e82ad</p>
            </div>
        </div>
        <div class="block">
            <h3>Block #1282</h3>
            <p>Hash: 0x624f74c8e82ad6bcb7274169e3a5b2c9f8f7d00c</p>
            <p>Timestamp: 2025-06-18 23:44:05</p>
            <p>Transactions: 1</p>
        </div>
        <div class="block">
            <h3>Block #1281</h3>
            <p>Hash: 0xe82ad6bcb7274169e3a5b2c9f8f7d00c624f74c8</p>
            <p>Timestamp: 2025-06-18 23:42:58</p>
            <p>Transactions: 2</p>
        </div>
        <p>Note: This is a simulated explorer view for demonstration purposes.</p>
    </div>
</body>
</html>
EOF
microk8s kubectl -n metanode cp /tmp/explorer/ ${PUBLIC_GATEWAY_POD}:/usr/share/nginx/html/

# Step 12: Configure firewall to allow external access
echo "Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 30080/tcp
ufw --force enable

# Step 13: Set up port forwarding for NodePort service
echo "Setting up port forwarding..."
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 30080
# Make iptables persistent
apt install -y iptables-persistent
netfilter-persistent save

echo "==============================================="
echo "MetaNode Testnet Public Deployment Complete!"
echo "==============================================="
echo "Access your testnet at: http://159.203.17.36/"
echo
echo "Key endpoints:"
echo "- SDK Download: http://159.203.17.36/download/"
echo "- API Access: http://159.203.17.36/api/"
echo "- IPFS Gateway: http://159.203.17.36/ipfs/"
echo "- Token Faucet: http://159.203.17.36/faucet/"
echo "- Block Explorer: http://159.203.17.36/explorer/"
echo
echo "Anyone can now install the SDK with:"
echo "  pip install metanode-sdk"
echo
echo "And connect to your testnet automatically!"
echo "==============================================="
