# MetaNode SDK: Validator Module Reference

This document provides a comprehensive API reference for the Validator module within the MetaNode SDK.

## Table of Contents

- [Overview](#overview)
- [Core Classes](#core-classes)
- [Validator Operations](#validator-operations)
- [Agreement Validation](#agreement-validation)
- [Consensus Management](#consensus-management)
- [Runtime Proof Management](#runtime-proof-management)
- [vPod Integration](#vpod-integration)
- [CLI Integration](#cli-integration)
- [Error Handling](#error-handling)

## Overview

The Validator module provides tools for managing validation operations, including agreement validation, consensus verification, and runtime proof management. It integrates with MetaNode's blockchain infrastructure and vPod container technology to enable decentralized validation.

## Core Classes

### ValidatorManager

The primary class for validator operations.

```python
from metanode.blockchain import ValidatorManager

# Create a validator manager
validator_manager = ValidatorManager()

# Or access through the SDK
from metanode.full_sdk import MetaNodeSDK
sdk = MetaNodeSDK()
validator_manager = sdk.validator
```

### ConsensusVerifier

Class for verifying consensus operations.

```python
from metanode.blockchain import ConsensusVerifier

# Create a consensus verifier
consensus_verifier = ConsensusVerifier()

# Or access through the SDK
consensus_verifier = sdk.consensus_verifier
```

### ProofManager

Class for managing runtime verification proofs.

```python
from metanode.blockchain import ProofManager

# Create a proof manager
proof_manager = ProofManager()

# Or access through the SDK
proof_manager = sdk.proof_manager
```

## Validator Operations

### register_validator

Registers a new validator on the testnet.

```python
# Register a validator
registration = sdk.register_validator(
    node_identity={                       # Required: Node identity
        "address": "0x123abc...",
        "public_key": "0x456def..."
    },
    stake_amount=1000000000000000000,     # Optional: Stake amount in wei
    metadata={                            # Optional: Validator metadata
        "organization": "Example Org",
        "region": "us-east",
        "contact": "validator@example.com"
    },
    validator_config={                    # Optional: Validator configuration
        "consensus_role": "participant",  # Options: participant, leader
        "validation_types": ["agreement", "transaction", "proof"],
        "max_agreements": 500
    }
)

print(f"Validator registration: {registration['status']}")
print(f"Transaction hash: {registration['tx_hash']}")
print(f"Validator ID: {registration['validator_id']}")
```

### get_validator_list

Retrieves the list of active validators on the network.

```python
# Get validators
validators = sdk.get_validator_list(
    network_id="metanode-testnet",    # Optional: Network ID
    status="active",                  # Optional: Filter by status
    limit=20,                         # Optional: Pagination limit
    offset=0                          # Optional: Pagination offset
)

print(f"Total validators: {len(validators)}")
for validator in validators:
    print(f"Validator: {validator['address']}")
    print(f"  Status: {validator['status']}")
    print(f"  Blocks produced: {validator['blocks_produced']}")
    print(f"  Last active: {validator['last_active']}")
    print(f"  Performance score: {validator['performance_score']}")
```

### check_validator_status

Checks the status of a specific validator.

```python
# Check validator status
validator_status = sdk.check_validator_status(
    validator_address="0x123abc..."     # Required: Validator address
)

print(f"Validator status: {validator_status['status']}")
print(f"Currently active: {validator_status['active']}")
print(f"Last block produced: {validator_status['last_block']}")
print(f"Performance score: {validator_status['performance_score']}/100")
print(f"Agreements validated: {validator_status['agreements_validated']}")
print(f"Proofs generated: {validator_status['proofs_generated']}")
```

### update_validator_config

Updates the configuration of a validator.

```python
# Update validator configuration
update_result = sdk.update_validator_config(
    validator_address="0x123abc...",     # Required: Validator address
    config_updates={                     # Required: Configuration updates
        "consensus_role": "leader",
        "max_agreements": 1000,
        "validation_priority": "high"
    }
)

print(f"Configuration updated: {update_result['status']}")
print(f"Transaction hash: {update_result['tx_hash']}")
```

### deactivate_validator

Temporarily deactivates a validator.

```python
# Deactivate validator
deactivation = sdk.deactivate_validator(
    validator_address="0x123abc...",     # Required: Validator address
    reason="Maintenance",                # Optional: Deactivation reason
    duration_hours=24                    # Optional: Deactivation duration
)

print(f"Validator deactivated: {deactivation['status']}")
print(f"Will reactivate at: {deactivation['reactivation_time']}")
```

## Agreement Validation

### validate_agreement

Validates an agreement using the validator network.

```python
# Validate an agreement
validation_result = sdk.validate_agreement(
    agreement_id="agr-123",              # Required: Agreement ID
    validation_options={                 # Optional: Validation options
        "validator_count": 3,            # Number of validators to use
        "consensus_threshold": 2,        # Minimum validators in agreement
        "validation_level": "standard",  # Options: basic, standard, enhanced
        "validate_on_chain": True,       # Validate on blockchain
        "validation_timeout_seconds": 60 # Validation timeout
    }
)

if validation_result["valid"]:
    print("Agreement validation successful!")
    print(f"Validators used: {len(validation_result['validators'])}")
    print(f"Consensus achieved: {validation_result['consensus_achieved']}")
    print(f"Blockchain record: {validation_result['blockchain_record']}")
else:
    print(f"Validation failed: {validation_result['reason']}")
    for error in validation_result["validation_errors"]:
        print(f"- {error['message']}")
```

### register_validator_hook

Registers a hook to be called during the validation process.

```python
# Define a validator hook function
def custom_validation_hook(agreement, context):
    # Perform custom validation logic
    if "special_terms" not in agreement["terms"]:
        return {
            "valid": False,
            "reason": "Missing special terms",
            "severity": "error"
        }
    return {"valid": True}

# Register the hook
hook_id = sdk.register_validator_hook(
    hook_function=custom_validation_hook,    # Required: Hook function
    hook_name="special_terms_validator",     # Optional: Hook name
    description="Validates special terms",   # Optional: Description
    execution_phase="pre_consensus",         # Optional: When to execute
    applicable_types=["custom_agreement"]    # Optional: Agreement types
)

print(f"Validator hook registered with ID: {hook_id}")
```

### get_validation_report

Retrieves a detailed validation report for an agreement.

```python
# Get validation report
validation_report = sdk.get_validation_report(
    agreement_id="agr-123",              # Required: Agreement ID
    report_options={                     # Optional: Report options
        "include_validator_details": True,
        "include_execution_trace": True
    }
)

print(f"Validation report ID: {validation_report['report_id']}")
print(f"Overall result: {validation_report['result']}")
print(f"Validation timestamp: {validation_report['timestamp']}")
print(f"Validators participated: {len(validation_report['validators'])}")

# Process validator details
for validator in validation_report["validators"]:
    print(f"\nValidator: {validator['address']}")
    print(f"  Result: {validator['result']}")
    print(f"  Comments: {validator['comments']}")
```

## Consensus Management

### init_consensus_round

Initiates a new consensus round for agreement validation.

```python
# Initiate consensus round
consensus_round = sdk.init_consensus_round(
    agreement_id="agr-123",              # Required: Agreement ID
    consensus_options={                  # Optional: Consensus options
        "algorithm": "poa",              # Proof of Authority consensus
        "validator_count": 3,            # Number of validators
        "timeout_seconds": 60            # Timeout for consensus
    }
)

print(f"Consensus round initiated: {consensus_round['round_id']}")
print(f"Selected validators: {len(consensus_round['validators'])}")
```

### check_consensus_status

Checks the status of a consensus round.

```python
# Check consensus status
consensus_status = sdk.check_consensus_status(
    round_id=consensus_round["round_id"]  # Required: Consensus round ID
)

print(f"Consensus status: {consensus_status['status']}")
print(f"Votes received: {consensus_status['votes_received']}/{consensus_status['total_validators']}")
print(f"Consensus achieved: {consensus_status['consensus_achieved']}")
print(f"Results: {consensus_status['consensus_result']}")
```

### verify_consensus

Verifies that consensus was properly achieved.

```python
# Verify consensus
verification = sdk.verify_consensus(
    round_id=consensus_round["round_id"],  # Required: Consensus round ID
    verification_options={                 # Optional: Verification options
        "check_signatures": True,
        "check_blockchain_record": True
    }
)

if verification["verified"]:
    print("Consensus verification successful!")
    print(f"Blockchain transaction: {verification['blockchain_tx']}")
else:
    print(f"Consensus verification failed: {verification['reason']}")
```

## Runtime Proof Management

### generate_runtime_proof

Generates a runtime verification proof for an agreement or operation.

```python
# Generate a runtime proof
runtime_proof = sdk.generate_runtime_proof(
    proof_type="zkp",                   # Required: Proof type
    target_id="agr-123",                # Required: Target to prove
    target_type="agreement",            # Required: Type of target
    proof_parameters={                  # Optional: Proof parameters
        "include_state": True,
        "zk_protocol": "groth16",
        "witness_data": {"key": "value"}
    }
)

print(f"Runtime proof generated: {runtime_proof['proof_id']}")
print(f"Proof hash: {runtime_proof['proof_hash']}")
print(f"Blockchain record: {runtime_proof['blockchain_record']}")
```

### verify_runtime_proof

Verifies a runtime proof.

```python
# Verify a runtime proof
proof_verification = sdk.verify_runtime_proof(
    proof_id=runtime_proof["proof_id"],  # Required: Proof ID
    verification_options={               # Optional: Verification options
        "verify_on_chain": True,
        "check_witness_data": True
    }
)

if proof_verification["valid"]:
    print("Runtime proof is valid!")
    print(f"Verification timestamp: {proof_verification['timestamp']}")
else:
    print(f"Proof verification failed: {proof_verification['reason']}")
```

### list_proofs

Lists runtime proofs.

```python
# List proofs
proofs = sdk.list_proofs(
    target_type="agreement",            # Optional: Filter by target type
    target_id="agr-123",                # Optional: Filter by target ID
    proof_type="zkp",                   # Optional: Filter by proof type
    limit=10,                           # Optional: Pagination limit
    offset=0                            # Optional: Pagination offset
)

print(f"Found {len(proofs)} proofs")
for proof in proofs:
    print(f"Proof ID: {proof['id']}")
    print(f"Type: {proof['type']}")
    print(f"Created: {proof['created_at']}")
    print(f"Status: {proof['status']}")
    print("---")
```

## vPod Integration

### deploy_validator_vpod

Deploys a validator using vPod container technology.

```python
# Deploy a validator vPod
validator_pod = sdk.deploy_validator_vpod(
    node_identity={                      # Required: Node identity
        "address": "0x123abc...",
        "public_key": "0x456def..."
    },
    vpod_options={                       # Optional: vPod options
        "vpod_type": "validator",
        "resources": {
            "cpu": 2,
            "memory": "4Gi",
            "storage": "100Gi"
        },
        "deployment_target": "docker",   # Options: docker, kubernetes
        "enable_monitoring": True
    }
)

print(f"Validator vPod deployed: {validator_pod['vpod_id']}")
print(f"Status: {validator_pod['status']}")
print(f"Endpoint: {validator_pod['endpoint']}")
```

### check_vpod_status

Checks the status of a validator vPod.

```python
# Check vPod status
vpod_status = sdk.check_vpod_status(
    vpod_id=validator_pod["vpod_id"]    # Required: vPod ID
)

print(f"vPod status: {vpod_status['status']}")
print(f"Running: {vpod_status['running']}")
print(f"Uptime: {vpod_status['uptime_seconds']} seconds")
print(f"CPU usage: {vpod_status['resources']['cpu_usage']}%")
print(f"Memory usage: {vpod_status['resources']['memory_usage']}%")
print(f"Disk usage: {vpod_status['resources']['disk_usage']}%")
```

### manage_validator_vpod

Manages a validator vPod (start, stop, restart).

```python
# Manage vPod operations
operation_result = sdk.manage_validator_vpod(
    vpod_id=validator_pod["vpod_id"],    # Required: vPod ID
    operation="restart",                 # Required: Operation to perform
    options={                            # Optional: Operation options
        "force": False,
        "timeout_seconds": 30
    }
)

print(f"Operation {operation_result['operation']} completed: {operation_result['success']}")
print(f"New status: {operation_result['new_status']}")
```

## CLI Integration

The validator module integrates with the MetaNode CLI for validator operations.

### Command Line Usage

```bash
# Register a validator
metanode-cli validator register \
  --address 0x123abc... \
  --public-key 0x456def... \
  --metadata '{"organization":"Example Org"}'

# Check validator status
metanode-cli validator status --address 0x123abc...

# List validators
metanode-cli validator list --network metanode-testnet

# Deploy validator vPod
metanode-cli validator deploy-vpod \
  --address 0x123abc... \
  --vpod-type validator \
  --target docker
  
# Generate runtime proof
metanode-cli proof generate \
  --type zkp \
  --target agr-123 \
  --target-type agreement
  
# Verify runtime proof
metanode-cli proof verify --id prf-789
```

## Error Handling

The SDK uses a consistent error handling pattern for validator operations:

```python
from metanode.exceptions import (
    ValidatorError,
    ConsensusError,
    ProofGenerationError,
    ProofVerificationError,
    VPodDeploymentError
)

try:
    # SDK operations
    validation_result = sdk.validate_agreement("agr-123")
except ValidatorError as e:
    print(f"Validator error: {e.message}")
    print(f"Validator address: {e.validator_address}")
except ConsensusError as e:
    print(f"Consensus error: {e.message}")
    print(f"Round ID: {e.round_id}")
except ProofGenerationError as e:
    print(f"Proof generation error: {e.message}")
    print(f"Proof type: {e.proof_type}")
except ProofVerificationError as e:
    print(f"Proof verification error: {e.message}")
    print(f"Proof ID: {e.proof_id}")
except VPodDeploymentError as e:
    print(f"vPod deployment error: {e.message}")
    print(f"Deployment target: {e.deployment_target}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Conclusion

This reference covers the core functionality of the MetaNode SDK Validator module, which provides comprehensive tools for agreement validation, consensus verification, and runtime proof management. The module integrates with MetaNode's blockchain infrastructure and vPod container technology to enable secure and decentralized validation operations.

For more detailed information on specific use cases and workflow integration, refer to the tutorial documents:

- [Complete Workflow](/docs/tutorials/01_complete_workflow.md)
- [Testnet Connection](/docs/tutorials/02_testnet_connection.md)
- [Production Migration](/docs/tutorials/03_production_migration.md)
