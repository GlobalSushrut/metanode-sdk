# Agreement Integration with Dapp Execution

## Overview

The MetaNode SDK's agreement system and dapp execution environment are designed to work seamlessly together, providing a comprehensive framework for blockchain-based application execution governed by formal agreements. This document explains how these two core components integrate to enable trustless, verifiable, and compliant decentralized applications.

## Agreement-Governed Execution

### Core Concept

Agreement-governed execution is a paradigm where decentralized applications execute according to the terms and conditions specified in a blockchain-based agreement. This ensures that:

1. Execution complies with predefined rules and permissions
2. Resource usage adheres to agreed-upon limits
3. All parties have transparency into execution conditions
4. Results are verifiable and linked to agreement terms
5. Compliance and auditability are guaranteed

## Implementation

### Creating an Execution Agreement

```python
from metanode.full_sdk import MetaNodeSDK

sdk = MetaNodeSDK()

# Create an agreement for dapp execution
execution_agreement = sdk.create_agreement(
    name="ml-training-agreement",
    agreement_type="compute_execution",
    participants=[
        {"address": "0x123abc...", "role": "data_provider"},
        {"address": "0x456def...", "role": "compute_provider"},
        {"address": "0x789ghi...", "role": "result_consumer"}
    ],
    terms={
        "execution_parameters": {
            "algorithm": "federated-average",
            "max_execution_time_hours": 48,
            "resource_limits": {
                "cpu_cores": 8,
                "memory_gb": 16,
                "storage_gb": 100
            }
        },
        "data_access": {
            "allowed_datasets": [
                "ipfs://QmDataset1...",
                "ipfs://QmDataset2..."
            ],
            "data_retention_days": 7,
            "data_usage_purpose": "model_training_only"
        },
        "result_handling": {
            "result_access": ["data_provider", "result_consumer"],
            "verification_required": True,
            "audit_trail_retention_days": 365
        }
    },
    validation_options={
        "validators_required": 3,
        "consensus_threshold": 2
    }
)

print(f"Execution agreement created with ID: {execution_agreement['id']}")
```

### Deploying a Dapp Linked to an Agreement

```python
# Deploy a dapp linked to the agreement
dapp_deployment = sdk.deploy_dapp(
    name="ml-training-dapp",
    source_path="./ml_model",
    agreement_id=execution_agreement["id"],  # Link to agreement
    execution_options={
        "algorithm": "federated-average",
        "vpod_count": 5,
        "resource_allocation": {
            "cpu_per_vpod": 2,
            "memory_per_vpod": "4Gi"
        }
    }
)

print(f"Dapp deployed with ID: {dapp_deployment['dapp_id']}")
```

### Executing Within Agreement Constraints

```python
# Execute the dapp under agreement governance
execution = sdk.execute_dapp_from_agreement(
    agreement_id=execution_agreement["id"],
    dapp_id=dapp_deployment["dapp_id"],
    execution_parameters={
        "dataset_uri": "ipfs://QmDataset1...",
        "training_parameters": {
            "epochs": 20,
            "batch_size": 64,
            "learning_rate": 0.001
        }
    },
    compliance_options={
        "enforce_resource_limits": True,
        "validate_data_access": True,
        "generate_compliance_proof": True
    }
)

print(f"Agreement-governed execution started: {execution['execution_id']}")
```

## Enforcement Mechanisms

The MetaNode SDK uses several mechanisms to enforce agreement terms during dapp execution:

### 1. Resource Limiting

```python
# Enforcing resource limits from agreement
resource_config = sdk.configure_execution_resources(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    enforcement_options={
        "hard_limits": True,
        "monitoring_interval_seconds": 60,
        "action_on_violation": "suspend"  # Options: warn, suspend, terminate
    }
)
```

### 2. Data Access Control

```python
# Configuring data access based on agreement terms
data_access = sdk.configure_execution_data_access(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    access_enforcement={
        "verify_dataset_permission": True,
        "encrypt_intermediate_results": True,
        "data_usage_tracking": True
    }
)
```

### 3. Compliance Monitoring

```python
# Set up compliance monitoring for the execution
compliance_monitor = sdk.monitor_execution_compliance(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    monitoring_options={
        "real_time": True,
        "monitoring_interval_seconds": 300,
        "alert_on_violation": True
    }
)

# Register a compliance violation handler
def on_compliance_violation(violation):
    print(f"Compliance violation detected: {violation['type']}")
    print(f"Severity: {violation['severity']}")
    print(f"Details: {violation['details']}")
    print(f"Timestamp: {violation['timestamp']}")

compliance_monitor.on_violation(on_compliance_violation)
```

## Verification of Agreement Compliance

### Runtime Verification

```python
# Runtime verification of agreement compliance
verification = sdk.verify_execution_compliance(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    verification_points=["resource_usage", "data_access", "result_handling"]
)

for point in verification["verification_points"]:
    print(f"Verification point: {point['name']}")
    print(f"Compliant: {point['compliant']}")
    if not point['compliant']:
        print(f"Violation details: {point['violation_details']}")
```

### Post-Execution Audit

```python
# Generate an audit report for the execution
audit_report = sdk.generate_execution_audit(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    report_options={
        "include_resource_usage": True,
        "include_data_access_logs": True,
        "include_verification_proofs": True,
        "format": "pdf"
    }
)

print(f"Audit report generated: {audit_report['report_path']}")
```

## Results Handling According to Agreement

```python
# Retrieve and distribute results according to agreement terms
results = sdk.get_dapp_results(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    result_options={
        "verify_agreement_compliance": True,
        "apply_access_controls": True,
        "generate_verification_proof": True
    }
)

# Distribute results to authorized parties
distribution = sdk.distribute_execution_results(
    results_id=results["results_id"],
    agreement_id=execution_agreement["id"],
    distribution_options={
        "notify_participants": True,
        "access_control_enforcement": True,
        "include_verification_proofs": True
    }
)

for recipient in distribution["recipients"]:
    print(f"Results distributed to: {recipient['address']}")
    print(f"Access URL: {recipient['access_url']}")
    print(f"Verification proof: {recipient['verification_proof_id']}")
```

## CLI Integration

```bash
# Create an execution agreement
metanode-cli agreement create \
  --name ml-training-agreement \
  --type compute_execution \
  --participants '[{"address":"0x123...","role":"data_provider"},{"address":"0x456...","role":"compute_provider"},{"address":"0x789...","role":"result_consumer"}]' \
  --terms '{"execution_parameters":{"algorithm":"federated-average","max_execution_time_hours":48},"data_access":{"allowed_datasets":["ipfs://QmDataset1..."]}}'

# Deploy a dapp under agreement governance
metanode-cli dapp deploy \
  --name ml-training-dapp \
  --source ./ml_model \
  --agreement AGR-123456 \
  --algorithm federated-average \
  --vpods 5

# Execute the dapp within agreement constraints
metanode-cli dapp execute-from-agreement \
  --agreement AGR-123456 \
  --dapp DAPP-123456 \
  --params '{"dataset_uri":"ipfs://QmDataset1...","training_parameters":{"epochs":20}}'
```

## Advanced Integration Patterns

### Multi-Agreement Execution

For complex workflows involving multiple agreements:

```python
# Create a primary execution agreement
primary_agreement = sdk.create_agreement(
    name="primary-execution-agreement",
    agreement_type="compute_execution",
    # ... agreement details
)

# Create a data access agreement
data_agreement = sdk.create_agreement(
    name="data-access-agreement",
    agreement_type="data_sharing",
    # ... agreement details
)

# Create a results distribution agreement
results_agreement = sdk.create_agreement(
    name="results-distribution-agreement",
    agreement_type="result_sharing",
    # ... agreement details
)

# Link agreements for a unified workflow
linked_workflow = sdk.link_agreements(
    primary_agreement_id=primary_agreement["id"],
    linked_agreements=[
        {"agreement_id": data_agreement["id"], "relationship": "data_source"},
        {"agreement_id": results_agreement["id"], "relationship": "result_distribution"}
    ],
    workflow_name="complete-ml-workflow"
)

# Execute the workflow
workflow_execution = sdk.execute_agreement_workflow(
    workflow_id=linked_workflow["workflow_id"],
    execution_parameters={
        # ... execution details
    }
)
```

### Dynamic Agreement Updates During Execution

For long-running executions that may require agreement amendments:

```python
# Monitor long-running execution
execution_status = sdk.check_dapp_execution(
    execution_id=execution["execution_id"]
)

# If resource adjustment is needed, update the agreement
if execution_status["resource_usage"]["cpu_utilization"] > 90:
    agreement_update = sdk.update_agreement(
        agreement_id=execution_agreement["id"],
        terms={
            "execution_parameters": {
                "resource_limits": {
                    "cpu_cores": 12,  # Increased from 8
                    "memory_gb": 24   # Increased from 16
                }
            }
        },
        update_reason="Resource adjustment for optimal performance"
    )
    
    # Apply the updated agreement terms to the running execution
    resource_update = sdk.update_execution_resources(
        execution_id=execution["execution_id"],
        agreement_id=execution_agreement["id"]
    )
```

## Integration with vPod Technology

vPods are configured to enforce agreement terms at the container level:

```python
# Deploy vPods with agreement-enforcing configuration
vpod_deployment = sdk.deploy_agreement_vpods(
    agreement_id=execution_agreement["id"],
    vpod_options={
        "enforce_resource_limits": True,
        "enforce_data_access_controls": True,
        "enforce_network_policies": True,
        "monitoring_enabled": True
    }
)

# Each vPod receives agreement-specific configuration
for vpod in vpod_deployment["vpods"]:
    print(f"vPod {vpod['vpod_id']} configured with agreement constraints")
    print(f"Resource limits: {vpod['resource_limits']}")
    print(f"Access controls: {vpod['access_controls']}")
```

## Blockchain Integration

Agreement compliance is recorded on the blockchain:

```python
# Record execution compliance on blockchain
blockchain_record = sdk.record_execution_compliance(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    blockchain_options={
        "record_method": "transaction",  # Options: transaction, event, state
        "include_compliance_hash": True,
        "include_verification_proof": True,
        "gas_limit": 300000
    }
)

print(f"Compliance recorded on blockchain: {blockchain_record['tx_hash']}")
print(f"Block number: {blockchain_record['block_number']}")
```

## Benefits of Integration

The integration between agreements and dapp execution provides several key benefits:

1. **Trustless Execution**: All parties can trust that execution follows agreed terms
2. **Verifiable Compliance**: Cryptographic proofs verify agreement adherence
3. **Automated Enforcement**: Terms are automatically enforced during execution
4. **Transparent Governance**: All parties have visibility into execution conditions
5. **Regulatory Compliance**: Audit trails provide evidence of compliant execution
6. **Dispute Resolution**: Clear evidence in case of disagreements
7. **Flexible Workflows**: Complex multi-party workflows can be securely coordinated

## Best Practices

### 1. Agreement Precision

Create agreements with precise, machine-enforceable terms:

```python
# Example of well-defined, enforceable terms
precise_terms = {
    "execution_parameters": {
        "algorithm": "federated-average",
        "max_execution_time_hours": 48,
        "resource_limits": {
            "cpu_cores": 8,
            "memory_gb": 16,
            "storage_gb": 100
        },
        "timeout_action": "terminate_and_notify"
    }
}
```

### 2. Pre-Execution Validation

Always validate agreement compatibility before execution:

```python
# Validate agreement compatibility with execution parameters
validation = sdk.validate_execution_compatibility(
    agreement_id=execution_agreement["id"],
    dapp_id=dapp_deployment["dapp_id"],
    execution_parameters={
        "dataset_uri": "ipfs://QmDataset1...",
        "training_parameters": {
            "epochs": 20
        }
    }
)

if validation["compatible"]:
    print("Execution parameters compatible with agreement")
else:
    print(f"Compatibility issues: {validation['issues']}")
```

### 3. Comprehensive Monitoring

Implement real-time monitoring of agreement compliance:

```python
# Set up comprehensive monitoring
monitoring = sdk.configure_execution_monitoring(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    monitoring_options={
        "resource_monitoring": True,
        "data_access_monitoring": True,
        "network_monitoring": True,
        "blockchain_interaction_monitoring": True,
        "monitoring_interval_seconds": 60,
        "alert_thresholds": {
            "resource_usage": 0.8,  # Alert at 80% of limit
            "unauthorized_access_attempts": 0,  # Alert on any attempt
            "compliance_deviation": 0.05  # Alert at 5% deviation
        }
    }
)
```

### 4. Thorough Auditing

Maintain comprehensive audit trails:

```python
# Configure detailed audit logging
audit_config = sdk.configure_execution_audit(
    execution_id=execution["execution_id"],
    agreement_id=execution_agreement["id"],
    audit_options={
        "audit_detail_level": "high",  # Options: basic, standard, high
        "log_storage": {
            "blockchain_anchoring": True,
            "ipfs_storage": True,
            "local_storage": True
        },
        "event_types": ["resource_usage", "data_access", "network_activity", "results_handling"]
    }
)
```

## Conclusion

The integration of the MetaNode SDK's agreement system with its dapp execution environment provides a comprehensive framework for trustless, verifiable, and compliant decentralized applications. By governing execution through blockchain-based agreements, the MetaNode SDK ensures that all parties can collaborate with confidence, knowing that terms will be enforced and compliance can be verified cryptographically.

This agreement-governed execution model is particularly valuable for applications requiring trustless collaboration, regulatory compliance, or verifiable computation across organizational boundaries.

For implementation examples, refer to the [Complete Workflow Tutorial](/docs/tutorials/01_complete_workflow.md) which includes detailed steps for creating and executing agreement-governed applications.
