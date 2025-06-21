# Infrastructure Scaling

This document explains how to scale MetaNode infrastructure components to handle increased load and ensure optimal performance as your application grows.

## Overview

As your MetaNode applications grow, you'll need to scale your infrastructure accordingly. The MetaNode SDK provides tools and strategies for both vertical scaling (adding more resources to existing nodes) and horizontal scaling (adding more nodes).

## When to Scale

Consider scaling your infrastructure when you observe:

- High CPU or memory utilization (>70% sustained)
- Increased transaction processing times
- Growing blockchain data size
- Higher API request latency
- Increased number of concurrent users

## Scaling Options

### Horizontal Scaling

Horizontal scaling involves adding more nodes to distribute the load:

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Scale by increasing replicas
sdk.scale_infrastructure(
    app_name="my-app",
    component="blockchain",
    replicas=3  # Increase from 1 to 3 nodes
)

# Scale validator cluster
sdk.scale_infrastructure(
    app_name="my-app",
    component="validator",
    replicas=5  # Increase validator count for better consensus
)
```

Using the CLI:

```bash
# Scale blockchain nodes
metanode-cli infra scale --component blockchain --replicas 3 --app my-app

# Scale validator nodes
metanode-cli infra scale --component validator --replicas 5 --app my-app
```

### Vertical Scaling

Vertical scaling increases resources for existing nodes:

```python
# Increase resources for blockchain component
sdk.update_resource_allocation(
    app_name="my-app",
    component="blockchain",
    cpu="4",        # Cores
    memory="8Gi",   # Memory
    storage="100Gi" # Storage
)
```

Using the CLI:

```bash
# Update resources for blockchain component
metanode-cli infra resources --component blockchain --cpu 4 --memory 8Gi --app my-app
```

## Load Balancing

When horizontally scaling, implement load balancing:

### Kubernetes Load Balancing

```yaml
apiVersion: v1
kind: Service
metadata:
  name: metanode-blockchain-lb
  namespace: metanode
spec:
  type: LoadBalancer
  selector:
    app: metanode
    component: blockchain
  ports:
  - name: rpc
    port: 8545
    targetPort: 8545
  - name: ws
    port: 8546
    targetPort: 8546
```

The SDK can automate this configuration:

```python
# Configure load balancing
sdk.configure_load_balancing(
    app_name="my-app",
    component="blockchain",
    strategy="round-robin",
    session_sticky=False
)
```

### Docker Load Balancing

For Docker environments, use Traefik or Nginx:

```yaml
# docker-compose.yml with Traefik
version: '3.8'

services:
  traefik:
    image: traefik:v2.5
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
    ports:
      - "80:80"
      - "8545:8545"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - metanode-net

  metanode-blockchain-1:
    image: metanode/blockchain:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.blockchain.rule=Host(`blockchain.localhost`)"
      - "traefik.http.services.blockchain.loadbalancer.server.port=8545"
    networks:
      - metanode-net

  metanode-blockchain-2:
    image: metanode/blockchain:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.blockchain.rule=Host(`blockchain.localhost`)"
      - "traefik.http.services.blockchain.loadbalancer.server.port=8545"
    networks:
      - metanode-net

networks:
  metanode-net:
    external: true
```

## Database Scaling

For blockchain state databases:

```python
# Scale database capacity
sdk.configure_database_scaling(
    app_name="my-app",
    max_connections=500,
    connection_pool_size=100,
    shared_buffers="2GB",
    effective_cache_size="6GB"
)
```

## Auto-scaling Configuration

Configure auto-scaling based on load:

### Kubernetes Auto-scaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: metanode-blockchain-autoscaler
  namespace: metanode
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: metanode-blockchain
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### SDK Auto-scaling Configuration

```python
# Configure auto-scaling
sdk.configure_auto_scaling(
    app_name="my-app",
    component="blockchain",
    min_replicas=1,
    max_replicas=5,
    cpu_threshold=70,  # Percentage
    memory_threshold=80  # Percentage
)
```

## Network Optimization

As you scale, optimize network communication:

```python
# Configure network for scale
sdk.optimize_network(
    app_name="my-app",
    peer_limit=50,            # Max number of peers
    max_pending_peers=30,     # Max pending peer connections
    discovery_dns=True,       # Use DNS discovery
    connection_timeout=10     # Connection timeout in seconds
)
```

## Storage Scaling

Scale blockchain storage efficiently:

```python
# Configure storage scaling
sdk.configure_storage_scaling(
    app_name="my-app",
    pruning_mode="archive",   # Options: archive, full, fast
    state_cache_size=2048,    # MB
    block_retention=10000,    # Number of blocks to retain full data for
    auto_expand_storage=True, # Automatically expand storage when needed
    max_storage_size="500Gi"  # Maximum storage size
)
```

## Monitoring Scaled Infrastructure

When scaling, enhance monitoring:

```python
# Configure enhanced monitoring for scaled infrastructure
sdk.configure_monitoring(
    app_name="my-app",
    metrics_scrape_interval=15,  # Seconds
    metrics_retention="30d",     # 30 days
    alert_on_high_load=True,
    alert_thresholds={
        "cpu_utilization": 85,
        "memory_utilization": 85,
        "disk_utilization": 80,
        "transaction_queue_length": 5000
    }
)
```

## Performance Benchmarking

Before and after scaling, benchmark performance:

```bash
# Run performance benchmark
metanode-cli benchmark --transactions 1000 --concurrent 50 --app my-app

# Generate load test report
metanode-cli benchmark report --output benchmark-results.pdf
```

## Scaling Patterns

### Read-Heavy Applications

For applications with many read operations:

```python
# Configure for read-heavy scaling
sdk.optimize_for_read_operations(
    app_name="my-app",
    read_replicas=5,  # More read replicas
    cache_size="4Gi", # Larger cache
    query_timeout=30  # Extended query timeout
)
```

### Write-Heavy Applications

For applications with many write operations:

```python
# Configure for write-heavy scaling
sdk.optimize_for_write_operations(
    app_name="my-app",
    transaction_pool_size=8192,
    block_gas_limit=8000000,
    block_period=5,  # seconds
    state_cache_size=1024  # MB
)
```

### Geographical Distribution

For globally distributed applications:

```python
# Deploy in multiple regions
regions = ["us-east", "eu-west", "asia-east"]

for region in regions:
    sdk.deploy_infrastructure(
        app_name=f"my-app-{region}",
        region=region,
        components=["blockchain", "validator", "agreement"]
    )
    
# Configure global load balancing
sdk.configure_global_load_balancing(
    app_name="my-app",
    regions=regions,
    routing_strategy="latency-based"
)
```

## Cost Optimization

As you scale, optimize costs:

```python
# Analyze infrastructure costs
cost_analysis = sdk.analyze_infrastructure_costs(app_name="my-app")
print(f"Estimated monthly cost: ${cost_analysis['estimated_monthly_cost']}")

# Get cost optimization recommendations
recommendations = sdk.get_cost_optimization_recommendations(app_name="my-app")
for recommendation in recommendations:
    print(f"- {recommendation['description']}: Save ${recommendation['estimated_savings']}/month")
```

## Scaling Checklist

Before scaling production infrastructure:

1. **Backup Data**: Ensure all critical data is backed up
2. **Performance Baseline**: Document current performance metrics
3. **Capacity Planning**: Calculate future resource needs
4. **Test at Scale**: Test application with simulated load
5. **Monitor Closely**: Enhance monitoring during scaling
6. **Rollback Plan**: Have a plan to revert changes if needed

## Troubleshooting Scaled Infrastructure

### Common Scaling Issues

1. **Consensus Delays**: 
   - Check validator node count and network latency
   - Ensure quorum settings are appropriate for node count

2. **Database Bottlenecks**:
   - Optimize database configuration
   - Consider sharding for large datasets

3. **Network Saturation**:
   - Monitor network I/O and bandwidth usage
   - Implement rate limiting if needed

4. **Resource Contention**:
   - Check for CPU or memory bottlenecks
   - Adjust resource allocation based on usage patterns

## Next Steps

- Implement [High Availability](06_high_availability.md) for resilient deployments
- Explore [Monitoring and Alerts](../management/01_monitoring_overview.md) for scaled infrastructure
- Learn about [Performance Tuning](../management/03_performance_tuning.md) for optimized operations
