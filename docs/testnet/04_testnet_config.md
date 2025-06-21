# Application-Specific Testnet Configuration

This document explains how to configure testnet settings for your specific application needs using the MetaNode SDK.

## Overview

The MetaNode testnet allows for application-specific configurations that determine how your application interacts with the blockchain, validators, and consensus mechanisms. These configurations are stored in your application's configuration files and can be managed through the SDK or CLI.

## Configuration File Structure

By default, your application's testnet configuration is stored in:
- `~/.metanode/apps/[app-name]/metanode_config/testnet_connection.json`

A typical configuration looks like this:

```json
{
  "rpc_url": "http://159.203.17.36:8545",
  "ws_url": "ws://159.203.17.36:8546",
  "connected_at": "2025-06-21T01:06:48.970731",
  "connection_id": "13cd72a1-8071-4324-9dbc-2d37a1a6469b",
  "status": "active",
  "app_settings": {
    "block_confirmation_count": 6,
    "consensus_enabled": true,
    "agreement_enabled": true,
    "gas_price_strategy": "medium",
    "transaction_timeout": 300
  }
}
```

## Configuring Your Application

### Using the SDK

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Configure testnet settings for a specific application
sdk.configure_testnet(
    app_name="my-app",
    block_confirmations=6,
    consensus_enabled=True,
    agreement_enabled=True,
    gas_price_strategy="medium",
    transaction_timeout=300
)

# Get current configuration
config = sdk.get_testnet_config("my-app")
print(f"Current configuration: {config}")
```

### Using the CLI

```bash
# Configure testnet settings
metanode-cli testnet config my-app --block-confirmations 6 --consensus enabled --agreements enabled

# View current configuration
metanode-cli testnet config my-app --view
```

## Configuration Options

| Setting | Description | Default | Options |
|---------|-------------|---------|---------|
| `block_confirmation_count` | Number of block confirmations required | 6 | 1-30 |
| `consensus_enabled` | Whether to use consensus for transactions | true | true, false |
| `agreement_enabled` | Whether agreements are enabled | true | true, false |
| `gas_price_strategy` | Strategy for setting gas prices | "medium" | "low", "medium", "high", "custom" |
| `transaction_timeout` | Seconds to wait for transaction confirmation | 300 | 30-3600 |
| `api_retry_count` | API request retry count | 3 | 1-10 |
| `api_retry_delay` | Seconds between API retries | 2 | 1-60 |

## Advanced Configuration

For more advanced needs, you can directly edit the configuration file or use the advanced configuration methods in the SDK:

```python
# Advanced configuration with custom parameters
sdk.configure_testnet_advanced(
    app_name="my-app",
    config={
        "custom_endpoints": {
            "validator": "http://custom-validator:7545"
        },
        "transaction_settings": {
            "custom_gas_price": 20000000000,  # 20 Gwei
            "gas_limit": 3000000
        },
        "network_settings": {
            "max_peers": 50,
            "discovery_enabled": True
        }
    }
)
```

## Environment-Specific Configurations

You can create environment-specific configurations for development, testing, and production scenarios:

```bash
# Configure for development
metanode-cli testnet config my-app --env dev --block-confirmations 1 --transaction-timeout 60

# Configure for production-like testing
metanode-cli testnet config my-app --env staging --block-confirmations 12 --transaction-timeout 600
```

## Wallet Configuration

Configure how your application's wallet interacts with the testnet:

```python
# Configure wallet settings through the SDK
sdk.configure_wallet(
    app_name="my-app",
    auto_fund=True,  # Automatically request funds from faucet if needed
    min_balance=0.1,  # ETH
    key_storage="encrypted_file"  # How to store private keys
)
```

## RPC and API Configuration

Configure custom RPC endpoints or API settings:

```bash
# Set custom RPC endpoint
metanode-cli testnet config my-app --rpc-url http://custom-endpoint:8545

# Configure API settings
metanode-cli testnet config my-app --api-retry-count 5 --api-retry-delay 3
```

## Security Configuration

Configure security settings for testnet interaction:

```python
# Configure security settings
sdk.configure_testnet_security(
    app_name="my-app",
    require_https=True,  # Require HTTPS for API connections
    verify_ssl=True,      # Verify SSL certificates
    use_encryption=True,  # Encrypt local storage
    auto_lock_timeout=300  # Auto-lock wallet after inactivity
)
```

## Configuration Profiles

You can save and load configuration profiles to quickly switch between different settings:

```bash
# Save current configuration as a profile
metanode-cli testnet config-profile save my-app --name "high-security"

# Load a saved profile
metanode-cli testnet config-profile load my-app --name "high-security"

# List available profiles
metanode-cli testnet config-profile list my-app
```

## Troubleshooting Configuration Issues

If you're experiencing issues with your configuration:

1. Verify your configuration file exists and is valid JSON
2. Check that your RPC endpoint is accessible: `curl -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}' http://159.203.17.36:8545`
3. Reset to default configuration: `metanode-cli testnet config my-app --reset`
4. Check logs for connection issues: `~/.metanode/logs/testnet_connection.log`

## Next Steps

- Learn about [Testnet-to-Production Migration](05_testnet_to_prod.md)
- Explore [Agreement Management](../agreements/01_agreement_overview.md)
- Set up [Infrastructure Automation](../infrastructure/01_infrastructure_overview.md)
