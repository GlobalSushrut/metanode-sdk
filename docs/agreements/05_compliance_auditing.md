# Agreement Compliance and Auditing

This document covers compliance monitoring, audit capabilities, and verification mechanisms for MetaNode agreements.

## Introduction to Compliance and Auditing

MetaNode provides comprehensive tools for monitoring agreement compliance and generating audit trails. These capabilities help ensure data governance, regulatory compliance, and operational transparency.

## Compliance Monitoring

### Real-time Compliance Checks

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Monitor agreement compliance in real-time
monitoring_handle = sdk.monitor_agreement_compliance(
    agreement_id="agr-123",
    monitoring_options={
        "check_interval_seconds": 300,  # Check every 5 minutes
        "alert_on_violation": True,
        "monitored_conditions": [
            "access_permissions",
            "data_usage_limits",
            "participant_roles"
        ]
    }
)

# Set up compliance event handlers
def on_compliance_violation(event):
    violation = event["violation"]
    print(f"Compliance violation detected at {event['timestamp']}")
    print(f"Condition violated: {violation['condition_name']}")
    print(f"Severity: {violation['severity']}")
    print(f"Details: {violation['details']}")
    
    # Take remedial action
    if violation["severity"] == "critical":
        sdk.suspend_agreement(agreement_id="agr-123", reason=violation["details"])

# Register the event handler
monitoring_handle.on_violation(on_compliance_violation)

# Start monitoring
monitoring_handle.start()

# Later, when monitoring is no longer needed
monitoring_handle.stop()
```

### Scheduled Compliance Reports

```python
# Schedule regular compliance reports
sdk.schedule_compliance_report(
    agreement_id="agr-123",
    schedule={
        "frequency": "weekly",
        "day_of_week": "monday",
        "time": "00:00",
        "timezone": "UTC"
    },
    report_format="pdf",
    delivery_options={
        "email": ["compliance@example.com"],
        "store_in_system": True,
        "retention_period_days": 90
    }
)
```

## Audit Trail Management

### Comprehensive Audit Records

MetaNode automatically generates audit records for all agreement-related activities:

```python
# Get complete audit trail for an agreement
audit_trail = sdk.get_audit_trail(
    agreement_id="agr-123",
    time_range={
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-06-21T00:00:00Z"
    },
    include_events=[
        "creation",
        "modification",
        "signature",
        "validation",
        "execution",
        "termination",
        "data_access",
        "compliance_check"
    ],
    detailed=True
)

# Process audit records
for record in audit_trail["records"]:
    print(f"Event: {record['event_type']} at {record['timestamp']}")
    print(f"Actor: {record['actor']}")
    print(f"Details: {record['details']}")
    print(f"Verification: {record['verification_hash']}")
    print("---")
```

### Immutable Audit Storage

MetaNode ensures audit records are tamper-proof:

```python
# Store audit trail with cryptographic verification
verification_record = sdk.store_audit_trail(
    audit_trail_id="audit-123",
    storage_options={
        "use_chainlink_lock": True,
        "store_on_ipfs": True,
        "generate_pdf": True
    }
)

print(f"Audit trail stored with verification proof: {verification_record['proof_id']}")
print(f"Verification URL: {verification_record['verification_url']}")
print(f"IPFS CID: {verification_record['ipfs_cid']}")
```

## Verification and Proof Systems

### Agreement Verification

```python
# Verify an agreement's current state
verification = sdk.verify_agreement(
    agreement_id="agr-123",
    verification_options={
        "check_signatures": True,
        "check_blockchain_state": True,
        "check_execution_status": True,
        "check_compliance_status": True
    }
)

if verification["verified"]:
    print("Agreement verification successful")
    print(f"Status: {verification['status']}")
    print(f"Active participants: {verification['active_participants']}")
    print(f"Last updated: {verification['last_updated']}")
else:
    print(f"Agreement verification failed: {verification['reason']}")
```

### Chainlink.lock Integration

MetaNode uses Chainlink.lock for cryptographic verification of agreements:

```python
# Generate a chainlink.lock verification proof
proof = sdk.generate_chainlink_proof(
    agreement_id="agr-123",
    proof_options={
        "include_full_agreement": True,
        "include_signatures": True,
        "include_audit_events": True
    }
)

# Verify a chainlink.lock proof
verification = sdk.verify_chainlink_proof(
    proof_id=proof["proof_id"],
    verification_options={
        "check_blockchain_record": True,
        "check_ipfs_record": True
    }
)

if verification["valid"]:
    print("Chainlink.lock proof is valid")
    print(f"Blockchain transaction: {verification['blockchain_tx']}")
    print(f"Recorded at block: {verification['block_number']}")
    print(f"Timestamp: {verification['timestamp']}")
else:
    print(f"Proof verification failed: {verification['reason']}")
```

## CLI Tools for Compliance and Auditing

```bash
# Generate a compliance report
metanode-cli agreement compliance-report --id agr-123 --format pdf --output report.pdf

# View audit trail
metanode-cli agreement audit --id agr-123 --from 2025-01-01 --to 2025-06-21

# Generate verification proof
metanode-cli agreement verify --id agr-123 --generate-proof --store-on-chain

# Validate a chainlink.lock proof
metanode-cli verify chainlink-proof --proof-id prf-789 --verbose
```

## Best Practices

### Compliance Monitoring

1. **Continuous Verification**: Set up real-time compliance monitoring for critical agreements
2. **Proactive Alerts**: Configure alerting for potential compliance issues before violations occur
3. **Regular Reviews**: Schedule periodic compliance reviews, especially for long-running agreements
4. **Escalation Procedures**: Define clear procedures for handling compliance violations

### Audit Trails

1. **Comprehensive Recording**: Capture all relevant events throughout the agreement lifecycle
2. **Immutable Storage**: Always store audit trails using blockchain-based verification
3. **Access Controls**: Implement proper access restrictions for audit information
4. **Retention Policies**: Define and enforce appropriate retention periods for audit data

### Verification Proofs

1. **Critical Transactions**: Generate verification proofs for all critical agreement operations
2. **Third-party Verification**: Enable independent verification of agreement state and history
3. **Proof Storage**: Store verification proofs both on-chain and in distributed storage (IPFS)
4. **Periodic Re-verification**: Periodically re-verify long-term agreements to ensure ongoing validity

## Conclusion

MetaNode's comprehensive compliance, auditing, and verification capabilities ensure transparent, accountable, and verifiable agreement management. By implementing the practices described in this document, you can establish a robust governance framework for your agreements while maintaining cryptographic proof of compliance.
