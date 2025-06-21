"""
MetaNode SDK - CLI Module
========================

Command-line interface for the MetaNode SDK. Provides access to wallet management,
testnet operations, Kubernetes deployment, and utility functions.
"""

from .main import app as cli
from .commands import (
    K8sCommands,
    SecurityCommands,
    IPFSCommands,
    ZKProofCommands
)

__all__ = [
    'cli',
    'K8sCommands',
    'SecurityCommands', 
    'IPFSCommands',
    'ZKProofCommands'
]
