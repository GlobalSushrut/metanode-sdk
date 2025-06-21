# MetaNode Full Infrastructure SDK

[![PyPI version](https://img.shields.io/pypi/v/metanode-sdk-full.svg)](https://pypi.org/project/metanode-sdk-full/)
[![npm version](https://img.shields.io/npm/v/metanode-sdk-full.svg)](https://www.npmjs.com/package/metanode-sdk-full)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive SDK for building and deploying decentralized applications with full blockchain integration, IPFS storage, validator nodes, and agreement management.

## Features

- **Complete Blockchain Integration**: Deploy with full consensus, ledger, and validator support
- **IPFS Integration**: Built-in distributed storage functionality
- **Agreement Management**: Create, deploy and verify blockchain agreements
- **Testnet Connectivity**: Connect to and contribute to external testnets
- **Decentralization Enhancement**: Deploy node clusters to improve testnet decentralization
- **Cross-Platform Support**: Available for Python, JavaScript, and Go developers
- **Docker Integration**: Run as containers for easy deployment
- **Full Kubernetes Support**: Enterprise-grade deployment options

## Installation

### Python (PyPI)

```bash
pip install metanode-sdk-full
```

### JavaScript (npm)

```bash
npm install -g metanode-sdk-full
```

### Go

```bash
go get github.com/metanode/metanode-sdk-go
```

### Quick Install Script

For a complete setup that works across platforms:

```bash
curl -sSL https://raw.githubusercontent.com/metanode/metanode-sdk/main/install.sh | bash
```

## Quick Start

### Command Line Interface

```bash
# Initialize a new MetaNode app
metanode-cli init my-dapp

# Deploy with blockchain integration
metanode-cli deploy my-dapp --blockchain --ipfs

# Create and deploy an agreement
metanode-cli agreement my-dapp --create
metanode-cli agreement my-dapp --deploy --id [AGREEMENT_ID]

# Create a node cluster for decentralization
metanode-cli cluster my-dapp --create

# Check status
metanode-cli status my-dapp
```

### Python SDK

```python
from metanode.full_sdk import MetaNodeSDK

# Initialize SDK
sdk = MetaNodeSDK()

# Create and deploy application
sdk.init_app("my-dapp")
sdk.deploy_app("my-dapp", with_blockchain=True, with_ipfs=True)

# Create and deploy agreement
agreement_id = sdk.create_agreement("my-dapp")
sdk.deploy_agreement("my-dapp", agreement_id)

# Create node cluster for decentralization
sdk.create_node_cluster("my-dapp")

# Check status
status = sdk.check_status("my-dapp")
print(status)
```

### JavaScript SDK

```javascript
const MetaNodeSDK = require('metanode-sdk-full');

// Initialize SDK
const sdk = new MetaNodeSDK();

// Create and deploy application
sdk.initApp('my-dapp')
  .then(() => sdk.deployApp('my-dapp'))
  .then(() => sdk.createAgreement('my-dapp'))
  .then(agreementId => sdk.deployAgreement('my-dapp', agreementId))
  .then(() => sdk.createNodeCluster('my-dapp'))
  .then(() => sdk.checkStatus('my-dapp'))
  .then(status => console.log(status))
  .catch(err => console.error(err));
```

### Go SDK

```go
package main

import (
	"fmt"
	
	"github.com/metanode/metanode-sdk-go/metanode"
)

func main() {
	// Create SDK instance
	sdk, err := metanode.NewSDK()
	if err != nil {
		panic(err)
	}
	
	// Initialize
	sdk.Initialize()
	
	// Create and deploy application
	sdk.InitApp("my-dapp")
	sdk.DeployApp("my-dapp")
	
	// Create node cluster
	sdk.CreateNodeCluster("my-dapp")
}
```

## Architecture

The MetaNode Full Infrastructure SDK provides a comprehensive solution for decentralized applications:

```
┌────────────────────────────────────────────────┐
│              MetaNode Application              │
├────────────────────────────────────────────────┤
│ ┌──────────────┐ ┌─────────┐ ┌───────────────┐ │
│ │  Blockchain  │ │  IPFS   │ │   Validator   │ │
│ │   Support    │ │ Storage │ │     Nodes     │ │
│ └──────────────┘ └─────────┘ └───────────────┘ │
├────────────────────────────────────────────────┤
│ ┌──────────────┐ ┌─────────────────────────┐   │
│ │  Agreement   │ │     Node Clusters       │   │
│ │  Management  │ │  for Decentralization   │   │
│ └──────────────┘ └─────────────────────────┘   │
├────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌────────────────────────┐ │
│ │     Testnet     │ │   Blockchain Ledger    │ │
│ │   Integration   │ │  & Consensus Engine    │ │
│ └─────────────────┘ └────────────────────────┘ │
└────────────────────────────────────────────────┘
```

## Documentation

Full documentation is available at [https://metanode-sdk.io/docs](https://metanode-sdk.io/docs)

## Examples

Check the `examples` directory for complete implementations:

- Basic dApp deployment
- Blockchain agreement management
- Node cluster creation
- Full infrastructure deployment
- Integration with external systems

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
