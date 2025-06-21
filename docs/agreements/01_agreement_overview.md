# Agreement Overview

This document provides an introduction to the MetaNode Agreement system, which enables secure, verifiable contracts for data sharing and computing on the blockchain.

## What Are MetaNode Agreements?

MetaNode Agreements are blockchain-based contracts that define terms, conditions, and permissions for data sharing and distributed computing between parties. Agreements provide:

1. **Verifiable Consent**: Cryptographically signed records of all parties' consent
2. **Terms Enforcement**: Automatic enforcement of agreement rules
3. **Audit Trail**: Immutable record of agreement history
4. **Conditional Access**: Data access governed by agreement terms
5. **Resource Management**: Configurable access limits and scheduling

## Agreement Architecture

```
┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │
│      Party A      │     │      Party B      │
│                   │     │                   │
└─────────┬─────────┘     └────────┬──────────┘
          │                        │
          │                        │
┌─────────▼────────────────────────▼──────────┐
│                                             │
│              Agreement Contract             │
│                                             │
├─────────────────────┬───────────────────────┤
│                     │                       │
│     Terms & Rules   │   Execution Logic     │
│                     │                       │
└─────────────────────┴───────────────────────┘
          │                        │
          │                        │
┌─────────▼────────────┐ ┌─────────▼──────────┐
│                      │ │                    │
│   Blockchain Ledger  │ │ Validator Network  │
│                      │ │                    │
└──────────────────────┘ └────────────────────┘
```

## Agreement Components

Each MetaNode Agreement consists of:

1. **Participants**: Parties bound by the agreement
2. **Terms**: Specific conditions and requirements
3. **Assets**: Data or resources governed by the agreement
4. **Actions**: Operations permitted or required by the agreement
5. **Validators**: Nodes that validate agreement execution
6. **Proofs**: Cryptographic verification of agreement compliance

## Creating an Agreement

### Using the SDK

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Define agreement terms
terms = {
    "title": "Data Processing Agreement",
    "description": "Agreement for processing customer data",
    "duration": 90,  # days
    "auto_renewal": True,
    "data_access": {
        "allowed_operations": ["read", "aggregate"],
        "prohibited_operations": ["store", "share"]
    },
    "resource_management": {
        "rate_limit": 100,  # requests per hour
        "access_schedule": "business_hours_only"
    }
}

# Define participants
participants = [
    {
        "address": "0x8956782345dcBA12345", 
        "role": "data_provider"
    },
    {
        "address": "0x9876543210fedcba", 
        "role": "data_processor"
    }
]

# Create the agreement
agreement = sdk.create_agreement(
    name="customer-data-processing",
    terms=terms,
    participants=participants,
    verify=True  # Generate verification proof
)

# Get agreement ID
agreement_id = agreement["id"]
print(f"Agreement created with ID: {agreement_id}")
```

### Using the CLI

```bash
# Create agreement using CLI
metanode-cli agreement create \
  --name customer-data-processing \
  --terms-file ./terms.json \
  --participants 0x8956782345dcBA12345:data_provider,0x9876543210fedcba:data_processor \
  --verify
```

## Agreement Lifecycle

Agreements go through several phases during their lifecycle:

1. **Creation**: Agreement is defined and deployed
2. **Approval**: Participants approve agreement terms
3. **Activation**: Agreement becomes active and enforceable
4. **Execution**: Operations are performed under agreement terms
5. **Termination**: Agreement ends through completion or cancelation

```python
# Approve an agreement
sdk.approve_agreement(agreement_id, participant_address="0x8956782345dcBA12345")

# Activate an agreement (typically automatic after all approvals)
sdk.activate_agreement(agreement_id)

# Execute an operation under the agreement
operation_result = sdk.execute_agreement_operation(
    agreement_id=agreement_id,
    operation="read",
    resource_id="customer_dataset_123",
    executor="0x9876543210fedcba"
)

# Terminate an agreement
sdk.terminate_agreement(
    agreement_id=agreement_id,
    reason="Agreement completed successfully"
)
```

## Agreement Templates

The SDK provides common agreement templates for quick implementation:

```python
# Create an agreement from template
data_sharing_agreement = sdk.create_agreement_from_template(
    template="data_sharing",
    name="genomic-data-sharing",
    participants=[
        {"address": "0x8956782345dcBA12345", "role": "provider"},
        {"address": "0x9876543210fedcba", "role": "consumer"}
    ],
    assets=["genomic_dataset_456"],
    customization={
        "access_duration": 30,  # days
        "permitted_uses": ["research", "non_commercial"]
    }
)
```

Available templates include:
- Data sharing agreements
- Federated learning agreements
- Service level agreements
- Marketplace purchase agreements
- Collaborative research agreements

## Verification and Compliance

Agreements include verification mechanisms:

```python
# Verify agreement compliance
verification = sdk.verify_agreement_compliance(
    agreement_id=agreement_id,
    operation_id=operation_id
)

print(f"Compliance status: {verification['status']}")
print(f"Verification proof: {verification['proof']}")

# Get audit log of agreement
audit_log = sdk.get_agreement_audit_log(agreement_id)
```

## Custom Agreement Logic

For complex agreements, you can define custom logic:

```python
# Define custom rules using Python
custom_rules = """
def validate_data_access(request, context):
    # Only allow access during business hours
    current_hour = context.get_current_hour()
    if current_hour < 9 or current_hour > 17:
        return False, "Access only permitted during business hours (9AM-5PM)"
    
    # Limit data access volume
    if request.data_size_mb > 100:
        return False, "Data request exceeds 100MB limit"
    
    return True, "Access granted"
"""

# Create agreement with custom logic
agreement = sdk.create_agreement(
    name="custom-data-access",
    terms=terms,
    participants=participants,
    custom_rules=custom_rules
)
```

## Agreement Storage and Privacy

Agreement data can be stored with different privacy levels:

```python
# Create private agreement
private_agreement = sdk.create_agreement(
    name="private-research",
    terms=terms,
    participants=participants,
    privacy_level="private",  # Options: public, private, confidential
    encryption={
        "enabled": True,
        "algorithm": "AES-256-GCM",
        "key_management": "participant_keys"
    }
)
```

## Testing Agreements

Before deployment, test agreements with simulations:

```python
# Run agreement simulation
simulation = sdk.simulate_agreement(
    agreement_draft=draft_agreement,
    scenarios=[
        {"name": "normal_access", "operation": "read", "user": "participant_b"},
        {"name": "unauthorized_access", "operation": "write", "user": "participant_b"},
        {"name": "termination", "operation": "terminate", "user": "participant_a"}
    ]
)

# Review simulation results
for result in simulation["results"]:
    print(f"Scenario: {result['scenario']}")
    print(f"Outcome: {result['outcome']}")
    print(f"Details: {result['details']}")
```

## Agreement Management

Manage your agreements with these tools:

```python
# List all agreements
agreements = sdk.list_agreements()

# Get agreement details
details = sdk.get_agreement_details(agreement_id)

# Update agreement terms (requires all parties to re-approve)
updated = sdk.update_agreement(
    agreement_id=agreement_id,
    updated_terms=updated_terms
)

# Track agreement status
status = sdk.get_agreement_status(agreement_id)
print(f"Agreement status: {status['state']}")
print(f"Active since: {status['active_since']}")
print(f"Operations performed: {status['operation_count']}")
```

## Next Steps

- Learn about [Agreement Types](02_agreement_types.md)
- Explore [Creating Custom Agreements](03_custom_agreements.md)
- Set up [Agreement Validation](04_agreement_validation.md)
- Understand [Agreement Compliance & Auditing](05_compliance_auditing.md)
