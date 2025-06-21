# MetaNode SDK for JavaScript

This package provides a JavaScript wrapper for the MetaNode SDK, enabling blockchain-grade infrastructure for secure, lightweight, and highly scalable federated computing and dApp deployment from your Node.js applications.

## Installation

The MetaNode SDK can be installed via npm:

```bash
npm install metanode-sdk
```

During installation, the package will automatically check for and install the required Python components. The SDK uses a dual-language architecture with JavaScript as the frontend and Python for the core SDK functionality.

## Requirements

- Node.js 14 or higher
- Python 3.8 or higher

## Usage

### Basic Usage

```javascript
const { MetaNode } = require('metanode-sdk');

// Create a new MetaNode SDK instance
const metanode = new MetaNode();

// Deploy an application to testnet
async function deployToTestnet() {
  try {
    const result = await metanode.deploy('/path/to/app', { testnet: true });
    console.log('Deployment successful:', result);
  } catch (error) {
    console.error('Deployment failed:', error);
  }
}

deployToTestnet();
```

### Create a dApp

Transform any application into a decentralized application:

```javascript
const { MetaNode } = require('metanode-sdk');
const metanode = new MetaNode();

async function createDapp() {
  try {
    const result = await metanode.createDapp('/path/to/app', { 
      testnet: true,
      wallet: '/path/to/wallet.json'
    });
    console.log('dApp created:', result);
  } catch (error) {
    console.error('Failed to create dApp:', error);
  }
}

createDapp();
```

### Create an Agreement

Create a blockchain agreement for your application:

```javascript
const { MetaNode } = require('metanode-sdk');
const metanode = new MetaNode();

async function createAgreement() {
  try {
    const result = await metanode.createAgreement('/path/to/app', {
      name: 'My Agreement',
      version: '1.0.0',
      parties: ['0xabcd...', '0x1234...']
    });
    console.log('Agreement created:', result);
  } catch (error) {
    console.error('Failed to create agreement:', error);
  }
}

createAgreement();
```

### Connect to Testnet

Connect your application to the MetaNode testnet:

```javascript
const { MetaNode } = require('metanode-sdk');
const metanode = new MetaNode();

async function connectAndVerify() {
  try {
    // Connect to testnet
    await metanode.connectTestnet('/path/to/app');
    
    // Create a node cluster
    await metanode.createNodeCluster('/path/to/app');
    
    // Generate verification proofs
    await metanode.generateProofs('/path/to/app');
    
    console.log('Application connected and verified on testnet');
  } catch (error) {
    console.error('Testnet connection failed:', error);
  }
}

connectAndVerify();
```

## API Reference

### `MetaNode` Class

#### Constructor
- `new MetaNode()` - Creates a new MetaNode SDK instance

#### Methods
- `execute(command, args)` - Execute a MetaNode command directly
- `deploy(appPath, options)` - Deploy an application
- `createAgreement(appPath, options)` - Create a blockchain agreement
- `connectTestnet(appPath)` - Connect an application to the testnet
- `createNodeCluster(appPath)` - Create a node cluster for an application
- `generateProofs(appPath)` - Generate verification proofs for an application
- `createDapp(appPath, options)` - Transform an application into a dApp

## CLI Usage

This package also provides command-line tools:

- `metanode-cli` - Main CLI interface
- `metanode-agreement` - Agreement management
- `metanode-testnet` - Testnet connection management
- `metanode-deploy` - Automatic dApp deployment

Example:
```bash
npx metanode-cli --help
npx metanode-deploy --app /path/to/app --testnet
```

## License

Proprietary License - All Rights Reserved. See the LICENSE file for details.
