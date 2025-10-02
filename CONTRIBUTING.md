# Contributing to GenX FX

First off, thank you for considering contributing to GenX FX! It's people like you that make this project a powerful and reliable trading platform.

This document provides guidelines for contributing to the project. Please feel free to propose changes to this document in a pull request.

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please open an issue on our [GitHub Issues](https://github.com/Mouy-leng/GenX_FX/issues) page.

When filing a bug report, please include:
- A clear and descriptive title.
- A detailed description of the problem, including steps to reproduce it.
- Your system information (OS, Python version, etc.).
- Any relevant logs or screenshots.

### Suggesting Enhancements
If you have an idea for a new feature or an improvement to an existing one, please open an issue on our [GitHub Issues](https://github.com/Mouy-leng/GenX_FX/issues) page.

Provide a clear and detailed explanation of the feature, its potential benefits, and any implementation ideas you might have.

### Pull Requests
We welcome pull requests for bug fixes and new features. Before you start working on a major change, it's best to discuss it in an issue first.

## Development Setup

Please refer to the `README.md` for instructions on how to set up your development environment. The `AGENT.md` file also contains valuable information about the project's architecture and build commands.

## Branching Strategy

To keep our repository history clean and organized, we follow this branching strategy:

- **`main`**: This is the primary branch, representing the latest stable release. All pull requests should be merged into `main`.
- **Feature Branches**: All new features and bug fixes should be developed in a separate feature branch.
  - Branch names should be descriptive and prefixed with `feat/` for new features or `fix/` for bug fixes (e.g., `feat/new-indicator` or `fix/api-endpoint-bug`).
  - Create your branch from the latest `main` branch.

**Example:**
```bash
# Get the latest code
git checkout main
git pull origin main

# Create your feature branch
git checkout -b feat/my-amazing-feature
```

## Pull Request Process

1.  **Fork the repository** and create your branch from `main`.
2.  **Make your changes** and commit them with a clear and descriptive message.
3.  **Ensure your code lints and tests pass.** Refer to `AGENT.md` for the correct commands (`npm run lint`, `npm test`, `python run_tests.py`).
4.  **Push your changes** to your forked repository.
5.  **Open a pull request** to the `main` branch of the `GenX_FX` repository.
6.  **Provide a clear title and description** for your pull request, explaining the "what" and "why" of your changes. Link to any relevant issues.
7.  **Wait for a review.** One of the project maintainers will review your pull request and may ask for changes.

### Squash and Merge
All pull requests will be merged using the **Squash and Merge** method on GitHub. This keeps the `main` branch history clean and easy to follow. Please ensure your PR title and description are well-written, as they will become the commit message.

## Coding Style

Please follow the coding style guidelines outlined in the `AGENT.md` file:
- **Python**: PEP 8
- **TypeScript/JavaScript**: As defined by our ESLint configuration.
- **Naming Conventions**: `snake_case` for Python, `camelCase` for JS/TS.

Thank you for your contribution!