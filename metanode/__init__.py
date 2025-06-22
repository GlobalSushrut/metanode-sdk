"""
MetaNode SDK - Next-generation Blockchain Infrastructure

A complete console-based SDK for building, deploying, and interacting with MetaNode's blockchain-grade federated computing system.
"""

from typing import List

__version__ = "0.1.0"

from .cli import main

__all__: List[str] = [
    "main",
]
