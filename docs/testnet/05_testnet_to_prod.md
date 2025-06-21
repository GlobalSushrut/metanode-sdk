# Testnet to Production Migration

This document guides you through the process of migrating your MetaNode applications from testnet to a production environment.

## Overview

After developing and testing your application on the MetaNode testnet (`http://159.203.17.36:8545`), you'll need to prepare for production deployment. This involves adjusting configurations, ensuring proper security measures, and planning for increased resource requirements.

## Migration Checklist

Before migrating to production, ensure your application is ready by checking the following:

- [x] Application fully tested on testnet
- [x] Agreements properly validated and verified
- [x] Verification proofs generated and stored
- [x] Resource requirements calculated for production load
- [x] Security configurations reviewed and hardened
- [x] Backup and recovery strategy defined
- [x] Monitoring and alerting configured

## Configuration Changes

### Network Configuration

Update your application's network configuration from testnet to production:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK with production endpoint
sdk = MetaNodeSDK(network_type="production")

# Or update an existing application
sdk.update_network_config(
    app_name="my-app",
    network_type="production",
    rpc_endpoint="http://your-production-endpoint:8545",
    ws_endpoint="ws://your-production-endpoint:8546"
)
```

### Using the CLI

```bash
# Update network configuration
metanode-cli network switch my-app --type production

# Configure production endpoint manually
metanode-cli network config my-app --rpc-url http://your-production-endpoint:8545
```

## Wallet Migration

Securely migrate your wallet to the production environment:

```python
# Export wallet (securely)
wallet_data = sdk.export_wallet(
    wallet_id="testnet-wallet-id",
    secure=True,
    password="strong-password"
)

# Import to production
sdk.import_wallet(
    wallet_data=wallet_data,
    password="strong-password",
    environment="production"
)
```

## Agreement Migration

Migrate your agreements to the production environment:

```python
# List existing agreements
agreements = sdk.list_agreements(app_name="my-app")

# Migrate each agreement to production
for agreement in agreements:
    prod_agreement = sdk.migrate_agreement(
        agreement_id=agreement["id"],
        target_network="production",
        update_parties=True  # Updates party addresses to production addresses
    )
    print(f"Migrated agreement: {prod_agreement['id']}")
```

## Infrastructure Scaling

### Node Cluster Scaling

Scale your node clusters for production load:

```python
# Scale up existing cluster
sdk.update_node_cluster(
    cluster_id="testnet-cluster-id",
    node_count=5,
    resources={
        "cpu": 4,
        "memory": "8Gi",
        "storage": "200Gi"
    }
)

# Or create new production cluster
sdk.create_node_cluster(
    name="production-cluster",
    node_type="validator",
    node_count=3,
    network="production",
    high_availability=True
)
```

### Kubernetes Configuration

For production deployments, adjust your Kubernetes configuration:

```bash
# Generate production Kubernetes manifests
metanode-cli k8s generate-manifests \
  --output-dir ./k8s-prod \
  --environment production \
  --replicas 3 \
  --resources high
```

## Security Hardening

Apply additional security measures for production:

```python
# Configure enhanced security settings
sdk.configure_testnet_security(
    app_name="my-app",
    environment="production",
    require_https=True,
    verify_ssl=True,
    use_encryption=True,
    auto_lock_timeout=120,
    max_failed_attempts=5,
    transaction_signing_policy="multi-sig"  # Requires multiple signatures for transactions
)
```

## Verification Proof Updates

Update verification proofs for production:

```python
# Regenerate verification proofs for production
proof = sdk.generate_verification_proof(
    app_id="my-app",
    environment="production"
)

# Verify the new proof
is_valid = sdk.verify_proof(proof_id=proof['hash'])
print(f"Production proof is valid: {is_valid}")
```

## Monitoring and Alerting

Configure monitoring and alerting for your production deployment:

```python
# Set up monitoring
sdk.configure_monitoring(
    app_name="my-app",
    metrics_enabled=True,
    alert_endpoints=[
        {
            "type": "email",
            "address": "alerts@example.com"
        },
        {
            "type": "webhook",
            "url": "https://alerts.example.com/webhook"
        }
    ],
    alert_thresholds={
        "transaction_failure_rate": 0.01,  # 1%
        "block_processing_delay": 60,      # 60 seconds
        "api_error_rate": 0.05             # 5%
    }
)
```

## Testing the Migration

After migration, perform these validation tests:

```bash
# Test production connection
metanode-cli network test --app my-app

# Verify wallet functionality
metanode-cli wallet test --app my-app

# Test agreement deployment
metanode-cli agreement deploy test-agreement --app my-app --verify
```

## Rollback Plan

Always maintain a rollback plan in case of migration issues:

```python
# Store testnet configuration backup
backup = sdk.backup_configuration(
    app_name="my-app",
    include_wallets=True,
    include_agreements=True
)

# Restore from backup if needed
sdk.restore_configuration(
    app_name="my-app",
    backup_id=backup["id"]
)
```

## Troubleshooting Migration Issues

If you encounter issues during migration:

1. Check connection to production endpoints
2. Verify wallet and private key accessibility  
3. Compare chainlink.lock files between environments
4. Review transaction history for any pending transactions
5. Check node cluster status and scaling issues

## Production Best Practices

- **Regular Backups**: Schedule regular backups of all critical data
- **Monitoring**: Implement comprehensive monitoring for all components
- **Update Strategy**: Plan for regular updates and maintenance windows
- **Security Audits**: Conduct periodic security audits
- **Disaster Recovery**: Test your disaster recovery process regularly
- **Documentation**: Keep all production configurations documented

## Next Steps

- Explore [Infrastructure Automation](../infrastructure/01_infrastructure_overview.md)
- Learn about [Monitoring and Management](../management/01_monitoring_overview.md) 
- Review [Security Best Practices](../security/01_security_overview.md)
