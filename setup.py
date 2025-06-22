#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    url="https://github.com/metanode/metanode-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/metanode/metanode-sdk/issues",
        "Documentation": "https://github.com/metanode/metanode-sdk/docs",
        "Source Code": "https://github.com/metanode/metanode-sdk",
    },
    name="metanode-sdk",
    version="1.1.0",
    description="MetaNode SDK - Blockchain & dApp Deployment Infrastructure",
    long_description="""
    MetaNode SDK provides a complete blockchain-grade infrastructure for secure,
    lightweight federated computing and automated dApp deployments. It includes wallet management, 
    mining console, mainnet deployment, cloud resource management tools, and secure 
    Kubernetes integration for testnet and application deployment.
    
    The SDK now supports automatic transformation of any application into a decentralized
    application (dApp) with blockchain properties using the successful vPod container approach.
    Applications can be automatically deployed to mainnet or testnet with proper docker.lock
    and Kubernetes blockchain cluster integration.
    """,
    author="MetaNode Foundation",
    author_email="dev@metanode.network",
    packages=find_packages(),
    install_requires=[
        "typer>=0.7.0",
        "rich>=12.0.0",
        "pyyaml>=5.4.1,<6.0",  # Use PyYAML <6.0 for docker-compose compatibility
        "cryptography>=38.0.0",
        "requests>=2.28.0",
        "urllib3<2.0.0",  # Added to ensure blockchain testnet compatibility
        "pydantic>=1.9.0",
        "click>=8.0.0",
        "kubernetes>=26.1.0,<28.0.0",
        "ipfshttpclient==0.8.0a2",
        "base58>=2.1.1",
        "web3>=6.0.0",
        "eth-account>=0.7.0",  # Required for blockchain transaction signing
        "eth-utils>=2.1.0",  # Required for blockchain data processing
        "merklelib>=1.0.0",  # Required for blockchain verification proofs
        "websockets>=11.0.0", # Required for testnet connections
        "sshpass>=1.0.6"
    ],
    package_data={
        'metanode': [
            'k8s-deployment/*.yaml',
            'dapp/templates/*.yaml',
            'dapp/templates/*.yml',
            'dapp/templates/*.json',
        ],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "metanode=metanode.cli.main:app",
            "metanode-cli=metanode.cli.main:app",
            "metanode-miner=metanode.mining.console:main",
            "metanode-wallet=metanode.wallet.cli:main",
            "metanode-cloud=metanode.cloud.cli:main",
            "metanode-k8s=metanode.cli.main:k8s_app",
            "metanode-deploy=metanode.deployment.auto_deploy_agent:cli_main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    keywords=["blockchain", "dapp", "federated computing", "web3", "docker", "kubernetes", "decentralized"],
    zip_safe=False,
)
