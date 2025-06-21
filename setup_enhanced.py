#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

# Package meta-data
NAME = "metanode-sdk-full"
DESCRIPTION = "MetaNode Full Infrastructure SDK with Blockchain, IPFS, and Agreement Support"
URL = "https://github.com/metanode/metanode-sdk"
EMAIL = "info@metanode.io"
AUTHOR = "MetaNode Team"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "1.1.0"

# Required packages
REQUIRED = [
    "requests>=2.25.0",
    "web3>=5.20.0",
    "pyyaml>=5.4.1",
    "docker>=5.0.0",
    "kubernetes>=12.0.0",
    "ipfshttpclient>=0.8.0",
    "eth-account>=0.5.6",
    "eth-keys>=0.3.3",
    "solc-select>=1.0.0",
    "py-solc-x>=1.1.1",
    "jsonschema>=3.2.0",
    "psutil>=5.8.0",
    "argparse>=1.4.0",
    "python-dotenv>=0.17.1",
]

# Optional packages
EXTRAS = {
    "dev": [
        "pytest>=6.0.0",
        "black>=21.5b2",
        "flake8>=3.9.2",
        "isort>=5.8.0",
    ],
    "ipfs": ["ipfshttpclient>=0.8.0"],
    "blockchain": [
        "web3>=5.20.0",
        "eth-account>=0.5.6",
        "eth-keys>=0.3.3",
    ],
    "kubernetes": ["kubernetes>=12.0.0"],
}

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Script executables to be installed
scripts = [
    "bin/metanode-cli",
    "bin/metanode-cli-agreement",
    "bin/metanode-cli-testnet",
    "bin/metanode-cli-main",
    "bin/metanode-cli-enhanced",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    scripts=scripts,
    entry_points={
        "console_scripts": [
            "metanode=metanode.cli:main",
            "metanode-agreement=metanode.agreement.cli:main",
            "metanode-testnet=metanode.testnet.cli:main",
            "metanode-deploy=metanode.deploy.cli:main",
        ],
    },
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Networking",
    ],
    project_urls={
        "Documentation": "https://metanode-sdk.readthedocs.io",
        "Source": "https://github.com/metanode/metanode-sdk",
        "Bug Reports": "https://github.com/metanode/metanode-sdk/issues",
    },
)
