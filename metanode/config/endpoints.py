#!/usr/bin/env python3
"""
MetaNode SDK Endpoint Configuration
==================================

Default endpoints and URL building for MetaNode services.
"""

# Default server
DEFAULT_SERVER = "159.203.17.36"

# Default ports
API_PORT = 8000
BLOCKCHAIN_PORT = 8545
WALLET_PORT = 8080
MINING_PORT = 8090
BFR_PORT = 9000
VALIDATOR_PORT = 9001

# Default URLs
API_URL = f"http://{DEFAULT_SERVER}:{API_PORT}"
BLOCKCHAIN_URL = f"http://{DEFAULT_SERVER}:{BLOCKCHAIN_PORT}"
WALLET_URL = f"http://{DEFAULT_SERVER}:{WALLET_PORT}"
MINING_URL = f"http://{DEFAULT_SERVER}:{MINING_PORT}/health.json"
BFR_URL = f"http://{DEFAULT_SERVER}:{BFR_PORT}"
VALIDATOR_URL = f"http://{DEFAULT_SERVER}:{VALIDATOR_PORT}"

def build_urls(server: str = DEFAULT_SERVER) -> dict:
    """Build endpoint URLs for a given server"""
    return {
        "api": f"http://{server}:{API_PORT}",
        "blockchain": f"http://{server}:{BLOCKCHAIN_PORT}",
        "wallet": f"http://{server}:{WALLET_PORT}",
        "mining": f"http://{server}:{MINING_PORT}/health.json",
        "bfr": f"http://{server}:{BFR_PORT}",
        "validator": f"http://{server}:{VALIDATOR_PORT}",
    }
