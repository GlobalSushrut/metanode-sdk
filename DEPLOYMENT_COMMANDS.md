# MetaNode SDK Deployment Commands

Use these step-by-step commands to deploy the MetaNode SDK to GitHub, PyPI, and npm.

## 1. Deploy to GitHub

```bash
# Ensure you're in the SDK directory
cd /home/umesh/Videos/vKuber9/metanode-sdk

# Configure Git (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Create GitHub repository using GitHub CLI
gh repo create metanode-sdk --public --description "Blockchain & dApp Deployment Infrastructure with vPod Container Integration" --source=.

# OR add the remote and push manually
git remote add origin https://github.com/YOUR_USERNAME/metanode-sdk.git
git push -u origin main

# Create a release tag for version 1.1.0
git tag -a v1.1.0 -m "Initial release of MetaNode SDK with blockchain integration and vPod containers"
git push origin v1.1.0

# Create a GitHub release with the tag (optional)
gh release create v1.1.0 --title "MetaNode SDK v1.1.0" --notes "Initial release with blockchain integration and vPod container technology"
```

## 2. Deploy to PyPI

```bash
# Clean previous builds
cd /home/umesh/Videos/vKuber9/metanode-sdk
rm -rf dist/ build/ *.egg-info/

# Build the package
python3 -m pip install --upgrade build twine
python3 -m build

# Upload to PyPI (you'll need PyPI credentials)
python3 -m twine upload dist/*

# If you need to create a PyPI account first:
# 1. Go to https://pypi.org/account/register/
# 2. Complete registration
# 3. Create an API token at https://pypi.org/manage/account/token/
```

## 3. Deploy to npm

```bash
# Ensure you're in the SDK directory
cd /home/umesh/Videos/vKuber9/metanode-sdk

# Log in to npm (if not already logged in)
npm login

# Publish to npm
npm publish

# If you need to create an npm account first:
# 1. Go to https://www.npmjs.com/signup
# 2. Complete registration
# 3. Run npm login
```

## 4. Verify Installations

After publishing, verify that your packages can be installed:

```bash
# Python package
pip install metanode-sdk

# npm package
npm install metanode-sdk
```

## Important Notes

- Make sure your GitHub, PyPI, and npm accounts are properly set up
- The package versions in setup.py and package.json should match (1.1.0)
- Your PyPI and npm accounts should have verified email addresses
- For PyPI, the license classifier has been set to "OSI Approved :: MIT License" for compatibility
- Remember to keep your npm and PyPI tokens secure

## Post-Deployment Tasks

1. Update documentation links with the actual GitHub repository URL
2. Configure GitHub Actions for automatic publishing
3. Set up the GitHub Pages site for comprehensive documentation
4. Add badges to your README.md showing package versions and build status
