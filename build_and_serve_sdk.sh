#!/bin/bash
# MetaNode SDK Build, Test and Server Script
# This script automates the process of building, testing, and serving the MetaNode SDK.

set -e  # Exit on any error

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Define paths
SDK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILD_DIR="${SDK_DIR}/dist"
SERVER_DIR="${SDK_DIR}/sdk-server"
DOWNLOAD_DIR="${SERVER_DIR}/download"
VENV_DIR="${SDK_DIR}/.venv"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}MetaNode SDK Build and Deployment Tool${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Function to handle errors
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" 1>&2
    exit 1
}

# Check if we're running in a Python virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}No virtual environment detected. Creating one...${NC}"
    
    # Check if python3 and venv are available
    if ! command -v python3 &> /dev/null; then
        error_exit "python3 is not installed. Please install it first."
    fi
    
    if ! python3 -c "import venv" &> /dev/null; then
        error_exit "python3-venv is not installed. Please install it first."
    fi
    
    # Create virtual environment if it doesn't exist
    if [[ ! -d "$VENV_DIR" ]]; then
        echo -e "${BLUE}Creating virtual environment...${NC}"
        python3 -m venv "$VENV_DIR" || error_exit "Failed to create virtual environment"
    fi
    
    # Activate virtual environment
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source "$VENV_DIR/bin/activate" || error_exit "Failed to activate virtual environment"
else
    echo -e "${GREEN}Using existing virtual environment: $VIRTUAL_ENV${NC}"
fi

# Install build dependencies
echo -e "${BLUE}Installing build dependencies...${NC}"
pip install --upgrade pip wheel setuptools twine build || error_exit "Failed to install build dependencies"

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf "${BUILD_DIR}" "${SDK_DIR}/*.egg-info"

# Build the package
echo -e "${BLUE}Building the MetaNode SDK package...${NC}"
python -m build || error_exit "Failed to build the package"

# Copy packages to the download directory
echo -e "${BLUE}Copying packages to download directory...${NC}"
mkdir -p "${DOWNLOAD_DIR}"
cp "${BUILD_DIR}"/*.whl "${DOWNLOAD_DIR}/" || error_exit "Failed to copy wheel package"
cp "${BUILD_DIR}"/*.tar.gz "${DOWNLOAD_DIR}/" || error_exit "Failed to copy source package"

# Install the package for testing
echo -e "${BLUE}Installing the package for testing...${NC}"
pip install --force-reinstall "${BUILD_DIR}"/*.whl || error_exit "Failed to install the package"

# Run the test script
echo -e "${BLUE}Running tests...${NC}"
python "${SDK_DIR}/test_sdk.py" -v || error_exit "Tests failed"

# Start the SDK download server
echo -e "${BLUE}Starting SDK download server...${NC}"
echo -e "${GREEN}The SDK download server will be available at: http://localhost:8000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"

# Change to the server directory and start a simple HTTP server
cd "${SERVER_DIR}"
python -m http.server 8000
