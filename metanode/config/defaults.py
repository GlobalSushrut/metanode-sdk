# Default configuration for MetaNode SDK
# This file configures the default endpoints for testnet connection

# Testnet configuration - pointing to our deployed server
TESTNET_API_ENDPOINT = "http://159.203.17.36/api"
TESTNET_EXPLORER_URL = "http://159.203.17.36/explorer"
TESTNET_FAUCET_URL = "http://159.203.17.36/faucet"
TESTNET_IPFS_GATEWAY = "http://159.203.17.36/ipfs"
TESTNET_SDK_DOWNLOAD = "http://159.203.17.36/download"

# Default network configuration
DEFAULT_NETWORK = "testnet"

# API server configuration
API_SERVER_HOST = "0.0.0.0"  # Listen on all interfaces
API_SERVER_PORT = 8000

# Console mode settings
CONSOLE_MODE = True
USE_EXISTING_VPOD = True  # Use existing Docker vPod containers

# SDK version
SDK_VERSION = "1.0.0-beta"
