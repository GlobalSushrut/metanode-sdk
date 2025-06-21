'use strict';

const { spawn, spawnSync } = require('child_process');
const path = require('path');

/**
 * MetaNode SDK - JavaScript wrapper for the Python SDK
 * This library bridges JavaScript applications to the Python-based MetaNode SDK
 */
class MetaNode {
  /**
   * Create a new MetaNode SDK instance
   */
  constructor() {
    this.initialized = this._checkPythonSdk();
  }

  /**
   * Check if the Python SDK is installed
   * @private
   * @returns {boolean} Whether Python SDK is installed
   */
  _checkPythonSdk() {
    try {
      const result = spawnSync('metanode-cli', ['--version'], {
        encoding: 'utf8',
        stdio: 'pipe'
      });
      
      return result.status === 0;
    } catch (error) {
      console.error('Error checking MetaNode SDK:', error.message);
      return false;
    }
  }

  /**
   * Execute a MetaNode command
   * @param {string} command - Command to execute
   * @param {Array} args - Command arguments
   * @returns {Promise} Promise that resolves with the command output
   */
  async execute(command, args = []) {
    if (!this.initialized) {
      throw new Error('MetaNode SDK is not properly installed');
    }

    return new Promise((resolve, reject) => {
      const fullArgs = [command, ...args];
      const process = spawn('metanode-cli', fullArgs, {
        encoding: 'utf8',
        stdio: 'pipe'
      });

      let stdout = '';
      let stderr = '';

      process.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      process.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve(stdout.trim());
        } else {
          reject(new Error(`Command failed with code ${code}: ${stderr}`));
        }
      });
    });
  }

  /**
   * Deploy an application to the MetaNode network
   * @param {string} appPath - Path to the application
   * @param {Object} options - Deployment options
   * @returns {Promise} Promise that resolves with deployment result
   */
  async deploy(appPath, options = {}) {
    const args = ['deploy'];
    
    if (options.testnet) {
      args.push('--testnet');
    }
    
    if (options.mainnet) {
      args.push('--mainnet');
    }
    
    if (options.cluster) {
      args.push('--cluster', options.cluster);
    }
    
    args.push(appPath);
    
    return this.execute(args.shift(), args);
  }

  /**
   * Create a new agreement
   * @param {string} appPath - Path to the application
   * @param {Object} options - Agreement options
   * @returns {Promise} Promise that resolves with agreement creation result
   */
  async createAgreement(appPath, options = {}) {
    const args = ['agreement', appPath, '--create'];
    
    if (options.name) {
      args.push('--name', options.name);
    }
    
    if (options.version) {
      args.push('--version', options.version);
    }
    
    if (options.parties) {
      args.push('--parties', options.parties.join(','));
    }
    
    return this.execute(args[0], args.slice(1));
  }

  /**
   * Connect to the testnet
   * @param {string} appPath - Path to the application
   * @returns {Promise} Promise that resolves with testnet connection result
   */
  async connectTestnet(appPath) {
    return this.execute('testnet', [appPath, '--setup']);
  }

  /**
   * Create a node cluster
   * @param {string} appPath - Path to the application
   * @returns {Promise} Promise that resolves with cluster creation result
   */
  async createNodeCluster(appPath) {
    return this.execute('testnet', [appPath, '--create-cluster']);
  }

  /**
   * Generate verification proofs
   * @param {string} appPath - Path to the application
   * @returns {Promise} Promise that resolves with proof generation result
   */
  async generateProofs(appPath) {
    return this.execute('testnet', [appPath, '--setup-proofs']);
  }

  /**
   * Create a MetaNode dApp from any application
   * @param {string} appPath - Path to the application
   * @param {Object} options - dApp creation options
   * @returns {Promise} Promise that resolves with dApp creation result
   */
  async createDapp(appPath, options = {}) {
    const args = ['--app', appPath];
    
    if (options.testnet) {
      args.push('--testnet');
    }
    
    if (options.mainnet) {
      args.push('--mainnet');
    }
    
    if (options.wallet) {
      args.push('--wallet', options.wallet);
    }
    
    return new Promise((resolve, reject) => {
      const process = spawn('metanode-deploy', args, {
        encoding: 'utf8',
        stdio: 'pipe'
      });

      let stdout = '';
      let stderr = '';

      process.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      process.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve(stdout.trim());
        } else {
          reject(new Error(`Command failed with code ${code}: ${stderr}`));
        }
      });
    });
  }
}

// Export the MetaNode class
module.exports = {
  MetaNode,
  createMetaNode: () => new MetaNode()
};
