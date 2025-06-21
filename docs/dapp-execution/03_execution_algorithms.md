# Execution Algorithms

## Overview

The MetaNode SDK supports multiple execution algorithms for distributed application processing in a Web3 environment. This document provides a comprehensive explanation of the supported algorithms, their benefits, implementation details, and use cases.

## Supported Algorithms

The MetaNode SDK currently implements two primary execution algorithms:

1. **Federated Average (federated-average)**
2. **Secure Aggregation (secure-aggregation)**

Each algorithm offers different tradeoffs between performance, privacy, security, and computational efficiency.

## Federated Average

### Core Concept

Federated Average is a distributed computation algorithm that enables collaborative model training and data processing without sharing raw data. It works by:

1. Distributing computation across multiple vPods
2. Each vPod performing local computation on its data partition
3. Aggregating results using a weighted averaging mechanism
4. Generating a consensus result with blockchain verification

### Implementation

```python
from metanode.full_sdk import MetaNodeSDK

sdk = MetaNodeSDK()

# Deploy a federated average computation
federated_deployment = sdk.deploy_dapp(
    name="federated-model-training",
    source_path="./ml_model",
    execution_options={
        "algorithm": "federated-average",
        "vpod_count": 5,
        "aggregation_method": "weighted_average",
        "convergence_threshold": 0.001,
        "max_rounds": 100
    }
)

# Execute the federated computation
execution = sdk.execute_dapp(
    dapp_id=federated_deployment["dapp_id"],
    input_parameters={
        "dataset_partitions": [
            "ipfs://Qm123...",
            "ipfs://Qm456...",
            "ipfs://Qm789..."
        ],
        "learning_rate": 0.01,
        "batch_size": 32
    }
)
```

### Workflow

1. **Initialization Phase**
   - Global parameters are distributed to all participating vPods
   - Data partitions are assigned to each vPod
   - Initial model state is established

2. **Local Computation Phase**
   - Each vPod independently processes its data partition
   - Local updates are computed
   - Results are prepared for aggregation

3. **Aggregation Phase**
   - Local results are collected from all vPods
   - Weighted averaging is applied based on data contribution
   - Global model is updated

4. **Verification Phase**
   - Results consensus is verified
   - Cryptographic proofs are generated
   - Results are recorded on blockchain

5. **Iteration Phase**
   - Process repeats until convergence or max rounds reached

### CLI Integration

```bash
# Deploy a federated average computation
metanode-cli dapp deploy \
  --name federated-model-training \
  --source ./ml_model \
  --algorithm federated-average \
  --vpods 5

# Execute the computation
metanode-cli dapp execute \
  --id DAPP-123456 \
  --params '{"dataset_partitions":["ipfs://Qm123..."], "learning_rate":0.01}'
```

### Use Cases

- **Collaborative Machine Learning**: Train models across multiple organizations without sharing raw data
- **Distributed Analytics**: Perform analytics on partitioned datasets
- **Privacy-Preserving Computations**: Process sensitive data while keeping it local

### Benefits

- Preserves data privacy by keeping raw data within each vPod
- Reduces network bandwidth requirements
- Enables collaboration among multiple parties
- Provides auditability through blockchain verification

## Secure Aggregation

### Core Concept

Secure Aggregation enhances the Federated Average algorithm with advanced cryptographic protections that ensure even the intermediate results remain encrypted. It provides:

1. End-to-end encryption of model updates
2. Threshold cryptography for aggregation
3. Zero-knowledge validation of computation
4. Cryptographic guarantees of privacy and correctness

### Implementation

```python
from metanode.full_sdk import MetaNodeSDK

sdk = MetaNodeSDK()

# Deploy a secure aggregation computation
secure_deployment = sdk.deploy_dapp(
    name="secure-data-analysis",
    source_path="./analysis_model",
    execution_options={
        "algorithm": "secure-aggregation",
        "vpod_count": 3,
        "security_threshold": 2,  # t-of-n threshold
        "encryption_scheme": "threshold_paillier",
        "zero_knowledge_proofs": True
    }
)

# Execute secure computation
execution = sdk.execute_dapp(
    dapp_id=secure_deployment["dapp_id"],
    input_parameters={
        "encrypted_data_sources": [
            "ipfs://QmSec1...",
            "ipfs://QmSec2...",
            "ipfs://QmSec3..."
        ],
        "analysis_parameters": {
            "confidence_interval": 0.95,
            "iterations": 500
        }
    },
    security_options={
        "threshold_signatures": True,
        "generate_zkp": True
    }
)
```

### Workflow

1. **Setup Phase**
   - Cryptographic key generation and distribution
   - Threshold encryption scheme initialization
   - Zero-knowledge proving system setup

2. **Encryption Phase**
   - Input data and parameters are encrypted
   - Homomorphic encryption enables computation on encrypted data
   - Secure shares are distributed among participants

3. **Computation Phase**
   - vPods perform computation on encrypted data
   - Operations use homomorphic properties to maintain encryption
   - Zero-knowledge proofs are generated for verification

4. **Secure Aggregation Phase**
   - Encrypted results are combined using threshold cryptography
   - No single party can view intermediate results
   - Final result is cooperatively decrypted

5. **Verification Phase**
   - Zero-knowledge proofs verify correct execution
   - Verification results are recorded on blockchain
   - Chainlink.lock proofs are generated for the entire process

### CLI Integration

```bash
# Deploy a secure aggregation computation
metanode-cli dapp deploy \
  --name secure-data-analysis \
  --source ./analysis_model \
  --algorithm secure-aggregation \
  --vpods 3 \
  --threshold 2 \
  --zkp true

# Execute with secure parameters
metanode-cli dapp execute \
  --id DAPP-123456 \
  --secure-params '{"encrypted_data_sources":["ipfs://QmSec1..."]}'
```

### Use Cases

- **Financial Data Analysis**: Process sensitive financial information across institutions
- **Healthcare Research**: Analyze patient data while maintaining strict privacy
- **Secure Multi-Party Computation**: Enable mutually distrusting parties to collaborate
- **Privacy-Preserving Machine Learning**: Train models on sensitive data with cryptographic privacy

### Benefits

- Provides cryptographic privacy guarantees beyond federated average
- Ensures computational integrity with zero-knowledge proofs
- Prevents even intermediary results from being exposed
- Creates cryptographically verifiable audit trails

## Algorithm Selection Guidelines

When choosing between execution algorithms, consider these factors:

1. **Privacy Requirements**
   - For standard privacy needs: Use Federated Average
   - For maximum privacy with cryptographic guarantees: Use Secure Aggregation

2. **Performance Considerations**
   - Federated Average: Higher performance, lower computational overhead
   - Secure Aggregation: Higher security, but increased computational cost

3. **Trust Model**
   - Collaborative parties with some trust: Federated Average may be sufficient
   - Mutually distrusting parties: Secure Aggregation provides stronger guarantees

4. **Data Sensitivity**
   - Moderate sensitivity: Federated Average
   - High sensitivity (financial, healthcare): Secure Aggregation

5. **Regulatory Requirements**
   - Basic compliance: Federated Average with audit trails
   - Stringent regulatory environments: Secure Aggregation with ZK proofs

## Implementation Examples

### Machine Learning Model Training

```python
# Deploy federated learning application
ml_deployment = sdk.deploy_dapp(
    name="distributed-ml-training",
    source_path="./ml_model",
    execution_options={
        "algorithm": "federated-average",
        "vpod_count": 5,
        "ml_framework": "tensorflow",
        "epochs": 20,
        "batch_size": 64
    }
)

# Configure data sources for each vPod
data_config = sdk.configure_dapp_data(
    dapp_id=ml_deployment["dapp_id"],
    data_sources=[
        {"vpod_id": "vpod-1", "data_uri": "ipfs://QmData1..."},
        {"vpod_id": "vpod-2", "data_uri": "ipfs://QmData2..."},
        {"vpod_id": "vpod-3", "data_uri": "ipfs://QmData3..."},
        {"vpod_id": "vpod-4", "data_uri": "ipfs://QmData4..."},
        {"vpod_id": "vpod-5", "data_uri": "ipfs://QmData5..."}
    ]
)

# Execute training
training = sdk.execute_dapp(
    dapp_id=ml_deployment["dapp_id"],
    input_parameters={
        "model_architecture": "cnn",
        "learning_rate": 0.001,
        "optimizer": "adam"
    }
)

# Monitor training progress
progress = sdk.check_dapp_execution(
    execution_id=training["execution_id"]
)

# Get final model
result = sdk.get_dapp_results(
    execution_id=training["execution_id"]
)
print(f"Final model stored at: {result['output_uri']}")
```

### Privacy-Preserving Data Analysis

```python
# Deploy secure data analysis application
analysis_deployment = sdk.deploy_dapp(
    name="privacy-preserving-analytics",
    source_path="./analytics",
    execution_options={
        "algorithm": "secure-aggregation",
        "vpod_count": 3,
        "security_threshold": 2
    }
)

# Execute secure analysis
analysis = sdk.execute_dapp(
    dapp_id=analysis_deployment["dapp_id"],
    input_parameters={
        "analysis_type": "statistics",
        "target_fields": ["income", "spending", "savings"],
        "operations": ["mean", "median", "correlation"]
    },
    security_options={
        "encryption_level": "high",
        "generate_zkp": True
    }
)

# Get cryptographically verified results
verified_results = sdk.get_verified_results(
    execution_id=analysis["execution_id"],
    verification_options={
        "verify_zkp": True,
        "verify_blockchain_record": True
    }
)

# Export verification proof for auditors
proof_export = sdk.export_verification_proof(
    proof_id=verified_results["proof_id"],
    export_format="pdf",
    destination="./analysis_verification_proof.pdf"
)
```

## Integration with Blockchain

Both algorithms integrate with the MetaNode blockchain infrastructure:

1. **Results Recording**
   - Computation results are hashed and recorded on-chain
   - Transaction hash serves as immutable reference

2. **Verification Proofs**
   - Chainlink.lock proofs link computation results to blockchain state
   - Proofs contain cryptographic evidence of correct execution

3. **Audit Trail**
   - Complete execution history is recorded in immutable blockchain logs
   - Execution can be verified and audited by third parties

## Conclusion

The MetaNode SDK provides two powerful execution algorithms that enable decentralized application execution in a Web3 environment. Federated Average offers a balanced approach to distributed computing with privacy preservation, while Secure Aggregation provides enhanced cryptographic guarantees for sensitive computations.

By leveraging these algorithms through the vPod technology, developers can build applications that maintain data privacy, ensure computational integrity, and provide verifiable results through blockchain integration.

For implementation guidance and examples, refer to the [Complete Workflow Tutorial](/docs/tutorials/01_complete_workflow.md) and the [SDK API Reference](/docs/sdk-reference/).
