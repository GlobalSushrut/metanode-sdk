# Agreement Types

This document explores the different types of agreements available in the MetaNode SDK, their specific features, and usage patterns.

## Overview of Agreement Types

MetaNode supports several agreement types, each designed for specific use cases:

| Agreement Type | Purpose | Key Features |
|---------------|---------|--------------|
| Data Sharing | Control data access between parties | Access control, usage tracking, data lineage |
| Compute | Manage distributed computing tasks | Resource allocation, compute verification, result integrity |
| Service Level | Define service commitments | Performance metrics, uptime guarantees, penalty clauses |
| Resource Exchange | Facilitate sharing of digital assets | Resource tracking, delivery verification, access control |
| Collaborative | Enable multi-party collaboration | Role-based permissions, shared resources, joint ownership |
| Regulatory | Ensure regulatory compliance | Audit trails, compliance verification, reporting |

## Data Sharing Agreements

Data sharing agreements enable controlled access to data assets with verifiable terms.

### Features

- Fine-grained access control
- Usage tracking and reporting
- Data lineage preservation
- Privacy-preserving options
- Revocation capabilities

### Implementation

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Create a data sharing agreement
data_agreement = sdk.create_data_sharing_agreement(
    name="clinical-dataset-sharing",
    provider={"address": "0x123abc...", "identity": "hospital_research_dept"},
    consumer={"address": "0x456def...", "identity": "pharmaceutical_research"},
    dataset_id="clinical_trials_2024_q2",
    terms={
        "access_duration": 90,  # days
        "allowed_operations": ["read", "query", "analyze"],
        "prohibited_operations": ["download", "distribute", "modify"],
        "purpose_limitation": "cancer research only",
        "anonymization_required": True,
        "deletion_required": True
    },
    resource_limits={
        "max_queries_per_day": 1000,
        "max_concurrent_connections": 5,
        "access_schedule": "weekdays-only"
    }
)

print(f"Data sharing agreement created: {data_agreement['id']}")
```

### CLI Usage

```bash
metanode-cli agreement create-data-sharing \
  --name "clinical-dataset-sharing" \
  --provider 0x123abc...:hospital_research_dept \
  --consumer 0x456def...:pharmaceutical_research \
  --dataset clinical_trials_2024_q2 \
  --terms-file ./data_sharing_terms.json
```

## Compute Agreements

Compute agreements manage distributed computation across nodes with resource allocation and verification.

### Features

- Resource allocation and pricing
- Computation verification
- Result integrity assurance
- Privacy-preserving computation
- Federated machine learning support

### Implementation

```python
# Create a compute agreement
compute_agreement = sdk.create_compute_agreement(
    name="distributed-genomic-analysis",
    data_provider={"address": "0x123abc...", "identity": "genomic_data_center"},
    compute_provider={"address": "0x789ghi...", "identity": "cloud_compute_provider"},
    algorithm_provider={"address": "0x456def...", "identity": "research_institution"},
    compute_terms={
        "algorithm_hash": "sha256:8a7b8ef9c82a4d2f6e29c36f5e170dbd640",
        "max_compute_time": 3600,  # seconds
        "max_memory": 16,  # GB
        "gpu_required": True,
        "input_data_access": "query_only",  # no raw data access
        "result_sharing": ["algorithm_provider", "data_provider"]
    },
    resource_allocation={
        "max_compute_time": 24,  # hours
        "priority_level": "standard",
        "resource_quota": "dedicated-3-cpu-8gb-ram"
    }
)
```

## Service Level Agreements

Service Level Agreements (SLAs) define performance metrics and guarantees for node operation and API access.

### Features

- Performance monitoring
- Uptime guarantees
- Response time thresholds
- Penalty conditions
- Automatic enforcement

### Implementation

```python
# Create a service level agreement
sla = sdk.create_service_level_agreement(
    name="high-availability-blockchain-api",
    provider={"address": "0x123abc...", "identity": "metanode_infrastructure_provider"},
    consumer={"address": "0x456def...", "identity": "dapp_developer"},
    service_metrics={
        "uptime": 99.9,  # percentage
        "response_time": 500,  # milliseconds
        "throughput": 1000,  # requests per second
        "error_rate": 0.1  # percentage
    },
    monitoring={
        "interval": 60,  # seconds between checks
        "method": "heartbeat",
        "endpoints": ["https://api.example.com/health"]
    },
    remediation={
        "uptime_violation": {
            "threshold": 99.5,  # percentage
            "action": "automatic_failover",
            "notification": "immediate_alert"
        },
        "response_time_violation": {
            "threshold": 1000,  # milliseconds
            "action": "throttle_requests"
        }
    }
)
```

## Resource Exchange Agreements

Resource exchange agreements facilitate the sharing of digital assets between parties on the MetaNode platform.

### Features

- Access control
- Delivery verification
- Dispute resolution
- Quality assurance
- Multi-stage transfers

### Implementation

```python
# Create a resource exchange agreement
resource_exchange = sdk.create_resource_exchange_agreement(
    name="algorithm-sharing",
    provider={"address": "0x123abc...", "identity": "algorithm_developer"},
    consumer={"address": "0x456def...", "identity": "research_lab"},
    resource={
        "id": "algo-123",
        "name": "Advanced Clustering Algorithm",
        "type": "algorithm",
        "description": "State-of-art clustering algorithm for genomic data",
        "hash": "sha256:d7a8fbb307d7809469c9",
        "preview_url": "https://repository.example.com/preview/algo-123"
    },
    transfer_terms={
        "access_level": "execution_only",
        "transfer_verification": True,
        "success_conditions": ["successful_execution", "consumer_approval"],
        "access_period": 30,  # days
        "delivery_method": "ipfs",
        "usage_restrictions": "research_purposes_only"
    }
)
```

## Collaborative Agreements

Collaborative agreements enable multiple parties to work together with defined roles and responsibilities.

### Features

- Multi-party signatures
- Role-based permissions
- Shared resource management
- Output ownership rules
- Contribution tracking

### Implementation

```python
# Create a collaborative agreement
collaborative_agreement = sdk.create_collaborative_agreement(
    name="multi-institution-research",
    participants=[
        {"address": "0x123abc...", "identity": "university_a", "role": "data_provider"},
        {"address": "0x456def...", "identity": "university_b", "role": "algorithm_provider"},
        {"address": "0x789ghi...", "identity": "research_institute", "role": "compute_provider"},
        {"address": "0xabc123...", "identity": "funding_agency", "role": "observer"}
    ],
    resources={
        "datasets": ["patient_records_anonymized", "control_group_data"],
        "algorithms": ["genomic_analysis_v2", "statistical_model_k3"],
        "compute_resources": ["gpu_cluster", "secure_enclave"]
    },
    contribution_weights={
        "university_a": 0.4,
        "university_b": 0.4,
        "research_institute": 0.2
    },
    output_rights={
        "publication": "joint_approval_required",
        "commercialization": "profit_sharing_per_weights",
        "intellectual_property": "joint_ownership"
    },
    governance={
        "decision_making": "majority_vote",
        "dispute_resolution": "arbitration_by_funding_agency",
        "termination_conditions": ["mutual_agreement", "deadline_expiration"]
    }
)
```

## Regulatory Agreements

Regulatory agreements ensure compliance with legal and governance requirements.

### Features

- Audit trails
- Regulatory reporting
- Compliance verification
- Jurisdictional rules
- Data sovereignty

### Implementation

```python
# Create a regulatory compliance agreement
regulatory_agreement = sdk.create_regulatory_agreement(
    name="hipaa-compliance-health-data",
    data_custodian={"address": "0x123abc...", "identity": "hospital_system"},
    data_processor={"address": "0x456def...", "identity": "analytics_provider"},
    regulatory_framework="HIPAA",
    compliance_requirements={
        "data_encryption": "AES-256",
        "access_controls": "role_based",
        "audit_logging": "all_access_events",
        "retention_period": 365,  # days
        "breach_notification": True,
        "geographic_restrictions": ["US-only"],
        "right_to_erasure": True
    },
    verification_process={
        "audit_frequency": 90,  # days
        "audit_provider": "independent_third_party",
        "documentation_required": ["access_logs", "encryption_certificates", "staff_training"],
        "reporting_schedule": "quarterly"
    }
)
```

## Custom Agreement Types

You can create custom agreement types for specialized needs:

```python
# Define a custom agreement template
custom_template = {
    "name": "data_collaboration",
    "schema": {
        "data_provider": {"type": "participant", "required": True},
        "data_consumer": {"type": "participant", "required": True},
        "data_volume": {"type": "number", "required": True},
        "access_frequency": {"type": "number", "required": True},
        "access_schedule": {"type": "string", "required": True},
        "anonymization_required": {"type": "boolean", "default": True}
    },
    "rules": [
        "provider_must_verify_data_quality",
        "consumer_must_report_usage",
        "minimum_request_interval: 60"
    ],
    "execution_logic": "data_access_logic.py"
}

# Register the custom template
sdk.register_agreement_template(
    template_definition=custom_template,
    template_id="energy_trading"
)

# Create an agreement using the custom template
data_collaboration_agreement = sdk.create_agreement_from_template(
    template="data_collaboration",
    name="research-data-sharing",
    params={
        "data_provider": {"address": "0x123abc...", "identity": "research_institute_a"},
        "data_consumer": {"address": "0x456def...", "identity": "university_lab_b"},
        "data_volume": 500,  # GB
        "access_frequency": 24,  # hours
        "access_schedule": "daily:0800-1700",
        "anonymization_required": True
    }
)
```

## Hybrid Agreements

Combine multiple agreement types for complex use cases:

```python
# Create a hybrid agreement combining data sharing and compute
hybrid_agreement = sdk.create_hybrid_agreement(
    name="secure-federated-learning",
    agreement_types=["data_sharing", "compute"],
    participants=[
        {"address": "0x123abc...", "identity": "hospital_a", "role": "data_provider"},
        {"address": "0x456def...", "identity": "hospital_b", "role": "data_provider"},
        {"address": "0x789ghi...", "identity": "research_lab", "role": "algorithm_provider"},
        {"address": "0xabc123...", "identity": "tech_company", "role": "compute_provider"}
    ],
    data_sharing_terms={
        "access_type": "federated_only",
        "no_raw_data_exposure": True
    },
    compute_terms={
        "algorithm_hash": "sha256:8a7b8ef9c82a4d2f",
        "federated_learning_protocol": "secure_aggregation",
        "local_computation_only": True
    },
    output_terms={
        "model_access": ["all_participants"],
        "model_ownership": "joint"
    }
)
```

## Agreement Selection Guide

When choosing an agreement type, consider:

1. **Data Sensitivity**: Higher sensitivity requires stronger access controls and verification
2. **Number of Parties**: More parties may require collaborative agreements
3. **Resource Requirements**: Intensive computation needs compute agreements
4. **Resource Sharing Context**: Resource exchange agreements for digital asset sharing
5. **Regulatory Environment**: Regulatory agreements for compliance
6. **Performance Requirements**: SLAs for guaranteed service levels

## Next Steps

- Explore [Creating Custom Agreements](03_custom_agreements.md)
- Set up [Agreement Validation](04_agreement_validation.md)
- Understand [Agreement Compliance & Auditing](05_compliance_auditing.md)
