#!/bin/bash
# ============================================================
# MetaNode Full SDK Packaging Script
# ============================================================
# This script packages the complete MetaNode SDK with:
# - Python package (PyPI)
# - Node.js package (npm)
# - Go package (for Geth integration)
# - Docker containers for all infrastructure

echo "===== MetaNode Full Infrastructure SDK Packager ====="
echo "Creating packages for PyPI, npm, and Go integration..."

# Create directory structure
mkdir -p packaging/{pypi,npm,go,docker}

# Copy all required files for Python package
echo "Packaging Python SDK for PyPI..."
cp metanode-sdk/setup_enhanced.py packaging/pypi/setup.py
cp -r metanode-sdk/bin packaging/pypi/
cp -r metanode-sdk/metanode packaging/pypi/
cp metanode-sdk/README.md packaging/pypi/
cat > packaging/pypi/MANIFEST.in << EOF
include bin/*
include README.md
recursive-include metanode *
EOF

# Package for PyPI
cd packaging/pypi
python setup.py sdist bdist_wheel
cd ../..
echo "Python package created successfully"

# Create Node.js package
echo "Packaging Node.js SDK for npm..."
cp metanode-sdk/package.json packaging/npm/
cp -r metanode-sdk/bin packaging/npm/
mkdir -p packaging/npm/scripts

# Create postinstall script for npm
cat > packaging/npm/scripts/postinstall.js << EOF
#!/usr/bin/env node

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log('Installing MetaNode full infrastructure dependencies...');

// Check for Python
const pythonProcess = spawn('python3', ['--version']);
pythonProcess.on('error', () => {
  console.error('Python 3 is required but not found. Please install Python 3 first.');
  process.exit(1);
});

// Install Python dependencies
const pipProcess = spawn('pip', ['install', 'web3', 'requests', 'docker', 'kubernetes', 'ipfshttpclient', 'eth-account']);

pipProcess.stdout.on('data', (data) => {
  console.log(data.toString());
});

pipProcess.stderr.on('data', (data) => {
  console.error(data.toString());
});

pipProcess.on('close', (code) => {
  if (code !== 0) {
    console.error('Failed to install Python dependencies');
    return;
  }
  console.log('Python dependencies installed successfully');
  
  // Make CLI scripts executable
  const scriptsDir = path.join(__dirname, '..', 'bin');
  fs.readdirSync(scriptsDir).forEach(file => {
    fs.chmodSync(path.join(scriptsDir, file), '755');
  });
  
  console.log('MetaNode SDK installed successfully!');
  console.log('You can now use "metanode-cli" command to interact with the SDK.');
});
EOF

# Create main Node.js module
cat > packaging/npm/index.js << EOF
/**
 * MetaNode SDK - Full Infrastructure with Blockchain
 * Main module for Node.js integration
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class MetaNodeSDK {
  constructor(options = {}) {
    this.network = options.network || 'testnet';
    this.rpcUrl = options.rpcUrl || 'http://159.203.17.36:8545';
    this.wsUrl = options.wsUrl || 'ws://159.203.17.36:8546';
    this.ipfsGateway = options.ipfsGateway || 'http://localhost:8081';
    this.cliPath = path.join(__dirname, 'bin', 'metanode-cli-wrapper.js');
    
    // Make sure CLI is executable
    fs.chmodSync(this.cliPath, '755');
  }

  /**
   * Initialize a new MetaNode application
   * @param {string} appName - Name of the application
   * @returns {Promise} - Promise resolving with output or rejecting with error
   */
  initApp(appName) {
    return this._runCommand(['init', appName, '--network', this.network, '--rpc', this.rpcUrl]);
  }

  /**
   * Deploy a MetaNode application
   * @param {string} appPath - Path to the application
   * @returns {Promise} - Promise resolving with output or rejecting with error
   */
  deployApp(appPath) {
    return this._runCommand(['deploy', appPath, '--network', this.network, '--rpc', this.rpcUrl]);
  }

  /**
   * Create a blockchain agreement
   * @param {string} appPath - Path to the application
   * @param {string} type - Agreement type
   * @returns {Promise} - Promise resolving with output or rejecting with error
   */
  createAgreement(appPath, type = 'standard') {
    return this._runCommand(['agreement', appPath, '--create', '--type', type]);
  }

  /**
   * Deploy a blockchain agreement
   * @param {string} appPath - Path to the application
   * @param {string} agreementId - ID of the agreement
   * @returns {Promise} - Promise resolving with output or rejecting with error
   */
  deployAgreement(appPath, agreementId) {
    return this._runCommand(['agreement', appPath, '--deploy', '--id', agreementId]);
  }

  /**
   * Create a node cluster for decentralization
   * @param {string} appPath - Path to the application
   * @returns {Promise} - Promise resolving with output or rejecting with error
   */
  createNodeCluster(appPath) {
    return this._runCommand(['cluster', appPath, '--create', '--rpc', this.rpcUrl]);
  }

  /**
   * Check status of a MetaNode application
   * @param {string} appPath - Path to the application
   * @returns {Promise} - Promise resolving with output or rejecting with error
   */
  checkStatus(appPath) {
    return this._runCommand(['status', appPath]);
  }

  /**
   * Run a CLI command
   * @private
   * @param {Array} args - Arguments to pass to the CLI
   * @returns {Promise} - Promise resolving with output or rejecting with error
   */
  _runCommand(args) {
    return new Promise((resolve, reject) => {
      const cmd = spawn(this.cliPath, args, { stdio: 'pipe' });
      let stdout = '';
      let stderr = '';

      cmd.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      cmd.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      cmd.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(\`Command failed with code \${code}: \${stderr}\`));
        } else {
          resolve(stdout);
        }
      });
    });
  }
}

module.exports = MetaNodeSDK;
EOF

echo "Node.js package created successfully"

# Create Go SDK package
echo "Packaging Go SDK for integration with Geth..."
mkdir -p packaging/go/metanode
cp metanode-sdk/go/metanode.go packaging/go/metanode/
cat > packaging/go/metanode/go.mod << EOF
module github.com/metanode/metanode-sdk-go

go 1.18

require (
	github.com/ethereum/go-ethereum v1.10.17
)
EOF

cat > packaging/go/metanode/examples/basic_usage.go << EOF
package main

import (
	"fmt"
	"os"
	
	"github.com/metanode/metanode-sdk-go/metanode"
)

func main() {
	// Create a new MetaNode SDK instance
	sdk, err := metanode.NewSDK()
	if err != nil {
		fmt.Printf("Error initializing SDK: %v\n", err)
		os.Exit(1)
	}
	
	// Initialize the SDK
	err = sdk.Initialize()
	if err != nil {
		fmt.Printf("Error initializing SDK: %v\n", err)
		os.Exit(1)
	}
	
	// Initialize a new application
	appName := "example-app"
	err = sdk.InitApp(appName)
	if err != nil {
		fmt.Printf("Error initializing app: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Printf("Application %s initialized successfully!\n", appName)
	
	// Deploy the application
	err = sdk.DeployApp(appName)
	if err != nil {
		fmt.Printf("Error deploying app: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Println("Application deployed successfully!")
	
	// Check application status
	err = sdk.CheckStatus(appName)
	if err != nil {
		fmt.Printf("Error checking status: %v\n", err)
		os.Exit(1)
	}
}
EOF

echo "Go package created successfully"

# Create Docker image for easy deployment
echo "Creating Docker image for full infrastructure deployment..."
cat > packaging/docker/Dockerfile << EOF
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    nodejs \\
    npm \\
    golang \\
    git \\
    curl \\
    wget \\
    ipfs \\
    docker.io \\
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy MetaNode SDK
COPY . /app/metanode-sdk

# Install Python SDK
RUN cd /app/metanode-sdk && \\
    pip3 install -e .

# Install Node.js SDK
RUN cd /app/metanode-sdk && \\
    npm install -g

# Make CLI executable
RUN chmod +x /app/metanode-sdk/bin/metanode-cli-enhanced && \\
    ln -s /app/metanode-sdk/bin/metanode-cli-enhanced /usr/local/bin/metanode-cli

# Create volume for application data
VOLUME ["/data"]

# Expose ports
EXPOSE 8545 8546 8081 30303

# Set entrypoint
ENTRYPOINT ["metanode-cli"]
CMD ["--help"]
EOF

echo "Docker packaging complete"

# Create unified install script
cat > install_metanode_full_sdk.sh << EOF
#!/bin/bash
# MetaNode Full Infrastructure SDK Installer
# ------------------------------------------

echo "===== MetaNode Full Infrastructure SDK Installer ====="
echo "This script will install the complete MetaNode SDK with blockchain, IPFS, and agreement support."

# Check for dependencies
echo "Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 is required but not installed. Aborting."; exit 1; }

# Create installation directory
echo "Setting up installation directory..."
mkdir -p ~/metanode-sdk
cp -r metanode-sdk/* ~/metanode-sdk/

# Install Python package
echo "Installing Python package..."
cd ~/metanode-sdk
pip3 install -e .

# Create bin directory and symlinks
echo "Creating CLI links..."
mkdir -p ~/bin
chmod +x ~/metanode-sdk/bin/metanode-cli-enhanced
ln -sf ~/metanode-sdk/bin/metanode-cli-enhanced ~/bin/metanode-cli

# Add to PATH if not already there
if ! grep -q "export PATH=\\\$PATH:~/bin" ~/.bashrc; then
  echo 'export PATH=\$PATH:~/bin' >> ~/.bashrc
  source ~/.bashrc
fi

echo ""
echo "===== Installation Complete ====="
echo "MetaNode Full Infrastructure SDK has been installed successfully!"
echo ""
echo "To get started, run:"
echo "  metanode-cli init my-app"
echo ""
echo "For more information, visit: https://github.com/metanode/metanode-sdk"
echo ""
EOF

chmod +x install_metanode_full_sdk.sh

echo ""
echo "===== All Packages Created Successfully ====="
echo "The MetaNode Full Infrastructure SDK is now ready for distribution."
echo ""
echo "Python package (PyPI): ./packaging/pypi/"
echo "Node.js package (npm): ./packaging/npm/"
echo "Go package (Geth): ./packaging/go/"
echo "Docker package: ./packaging/docker/"
echo ""
echo "To install locally, run: ./install_metanode_full_sdk.sh"
echo ""
echo "To publish to distribution platforms:"
echo "- PyPI:  cd packaging/pypi && python setup.py upload"
echo "- npm:   cd packaging/npm && npm publish"
echo "- Go:    Push to your GitHub repository"
echo "- Docker: docker build -t metanode/full-sdk:latest packaging/docker/"
