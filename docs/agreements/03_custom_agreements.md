# Creating Custom Agreements

This document explains how to create and manage custom agreements in the MetaNode SDK.

## Introduction to Custom Agreements

While the MetaNode SDK provides standard agreement types, custom agreements allow you to define specialized terms, conditions, and validation logic for unique requirements.

## Custom Agreement Components

A custom agreement consists of:

1. **Schema Definition**: Structure of the agreement data
2. **Rules**: Business logic that governs the agreement
3. **Execution Logic**: Code that implements agreement operations
4. **Validation**: Checks ensuring agreement conditions are met

## Basic Custom Agreement Creation

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Create a simple custom agreement
custom_agreement = sdk.create_agreement(
    name="research-data-access",
    custom_type="data_access_agreement",
    participants=[
        {"address": "0x123abc...", "role": "provider"},
        {"address": "0x456def...", "role": "consumer"}
    ],
    terms={
        "access_duration": 30,  # days
        "data_description": "Genomic research dataset",
        "allowed_operations": ["read", "analyze"],
        "allowed_purpose": "academic_research_only",
        "security_requirements": "encrypted_storage"
    },
    validation_rules=[
        "consumer_must_have_credentials",
        "provider_must_verify_purpose",
        "access_limited_to_duration"
    ]
)
```

## Agreement Templates

Creating a reusable agreement template:

```python
# Define a custom agreement template
custom_template = {
    "name": "research_collaboration",
    "description": "Template for research collaboration agreements",
    "schema": {
        "research_topic": {"type": "string", "required": True},
        "institutions": {"type": "array", "required": True},
        "duration_months": {"type": "number", "required": True},
        "data_sharing_permitted": {"type": "boolean", "default": False},
        "publication_rights": {"type": "string", "enum": ["joint", "independent", "approval_required"]}
    },
    "default_rules": [
        "all_parties_approve_publications",
        "data_deletion_at_termination"
    ]
}

# Register the template
sdk.register_agreement_template(
    template_definition=custom_template,
    template_id="research_collaboration_v1"
)
```

## Schema Definition

The schema defines the structure of your agreement:

```python
# Define a complex agreement schema
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["project_name", "participants", "resources"],
    "properties": {
        "project_name": {"type": "string"},
        "participants": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "role"],
                "properties": {
                    "id": {"type": "string"},
                    "role": {"type": "string", "enum": ["data_provider", "algorithm_provider", "compute_provider"]},
                    "permissions": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "resources": {
            "type": "object",
            "properties": {
                "datasets": {"type": "array", "items": {"type": "string"}},
                "algorithms": {"type": "array", "items": {"type": "string"}},
                "compute": {
                    "type": "object",
                    "properties": {
                        "cpu_hours": {"type": "number"},
                        "memory_gb": {"type": "number"},
                        "gpu_required": {"type": "boolean"}
                    }
                }
            }
        },
        "duration": {"type": "object",
            "properties": {
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"}
            }
        },
        "terms": {
            "type": "object",
            "properties": {
                "confidentiality": {"type": "string", "enum": ["strict", "moderate", "open"]},
                "result_sharing": {"type": "string"},
                "termination_conditions": {"type": "array", "items": {"type": "string"}}
            }
        }
    }
}

# Create agreement with this schema
sdk.register_agreement_schema(
    schema=schema,
    schema_id="collaborative_research_schema_v1"
)
```

## Solidity Smart Contract Implementation

MetaNode agreements are implemented as Solidity smart contracts on the blockchain. The SDK abstracts these contracts, but you can also work directly with them.

Here's an example of the underlying Solidity contract for a task agreement:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title TaskAgreement
 * @dev Contract for managing task agreements between users and execution rules
 */
contract TaskAgreement {
    // Task status enum
    enum TaskStatus { Created, InProgress, Completed, Disputed, Cancelled }
    
    // Task structure
    struct Task {
        uint256 id;
        address owner;
        string title;
        string description;
        uint256 createdAt;
        uint256 updatedAt;
        TaskStatus status;
        mapping(address => bool) approvedExecutors;
        address assignedExecutor;
        bytes32 resultHash;
    }
    
    // Contract state variables
    uint256 public taskCount;
    mapping(uint256 => Task) public tasks;
    
    // Events
    event TaskCreated(uint256 indexed taskId, address indexed owner, string title);
    event TaskAssigned(uint256 indexed taskId, address indexed executor);
    event TaskCompleted(uint256 indexed taskId, bytes32 resultHash);
    event TaskStatusChanged(uint256 indexed taskId, TaskStatus newStatus);
    
    // Task creation function
    function createTask(string memory _title, string memory _description) public returns (uint256) {
        // Implementation details...
    }
    
    // Other task management functions...
}
```

### Creating Custom Solidity Agreement Contracts

You can deploy custom agreement contracts:

```python
# Define a custom Solidity contract
contract_source = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CustomAgreement {
    struct Agreement {
        address creator;
        string name;
        mapping(address => bool) participants;
        mapping(address => bool) signatures;
        bool isActive;
    }
    
    mapping(bytes32 => Agreement) public agreements;
    
    event AgreementCreated(bytes32 indexed id, string name, address creator);
    event ParticipantAdded(bytes32 indexed id, address participant);
    event AgreementSigned(bytes32 indexed id, address signer);
    
    function createAgreement(string memory name) public returns (bytes32) {
        bytes32 id = keccak256(abi.encodePacked(msg.sender, name, block.timestamp));
        
        Agreement storage agreement = agreements[id];
        agreement.creator = msg.sender;
        agreement.name = name;
        agreement.participants[msg.sender] = true;
        agreement.isActive = true;
        
        emit AgreementCreated(id, name, msg.sender);
        return id;
    }
    
    function addParticipant(bytes32 id, address participant) public {
        require(agreements[id].creator == msg.sender, "Only creator can add participants");
        agreements[id].participants[participant] = true;
        emit ParticipantAdded(id, participant);
    }
    
    function signAgreement(bytes32 id) public {
        require(agreements[id].participants[msg.sender], "Not a participant");
        agreements[id].signatures[msg.sender] = true;
        emit AgreementSigned(id, msg.sender);
    }
}
"""

# Deploy the custom contract
custom_contract = sdk.deploy_solidity_contract(
    contract_source=contract_source,
    contract_name="CustomAgreement"
)

# Get the contract address
contract_address = custom_contract["address"]
print(f"Custom agreement contract deployed at {contract_address}")
```

### Interacting with Custom Agreement Contracts

Once deployed, you can interact with your custom agreement contract:

```python
# Create an agreement using the deployed contract
create_tx = sdk.execute_contract_function(
    contract_address=contract_address,
    function_name="createAgreement",
    function_params=["Research Collaboration Agreement"],
    sender_address="0x123abc..."
)

# Get the agreement ID from the transaction receipt
agreement_id = sdk.get_event_data(
    transaction_hash=create_tx["transaction_hash"],
    event_name="AgreementCreated"
)["id"]

# Add participants to the agreement
sdk.execute_contract_function(
    contract_address=contract_address,
    function_name="addParticipant",
    function_params=[agreement_id, "0x456def..."],
    sender_address="0x123abc..."
)
```

## Agreement Validation Rules

Validation rules ensure that agreements meet required conditions before execution. The MetaNode SDK provides several ways to implement validation.

### Built-in Validation Rules

```python
# Create agreement with built-in validation rules
validated_agreement = sdk.create_agreement(
    name="validated-data-sharing",
    agreement_type="data_sharing",
    participants=[
        {"address": "0x123abc...", "role": "provider"},
        {"address": "0x456def...", "role": "consumer"}
    ],
    terms={
        "dataset_id": "genomic-dataset-123",
        "access_level": "read_only",
        "access_duration": 90  # days
    },
    validation_rules=[
        "participant_roles_must_be_unique",
        "all_participants_must_sign",
        "provider_must_own_dataset",
        "consumer_must_have_valid_credentials"
    ]
)
```

### Custom Validation Functions

You can implement custom validation logic:

```python
# Define a custom validation function
def validate_research_credentials(agreement):
    """Verify that consumers have proper research credentials"""
    from metanode.verification import credential_service
    
    # Extract consumer addresses from agreement
    consumers = [p["address"] for p in agreement["participants"] if p["role"] == "consumer"]
    
    # Check each consumer's credentials
    for consumer in consumers:
        credential = credential_service.get_credential(consumer)
        
        if not credential or not credential.is_valid():
            return {
                "valid": False,
                "reason": f"Consumer {consumer} does not have valid research credentials"
            }
            
        if credential.type != "research_institution":
            return {
                "valid": False,
                "reason": f"Consumer {consumer} is not affiliated with a research institution"
            }
    
    # All checks passed
    return {"valid": True}

# Register the custom validation function
sdk.register_validation_function(
    function=validate_research_credentials,
    name="validate_research_credentials"
)

# Use custom validation in agreement
agreement = sdk.create_agreement(
    name="research-data-access",
    # Other parameters as before...
    validation_rules=[
        "participant_roles_must_be_unique",
        "validate_research_credentials"  # Custom validation
    ]
)
```

## Agreement Execution Logic

Agreements can include execution logic that governs automated actions.

### Defining Execution Logic

```python
# Define execution logic for data access agreement
execution_logic = """
from metanode.execution import DataAccessControl

def on_agreement_activated(agreement, context):
    """Called when agreement becomes active"""
    # Set up access control
    dataset_id = agreement['terms']['dataset_id']
    
    # Get consumer addresses
    consumers = [p['address'] for p in agreement['participants'] if p['role'] == 'consumer']
    
    # Create access permissions for each consumer
    for consumer in consumers:
        DataAccessControl.grant_access(
            dataset_id=dataset_id,
            address=consumer,
            access_level=agreement['terms']['access_level'],
            expires_at=context.current_time + (agreement['terms']['access_duration'] * 86400)
        )

def on_agreement_terminated(agreement, context):
    """Called when agreement is terminated"""
    # Revoke all access
    dataset_id = agreement['terms']['dataset_id']
    consumers = [p['address'] for p in agreement['participants'] if p['role'] == 'consumer']
    
    for consumer in consumers:
        DataAccessControl.revoke_access(dataset_id=dataset_id, address=consumer)
"""

# Register the execution logic
sdk.register_execution_logic(
    code=execution_logic,
    name="data_access_execution"
)

# Create agreement with this execution logic
agreement = sdk.create_agreement(
    name="automated-data-access",
    # Other parameters as before...
    execution_logic="data_access_execution"
)
```

### Execution Triggers

Agreement execution logic can be triggered by various events:

```python
# Define execution triggers
triggers = {
    "on_activated": "on_agreement_activated",
    "on_terminated": "on_agreement_terminated",
    "on_milestone": "on_milestone_reached",
    "on_condition": {
        "condition": "access_count > 1000",
        "action": "notify_provider"
    },
    "scheduled": {
        "interval": "daily",
        "action": "update_access_logs"
    }
}

# Create agreement with execution triggers
agreement = sdk.create_agreement(
    name="triggered-data-access",
    # Other parameters as before...
    execution_logic="data_access_execution",
    execution_triggers=triggers
)
```

## Verification Proofs and Chainlink.lock 

Agreements in MetaNode use cryptographic verification proofs to ensure integrity and immutability.

### Creating Verification Proofs

```python
# Generate a verification proof for an agreement
verification_proof = sdk.generate_verification_proof(
    agreement_id="agr-123",
    verification_type="chainlink.lock",
    proof_parameters={
        "include_signatures": True,
        "include_terms": True,
        "hash_algorithm": "keccak256"
    }
)

# The proof can be verified independently
print(f"Verification proof generated: {verification_proof['proof_id']}")
print(f"Verification URL: {verification_proof['verification_url']}")
```

### Validating External Verification

```python
# Validate a verification proof
validation_result = sdk.validate_verification_proof(
    proof_id="prf-456",
    validation_options={
        "check_blockchain_record": True,
        "check_signatures": True
    }
)

if validation_result["valid"]:
    print("Proof is valid")
    print(f"Recorded on blockchain at: {validation_result['blockchain_record']}")
    print(f"Signed by: {', '.join(validation_result['signers'])}")
else:
    print(f"Proof validation failed: {validation_result['reason']}")
```

## Agreement Testing

Before deploying production agreements, test them thoroughly:

```python
# Test agreement execution in sandbox environment
test_result = sdk.test_agreement(
    agreement_template="data_sharing",
    test_parameters={
        "participants": [
            {"address": "0xtest1", "role": "provider"},
            {"address": "0xtest2", "role": "consumer"}
        ],
        "terms": {
            "dataset_id": "test-dataset",
            "access_level": "read_only",
            "access_duration": 30
        }
    },
    test_scenarios=[
        "activation",
        "termination",
        "dispute_resolution"
    ]
)

print("Test Results:")
for scenario, result in test_result["scenarios"].items():
    print(f"Scenario '{scenario}': {'Success' if result['passed'] else 'Failed'}")
    if not result["passed"]:
        print(f"  Reason: {result['reason']}")
```

## Best Practices

### Security Considerations

1. **Validation Priority**: Always include validation rules that protect sensitive operations
2. **Access Control**: Use precise access controls to limit data visibility
3. **Versioning**: Include schema versioning for forward compatibility
4. **Audit Logging**: Enable comprehensive logging for tracking agreement activities
5. **Verification Proofs**: Generate and store verification proofs for all critical agreements

### Performance Optimization

1. **Batched Operations**: Bundle multiple related agreements for efficiency
2. **Smart Schema Design**: Only capture necessary data in agreement schemas
3. **Cached Validation**: Cache validation results when appropriate
4. **Execution Throttling**: Set reasonable limits for automated execution actions

### Multi-party Agreements

1. **Clear Roles**: Define explicit roles and permissions for each participant
2. **Staged Execution**: Implement multi-stage agreement execution for complex workflows
3. **Dispute Resolution**: Include clear dispute resolution procedures
4. **Partial Execution**: Allow agreements to proceed with partial participant sets when appropriate

## Conclusion

Custom agreements in MetaNode provide powerful mechanisms for defining, validating, and executing complex multi-party relationships. By leveraging the MetaNode SDK, on-chain Solidity contracts, and verification proofs, you can create secure and auditable agreements for any use case.
