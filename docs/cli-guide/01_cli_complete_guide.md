# MetaNode CLI: Complete User Guide

## Introduction

The MetaNode SDK Command Line Interface (CLI) provides developers with powerful tools to create, deploy, and manage decentralized applications with built-in blockchain integration. This guide offers comprehensive documentation on using the CLI to deploy any application with the MetaNode SDK.

## Installation

The MetaNode CLI comes installed with the MetaNode SDK. If you need to install or update it:

```bash
# Install the enhanced CLI
./install_enhanced_cli.sh

# Verify installation
metanode-cli --version
```

## CLI Architecture

The MetaNode CLI consists of several integrated components:

```
┌───────────────────────────────────────────┐
│             metanode-cli                  │
│         (Enhanced CLI Wrapper)            │
└───────────────────────────────────────────┘
                   │
                   ▼
┌───────────────────────────────────────────┐
│            metanode-cli-main              │
│     (Main CLI with core functionality)    │
└───────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌─────────────────┐    ┌─────────────────┐
│ metanode-cli-   │    │ metanode-cli-   │
│   agreement     │    │    testnet      │
└─────────────────┘    └─────────────────┘
```

## Getting Started

### First Steps

1. Check the CLI version:

```bash
metanode-cli --version
```

2. View available commands:

```bash
metanode-cli --help
```

## Application Lifecycle Management

### 1. Initialize a New Application

```bash
metanode-cli init my-dapp --network testnet --rpc http://159.203.17.36:8545
```

This command:
- Creates a new application directory structure
- Initializes configuration files
- Sets up testnet connection settings

The created project structure:

```
my-dapp/
├── metanode_config/           # Configuration directory
├── metanode_agreements/       # Agreement storage directory
├── src/                      # Application source code
├── metanode_config.json      # Main configuration file
└── README.md                 # Project documentation
```

### 2. Deploy Your Application

Once you've developed your application, deploy it to the MetaNode ecosystem:

```bash
metanode-cli deploy my-dapp --network testnet
```

This command:
- Sets up testnet connection
- Configures verification proofs
- Creates and deploys an agreement
- Connects your application to the MetaNode infrastructure

### 3. Check Application Status

Monitor your application's deployment status:

```bash
metanode-cli status my-dapp
```

This provides information about:
- Application deployment status
- Agreement status
- Testnet connection
- Verification proofs

## Testnet Management

The testnet module provides tools for connecting to and working with the MetaNode testnet.

### Test Connection

```bash
metanode-cli testnet my-dapp --test
```

### Setup Connection

```bash
metanode-cli testnet my-dapp --setup --rpc http://159.203.17.36:8545
```

### Create Node Cluster

Enhance decentralization by contributing to the testnet:

```bash
metanode-cli testnet my-dapp --create-cluster
```

### Setup Verification Proofs

Generate cryptographic proofs for trustless verification:

```bash
metanode-cli testnet my-dapp --setup-proofs
```

### Check Status

```bash
metanode-cli testnet my-dapp --status
```

## Agreement Management

Agreements in MetaNode are blockchain-based contracts that govern your application's execution.

### Create Agreement

```bash
metanode-cli agreement my-dapp --create --type standard
```

This generates a unique agreement with an ID. The agreement is stored in `my-dapp/metanode_agreements/`.

### Deploy Agreement

Deploy your agreement to the blockchain:

```bash
metanode-cli agreement my-dapp --deploy --id <agreement-id>
```

Replace `<agreement-id>` with the ID generated during agreement creation.

### Verify Agreement

Verify your agreement's blockchain status:

```bash
metanode-cli agreement my-dapp --verify --id <agreement-id>
```

### Check Agreement Status

```bash
metanode-cli agreement my-dapp --status [--id <agreement-id>]
```

If you omit the `--id` parameter, status for all agreements will be displayed.

## Node Cluster Management

Enhance testnet decentralization by creating and managing node clusters.

```bash
metanode-cli cluster my-dapp --create
```

## Complete Application Deployment Workflow

Below is a step-by-step guide to deploy a complete application with the MetaNode SDK CLI:

### Step 1: Initialize a new application

```bash
metanode-cli init my-decentralized-app --network testnet
```

### Step 2: Develop your application

Place your application code in the `src` directory. Here's a simple example:

```bash
mkdir -p my-decentralized-app/src
```

Create a simple application file:

```python
# my-decentralized-app/src/app.py
from metanode.full_sdk import MetaNodeSDK

def main():
    # Initialize the SDK
    sdk = MetaNodeSDK()
    
    # Connect to testnet
    sdk.connect_to_testnet(rpc_url="http://159.203.17.36:8545")
    
    # Create simple computation function
    def compute_function(data):
        return {"result": sum(data) / len(data) if data else 0}
    
    # Register computation
    computation_id = sdk.register_computation(
        function=compute_function,
        description="Simple average calculation"
    )
    
    print(f"Registered computation with ID: {computation_id}")
    return computation_id

if __name__ == "__main__":
    main()
```

### Step 3: Set up testnet connection

```bash
metanode-cli testnet my-decentralized-app --setup
```

### Step 4: Create and deploy an agreement

```bash
# Create agreement
metanode-cli agreement my-decentralized-app --create
# Note the agreement ID from the output
AGREEMENT_ID="<output-agreement-id>"

# Deploy agreement to blockchain
metanode-cli agreement my-decentralized-app --deploy --id $AGREEMENT_ID

# Verify agreement deployment
metanode-cli agreement my-decentralized-app --verify --id $AGREEMENT_ID
```

### Step 5: Set up verification proofs

```bash
metanode-cli testnet my-decentralized-app --setup-proofs
```

### Step 6: Deploy application

```bash
metanode-cli deploy my-decentralized-app
```

### Step 7: Check status

```bash
metanode-cli status my-decentralized-app
```

### Step 8: Create a node cluster (optional)

```bash
metanode-cli cluster my-decentralized-app --create
```

### Step 9: Monitor your application

```bash
# Check application status
metanode-cli status my-decentralized-app

# Check agreement status
metanode-cli agreement my-decentralized-app --status --id $AGREEMENT_ID

# Check testnet connection
metanode-cli testnet my-decentralized-app --status
```

## Deployment Examples

### Example 1: Data Analysis Application

```bash
# Initialize application
metanode-cli init data-analysis-app

# Setup testnet connection
metanode-cli testnet data-analysis-app --setup

# Create and deploy agreement
metanode-cli agreement data-analysis-app --create
# Save the agreement ID for later use
AGREEMENT_ID="<output-agreement-id>"
metanode-cli agreement data-analysis-app --deploy --id $AGREEMENT_ID

# Configure verification proofs
metanode-cli testnet data-analysis-app --setup-proofs

# Deploy the application
metanode-cli deploy data-analysis-app
```

### Example 2: Federated Learning Application with Secure Aggregation

```bash
# Initialize application
metanode-cli init federated-learning-app

# Setup testnet connection
metanode-cli testnet federated-learning-app --setup

# Create and deploy agreement
metanode-cli agreement federated-learning-app --create --type secure_computation
AGREEMENT_ID="<output-agreement-id>"
metanode-cli agreement federated-learning-app --deploy --id $AGREEMENT_ID

# Setup verification proofs
metanode-cli testnet federated-learning-app --setup-proofs

# Create node cluster for enhanced decentralization
metanode-cli cluster federated-learning-app --create

# Deploy the application
metanode-cli deploy federated-learning-app
```

## Integration with Python SDK

The CLI integrates seamlessly with the MetaNode Python SDK. You can use both together for a comprehensive development experience:

```python
# Example of using the SDK with deployed application
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Load agreement from CLI-deployed application
agreement_id = "your-agreement-id"  # From CLI output
app_path = "my-decentralized-app"

# Load agreement data
with open(f"{app_path}/metanode_agreements/agreement_{agreement_id}.json", "r") as f:
    agreement_data = json.load(f)

# Execute computation with the agreement
result = sdk.execute_computation_with_agreement(
    agreement_id=agreement_id,
    input_data=[1, 2, 3, 4, 5],
    verification_proofs=True
)

print(f"Computation result: {result}")
```

## Best Practices

### Application Structure

Organize your MetaNode application with the following structure for the best experience:

```
my-app/
├── metanode_config/
│   ├── testnet_connection.json
│   ├── testnet_cluster.json
│   └── verification_proofs/
│       └── chainlink.lock
├── metanode_agreements/
│   └── agreement_<id>.json
├── src/
│   ├── app.py          # Main application logic
│   └── models/         # Application-specific models
├── metanode_config.json
└── README.md
```

### Version Control

Track your application configuration:

```bash
# Recommended .gitignore entries
*.pyc
__pycache__/
*.swp
.env
```

### Deployment Checklist

Before deploying:
- Test testnet connection (`metanode-cli testnet app-path --test`)
- Verify agreement terms
- Ensure verification proofs are set up
- Check current testnet status

## Troubleshooting

### Connection Issues

If you encounter testnet connection problems:

```bash
# Verify RPC endpoint
metanode-cli testnet my-app --test --rpc http://159.203.17.36:8545

# Reconnect if needed
metanode-cli testnet my-app --setup --rpc http://159.203.17.36:8545
```

### Agreement Verification Failures

If agreement verification fails:

```bash
# Check agreement status
metanode-cli agreement my-app --status --id <agreement-id>

# Redeploy if needed
metanode-cli agreement my-app --deploy --id <agreement-id>
```

### Application Deployment Issues

For deployment problems:

```bash
# Check application status
metanode-cli status my-app

# Verify testnet connection
metanode-cli testnet my-app --status

# Redeploy application
metanode-cli deploy my-app
```

## CLI Reference

### Global Options

| Option | Description |
|--------|-------------|
| `--version` | Show CLI version |
| `--help` | Display help information |

### Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new MetaNode application |
| `deploy` | Deploy a MetaNode application |
| `status` | Check application status |
| `agreement` | Manage agreements |
| `testnet` | Manage testnet connections |
| `cluster` | Manage node clusters |

## Conclusion

The MetaNode SDK CLI provides a comprehensive set of tools for managing the entire lifecycle of decentralized applications. By following this guide, you can efficiently create, deploy, and manage applications with blockchain integration, verification proofs, and decentralized execution.

For more information, refer to other sections of the documentation:
- [Dapp Execution Overview](/docs/dapp-execution/01_dapp_execution_overview.md)
- [vPod Technology](/docs/dapp-execution/02_vpod_technology.md)
- [Execution Algorithms](/docs/dapp-execution/03_execution_algorithms.md)
- [Advanced Proof Generation](/docs/dapp-execution/04_advanced_proof_generation.md)
- [Agreement Integration](/docs/dapp-execution/05_agreement_integration.md)
