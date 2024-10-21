# Quick Start Guide

This guide will help you get started with GCOP (Git Copilot) quickly and easily.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or newer
- Git installed on your system
- An API key for your preferred LLM (e.g., OpenAI, Anthropic)

## Installation

1. Install GCOP using pip:

   ```
   pip install gcop
   ```

2. Initialize GCOP:

   ```
   gcop init
   ```

   This command sets up GCOP and adds its aliases to your Git configuration.

3. Configure your AI model:

   ```
   git gconfig
   ```

   This opens the configuration file. Edit it to include your AI provider details:

   ```yaml
   model:
     model_name: provider/name, eg openai/gpt-4o
     api_key: your_api_key
   ```

   How to config your model? Please refer to [How to Config Model](../how-to-config-model.md)

   The `config.yaml` file will be stored in:
   - Windows: `%USERPROFILE%\.gcop\config.yaml`
   - Linux: `~/.gcop/config.yaml`
   - MacOS: `~/.gcop/config.yaml`

4. Verify the installation:

   ```
   git ghelp
   ```

   You should see a list of available GCOP commands.

## Basic Usage

### Generating AI Commit Messages

1. Stage your changes:

   ```
   git add .
   ```

2. Generate and apply an AI commit message:

   ```
   git c
   ```

3. Choose the most appropriate message using arrow keys and press Enter.

### Other Useful Commands

- `git ac`: Add all changes and commit with an AI-generated message
- `git p`: Push changes to the remote repository
- `git undo`: Undo the last commit while keeping changes staged
- `git gconfig`: Open the GCOP configuration file for adjustments

For more detailed information on each command, refer to the [Commands](./commands.md) section.

## Next Steps

- Explore the [Introduction](./introduction.md) for an overview of GCOP's features
- Check out the [How to Config Model](../how-to-config-model.md) guide for advanced configuration options
- Visit our [FAQ](../faq.md) for common questions and troubleshooting

Start enhancing your Git workflow with GCOP today!
