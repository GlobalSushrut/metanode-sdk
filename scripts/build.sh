#!/bin/bash

# MetaNode SDK Build Script
# This script prepares releases for both PyPI and npm

set -e

# Colors
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     MetaNode SDK Release Preparation Tool    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"

# Check dependencies
echo -e "\n${YELLOW}Checking dependencies...${NC}"

# Check Python
python --version >/dev/null 2>&1 || { echo -e "${RED}Python not found. Please install Python 3.8+${NC}"; exit 1; }
echo -e "${GREEN}✓ Python found$(python --version 2>&1)${NC}"

# Check pip
pip --version >/dev/null 2>&1 || { echo -e "${RED}pip not found. Please install pip${NC}"; exit 1; }
echo -e "${GREEN}✓ pip found$(pip --version)${NC}"

# Check npm
npm --version >/dev/null 2>&1 || { echo -e "${RED}npm not found. Please install npm${NC}"; exit 1; }
echo -e "${GREEN}✓ npm found$(npm --version)${NC}"

# Check build tools
python -m pip install --upgrade pip build twine wheel pytest >/dev/null 2>&1 || { echo -e "${RED}Failed to install Python build tools${NC}"; exit 1; }
echo -e "${GREEN}✓ Python build tools installed${NC}"

# Clean previous builds
echo -e "\n${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info/
echo -e "${GREEN}✓ Cleaned previous builds${NC}"

# Run tests
echo -e "\n${YELLOW}Running tests...${NC}"
pytest -xvs || { echo -e "${RED}Tests failed${NC}"; exit 1; }
echo -e "${GREEN}✓ Tests passed${NC}"

# Build Python package
echo -e "\n${YELLOW}Building Python package...${NC}"
python -m build || { echo -e "${RED}Failed to build Python package${NC}"; exit 1; }
echo -e "${GREEN}✓ Built Python package${NC}"

# Build npm package
echo -e "\n${YELLOW}Building npm package...${NC}"
npm run build || { echo -e "${RED}Failed to build npm package${NC}"; exit 1; }
echo -e "${GREEN}✓ Built npm package${NC}"

# Check PyPI package
echo -e "\n${YELLOW}Checking PyPI package...${NC}"
twine check dist/* || { echo -e "${RED}PyPI package check failed${NC}"; exit 1; }
echo -e "${GREEN}✓ PyPI package verified${NC}"

echo -e "\n${GREEN}Build completed successfully!${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}To publish to PyPI:${NC} python -m twine upload dist/*"
echo -e "${YELLOW}To publish to npm:${NC} npm publish"
echo -e "${BLUE}═════════════════════════════════════════════════${NC}"
