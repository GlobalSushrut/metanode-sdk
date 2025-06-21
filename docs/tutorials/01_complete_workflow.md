# MetaNode SDK: Complete Step-by-Step Workflow

This tutorial provides a comprehensive guide to using the MetaNode SDK, from installation to advanced operations.

## Table of Contents

1. [Installation](#1-installation)
2. [SDK Initialization](#2-sdk-initialization)
3. [Wallet Management](#3-wallet-management)
4. [Testnet Connectivity](#4-testnet-connectivity)
5. [Basic Agreement Creation](#5-basic-agreement-creation)
6. [Custom Agreement Development](#6-custom-agreement-development)
7. [Deploying Infrastructure](#7-deploying-infrastructure)
8. [Node Cluster Creation](#8-node-cluster-creation)
9. [Agreement Validation](#9-agreement-validation)
10. [Verification Proofs](#10-verification-proofs)
11. [Compliance Monitoring](#11-compliance-monitoring)
12. [Troubleshooting](#12-troubleshooting)

## 1. Installation

Start by installing the MetaNode SDK and CLI:

```bash
# Install the SDK via pip
pip install metanode-sdk

# Install the CLI tools
pip install metanode-cli

# Verify installation
metanode-cli --version
```

### Environment Setup

Configure your environment:

```bash
# Create directory for MetaNode configuration
mkdir -p ~/.metanode/config

# Generate initial configuration
metanode-cli init
```

## 2. SDK Initialization

Initialize the SDK in your Python code:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize with default settings
sdk = MetaNodeSDK()

# Or with custom configuration
sdk = MetaNodeSDK(
    config_path="/path/to/custom/config.yaml",
    env="testnet",  # Options: testnet, production
    log_level="info"
)

# Verify SDK connection
status = sdk.check_status()
print(f"SDK Status: {status['status']}")
print(f"Connected to network: {status['network']}")
print(f"API Version: {status['api_version']}")
```

## 3. Wallet Management

Create and manage wallets for blockchain interactions:

```python
# Create a new wallet
wallet = sdk.create_wallet(name="my-metanode-wallet")
print(f"Wallet created with address: {wallet.address}")

# Or use an existing wallet
wallet = sdk.get_wallet(name="my-metanode-wallet")

# List all available wallets
wallets = sdk.list_wallets()
for w in wallets:
    print(f"Wallet: {w.name}, Address: {w.address}")

# Set default wallet for transactions
sdk.set_default_wallet(wallet.name)
```

## 4. Testnet Connectivity

Connect to the MetaNode testnet:

```python
# Connect to testnet
testnet = sdk.connect_to_testnet()
print(f"Connected to testnet at {testnet.rpc_url}")

# Test connection
connection_status = sdk.test_rpc_connection()
if connection_status["connected"]:
    print("Successfully connected to testnet!")
    print(f"Current block number: {connection_status['block_number']}")
    print(f"Network ID: {connection_status['network_id']}")
else:
    print(f"Connection failed: {connection_status['error']}")
```

### Using CLI for Testnet Connection

```bash
# Connect to testnet via CLI
metanode-cli testnet connect

# Check testnet status
metanode-cli testnet status

# Get testnet information
metanode-cli testnet info
```

## 5. Basic Agreement Creation

Create a simple data sharing agreement:

```python
# Create a basic data sharing agreement
agreement = sdk.create_agreement(
    name="sample-data-sharing",
    agreement_type="data_sharing",
    participants=[
        {"address": wallet.address, "role": "provider"},
        {"address": "0x456def...", "role": "consumer"}
    ],
    terms={
        "dataset_id": "genomic-dataset-123",
        "access_level": "read_only",
        "access_duration": 30,  # days
        "allowed_operations": ["query", "analyze"],
        "anonymization_required": True
    },
    resource_limits={
        "max_queries_per_day": 1000,
        "max_concurrent_connections": 5
    }
)

# Get the agreement ID
agreement_id = agreement["id"]
print(f"Agreement created with ID: {agreement_id}")

# Load an existing agreement
existing_agreement = sdk.get_agreement(agreement_id)
```

### Using CLI for Agreement Creation

```bash
# Create agreement via CLI
metanode-cli agreement create \
  --type data_sharing \
  --name "sample-data-sharing" \
  --participant "provider:$MY_WALLET_ADDRESS" \
  --participant "consumer:0x456def..." \
  --term "dataset_id:genomic-dataset-123" \
  --term "access_level:read_only" \
  --term "access_duration:30" \
  --resource-limit "max_queries_per_day:1000"

# List agreements
metanode-cli agreement list
```

## 6. Custom Agreement Development

Develop a custom agreement with specialized terms:

```python
# Define a custom agreement schema
custom_schema = {
    "title": "Research Collaboration Agreement",
    "type": "object",
    "required": ["project_name", "researchers", "institutions"],
    "properties": {
        "project_name": {"type": "string"},
        "researchers": {
            "type": "array",
            "items": {"type": "string"}
        },
        "institutions": {
            "type": "array",
            "items": {"type": "string"}
        },
        "start_date": {"type": "string", "format": "date"},
        "end_date": {"type": "string", "format": "date"},
        "data_sharing_policy": {"type": "string"}
    }
}

# Register the custom schema
schema_id = sdk.register_agreement_schema(
    schema=custom_schema,
    schema_id="research_collaboration_v1"
)

# Create agreement with custom schema
custom_agreement = sdk.create_agreement(
    name="genomics-research-collaboration",
    schema_id=schema_id,
    participants=[
        {"address": wallet.address, "role": "lead_researcher"},
        {"address": "0x789ghi...", "role": "collaborator"}
    ],
    terms={
        "project_name": "Genomic Markers Analysis",
        "researchers": ["Dr. John Smith", "Dr. Jane Doe"],
        "institutions": ["Research Institute A", "University B"],
        "start_date": "2025-07-01",
        "end_date": "2026-06-30",
        "data_sharing_policy": "Anonymized data sharing permitted with attribution"
    }
)
```

## 7. Deploying Infrastructure

Deploy MetaNode infrastructure components:

```python
# Deploy a basic infrastructure setup
deployment = sdk.deploy_infrastructure(
    deployment_name="my-metanode-infra",
    components=["blockchain", "validator", "agreement", "ipfs"],
    deployment_options={
        "environment": "development",
        "container_technology": "docker",
        "resource_limits": {
            "cpu": 2,
            "memory": "4Gi",
            "storage": "100Gi"
        }
    }
)

print(f"Infrastructure deployment started: {deployment['deployment_id']}")

# Check deployment status
status = sdk.check_deployment_status(deployment["deployment_id"])
print(f"Deployment status: {status['status']}")
print(f"Components deployed: {', '.join(status['deployed_components'])}")
```

### Using CLI for Infrastructure Deployment

```bash
# Deploy infrastructure via CLI
metanode-cli infrastructure deploy \
  --name my-metanode-infra \
  --components blockchain,validator,agreement,ipfs \
  --environment development \
  --container-technology docker

# Check deployment status
metanode-cli infrastructure status --deployment-id <deployment_id>
```

## 8. Node Cluster Creation

Enhance testnet decentralization by creating a node cluster:

```python
# Generate node identities
node_identities = sdk.generate_node_identities(
    count=3,
    roles=["validator", "peer"]
)

# Create node configuration files
node_configs = sdk.create_node_configs(
    node_identities=node_identities,
    network_id="metanode-testnet"
)

# Deploy node cluster
cluster = sdk.deploy_node_cluster(
    cluster_name="my-validator-cluster",
    node_configs=node_configs,
    deployment_options={
        "infrastructure_id": deployment["deployment_id"],
        "connection_endpoints": ["http://159.203.17.36:8545"]
    }
)

print(f"Node cluster deployed: {cluster['cluster_id']}")

# Generate verification proof for the cluster
proof = sdk.generate_verification_proof(
    verification_type="chainlink.lock",
    target_id=cluster["cluster_id"],
    proof_parameters={"include_node_identities": True}
)
```

### Using CLI for Node Cluster Creation

```bash
# Create node cluster via CLI
metanode-cli node create-cluster \
  --name my-validator-cluster \
  --nodes 3 \
  --roles validator,peer \
  --connect-to http://159.203.17.36:8545

# Generate verification proof
metanode-cli node generate-proof \
  --cluster-id <cluster_id> \
  --type chainlink.lock
```

## 9. Agreement Validation

Validate and verify agreements:

```python
# Validate an agreement before finalization
validation_result = sdk.validate_agreement(
    agreement_id=agreement_id,
    validation_options={
        "check_structure": True,
        "check_permissions": True,
        "check_signatures": True,
        "verify_on_chain": True
    }
)

if validation_result["valid"]:
    print("Agreement validation successful!")
    
    # Finalize the agreement
    finalized = sdk.finalize_agreement(agreement_id)
    print(f"Agreement finalized: {finalized['status']}")
else:
    print(f"Validation failed: {validation_result['reason']}")
    for check, error in validation_result["validation_errors"].items():
        print(f"Error in {check}: {error['message']}")
```

### Using CLI for Agreement Validation

```bash
# Validate agreement via CLI
metanode-cli agreement validate \
  --id <agreement_id> \
  --checks structure,permissions,signatures,on-chain

# Finalize agreement
metanode-cli agreement finalize --id <agreement_id>
```

## 10. Verification Proofs

Create and verify cryptographic proofs:

```python
# Generate verification proof for an agreement
verification_proof = sdk.generate_verification_proof(
    agreement_id=agreement_id,
    verification_type="chainlink.lock",
    proof_parameters={
        "include_signatures": True,
        "include_terms": True,
        "hash_algorithm": "keccak256"
    }
)

print(f"Verification proof generated: {verification_proof['proof_id']}")
print(f"Verification URL: {verification_proof['verification_url']}")

# Validate a verification proof
validation_result = sdk.validate_verification_proof(
    proof_id=verification_proof['proof_id'],
    validation_options={
        "check_blockchain_record": True,
        "check_signatures": True
    }
)

if validation_result["valid"]:
    print("Proof is valid!")
    print(f"Recorded on blockchain at: {validation_result['blockchain_record']}")
else:
    print(f"Proof validation failed: {validation_result['reason']}")
```

## 11. Compliance Monitoring

Set up compliance monitoring for agreements:

```python
# Monitor agreement compliance
monitoring_handle = sdk.monitor_agreement_compliance(
    agreement_id=agreement_id,
    monitoring_options={
        "check_interval_seconds": 300,  # Check every 5 minutes
        "alert_on_violation": True,
        "monitored_conditions": [
            "access_permissions",
            "data_usage_limits",
            "participant_roles"
        ]
    }
)

# Set up compliance event handler
def on_compliance_violation(event):
    violation = event["violation"]
    print(f"Compliance violation detected at {event['timestamp']}")
    print(f"Condition violated: {violation['condition_name']}")
    print(f"Details: {violation['details']}")

# Register the event handler
monitoring_handle.on_violation(on_compliance_violation)

# Start monitoring
monitoring_handle.start()
```

### Generate Compliance Reports

```python
# Generate a compliance report
report = sdk.generate_compliance_report(
    agreement_id=agreement_id,
    report_format="pdf",
    time_range={
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-06-21T00:00:00Z"
    },
    include_sections=[
        "summary",
        "violations",
        "usage_statistics",
        "recommendations"
    ]
)

print(f"Compliance report generated: {report['report_id']}")
print(f"Report URL: {report['report_url']}")
```

## 12. Troubleshooting

Common issues and their solutions:

### Connection Issues

```python
# Test testnet connection
connection_status = sdk.test_rpc_connection()
if not connection_status["connected"]:
    # Try reconnecting
    sdk.reconnect_testnet()
    
    # Check specific components
    component_status = sdk.check_component_status(["blockchain", "validator"])
    print(f"Component status: {component_status}")
    
    # Get diagnostic information
    diagnostics = sdk.get_diagnostics()
    print(f"Diagnostics: {diagnostics}")
```

### Agreement Issues

```python
# Check agreement status
agreement_status = sdk.get_agreement_status(agreement_id)
print(f"Agreement status: {agreement_status['status']}")
print(f"Issues found: {len(agreement_status['issues'])}")

# Fix common issues
if agreement_status["issues"]:
    for issue in agreement_status["issues"]:
        print(f"Attempting to fix: {issue['description']}")
        fix_result = sdk.fix_agreement_issue(
            agreement_id=agreement_id,
            issue_id=issue["id"]
        )
        print(f"Fix result: {fix_result['result']}")
```

### CLI Diagnostic Tools

```bash
# Diagnose issues via CLI
metanode-cli diagnostics run

# Check logs
metanode-cli logs --component blockchain --lines 50

# Reset SDK configuration (if needed)
metanode-cli reset --confirm

# Repair infrastructure
metanode-cli infrastructure repair --deployment-id <deployment_id>
```

## Conclusion

This step-by-step guide covers the complete MetaNode SDK workflow. By following these steps, you can set up, deploy, and manage blockchain agreements with validation, compliance monitoring, and verification proofs.

For more detailed information about specific components, refer to the other documentation sections:

- [Agreement Overview](/docs/agreements/01_agreement_overview.md)
- [Agreement Types](/docs/agreements/02_agreement_types.md)
- [Custom Agreements](/docs/agreements/03_custom_agreements.md)
- [Agreement Validation](/docs/agreements/04_agreement_validation.md)
- [Compliance and Auditing](/docs/agreements/05_compliance_auditing.md)
- [Infrastructure Deployment](/docs/infrastructure/03_docker_deployment.md)
- [vPod Technology](/docs/infrastructure/04_vpod_technology.md)
- [Infrastructure Scaling](/docs/infrastructure/05_infrastructure_scaling.md)
- [High Availability](/docs/infrastructure/06_high_availability.md)
