# MetaNode SDK Publishing Guide

This guide will walk you through publishing the MetaNode SDK to GitHub, PyPI, and npm.

## 1. Create GitHub Repository

1. Go to [GitHub](https://github.com/) and sign in to your account
2. Click on the "+" icon in the top-right corner and select "New repository"
3. Enter the repository name: `metanode-sdk`
4. Add a description: "Blockchain & dApp Deployment Infrastructure with vPod Container Integration"
5. Choose "Public" visibility
6. Do NOT initialize with README, .gitignore, or license (we already have these files)
7. Click "Create repository"

## 2. Push Your Code to GitHub

After creating the repository, GitHub will show instructions for pushing existing code. Run the following commands:

```bash
# Make sure you're in the metanode-sdk directory
cd /home/umesh/Videos/vKuber9/metanode-sdk

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/metanode-sdk.git

# Push your code to GitHub
git push -u origin main
```

## 3. Create a Release Tag for Publishing

Create a version tag for automatic publishing:

```bash
# Create a tag for version 1.1.0
git tag -a v1.1.0 -m "Initial release with blockchain integration and vPod containers"

# Push the tag to GitHub
git push origin v1.1.0
```

## 4. Publish to PyPI

1. Register on [PyPI](https://pypi.org/) if you haven't already
2. Create an API token on PyPI for secure publishing
3. Run the following commands:

```bash
# Install build tools
pip install --upgrade build twine

# Build the distribution packages
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

You will be prompted for your PyPI username and password (or token).

## 5. Publish to npm

1. Register on [npm](https://www.npmjs.com/) if you haven't already
2. Log in to npm from the command line:

```bash
npm login
```

3. Publish the package:

```bash
npm publish
```

## 6. Additional Publishing Options

### Using GitHub Actions for Automated Publishing

The repository is already set up with GitHub Actions workflows in `.github/workflows/publish.yml` that will automatically publish to PyPI and npm when you push a version tag (e.g., v1.1.0).

To use this workflow:

1. Go to your GitHub repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add the following secrets:
   - `PYPI_USERNAME`: Your PyPI username
   - `PYPI_PASSWORD`: Your PyPI password or token
   - `NPM_TOKEN`: Your npm access token

### Using the Build Script

A comprehensive build script is included that prepares releases for both PyPI and npm:

```bash
# Make the script executable
chmod +x scripts/build.sh

# Run the build script
./scripts/build.sh
```

This script will:
- Check dependencies
- Clean previous builds
- Run tests
- Build both PyPI and npm packages
- Verify package integrity
