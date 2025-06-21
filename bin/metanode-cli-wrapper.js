#!/usr/bin/env node

/**
 * MetaNode CLI - JavaScript wrapper for the Python CLI
 * This provides a seamless interface for JavaScript/Node.js developers
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { Command } = require('commander');
const chalk = require('chalk');
const ora = require('ora');

// Find Python CLI script
const pythonCLI = path.join(__dirname, 'metanode-cli-enhanced');

// Check if the CLI exists
if (!fs.existsSync(pythonCLI)) {
  console.error(chalk.red('MetaNode CLI not found. Please ensure the SDK is installed correctly.'));
  process.exit(1);
}

// Parse arguments
const program = new Command();

program
  .version('1.1.0')
  .description(chalk.blue('MetaNode Full Infrastructure SDK with Blockchain, IPFS, and Agreement Support'))
  .usage('<command> [options]');

// Pass all arguments to the Python CLI
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log(chalk.yellow('MetaNode SDK - Full Infrastructure Edition'));
  console.log(chalk.gray('Run with --help to see available commands'));
  process.exit(0);
}

// Spinner for long-running commands
const spinner = ora('Processing command...').start();

// Execute Python CLI with passed arguments
const python = spawn('python3', [pythonCLI, ...args], { 
  stdio: 'pipe',  // Capture output
});

// Handle stdout
python.stdout.on('data', (data) => {
  // Stop spinner when getting first output
  if (spinner.isSpinning) {
    spinner.stop();
  }
  process.stdout.write(data.toString());
});

// Handle stderr
python.stderr.on('data', (data) => {
  // Stop spinner when getting first error
  if (spinner.isSpinning) {
    spinner.stop();
  }
  process.stderr.write(chalk.red(data.toString()));
});

// Handle process exit
python.on('close', (code) => {
  if (spinner.isSpinning) {
    spinner.stop();
  }
  
  if (code !== 0) {
    console.log(chalk.red(`\nCommand failed with exit code ${code}`));
  } else {
    console.log(chalk.green('\nCommand completed successfully.'));
  }
});
