"""
MetaNode dApp Integration SDK
===========================
Transform any application into a decentralized application with blockchain properties
"""

# Import connector and transformers
from .connector import DAppConnector
from .docker_transformer import DockerTransformer
from .k8s_transformer import K8sTransformer
from .agent import DecentralizedAgent
from .templates import get_template

# Import API functions for easy use
from .api import make_dapp, deploy_dapp, create_agent, execute_immutable_action, check_blockchain_connection

__all__ = [
    # Main classes
    'DAppConnector', 
    'DockerTransformer',
    'K8sTransformer',
    'DecentralizedAgent',
    'get_template',
    
    # API functions
    'make_dapp',
    'deploy_dapp',
    'create_agent',
    'execute_immutable_action',
    'check_blockchain_connection'
]
