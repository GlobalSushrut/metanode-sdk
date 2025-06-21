# Agreement Validation and Compliance

This document provides a detailed overview of agreement validation and compliance mechanisms in the MetaNode SDK.

## Introduction to Agreement Validation

Agreement validation ensures that agreements meet required conditions and constraints before acceptance and execution. The MetaNode platform provides robust validation capabilities to ensure agreement integrity and compliance.

## Validation Types

MetaNode supports several types of validation:

1. **Structural Validation**: Ensures agreement schemas conform to expected formats
2. **Logical Validation**: Verifies business rules and constraints are satisfied
3. **Participant Validation**: Confirms participants have proper credentials and permissions
4. **Regulatory Validation**: Ensures agreements comply with applicable regulations
5. **Cryptographic Validation**: Verifies digital signatures and authentication

## Validation Process

### Basic Validation Flow

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Validate an agreement before finalizing
validation_result = sdk.validate_agreement(
    agreement_id="agr-123",
    validation_options={
        "check_structure": True,
        "check_permissions": True,
        "check_signatures": True,
        "verify_on_chain": True
    }
)

# Check validation results
if validation_result["valid"]:
    print("Agreement is valid!")
else:
    print(f"Validation failed: {validation_result['reason']}")
    print(f"Failed checks: {', '.join(validation_result['failed_checks'])}")
    
    # Get detailed validation errors
    for check, error in validation_result["validation_errors"].items():
        print(f"Error in {check}: {error['message']}")
```

### Custom Validators

You can create custom validators for specialized validation requirements:

```python
# Define a custom validator
class DatasetSizeValidator:
    """Validator to ensure dataset size is within agreement limits"""
    
    def __init__(self, max_size_gb=100):
        self.max_size_gb = max_size_gb
    
    def validate(self, agreement):
        from metanode.data import DatasetRegistry
        
        # Extract dataset ID from agreement
        try:
            dataset_id = agreement["terms"]["dataset_id"]
            
            # Get dataset metadata
            dataset_info = DatasetRegistry.get_dataset_info(dataset_id)
            dataset_size_gb = dataset_info["size_bytes"] / (1024 * 1024 * 1024)
            
            # Check if dataset size exceeds limit
            if dataset_size_gb > self.max_size_gb:
                return {
                    "valid": False,
                    "reason": f"Dataset size ({dataset_size_gb:.2f} GB) exceeds maximum allowed size ({self.max_size_gb} GB)"
                }
                
            return {"valid": True}
            
        except KeyError:
            return {
                "valid": False,
                "reason": "Agreement missing required dataset_id field"
            }
        except Exception as e:
            return {
                "valid": False,
                "reason": f"Validation error: {str(e)}"
            }

# Register the custom validator
sdk.register_validator(
    validator=DatasetSizeValidator(max_size_gb=50),
    name="dataset_size_validator"
)

# Use the custom validator
validation_result = sdk.validate_agreement(
    agreement_id="agr-123",
    validators=["dataset_size_validator"]
)
```

## On-chain Validation

MetaNode can validate agreements directly on the blockchain for maximum transparency and security:

```python
# Perform on-chain validation using smart contract validators
onchain_validation = sdk.validate_agreement_on_chain(
    agreement_id="agr-123",
    validation_contract="0x7890def...",  # Address of validation contract
    validation_method="validateAgreementTerms",
    gas_limit=200000
)

# Check validation status
if onchain_validation["valid"]:
    print(f"On-chain validation successful")
    print(f"Transaction hash: {onchain_validation['transaction_hash']}")
    print(f"Block number: {onchain_validation['block_number']}")
else:
    print(f"On-chain validation failed: {onchain_validation['reason']}")
```

## Regulatory Compliance

MetaNode provides tools to ensure agreements comply with relevant regulations:

### Compliance Frameworks

```python
# Check agreement against compliance frameworks
compliance_result = sdk.validate_compliance(
    agreement_id="agr-123",
    frameworks=[
        "gdpr",           # General Data Protection Regulation
        "hipaa",          # Health Insurance Portability and Accountability Act
        "ccpa"            # California Consumer Privacy Act
    ],
    compliance_options={
        "region": "eu",   # Geographical region for compliance check
        "data_type": "personal_health",
        "log_check_results": True,
        "require_all": False  # Agreement passes if any framework validates
    }
)

# Review compliance results
print(f"Overall compliance: {compliance_result['compliant']}")

# Check compliance with specific frameworks
for framework, result in compliance_result["framework_results"].items():
    print(f"{framework}: {'Compliant' if result['compliant'] else 'Non-compliant'}")
    
    if not result["compliant"]:
        print(f"  Issues:")
        for issue in result["issues"]:
            print(f"  - {issue['description']}")
            print(f"    Severity: {issue['severity']}")
            print(f"    Recommendation: {issue['recommendation']}")
```

## Audit Trails

MetaNode automatically generates comprehensive audit trails for agreement validation and compliance checks.

### Retrieving Audit Records

```python
# Get audit trail for an agreement
audit_trail = sdk.get_agreement_audit_trail(
    agreement_id="agr-123",
    time_range={
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-06-21T00:00:00Z"
    },
    event_types=[
        "validation",
        "signature",
        "modification",
        "execution"
    ],
    include_metadata=True
)

# Process audit records
for record in audit_trail["records"]:
    print(f"Event: {record['event_type']} at {record['timestamp']}")
    print(f"Performed by: {record['actor']}")
    print(f"Details: {record['details']}")
    print(f"Verification hash: {record['verification_hash']}")
    print("---")
```

### Exporting Audit Logs

```python
# Export audit trail for compliance reporting
sdk.export_agreement_audit_trail(
    agreement_id="agr-123",
    export_format="pdf",  # Options: pdf, csv, json
    destination="/path/to/audit-report.pdf",
    include_signatures=True,
    include_verification_proofs=True
)
```

## Signature Verification

MetaNode agreements rely on cryptographic signatures that can be independently verified.

### Signature Creation

```python
# Sign an agreement
signature = sdk.sign_agreement(
    agreement_id="agr-123",
    signer_address="0x123abc...",
    signature_type="personal_sign",
    signature_message="I agree to the terms as specified in agreement agr-123",
    include_timestamp=True
)

# Output signature information
print(f"Signature created: {signature['signature_id']}")
print(f"Signature hash: {signature['signature_hash']}")
```

### Signature Verification

```python
# Verify a signature
verification = sdk.verify_agreement_signature(
    agreement_id="agr-123",
    signature_id="sig-456",
    verification_options={
        "check_signer_authority": True,
        "check_timestamp_validity": True,
        "max_signature_age_days": 30
    }
)

if verification["valid"]:
    print("Signature is valid")
    print(f"Signed by: {verification['signer_address']}")
    print(f"Role in agreement: {verification['signer_role']}")
    print(f"Signature timestamp: {verification['timestamp']}")
else:
    print(f"Signature verification failed: {verification['reason']}")
```

## Verification Proofs

MetaNode uses chainlink.lock verification proofs to provide immutable evidence of agreement validity.

```python
# Generate a verification proof for an agreement
proof = sdk.generate_agreement_proof(
    agreement_id="agr-123",
    proof_type="chainlink.lock",
    included_elements=[
        "full_agreement",
        "signatures",
        "validation_results",
        "participant_identities"
    ],
    storage_options={
        "store_on_ipfs": True,
        "store_on_chain": True
    }
)

print(f"Verification proof generated: {proof['proof_id']}")
print(f"Blockchain record: {proof['blockchain_address']}")
print(f"IPFS record: {proof['ipfs_cid']}")
print(f"Verification URL: {proof['verification_url']}")
```

## Best Practices for Validation

### Performance Optimization

1. **Prioritize Validations**: Run critical validations first and fail fast when possible
2. **Caching Strategy**: Cache validation results for frequently used validators
3. **Batch Validations**: Group related validations to minimize blockchain transactions
4. **Optimize Gas Usage**: For on-chain validation, optimize contracts for gas efficiency

### Security Considerations

1. **Defense in Depth**: Apply multiple validation layers for critical agreements
2. **Segregated Validation**: Use separate validation contracts for different agreement types
3. **Regular Auditing**: Periodically review and test validators for accuracy
4. **Access Controls**: Implement proper permissions for validation operations

### Compliance Verification

1. **Regular Updates**: Keep compliance validators updated with regulatory changes
2. **Jurisdiction Awareness**: Apply appropriate compliance rules based on participant locations
3. **Documentation**: Maintain comprehensive validation records for audit purposes
4. **Expert Review**: Periodically have validation logic reviewed by domain experts

## Validation CLI Tools

MetaNode provides command-line tools for agreement validation:

```bash
# Validate an agreement from the command line
metanode-cli agreement validate --id agr-123 --validators base,regulatory,custom

# Check compliance with specific frameworks
metanode-cli agreement compliance --id agr-123 --frameworks gdpr,hipaa --region eu

# Generate a verification proof
metanode-cli agreement proof --id agr-123 --type chainlink.lock --store-on-chain

# Export audit trail
metanode-cli agreement audit --id agr-123 --format pdf --output audit-report.pdf
```

## Conclusion

Robust validation is critical to ensuring agreements in MetaNode are secure, compliant, and enforceable. By leveraging the validation mechanisms described in this document, you can create agreements that maintain integrity throughout their lifecycle and provide verifiable proof of their conditions and execution.
