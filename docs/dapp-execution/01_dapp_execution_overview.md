# Decentralized Application Execution

## Overview

The MetaNode SDK provides a comprehensive Web3 decentralized application (dapp) execution environment that allows developers to deploy and run applications in a trustless, verifiable manner. This document explains how the MetaNode SDK enables dapp execution in a Web3 environment using vPod technology.

## Key Concepts

### vPod Technology

vPods (Virtual Pods) are MetaNode's containerized execution environments that enable decentralized application deployment and execution:

- **Decentralized Execution**: Applications run in a trustless environment across distributed nodes
- **Blockchain Integration**: Direct connectivity to the MetaNode blockchain infrastructure
- **Verifiable Execution**: Cryptographic proofs of application execution and state
- **Resource Isolation**: Containerized environments with controlled resource allocation
- **Cross-Platform**: Support for Docker and Kubernetes deployment targets

### Web3 Execution Environment

The MetaNode SDK provides a full Web3 execution context:

- **Blockchain Connectivity**: Direct access to blockchain state and events
- **Decentralized Storage**: IPFS integration for content storage and retrieval
- **Identity Management**: Secure wallet and identity services
- **Consensus Verification**: Validation of distributed execution results
- **Zero-Knowledge Proofs**: Optional privacy-preserving computation validation

### Execution Flow

1. **Application Deployment**: Containerized applications are deployed as vPods
2. **Decentralized Execution**: vPods execute across the MetaNode network
3. **State Verification**: Execution results are validated through consensus
4. **Proof Generation**: Cryptographic proofs verify correct execution
5. **Blockchain Recording**: Execution results and proofs are recorded on-chain

## Implementation

### Deploying an Application

```python
from metanode.full_sdk import MetaNodeSDK

sdk = MetaNodeSDK()

# Deploy a decentralized application
app_deployment = sdk.deploy_dapp(
    name="my-decentralized-app",
    source_path="./app_directory",
    execution_options={
        "algorithm": "federated-average",  # or "secure-aggregation"
        "vpod_type": "compute",
        "compute_resources": {
            "cpu": 2,
            "memory": "4Gi",
            "gpu": 0
        },
        "blockchain_enabled": True,
        "consensus_participants": 3
    }
)

print(f"App deployed with ID: {app_deployment['dapp_id']}")
print(f"vPod instances: {app_deployment['vpod_count']}")
```

### Executing an Application

```python
# Execute the deployed application
execution = sdk.execute_dapp(
    dapp_id=app_deployment["dapp_id"],
    input_parameters={
        "dataset_uri": "ipfs://QmZ9...",
        "iterations": 100,
        "learning_rate": 0.01
    },
    execution_context={
        "generate_proof": True,
        "record_on_chain": True,
        "consensus_threshold": 2  # out of 3 participants
    }
)

print(f"Execution started with ID: {execution['execution_id']}")
```

### Monitoring Execution

```python
# Check execution status
status = sdk.check_dapp_execution(
    execution_id=execution["execution_id"]
)

print(f"Execution status: {status['status']}")
print(f"Progress: {status['progress']}%")
```

### Retrieving Results

```python
# Get execution results
results = sdk.get_dapp_results(
    execution_id=execution["execution_id"]
)

print(f"Execution completed: {results['completed']}")
print(f"Result hash: {results['result_hash']}")
print(f"IPFS URI: {results['ipfs_uri']}")
print(f"Blockchain transaction: {results['blockchain_tx']}")
```

### Verifying Execution Proof

```python
# Verify execution proof
verification = sdk.verify_execution_proof(
    proof_id=results["proof_id"]
)

if verification["verified"]:
    print("Execution proof verification successful!")
    print(f"Consensus: {verification['consensus_level']}%")
    print(f"Blockchain record: {verification['blockchain_record']}")
else:
    print(f"Proof verification failed: {verification['reason']}")
```

## CLI Integration

The MetaNode CLI provides command-line access to dapp execution functionality:

```bash
# Deploy a decentralized application
metanode-cli dapp deploy \
  --name my-decentralized-app \
  --source ./app_directory \
  --algorithm federated-average \
  --vpods 3 \
  --cpu 2 \
  --memory 4Gi

# Execute a deployed application
metanode-cli dapp execute \
  --id DAPP-123456 \
  --params '{"dataset_uri":"ipfs://QmZ9...","iterations":100}'

# Check execution status
metanode-cli dapp status --execution-id EXEC-123456

# Get execution results
metanode-cli dapp results --execution-id EXEC-123456

# Verify execution proof
metanode-cli proof verify --id PROOF-123456
```

## vPod Management

### Creating vPods Manually

```python
# Create vPods manually
vpods = sdk.create_vpods(
    count=3,
    vpod_type="compute",
    deployment_options={
        "deployment_method": "docker",  # or "kubernetes"
        "resource_limits": {
            "cpu_per_vpod": 2,
            "memory_per_vpod": "4Gi"
        },
        "environment_variables": {
            "BLOCKCHAIN_RPC": "http://159.203.17.36:8545",
            "IPFS_GATEWAY": "http://ipfs.metanode.example:8080"
        }
    }
)
```

### Managing vPod Lifecycle

```python
# Check vPod status
vpod_status = sdk.check_vpod_status(
    vpod_id=vpods[0]["vpod_id"]
)

# Start, stop, or restart vPod
operation_result = sdk.manage_vpod(
    vpod_id=vpods[0]["vpod_id"],
    operation="restart",
    force=False
)

# Get vPod logs
logs = sdk.get_vpod_logs(
    vpod_id=vpods[0]["vpod_id"],
    lines=100
)
```

## Algorithms and Execution Patterns

The MetaNode SDK currently supports two primary execution algorithms:

1. **Federated Average (federated-average)**
   - Distributed execution with aggregated results
   - Privacy-preserving model training
   - Result consensus through weighted averaging

2. **Secure Aggregation (secure-aggregation)**
   - Enhanced privacy protection
   - Cryptographically secure result aggregation
   - Zero-knowledge result verification

## Integration with Agreements

Dapp execution can be linked directly to agreement terms and conditions:

```python
# Create an agreement linked to dapp execution
agreement = sdk.create_agreement(
    name="dapp-execution-agreement",
    agreement_type="compute_execution",
    participants=[
        {"address": "0x123abc...", "role": "provider"},
        {"address": "0x456def...", "role": "consumer"}
    ],
    terms={
        "dapp_id": app_deployment["dapp_id"],
        "execution_parameters": {
            "max_executions": 100,
            "max_compute_resources": {
                "cpu_hours": 1000,
                "memory_gb_hours": 4000
            }
        }
    }
)

# Execute dapp based on agreement
execution = sdk.execute_dapp_from_agreement(
    agreement_id=agreement["id"],
    execution_parameters={
        "dataset_uri": "ipfs://QmZ9...",
        "iterations": 100
    }
)
```

## Best Practices

1. **Resource Allocation**
   - Allocate appropriate CPU, memory, and storage based on application needs
   - Over-allocation can lead to wasted resources, under-allocation to poor performance

2. **Error Handling**
   - Implement robust error handling in your dapp
   - Use the SDK's status monitoring to track execution issues

3. **Verification Strategy**
   - Choose appropriate consensus thresholds based on your trust requirements
   - Enable proof generation for critical applications

4. **Performance Optimization**
   - Design applications to work efficiently in distributed environments
   - Use appropriate data partitioning strategies

5. **Security Considerations**
   - Encrypt sensitive data before processing
   - Validate inputs and outputs
   - Control access to execution results using agreements

## Conclusion

The MetaNode SDK provides a comprehensive Web3 execution environment for decentralized applications through its vPod technology. By combining containerized execution with blockchain verification, it enables trustless, verifiable application execution with strong integration into the agreement lifecycle.

For more detailed information on specific aspects of dapp execution, refer to the following resources:

- [vPod Technology Reference](./02_vpod_technology.md)
- [Execution Algorithms](./03_execution_algorithms.md)
- [Advanced Proof Generation](./04_advanced_proof_generation.md)
- [Agreement Integration](./05_agreement_integration.md)
- [Complete Workflow Tutorial](../tutorials/01_complete_workflow.md)
