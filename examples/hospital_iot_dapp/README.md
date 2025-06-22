# Hospital IoT Manager dApp Demo

This demo showcases how the Hospital IoT Manager decentralized application (dApp) functions with blockchain interactions using the MetaNode SDK, while maintaining a Web2-like user experience.

## Overview

The Hospital IoT Manager dApp demonstrates how healthcare institutions can leverage blockchain technology to:

1. Connect to the blockchain testnet
2. Create and manage healthcare data agreements
3. Deploy decentralized agents for medical data verification
4. Register and manage IoT medical devices
5. Process real-time patient vital signs with anomaly detection
6. Store and retrieve medical data with blockchain verification
7. Generate medical alerts based on vital sign thresholds

## Features

- **Blockchain Connection**: Connects to the MetaNode testnet at `http://159.203.17.36:8545` 
- **Decentralized Agents**: Creates blockchain-verified agents for medical data verification
- **IoT Device Management**: Registers medical devices with blockchain verification
- **Real-time Monitoring**: Processes vital signs data with anomaly detection
- **Patient History**: Maintains blockchain-verified patient health records
- **Medical Alerts**: Generates warnings when patient vitals exceed safe thresholds

## Demo Components

- `hospital_mini_core.py` - Core utilities and helper functions
- `hospital_mini_dapp.py` - Main Hospital IoT Manager dApp class with blockchain connection
- `hospital_mini_device.py` - Device registration and management functionality
- `run_hospital_demo_mini.py` - Complete demo runner with data handling methods
- `demo_output.log` - Sample output from a demo execution

## Running the Demo

```bash
# Make the demo runner executable
chmod +x run_hospital_demo_mini.py

# Run the demo
python3 run_hospital_demo_mini.py
```

## Demo Workflow

The demo simulates a complete workflow for a hospital IoT system:

1. Blockchain connection and agreement setup
2. Decentralized agent creation for data verification
3. IoT medical device registration
4. Real-time vital signs data processing
5. Anomaly detection and alert generation
6. Patient history retrieval

## Integration with MetaNode SDK

This demo integrates with several MetaNode SDK modules:

- **Blockchain Core**: Connection to testnet using `BlockchainConfig`
- **Ledger Agreement**: Creation and deployment of blockchain agreements
- **Decentralized Agents**: Creation and management of data verification agents
- **Blockchain Storage**: Secure storage and retrieval of medical data

## Deployed dApp Behavior

When deployed, the Hospital IoT Manager dApp provides a Web2-like interface while handling blockchain operations behind the scenes:

- Structured JSON responses with consistent formatting
- Clear status codes for normal operations and alerts
- Blockchain transaction references included in responses
- Seamless blockchain storage and retrieval

## Related Documentation

See the following documentation for more information:

- [01. Introduction and Installation](../../docs/01_introduction_and_installation.md)
- [02. Agreement Creation and Deployment](../../docs/02_agreement_creation_deployment.md)
- [03. Blockchain Connection and Verification](../../docs/03_blockchain_connection_verification.md)
- [04. Data Storage and Retrieval](../../docs/04_data_storage_retrieval.md)
- [05. Decentralized Agent Creation](../../docs/05_decentralized_agent_creation.md)

## Notes on Implementation

This demo simulates blockchain interactions to showcase the behavior of the dApp. In a production deployment:

- Real blockchain transactions are executed using the MetaNode SDK
- Integration with the enhanced MetaNode CLI for blockchain interaction
- Full Kubernetes deployment using vPod containers
- Multi-layer infrastructure automation for blockchain, ledger, validator, and storage layers

## Future Enhancements

- Integration with real MetaNode SDK blockchain calls
- CLI tool integration for hospital dApp deployment
- Kubernetes vPod deployment automation
- Zero-knowledge proofs for patient data privacy
- Multi-node consensus for medical data verification
