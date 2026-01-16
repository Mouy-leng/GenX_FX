# Contributing to GenX_FX

First off, thank you for considering contributing to GenX_FX. Whether you're fixing a bug, adding a new feature, or improving the documentation, your contributions are welcome.

## Getting Started

Before you begin, please make sure you have the following installed:

*   [Node.js](https://nodejs.org/) (LTS version)
*   [Python](https://www.python.org/) (3.8 or higher)
*   [Docker](https://www.docker.com/)

To get the development environment running, please follow the instructions in the [REPOSITORY_LAUNCH_GUIDE.md](REPOSITORY_LAUNCH_GUIDE.md).

## Branching Strategy

We use a simple branching strategy based on the following prefixes:

*   `feature/`: For new features (e.g., `feature/add-new-expert-advisor`)
*   `bugfix/`: For bug fixes (e.g., `bugfix/fix-mt5-connection-issue`)
*   `docs/`: For documentation changes (e.g., `docs/update-readme`)
*   `chore/`: For routine maintenance and other tasks (e.g., `chore/update-dependencies`)

Please make sure your branch names are descriptive and concise.

## Code Style

We use [Prettier](https://prettier.io/) to maintain a consistent code style across the project. Before you commit your changes, please run the following command to format your code:

```bash
npm run format
```

## Pull Request Process

1.  **Fork the repository** and create your branch from `main`.
2.  **Make your changes** and ensure that all tests pass.
3.  **Open a pull request** with a clear and descriptive title.
4.  **In the pull request description**, please include the following:
    *   A summary of the changes you've made.
    *   Any relevant screenshots or GIFs.
    *   A link to any related issues.

Once you've opened a pull request, a member of the team will review your changes and provide feedback. Please be patient and responsive to any comments or questions.
