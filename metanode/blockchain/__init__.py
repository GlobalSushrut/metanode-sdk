"""
MetaNode SDK - Blockchain Module
============================

This module provides core blockchain functionality using the MetaNode architecture:
- ZK blockchain running in Kubernetes vPods clusters
- Integration with Ethereum mainnet/testnet networks
- Automated cluster management for blockchain nodes
- Secured validator, agreement, & consensus mechanisms
- Distributed immutable storage replacing traditional IPFS

Implements a fully automatic production-grade blockchain environment.
"""

from metanode.blockchain.core import (
    initialize_blockchain,
    connect_to_mainnet,
    connect_to_testnet,
)

from metanode.blockchain.storage import (
    store_data,
    retrieve_data,
    validate_data_integrity,
)

from metanode.blockchain.validator import (
    validate_agreement,
    register_validator,
    get_validator_status,
)

from metanode.blockchain.cluster import (
    create_vpod_cluster,
    configure_rpc_nodes,
    setup_communicator_node,
)

from metanode.blockchain.transaction import (
    create_transaction,
    sign_transaction,
    submit_transaction,
    get_transaction_status,
)
