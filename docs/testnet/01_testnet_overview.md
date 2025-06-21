# MetaNode Testnet Connection Guide

## Overview

The MetaNode SDK provides tools for connecting to the external testnet RPC endpoint at `http://159.203.17.36:8545` (HTTP RPC) and `ws://159.203.17.36:8546` (WebSocket). This testnet is a basic blockchain environment that developers can use for testing applications built with the MetaNode SDK.

## Testnet Functionality

The testnet provides:

1. **Basic RPC Interface**: Standard JSON-RPC methods including `eth_blockNumber`, `net_version`, and `eth_syncing`
2. **Agreement Deployment**: Support for deploying and verifying application agreements
3. **Transaction Processing**: For applications that require blockchain transactions

## Connection Details

- **HTTP RPC Endpoint**: http://159.203.17.36:8545
- **WebSocket Endpoint**: ws://159.203.17.36:8546
- **Access Method**: Public, no authentication required

## Testing Connection

The SDK provides a tool for testing connectivity:

```python
# Using the test_rpc_connection.py script
python test_rpc_connection.py http://159.203.17.36:8545

# Or using the CLI
metanode-cli testnet --test --rpc http://159.203.17.36:8545
```

Expected output shows basic network information:

```
Connected to RPC endpoint: http://159.203.17.36:8545
Block number: 1
Network ID: 1337
Node is not syncing
Client version: MetaNode/v1.0.0
```

## Enhancing Testnet Decentralization

Developers can contribute to testnet decentralization by setting up node clusters:

```bash
# Using the CLI
metanode-cli cluster my-app --create --rpc http://159.203.17.36:8545

# Or directly with the shell script
./enhance_testnet_decentralization.sh
```

This creates additional nodes that connect to the testnet and provide:
- Additional validation nodes
- Light client nodes for redundancy
- Improved network robustness

## Connection Process

When an application is deployed with the MetaNode SDK:

1. The SDK establishes a connection to the testnet
2. Verifies the connection with basic RPC calls
3. Creates verification proofs (chainlink.lock files)
4. Optionally sets up node clusters to enhance decentralization

## Troubleshooting

If connection issues occur:

1. Verify the RPC endpoint is accessible: `curl -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' http://159.203.17.36:8545`

2. Check network connectivity: `ping 159.203.17.36`

3. Review SDK logs: `~/.metanode/logs/testnet_connection.log`

## Next Steps

- Learn about [Contributing to Testnet Decentralization](02_enhancing_testnet.md)
- Set up [Verification Proofs](03_verification_proofs.md)
- Configure [Application-Specific Testnet Settings](04_testnet_config.md)
