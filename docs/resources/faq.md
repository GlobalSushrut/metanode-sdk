# Frequently Asked Questions (FAQ)

## General Questions

### What is the MetaNode SDK?

The MetaNode SDK is a comprehensive toolkit for creating, managing, and validating blockchain-based agreements. It enables developers to build applications that leverage blockchain technology for secure, transparent, and compliant agreement lifecycle management.

### What programming languages does the MetaNode SDK support?

Currently, the MetaNode SDK is available for Python (version 3.8 and higher). Support for JavaScript/TypeScript and Go is planned for future releases.

### Is the SDK open-source?

The MetaNode SDK core components are open-source and available on GitHub. Some enterprise features may require a commercial license.

## Testnet and Connectivity

### Where is the MetaNode testnet hosted?

The MetaNode testnet is accessible at the following endpoints:
- RPC: http://159.203.17.36:8545
- WebSocket: ws://159.203.17.36:8546

### How can I test if my connection to the testnet is working?

You can use the following code snippet to test your connection:

```python
from metanode.full_sdk import MetaNodeSDK

sdk = MetaNodeSDK()
connection_test = sdk.test_rpc_connection()

if connection_test["connected"]:
    print("Successfully connected to testnet!")
    print(f"Current block number: {connection_test['block_number']}")
else:
    print(f"Connection failed: {connection_test['error']}")
```

Or use the CLI:

```bash
metanode-cli testnet connect
```

### How do I contribute to the testnet decentralization?

You can deploy your own node cluster to enhance testnet decentralization:

```python
# Generate node identities and deploy a cluster
node_identities = sdk.generate_node_identities(count=3, roles=["validator", "peer"])
node_configs = sdk.create_node_configs(node_identities, "metanode-testnet")
cluster = sdk.deploy_node_cluster("my-validator-cluster", node_configs)
```

Or use the CLI:

```bash
metanode-cli node create-cluster --name my-validator-cluster --nodes 3 --roles validator,peer
```

## Agreements

### What types of agreements can I create with the MetaNode SDK?

The SDK supports various agreement types including data sharing agreements, service level agreements, collaboration agreements, and more. You can also create custom agreement types with your own schema definitions.

### Can I create custom agreement schemas?

Yes, you can register custom agreement schemas:

```python
schema = {
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
        }
    }
}

schema_id = sdk.register_agreement_schema(schema, "research_collab_v1")
```

### How are agreements stored?

Agreements are stored both off-chain and on-chain:
- The complete agreement contents are stored off-chain in a distributed storage system
- A cryptographic hash and essential metadata are stored on-chain for verification and enforcement
- All storage is secure, immutable, and designed for compliance with various regulatory frameworks

## Validation and Verification

### What is the difference between validation and verification in the MetaNode SDK?

- **Validation** checks an agreement against rules, schemas, and conditions to ensure it's well-formed, complete, and meets all requirements.
- **Verification** is the process of cryptographically proving that an agreement exists, hasn't been tampered with, and has been properly signed by all parties.

### What is a chainlink.lock verification proof?

A chainlink.lock verification proof is a cryptographic proof that links an agreement to the blockchain, providing an immutable record of its existence, contents, and signatures. It can be independently verified by third parties and serves as evidence of agreement integrity.

### How do I validate that an agreement meets my organization's requirements?

You can register custom validators:

```python
def custom_validator(agreement):
    if "special_terms" not in agreement["terms"]:
        return {
            "valid": False,
            "reason": "Missing special terms",
            "severity": "error"
        }
    return {"valid": True}

validator_id = sdk.register_validator(custom_validator, "special_terms_validator")
```

## Compliance and Auditing

### How does the MetaNode SDK help with regulatory compliance?

The SDK provides:
- Built-in compliance checks for common regulatory frameworks
- Immutable audit trails with blockchain anchoring
- Cryptographic verification proofs
- Real-time compliance monitoring
- Scheduled compliance reporting

### How do I access an agreement's audit trail?

```python
audit_trail = sdk.get_agreement_audit_trail(
    agreement_id="agr-123",
    time_range={
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-06-21T00:00:00Z"
    }
)
```

### Can I export audit trails for external auditors?

Yes, you can export audit trails in various formats:

```python
export_result = sdk.export_agreement_audit_trail(
    agreement_id="agr-123",
    export_format="pdf",
    destination="/path/to/audit-report.pdf"
)
```

## Web3 Dapp Execution

### What is the dapp execution environment in MetaNode SDK?

The MetaNode SDK's dapp execution environment is a Web3-native system for running decentralized applications. It enables trustless, verifiable execution of applications in containerized environments (vPods) with blockchain integration. Applications execute in a decentralized context with cryptographic proofs of correct execution.

### What are vPods and how do they work?

vPods (Virtual Pods) are MetaNode's containerized execution environments that enable decentralized application execution:

```python
# Deploy a decentralized application using vPods
app_deployment = sdk.deploy_dapp(
    name="my-decentralized-app",
    source_path="./app_directory",
    execution_options={
        "algorithm": "federated-average",
        "vpod_count": 3
    }
)
```

vPods provide isolated execution environments with direct blockchain connectivity, verification capabilities, and secure multi-party computation features.

### What execution algorithms does the SDK support?

The MetaNode SDK currently supports two primary execution algorithms:

1. **Federated Average (federated-average)** - For distributed computation with aggregated results, suitable for collaborative machine learning and data analysis.

2. **Secure Aggregation (secure-aggregation)** - Enhanced privacy protection with cryptographic security for sensitive applications requiring stronger privacy guarantees.

### How do I integrate dapp execution with agreements?

You can link dapp executions directly to agreement terms:

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
            "max_executions": 100
        }
    }
)

# Execute dapp based on agreement
execution = sdk.execute_dapp_from_agreement(
    agreement_id=agreement["id"],
    execution_parameters={
        "dataset_uri": "ipfs://QmZ9..."
    }
)
```

### How are execution results verified?

Execution results are verified through cryptographic proofs and blockchain consensus:

```python
# Verify execution proof
verification = sdk.verify_execution_proof(
    proof_id=results["proof_id"]
)

if verification["verified"]:
    print("Execution proof verification successful!")
    print(f"Consensus: {verification['consensus_level']}%")
else:
    print(f"Proof verification failed: {verification['reason']}")
```

## Infrastructure and Deployment

### What deployment options does the MetaNode SDK support?

The SDK supports multiple deployment options:
- Local development environment
- Docker containers
- Kubernetes clusters
- Cloud providers (AWS, Azure, GCP)

### How do I deploy node clusters for production?

For production deployments, we recommend using Kubernetes:

```python
# Deploy a production node cluster
production_cluster = sdk.deploy_node_cluster(
    cluster_name="production-validator-cluster",
    node_configs=node_configs,
    deployment_options={
        "deployment_method": "kubernetes",
        "resource_limits": {
            "cpu_per_node": 4,
            "memory_per_node": "8Gi"
        },
        "high_availability": True,
        "monitoring_enabled": True,
        "alerts_enabled": True
    }
)
```

### How do I move from testnet to production?

Follow our [Production Migration Tutorial](/docs/tutorials/03_production_migration.md) for a step-by-step guide on migrating from testnet to production. Key steps include:
1. Planning your migration
2. Deploying production infrastructure
3. Configuring the SDK for production
4. Migrating agreements
5. Verification and validation
6. Security hardening
7. Setting up monitoring and alerting

## Troubleshooting

### How do I debug connection issues to the testnet?

1. Verify network connectivity to the testnet endpoint (159.203.17.36:8545)
2. Check firewall settings that might block the connection
3. Use the verbose logging option in the SDK:
   ```python
   sdk = MetaNodeSDK(log_level="debug")
   ```
4. Use the CLI diagnostic tool:
   ```bash
   metanode-cli testnet diagnostics
   ```

### What should I do if agreement validation fails?

1. Check the validation error message for specific issues
2. Review the agreement structure against its schema
3. Ensure all required fields are present and correctly formatted
4. Verify that all signatures are valid
5. Check if custom validators are properly registered

### How do I resolve vPod deployment failures?

1. Verify that Docker or Kubernetes is properly configured
2. Check resource availability (CPU, memory, disk)
3. Review networking settings and ensure ports are accessible
4. Check the vPod logs:
   ```bash
   metanode-cli vpod logs --id <vpod_id>
   ```
5. Try redeploying with more resources:
   ```python
   sdk.deploy_validator_vpod(
       node_identity=node_identity,
       vpod_options={"resources": {"cpu": 4, "memory": "8Gi"}}
   )
   ```

## Additional Resources

For more detailed information, please refer to:
- [Complete Workflow Tutorial](/docs/tutorials/01_complete_workflow.md)
- [Testnet Connection Tutorial](/docs/tutorials/02_testnet_connection.md)
- [Production Migration Tutorial](/docs/tutorials/03_production_migration.md)
- [SDK API Reference](/docs/sdk-reference/)

If your question isn't answered here, please contact our support team at support@metanode.example.com.
