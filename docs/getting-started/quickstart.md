# MetaNode SDK Quick Start Guide

This guide will help you quickly get started with the MetaNode SDK to create and manage blockchain-based agreements.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for testnet access
- Basic understanding of blockchain concepts

## Installation

Install the MetaNode SDK using pip:

```bash
pip install metanode-sdk
```

Install the MetaNode CLI for command-line operations (optional):

```bash
pip install metanode-cli
```

## Basic Usage

### Initialize the SDK

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize with default settings (testnet)
sdk = MetaNodeSDK()

# Or with custom configuration
sdk = MetaNodeSDK(
    config_path="/path/to/config.yaml",  # Optional
    env="testnet",                        # Optional: testnet, production
    log_level="info"                      # Optional: debug, info, warning, error
)
```

### Connect to the Testnet

```python
# Connect to the MetaNode testnet
testnet = sdk.connect_to_testnet()

# Test the connection
connection_test = sdk.test_rpc_connection()
if connection_test["connected"]:
    print("Successfully connected to testnet!")
    print(f"Current block number: {connection_test['block_number']}")
else:
    print(f"Connection failed: {connection_test['error']}")
```

### Create a Simple Agreement

```python
# Create a basic agreement
agreement = sdk.create_agreement(
    name="sample-agreement",
    agreement_type="data_sharing",
    participants=[
        {"address": "0x123abc...", "role": "provider"},
        {"address": "0x456def...", "role": "consumer"}
    ],
    terms={
        "dataset_id": "dataset-123",
        "access_level": "read_only",
        "access_duration": 30  # days
    }
)

print(f"Agreement created with ID: {agreement['id']}")
```

### Validate an Agreement

```python
# Validate an agreement
validation = sdk.validate_agreement(
    agreement_id=agreement["id"],
    validation_options={
        "check_structure": True,
        "check_signatures": True
    }
)

if validation["valid"]:
    print("Agreement is valid")
else:
    print(f"Validation failed: {validation['reason']}")
```

### Sign and Finalize an Agreement

```python
# Sign the agreement
signature = sdk.sign_agreement(
    agreement_id=agreement["id"],
    signer_address="0x123abc..."
)

# Finalize the agreement
finalized = sdk.finalize_agreement(
    agreement_id=agreement["id"],
    deploy_on_chain=True
)

print(f"Agreement finalized: {finalized['status']}")
```

### Generate a Verification Proof

```python
# Generate a verification proof
proof = sdk.generate_verification_proof(
    agreement_id=agreement["id"],
    verification_type="chainlink.lock"
)

print(f"Verification proof generated: {proof['proof_id']}")
print(f"IPFS CID: {proof['ipfs_cid']}")
```

## Using the CLI

The MetaNode CLI provides command-line access to SDK functionality.

### Connect to Testnet

```bash
metanode-cli testnet connect
```

### Create an Agreement

```bash
metanode-cli agreement create \
  --name "sample-agreement" \
  --type data_sharing \
  --participants '[{"address":"0x123abc...","role":"provider"},{"address":"0x456def...","role":"consumer"}]' \
  --terms '{"dataset_id":"dataset-123","access_level":"read_only","access_duration":30}'
```

### Validate an Agreement

```bash
metanode-cli agreement validate --id AGR-123456
```

### Generate a Verification Proof

```bash
metanode-cli agreement generate-proof --id AGR-123456 --type chainlink.lock
```

## Next Steps

Now that you've completed the basic operations with the MetaNode SDK, you can explore these topics:

1. [Complete Workflow Tutorial](/docs/tutorials/01_complete_workflow.md) - Learn the complete agreement lifecycle
2. [Custom Agreements](/docs/agreements/03_custom_agreements.md) - Create agreements with custom schemas
3. [Testnet Connection Tutorial](/docs/tutorials/02_testnet_connection.md) - Set up and manage testnet connections
4. [Compliance and Auditing](/docs/agreements/05_compliance_auditing.md) - Implement compliance monitoring

For complete API details, refer to the [SDK Reference](/docs/sdk-reference/) documentation.

---

For any issues or questions, refer to the [Troubleshooting Guide](/docs/resources/troubleshooting.md) or contact support@metanode.example.com.
