# High Availability Infrastructure

This document provides guidelines for implementing highly available MetaNode infrastructure to minimize downtime and ensure continuous operation of your blockchain applications.

## Overview

High availability (HA) in MetaNode infrastructure ensures that applications remain operational despite component failures, maintenance activities, or unexpected outages. This is achieved through redundancy, automated failover, and proper monitoring.

## Key HA Components

A highly available MetaNode infrastructure includes:

1. **Redundant Nodes**: Multiple instances of each component
2. **Failover Mechanisms**: Automatic detection and recovery from failures
3. **Load Balancing**: Distribution of requests across available resources
4. **Data Replication**: Synchronized data across multiple instances
5. **Health Monitoring**: Continuous checking of component health

## Architecture

A typical HA MetaNode infrastructure has this architecture:

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    └───────┬─────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
     ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
     │ Blockchain  │ │ Blockchain  │ │ Blockchain  │
     │   Node 1    │ │   Node 2    │ │   Node 3    │
     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
            │               │               │
     ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
     │  Validator  │ │  Validator  │ │  Validator  │
     │   Node 1    │ │   Node 2    │ │   Node 3    │
     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                    ┌───────┴───────┐
                    │  Distributed  │
                    │    Storage    │
                    └───────────────┘
```

## Kubernetes HA Configuration

For Kubernetes environments, implement high availability using:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: metanode-blockchain-ha
  namespace: metanode
spec:
  replicas: 3
  selector:
    matchLabels:
      app: metanode
      component: blockchain
  serviceName: "metanode-blockchain"
  podManagementPolicy: Parallel
  updateStrategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: metanode
        component: blockchain
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: "component"
                    operator: In
                    values:
                      - blockchain
              topologyKey: "kubernetes.io/hostname"
      containers:
      - name: blockchain
        image: metanode/blockchain:latest
        env:
        - name: METANODE_ROLE
          value: "blockchain"
        - name: METANODE_NETWORK
          value: "testnet"
        - name: METANODE_NODE_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
          requests:
            cpu: "1"
            memory: "2Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8545
          initialDelaySeconds: 60
          periodSeconds: 30
        volumeMounts:
        - name: blockchain-data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: blockchain-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi
```

## Using the SDK for HA Configuration

Configure high availability using the SDK:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Deploy with high availability configuration
deployment = sdk.deploy_ha_infrastructure(
    app_name="my-app",
    components=["blockchain", "validator", "agreement", "ipfs"],
    replicas={
        "blockchain": 3,
        "validator": 5,
        "agreement": 2,
        "ipfs": 3
    },
    anti_affinity=True,  # Ensure pods run on different nodes
    automatic_failover=True,
    health_check={
        "interval": 30,  # seconds
        "timeout": 10,   # seconds
        "retries": 3
    }
)
```

## Docker HA Configuration

For Docker environments without Kubernetes:

```yaml
# docker-compose with high availability
version: '3.8'

services:
  haproxy:
    image: haproxy:2.4
    ports:
      - "8545:8545"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    depends_on:
      - blockchain1
      - blockchain2
      - blockchain3
    networks:
      - metanode-net

  blockchain1:
    image: metanode/blockchain:latest
    environment:
      - METANODE_ROLE=blockchain
      - METANODE_NETWORK=testnet
      - METANODE_NODE_ID=node1
    volumes:
      - blockchain1_data:/data
    networks:
      - metanode-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8545"]
      interval: 30s
      timeout: 10s
      retries: 3

  blockchain2:
    image: metanode/blockchain:latest
    environment:
      - METANODE_ROLE=blockchain
      - METANODE_NETWORK=testnet
      - METANODE_NODE_ID=node2
    volumes:
      - blockchain2_data:/data
    networks:
      - metanode-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8545"]
      interval: 30s
      timeout: 10s
      retries: 3

  blockchain3:
    image: metanode/blockchain:latest
    environment:
      - METANODE_ROLE=blockchain
      - METANODE_NETWORK=testnet
      - METANODE_NODE_ID=node3
    volumes:
      - blockchain3_data:/data
    networks:
      - metanode-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8545"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  blockchain1_data:
  blockchain2_data:
  blockchain3_data:

networks:
  metanode-net:
    external: true
```

Example HAProxy configuration:

```
frontend blockchain_frontend
    bind *:8545
    mode http
    default_backend blockchain_backend

backend blockchain_backend
    mode http
    balance roundrobin
    option httpchk POST / HTTP/1.1\r\nContent-Type:\ application/json\r\nContent-Length:\ 44\r\n\r\n{"jsonrpc":"2.0","method":"web3_clientVersion","id":1}
    http-check expect status 200
    server node1 blockchain1:8545 check
    server node2 blockchain2:8545 check
    server node3 blockchain3:8545 check
```

## Consensus Configuration for HA

Optimize consensus parameters for high availability:

```python
# Configure consensus for HA
sdk.configure_consensus(
    app_name="my-app",
    quorum=3,  # Minimum nodes required for consensus
    timeout=10,  # Seconds to wait for consensus
    block_confirmation_count=6,  # Blocks required for finality
    heartbeat_interval=5  # Seconds between heartbeats
)
```

## Data Replication

Configure data replication for redundancy:

```python
# Configure data replication
sdk.configure_data_replication(
    app_name="my-app",
    replication_factor=3,  # Number of data copies
    sync_interval=5,        # Seconds between syncs
    consistency_level="quorum"  # Options: one, quorum, all
)
```

## Automated Failover

Set up automated failover for resilience:

```python
# Configure failover
sdk.configure_failover(
    app_name="my-app",
    detection_timeout=30,  # Seconds to detect failure
    recovery_action="restart",  # Options: restart, recreate, failover
    max_retry_count=3,
    notify_on_failover=True
)
```

## Backup and Recovery

Implement robust backup strategy:

```python
# Configure automated backups
sdk.configure_backups(
    app_name="my-app",
    schedule="0 2 * * *",  # Daily at 2 AM (cron format)
    retention_days=7,
    backup_storage="s3://metanode-backups",
    encryption=True,
    compression=True
)

# Configure disaster recovery
sdk.configure_disaster_recovery(
    app_name="my-app",
    recovery_point_objective=60,  # Minutes
    recovery_time_objective=120,  # Minutes
    secondary_region="us-west-2"  # Backup region
)
```

## Health Monitoring

Set up comprehensive health monitoring:

```python
# Configure health monitoring
sdk.configure_health_monitoring(
    app_name="my-app",
    components=["blockchain", "validator", "agreement"],
    check_interval=30,  # Seconds
    alerts_enabled=True,
    alert_endpoints=[
        {"type": "email", "address": "admin@example.com"},
        {"type": "slack", "webhook": "https://hooks.slack.com/services/..."}
    ]
)
```

## Multi-Region Deployment

For global high availability:

```python
# Deploy in multiple regions
regions = ["us-east-1", "eu-west-1", "ap-southeast-1"]

for region in regions:
    sdk.deploy_infrastructure(
        app_name=f"my-app-{region}",
        region=region,
        components=["blockchain", "validator", "agreement"],
        high_availability=True
    )
    
# Configure multi-region synchronization
sdk.configure_multi_region(
    app_name="my-app",
    regions=regions,
    primary_region="us-east-1",
    synchronization_mode="eventual",  # Options: eventual, strong
    failover_automatic=True
)
```

## Network Redundancy

Ensure network redundancy:

```python
# Configure network redundancy
sdk.configure_network_redundancy(
    app_name="my-app",
    dual_stack=True,  # Support both IPv4 and IPv6
    multi_provider=True,  # Use multiple network providers
    dns_redundancy=True   # Multiple DNS servers
)
```

## Maintenance Strategies

Implement zero-downtime maintenance:

```python
# Configure maintenance window
sdk.configure_maintenance(
    app_name="my-app",
    strategy="rolling",  # Options: rolling, blue-green, canary
    maintenance_window="Sun 01:00-05:00",
    max_unavailable="25%",
    drain_timeout=300  # Seconds
)
```

## Testing HA Configuration

Verify your high availability configuration:

```python
# Run resilience test
test_results = sdk.test_resilience(
    app_name="my-app",
    tests=["node_failure", "network_partition", "region_outage"],
    duration=60  # Minutes to run tests
)

# Generate resilience report
sdk.generate_resilience_report(
    test_results=test_results,
    output_file="resilience_report.pdf"
)
```

## Chaos Engineering

Implement chaos testing to verify HA:

```python
# Run chaos experiments
sdk.run_chaos_experiment(
    app_name="my-app",
    scenario="kill_random_pod",
    duration=30,  # Minutes
    target_components=["blockchain", "validator"]
)
```

## Troubleshooting HA Issues

Common high availability issues:

1. **Split Brain Syndrome**:
   - Symptoms: Conflicting state between nodes
   - Solution: Implement proper quorum settings and fencing mechanisms

2. **Replication Lag**:
   - Symptoms: Secondary nodes behind primary
   - Solution: Optimize network between nodes, increase sync frequency

3. **Failover Delays**:
   - Symptoms: Extended downtime during failover
   - Solution: Tune detection timeouts, implement warm standby

4. **Resource Contention**:
   - Symptoms: Performance degradation during failover
   - Solution: Ensure adequate resources on all nodes

## Next Steps

- Explore [Monitoring and Alerts](../management/01_monitoring_overview.md) for high availability
- Learn about [Performance Tuning](../management/03_performance_tuning.md) for optimized operations
- Review [Disaster Recovery](../management/04_disaster_recovery.md) for business continuity
