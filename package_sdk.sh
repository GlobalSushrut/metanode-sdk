#!/bin/bash
# Script to package the MetaNode SDK for distribution

set -e

echo "Packaging MetaNode SDK for distribution..."

# Create a clean build directory
rm -rf build/ dist/ *.egg-info/
echo "Cleaned build directories"

# Create source distribution
python3 setup.py sdist bdist_wheel
echo "Created source distribution and wheel"

# Show the created packages
echo "Created packages:"
ls -la dist/

echo "SDK packaging complete! You can install the package with:"
echo "pip install dist/metanode_sdk-*.whl"

echo "Or upload to PyPI with:"
echo "python -m twine upload dist/*"
