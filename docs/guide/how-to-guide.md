# How to guide

Here you’ll find answers to “How do I….?” types of questions. These guides are goal-oriented and concrete; they're meant to help you complete a specific task.

- [How to config custom language model](/other/how-to-config-model)

- [How to config custom commit message template](/guide/configuration.html#commit-message-template)

- [How to connect to Gaianet](/other/connect2gaianet)

- [How to contribute to GCOP](/other/contributing)

## FAQ

### How does GCOP work?

GCOP integrates with your existing Git workflow and uses advanced language models to analyze your code changes and generate appropriate commit messages. It also provides AI-assisted features for other Git operations.

### Is GCOP free to use?

GCOP is an open-source project and is free to use. However, some advanced features may require access to paid language model APIs.

### Why doesn't GCOP work after switching Python environments?

When you switch Python environments (e.g., using conda), you might find that GCOP no longer works. This is because:

- GCOP uses the current Python environment where it's installed.
- If you switch to a different conda environment, you'll need to reinstall GCOP in that environment using `pip install gcop`.
- However, you don't need to run `gcop init` again to reconfigure GCOP. Different Python environments share the same GCOP configuration.

Remember:

1. Install GCOP in each Python environment you want to use it in.
2. The GCOP configuration is shared across all environments, so you only need to set it up once.

### How to see the logs?

GCOP will store the logs in the `logs` folder in the GCOP storage path, which is usually `~/.zeeland/gcop/logs/`.
