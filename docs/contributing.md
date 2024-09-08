# Contributing to GCOP

We welcome contributions to GCOP! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/gcop.git
   cd gcop
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   conda create -n gcop python==3.10
   conda activate gcop
   pip install poetry
   poetry install
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-or-fix-name
   ```
2. Make your changes and commit them:
   ```bash
   git commit -am "Your detailed commit message"
   ```
3. Push your changes to your fork:
   ```bash
   git push origin feature-or-fix-name
   ```
4. Submit a pull request through the GitHub website.

## Coding Standards

- We use `ruff` for code formatting. Run `make polish-codestyle` before committing.
- Write clear, commented code.
- Include unit tests for new features.

## Running Tests

Run the test suite using: