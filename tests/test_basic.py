"""
Basic tests for the MetaNode SDK to ensure CI pipeline passes.
"""
import os
import sys

# Add the parent directory to the path so we can import metanode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import metanode


def test_package_init():
    """Test that the package can be imported."""
    assert hasattr(metanode, "__version__")


def test_basic_import():
    """Test that the package can be imported."""
    import metanode
    assert metanode is not None


def test_hospital_iot_demo_files_exist():
    """Test that the Hospital IoT Manager dApp demo files exist."""
    demo_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "examples",
        "hospital_iot_dapp"
    )
    assert os.path.isdir(demo_dir)
    
    # Check for essential demo files
    essential_files = [
        "README.md",
        "hospital_mini_core.py",
        "hospital_mini_dapp.py",
        "hospital_mini_device.py",
        "run_hospital_demo_mini.py"
    ]
    
    for file in essential_files:
        file_path = os.path.join(demo_dir, file)
        assert os.path.isfile(file_path), f"File {file} missing from hospital_iot_dapp demo"
