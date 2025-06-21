# Verification Proofs in MetaNode Testnet

This document explains how verification proofs work in the MetaNode testnet environment and how they're used to secure application deployments and agreements.

## What Are Verification Proofs?

Verification proofs in the MetaNode ecosystem provide cryptographic evidence that:
- Your application is correctly connected to the testnet
- Transactions and agreements have been properly validated
- Node contributions are legitimate and authorized

The primary verification mechanism in the MetaNode testnet is the `chainlink.lock` file, which contains cryptographic proof of validation.

## How Verification Proofs Work

1. When you connect to the testnet or create an agreement, the SDK generates a verification proof
2. This proof contains timestamps, hashes, and cryptographic signatures
3. The proof is stored both locally and on the blockchain
4. When transactions or agreements are verified, these proofs are checked against the blockchain record

## The chainlink.lock File

The `chainlink.lock` file is the primary verification artifact. It's created in your application's configuration directory and contains:

```json
{
  "provider": "chainlink",
  "network": "testnet",
  "timestamp": 1624552286,
  "rpc_endpoint": "http://159.203.17.36:8545",
  "ws_endpoint": "ws://159.203.17.36:8546",
  "chain_id": 11155111,
  "proof_of_execution": {
    "hash": "0xabcdef1234567890",
    "timestamp": 1624552286,
    "block_number": 12345678,
    "validator": "0x9876543210fedcba"
  }
}
```

## Creating Verification Proofs

### Using the SDK

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize the SDK
sdk = MetaNodeSDK()

# Generate a verification proof for your application
proof = sdk.generate_verification_proof(app_id="my-app")
print(f"Proof generated: {proof['hash']}")

# Verify an existing proof
is_valid = sdk.verify_proof(proof_id=proof['hash'])
print(f"Proof is valid: {is_valid}")
```

### Using the CLI

```bash
# Generate a verification proof
metanode-cli testnet verify --app my-app

# Check status of a verification proof
metanode-cli testnet proof-status --hash 0xabcdef1234567890
```

## Verification for Agreements

When creating agreements on the testnet, verification proofs ensure that all parties can trust the agreement's execution:

```python
# Create an agreement with automatic verification
agreement_id = sdk.create_agreement(
    name="data-sharing-agreement",
    parties=["0xParty1Address", "0xParty2Address"],
    terms_file="./terms.json",
    verify=True  # Enables automatic verification proof generation
)

# Manually verify an agreement
verification = sdk.verify_agreement(agreement_id)
```

## Validator Architecture

The testnet utilizes a network of validators to create and verify proofs:

1. When a proof is requested, it's submitted to multiple validators
2. Validators check the request against blockchain records
3. A consensus threshold must be reached (typically 2/3 of validators)
4. The final proof is recorded on-chain for future verification

## Proof Security Features

MetaNode verification proofs include several security features:

- **Timestamping**: All proofs are precisely timestamped to prevent replay attacks
- **Block Anchoring**: Proofs are anchored to specific blockchain blocks
- **Multi-signature Validation**: Multiple validators sign each proof
- **Revocation Support**: Compromised proofs can be revoked by authorized validators

## Manual Verification

You can manually verify a proof using the CLI or web3 library:

```bash
# CLI verification
metanode-cli testnet verify-proof --hash 0xabcdef1234567890

# Raw RPC verification
curl -X POST -H "Content-Type: application/json" --data '{
  "jsonrpc":"2.0",
  "method":"metanode_verifyProof",
  "params":["0xabcdef1234567890"],
  "id":1
}' http://159.203.17.36:8545
```

## Troubleshooting Verification Issues

If you encounter verification problems:

1. Check that your local chainlink.lock file exists and is valid
2. Ensure your application is properly connected to the testnet
3. Verify that the testnet validators are operational: `metanode-cli testnet status --validators`
4. Try regenerating the verification proof: `metanode-cli testnet reverify --app my-app`

## Next Steps

- Configure [Application-Specific Testnet Settings](04_testnet_config.md)
- Learn about [Testnet-to-Production Migration](05_testnet_to_prod.md)
- Explore [Agreement Management](../agreements/01_agreement_overview.md)
