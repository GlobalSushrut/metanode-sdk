#!/usr/bin/env node

'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log('📦 Setting up MetaNode SDK...');

// Detect if Python is available
function checkPythonInstallation() {
  console.log('🔍 Checking for Python installation...');
  
  try {
    const pythonCheck = spawnSync('python', ['-c', 'import sys; print(sys.version)'], {
      encoding: 'utf8',
      stdio: 'pipe'
    });
    
    if (pythonCheck.status === 0) {
      console.log(`✅ Python found: ${pythonCheck.stdout.trim()}`);
      return true;
    }
    
    // Try python3 if python fails
    const python3Check = spawnSync('python3', ['-c', 'import sys; print(sys.version)'], {
      encoding: 'utf8',
      stdio: 'pipe'
    });
    
    if (python3Check.status === 0) {
      console.log(`✅ Python3 found: ${python3Check.stdout.trim()}`);
      return true;
    }
    
    console.error('❌ Python not found. Please install Python 3.8 or higher.');
    return false;
  } catch (error) {
    console.error('❌ Error checking Python installation:', error.message);
    return false;
  }
}

// Install Python SDK if not already installed
function installPythonSDK() {
  console.log('📥 Installing MetaNode Python SDK...');
  
  try {
    const sdkPath = path.resolve(__dirname, '..');
    
    // Check if we should install in development mode
    const devMode = fs.existsSync(path.join(sdkPath, 'setup.py'));
    
    let installCommand;
    if (devMode) {
      console.log('🔧 Development mode detected, installing in editable mode...');
      installCommand = spawnSync('pip', ['install', '-e', '.'], {
        cwd: sdkPath,
        encoding: 'utf8',
        stdio: 'inherit'
      });
      
      // If pip fails, try pip3
      if (installCommand.status !== 0) {
        installCommand = spawnSync('pip3', ['install', '-e', '.'], {
          cwd: sdkPath,
          encoding: 'utf8',
          stdio: 'inherit'
        });
      }
    } else {
      // Install from PyPI
      installCommand = spawnSync('pip', ['install', 'metanode-sdk'], {
        encoding: 'utf8',
        stdio: 'inherit'
      });
      
      // If pip fails, try pip3
      if (installCommand.status !== 0) {
        installCommand = spawnSync('pip3', ['install', 'metanode-sdk'], {
          encoding: 'utf8',
          stdio: 'inherit'
        });
      }
    }
    
    if (installCommand.status === 0) {
      console.log('✅ MetaNode Python SDK installed successfully');
      return true;
    } else {
      console.error('❌ Failed to install MetaNode Python SDK');
      console.error('Please try manually with: pip install metanode-sdk');
      return false;
    }
  } catch (error) {
    console.error('❌ Error installing Python SDK:', error.message);
    return false;
  }
}

// Create wrapper scripts
function createWrapperScripts() {
  console.log('🔧 Creating command wrappers...');
  
  const binDir = path.join(__dirname, '..', 'bin');
  if (!fs.existsSync(binDir)) {
    fs.mkdirSync(binDir, { recursive: true });
  }
  
  const wrapperTemplate = (command) => `#!/usr/bin/env node

'use strict';

const { spawn } = require('child_process');
const process = require('process');

// Forward all arguments to the Python command
const args = process.argv.slice(2);
const pythonProcess = spawn('${command}', args, { 
  stdio: 'inherit',
  shell: true
});

pythonProcess.on('exit', (code) => {
  process.exit(code);
});
`;

  // Create wrapper scripts for each CLI command
  const commands = [
    { file: 'metanode-cli-wrapper.js', command: 'metanode-cli' },
    { file: 'metanode-agreement-wrapper.js', command: 'metanode agreement' },
    { file: 'metanode-testnet-wrapper.js', command: 'metanode testnet' },
    { file: 'metanode-deploy-wrapper.js', command: 'metanode-deploy' }
  ];
  
  commands.forEach(({ file, command }) => {
    const wrapperPath = path.join(binDir, file);
    fs.writeFileSync(wrapperPath, wrapperTemplate(command));
    
    // Make executable on Unix-like systems
    if (os.platform() !== 'win32') {
      fs.chmodSync(wrapperPath, '755');
    }
    
    console.log(`✅ Created wrapper for ${command}`);
  });
}

// Run the installation
async function run() {
  if (!checkPythonInstallation()) {
    console.log('⚠️  Please install Python 3.8+ to use MetaNode SDK');
    console.log('🌐 https://www.python.org/downloads/');
    return;
  }
  
  if (installPythonSDK()) {
    createWrapperScripts();
    console.log('🎉 MetaNode SDK setup complete!');
    console.log('📚 Documentation: https://github.com/metanode/metanode-sdk/docs');
  }
}

run();
