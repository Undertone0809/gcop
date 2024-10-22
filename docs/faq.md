# Frequently Asked Questions

## General Questions

### What is GCOP?

GCOP (Git COpilot) is an AI-powered tool designed to enhance your Git workflow by automatically generating meaningful commit messages and providing intelligent assistance for various Git operations.

### How does GCOP work?

GCOP integrates with your existing Git workflow and uses advanced language models to analyze your code changes and generate appropriate commit messages. It also provides AI-assisted features for other Git operations.

### Is GCOP free to use?

GCOP is an open-source project and is free to use. However, some advanced features may require access to paid language model APIs.

### How to config my model?

Please refer to [How to Config Model](./how-to-config-model.md)

### Why doesn't GCOP work after switching Python environments?

When you switch Python environments (e.g., using conda), you might find that GCOP no longer works. This is because:

- GCOP uses the current Python environment where it's installed.
- If you switch to a different conda environment, you'll need to reinstall GCOP in that environment using `pip install gcop`.
- However, you don't need to run `gcop init` again to reconfigure GCOP. Different Python environments share the same GCOP configuration.

Remember:

1. Install GCOP in each Python environment you want to use it in.
2. The GCOP configuration is shared across all environments, so you only need to set it up once.
