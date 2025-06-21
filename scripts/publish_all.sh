#!/bin/bash

# MetaNode SDK Complete Publishing Script
# This script handles the entire process of publishing to GitHub, PyPI, and npm

set -e

# Colors for output
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

echo -e "${BLUE}╔═════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     MetaNode SDK Complete Publishing Tool       ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════╝${NC}"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI (gh) is not installed. Please install it first.${NC}"
    echo -e "Installation instructions: https://github.com/cli/cli#installation"
    exit 1
fi

echo -e "\n${YELLOW}Checking GitHub authentication...${NC}"
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Not authenticated with GitHub. Please login first.${NC}"
    echo -e "${YELLOW}Run: gh auth login${NC}"
    exit 1
fi
echo -e "${GREEN}✓ GitHub authentication verified${NC}"

# Check dependencies
echo -e "\n${YELLOW}Checking dependencies...${NC}"

# Check Python
python3 --version >/dev/null 2>&1 || { echo -e "${RED}Python3 not found${NC}"; exit 1; }
echo -e "${GREEN}✓ Python found$(python3 --version 2>&1)${NC}"

# Check pip
pip3 --version >/dev/null 2>&1 || { echo -e "${RED}pip3 not found${NC}"; exit 1; }
echo -e "${GREEN}✓ pip found$(pip3 --version)${NC}"

# Check npm
npm --version >/dev/null 2>&1 || { echo -e "${RED}npm not found${NC}"; exit 1; }
echo -e "${GREEN}✓ npm found$(npm --version)${NC}"

# Check twine
python3 -m pip install --upgrade twine >/dev/null 2>&1
echo -e "${GREEN}✓ twine installed/updated${NC}"

# Verify git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Not a git repository. Please run from the root of the metanode-sdk repository.${NC}"
    exit 1
fi

# Get version
VERSION=$(python3 -c "from setuptools import setup; import sys; sys.argv=['setup.py', '--version']; setup()" 2>/dev/null || echo "1.1.0")
echo -e "${GREEN}✓ SDK Version: ${VERSION}${NC}"

# 1. Create GitHub repository if it doesn't exist
echo -e "\n${YELLOW}Setting up GitHub repository...${NC}"

GITHUB_USERNAME=$(gh api user | jq -r '.login')
REPO_NAME="metanode-sdk"

# Check if repository exists
if ! gh repo view "${GITHUB_USERNAME}/${REPO_NAME}" &>/dev/null; then
    echo -e "${YELLOW}Creating GitHub repository: ${GITHUB_USERNAME}/${REPO_NAME}${NC}"
    gh repo create "${REPO_NAME}" --public --description "Blockchain & dApp Deployment Infrastructure with vPod Container Integration" --source=.
    echo -e "${GREEN}✓ GitHub repository created${NC}"
else
    echo -e "${GREEN}✓ GitHub repository already exists${NC}"
    
    # Configure remote if not already set
    if ! git remote | grep -q "origin"; then
        git remote add origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
        echo -e "${GREEN}✓ Git remote 'origin' added${NC}"
    else
        echo -e "${GREEN}✓ Git remote 'origin' already configured${NC}"
    fi
fi

# 2. Push to GitHub if needed
echo -e "\n${YELLOW}Pushing to GitHub...${NC}"

# Make sure we're on the main branch
git branch -M main

# Add all files if there are changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Changes detected, committing...${NC}"
    git add .
    git commit -m "Prepare v${VERSION} for publishing to PyPI and npm"
    echo -e "${GREEN}✓ Changes committed${NC}"
fi

# Push to GitHub
git push -u origin main
echo -e "${GREEN}✓ Code pushed to GitHub${NC}"

# 3. Create a version tag if it doesn't exist
echo -e "\n${YELLOW}Creating version tag...${NC}"

TAG_NAME="v${VERSION}"
if ! git tag -l | grep -q "^${TAG_NAME}$"; then
    git tag -a "${TAG_NAME}" -m "Release version ${VERSION}"
    git push origin "${TAG_NAME}"
    echo -e "${GREEN}✓ Created and pushed tag ${TAG_NAME}${NC}"
else
    echo -e "${GREEN}✓ Tag ${TAG_NAME} already exists${NC}"
fi

# 4. Clean build artifacts
echo -e "\n${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info/
echo -e "${GREEN}✓ Build directories cleaned${NC}"

# 5. Build and publish to PyPI
echo -e "\n${YELLOW}Building and publishing to PyPI...${NC}"

# Build the package
python3 -m pip install --upgrade build
python3 -m build
echo -e "${GREEN}✓ Python package built${NC}"

# Check if the user wants to publish to PyPI
echo -e "${YELLOW}Do you want to publish to PyPI now? (y/n)${NC}"
read -r PUBLISH_PYPI

if [[ $PUBLISH_PYPI == "y" || $PUBLISH_PYPI == "Y" ]]; then
    echo -e "${YELLOW}Publishing to PyPI...${NC}"
    python3 -m twine upload dist/*
    echo -e "${GREEN}✓ Published to PyPI${NC}"
else
    echo -e "${YELLOW}Skipping PyPI publishing${NC}"
    echo -e "To publish later, run: python3 -m twine upload dist/*"
fi

# 6. Publish to npm
echo -e "\n${YELLOW}Preparing npm package...${NC}"

# Copy npm-README.md to package directory as README.md (temporarily)
if [ -f "npm-README.md" ]; then
    cp README.md README.md.bak
    cp npm-README.md README.md
    echo -e "${GREEN}✓ npm README prepared${NC}"
fi

# Check if the user wants to publish to npm
echo -e "${YELLOW}Do you want to publish to npm now? (y/n)${NC}"
read -r PUBLISH_NPM

if [[ $PUBLISH_NPM == "y" || $PUBLISH_NPM == "Y" ]]; then
    echo -e "${YELLOW}Publishing to npm...${NC}"
    npm publish
    echo -e "${GREEN}✓ Published to npm${NC}"
else
    echo -e "${YELLOW}Skipping npm publishing${NC}"
    echo -e "To publish later, run: npm publish"
fi

# Restore original README
if [ -f "README.md.bak" ]; then
    mv README.md.bak README.md
    echo -e "${GREEN}✓ Original README restored${NC}"
fi

# 7. Create a GitHub release
echo -e "\n${YELLOW}Creating GitHub release...${NC}"

RELEASE_NOTES="# MetaNode SDK v${VERSION}
## Blockchain & dApp Deployment Infrastructure

### Features
- Smart Agreement Management with blockchain integration
- Transaction Management, creation, signing, and submission
- Docker vPod Technology with console-based workflows
- Testnet connectivity with blockchain verification
- Node Cluster Creation for enhanced decentralization
- Kubernetes Integration for scalable deployment

### Installation
- PyPI: \`pip install metanode-sdk\`
- npm: \`npm install metanode-sdk\`

See full documentation at: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/tree/main/docs"

echo -e "${YELLOW}Do you want to create a GitHub release now? (y/n)${NC}"
read -r CREATE_RELEASE

if [[ $CREATE_RELEASE == "y" || $CREATE_RELEASE == "Y" ]]; then
    echo -e "${YELLOW}Creating GitHub release...${NC}"
    echo "$RELEASE_NOTES" > release_notes.tmp
    gh release create "${TAG_NAME}" --title "MetaNode SDK v${VERSION}" --notes-file release_notes.tmp
    rm release_notes.tmp
    echo -e "${GREEN}✓ GitHub release created${NC}"
else
    echo -e "${YELLOW}Skipping GitHub release creation${NC}"
    echo -e "To create a release later, visit: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/releases/new"
fi

echo -e "\n${GREEN}✅ Publishing process completed!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "GitHub Repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo -e "PyPI Package: https://pypi.org/project/metanode-sdk/"
echo -e "npm Package: https://www.npmjs.com/package/metanode-sdk"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
