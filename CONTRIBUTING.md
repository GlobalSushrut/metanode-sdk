# Contributing to MetaNode SDK

Thank you for your interest in contributing to the MetaNode SDK! This document provides guidelines and instructions for contributing to this project.

## Important Notice on Intellectual Property

Before contributing, please note that this project is released under a Proprietary License. By contributing to this project, you agree that:

1. You have the right to submit your contribution
2. Your contribution will be licensed under the project's Proprietary License
3. You will receive attribution for accepted contributions

## Code of Conduct

All contributors are expected to adhere to our code of conduct:

* Be respectful and inclusive
* Focus on constructive feedback
* Avoid personal attacks
* Maintain professionalism in all communications

## Getting Started

### Prerequisites

* Python 3.8 or higher
* Docker (for testing container functionality)
* Kubernetes (optional, for testing K8s integration)

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/metanode-sdk.git
   cd metanode-sdk
   ```

3. Set up the development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Making Changes

1. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards
3. Write or update tests as necessary
4. Run the test suite to ensure all tests pass
5. Update documentation as needed

## Coding Standards

* Follow PEP 8 style guidelines
* Write clear, descriptive commit messages
* Include docstrings for all functions and classes
* Maintain test coverage for your code

## Testing

Run the test suite with:

```bash
pytest
```

## Submitting Changes

1. Push your changes to your fork
2. Create a pull request against our main branch
3. Describe your changes in detail
4. Link any relevant issues

## Review Process

All submissions will go through a review process:

1. Code review by maintainers
2. Automated testing via CI/CD
3. Documentation review when applicable
4. Possible revision requests

## Documentation

When adding or modifying features, please update the relevant documentation:

* Update the README.md if needed
* Add or update documentation in the docs/ directory
* Include code examples for new features

## Additional Resources

* [Issue Tracker](https://github.com/metanode/metanode-sdk/issues)
* [Documentation](https://github.com/metanode/metanode-sdk/docs)

Thank you for contributing to the MetaNode SDK!
