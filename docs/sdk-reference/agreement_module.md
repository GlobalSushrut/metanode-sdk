# MetaNode SDK: Agreement Module Reference

This document provides a comprehensive API reference for the Agreement module within the MetaNode SDK.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Core Classes](#core-classes)
- [Agreement Creation](#agreement-creation)
- [Agreement Management](#agreement-management)
- [Agreement Validation](#agreement-validation)
- [Verification Proofs](#verification-proofs)
- [Compliance and Auditing](#compliance-and-auditing)
- [Error Handling](#error-handling)

## Overview

The Agreement module provides tools for creating, managing, validating, and enforcing blockchain-based agreements in MetaNode. It connects directly to the MetaNode blockchain infrastructure and supports both on-chain and off-chain agreement functionality.

## Installation

```bash
pip install metanode-sdk
```

## Core Classes

### MetaNodeSDK

The main entry point for the SDK.

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize with default settings
sdk = MetaNodeSDK()

# Initialize with custom settings
sdk = MetaNodeSDK(
    config_path="/path/to/config.yaml",  # Optional
    env="testnet",                       # Optional: testnet, production
    log_level="info"                     # Optional: debug, info, warning, error
)
```

### AgreementManager

The primary class for working with agreements.

```python
# Access through the SDK
agreement_manager = sdk.agreement

# Or import directly if needed
from metanode.agreements import AgreementManager
agreement_manager = AgreementManager()
```

## Agreement Creation

### create_agreement

Creates a new agreement with specified parameters.

```python
agreement = sdk.create_agreement(
    name="sample-agreement",                     # Required: Name of the agreement
    agreement_type="data_sharing",               # Required: Type of agreement
    schema_id="data_sharing_v1",                 # Optional: Use custom schema
    participants=[                               # Required: List of participants
        {"address": "0x123...", "role": "provider"},
        {"address": "0x456...", "role": "consumer"}
    ],
    terms={                                      # Required: Agreement terms
        "dataset_id": "dataset-123",
        "access_level": "read_only",
        "access_duration": 30  # days
    },
    resource_limits={                            # Optional: Resource limitations
        "max_queries_per_day": 1000,
        "max_concurrent_connections": 5
    },
    metadata={                                   # Optional: Additional metadata
        "industry": "healthcare",
        "compliance": "hipaa"
    }
)

# Access agreement ID and other properties
agreement_id = agreement["id"]
print(f"Agreement created with ID: {agreement_id}")
print(f"Status: {agreement['status']}")
```

### register_agreement_schema

Registers a custom schema for agreements.

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
        },
        "start_date": {"type": "string", "format": "date"},
        "end_date": {"type": "string", "format": "date"}
    }
}

schema_id = sdk.register_agreement_schema(
    schema=schema,                     # Required: JSON Schema
    schema_id="research_collab_v1",    # Optional: Custom ID, auto-generated if not provided
    description="Research collaboration agreement schema" # Optional
)

print(f"Schema registered with ID: {schema_id}")
```

### create_agreement_from_template

Creates an agreement from a pre-defined template.

```python
agreement = sdk.create_agreement_from_template(
    template_id="data_sharing_template_v1",  # Required: Template ID
    name="genomics-data-sharing",            # Required: Agreement name
    participants=[                           # Required: Participants
        {"address": "0x123...", "role": "provider"},
        {"address": "0x456...", "role": "consumer"}
    ],
    template_parameters={                    # Required: Template-specific parameters
        "dataset_id": "genomic-dataset-123",
        "access_level": "read_only",
        "access_duration": 90  # days
    }
)

print(f"Agreement created from template with ID: {agreement['id']}")
```

## Agreement Management

### get_agreement

Retrieves an existing agreement by ID.

```python
agreement = sdk.get_agreement(
    agreement_id="agr-123",            # Required: Agreement ID
    include_history=True,              # Optional: Include state changes
    include_signatures=True            # Optional: Include signature details
)

print(f"Agreement name: {agreement['name']}")
print(f"Status: {agreement['status']}")
print(f"Created: {agreement['created_at']}")
```

### list_agreements

Lists agreements based on specified filters.

```python
agreements = sdk.list_agreements(
    status=["active", "pending"],      # Optional: Filter by status
    type="data_sharing",               # Optional: Filter by type
    participant_address="0x123...",    # Optional: Filter by participant
    limit=10,                          # Optional: Pagination limit
    offset=0                           # Optional: Pagination offset
)

print(f"Found {len(agreements)} agreements")
for agreement in agreements:
    print(f"ID: {agreement['id']}, Name: {agreement['name']}")
```

### update_agreement

Updates an existing agreement.

```python
updated = sdk.update_agreement(
    agreement_id="agr-123",            # Required: Agreement ID
    terms={                            # Optional: Updated terms
        "access_duration": 60  # days
    },
    resource_limits={                  # Optional: Updated resource limits
        "max_queries_per_day": 2000
    },
    metadata={                         # Optional: Updated metadata
        "updated_by": "admin"
    }
)

print(f"Agreement updated: {updated['status']}")
```

### sign_agreement

Signs an agreement to indicate acceptance.

```python
signature = sdk.sign_agreement(
    agreement_id="agr-123",            # Required: Agreement ID
    signer_address="0x123...",         # Required: Signer's address
    signature_type="personal_sign",    # Optional: Signature type
    signature_message="I agree to the terms"  # Optional: Custom message
)

print(f"Agreement signed with signature ID: {signature['signature_id']}")
```

### finalize_agreement

Finalizes an agreement after all required signatures are collected.

```python
finalized = sdk.finalize_agreement(
    agreement_id="agr-123",            # Required: Agreement ID
    deploy_on_chain=True               # Optional: Deploy to blockchain
)

print(f"Agreement finalized: {finalized['status']}")
print(f"On-chain address: {finalized['blockchain_address']}")
```

### terminate_agreement

Terminates an active agreement.

```python
terminated = sdk.terminate_agreement(
    agreement_id="agr-123",            # Required: Agreement ID
    reason="All terms fulfilled",      # Optional: Termination reason
    termination_date="2025-12-31"      # Optional: Specific termination date
)

print(f"Agreement terminated: {terminated['status']}")
```

## Agreement Validation

### validate_agreement

Validates an agreement against rules and schemas.

```python
validation = sdk.validate_agreement(
    agreement_id="agr-123",            # Required: Agreement ID
    validation_options={               # Optional: Validation options
        "check_structure": True,
        "check_permissions": True,
        "check_signatures": True,
        "check_on_chain": True
    }
)

if validation["valid"]:
    print("Agreement is valid")
else:
    print(f"Validation failed: {validation['reason']}")
    for error in validation["validation_errors"]:
        print(f"- {error['message']}")
```

### register_validator

Registers a custom validator for agreements.

```python
# Define a custom validator function
def custom_validator(agreement):
    if "special_terms" not in agreement["terms"]:
        return {
            "valid": False,
            "reason": "Missing special terms",
            "severity": "error"
        }
    return {"valid": True}

# Register the validator
validator_id = sdk.register_validator(
    validator_function=custom_validator,   # Required: Validator function
    validator_id="special_terms_validator", # Optional: Custom ID
    description="Validates special terms",  # Optional: Description
    applicable_types=["custom_agreement"]   # Optional: Agreement types
)

print(f"Validator registered with ID: {validator_id}")
```

### compliance_check

Checks an agreement for compliance with regulatory frameworks.

```python
compliance = sdk.compliance_check(
    agreement_id="agr-123",              # Required: Agreement ID
    frameworks=["gdpr", "hipaa"],        # Required: Compliance frameworks
    region="eu"                          # Optional: Regional context
)

print(f"Compliance check result: {compliance['compliant']}")
if not compliance["compliant"]:
    for issue in compliance["issues"]:
        print(f"- {issue['description']}")
        print(f"  Severity: {issue['severity']}")
        print(f"  Recommendation: {issue['recommendation']}")
```

## Verification Proofs

### generate_verification_proof

Generates a cryptographic proof for an agreement.

```python
proof = sdk.generate_verification_proof(
    agreement_id="agr-123",              # Required: Agreement ID
    verification_type="chainlink.lock",  # Required: Type of verification
    proof_parameters={                   # Optional: Proof parameters
        "include_signatures": True,
        "include_terms": True,
        "hash_algorithm": "keccak256"
    },
    storage_options={                    # Optional: Storage options
        "store_on_ipfs": True,
        "store_on_chain": True
    }
)

print(f"Verification proof generated: {proof['proof_id']}")
print(f"Blockchain record: {proof['blockchain_address']}")
print(f"IPFS record: {proof['ipfs_cid']}")
```

### validate_verification_proof

Validates a previously generated verification proof.

```python
validation = sdk.validate_verification_proof(
    proof_id="prf-789",                 # Required: Proof ID
    validation_options={                # Optional: Validation options
        "check_blockchain_record": True,
        "check_ipfs_record": True,
        "check_signatures": True
    }
)

if validation["valid"]:
    print("Proof is valid!")
    print(f"Recorded on blockchain at: {validation['blockchain_record']}")
else:
    print(f"Proof validation failed: {validation['reason']}")
```

## Compliance and Auditing

### get_agreement_audit_trail

Retrieves the audit trail for an agreement.

```python
audit_trail = sdk.get_agreement_audit_trail(
    agreement_id="agr-123",              # Required: Agreement ID
    time_range={                         # Optional: Time range
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-06-21T00:00:00Z"
    },
    event_types=[                        # Optional: Event types
        "validation",
        "signature",
        "modification",
        "execution"
    ],
    include_metadata=True                # Optional: Include metadata
)

print(f"Found {len(audit_trail['records'])} audit records")
for record in audit_trail["records"]:
    print(f"Event: {record['event_type']} at {record['timestamp']}")
    print(f"Performed by: {record['actor']}")
    print(f"Details: {record['details']}")
```

### export_agreement_audit_trail

Exports the audit trail for an agreement.

```python
export_result = sdk.export_agreement_audit_trail(
    agreement_id="agr-123",              # Required: Agreement ID
    export_format="pdf",                 # Required: Format (pdf, csv, json)
    destination="/path/to/audit-report.pdf", # Required: Output path
    include_signatures=True,             # Optional: Include signatures
    include_verification_proofs=True     # Optional: Include verification proofs
)

print(f"Audit trail exported to: {export_result['export_path']}")
```

### monitor_agreement_compliance

Sets up real-time compliance monitoring for an agreement.

```python
monitoring_handle = sdk.monitor_agreement_compliance(
    agreement_id="agr-123",              # Required: Agreement ID
    monitoring_options={                 # Optional: Monitoring options
        "check_interval_seconds": 300,   # Check every 5 minutes
        "alert_on_violation": True,
        "monitored_conditions": [
            "access_permissions",
            "data_usage_limits",
            "participant_roles"
        ]
    }
)

# Set up a violation handler
def on_compliance_violation(event):
    violation = event["violation"]
    print(f"Compliance violation detected at {event['timestamp']}")
    print(f"Condition violated: {violation['condition_name']}")
    print(f"Severity: {violation['severity']}")
    print(f"Details: {violation['details']}")

# Register the handler and start monitoring
monitoring_handle.on_violation(on_compliance_violation)
monitoring_handle.start()
```

## Error Handling

The SDK uses a consistent error handling pattern:

```python
from metanode.exceptions import (
    AgreementValidationError,
    AgreementCreationError,
    BlockchainConnectionError,
    ValidationError
)

try:
    # SDK operations
    agreement = sdk.create_agreement(...)
except AgreementValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Validation details: {e.details}")
except AgreementCreationError as e:
    print(f"Creation error: {e.message}")
except BlockchainConnectionError as e:
    print(f"Blockchain connection error: {e.message}")
    print(f"RPC URL: {e.rpc_url}")
except ValidationError as e:
    print(f"General validation error: {e.message}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Conclusion

This reference covers the core functionality of the MetaNode SDK Agreement module. For more detailed information on specific use cases, refer to the tutorial documents:

- [Complete Workflow](/docs/tutorials/01_complete_workflow.md)
- [Testnet Connection](/docs/tutorials/02_testnet_connection.md)
- [Production Migration](/docs/tutorials/03_production_migration.md)
