# MetaNode: Migration to Production

This guide outlines the step-by-step process for migrating MetaNode applications and infrastructure from testnet to production environments.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Prerequisites](#2-prerequisites)
3. [Planning Your Migration](#3-planning-your-migration)
4. [Infrastructure Setup](#4-infrastructure-setup)
5. [SDK Configuration](#5-sdk-configuration)
6. [Agreement Migration](#6-agreement-migration)
7. [Verification and Validation](#7-verification-and-validation)
8. [Monitoring and Operations](#8-monitoring-and-operations)
9. [Security Best Practices](#9-security-best-practices)
10. [Troubleshooting](#10-troubleshooting)

## 1. Introduction

Moving from MetaNode's testnet to production requires careful planning and execution. This guide covers all necessary steps to ensure a smooth transition while maintaining security, reliability, and performance.

## 2. Prerequisites

Before beginning the migration process, ensure you have:

- Successfully tested your application on the MetaNode testnet
- Access to production infrastructure (cloud provider or on-premises)
- Production-ready security credentials and wallets
- Backup strategy for critical data
- Migration plan approved by stakeholders

## 3. Planning Your Migration

### Assessment Phase

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Get test environment inventory
test_inventory = sdk.get_environment_inventory(env="testnet")

# Generate migration plan
migration_plan = sdk.generate_migration_plan(
    source_env="testnet",
    target_env="production",
    inventory=test_inventory,
    migration_options={
        "data_migration": True,
        "agreement_migration": True,
        "infrastructure_migration": True,
        "parallel_operation_period_days": 7
    }
)

# Save migration plan
with open("migration_plan.json", "w") as f:
    import json
    json.dump(migration_plan, f, indent=2)

print("Migration plan generated successfully")
```

### Creating a Migration Checklist

```bash
# Generate migration checklist via CLI
metanode-cli migration create-checklist \
  --source testnet \
  --target production \
  --output migration_checklist.md

# View the checklist
cat migration_checklist.md
```

## 4. Infrastructure Setup

### Production Infrastructure Deployment

```python
# Deploy production infrastructure
production_deployment = sdk.deploy_infrastructure(
    deployment_name="production-metanode",
    components=["blockchain", "validator", "agreement", "ipfs"],
    deployment_options={
        "environment": "production",
        "container_technology": "kubernetes",  # For production, Kubernetes is recommended
        "high_availability": True,
        "resource_limits": {
            "cpu": 8,
            "memory": "16Gi",
            "storage": "500Gi"
        },
        "security_options": {
            "encrypted_storage": True,
            "network_isolation": True,
            "rbac_enabled": True,
            "secrets_management": "vault"
        }
    }
)

print(f"Production infrastructure deployment started: {production_deployment['deployment_id']}")

# Check deployment status
import time
max_wait_time = 600  # 10 minutes
interval = 30  # seconds
elapsed_time = 0

while elapsed_time < max_wait_time:
    status = sdk.check_deployment_status(production_deployment["deployment_id"])
    print(f"Deployment status: {status['status']}")
    
    if status['status'] == 'complete':
        break
    
    time.sleep(interval)
    elapsed_time += interval

# Get infrastructure details
infrastructure = sdk.get_infrastructure_details(
    deployment_id=production_deployment["deployment_id"]
)

print(f"Access URL: {infrastructure['access_url']}")
print(f"API Endpoint: {infrastructure['api_endpoint']}")
print(f"RPC URL: {infrastructure['rpc_url']}")
```

### Using CLI for Infrastructure Deployment

```bash
# Deploy production infrastructure via CLI
metanode-cli infrastructure deploy \
  --name production-metanode \
  --components blockchain,validator,agreement,ipfs \
  --environment production \
  --container-technology kubernetes \
  --high-availability true \
  --encrypted-storage true

# Check deployment status
metanode-cli infrastructure status --deployment-id <deployment_id>
```

## 5. SDK Configuration

### Configuring SDK for Production

```python
# Configure SDK for production
production_sdk = MetaNodeSDK(
    config_path="/path/to/production_config.yaml",
    env="production",
    log_level="info"
)

# Test connection to production environment
status = production_sdk.check_status()
if status["connected"]:
    print("Successfully connected to production environment")
    print(f"API version: {status['api_version']}")
else:
    print(f"Connection failed: {status['error']}")
```

### Setting Up Production Config

```python
# Create production configuration
production_config = {
    "environment": "production",
    "api_endpoint": infrastructure["api_endpoint"],
    "rpc_url": infrastructure["rpc_url"],
    "ws_url": infrastructure["ws_url"],
    "ipfs_gateway": infrastructure["ipfs_gateway"],
    "log_level": "info",
    "security": {
        "encryption_enabled": True,
        "signature_verification_required": True,
        "mfa_required": True
    }
}

# Save production configuration
production_sdk.save_configuration(
    config=production_config,
    file_path="/path/to/production_config.yaml"
)
```

## 6. Agreement Migration

### Exporting Agreements from Testnet

```python
# List agreements from testnet
testnet_agreements = sdk.list_agreements()
print(f"Found {len(testnet_agreements)} agreements on testnet")

# Export agreements for migration
export_results = sdk.export_agreements_for_migration(
    agreement_ids=[agreement["id"] for agreement in testnet_agreements],
    export_options={
        "include_history": True,
        "include_signatures": True,
        "include_verification_proofs": True
    }
)

print(f"Exported {len(export_results['exported_agreements'])} agreements")
print(f"Export file: {export_results['export_file']}")
```

### Importing Agreements to Production

```python
# Import agreements to production
import_results = production_sdk.import_agreements_from_migration(
    import_file=export_results["export_file"],
    import_options={
        "create_new_ids": True,
        "validate_before_import": True,
        "update_participants": True
    }
)

print(f"Successfully imported {len(import_results['imported_agreements'])} agreements")
print("Agreement ID mapping:")
for old_id, new_id in import_results["id_mapping"].items():
    print(f"  {old_id} -> {new_id}")

# Verify imported agreements
for agreement_id in import_results["imported_agreements"]:
    agreement = production_sdk.get_agreement(agreement_id)
    print(f"Agreement {agreement_id} successfully imported")
    print(f"Status: {agreement['status']}")
```

## 7. Verification and Validation

### Validating Production Deployment

```python
# Validate production environment
validation_result = production_sdk.validate_environment(
    validation_checks=[
        "infrastructure",
        "connectivity",
        "security",
        "performance"
    ]
)

print("Validation results:")
for check, result in validation_result["checks"].items():
    status = "PASSED" if result["passed"] else "FAILED"
    print(f"{check}: {status}")
    if not result["passed"]:
        print(f"  Error: {result['error']}")
        print(f"  Recommendation: {result['recommendation']}")
```

### Running Integration Tests

```python
# Run comprehensive integration tests
test_results = production_sdk.run_integration_tests(
    test_suites=[
        "agreement_creation",
        "validation_process",
        "verification_proofs",
        "compliance_checks"
    ]
)

print("Integration test results:")
for suite, result in test_results["test_suites"].items():
    pass_count = result["passed"]
    total_count = result["total"]
    print(f"{suite}: {pass_count}/{total_count} tests passed")
    
    if result["failed"] > 0:
        print("  Failed tests:")
        for failed in result["failed_tests"]:
            print(f"    - {failed['name']}: {failed['error']}")
```

## 8. Monitoring and Operations

### Setting Up Monitoring

```python
# Set up production monitoring
monitoring = production_sdk.configure_monitoring(
    monitoring_options={
        "alerts_enabled": True,
        "metrics_collection": True,
        "log_aggregation": True,
        "dashboard_enabled": True,
        "notification_channels": [
            {"type": "email", "target": "admin@example.com"},
            {"type": "slack", "target": "#metanode-alerts"}
        ]
    }
)

print(f"Monitoring configured: {monitoring['status']}")
print(f"Dashboard URL: {monitoring['dashboard_url']}")
```

### Configuring Backup Strategy

```python
# Set up automated backups
backup_config = production_sdk.configure_backups(
    backup_options={
        "schedule": "0 2 * * *",  # Daily at 2 AM
        "retention_days": 30,
        "storage_location": "s3://metanode-backups/production",
        "components": [
            "agreements",
            "blockchain_state",
            "verification_proofs",
            "configuration"
        ],
        "encryption_enabled": True
    }
)

print(f"Backup configuration: {backup_config['status']}")
print(f"Next backup scheduled for: {backup_config['next_backup_time']}")
```

## 9. Security Best Practices

### Security Hardening

```python
# Perform security hardening
security_hardening = production_sdk.apply_security_hardening(
    security_options={
        "apply_infrastructure_hardening": True,
        "enable_network_policies": True,
        "configure_authentication": {
            "mfa_required": True,
            "session_timeout_minutes": 30
        },
        "configure_authorization": {
            "rbac_enabled": True,
            "default_deny": True
        },
        "enable_audit_logging": True
    }
)

print(f"Security hardening applied: {security_hardening['status']}")

# Generate security report
security_report = production_sdk.generate_security_report()
print(f"Security report: {security_report['summary']}")
print(f"Security score: {security_report['security_score']}/100")
```

### Access Control Configuration

```python
# Configure access controls for production
access_config = production_sdk.configure_access_control(
    roles=[
        {
            "name": "admin",
            "permissions": ["*"]
        },
        {
            "name": "operator",
            "permissions": [
                "read:*",
                "write:agreements",
                "execute:validation"
            ]
        },
        {
            "name": "auditor",
            "permissions": [
                "read:agreements",
                "read:audit_logs",
                "read:compliance_reports"
            ]
        }
    ],
    users=[
        {"username": "admin1", "role": "admin"},
        {"username": "operator1", "role": "operator"},
        {"username": "auditor1", "role": "auditor"}
    ]
)

print(f"Access control configured: {access_config['status']}")
```

## 10. Troubleshooting

### Common Migration Issues

```python
# Check for common migration issues
health_check = production_sdk.run_health_check()
if health_check["issues"]:
    print("Found issues:")
    for issue in health_check["issues"]:
        print(f"  - {issue['description']}")
        print(f"    Severity: {issue['severity']}")
        print(f"    Recommendation: {issue['recommendation']}")

# Troubleshoot specific components
component_diagnostics = production_sdk.run_component_diagnostics(
    component="blockchain"
)
print(f"Component diagnostics: {component_diagnostics['status']}")
```

### Recovery Procedures

```python
# Execute recovery procedure if needed
recovery = production_sdk.execute_recovery_procedure(
    procedure="agreement_sync",
    options={
        "source": "backup",
        "backup_id": "backup-20250620",
        "validate_after_recovery": True
    }
)

print(f"Recovery status: {recovery['status']}")
if recovery["status"] == "complete":
    print("Recovery completed successfully")
else:
    print(f"Recovery failed: {recovery['error']}")
```

## Conclusion

By following this step-by-step guide, you can successfully migrate your MetaNode application from testnet to production. The production environment provides enhanced security, reliability, and performance for your blockchain agreements and verification proofs.

Remember to regularly update your production environment, monitor its performance, and conduct security audits to maintain optimal operation.

For more detailed information, refer to the following documentation:

- [High Availability Configuration](/docs/infrastructure/06_high_availability.md)
- [Infrastructure Scaling](/docs/infrastructure/05_infrastructure_scaling.md)
- [Agreement Validation](/docs/agreements/04_agreement_validation.md)
- [Compliance and Auditing](/docs/agreements/05_compliance_auditing.md)
