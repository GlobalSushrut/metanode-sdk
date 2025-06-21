# MetaNode CLI: Quick Reference

This document serves as a quick reference guide for the MetaNode SDK CLI commands. Use it as a cheat sheet when working with MetaNode applications.

## Common Commands

### Installation & Version

```bash
# Install enhanced CLI
./install_enhanced_cli.sh

# Check version
metanode-cli --version

# Get help
metanode-cli --help
```

### Application Lifecycle

```bash
# Initialize new application
metanode-cli init <app-name> --network testnet

# Deploy application
metanode-cli deploy <app-path> --network testnet

# Check application status
metanode-cli status <app-path>
```

### Testnet Management

```bash
# Test connection
metanode-cli testnet <app-path> --test

# Setup connection
metanode-cli testnet <app-path> --setup --rpc http://159.203.17.36:8545

# Setup verification proofs
metanode-cli testnet <app-path> --setup-proofs

# Check testnet status
metanode-cli testnet <app-path> --status
```

### Agreement Management

```bash
# Create agreement
metanode-cli agreement <app-path> --create --type standard
# Output includes agreement ID

# Deploy agreement
metanode-cli agreement <app-path> --deploy --id <agreement-id>

# Verify agreement
metanode-cli agreement <app-path> --verify --id <agreement-id>

# Check agreement status
metanode-cli agreement <app-path> --status --id <agreement-id>

# Check all agreements
metanode-cli agreement <app-path> --status
```

### Node Cluster Management

```bash
# Create node cluster
metanode-cli cluster <app-path> --create --rpc http://159.203.17.36:8545
```

## Command Options

### Initialize Options

```bash
metanode-cli init <app-name> [options]

Options:
  --network NETWORK    Network type (testnet/mainnet), default: testnet
  --rpc RPC           RPC URL, default: http://159.203.17.36:8545
```

### Deploy Options

```bash
metanode-cli deploy <app-path> [options]

Options:
  --network NETWORK    Network type (testnet/mainnet), default: testnet
  --rpc RPC           RPC URL, default: http://159.203.17.36:8545
```

### Agreement Options

```bash
metanode-cli agreement <app-path> [options]

Options:
  --create             Create a new agreement
  --deploy             Deploy an agreement
  --verify             Verify an agreement
  --status             Check agreement status
  --id ID              Agreement ID
  --type TYPE          Agreement type, default: standard
  --network NETWORK    Network type (testnet/mainnet), default: testnet
  --rpc RPC           RPC URL, default: http://159.203.17.36:8545
```

### Testnet Options

```bash
metanode-cli testnet <app-path> [options]

Options:
  --test               Test connection
  --setup              Set up connection
  --setup-proofs       Setup verification proofs
  --status             Check connection status
  --rpc RPC           RPC URL, default: http://159.203.17.36:8545
```

## Workflow Examples

### Basic Application Deployment

```bash
# Initialize application
metanode-cli init my-app

# Setup testnet connection
metanode-cli testnet my-app --setup

# Create agreement
metanode-cli agreement my-app --create
# Note the agreement ID from output

# Deploy agreement (replace with your agreement ID)
metanode-cli agreement my-app --deploy --id <agreement-id>

# Setup verification proofs
metanode-cli testnet my-app --setup-proofs

# Deploy application
metanode-cli deploy my-app

# Check status
metanode-cli status my-app
```

### Execution with Agreement

Use this pattern in your Python code to execute with an agreement:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Execute with agreement
result = sdk.execute_computation_with_agreement(
    agreement_id="<agreement-id>",
    computation_id="<computation-id>",
    input_data=[1, 2, 3, 4, 5],
    verification_proofs=True
)

print(result)
```

## Common Error Solutions

### Connection Errors

```bash
# Verify RPC endpoint
metanode-cli testnet my-app --test --rpc http://159.203.17.36:8545

# Reconnect
metanode-cli testnet my-app --setup --rpc http://159.203.17.36:8545
```

### Agreement Errors

```bash
# Check status
metanode-cli agreement my-app --status --id <agreement-id>

# Redeploy
metanode-cli agreement my-app --deploy --id <agreement-id>
```

### Application Errors

```bash
# Check status
metanode-cli status my-app

# Redeploy
metanode-cli deploy my-app
```

## Application Structure Reference

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
│   ├── app.py
├── metanode_config.json
└── README.md
```

## Environment Variables

```bash
# Agreement ID for application execution
export METANODE_AGREEMENT_ID=<agreement-id>
```

For complete documentation, refer to:
- [Complete CLI Guide](/docs/cli-guide/01_cli_complete_guide.md)
- [Practical Deployment Tutorial](/docs/cli-guide/02_practical_deployment_tutorial.md)
