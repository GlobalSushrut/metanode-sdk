# Self-Hosted Infrastructure with MetaNode CLI

This guide explains how to deploy and manage your own infrastructure using the MetaNode CLI while connecting to the testnet for decentralization verification.

## Overview

MetaNode's architecture allows you to:

1. **Deploy your own infrastructure** on your servers/cloud
2. **Connect to the MetaNode testnet** to leverage decentralization
3. **Deploy node clusters** to enhance testnet contribution
4. **Maintain local control** while benefiting from decentralized verification

## Infrastructure Deployment Workflow

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│ 1. Deploy Local     │     │ 2. Create Node      │     │ 3. Connect to       │
│    Infrastructure   │────>│    Cluster          │────>│    Testnet          │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                                               │
┌─────────────────────┐     ┌─────────────────────┐           │
│ 5. Monitor & Manage │<────│ 4. Verify Connection│<──────────┘
│    Infrastructure   │     │    & Deploy App     │
└─────────────────────┘     └─────────────────────┘
```

## Prerequisites

Before starting:

- Ensure you have MetaNode SDK installed
- Have access to your own cloud or server infrastructure
- Have network connectivity to the testnet at `http://159.203.17.36:8545`

## Step 1: Deploy Local Infrastructure

First, initialize your MetaNode application:

```bash
metanode-cli init my-app --network testnet --rpc http://159.203.17.36:8545
```

This creates a basic application structure and configuration but does not yet deploy any local infrastructure.

## Step 2: Create Your Node Cluster

Before connecting to the testnet, deploy your local node cluster:

```bash
metanode-cli cluster my-app --create
```

This command:
- Creates a cluster configuration in `my-app/metanode_config/testnet_cluster.json`
- Defines three node types (light client, validator, sync) with specified ports
- Prepares configuration for local deployment

### Cluster Configuration Details

The generated configuration looks like:

```json
{
  "cluster_id": "abc123-unique-id",
  "created_at": "2025-06-21T09:35:00-04:00",
  "testnet_rpc": "http://159.203.17.36:8545",
  "testnet_ws": "ws://159.203.17.36:8546",
  "nodes": [
    {"id": "node1", "port": 6547, "role": "light_client", "peer_limit": 25},
    {"id": "node2", "port": 6548, "role": "validator", "peer_limit": 50},
    {"id": "node3", "port": 6549, "role": "sync", "peer_limit": 100}
  ],
  "status": "configured"
}
```

### Deploy the Cluster

After creating the configuration, deploy your node cluster on your infrastructure:

```bash
cd my-app
./enhance_testnet_decentralization.sh
```

> **Note:** If you don't have the enhancement script, you can create it based on your specific infrastructure requirements. The script should use the cluster configuration to deploy Docker containers or Kubernetes pods for the nodes.

## Step 3: Connect to the Testnet

After deploying your local infrastructure, connect it to the testnet:

```bash
metanode-cli testnet my-app --setup
```

This command:
- Configures your local infrastructure to connect to the testnet
- Sets up the RPC connection to `http://159.203.17.36:8545`
- Creates necessary connection configuration files

## Step 4: Verify Connection and Deploy Your Application

Verify that your local infrastructure is properly connected to the testnet:

```bash
metanode-cli testnet my-app --test
```

Set up verification proofs to ensure trustless execution:

```bash
metanode-cli testnet my-app --setup-proofs
```

Now deploy your application using your local infrastructure with testnet verification:

```bash
# Create and deploy an agreement
metanode-cli agreement my-app --create
# Note the agreement ID from output
AGREEMENT_ID="<output-agreement-id>"
metanode-cli agreement my-app --deploy --id $AGREEMENT_ID

# Deploy the application
metanode-cli deploy my-app
```

## Step 5: Monitor and Manage Your Infrastructure

Check the status of your local infrastructure and testnet connection:

```bash
# Check cluster status
metanode-cli testnet my-app --status

# Check application status
metanode-cli status my-app

# Check agreement status
metanode-cli agreement my-app --status --id $AGREEMENT_ID
```

## Advanced: Custom Infrastructure Deployment

For more advanced infrastructure needs, you can customize the node cluster deployment:

### Custom Ports and Configuration

Edit the `metanode_config/testnet_cluster.json` file to customize node configuration:

```json
{
  "nodes": [
    {"id": "custom-node1", "port": 8001, "role": "validator", "peer_limit": 100},
    {"id": "custom-node2", "port": 8002, "role": "validator", "peer_limit": 100}
  ]
}
```

### Integration with Kubernetes

Create a Kubernetes deployment script that uses the MetaNode cluster configuration:

```bash
#!/bin/bash
# Example kubernetes_deploy.sh

CLUSTER_CONFIG="./metanode_config/testnet_cluster.json"

# Read cluster config
CLUSTER_ID=$(jq -r '.cluster_id' $CLUSTER_CONFIG)

# Deploy nodes to Kubernetes
for node in $(jq -c '.nodes[]' $CLUSTER_CONFIG); do
  NODE_ID=$(echo $node | jq -r '.id')
  NODE_PORT=$(echo $node | jq -r '.port')
  NODE_ROLE=$(echo $node | jq -r '.role')
  
  # Create Kubernetes deployment
  cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metanode-$NODE_ID
spec:
  replicas: 1
  selector:
    matchLabels:
      app: metanode
      node: $NODE_ID
  template:
    metadata:
      labels:
        app: metanode
        node: $NODE_ID
    spec:
      containers:
      - name: metanode
        image: metanode/node:latest
        args: ["--role", "$NODE_ROLE", "--testnet", "http://159.203.17.36:8545"]
        ports:
        - containerPort: $NODE_PORT
---
apiVersion: v1
kind: Service
metadata:
  name: metanode-$NODE_ID
spec:
  selector:
    app: metanode
    node: $NODE_ID
  ports:
  - port: $NODE_PORT
    targetPort: $NODE_PORT
EOF

done

echo "Deployed MetaNode cluster $CLUSTER_ID to Kubernetes"
```

## Docker Compose Integration

For Docker-based deployments, create a Docker Compose file from your cluster configuration:

```bash
#!/bin/bash
# Example docker_deploy.sh

CLUSTER_CONFIG="./metanode_config/testnet_cluster.json"
DOCKER_COMPOSE="./docker-compose.yml"

# Create docker-compose.yml header
cat > $DOCKER_COMPOSE <<EOF
version: '3'
services:
EOF

# Add each node as a service
for node in $(jq -c '.nodes[]' $CLUSTER_CONFIG); do
  NODE_ID=$(echo $node | jq -r '.id')
  NODE_PORT=$(echo $node | jq -r '.port')
  NODE_ROLE=$(echo $node | jq -r '.role')
  
  cat >> $DOCKER_COMPOSE <<EOF
  $NODE_ID:
    image: metanode/node:latest
    command: --role $NODE_ROLE --testnet http://159.203.17.36:8545
    ports:
      - "$NODE_PORT:$NODE_PORT"
    volumes:
      - ./metanode_data/$NODE_ID:/data
    restart: unless-stopped
EOF
done

echo "Created Docker Compose configuration for MetaNode cluster"
echo "To deploy: docker compose -f $DOCKER_COMPOSE up -d"
```

## Benefits of Self-Hosted Infrastructure

- **Control**: Maintain full control over your infrastructure while benefiting from decentralization
- **Security**: Keep sensitive computations within your own environment
- **Compliance**: Meet regulatory requirements by keeping data within your boundaries
- **Decentralization**: Contribute to and benefit from network decentralization
- **Verification**: Leverage testnet for trustless verification of execution

## Troubleshooting

### Infrastructure Deployment Issues

If your local infrastructure deployment fails:

```bash
# Check cluster configuration
cat my-app/metanode_config/testnet_cluster.json

# Verify enhancement script execution permissions
chmod +x ./enhance_testnet_decentralization.sh
```

### Testnet Connection Issues

If you have trouble connecting to the testnet:

```bash
# Test connection explicitly
metanode-cli testnet my-app --test --rpc http://159.203.17.36:8545

# Check your firewall settings to ensure ports 8545 and 8546 are accessible
```

### Application Deployment Issues

If application deployment fails:

```bash
# Check application status
metanode-cli status my-app

# Verify local infrastructure is running
# (Docker command example - your specific command may differ)
docker ps | grep metanode
```

## Conclusion

By following this guide, you've learned how to:
1. Deploy your own infrastructure on your servers or cloud
2. Create a node cluster for local deployment
3. Connect your infrastructure to the MetaNode testnet
4. Deploy and verify applications using your infrastructure
5. Monitor and manage your local infrastructure

This approach gives you the best of both worlds: full control over your infrastructure while leveraging the decentralization and verification benefits of the MetaNode testnet.
